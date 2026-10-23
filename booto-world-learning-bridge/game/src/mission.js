/* BOOTO FLE MULTIVERSE 3D · moteur narratif pur, compatible navigateur et Node. */
(function(root,factory){const api=factory();if(typeof module==='object'&&module.exports)module.exports=api;root.MultiverseMission=api;})(typeof globalThis!=='undefined'?globalThis:this,function(){
  'use strict';
  const PHASES=['START','DISCOVER','DECIDE','ACT','REPORT','COMPLETE'];
  const initial=()=>({phase:'START',path:null,amina:false,clue:null,action:null,report:null,assists:0,retries:0,history:[],world:{riverClean:false,binsVisible:false,treesPlanted:false},lastFeedback:'',lastSkill:null});
  function proceed(state,action,scenario){
    const s=JSON.parse(JSON.stringify(state));
    if(action.type==='RESET')return initial();
    if(action.type==='START'&&s.phase==='START'){
      s.phase='DISCOVER';s.lastFeedback='Parle à Amina dans le quartier des habitants.';return s;
    }
    if(action.type==='HINT'){
      s.assists++;s.lastFeedback=hint(s);return s;
    }
    if(action.type==='REPLY'){
      const {dialogue,id}=action;let expected=null;
      if(s.phase==='DISCOVER'&&dialogue==='amina')expected='amina';
      if(s.phase==='ACT'&&dialogue===s.path)expected=s.path;
      if(s.phase==='REPORT'&&dialogue==='report_'+s.path)expected='report_'+s.path;
      if(expected!==dialogue)return s;
      const opt=scenario.dialogues[dialogue]?.options?.find(x=>x.id===id);
      if(!opt)return s;
      s.lastFeedback=opt.feedback;
      if(!opt.valid){s.retries++;s.history.push({phase:s.phase,dialogue,id,valid:false,text:opt.text});return s;}
      s.history.push({phase:s.phase,dialogue,id,valid:true,text:opt.text,skill:opt.skill});
      s.lastSkill=opt.skill;
      if(dialogue==='amina'){s.phase='DECIDE';s.amina=true;s.clue=id;}
      else if(dialogue==='recycle'){s.phase='REPORT';s.action=id;s.world.riverClean=true;s.world.binsVisible=true;}
      else if(dialogue==='plant'){s.phase='REPORT';s.action=id;s.world.treesPlanted=true;}
      else if(dialogue.startsWith('report_')){s.phase='COMPLETE';s.report=id;}
      return s;
    }
    if(action.type==='CHOOSE_PATH'&&s.phase==='DECIDE'&&['recycle','plant'].includes(action.path)){
      s.path=action.path;s.phase='ACT';
      s.lastFeedback=action.path==='recycle'?'Va parler à Éric près de la rivière.':'Va parler à Nadia dans le parc.';
      return s;
    }
    return s;
  }
  function hint(s){return {START:'Commence la mission pour découvrir Éco-Cité.',DISCOVER:'Rejoins Amina dans le quartier, puis demande où est la rivière ou comment aider.',DECIDE:'Choisis une solution : recycler près de la rivière ou planter dans le parc.',ACT:s.path==='recycle'?'Parle à Éric. Propose de recycler les déchets ou de nettoyer la rivière.':'Parle à Nadia. Propose de planter des arbres ou de protéger le parc.',REPORT:'Retourne à la mairie et décris le changement observé.',COMPLETE:'Ouvre le bilan ou recommence pour choisir un autre chemin.'}[s.phase]}
  function target(s){return {START:'mairie',DISCOVER:'quartier',DECIDE:'mairie',ACT:s.path==='recycle'?'riviere':'parc',REPORT:'mairie',COMPLETE:'mairie'}[s.phase]}
  function observations(s){return {
    comprehension: s.amina?(s.assists?'Observé avec aide':'Observé'):'Non observé',
    interaction: s.path?(s.retries?'Observé après reformulation':'Observé'):'Non observé',
    mediation: s.report?'Observé':'Non observé'};}
  function report(s,scenario){const actions=s.history.filter(x=>x.valid);return {
    title:'Bilan de mission — Éco-Cité francophone',
    route:s.path==='recycle'?'Nettoyage et tri':s.path==='plant'?'Plantation et protection':'Non choisie',
    outcome:s.path==='recycle'&&s.world.riverClean?'Des bacs de tri sont visibles ; la rivière est plus propre.':s.path==='plant'&&s.world.treesPlanted?'De nouveaux arbres ont poussé dans le parc.':'Mission en cours.',
    status:s.phase==='COMPLETE'?'Mission terminée':'Mission en cours',
    phrases:actions.map(x=>x.text),
    skills:[...new Set(actions.map(x=>x.skill))],
    observations:observations(s),
    assists:s.assists,retries:s.retries,
    canDo:scenario.can_do,
    disclaimer:scenario.disclaimer
  };}
  function reportText(s,scenario){const r=report(s,scenario);return [r.title,r.status,'Parcours : '+r.route,r.outcome,'','Phrases utilisées :',...r.phrases.map((p,i)=>`${i+1}. ${p}`),'','Compétences mobilisées :',...r.skills.map(p=>'• '+p),'','Traces formatives :',...Object.entries(r.observations).map(([k,v])=>`${k} : ${v}`),`Aides consultées : ${r.assists}`,`Essais révisés : ${r.retries}`,'','Objectifs « Je peux… » :',...r.canDo.map(p=>'• '+p),'',r.disclaimer,'© 2026 Junior BOOTO Waba'].join('\n')}
  function passport(s,scenario){
    if(s.phase!=='COMPLETE')throw new Error('Le passeport n’est disponible qu’après la mission.');
    const mapping={amina:'ask_location',recycle:'propose_action',plant:'propose_action',report_recycle:'report_action',report_plant:'report_action'};
    const label={ask_location:'Demander un renseignement',propose_action:'Proposer une action écologique',report_action:'Présenter le résultat d’une action'};
    const evidence=s.history.filter(e=>e.valid&&mapping[e.dialogue]).map(e=>({criterion_id:mapping[e.dialogue],criterion_fr:label[mapping[e.dialogue]],french_expression:e.text}));
    return {
      schema_version:'booto.learning-evidence.v1',source:'booto-fle-multiverse-3d',mission_id:'eco-cite',
      learner_identity:null,status:'completed',branch:s.path,observations:evidence,
      assistance_requests:s.assists,extra_attempts:s.retries,
      world_state:{river_clean:!!s.world.riverClean,trees_planted:!!s.world.treesPlanted,bins_visible:!!s.world.binsVisible},
      limitations:'Choix guidés observés dans une mission fictive ; ni diagnostic individuel ni certification CECRL.'
    };
  }
  return {PHASES,initial,proceed,hint,target,report,reportText,passport};
});
