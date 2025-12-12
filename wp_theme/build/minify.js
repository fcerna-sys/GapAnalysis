const fs = require('fs');
const path = require('path');
const CleanCSS = require('clean-css');
const { minify } = require('terser');

const themeDir = path.join(__dirname, '..');
const assetsDir = path.join(themeDir, 'assets');

// Minificar CSS
function minifyCSS() {
    const cssDir = path.join(assetsDir, 'css');
    if (!fs.existsSync(cssDir)) return;
    
    fs.readdirSync(cssDir).forEach(file => {
        if (file.endsWith('.css') && !file.endsWith('.min.css')) {
            const filePath = path.join(cssDir, file);
            const content = fs.readFileSync(filePath, 'utf8');
            const minified = new CleanCSS({}).minify(content).styles;
            const minPath = filePath.replace('.css', '.min.css');
            fs.writeFileSync(minPath, minified);
            console.log(`✓ Minificado: ${file}`);
        }
    });
}

// Minificar JS
function minifyJS() {
    const jsDir = path.join(assetsDir, 'js');
    if (!fs.existsSync(jsDir)) return;
    
    fs.readdirSync(jsDir).forEach(file => {
        if (file.endsWith('.js') && !file.endsWith('.min.js')) {
            const filePath = path.join(jsDir, file);
            const content = fs.readFileSync(filePath, 'utf8');
            minify(content).then(result => {
                const minPath = filePath.replace('.js', '.min.js');
                fs.writeFileSync(minPath, result.code);
                console.log(`✓ Minificado: ${file}`);
            }).catch(err => {
                console.error(`Error minificando ${file}:`, err);
            });
        }
    });
}

minifyCSS();
minifyJS();
