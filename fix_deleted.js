const fs = require('fs');
let html = fs.readFileSync('html_template.py', 'utf8');

const missingCode = `
    <!-- iOS PWA Support -->
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <meta name="apple-mobile-web-app-title" content="FreeriderTR">
    <link rel="apple-touch-icon" href="https://cdn.freeridertr.com.tr/profil%20resmi/unnamed.jpg">
    
    <!-- Onboarding System (Driver.js) & Canvas Confetti -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/driver.js@0.9.8/dist/driver.min.css"/>
    <script src="https://cdn.jsdelivr.net/npm/driver.js@0.9.8/dist/driver.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"></script>
    
    <style>
        /* Modern Premium Driver.js Customizations */
        .driver-popover {
            background: rgba(15, 15, 20, 0.85) !important;
            backdrop-filter: blur(16px) saturate(180%) !important;`;

if (!html.includes('<!-- iOS PWA Support -->')) {
    html = html.replace('            backdrop-filter: blur(16px) saturate(180%) !important;', missingCode);
    fs.writeFileSync('html_template.py', html);
    console.log('Fixed deleted code.');
}
