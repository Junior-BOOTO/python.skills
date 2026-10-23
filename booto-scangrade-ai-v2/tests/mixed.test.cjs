const test=require('node:test'),assert=require('node:assert/strict');
const e=require('../src/mixed-engine.js'),core=require('../src/scanner-core.js'),Zip=require('../src/zip.js'),Excel=require('../src/export-xlsx.js');
const fakeAnswers=['B','vrai','me','un arbre','Je me lève à sept heures.'];
const demo=e.DEMO.map(x=>({...x}));
test('supports five mixed item types with a human review requirement',()=>{
 const p=e.propose(demo,fakeAnswers);assert.equal(p.details.length,5);assert.equal(p.requiresReview,3);assert.equal(p.total,10);
 assert.equal(p.details[0].suggested,2);assert.equal(p.details[1].suggested,1);assert.equal(p.details[2].suggested,2);
 assert.equal(p.details[3].suggested,null);assert.equal(p.details[4].suggested,null);
});
test('prevents recording when any item lacks explicit teacher confirmation',()=>{
 const p=e.propose(demo,fakeAnswers);p.details.forEach(d=>d.teacherPoints=d.suggested||0);
 assert.throws(()=>e.finalize({id:'C001',term:'T1',title:'Examen A1 pilote',scale:20,details:p.details,reviewed:[true,true,true,false,true],comment:'Un commentaire pédagogique suffisamment détaillé.'}),/Validez chaque question/);
});
test('calculates mixed grade from manually validated weighted items',()=>{
 const p=e.propose(demo,fakeAnswers);p.details.forEach(d=>d.teacherPoints=d.points);p.details[4].teacherPoints=1;
 const record=e.finalize({id:'C001',term:'T1',title:'Examen A1 pilote',scale:20,details:p.details,reviewed:p.details.map(()=>true),comment:e.commentFor(p.details)});
 assert.equal(record.score,16);assert.equal(record.correct,4);assert.equal(record.scale,20);assert.equal(record.details.length,5);
});
test('same student/term/activity updates without duplication, preserving revisions',()=>{
 const p=e.propose(demo,fakeAnswers);p.details.forEach(d=>d.teacherPoints=d.points);
 const args={id:'C001',term:'T1',title:'Examen A1 pilote',scale:20,details:p.details,reviewed:p.details.map(()=>true),comment:e.commentFor(p.details)};
 const a=e.finalize(args);let rows=e.upsert([],a);const second=e.finalize(args);rows=e.upsert(rows,second);
 assert.equal(rows.length,1);assert.equal(rows[0].revision,2);assert.equal(e.summary(rows)[0].T1,20);
});
test('rejects invalid personal code and arbitrary malicious question fields',()=>{
 assert.throws(()=>e.safeId('Juan Perez'),/Code anonyme/);assert.throws(()=>e.validateQuestions([{...demo[0],points:-20}]),/non valide/);assert.equal(e.isMatch(' l\u2019ARBRE ','l\u2019arbre|un arbre'),true);
});
test('sheet labels remain alternating recto verso for one copy',()=>{
 assert.deepEqual(core.captureSide(1,true),{sheet:1,side:'recto'});assert.deepEqual(core.captureSide(2,true),{sheet:1,side:'verso'});assert.deepEqual(core.captureSide(3,true),{sheet:2,side:'recto'});
});
test('writes a real XLSX ZIP with both sheets for a mixed validated record',async()=>{
 const p=e.propose(demo,fakeAnswers);p.details.forEach(d=>d.teacherPoints=d.points);
 const row=e.finalize({id:'C001',term:'T2',title:'Examen A1 pilote',scale:20,details:p.details,reviewed:p.details.map(()=>true),comment:e.commentFor(p.details)});
 const blob=Excel.generate([row],e,Zip);const bytes=new Uint8Array(await blob.arrayBuffer());
 assert.equal(Buffer.from(bytes.subarray(0,2)).toString('ascii'),'PK');assert(bytes.length>1400);
});
test('rejects malformed or oversized register imports',()=>{
 assert.throws(()=>e.importRegister({schema:e.VERSION,records:[{id:'ABC',term:'T1',details:[]}]}));
 assert.throws(()=>e.importRegister({schema:'fake',records:[]}));
});
