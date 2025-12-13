const fs = require('fs');
const path = require('path');
const { PurgeCSS } = require('purgecss');
const CleanCSS = require('clean-css');

const themeDir = process.cwd();
const componentsDir = path.join(themeDir, 'assets', 'blocks', 'components');

async function purgeCss(file) {
  const contentGlobs = [
    path.join(themeDir, '**/*.php'),
    path.join(themeDir, '**/*.html'),
    path.join(themeDir, 'blocks/**/*.css'),
    path.join(themeDir, 'assets/**/*.js'),
  ];
  const result = await new PurgeCSS().purge({
    content: contentGlobs,
    css: [file],
    safelist: [/^img2html-/, 'alignwide', 'alignfull']
  });
  const css = result && result[0] && result[0].css ? result[0].css : '';
  let minified = new CleanCSS({}).minify(css).styles;
  if (!minified || minified.length === 0) {
    const src = fs.readFileSync(file, 'utf8');
    minified = new CleanCSS({}).minify(src).styles;
  }
  const outPath = file.replace(/\.css$/, '.purged.css');
  fs.writeFileSync(outPath, minified, 'utf8');
}

function listCss(dir) {
  if (!fs.existsSync(dir)) return [];
  return fs.readdirSync(dir)
    .map(f => path.join(dir, f))
    .filter(p => fs.statSync(p).isFile() && p.endsWith('.css'));
}

(async () => {
  const files = listCss(componentsDir);
  for (const f of files) {
    await purgeCss(f);
  }
})();
