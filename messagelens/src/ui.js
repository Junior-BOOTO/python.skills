let model=null;
const form=document.getElementById('lens-form'),status=document.getElementById('status');
fetch('messagelens-assets/model.json').then(r=>{if(!r.ok)throw Error('model');return r.json();}).then(m=>{model=m;status.textContent='Modèle chargé. Saisissez un SMS anglais fictif pour essayer.';document.getElementById('analyze').disabled=false;}).catch(()=>{status.textContent='Modèle indisponible. Réessayez après avoir rechargé la page.';});
form.addEventListener('submit',event=>{
 event.preventDefault();const text=document.getElementById('message').value;
 if(!text.trim()){status.textContent='Saisissez un message.';return;}
 if(!model){status.textContent='Modèle en cours de chargement.';return;}
 const r=predict(text,model);status.textContent=r.known_terms?('Classe prédite : '+r.label+'. Score du modèle : '+r.score.toFixed(3)+' ; seuil : '+model.threshold+'. Ce score n’est pas une preuve de fraude.'):'Aucun terme connu : le modèle ne peut pas interpréter utilement ce texte.';
 const list=document.getElementById('reasons');list.replaceChildren();
 for(const c of r.contributions){const li=document.createElement('li');li.textContent=c.term+' : '+(c.value>=0?'+':'')+c.value.toFixed(3)+' sur le logit, vers '+(c.value>=0?'spam':'ham');list.appendChild(li);}
 document.getElementById('intercept').textContent='Intercept : '+model.intercept.toFixed(3)+'. Les contributions affichées sont les huit plus fortes au maximum.';
});
document.querySelectorAll('[data-example]').forEach(b=>b.addEventListener('click',()=>{document.getElementById('message').value=b.dataset.example;form.requestSubmit();}));
document.getElementById('compare').addEventListener('click',()=>{
 const a=normalize(document.getElementById('message').value),b=normalize(document.getElementById('second').value);
 function shingles(s){const z=new Set();for(let i=0;i<s.length-2;i++)z.add(s.slice(i,i+3));return z;}
 const x=shingles(a),y=shingles(b),u=new Set([...x,...y]);let n=0;for(const t of x)if(y.has(t))n++;
 document.getElementById('similarity').textContent=u.size?'Similarité Jaccard des trigrammes normalisés : '+(n/u.size).toFixed(3)+'. Une ressemblance ne prouve ni spam ni plagiat.':'Textes trop courts ou vides pour cette comparaison.';
});
