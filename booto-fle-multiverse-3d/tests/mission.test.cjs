const test=require('node:test'), assert=require('node:assert/strict'), fs=require('node:fs'), path=require('node:path');
const e=require('../src/mission.js');
const s=JSON.parse(fs.readFileSync(path.join(__dirname,'../data/scenario.json'),'utf-8'));
const begin=()=>e.proceed(e.initial(),{type:'START'},s);
const meet=()=>e.proceed(begin(),{type:'REPLY',dialogue:'amina',id:'ask_where'},s);
for(const route of ['recycle','plant']){
  test('parcours '+route+' complet, conséquence et bilan cohérents',()=>{
    let x=meet(); assert.equal(x.phase,'DECIDE');
    x=e.proceed(x,{type:'CHOOSE_PATH',path:route},s);assert.equal(x.phase,'ACT');
    x=e.proceed(x,{type:'REPLY',dialogue:route,id:route==='plant'?'trees':'clean'},s);
    assert.equal(x.phase,'REPORT');
    assert.equal(x.world.treesPlanted,route==='plant');
    assert.equal(x.world.riverClean,route==='recycle');
    assert.equal(x.world.binsVisible,route==='recycle');
    x=e.proceed(x,{type:'REPLY',dialogue:'report_'+route,id:'report_good'},s);
    assert.equal(x.phase,'COMPLETE');
    assert.equal(e.report(x,s).phrases.length,3);
    assert.ok(e.reportText(x,s).includes('Mission terminée'));
  });
  test('la mauvaise réponse '+route+" ne débloque pas l'action",()=>{
    let x=e.proceed(meet(),{type:'CHOOSE_PATH',path:route},s);
    x=e.proceed(x,{type:'REPLY',dialogue:route,id:'no_link'},s);
    assert.equal(x.phase,'ACT');assert.equal(x.retries,1);
    assert.equal(x.world.treesPlanted,false);assert.equal(x.world.riverClean,false);
  });
  test('la mauvaise médiation '+route+' ne termine pas la mission',()=>{
    let x=e.proceed(meet(),{type:'CHOOSE_PATH',path:route},s);
    x=e.proceed(x,{type:'REPLY',dialogue:route,id:route==='plant'?'garden':'other_good'},s);
    x=e.proceed(x,{type:'REPLY',dialogue:'report_'+route,id:'report_bad'},s);
    assert.equal(x.phase,'REPORT');assert.equal(x.retries,1);
  });
}
test('démarrage puis découverte',()=>{
 const v=begin();assert.equal(v.phase,'DISCOVER');assert.equal(e.target(v),'quartier');
});
test('aucune réponse hors phase ne change le parcours',()=>{
 const x=begin();
 let y=e.proceed(x,{type:'CHOOSE_PATH',path:'plant'},s);assert.equal(y.phase,'DISCOVER');
 y=e.proceed(x,{type:'REPLY',dialogue:'recycle',id:'clean'},s);assert.equal(y.phase,'DISCOVER');
});
test("indice ajoute de l'aide sans progression",()=>{
 const x=e.proceed(begin(),{type:'HINT'},s);assert.equal(x.phase,'DISCOVER');assert.equal(x.assists,1);
});
test("réinitialiser rétablit l'environnement initial",()=>{
 let x=e.proceed(meet(),{type:'CHOOSE_PATH',path:'recycle'},s);
 x=e.proceed(x,{type:'REPLY',dialogue:'recycle',id:'clean'},s);
 x=e.proceed(x,{type:'RESET'},s);assert.deepEqual(x,e.initial());
});
test('les dialogues ont tous une réponse pertinente et un indice de remédiation',()=>{
 for(const [key,dialogue] of Object.entries(s.dialogues)){
  assert.ok(dialogue.line.length>10,key);
  assert.ok(dialogue.options.some(o=>o.valid),key);
  assert.ok(dialogue.options.some(o=>!o.valid&&o.feedback),key);
 }
});
test('bilan sans niveau CECRL certifié ni donnée nominative',()=>{
 const r=e.report(meet(),s);
 assert.equal(r.status,'Mission en cours');
 assert.equal(r.observations.mediation,'Non observé');
 assert.equal(JSON.stringify(r).includes('nom_élève'),false);
});
test("destination de la phase ACTION reflète le parcours",()=>{
 for(const route of ['plant','recycle']){
  const x=e.proceed(meet(),{type:'CHOOSE_PATH',path:route},s);
  assert.equal(e.target(x),route==='plant'?'parc':'riviere');
 }
});
test('zones, personnages et objectifs pédagogiques présents',()=>{
 assert.equal(s.zones.length,4);assert.equal(s.characters.length,4);assert.equal(s.can_do.length,4);
});
