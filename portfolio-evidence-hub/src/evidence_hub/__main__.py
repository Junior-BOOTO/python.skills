import argparse,json,sys
from pathlib import Path
from .audit import audit,compare_local
from .collect import collect
from .render import export
from .server import serve


def main():
    parser=argparse.ArgumentParser(description='Read-only evidence-based portfolio audit')
    subs=parser.add_subparsers(dest='command',required=True)
    p=subs.add_parser('collect');p.add_argument('--config',default='projects.json');p.add_argument('--output',default='data/live')
    p=subs.add_parser('audit');p.add_argument('--config',default='projects.json');p.add_argument('--snapshot',default='data/github-snapshot.json');p.add_argument('--sites',default='data/site-observations.json');p.add_argument('--output',default='reports');p.add_argument('--local-snapshot',help='Replay dated local observations without rescanning files');p.add_argument('--local',action='append',default=[],help='project-id=/absolute/local/root')
    p=subs.add_parser('serve');p.add_argument('--report',default='reports/audit.json');p.add_argument('--port',type=int,default=8765)
    args=parser.parse_args()
    def read(path):return json.loads(Path(path).read_text(encoding='utf-8'))
    try:
        if args.command=='collect':
            snapshot,sites=collect(read(args.config));out=Path(args.output);out.mkdir(parents=True,exist_ok=True)
            (out/'github-snapshot.json').write_text(json.dumps(snapshot,ensure_ascii=False,indent=2),encoding='utf-8');(out/'site-observations.json').write_text(json.dumps(sites,ensure_ascii=False,indent=2),encoding='utf-8')
            print('Snapshot saved at '+snapshot['commit']);return 0
        if args.command=='serve':
            print(f'Local read-only API: http://127.0.0.1:{args.port}',flush=True);serve(read(args.report),args.port);return 0
        config,snapshot,sites=read(args.config),read(args.snapshot),read(args.sites);local=read(args.local_snapshot) if args.local_snapshot else {}
        for item in args.local:
            key,path=item.split('=',1);p=next(p for p in config['projects'] if p['id']==key);local[key]=compare_local(Path(path),p['path'],snapshot['files'],snapshot.get('documents'))
        report=audit(config,snapshot,sites,local);export(report,args.output);print(json.dumps(report['summary'],ensure_ascii=False,indent=2));return 0
    except (OSError,ValueError,KeyError,TypeError,StopIteration) as exc:
        print('Evidence Hub: '+type(exc).__name__+': '+str(exc),file=sys.stderr);return 2

if __name__=='__main__':sys.exit(main())
