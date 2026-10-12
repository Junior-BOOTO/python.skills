from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import urllib.request,json,hashlib
ROOT=Path(__file__).resolve().parent
def main():
    spec=json.loads((ROOT/'sources.json').read_text())
    (ROOT/'raw').mkdir(exist_ok=True)
    def download(item):
        path=ROOT/'raw'/item['name']
        if not path.exists():
            urllib.request.urlretrieve(item['url'],path)
        actual=hashlib.sha1(b'blob '+str(path.stat().st_size).encode()+b'\0'+path.read_bytes()).hexdigest()
        assert actual==item['sha'], f"Empreinte invalide : {item['name']}"
        return {'file':item['name'],'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'size':path.stat().st_size}
    with ThreadPoolExecutor(max_workers=4) as pool:
        result=list(pool.map(download,spec['files']))
    (ROOT/'reports'/'empreintes_sources.json').write_text(json.dumps(result,indent=2))
    print('Sources collectées et empreintes Git vérifiées :',len(result))
if __name__=='__main__':main()
