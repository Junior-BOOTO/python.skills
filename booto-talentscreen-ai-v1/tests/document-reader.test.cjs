const test=require('node:test'), assert=require('node:assert/strict'),D=require('../src/document-reader.js');
test('le filtre signale les emails et URL identifiantes',()=>{let x=D.privacySignals('contacter alice@example.test sur linkedin.com/in/alice');assert(x.includes('adresse e-mail'));assert(x.some(v=>v.includes('lien')))});
test('un projet factice technique ne déclenche aucun blocage',()=>{assert.deepEqual(D.privacySignals('Projet fictif Python et SQL pour tableau de bord et versionnement Git.'),[])});
test('fichier non autorisé refusé',()=>assert.throws(()=>D.recognize({name:'x.exe',size:12}),/Seuls/));
test('limite de 3 Mo appliquée avant la lecture',()=>assert.throws(()=>D.recognize({name:'x.docx',size:3000001}),/3 Mo/));
test('fichier PDF est identifié explicitement',()=>assert.equal(D.recognize({name:'demo.PDF',size:5}),'pdf'));
