import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const html = fs.readFileSync(path.resolve(here, '..', 'index.html'), 'utf8');
const blocks = [...html.matchAll(/<script(?![^>]*\bsrc=)[^>]*>([\s\S]*?)<\/script>/gi)].map(match => match[1]);

for (const [index, source] of blocks.entries()) {
  try {
    new Function(source);
  } catch (error) {
    throw new Error(`Inline script ${index + 1} failed to compile: ${error.message}`);
  }
}

console.log(`Compiled ${blocks.length} inline script blocks`);
