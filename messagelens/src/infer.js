/* Même normalisation ASCII et même calcul TF-IDF que le pipeline Python. */
function normalize(text){return (String(text).toLowerCase().replace(/https?:\/\/\S+|www\.\S+/g,' url ').replace(/[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}/g,' email ').replace(/\p{Decimal_Number}+/gu,' number ').match(/[a-z]{2,}/g)||[]).join(' ');}
function predict(text,m){
 const vocab=new Map(m.terms.map((t,i)=>[t,i])),counts=new Map();
 for(const t of normalize(text).split(' ')){if(vocab.has(t)){const i=vocab.get(t);counts.set(i,(counts.get(i)||0)+1);}}
 let weights=[...counts].map(([i,c])=>[i,c*m.idf[i]]),norm=Math.sqrt(weights.reduce((s,[i,w])=>s+w*w,0));
 const parts=norm?weights.map(([i,w])=>({term:m.terms[i],value:w/norm*m.coef[i]})):[];
 const logit=m.intercept+parts.reduce((s,p)=>s+p.value,0),score=1/(1+Math.exp(-Math.max(-700,Math.min(700,logit))));
 return {score,label:score>=m.threshold?'spam':'ham',known_terms:counts.size,logit,contributions:parts.sort((a,b)=>Math.abs(b.value)-Math.abs(a.value)).slice(0,8)};
}
if(typeof module!=='undefined')module.exports={normalize,predict};
