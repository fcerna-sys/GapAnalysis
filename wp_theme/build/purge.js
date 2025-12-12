const PurgeCSS = require('purgecss').PurgeCSS;
const fs = require('fs');
const path = require('path');

const themeDir = path.join(__dirname, '..');
const assetsDir = path.join(themeDir, 'assets');
const cssDir = path.join(assetsDir, 'css');

const content = [
    'c:\laragon\www\img2html\wp_theme/**/*.html',
    'c:\laragon\www\img2html\wp_theme/**/*.php',
    'c:\laragon\www\img2html\wp_theme/blocks/**/*.php',
    'c:\laragon\www\img2html\wp_theme/templates/**/*.html',
    'c:\laragon\www\img2html\wp_theme/parts/**/*.html',
    'c:\laragon\www\img2html\wp_theme/patterns/**/*.php'
];

// Listar archivos CSS desde el directorio

const safelist = [
    /^img2html-/,
    /wp-/,
    /has-/,
    /is-/,
    /align/,
    /^screen-reader/,
    /^sr-only/
];

async function purge() {
    if (!fs.existsSync(cssDir)) return;
    const files = fs.readdirSync(cssDir).filter(f => f.endsWith('.css') && !f.endsWith('.min.css') && !f.endsWith('.purged.css'));
    for (const file of files) {
        const filePath = path.join(cssDir, file);
        const results = await new PurgeCSS().purge({
            content: content,
            css: [filePath],
            safelist: safelist,
            defaultExtractor: (content) => content.match(/[A-Za-z0-9-_/:]*[A-Za-z0-9-_/]/g) || []
        });
        if (results && results[0]) {
            const purgedPath = path.join(cssDir, file.replace('.css', '.purged.css'));
            fs.writeFileSync(purgedPath, results[0].css);
            console.log(`✓ Purged: ${file}`);
        }
    }
}

purge();
