const fs=require('node:fs'),path=require('node:path');
const root=path.resolve(__dirname,'..'),dist=path.join(root,'dist');
if(fs.existsSync(dist))fs.rmSync(dist,{recursive:true,force:true});
for(const rel of ['index.html','src/passport.js','game/index.html','game/DEMO_AUTONOME.html','game/src/mission.js','game/src/app.js','game/src/world.js']){
 const target=path.join(dist,rel);fs.mkdirSync(path.dirname(target),{recursive:true});fs.copyFileSync(path.join(root,rel),target);
}
console.log('Bundle offline + 3D produced at dist/');
