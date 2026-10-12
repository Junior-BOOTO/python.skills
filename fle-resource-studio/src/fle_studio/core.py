import copy
import json
import re
from pathlib import Path
from urllib.parse import urlsplit,parse_qs

SUPPORTS={
 'guided':'Appui renforcé : trois cartes présélectionnées, article/structure mis en couleur par l’enseignant, répétition orale et choix guidés. Produire les trois phrases avec les modèles visibles.',
 'model':'Avec modèle : banque de mots et débuts de phrases. Choisir trois éléments et compléter les phrases, puis les dire à un partenaire.',
 'independent':'Autonomie : choisir trois éléments, produire les phrases sans modèle pendant la présentation, puis ajouter une question au partenaire. Le glossaire reste disponible pour préparer.'}


def validate_catalog(catalog):
 if catalog.get('schema_version')!=1:raise ValueError('Unsupported catalog schema')
 ids=set()
 for theme in catalog['themes']:
  if not re.fullmatch(r'[a-z][a-z0-9-]*',theme['id']) or theme['id'] in ids:raise ValueError('Invalid or duplicate theme id')
  ids.add(theme['id'])
  if theme['level']!='A1' or len(theme['models'])!=3 or not theme['lexicon']:raise ValueError('A1 content and three models required')
  word_ids=set()
  for word in theme['lexicon']:
   if word['id'] in word_ids or any(not isinstance(word.get(k),str) or not word[k].strip() for k in ('fr','es','en')):raise ValueError('Invalid glossary entry')
   word_ids.add(word['id'])
  for video in theme['videos']:
   if not re.fullmatch(r'[A-Za-z0-9_-]{11}',video['id']):raise ValueError('Invalid YouTube id')
   url=urlsplit(video['url'])
   if url.scheme!='https' or url.hostname!='www.youtube.com' or url.path!='/watch' or parse_qs(url.query).get('v')!=[video['id']]:raise ValueError('Invalid video URL')
 return catalog


def approved_videos(theme):
 return [copy.deepcopy(v) for v in theme['videos'] if v.get('review_status')=='approved' and v.get('reviewer') and v.get('reviewed_at') and all(v.get('checks',{}).get(k) is True for k in ('age_appropriate','language_accessible','matches_objective','usable_segment'))]


