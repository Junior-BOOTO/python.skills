import argparse,json,sys,datetime
from pathlib import Path
from .core import compare
from .collect import collect
from .render import export

def main():
 parser=argparse.ArgumentParser(description='Explain transfer-cost scenarios at equal total budgets')
 sub=parser.add_subparsers(dest='command',required=True)
 p=sub.add_parser('compare');p.add_argument('--config',default='data/scenarios.json');p.add_argument('--rates',default='data/rates-synthetic.json');p.add_argument('--as-of',default=datetime.date.today().isoformat());p.add_argument('--output',default='reports')
 p=sub.add_parser('collect');p.add_argument('--base',default='USD');p.add_argument('--quotes',nargs='+',default=['COP','CDF','ZAR']);p.add_argument('--output',default='data/live')
 args=parser.parse_args()
 try:
  if args.command=='compare':
   read=lambda p:json.loads(Path(p).read_text(encoding='utf-8'));result=compare(read(args.config),read(args.rates),args.as_of);export(result,args.output);print(json.dumps(result['summary'],indent=2))
  else:
   rates,raw=collect(args.base,args.quotes);out=Path(args.output);out.mkdir(parents=True,exist_ok=True);(out/'rates-reference.json').write_text(json.dumps(rates,indent=2));(out/'response.json').write_bytes(raw);print('Missing pairs: '+', '.join(rates['missing_quotes']))
  return 0
 except (OSError,ValueError,KeyError,TypeError):print('Transfer Observatory: collection or input validation failed; no live rates assumed',file=sys.stderr);return 2

if __name__=='__main__':sys.exit(main())
