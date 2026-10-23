/* Lecture prudente des archives ZIP STORE émises par BOOTO ScanGrade V0 uniquement. */
(function(root,factory){const m=factory();if(typeof module==='object'&&module.exports)module.exports=m;root.BootoScans=m;})(typeof globalThis!=='undefined'?globalThis:this,function(){
'use strict';
const decoder=new TextDecoder();
function parse(bytes,zipper){if(!(bytes instanceof Uint8Array)||bytes.length>120*1024*1024)throw Error('Archive trop volumineuse (120 Mo maximum)');
 const view=new DataView(bytes.buffer,bytes.byteOffset,bytes.byteLength),files=new Map();let pos=0,count=0;
 while(pos+4<=bytes.length){const sig=view.getUint32(pos,true);if(sig===0x02014b50||sig===0x06054b50)break;if(sig!==0x04034b50)throw Error('Archive ZIP non reconnue');
 if(pos+30>bytes.length)throw Error('Archive ZIP incomplète');const flags=view.getUint16(pos+6,true),method=view.getUint16(pos+8,true);
 if(flags&0x0008||method!==0)throw Error('Archive incompatible : seules les archives V0 non compressées sont acceptées');
 const crc=view.getUint32(pos+14,true),compressed=view.getUint32(pos+18,true),length=view.getUint32(pos+22,true);
 const nameSize=view.getUint16(pos+26,true),extra=view.getUint16(pos+28,true),start=pos+30+nameSize+extra,end=start+compressed;
 if(compressed!==length||end>bytes.length||length>12*1024*1024)throw Error('Fichier interne trop volumineux ou endommagé');
 const name=decoder.decode(bytes.slice(pos+30,pos+30+nameSize));
 if(!/^(manifest\.json|inventaire\.csv|images\/C\d{3,5}\/page-\d{3}-(recto|verso)\.jpg)$/.test(name)||files.has(name))throw Error('Contenu ZIP inattendu');
 const content=bytes.slice(start,end);if(zipper.crc32(content)!==crc)throw Error('Intégrité ZIP invalide : '+name);files.set(name,content);
 count++;if(count>250)throw Error('Trop de fichiers dans l’archive');pos=end;
 }
 if(!files.has('manifest.json'))throw Error('Inventaire V0 absent');let manifest;try{manifest=JSON.parse(decoder.decode(files.get('manifest.json')));}catch(e){throw Error('Manifeste illisible');}
 if(manifest.schema!=='booto.scangrade.scan.v0'||!Array.isArray(manifest.pages)||manifest.pages.length>120)throw Error('Archive ne provenant pas de ScanGrade V0');
 const pages=manifest.pages.map(p=>{
  if(!/^C\d{3,5}$/.test(String(p.copie||''))||!['recto','verso'].includes(p.face)||!Number.isInteger(p.page)||p.page<1||p.page>120)throw Error('Métadonnées de copie invalides');
  const path=String(p.fichier||'');if(!files.has(path)||!/^images\/C\d{3,5}\/page-\d{3}-(recto|verso)\.jpg$/.test(path))throw Error('Image manquante ou non autorisée');
  return {id:p.copie,term:p.trimestre,side:p.face,page:p.page,path,image:files.get(path)};
 });
 return {pages,copies:[...new Set(pages.map(p=>p.id))].sort()};
}
return {parse};
});
