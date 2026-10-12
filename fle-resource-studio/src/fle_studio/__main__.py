import argparse,json,sys
from pathlib import Path
from .core import build_kit,export_kit,validate_catalog
from .render import render_studio
from .server import serve
from .youtube import metadata

def main():
 parser=argparse.ArgumentParser(description='FLE A1 resource studio: explicit glossary and differentiated kits')
 parser.add_argument('--catalog',default='data/catalog.json')
 sub=parser.add_subparsers(dest='command',required=True)
 p=sub.add_parser('build');p.add_argument('theme');p.add_argument('--level',default='A1');p.add_argument('--support',default='model');p.add_argument('--language',default='es');p.add_argument('--output',default='kits')
 p=sub.add_parser('studio');p.add_argument('--output',default='reports/studio.html')
 p=sub.add_parser('serve');p.add_argument('--port',type=int,default=8766)
 p=sub.add_parser('youtube');p.add_argument('ids',nargs='+');p.add_argument('--output',default='reports/youtube-metadata.json')
 args=parser.parse_args()
 try:
  catalog=validate_catalog(json.loads(Path(args.catalog).read_text(encoding='utf-8')))
  if args.command=='build':print(export_kit(build_kit(catalog,args.theme,args.level,args.support,args.language),args.output))
  elif args.command=='studio':p=Path(args.output);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(render_studio(catalog),encoding='utf-8');print(p)
  elif args.command=='serve':print(f'Local studio: http://127.0.0.1:{args.port}',flush=True);serve(catalog,args.port)
  else:p=Path(args.output);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(metadata(args.ids),ensure_ascii=False,indent=2),encoding='utf-8');print(p)
  return 0
 except (ValueError,OSError,KeyError,TypeError,RuntimeError) as exc:print('FLE Studio: '+str(exc),file=sys.stderr);return 2

if __name__=='__main__':sys.exit(main())
