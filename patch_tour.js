const fs = require('fs');
let html = fs.readFileSync('html_template.py', 'utf8');

// Replace alerts with showToast to prevent silent mobile blocking
html = html.replace(/alert\('Tur sistemi kütüphanesi yüklenemedi! \(İnternet bağlantınızı kontrol edin\)'\);/g, "if(typeof showToast==='function') showToast('Kütüphane Yüklenemedi!');");
html = html.replace(/alert\('Tur için ekranda geçerli hiçbir element bulunamadı!'\);/g, "if(typeof showToast==='function') showToast('Ekranda hedef bulunamadı!');");
html = html.replace(/alert\('Tur sistemi başlatılırken hata oluştu: ' \+ e\.message\);/g, "if(typeof showToast==='function') showToast('Hata: ' + e.message);");

// Ensure driver.start is wrapped with a toast
if (html.includes('this.driverInstance.start();') && !html.includes('showToast(\'Tur Başlıyor...\')')) {
    html = html.replace('this.driverInstance.start();', "if(typeof showToast==='function') showToast('Tur Başlıyor...', 'success');\n            this.driverInstance.start();");
}

// Add CSS to force driver overlay visibility just in case
if (!html.includes('#driver-page-overlay')) {
    const cssToAdd = `
        /* Force Driver.js Overlay Visibility */
        div#driver-page-overlay {
            z-index: 999999 !important;
            background: rgba(0,0,0,0.8) !important;
        }
        .driver-highlighted-element {
            z-index: 1000000 !important;
            pointer-events: auto !important;
        }
        div#driver-popover-item {
            z-index: 1000001 !important;
        }
    `;
    html = html.replace('</style>', cssToAdd + '\n    </style>');
}

fs.writeFileSync('html_template.py', html);
console.log('Successfully patched html_template.py');
