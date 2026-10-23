/* BOOTO ScanGrade AI V0 — uniquement local au navigateur, aucune API distante. */
(() => {
  'use strict';
  const $ = (id) => document.getElementById(id);
  const Core = window.ScanGradeCore;
  const MaxPages = 120;
  const state = {stream:null, timer:null, busy:false, scans:[], copyNum:1, gate:new Core.PageGate(), sampleCanvas:document.createElement('canvas'), captureCanvas:document.createElement('canvas')};
  const video = $('camera');
  state.sampleCanvas.width = 64; state.sampleCanvas.height = 48;
  const sampleCtx = state.sampleCanvas.getContext('2d', {willReadFrequently:true});
  const captureCtx = state.captureCanvas.getContext('2d');

  function status(message) { $('cameraStatus').textContent = message; }
  function batchStatus(message) { $('batchStatus').textContent = message; }
  function cameraRunning() { return Boolean(state.stream && video.readyState >= 2 && video.videoWidth); }
  function sample() {
    if (!cameraRunning()) return null;
    sampleCtx.drawImage(video, 0, 0, 64, 48);
    return Core.sampleLuma(sampleCtx.getImageData(0, 0, 64, 48).data);
  }
  function currentId() { return Core.anonymousId(state.copyNum); }
  function countFor(id) { return state.scans.filter((s) => s.copy === id).length; }
  function assignPages() {
    const nums = new Map();
    for (const s of state.scans) {
      const n = (nums.get(s.copy) || 0) + 1;
      nums.set(s.copy, n);
      s.page = n;
      Object.assign(s, Core.captureSide(n, s.duplex));
    }
  }
  function refresh() {
    assignPages();
    $('currentCopy').textContent = currentId();
    $('pageBadge').textContent = state.scans.length + (state.scans.length === 1 ? ' page' : ' pages');
    $('pagesCount').textContent = state.scans.length;
    $('copiesCount').textContent = new Set(state.scans.map(s=>s.copy)).size;
    $('versosCount').textContent = state.scans.filter(s=>s.side==='verso').length;
    $('exportZip').disabled = !state.scans.length;
    $('clear').disabled = !state.scans.length;
    $('snap').disabled = !state.stream || state.busy || state.scans.length >= MaxPages;
    $('snap').textContent = countFor(currentId()) ? '📷 Photographier cette page' : '📷 Photographier la première page';
    const view = $('scans');
    view.replaceChildren();
    if (!state.scans.length) { const e = document.createElement('div'); e.className='emptyScans'; e.textContent='Aucune page numérisée pour le moment.'; view.append(e); return; }
    for (let i=state.scans.length-1;i>=0;i--) {
      const s = state.scans[i];
      const card = document.createElement('div'); card.className='scan';
      const img = document.createElement('img'); img.src=s.url; img.loading='lazy'; img.alt=`Copie ${s.copy}, feuille ${s.sheet}, ${s.side}`;
      const details = document.createElement('div'); details.className='detail';
      const detailRow = document.createElement('div'); const label=document.createElement('strong');
      label.textContent=`${s.copy} · F${s.sheet} ${s.side}`;
      const del=document.createElement('button');del.textContent='Retirer';del.type='button';del.setAttribute('aria-label',`Retirer la page ${s.page} de la copie ${s.copy}`);
      del.addEventListener('click',()=>{if(!window.confirm('Retirer cette image du lot ?')) return;URL.revokeObjectURL(s.url);state.scans.splice(state.scans.indexOf(s),1);state.gate.reset();refresh();status('Page retirée. Prenez manuellement une nouvelle première photo pour réactiver la détection automatique.');});
      detailRow.append(label,del);
      const sub=document.createElement('small');sub.textContent=`Page ${s.page} · ${s.origin==='camera'?'Caméra':'Import'} · ${s.trimestre}`;
      details.append(detailRow,sub);card.append(img,details);view.append(card);
    }
  }
  function flash(){const el=$('freeze');el.hidden=false;setTimeout(()=>{el.hidden=true;},1000);}
  function asJpeg(canvas) {return new Promise((resolve,reject)=>canvas.toBlob((blob)=>blob?resolve(blob):reject(Error('Compression impossible')),'image/jpeg',.82));}
  function fit(w,h){const scale=Math.min(1,1600/Math.max(w,h));return [Math.max(1,Math.round(w*scale)),Math.max(1,Math.round(h*scale))];}
  async function normalizeImported(file) {
    if(!['image/jpeg','image/png','image/webp'].includes(file.type)) throw Error('Format de photo non pris en charge');
    if(file.size>12*1024*1024) throw Error('Photo supérieure à 12 Mo');
    let bitmap=null; let image=null; let url=null;
    try {
      if ('createImageBitmap' in window) {bitmap=await createImageBitmap(file); image=bitmap;}
      else { url=URL.createObjectURL(file); image=new Image(); image.src=url; await image.decode(); }
      const [w,h]=fit(image.width||image.naturalWidth,image.height||image.naturalHeight);
      const canvas=document.createElement('canvas');canvas.width=w;canvas.height=h;
      canvas.getContext('2d').drawImage(image,0,0,w,h);
      return await asJpeg(canvas); // Nettoie les métadonnées EXIF des originaux importés.
    } finally {bitmap?.close();if(url)URL.revokeObjectURL(url);}
  }
  function addScan(blob,origin) {
    if(state.scans.length>=MaxPages)throw Error(`Limite de ${MaxPages} pages par lot atteinte. Exportez le lot.`);
    const copy=currentId();
    const n=countFor(copy)+1;
    state.scans.push({blob,url:URL.createObjectURL(blob),copy,page:n,...Core.captureSide(n,$('duplex').checked),duplex:$('duplex').checked,trimestre:Core.safeTrimestre($('trimestre').value),origin,at:new Date().toISOString()});
    refresh();
    batchStatus(`${state.scans.length} page(s) enregistrée(s). Vérifiez le cadrage de chaque miniature. Exportez votre ZIP avant de fermer la page.`);
  }
  async function capture(isAuto=false,sampled=null) {
    if(!cameraRunning() || state.busy) return;
    if(state.scans.length>=MaxPages){status('Limite du lot atteinte : exportez puis effacez avant de recommencer.');return;}
    state.busy=true;refresh();
    try {
      const original=sampled||sample();
      const [w,h]=fit(video.videoWidth,video.videoHeight);
      state.captureCanvas.width=w;state.captureCanvas.height=h;
      captureCtx.drawImage(video,0,0,w,h);
      const blob=await asJpeg(state.captureCanvas);
      addScan(blob,'camera');
      state.gate.onCaptured(original || sample());
      flash();
      status(isAuto?'✅ Nouvelle page capturée automatiquement. Tournez la feuille suivante.':'✅ Première capture enregistrée. Tournez la feuille : le mode auto peut capturer la suivante.');
    } catch(e){status(`Impossible de prendre la photo : ${e.message}`);state.gate.reset();}
    finally{state.busy=false;refresh();}
  }
  function tick() {
    if(!cameraRunning() || state.busy || !$('auto').checked || document.hidden) return;
    const s=sample();
    if(s && state.gate.update(s, performance.now())) capture(true,s);
  }
  async function startCamera() {
    if(state.stream)return;
    if(!navigator.mediaDevices?.getUserMedia){status('Caméra indisponible : utilisez une URL HTTPS ou localhost, puis autorisez la caméra.');return;}
    $('cameraStart').disabled=true;status('Demande d’autorisation de la caméra…');
    try {
      state.stream=await navigator.mediaDevices.getUserMedia({audio:false,video:{facingMode:{ideal:'environment'},width:{ideal:1920},height:{ideal:1440}}});
      video.srcObject=state.stream;
      await video.play();
      video.classList.add('active');$('frameEmpty').hidden=true;
      $('camBadge').textContent='Caméra active';$('camBadge').classList.add('live');
      $('cameraStop').disabled=false;
      state.gate.reset();state.timer=setInterval(tick,260);
      status('Caméra active. Placez la première copie dans le cadre et appuyez sur « Photographier la première page ».');
    } catch(e) {
      state.stream?.getTracks().forEach(t=>t.stop());state.stream=null;
      status('Accès caméra impossible. Vérifiez les autorisations Chrome et HTTPS, ou importez des photos. ('+e.name+')');
    } finally {$('cameraStart').disabled=!!state.stream;refresh();}
  }
  function stopCamera(){
    clearInterval(state.timer);state.timer=null;
    state.stream?.getTracks().forEach(t=>t.stop());state.stream=null;
    video.pause();video.srcObject=null;video.classList.remove('active');$('frameEmpty').hidden=false;
    state.gate.reset();$('camBadge').textContent='Arrêtée';$('camBadge').classList.remove('live');
    $('cameraStop').disabled=true;$('cameraStart').disabled=false;refresh();status('Caméra arrêtée. Les photos déjà prises restent en mémoire jusqu’à export ou fermeture.');
  }
  function download(blob,name) {
    const url=URL.createObjectURL(blob),a=document.createElement('a');
    a.href=url;a.download=name;document.body.append(a);a.click();a.remove();
    setTimeout(()=>URL.revokeObjectURL(url),30000);
  }
  function csvEscape(value){return '"'+String(value).replaceAll('"','""')+'"';}
  async function exportZip() {
    if(!state.scans.length)return;
    const button=$('exportZip');button.disabled=true;button.textContent='Préparation de l’archive…';
    try {
      const records=[],files=[];
      for(const s of state.scans){
        const path=`images/${s.copy}/page-${String(s.page).padStart(3,'0')}-${s.side}.jpg`;
        files.push({name:path,bytes:new Uint8Array(await s.blob.arrayBuffer())});
        records.push({copie:s.copy,trimestre:s.trimestre,page:s.page,feuille:s.sheet,face:s.side,fichier:path,origine:s.origin,date_capture:s.at});
      }
      const cols=['copie','trimestre','page','feuille','face','fichier','origine','date_capture'];
      const csv='\ufeff'+cols.join(',')+'\r\n'+records.map(r=>cols.map(c=>csvEscape(r[c])).join(',')).join('\r\n')+'\r\n';
      files.push({name:'inventaire.csv',bytes:csv});
      files.push({name:'manifest.json',bytes:JSON.stringify({schema:Core.VERSION,generatedAt:new Date().toISOString(),pages:records,notes:'Aucun score ni donnée nominative. Validation requise avant usage scolaire.'},null,2)});
      download(window.ScanGradeZip.zip(files),`BOOTO_ScanGrade_${Core.safeTrimestre($('trimestre').value)}_${new Date().toISOString().slice(0,10)}.zip`);
      batchStatus('✅ Archive générée. Vérifiez qu’elle apparaît dans les téléchargements de la tablette avant d’effacer le lot.');
    } catch(e){batchStatus('Échec de l’export : '+e.message);}
    finally{button.textContent='⬇ Exporter le lot ZIP';refresh();}
  }
  function clearLot() {
    if(!window.confirm('Effacer définitivement les pages de cette session ? Vérifiez d’abord votre archive ZIP.'))return;
    for(const s of state.scans) URL.revokeObjectURL(s.url);
    state.scans=[];state.copyNum=1;state.gate.reset();refresh();batchStatus('Lot vidé. Aucune copie conservée par cette application.');status('Lot vide. Reprenez manuellement la première photographie.');
  }
  $('cameraStart').addEventListener('click',startCamera);
  $('cameraStop').addEventListener('click',stopCamera);
  $('snap').addEventListener('click',()=>capture());
  $('newCopy').addEventListener('click',()=>{
    if(!countFor(currentId())){batchStatus('La copie courante est vide : ajoutez d’abord sa première page.');return;}
    state.copyNum++;
    state.gate.reset();refresh();
    status('Nouvelle copie '+currentId()+'. Photographiez manuellement sa première page pour activer la capture automatique des suivantes.');
  });
  $('files').addEventListener('change',async(e)=>{
    const incoming=[...e.target.files];
    if(!incoming.length)return;
    if(state.busy)return;
    state.busy=true;
    try {
      for(const file of incoming){
        if(state.scans.length>=MaxPages)throw Error('Limite de pages atteinte : exportez le lot.');
        const blob=await normalizeImported(file);addScan(blob,'import');
      }
      state.gate.reset();status(`${incoming.length} photo(s) importée(s). Capture automatique réinitialisée : prenez une photo manuelle pour la réactiver.`);
    } catch(err){status(`Import incomplet : ${err.message}`);}finally{state.busy=false;e.target.value='';refresh();}
  });
  $('duplex').addEventListener('change',()=>{
    // Le mode n'est modifié que pour les prises suivantes ; avertir l'utilisateur.
    batchStatus('Mode choisi pour les prochaines pages uniquement. Pour éviter des séquences ambiguës, ne changez pas de mode au milieu d’une copie.');
  });
  $('exportZip').addEventListener('click',exportZip);
  $('clear').addEventListener('click',clearLot);
  window.addEventListener('pagehide',()=>{state.stream?.getTracks().forEach(t=>t.stop());for(const s of state.scans)URL.revokeObjectURL(s.url);});
  refresh();
})();
