const test=require('node:test');
const assert=require('node:assert/strict');
const c=require('../src/scanner-core.js');
const zip=require('../src/zip.js');
test('IDs anonymes, trimestre et faces de feuille',()=>{
 assert.equal(c.anonymousId(1),'C001'); assert.equal(c.safeTrimestre('T4'),'T1');
 assert.deepEqual(c.captureSide(1,true),{sheet:1,side:'recto'});
 assert.deepEqual(c.captureSide(2,true),{sheet:1,side:'verso'});
 assert.deepEqual(c.captureSide(3,true),{sheet:2,side:'recto'});
 assert.deepEqual(c.captureSide(2,false),{sheet:2,side:'recto'});
});
test('différence entre images quantifiée',()=>{
 assert.equal(c.meanDifference(Uint8Array.of(10,20),Uint8Array.of(10,20)),0);
 assert.ok(c.meanDifference(Uint8Array.of(10,20),Uint8Array.of(20,20))>0);
 assert.equal(c.meanDifference(null,Uint8Array.of(10)),1);
 assert.deepEqual([...c.sampleLuma(Uint8Array.of(255,0,0,255,0,255,0,255))],[54,182]);
});
test('pas de déclenchement avant première photo; page stable identique ignorée',()=>{
 const gate=new c.PageGate({motion:.2,still:.03,changed:.1,stillFor:1000});
 const a=Uint8Array.of(0,0,0,0),b=Uint8Array.of(255,255,255,255);
 assert.equal(gate.update(a,0),false);gate.onCaptured(a);
 assert.equal(gate.update(a,100),false);
 assert.equal(gate.update(b,400),false);
 assert.equal(gate.update(a,700),false);
 assert.equal(gate.update(a,1800),false);
});
test('une seule capture après une nouvelle page immobile',()=>{
 const gate=new c.PageGate({motion:.2,still:.03,changed:.1,stillFor:1000});
 const a=Uint8Array.of(0,0),b=Uint8Array.of(255,255);
 gate.onCaptured(a);
 assert.equal(gate.update(b,100),false);
 assert.equal(gate.update(b,200),false);
 assert.equal(gate.update(b,1100),false);
 assert.equal(gate.update(b,1200),true);
 assert.equal(gate.update(b,2400),false);
 gate.onCaptured(b);
 assert.equal(gate.update(b,3500),false);
});
test('ZIP avec fichiers UTF-8',async()=>{
 const blob=zip.zip([{name:'images/C001/page-001-recto.jpg',bytes:Uint8Array.of(1,2,3)},{name:'manifest.json',bytes:'{"ok":true}'}]);
 assert.equal(blob.type,'application/zip');
 const bytes=new Uint8Array(await blob.arrayBuffer());
 assert.equal(new DataView(bytes.buffer).getUint32(0,true),0x04034b50);
 assert.equal(new DataView(bytes.buffer).getUint32(bytes.length-22,true),0x06054b50);
 assert.equal(new DataView(bytes.buffer).getUint16(bytes.length-12,true),2);
 assert.equal(zip.crc32(new TextEncoder().encode('123456789')),0xcbf43926);
 assert.throws(()=>zip.zip([{name:'../../secret',bytes:'oops'}]));
});
