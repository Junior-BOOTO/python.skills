// Même transformation et distance euclidienne que l'export numérique Python.
export function assign(point,model){
 if(!Array.isArray(point)||point.length!==2||!point.every(Number.isFinite)||point[0]<=0||point[1]<1||point[1]>100)throw new Error('Revenu positif et score entre 1 et 100 attendus.');
 const z=point.map((v,i)=>(v-model.mean[i])/model.scale[i]);
 const distances=model.centers.map(c=>c.reduce((sum,v,i)=>sum+(v-z[i])**2,0));
 const squared=Math.min(...distances);return {group:distances.indexOf(squared),distance:Math.sqrt(squared)};
}
