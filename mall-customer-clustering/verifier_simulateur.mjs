import fs from 'node:fs';
import assert from 'node:assert/strict';
import {assign} from './affecter.mjs';
const model=JSON.parse(fs.readFileSync(new URL('./models/centroides.json',import.meta.url)));
const examples=JSON.parse(fs.readFileSync(new URL('./reports/exemples_synthetiques.json',import.meta.url)));
for(const example of examples){const result=assign(example.point,model);assert.equal(result.group,example.group);assert.ok(Math.abs(result.distance-example.distance)<1e-12);}
assert.throws(()=>assign([50,101],model));assert.throws(()=>assign([NaN,50],model));
console.log('Affectation JavaScript comparée à Python sur exemples synthétiques ; entrées invalides contrôlées.');
