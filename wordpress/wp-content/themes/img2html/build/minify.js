const fs = require('fs');
const path = require('path');
const CleanCSS = require('clean-css');
const terser = require('terser');

const themeDir = process.cwd();
const componentsDir = path.join(themeDir, 'assets', 'blocks', 'components');

function listFiles(dir) {
  if (!fs.existsSync(dir)) return [];
  return fs.readdirSync(dir)
    .map(f => path.join(dir, f))
    .filter(p => fs.statSync(p).isFile());
}

function minifyCss(file) {
  const src = fs.readFileSync(file, 'utf8');
  const output = new CleanCSS({}).minify(src).styles;
  const outPath = file.replace(/\.css$/, '.min.css');
  fs.writeFileSync(outPath, output, 'utf8');
}

function minifyJs(file) {
  const src = fs.readFileSync(file, 'utf8');
  const result = terser.minify(src);
  if (result.error) throw result.error;
  const outPath = file.replace(/\.js$/, '.min.js');
  fs.writeFileSync(outPath, result.code || '', 'utf8');
}

const files = listFiles(componentsDir);
files
  .filter(f => f.endsWith('.css') && !f.endsWith('.min.css'))
  .forEach(minifyCss);
files
  .filter(f => f.endsWith('.js') && !f.endsWith('.min.js'))
  .forEach(minifyJs);
