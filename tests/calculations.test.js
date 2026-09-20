'use strict';

const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const { calculateDose, packageOrderAmount, singleDose, validWeight, validAgeYears } = require('../dose-calculations.js');

const data = JSON.parse(fs.readFileSync(path.join(__dirname, '..', 'peds_drugs.json'), 'utf8'));
const drug = id => data.drugs.find(item => item.id === id);
const close = (actual, expected, label) => assert.ok(Math.abs(actual - expected) < 1e-9, `${label}: ${actual} !== ${expected}`);

let result = singleDose(20, 1, 50);
close(result.mg, 20, 'Ketamine IV initial mg');
close(result.ml, 0.4, 'Ketamine original solution mL');

result = singleDose(20, 0.5, 50);
close(result.mg, 10, 'Ketamine IV supplemental mg');
close(result.ml, 0.2, 'Ketamine supplemental original solution mL');

result = singleDose(20, 1, 10);
close(result.mg, 20, 'Ketamine diluted mg unchanged');
close(result.ml, 2, 'Ketamine confirmed 10 mg/mL solution mL');

let order = packageOrderAmount(80, 50, 10);
close(order.originalMl, 1.6, 'Ketamine IM initial original c.c.');
close(order.packageFraction, 0.16, 'Ketamine IM initial Vial fraction');

order = packageOrderAmount(40, 50, 10);
close(order.originalMl, 0.8, 'Ketamine IM supplemental original c.c.');
close(order.packageFraction, 0.08, 'Ketamine IM supplemental Vial fraction');

order = packageOrderAmount(20, 50, 10);
close(order.originalMl, 0.4, 'Ketamine diluted IV original c.c.');
close(order.packageFraction, 0.04, 'Ketamine diluted IV Vial fraction');
assert.equal(packageOrderAmount(20, 0, 10), null);

result = calculateDose(drug('antiphen_syrup'), drug('antiphen_syrup').calc, 20, 5);
assert.deepEqual(result.mgRange, [200, 300]);
close(result.mlRange[0], 20 / 2.4, 'Acetaminophen 10 mg/kg mL');
close(result.mlRange[1], 20 / 1.6, 'Acetaminophen 15 mg/kg mL');

result = calculateDose(drug('idefen_syrup'), drug('idefen_syrup').calc, 20, 5);
assert.deepEqual(result.mgRange, [100, 200]);
assert.deepEqual(result.mlRange, [5, 10]);

result = calculateDose(drug('antiphen_syrup'), drug('antiphen_syrup').calc, 120, 12);
assert.deepEqual(result.mgRange, [1000, 1000], 'single-dose ceiling is applied before mL conversion');
close(result.mlRange[0], 1000 / 24, 'capped dose mL');

assert.equal(validWeight(0), false);
assert.equal(validWeight(-1), false);
assert.equal(validWeight(0.1), true);
assert.equal(validWeight(121), false);
assert.equal(validAgeYears(-1), false);
assert.equal(validAgeYears(0), true);
assert.equal(validAgeYears(18), true);
assert.equal(validAgeYears(18.1), false);

console.log('Calculation tests passed');
