import json
from http.server import BaseHTTPRequestHandler,HTTPServer
from urllib.parse import urlsplit,parse_qs
from .core import build_kit
from .render import render_studio

def handler(catalog):
 class Handler(BaseHTTPRequestHandler):
  def log_message(self,*args):pass
  def do_GET(self):
   parsed=urlsplit(self.path);route=parsed.path;query=parse_qs(parsed.query)
   try:
    if route=='/':body=render_studio(catalog).encode();kind='text/html; charset=utf-8'
    elif route=='/api/catalog':body=json.dumps(catalog,ensure_ascii=False).encode();kind='application/json; charset=utf-8'
    elif route.startswith('/api/kits/'):
     kit=build_kit(catalog,route.rsplit('/',1)[-1],level=query.get('level',['A1'])[0],support=query.get('support',['model'])[0],language=query.get('language',['es'])[0]);body=json.dumps(kit,ensure_ascii=False).encode();kind='application/json; charset=utf-8'
    else:self.send_error(404);return
   except ValueError:self.send_error(400,'Invalid kit options');return
   self.send_response(200);self.send_header('Content-Type',kind);self.send_header('Content-Length',str(len(body)));self.send_header('X-Content-Type-Options','nosniff');self.end_headers();self.wfile.write(body)
  def do_POST(self):self.send_error(405,'Read-only API')
  do_PUT=do_DELETE=do_POST
 return Handler

def serve(catalog,port=8766):HTTPServer(('127.0.0.1',port),handler(catalog)).serve_forever()
