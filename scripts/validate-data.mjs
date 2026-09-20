import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const data = JSON.parse(fs.readFileSync(path.resolve(here, '..', 'peds_drugs.json'), 'utf8'));
const errors = [];
const ids = new Set();
const supportedAvailability = new Set(['available', 'shortage', 'unavailable', 'verification_required']);

for (const [index, drug] of data.drugs.entries()) {
  const at = `drugs[${index}]`;
  for (const key of ['id', 'generic', 'category']) {
    if (!drug[key]) errors.push(`${at}: missing ${key}`);
  }
  if (ids.has(drug.id)) errors.push(`${at}: duplicate id ${drug.id}`);
  ids.add(drug.id);
  if (drug.availability && !supportedAvailability.has(drug.availability.status)) {
    errors.push(`${at}: unknown availability.status ${drug.availability.status}`);
  }
  if (drug.concentration_mg_per_ml !== undefined && !(drug.concentration_mg_per_ml > 0)) {
    errors.push(`${at}: concentration_mg_per_ml must be positive`);
  }
  if (drug.calc?.type?.startsWith('mg_per_kg') && drug.calc.low === undefined) {
    errors.push(`${at}: ${drug.calc.type} requires calc.low`);
  }
  if (!drug.source && !drug.sources?.length) errors.push(`${at}: missing source`);
}

for (const required of ['antiphen_syrup', 'idefen_syrup', 'ketamine', 'midazolam_dormicum', 'citosol', 'chloral_hydrate']) {
  if (!ids.has(required)) errors.push(`missing required drug ${required}`);
}

const midatinBag = data.drugs.find(drug => drug.id === 'midazolam_dormicum');
if (midatinBag?.kmuh_code !== '2MID50' || midatinBag?.concentration_mg_per_ml !== 1 || midatinBag?.package !== '50 mL/Bag = 50 mg/Bag') {
  errors.push('midazolam_dormicum must match current 2MID50 50 mg/50 mL/Bag (1 mg/mL)');
}
if (midatinBag?.availability?.status !== 'available') {
  errors.push('midazolam_dormicum must be marked available');
}

const oldMidatin = data.drugs.find(drug => drug.id === 'midazolam_midatin_5mg_shortage');
if (oldMidatin?.kmuh_code !== '2MIDAT' || oldMidatin?.concentration_mg_per_ml !== 5) {
  errors.push('old Midatin reference must retain 2MIDAT 15 mg/3 mL (5 mg/mL)');
}
if (oldMidatin?.availability?.status !== 'shortage') {
  errors.push('old Midatin 2MIDAT must remain marked shortage');
}

const ketamine = data.drugs.find(drug => drug.id === 'ketamine');
if (ketamine?.kmuh_code !== '2KET10' || ketamine?.concentration_mg_per_ml !== 50 || ketamine?.order_unit_volume_ml !== 10 || ketamine?.order_unit !== 'Vial') {
  errors.push('ketamine ordering conversion must use HIS code 2KET10, 50 mg/mL original solution and 10 mL/Vial');
}
const ketamineSedationRoutes = ketamine?.protocols
  ?.filter(protocol => protocol.use === '處置鎮靜')
  .map(protocol => protocol.route);
if (JSON.stringify(ketamineSedationRoutes) !== JSON.stringify(['IM', 'IV'])) {
  errors.push('ketamine procedural sedation routes must default to IM with IV as the second option');
}

if (errors.length) {
  console.error(errors.join('\n'));
  process.exit(1);
}
console.log(`Validated ${data.drugs.length} drugs; IDs unique and required fields present`);
