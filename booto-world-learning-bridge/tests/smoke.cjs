const fs=require('node:fs');const assert=require('node:assert/strict');
const html=fs.readFileSync('index.html','utf-8');
assert.ok(html.startsWith('<!doctype html>'));
const m=html.match(/<script>([\s\S]*?)<\/script>/);assert.ok(m,'script absent');new Function(m[1]);
for(const id of ['locale','place','visualMode','essentialMode','world','stageLabel','hintBtn','choices','evidence','download','reset'])assert.ok(html.includes('id="'+id+'"'),id);
for(const t of ['fr:','es:','en:','learner_identity:null',"'recycle'","'plant'"])assert.ok(html.includes(t),t);
assert.ok(!html.includes('fetch(')&&!html.includes('XMLHttpRequest')&&!html.includes('localStorage'));
console.log('Demo syntax, semantics and privacy smoke checks OK');