def build_kit(catalog,theme_id,level='A1',support='model',language='es'):
 validate_catalog(catalog)
 if level!='A1':raise ValueError('Only A1 is implemented; no automatic A2 adaptation')
 if support not in SUPPORTS:raise ValueError('Unknown support mode')
 if language not in ('fr','es','en'):raise ValueError('Unknown aid language')
 theme=next((t for t in catalog['themes'] if t['id']==theme_id),None)
 if not theme:raise ValueError('Unknown theme')
 civic=theme_id=='ecocitoyen'
 criteria=[{'id':'recognize','text':'Je peux reconnaître au moins 3 expressions du thème.','evidence':'Associer oralement trois expressions à leur sens ou à un dessin explicite.','threshold':'3 correspondances correctes sur 3'},
 {'id':'produce','text':'Je peux dire un droit et deux devoirs en français.' if civic else 'Je peux dire 3 phrases simples sur le thème.','evidence':'Présentation individuelle au partenaire, puis observation par l’enseignant.','threshold':'3 phrases compréhensibles : un droit + deux devoirs.' if civic else '3 phrases compréhensibles.'},
 {'id':'structure','text':'Je peux utiliser « J’ai le droit de… » et « Je dois… ».' if civic else 'Je peux utiliser le modèle de phrase du thème.','evidence':'Observation de la structure travaillée, avec aides selon le parcours.','threshold':'Structure correcte dans au moins 2 phrases sur 3.'}]
 stages=[{'name':'Ouverture','minutes':8,'grouping':'classe entière','instructions':'Afficher trois expressions ou objets/dessins du thème. Faire nommer ce qui est déjà connu, autoriser une réponse initiale en espagnol, puis reformuler en français. Annoncer explicitement le lien avec le thème et la tâche finale.'},
 {'name':'Activité principale','minutes':29,'grouping':'binômes, puis production individuelle','instructions':'Les élèves vont écouter les trois modèles lus par l’enseignant (8 min), associer le lexique à des objets ou dessins (7 min), préparer trois phrases avec leur aide choisie (7 min), puis les présenter à leur partenaire (7 min). Pour les droits et devoirs : choisir un droit et deux devoirs. Le partenaire écoute et demande une répétition si nécessaire.'},
 {'name':'Clôture','minutes':8,'grouping':'production individuelle puis classe entière','instructions':'Chaque élève associe trois expressions à leur sens, puis dit ses trois phrases. L’enseignant utilise les trois critères et note atteint / en cours / non observé, ainsi que l’aide utilisée. Conserver la production écrite ou une trace de l’observation dans le portfolio ; aucun enregistrement audio d’élève nécessaire.'}]
 exercise={'prompt':'Retrouve le sens de ces trois expressions. Écris la bonne lettre.', 'items':[{'id':w['id'],'fr':w['fr']} for w in theme['lexicon'][:3]],'choices':[{'letter':letter,'text':w[language] if language!='fr' else w['fr']} for letter,w in zip(('A','B','C'),reversed(theme['lexicon'][:3]))],'answers':{'1':'C','2':'B','3':'A'},'note':'En mode FR, remplacer la copie mot à mot par des objets ou dessins montrés par l’enseignant ; la version texte FR est une activité de repérage, pas une preuve de compréhension.' if language=='fr' else 'Glossaire original, aide de sens ; pas de traduction automatique en direct.'}
 return {'schema_version':1,'theme':theme_id,'title':theme['title'],'level':level,'suggested_grade':theme['suggested_grade'],'duration_minutes':45,'objective':theme['objective'],'support':support,'aid_language':language,'differentiation':SUPPORTS[support],'lexicon':copy.deepcopy(theme['lexicon']),'models':theme['models'][:],'grammar':theme['grammar'],'teacher':{'stages':stages,'resources':'Glossaire FR/ES/EN : aide de sens graduée. Fiche apprenant : préparer les phrases. Dictionnaire : vérifier un mot choisi, avec accompagnement. Portfolio : conserver la production et la grille. Objets ou dessins explicites fournis par l’enseignant : relier mot et référent. Aucun manuel ni numéro de page inventé.','review_status':'teacher_review_required','criteria':criteria},'learner':{'exercise':exercise,'task':'Prépare un droit et deux devoirs, puis présente-les.' if civic else 'Choisis trois expressions et présente trois phrases.','writing_lines':['','',''],'criteria':[c['text'] for c in criteria]},'approved_videos':approved_videos(theme),'video_candidates':copy.deepcopy(theme['videos']),'audio':{'script':'\n'.join(theme['models']),'recording_available':False,'mode':'browser_voice_optional','note':'Lecture vocale selon les voix du navigateur. À contrôler avant la classe. Aucune voix ou bande-son préenregistrée incluse.'},'provenance':{'author':catalog['author'],'translation_mode':catalog['translation_mode'],'sources':copy.deepcopy(catalog['sources']),'classroom_validation':'not_claimed'}}


def export_kit(kit,directory):
 from .render import render_kit
 out=Path(directory)/kit['theme']
 if out.exists():raise ValueError('Kit directory already exists; refusing overwrite')
 out.mkdir(parents=True)
 (out/'kit.json').write_text(json.dumps(kit,ensure_ascii=False,indent=2),encoding='utf-8')
 (out/'kit.html').write_text(render_kit(kit),encoding='utf-8')
 (out/'audio-script.txt').write_text(kit['audio']['script'],encoding='utf-8')
 (out/'teacher.txt').write_text('\n\n'.join([kit['title'],kit['objective'],kit['differentiation'],kit['teacher']['resources']]+[f'{s["name"]} — {s["minutes"]} min — {s["grouping"]}\n{s["instructions"]}' for s in kit['teacher']['stages']]+[c['text']+'\n'+c['threshold'] for c in kit['teacher']['criteria']]),encoding='utf-8')
 (out/'answers.json').write_text(json.dumps(kit['learner']['exercise']['answers'],indent=2),encoding='utf-8')
 return out
