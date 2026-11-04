const fs = require('fs');
const path = require('path');

const rootDir = __dirname;
const distDir = path.join(rootDir, 'dist');

console.log('Starting static build for Cloudflare Pages...');

// Remove dist if exists, then recreate
if (fs.existsSync(distDir)) {
  fs.rmSync(distDir, { recursive: true, force: true });
}
fs.mkdirSync(distDir, { recursive: true });

// Items to ignore when copying to dist
const ignored = new Set([
  '.git',
  '.gitignore',
  'node_modules',
  'dist',
  'package.json',
  'package-lock.json',
  'build.js',
  'apply_optimizations.py',
  '__pycache__'
]);

const items = fs.readdirSync(rootDir);
let copiedCount = 0;

for (const item of items) {
  if (ignored.has(item) || item.endsWith('.zip')) continue;
  const src = path.join(rootDir, item);
  const dest = path.join(distDir, item);
  fs.cpSync(src, dest, { recursive: true });
  copiedCount++;
}

console.log(`Build completed successfully: ${copiedCount} root items copied into dist/`);
