// Calculs partagés par l'interface et la vérification Node.
export function select(cells, filters={}) {
  const index={market:1,region:2,category:3,segment:4};
  return cells.filter(c=>Object.entries(filters).every(([key,value])=>!value||(key==='year'?c[0].slice(0,4)===value:c[index[key]]===value)));
}
export function metrics(cells){
  const orders=new Set(),returned=new Set();let sales=0,profit=0,quantity=0,lines=0;
  for(const c of cells){sales+=c[5];profit+=c[6];quantity+=c[7];lines+=c[8];c[9].forEach(v=>orders.add(v));c[10].forEach(v=>returned.add(v));}
  return {sales,profit,quantity,lines,orders:orders.size,returned:returned.size,margin:sales?profit/sales:null,basket:orders.size?sales/orders.size:null,returnRate:orders.size?returned.size/orders.size:null};
}
export function group(cells,index){const map=new Map();for(const c of cells){if(!map.has(c[index]))map.set(c[index],[]);map.get(c[index]).push(c);}return [...map].map(([name,rows])=>({name,...metrics(rows)}));}
