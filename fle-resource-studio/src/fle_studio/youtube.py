"""Optional metadata retrieval, never automatic pedagogical approval."""
import json,os,re,urllib.parse,urllib.request,urllib.error

def metadata(video_ids):
 if not video_ids or len(video_ids)>50 or any(not re.fullmatch(r'[A-Za-z0-9_-]{11}',v) for v in video_ids):raise ValueError('Supply 1–50 valid video IDs')
 key=os.environ.get('YOUTUBE_API_KEY')
 if not key:raise ValueError('Set YOUTUBE_API_KEY in the secure environment; no key in chat or source')
 query=urllib.parse.urlencode({'part':'snippet,contentDetails,status','id':','.join(video_ids),'key':key})
 try:
  with urllib.request.urlopen('https://www.googleapis.com/youtube/v3/videos?'+query,timeout=15) as r:
   body=r.read(2_000_001)
   if len(body)>2_000_000:raise ValueError('Response too large')
   data=json.loads(body)
 except urllib.error.HTTPError as exc:raise RuntimeError('YouTube API HTTP '+str(exc.code)) from None
 except (OSError,ValueError):raise RuntimeError('YouTube metadata request failed') from None
 if not isinstance(data,dict) or not isinstance(data.get('items'),list):raise ValueError('Invalid YouTube response')
 result=[]
 for item in data['items']:
  if item.get('id') not in video_ids:raise ValueError('Unexpected video ID')
  result.append({'id':item['id'],'title':item.get('snippet',{}).get('title'),'channel':item.get('snippet',{}).get('channelTitle'),'duration_iso8601':item.get('contentDetails',{}).get('duration'),'embeddable':item.get('status',{}).get('embeddable'),'review_status':'pending','note':'API metadata only; no claim of pedagogical suitability'})
 return {'items':result,'unreturned_ids':sorted(set(video_ids)-{i['id'] for i in result}),'pedagogical_approval':False}
