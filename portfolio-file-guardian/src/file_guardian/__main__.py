import argparse
import json
import sys
from pathlib import Path
from .core import scan, export_report, organize, restore


def main():
    parser = argparse.ArgumentParser(description='Inventory and copy-only organization; simulation by default.')
    subs = parser.add_subparsers(dest='command', required=True)
    audit = subs.add_parser('scan', help='Read-only inventory; report output is optional')
    audit.add_argument('source', type=Path)
    audit.add_argument('--output', type=Path)
    audit.add_argument('--categories', type=Path)
    copy = subs.add_parser('organize', help='Preview or explicitly copy into a new directory')
    copy.add_argument('source', type=Path)
    copy.add_argument('destination', type=Path)
    copy.add_argument('--execute', action='store_true')
    copy.add_argument('--categories', type=Path)
    undo = subs.add_parser('restore', help='Preview removal of unchanged journaled copies')
    undo.add_argument('destination', type=Path)
    undo.add_argument('--execute', action='store_true')
    args = parser.parse_args()
    try:
        categories = json.loads(args.categories.read_text(encoding='utf-8')) if getattr(args, 'categories', None) else None
        if args.command == 'scan':
            result = scan(args.source, categories)
            if args.output:
                out, source = args.output.resolve(), args.source.resolve()
                if out.is_relative_to(source) or source.is_relative_to(out):
                    raise ValueError('Report directory must be disjoint from source')
                export_report(result, args.output)
        elif args.command == 'organize':
            result = organize(args.source, args.destination, categories) if args.execute else scan(args.source, categories)
        else:
            result = restore(args.destination, args.execute)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 2 if result.get('errors') else 0
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f'Guardian: {exc}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
