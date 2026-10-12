import datetime,json,urllib.parse,urllib.request
from .core import currency,number

def parse_response(rows,base,quotes,source_url,collected_at):
 if not isinstance(rows,list):raise ValueError('Expected a v2 rates array')
 result=[];seen=set()
 for row in rows:
  if not isinstance(row,dict) or row.get('base')!=base or row.get('quote') not in quotes:raise ValueError('Unexpected currency pair')
  if row['quote'] in seen:raise ValueError('Duplicate currency rate')
  seen.add(row['quote']);rate=number(str(row['rate']),'reference rate')
  if rate<=0:raise ValueError('Rate must be positive')
  datetime.date.fromisoformat(row['date'])
  result.append({'base':base,'quote':row['quote'],'rate':str(rate),'date':row['date'],'data_kind':'public_reference','provider':'Frankfurter v2 default blend','source_url':source_url,'collected_at':collected_at})
 return {'schema_version':1,'rates':result,'missing_quotes':sorted(set(quotes)-seen),'reference_only':True}

def collect(base='USD',quotes=('COP','CDF','ZAR')):
 currency(base)
 for q in quotes:currency(q)
 url='https://api.frankfurter.dev/v2/rates?'+urllib.parse.urlencode({'base':base,'quotes':','.join(quotes)})
 with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Transfer-Cost-Observatory/1.0'}),timeout=20) as response:
  body=response.read(2_000_001)
  if len(body)>2_000_000:raise ValueError('Rate response exceeds size limit')
 from decimal import Decimal
 rows=json.loads(body,parse_float=Decimal)
 return parse_response(rows,base,quotes,url,datetime.datetime.now(datetime.timezone.utc).isoformat()),body
