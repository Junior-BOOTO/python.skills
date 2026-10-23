const test=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs');
const engine=require('../game/src/mission.js'),P=require('../src/passport.js');
const s=JSON.parse(fs.readFileSync('game/data/scenario.json','utf8'));
function play(route){let x=engine.proceed(engine.initial(),{type:'START'},s);x=engine.proceed(x,{type:'REPLY',dialogue:'amina',id:'ask_where'},s);x=engine.proceed(x,{type:'CHOOSE_PATH',path:route},s);x=engine.proceed(x,{type:'HINT'},s);x=engine.proceed(x,{type:'REPLY',dialogue:route,id:route==='plant'?'trees':'clean'},s);x=engine.proceed(x,{type:'REPLY',dialogue:'report_'+route,id:'report_good'},s);return x;}
const base={project:'BOOTO WORLD LEARNING BRIDGE',learner_identity:null,steps_observed:4,branch:'recycle',guidance_language:'fr',observations:[{criterion:'identify_issue',french_expression:'La rivière est sale.'}],assistance_requests:0,extra_attempts:0};
for(const route of ['plant','recycle']){
 test('finished 3D route and passport '+route,()=>{const p=P.validate3D(engine.passport(play(route),s));assert.equal(p.branch,route);assert.equal(p.observations.length,3);assert.equal(p.learner_identity,null);assert.equal(p.world_state.river_clean,route==='recycle');});
 test('merged passport '+route,()=>{const p=P.bundle(base,engine.passport(play(route),s));assert.equal(p.activities.length,2);assert.equal(p.counts.activities_complete,2);});
 test('reject unfinished route '+route,()=>assert.throws(()=>engine.passport({...play(route),phase:'REPORT'},s)));
}
test('reject forged personally identified data',()=>{const p=engine.passport(play('plant'),s);assert.throws(()=>P.validate3D({...p,learner_identity:'someone'}));assert.throws(()=>P.validate3D({...p,observations:[]}));});
test('2D only activity remains valid',()=>{const p=P.bundle(base,null);assert.equal(p.activities.length,1);assert.equal(p.learner_identity,null);});
test('integrated bridge page includes 3D iframe and export',()=>{const h=fs.readFileSync('index.html','utf8');assert.ok(h.includes('id="multiverseFrame"')&&h.includes('id="mergedPassport"')&&h.includes('id="import3dPassport"'));});
