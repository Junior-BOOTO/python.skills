(function(root,factory){const api=factory();if(typeof module==='object'&&module.exports)module.exports=api;root.BootoPassport=api;})(typeof globalThis!=='undefined'?globalThis:this,function(){
'use strict';
const schema='booto.learning-evidence.v1';
const ID=['ask_location','propose_action','report_action'];
function finiteCount(x){return Number.isSafeInteger(x)&&x>=0&&x<=100000?x:0}
function validate3D(input){
 if(!input||typeof input!=='object'||input.schema_version!==schema||input.source!=='booto-fle-multiverse-3d'||input.mission_id!=='eco-cite'||input.learner_identity!==null||input.status!=='completed')throw Error('Passeport 3D non reconnu ou incomplet.');
 if(!['recycle','plant'].includes(input.branch)||!Array.isArray(input.observations)||input.observations.length!==3)throw Error('Les traces pédagogiques de la mission 3D sont incomplètes.');
 const observations=input.observations.map((o,i)=>{
   if(!o||o.criterion_id!==ID[i]||typeof o.french_expression!=='string'||o.french_expression.length>200||!o.french_expression.trim())throw Error('Une preuve pédagogique est invalide.');
   return {criterion_id:ID[i],french_expression:o.french_expression};
 });
 const w=input.world_state;if(!w||typeof w!=='object'||typeof w.river_clean!=='boolean'||typeof w.trees_planted!=='boolean'||typeof w.bins_visible!=='boolean')throw Error('L’état de la ville est incorrect.');
 if(w.river_clean!== (input.branch==='recycle')||w.trees_planted!== (input.branch==='plant'))throw Error('Le monde ne correspond pas au parcours enregistré.');
 return {schema_version:schema,source:'booto-fle-multiverse-3d',mission_id:'eco-cite',learner_identity:null,status:'completed',branch:input.branch,observations,assistance_requests:finiteCount(input.assistance_requests),extra_attempts:finiteCount(input.extra_attempts),world_state:{river_clean:w.river_clean,trees_planted:w.trees_planted,bins_visible:w.bins_visible}};
}
function fromBridgeV0(x){
 if(!x||x.project!=='BOOTO WORLD LEARNING BRIDGE'||x.learner_identity!==null||!Array.isArray(x.observations))throw Error('Données de mission Bridge invalides.');
 if(!Number.isInteger(x.steps_observed)||x.steps_observed<0||x.steps_observed>4||!['recycle','plant',null].includes(x.branch))throw Error('Progression incohérente.');
 return {source:'booto-world-learning-bridge',mission_id:'eco-cite',status:x.steps_observed===4?'completed':'in-progress',route:x.branch,steps_observed:x.steps_observed,
  guidance_language:['fr','es','en'].includes(x.guidance_language)?x.guidance_language:'fr',
  observations:x.observations.slice(0,4).map(o=>({criterion_id:String(o.criterion||'').slice(0,60),french_expression:String(o.french_expression||'').slice(0,200)})),
  assistance_requests:finiteCount(x.assistance_requests),extra_attempts:finiteCount(x.extra_attempts)};
}
function bundle(bridge,threeD){
 const b=fromBridgeV0(bridge);
 return {schema_version:schema,project:'BOOTO WORLD LEARNING BRIDGE',version:'V1 — passeport partagé de deux activités',learner_identity:null,
  activities:[b,...(threeD?[validate3D(threeD)]:[])],counts:{activities_complete:Number(b.status==='completed')+Number(!!threeD),observations:b.observations.length+(threeD?threeD.observations.length:0)},
  limitations:'Deux missions guidées illustratives, sans certification CECRL, sans score psychométrique ni identité d’élève. Aucune sauvegarde automatique.'};
}
return {schema,validate3D,fromBridgeV0,bundle};
});
