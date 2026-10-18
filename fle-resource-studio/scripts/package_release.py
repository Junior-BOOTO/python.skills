"""Build and smoke-test a portable source archive using the standard library."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parents[1]
VERSION = '1.0.0'
PREFIX = f'fle-resource-studio-{VERSION}'

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', default='dist')
    args = parser.parse_args()
    output = Path(args.output).resolve()
    if output == ROOT or ROOT in output.parents:
        parser.error('Output must be outside the project to avoid packaging generated archives.')
    output.mkdir(parents=True, exist_ok=True)
    archive = output / f'{PREFIX}.zip'
    entries = []
    with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED) as z:
        for path in sorted(ROOT.rglob('*')):
            relative = path.relative_to(ROOT)
            if any(part in {'.git', '.venv', '__pycache__', '.pytest_cache', '.DS_Store'} for part in relative.parts):
                continue
            if path.is_symlink():
                raise ValueError(f'Symlink not supported: {relative}')
            if not path.is_file() or path.suffix in {'.pyc', '.pyo'}:
                continue
            data = path.read_bytes()
            z.writestr(f'{PREFIX}/{relative.as_posix()}', data)
            entries.append({'path': relative.as_posix(), 'sha256': hashlib.sha256(data).hexdigest()})
    with tempfile.TemporaryDirectory() as temp:
        with zipfile.ZipFile(archive) as z:
            assert z.testzip() is None, 'Invalid archive CRC'
            z.extractall(temp)
        unpacked = Path(temp) / PREFIX
        for entry in entries:
            assert hashlib.sha256((unpacked / entry['path']).read_bytes()).hexdigest() == entry['sha256']
        env = dict(os.environ, PYTHONPATH=str(unpacked / 'src'))
        commands = [
            ['-m', 'unittest', 'discover', '-s', 'tests', '-v'],
            ['-m', 'fle_studio', 'studio', '--output', str(Path(temp) / 'studio.html')],
            ['-m', 'fle_studio', 'build', 'meubles', '--support', 'guided', '--language', 'es', '--output', str(Path(temp) / 'kits')],
        ]
        checks = []
        for command in commands:
            result = subprocess.run([sys.executable, *command], cwd=unpacked, env=env, capture_output=True, text=True, timeout=60)
            checks.append({'command': 'python ' + ' '.join(command[:5]), 'returncode': result.returncode, 'log': result.stdout + result.stderr})
            if result.returncode:
                raise RuntimeError(checks[-1]['log'])
        assert (Path(temp) / 'studio.html').is_file()
        assert (Path(temp) / 'kits/meubles/kit.html').is_file()
    checksum = hashlib.sha256(archive.read_bytes()).hexdigest()
    (output / 'SHA256SUMS.txt').write_text(f'{checksum}  {archive.name}\n', encoding='utf-8')
    (output / 'release-validation.json').write_text(json.dumps({'version': VERSION, 'python': sys.version, 'archive': archive.name, 'file_count': len(entries), 'sha256': checksum, 'files': entries, 'checks': checks, 'visual_browser_test': 'not performed', 'classroom_validation': 'not performed'}, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({'archive': str(archive), 'files': len(entries), 'checks_passed': len(checks)}))

if __name__ == '__main__':
    main()
