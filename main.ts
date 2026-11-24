// 24 November 2026 — World News in One Image.
// Runs on Node 22 with the standard library alone. It decodes the bundled
// entry.png.b64 (a 1024x1024 infographic of the 24 November 2026 stories in
// news.json, rendered by build_image.py) and writes it to /output/entry.png.
// No network, randomness or timestamps: every run writes identical PNG bytes.
// Try it locally with: MAKEFUN_OUTPUT_DIR=out node main.ts

import { mkdirSync } from 'node:fs';
import { readFileSync } from 'node:fs';
import { writeFileSync } from 'node:fs';
import { join } from 'node:path';

function main() {
  const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
  const encoded = readFileSync(
    new URL('./entry.png.b64', import.meta.url), 'utf8',
  ).trim();
  const png = Buffer.from(encoded, 'base64');
  if (png.subarray(0, 8).toString('hex') !== '89504e470d0a1a0a') {
    throw new Error('entry.png.b64 did not decode to a PNG');
  }
  mkdirSync(outDir, { recursive: true });
  writeFileSync(join(outDir, 'entry.png'), png);
}

main();
