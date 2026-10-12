from decimal import Decimal,ROUND_DOWN,ROUND_HALF_UP,localcontext
from datetime import date
import re


def number(value,label):
 if not isinstance(value,(str,Decimal)):raise ValueError(label+' must be an exact decimal string')
 try:v=Decimal(value)
 except Exception:raise ValueError('Invalid decimal: '+label) from None
 if not v.is_finite() or v<0 or v>Decimal('1000000000000'):raise ValueError('Invalid range: '+label)
 return v


def currency(value):
 if not isinstance(value,str) or not re.fullmatch('[A-Z]{3}',value):raise ValueError('Currency must be a three-letter uppercase code')
 return value


def quote(budget,rate,tariff,source_minor=2,target_minor=2):
 """Fixed total budget; source percentage fee applies to principal, not budget."""
 with localcontext() as context:
  context.prec=40
  if not isinstance(source_minor,int) or not isinstance(target_minor,int) or not 0<=source_minor<=4 or not 0<=target_minor<=4:raise ValueError('Precision must be 0–4 decimal places')
  budget=number(budget,'budget');rate=number(rate,'reference rate')
  if not budget or not rate:raise ValueError('Budget and rate must be positive')
  source_unit=Decimal(1).scaleb(-source_minor);target_unit=Decimal(1).scaleb(-target_minor)
  if budget!=budget.quantize(source_unit):raise ValueError('Budget has more decimals than the configured precision')
  fixed=number(tariff['sender_fixed'],'sender fixed fee');percent=number(tariff['sender_percent'],'sender percentage fee')/100
  margin=number(tariff['fx_margin_percent'],'FX margin')/100;receiver=number(tariff['receiver_fixed'],'receiver fee')
  if percent>1 or margin>=1:raise ValueError('Invalid fee or margin percentage')
  if fixed!=fixed.quantize(source_unit) or receiver!=receiver.quantize(target_unit):raise ValueError('Fixed fee precision exceeds currency configuration')
  if budget<=fixed:raise ValueError('Budget does not cover fixed sender fee')
  principal=((budget-fixed)/(1+percent)).quantize(source_unit,rounding=ROUND_DOWN)
  if principal<=0:raise ValueError('No principal remains')
  variable=(principal*percent).quantize(source_unit,rounding=ROUND_HALF_UP)
  spent=principal+fixed+variable
  if spent>budget:raise ValueError('Rounding exceeds total budget')
  effective=rate*(1-margin)
  gross=principal*effective
  received=(gross-receiver).quantize(target_unit,rounding=ROUND_HALF_UP)
  if received<=0:raise ValueError('Receiver fee consumes payout')
  ideal=budget*rate
  loss=ideal-received
  return {k:str(v) for k,v in {'budget':budget,'principal':principal,'sender_fixed':fixed,'sender_variable':variable,'spent':spent,'unspent':budget-spent,'reference_rate':rate,'effective_rate':effective,'gross_before_receiver_fee':gross,'receiver_fixed':receiver,'received':received,'effective_received_per_budget':received/budget,'reference_no_fee_amount':ideal,'reference_gap_target':loss,'reference_gap_percent':loss/ideal*100,'source_fee_effect_target':(fixed+variable)*rate,'unspent_effect_target':(budget-spent)*rate,'fx_margin_effect_target':principal*rate*margin,'rounding_effect_target':gross-receiver-received}.items()}


def validate_config(config):
 if config.get('schema_version')!=1:raise ValueError('Unsupported scenario schema')
 if not isinstance(config['max_reference_age_days'],int) or config['max_reference_age_days']<0:raise ValueError('Invalid reference age limit')
 ids=set()
 for corridor in config['corridors']:
  if corridor['id'] in ids or not re.fullmatch(r'[a-z0-9-]+',corridor['id']):raise ValueError('Invalid or duplicate corridor id')
  ids.add(corridor['id']);currency(corridor['source']);currency(corridor['target'])
  if corridor['source']==corridor['target']:raise ValueError('Different currencies required')
  if corridor['source_minor'] not in range(5) or corridor['target_minor'] not in range(5):raise ValueError('Unsupported precision')
  for budget in corridor['budgets']:
   if number(budget,'budget')<=0:raise ValueError('Positive budgets required')
  tariff_ids=set()
  for t in corridor['tariffs']:
   if not isinstance(t['id'],str) or not re.fullmatch(r'[A-Za-z0-9_-]+',t['id']) or t['id'] in tariff_ids:raise ValueError('Invalid or duplicate tariff id')
   tariff_ids.add(t['id'])
   if t['data_kind']!='synthetic':raise ValueError('MVP accepts synthetic tariff profiles only')
   for k in ('sender_fixed','sender_percent','fx_margin_percent','receiver_fixed'):number(t[k],k)
 return config


def validate_rates(rates):
 if rates.get('schema_version')!=1:raise ValueError('Unsupported rate schema')
 pairs=set()
 for r in rates['rates']:
  pair=(currency(r['base']),currency(r['quote']))
  if pair in pairs:raise ValueError('Duplicate reference pair')
  pairs.add(pair)
  if number(r['rate'],'rate')<=0:raise ValueError('Positive rate required')
  date.fromisoformat(r['date'])
  if r['data_kind'] not in ('synthetic','public_reference'):raise ValueError('Unknown rate provenance')
 return rates


def compare(config,rates,as_of):
 validate_config(config);validate_rates(rates);today=date.fromisoformat(as_of)
 result={'schema_version':1,'as_of':as_of,'tariff_kind':'synthetic','corridors':[],'limitations':['No real transfer-provider tariffs','Reference rates are not executable transfer quotes','No transfer initiated','No ranking across currencies or different budgets']}
 for corridor in config['corridors']:
  ref=next((r for r in rates['rates'] if (r['base'],r['quote'])==(corridor['source'],corridor['target'])),None)
  item={'id':corridor['id'],'source':corridor['source'],'target':corridor['target'],'reference':ref,'comparisons':[]}
  if ref is None:item['status']='reference_missing';result['corridors'].append(item);continue
  age=(today-date.fromisoformat(ref['date'])).days
  if age<0:raise ValueError('Reference date is in the future')
  item.update(status='available',reference_age_days=age,reference_stale=age>config['max_reference_age_days'])
  for budget in corridor['budgets']:
   rows=[]
   for tariff in corridor['tariffs']:
    try:
     calculation=quote(budget,ref['rate'],tariff,corridor['source_minor'],corridor['target_minor'])
     rows.append({'profile':tariff['id'],'label':tariff['label'],'status':'calculated','calculation':calculation})
    except ValueError as exc:rows.append({'profile':tariff['id'],'label':tariff['label'],'status':'infeasible','reason':str(exc)})
   valid=sorted((r for r in rows if r['status']=='calculated'),key=lambda r:(-Decimal(r['calculation']['received']),r['profile']))
   for row in valid:row['rank']=1+sum(Decimal(other['calculation']['received'])>Decimal(row['calculation']['received']) for other in valid)
   item['comparisons'].append({'budget':budget,'ranked':valid,'infeasible':[r for r in rows if r['status']=='infeasible'],'best_profiles':[r['profile'] for r in valid if r['rank']==1]})
  result['corridors'].append(item)
 result['summary']={'corridors':len(result['corridors']),'calculated_quotes':sum(len(c['ranked']) for p in result['corridors'] for c in p['comparisons']),'infeasible_quotes':sum(len(c['infeasible']) for p in result['corridors'] for c in p['comparisons']),'reference_missing':sum(p['status']=='reference_missing' for p in result['corridors'])}
 return result
