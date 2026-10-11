import {select,metrics,group} from './engine.mjs';
const ids=['year','market','region','category','segment'];
const $=id=>document.getElementById(id);
const number=v=>v==null?'—':new Intl.NumberFormat('fr-FR',{maximumFractionDigits:0}).format(v);
const money=v=>v==null?'—':new Intl.NumberFormat('fr-FR',{minimumFractionDigits:2,maximumFractionDigits:2}).format(v);
const percent=v=>v==null?'—':new Intl.NumberFormat('fr-FR',{style:'percent',maximumFractionDigits:1}).format(v);
const escape=v=>String(v).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
let data,filtered=[];
function trend(rows){
 const lookup=new Map(group(rows,0).map(r=>[r.name,r]));const year=$('year').value;
 const months=[...new Set(data.cells.map(c=>c[0]))].sort().filter(m=>!year||m.startsWith(year));
 const metric=$('measure').value;const values=months.map(m=>lookup.get(m)?.[metric]||0);
 const min=Math.min(0,...values),max=Math.max(1,...values),w=620,h=270,left=75,right=18,top=18,bottom=44;
 const x=i=>left+i*(w-left-right)/Math.max(1,months.length-1),y=v=>top+(max-v)*(h-top-bottom)/(max-min);
 const points=values.map((v,i)=>`${x(i)},${y(v)}`).join(' ');
 let grid='';for(let i=0;i<5;i++){const v=min+(max-min)*i/4;grid+=`<line x1="${left}" y1="${y(v)}" x2="${w-right}" y2="${y(v)}" stroke="#e4ebf1"/><text x="${left-8}" y="${y(v)+4}" text-anchor="end">${number(v)}</text>`;}
 const ticks=months.map((m,i)=>({m,i})).filter(({m,i})=>i===0||i===months.length-1||m.endsWith('-01'));
 $('trend').innerHTML=rows.length?`<svg class="chart" viewBox="0 0 ${w} ${h}" role="img" aria-label="Évolution mensuelle ${metric==='sales'?'des ventes':'du bénéfice'}, montants en UM. Valeurs dans le tableau mensuel.">${grid}<line x1="${left}" y1="${y(0)}" x2="${w-right}" y2="${y(0)}" stroke="#b9cbd4"/><polyline points="${points}" fill="none" stroke="#168392" stroke-width="2.5"/>${ticks.map(({m,i})=>`<text x="${x(i)}" y="${h-15}" text-anchor="middle">${m}</text>`).join('')}</svg>`:'<p>Aucune donnée pour ces filtres.</p>';
 $('monthly').innerHTML=months.map(m=>`<tr><td>${m}</td><td>${money(lookup.get(m)?.sales||0)}</td><td>${money(lookup.get(m)?.profit||0)}</td></tr>`).join('');
}
function render(){
 const filters=Object.fromEntries(ids.map(id=>[id,$(id).value]));filtered=select(data.cells,filters);const m=metrics(filtered);
 const labels=[['Ventes',`${money(m.sales)} UM`,'Total des lignes filtrées'],['Bénéfice',`${money(m.profit)} UM`,'Montant fourni par la source'],['Marge',percent(m.margin),'Bénéfice / ventes'],['Commandes',number(m.orders),`${number(m.lines)} lignes · ${number(m.quantity)} unités`],['Panier moyen',m.basket==null?'—':`${money(m.basket)} UM`,'Ventes / commandes distinctes'],['Commandes retournées',percent(m.returnRate),`${number(m.returned)} commandes signalées retournées`]];
 $('kpis').innerHTML=labels.map(([label,value,note],i)=>`<article class="kpi"><small>${label}</small><strong class="${i===1&&m.profit<0?'negative':''}">${value}</strong><p>${note}</p></article>`).join('');
 $('status').textContent=`${number(m.lines)} lignes · ${ids.filter(id=>filters[id]).map(id=>filters[id]).join(' / ')||'Toutes les données'} · Montants historiques en UM`;
 const regions=group(filtered,2).sort((a,b)=>b.sales-a.sales);const largest=Math.max(1,...regions.map(r=>r.sales));
 $('regions').innerHTML=regions.map(r=>`<div class="barrow"><span>${escape(r.name)}</span><div class="track" aria-hidden="true"><div class="fill" style="width:${r.sales/largest*100}%"></div></div><span class="barvalue">${number(r.sales)}</span></div>`).join('')||'<p>Aucune donnée.</p>';
 const categories=group(filtered,3).sort((a,b)=>b.sales-a.sales);
 $('categories').innerHTML=categories.map(r=>`<tr><td>${escape(r.name)}</td><td>${money(r.sales)}</td><td class="${r.profit<0?'negative':''}">${money(r.profit)}</td><td>${percent(r.margin)}</td><td>${number(r.orders)}</td><td>${number(r.quantity)}</td></tr>`).join('')||'<tr><td colspan="6">Aucune donnée pour ces filtres.</td></tr>';
 $('export').disabled=!filtered.length;trend(filtered);
}
$('reset').onclick=()=>{ids.forEach(id=>$(id).value='');render();};
$('export').onclick=()=>{
 const quote=v=>'"'+String(v).replaceAll('"','""')+'"';
 const rows=[['month','market','region','category','segment','sales','profit','quantity','lines','distinct_orders_in_cell','returned_orders_in_cell'],...filtered.map(c=>[...c.slice(0,9),c[9].length,c[10].length])];
 const csv='\uFEFF'+rows.map(r=>r.map(quote).join(';')).join('\r\n');const url=URL.createObjectURL(new Blob([csv],{type:'text/csv;charset=utf-8'}));const link=document.createElement('a');link.href=url;link.download='superstore_indicateurs_filtres.csv';link.click();setTimeout(()=>URL.revokeObjectURL(url),1000);
};
try{
 const response=await fetch('./dashboard-data.json');if(!response.ok)throw Error('Données indisponibles');data=await response.json();
 const indexes={market:1,region:2,category:3,segment:4};
 ids.forEach(id=>{const values=[...new Set(data.cells.map(c=>id==='year'?c[0].slice(0,4):c[indexes[id]]))].sort();values.forEach(v=>$(id).add(new Option(v,v)));$(id).onchange=render;});$('measure').onchange=render;render();
}catch(error){$('status').textContent='Le tableau de bord ne peut pas charger ses données. Réessayez depuis le site ou un serveur local.';console.error(error);}
