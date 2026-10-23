const fs=require('node:fs'),path=require('node:path');
const root=path.resolve(__dirname,'..'),dest=path.join(root,'dist');
if(fs.existsSync(dest))fs.rmSync(dest,{recursive:true,force:true});
fs.mkdirSync(path.join(dest,'src'),{recursive:true});
for(const name of ['index.html','DEMO_AUTONOME.html','src/mission.js','src/world.js','src/app.js']){
 const d=path.join(dest,name);
 fs.mkdirSync(path.dirname(d),{recursive:true});
 fs.copyFileSync(path.join(root,name),d);
}
console.log('Distribution statique dist/ créée. Aucun CDN ni serveur requis.');
