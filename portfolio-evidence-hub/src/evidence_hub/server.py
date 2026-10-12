"""Local read-only HTTP API; binds only to loopback."""
from http.server import BaseHTTPRequestHandler,HTTPServer
import json
from urllib.parse import urlsplit
from .render import render


def handler(report):
    class Handler(BaseHTTPRequestHandler):
        def log_message(self,*args):pass
        def do_GET(self):
            route=urlsplit(self.path).path
            if route=='/': body=render(report).encode();kind='text/html; charset=utf-8'
            elif route=='/api/report':body=json.dumps(report,ensure_ascii=False).encode();kind='application/json; charset=utf-8'
            elif route=='/api/projects':body=json.dumps([{'id':p['id'],'title':p['title']} for p in report['projects']]).encode();kind='application/json; charset=utf-8'
            elif route.startswith('/api/projects/'):
                project=next((p for p in report['projects'] if p['id']==route.rsplit('/',1)[-1]),None)
                if project is None:self.send_error(404);return
                body=json.dumps(project,ensure_ascii=False).encode();kind='application/json; charset=utf-8'
            else:self.send_error(404);return
            self.send_response(200);self.send_header('Content-Type',kind);self.send_header('Content-Length',str(len(body)));self.send_header('X-Content-Type-Options','nosniff');self.end_headers();self.wfile.write(body)
        def do_POST(self):self.send_error(405,'Read-only API')
        do_PUT=do_DELETE=do_POST
    return Handler


def serve(report,port=8765):
    HTTPServer(('127.0.0.1',port),handler(report)).serve_forever()
