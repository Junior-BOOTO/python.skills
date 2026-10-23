const fs=require('node:fs'); const path=require('node:path');
const root=path.resolve(__dirname,'..'); const out=path.join(root,'dist');
fs.mkdirSync(out,{recursive:true});fs.copyFileSync(path.join(root,'index.html'),path.join(out,'index.html'));
console.log('Static build created in dist/');
