/* BOOTO ScanGrade AI — déterministe, sans IA ni OCR en V1. */
(function(root,factory){const m=factory();if(typeof module==='object'&&module.exports)module.exports=m;root.BootoEval=m;})(typeof globalThis!=='undefined'?globalThis:this,function(){
'use strict';
const VERSION='booto.scangrade.grade.v1';
const QUESTIONS=[
{id:1,group:'Vocabulaire',q:'Quelle phrase décrit le début de la journée ?',options:['Je me lève.','Je me couche.','Je dors.','Je joue.'],correct:'A',explain:'Je me lève indique le début de la journée.'},
{id:2,group:'Vocabulaire',q:'Quelle expression correspond à la fin de la journée ?',options:['Le matin','Le soir','À midi','Ensuite'],correct:'B',explain:'Le soir désigne la dernière partie de la journée.'},
{id:3,group:'Vocabulaire',q:'Quel verbe correspond au repas ?',options:['Jouer','Dormir','Manger','Étudier'],correct:'C',explain:'Manger décrit l’action de prendre un repas.'},
{id:4,group:'Vocabulaire',q:'Quelle expression décrit le moment avant de partir ?',options:['Je dors','Je joue','Je mange','Je me prépare'],correct:'D',explain:'Je me prépare convient avant de partir.'},
{id:5,group:'Présent',q:'Complète : À sept heures, je ___ .',options:['lève','me lève','te lèves','se lève'],correct:'B',explain:'Avec je, le pronom réfléchi est me : je me lève.'},
{id:6,group:'Présent',q:'Complète : Je ___ à l’école.',options:['va','vas','vais','vont'],correct:'C',explain:'Aller au présent avec je : je vais.'},
{id:7,group:'Présent',q:'Complète : Nous ___ le français.',options:['étudions','étudie','étudiez','étudient'],correct:'A',explain:'Étudier au présent avec nous : nous étudions.'},
{id:8,group:'Présent',q:'Complète : Après l’école, je ___ au parc.',options:['joues','jouons','jouent','joue'],correct:'D',explain:'Jouer au présent avec je : je joue.'},
{id:9,group:'Heure et moments',q:'Quelle expression indique une heure précise ?',options:['À huit heures','Le soir','Ensuite','Enfin'],correct:'A',explain:'À huit heures indique une heure précise.'},
{id:10,group:'Heure et moments',q:'Quelle expression signifie « approximativement à midi » ?',options:['À minuit','Vers midi','Après-demain','Le lundi'],correct:'B',explain:'Vers indique une heure approximative.'},
{id:11,group:'Organisation',q:'Quel mot permet de poursuivre un récit après « d’abord » ?',options:['Hier','Jamais','Ensuite','Toujours'],correct:'C',explain:'Ensuite indique l’étape suivante.'},
{id:12,group:'Organisation',q:'Quel mot marque la dernière étape ?',options:['Souvent','D’abord','Puis','Enfin'],correct:'D',explain:'Enfin permet de terminer la description.'}
];
const GROUPS=['Vocabulaire','Présent','Heure et moments','Organisation'];
function safeId(x){let v=String(x||'').toUpperCase().trim();if(!/^C[0-9]{3,5}$/.test(v))throw Error('Identifiant anonyme requis : C001, C002…');return v;}
function safeTerm(t){if(!['T1','T2','T3'].includes(t))throw Error('Choisissez T1, T2 ou T3');return t;}
function safeScale(s){let v=Number(s);if(![7,10,20,100].includes(v))throw Error('Barème non disponible');return v;}
function parseAnswers(input){let v=String(input||'').toUpperCase().replace(/[\s,;|.\-]/g,'');if(v.length!==QUESTIONS.length||!/^[ABCD]+$/.test(v))throw Error('Saisissez exactement 12 réponses A, B, C ou D.');return v;}
function round(n){return Math.round((n+Number.EPSILON)*100)/100;}
function compute(input,scale=20){const answers=parseAnswers(input),max=safeScale(scale);const byGroup={},details=[];let correct=0;
  for(const group of GROUPS)byGroup[group]={correct:0,total:0};
  QUESTIONS.forEach((q,i)=>{const ok=answers[i]===q.correct;correct+=ok?1:0;byGroup[q.group].total++;byGroup[q.group].correct+=ok?1:0;details.push({n:q.id,group:q.group,answer:answers[i],expected:q.correct,ok,explain:q.explain});});
  const strengths=GROUPS.filter(g=>byGroup[g].correct/byGroup[g].total>=.75);
  const needs=GROUPS.filter(g=>byGroup[g].correct/byGroup[g].total<.75);
  let strengthText=strengths.length?`Points forts observés : ${strengths.join(', ').toLowerCase()}.`:'Points forts à consolider : l’élève a commencé à mobiliser les notions évaluées.';
  let weakText=needs.length?`À renforcer : ${needs.join(', ').toLowerCase()}.`:'Les domaines évalués sont globalement maîtrisés dans ce questionnaire.';
  const advice={
   'Vocabulaire':'Associer six activités quotidiennes à des images puis les nommer.',
   'Présent':'Construire des phrases avec je me lève, je vais, je joue et nous étudions.',
   'Heure et moments':'Décrire trois activités en précisant à ou vers une heure.',
   'Organisation':'Raconter sa routine en utilisant d’abord, ensuite et enfin.'
  };
  const recommendations=(needs.length?needs:GROUPS).slice(0,2).map(g=>advice[g]);
  const comment=`${strengthText} ${weakText} Recommandations : ${recommendations.join(' ')}`;
  return {answers,correct,total:QUESTIONS.length,scale:max,score:round(correct/QUESTIONS.length*max),byGroup,details,strengths,needs,recommendations,comment};
}
function safeScore(score,scale){const s=Number(score),m=safeScale(scale);if(!Number.isFinite(s)||s<0||s>m)throw Error('Note hors du barème');return round(s);}
function createRecord({id,term,answers,scale,validatedScore,comment,reason,now}){
 const evalResult=compute(answers,scale),anon=safeId(id),period=safeTerm(term),score=safeScore(validatedScore,evalResult.scale),text=String(comment||'').trim();
 if(text.length<15||text.length>2200)throw Error('Commentaire requis (15 à 2 200 caractères)');
 if(score!==evalResult.score && !String(reason||'').trim())throw Error('Expliquez toute modification manuelle de la note');
 return {schema:VERSION,id:anon,term:period,activity:'ROUTINE_A1_12',score,scale:evalResult.scale,automaticScore:evalResult.score,correct:evalResult.correct,total:evalResult.total,answers:evalResult.answers,byGroup:evalResult.byGroup,strengths:evalResult.strengths,needs:evalResult.needs,comment:text,overrideReason:String(reason||'').trim(),validatedAt:now||new Date().toISOString(),revision:1};
}
function upsert(records,record){if(!Array.isArray(records))throw Error('Registre invalide');const arr=records.map(x=>({...x}));const i=arr.findIndex(x=>x.id===record.id&&x.term===record.term&&x.activity===record.activity);
if(i>=0){record.revision=(arr[i].revision||1)+1;arr[i]=record;}else arr.push(record);return arr.sort((a,b)=>a.id.localeCompare(b.id)||a.term.localeCompare(b.term)||a.activity.localeCompare(b.activity));}
function summary(records){const m=new Map();for(const r of records){if(r.schema!==VERSION)continue;const key=r.id;let v=m.get(key);if(!v){v={id:key,T1:null,T2:null,T3:null,average:null};m.set(key,v);}v[r.term]=round(r.score/r.scale*20);}
for(const v of m.values()){const vals=['T1','T2','T3'].map(t=>v[t]).filter(Number.isFinite);v.average=vals.length?round(vals.reduce((a,b)=>a+b,0)/vals.length):null;}return [...m.values()].sort((a,b)=>a.id.localeCompare(b.id));}
function importRegister(x){if(!x||x.schema!==VERSION||!Array.isArray(x.records)||x.records.length>4000)throw Error('Fichier de registre non reconnu');let rows=[];for(let r of x.records){const safe=createRecord({id:r.id,term:r.term,answers:r.answers,scale:r.scale,validatedScore:r.score,comment:r.comment,reason:r.overrideReason,now:r.validatedAt});safe.revision=Number.isInteger(r.revision)&&r.revision>0?Math.min(r.revision,10000):1;rows=upsert(rows,safe);}return rows;}
return {VERSION,QUESTIONS,GROUPS,compute,parseAnswers,safeId,safeScore,createRecord,upsert,summary,importRegister,round};
});
