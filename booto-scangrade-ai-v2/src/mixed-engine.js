/* BOOTO ScanGrade AI V2 · Moteur déterministe · ni OCR, ni IA générative. */
(function(root,factory){const api=factory();if(typeof module==='object'&&module.exports)module.exports=api;root.BootoMixed=api;})(typeof globalThis!=='undefined'?globalThis:this,function(){
'use strict';
const VERSION='booto.scangrade.mixed.v2',TYPES=['qcm','vrai_faux','courte','image','ouverte'];
const TYPES_LABEL={qcm:'QCM',vrai_faux:'Vrai / Faux',courte:'Réponse courte',image:'Identification d’image',ouverte:'Question ouverte'};
const ROUND=n=>Math.round((n+Number.EPSILON)*100)/100;
function safeId(v){v=String(v??'').toUpperCase().trim();if(!/^C\d{3,5}$/.test(v))throw Error('Code anonyme requis : C001, C002…');return v;}
function safeTerm(v){if(!['T1','T2','T3'].includes(v))throw Error('Trimestre non reconnu');return v;}
function safeScale(v){v=Number(v);if(![7,10,20,100].includes(v))throw Error('Barème disponible : 7, 10, 20 ou 100');return v;}
function normalize(v){return String(v??'').normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLocaleLowerCase('fr').replace(/[’']/g,"'").replace(/\s+/g,' ').trim();}
function isMatch(answer,expected){const a=normalize(answer);return Boolean(a)&&String(expected).split('|').some(e=>normalize(e)===a);}
function safeTitle(t){t=String(t??'').trim();if(t.length<3||t.length>100)throw Error('Titre de l’évaluation : 3 à 100 caractères');return t;}
function validateQuestions(items){if(!Array.isArray(items)||!items.length||items.length>50)throw Error('Une à cinquante questions sont requises');let sum=0;
 const result=items.map((q,i)=>{const type=String(q.type||'');if(!TYPES.includes(type))throw Error(`Type invalide pour la question ${i+1}`);const prompt=String(q.prompt??'').trim(),skill=String(q.skill??'').trim(),expected=String(q.expected??'').trim(),points=Number(q.points);
 if(!prompt||prompt.length>400||!skill||skill.length>55||!Number.isFinite(points)||points<=0||points>20||!expected||expected.length>220)throw Error(`Question ${i+1} : consigne, domaine, points ou corrigé non valide`);
 sum+=points;return {id:i+1,type,prompt,skill,expected,points,options:String(q.options??'').slice(0,240)};});if(sum>200)throw Error('Total de points supérieur à 200');return result;}
function propose(items,answers){const questions=validateQuestions(items);if(!Array.isArray(answers)||answers.length!==questions.length)throw Error('Réponses incomplètes');let total=0,provisional=0,requiresReview=0;
 const details=questions.map((q,i)=>{const answer=String(answers[i]??'').trim().slice(0,700);let suggested=null,why='Validation humaine obligatoire';
 if(q.type==='qcm'||q.type==='vrai_faux') {suggested=isMatch(answer,q.expected)?q.points:0;why='Comparaison exacte avec le corrigé';}
 if(q.type==='courte'){suggested=isMatch(answer,q.expected)?q.points:0;why='Comparaison littérale indicative : variantes et synonymes possibles';}
 const manual=q.type==='courte'||q.type==='image'||q.type==='ouverte';if(manual)requiresReview++;
 total+=q.points;provisional+=suggested||0;return {...q,answer,suggested,manual,why};});
 return {details,total,maxSuggested:ROUND(provisional),requiresReview,partial:requiresReview>0};}
function commentFor(details){if(!Array.isArray(details)||!details.length)throw Error('Corrections requises');let buckets=new Map();for(const d of details){let b=buckets.get(d.skill)||{points:0,score:0};b.points+=d.points;b.score+=Number(d.teacherPoints)||0;buckets.set(d.skill,b);}const strong=[],weak=[];
 for(const [skill,x] of buckets){if(x.score/x.points>=.75)strong.push(skill);else weak.push(skill);}
 const p1=strong.length?`Points forts observés dans cette évaluation : ${strong.join(', ')}.`:'Points forts : quelques compétences sont en cours de construction ; poursuivre les observations.';
 const p2=weak.length?`Points à renforcer : ${weak.join(', ')}.`:'Aucune difficulté dominante dans les critères de ce travail.';
 const p3=weak.length?`Recommandations : proposer une courte activité ciblée sur ${weak.slice(0,2).join(' et ')} ; réévaluer sur une tâche différente.`:'Recommandations : consolider les acquis par une tâche nouvelle et une production personnelle.';
 return `${p1} ${p2} ${p3} Ce bilan repose sur les réponses et critères de cette activité, sans certification CECRL.`;}
function finalize({id,term,title,scale,details,reviewed,comment,now}){
 const copy=safeId(id),period=safeTerm(term),activity=safeTitle(title),max=safeScale(scale);
 if(!Array.isArray(details)||!details.length||!Array.isArray(reviewed)||reviewed.length!==details.length||reviewed.some(x=>x!==true))throw Error('Validez chaque question une par une avant de finaliser.');
 let total=0,raw=0;const safeDetails=details.map((d,i)=>{const pts=Number(d.points),val=Number(d.teacherPoints);
 if(!Number.isFinite(pts)||pts<=0||pts>20||!Number.isFinite(val)||val<0||val>pts)throw Error(`Points invalides à la question ${i+1}`);
 total+=pts;raw+=val;return {id:i+1,type:d.type,skill:String(d.skill).slice(0,55),prompt:String(d.prompt).slice(0,400),expected:String(d.expected).slice(0,220),answer:String(d.answer).slice(0,700),points:pts,teacherPoints:val,note:String(d.note||'').slice(0,450)};});
 const note=ROUND(raw/total*max),text=String(comment||'').trim();if(text.length<20||text.length>2500)throw Error('Appréciation validée requise (20 à 2 500 caractères)');
 return {schema:VERSION,id:copy,term:period,activity,score:note,scale:max,automaticScore:null,correct:safeDetails.filter(x=>x.teacherPoints===x.points).length,total:safeDetails.length,answers:safeDetails.map(d=>`Q${d.id}:${d.answer}`).join(' | ').slice(0,1500),comment:text,overrideReason:'Revue humaine de chaque réponse',validatedAt:now||new Date().toISOString(),revision:1,details:safeDetails};}
function upsert(records,record){let arr=records.map(r=>({...r}));const i=arr.findIndex(r=>r.id===record.id&&r.term===record.term&&r.activity===record.activity);if(i>=0){record.revision=(arr[i].revision||1)+1;arr[i]=record;}else arr.push(record);return arr.sort((a,b)=>a.id.localeCompare(b.id)||a.term.localeCompare(b.term)||a.activity.localeCompare(b.activity));}
function summary(records){let m=new Map();for(const r of records){if(!m.has(r.id))m.set(r.id,{id:r.id,T1:[],T2:[],T3:[],average:null});let v=m.get(r.id);v[r.term].push(r.score/r.scale*20);}return [...m.values()].map(x=>{const row={id:x.id};const vals=[];for(const t of ['T1','T2','T3']){row[t]=x[t].length?ROUND(x[t].reduce((a,b)=>a+b,0)/x[t].length):null;if(row[t]!==null)vals.push(row[t]);}row.average=vals.length?ROUND(vals.reduce((a,b)=>a+b,0)/vals.length):null;return row;}).sort((a,b)=>a.id.localeCompare(b.id));}
function importRegister(data){if(data?.schema!==VERSION||!Array.isArray(data.records)||data.records.length>1000)throw Error('Sauvegarde V2 non reconnue');let arr=[];for(const r of data.records){if(!r||!Array.isArray(r.details)||r.details.length>50||!['T1','T2','T3'].includes(r.term))throw Error('Entrée corrompue');const valid=finalize({id:r.id,term:r.term,title:r.activity,scale:r.scale,details:r.details,reviewed:r.details.map(()=>true),comment:r.comment,now:r.validatedAt});valid.revision=Number.isInteger(r.revision)&&r.revision>0?Math.min(r.revision,10000):1;arr=upsert(arr,valid);}return arr;}
const DEMO=[
 {type:'qcm',prompt:'Je ___ à l’école.',expected:'B',options:'A va ; B vais ; C vas ; D vont',points:2,skill:'Conjugaison'},
 {type:'vrai_faux',prompt:'« Ensuite » est un connecteur temporel.',expected:'vrai',points:1,skill:'Organisation'},
 {type:'courte',prompt:'Complète : Je ___ lève à sept heures.',expected:'me',points:2,skill:'Conjugaison'},
 {type:'image',prompt:'Identifie l’objet représenté sur l’image fournie par l’enseignant.',expected:'arbre|un arbre',points:2,skill:'Vocabulaire visuel'},
 {type:'ouverte',prompt:'Écris une phrase sur ta routine en indiquant une heure.',expected:'Phrase compréhensible avec une action et une heure.',points:3,skill:'Expression écrite'}
];
return {VERSION,TYPES,TYPES_LABEL,DEMO,normalize,isMatch,safeId,safeTerm,safeScale,validateQuestions,propose,commentFor,finalize,summary,upsert,importRegister};
});
