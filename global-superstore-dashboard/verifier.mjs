import fs from 'node:fs';
import assert from 'node:assert/strict';
import {select,metrics,group} from './web/engine.mjs';
const data=JSON.parse(fs.readFileSync(new URL('./web/dashboard-data.json',import.meta.url)));
const cases=JSON.parse(fs.readFileSync(new URL('./reports/verification_filtres.json',import.meta.url)));
for(const test of cases){const rows=select(data.cells,test.filters);const result=metrics(rows);for(const [key,value] of Object.entries(test.expected)){assert.ok(Math.abs(result[key]-value)<1e-6,`${key}: ${result[key]} != ${value}`);}const categories=group(rows,3);assert.ok(Math.abs(categories.reduce((s,x)=>s+x.sales,0)-result.sales)<1e-6);}
assert.equal(metrics([]).margin,null);assert.equal(metrics([]).returnRate,null);
console.log(`${cases.length} scénarios de filtres vérifiés contre les données source Python ; cas vide et totaux par catégorie vérifiés.`);
