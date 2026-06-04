const fs = require('fs');
let html = fs.readFileSync('html_template.py', 'utf8');

// 1. Remove Driver.js and add Intro.js
html = html.replace('<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/driver.js@0.9.8/dist/driver.min.css"/>', '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/intro.js/7.2.0/introjs.min.css"/>');
html = html.replace('<script src="https://cdn.jsdelivr.net/npm/driver.js@0.9.8/dist/driver.min.js"></script>', '<script src="https://cdnjs.cloudflare.com/ajax/libs/intro.js/7.2.0/intro.min.js"></script>');

// 2. Remove old custom Driver CSS
const cssStart = html.indexOf('/* Modern Premium Driver.js Customizations */');
if (cssStart !== -1) {
    const cssEnd = html.indexOf('</style>', cssStart);
    if (cssEnd !== -1) {
        html = html.substring(0, cssStart) + `
        /* Intro.js Customizations */
        .introjs-tooltip {
            background: rgba(15, 15, 20, 0.95) !important;
            backdrop-filter: blur(16px) saturate(180%) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            border-radius: 20px !important;
            color: #fff !important;
            box-shadow: 0 20px 50px rgba(0,0,0,0.8) !important;
        }
        .introjs-tooltiptext { color: #d4d4d8 !important; font-size: 14px !important; }
        .introjs-tooltipbuttons { border-top: 1px solid rgba(255,255,255,0.1) !important; }
        .introjs-button { background: rgba(255,255,255,0.1) !important; color: white !important; border: none !important; text-shadow: none !important; border-radius: 8px !important; }
        .introjs-button:hover { background: #0284c7 !important; }
        .introjs-overlay { z-index: 999999 !important; }
        .introjs-helperLayer { z-index: 999998 !important; }
        ` + html.substring(cssEnd);
    }
}

// 3. Rewrite OnboardingManager to use Intro.js
const tourStart = html.indexOf('startTour: function() {');
const tourEnd = html.indexOf('markCompleted: function() {');
if (tourStart !== -1 && tourEnd !== -1) {
    const newTour = `startTour: function() {
        if (typeof introJs !== 'function') {
            if(typeof showToast==='function') showToast('Tur kütüphanesi yüklenemedi!');
            return;
        }
        
        if(typeof showToast==='function') showToast('Uygulama Turu Başlıyor...', 'success');
        
        try {
            const intro = introJs();
            intro.setOptions({
                nextLabel: 'İleri ➔',
                prevLabel: '⬅ Geri',
                doneLabel: 'Bitir ✔',
                showProgress: true,
                exitOnOverlayClick: false,
                steps: [
                    {
                        title: 'Hoş Geldin! 🚴',
                        intro: 'FreeriderTR\\'ye katıldığın için harika hissediyoruz. Uygulamayı en iyi şekilde kullanman için detaylı bir tura çıkalım.'
                    },
                    {
                        element: document.querySelector('#bnav-0'),
                        title: '🗺️ Harita',
                        intro: 'Buradan Türkiye\\'deki tüm trail ve rampa noktalarını görebilirsin.'
                    },
                    {
                        element: document.querySelector('#bnav-1'),
                        title: '💬 Chat',
                        intro: 'Diğer sürücülerle anlık sohbet et ve etkinlik planla.'
                    },
                    {
                        element: document.querySelector('#bnav-9'),
                        title: '🎬 Reels',
                        intro: 'Sürüş videolarını izle veya kendi anlarını paylaş.'
                    },
                    {
                        element: document.querySelector('#bnav-ai'),
                        title: '🤖 AI Asistan',
                        intro: 'Yapay zeka asistanı ile bisikletini topla ve teknik analiz yap.'
                    },
                    {
                        element: document.querySelector('#bnav-7'),
                        title: '👤 Profil & Garaj',
                        intro: 'Kendi dijital garajını oluştur ve rozetlerini takip et.'
                    }
                ]
            });
            
            intro.onbeforechange(function(targetElement) {
                if(!targetElement) return;
                if(targetElement.id === 'bnav-0') switchTab(0);
                if(targetElement.id === 'bnav-1') switchTab(1);
                if(targetElement.id === 'bnav-9') switchTab(9);
                if(targetElement.id === 'bnav-7') switchTab(7);
            });
            
            intro.oncomplete(() => { this.markCompleted(); });
            intro.onexit(() => { this.markCompleted(); });
            
            intro.start();
        } catch(e) {
            if(typeof showToast==='function') showToast('Tur hatası: ' + e.message);
        }
    },
    `;
    html = html.substring(0, tourStart) + newTour + html.substring(tourEnd);
}

// 4. Fix AI Hub (Add direct style modifications to ensure it works)
const aiHubStart = html.indexOf('function openAIHub() {');
const aiHubEnd = html.indexOf('function closeAIHub() {');
if (aiHubStart !== -1 && aiHubEnd !== -1) {
    const newAiHub = `function openAIHub() {
    try {
        if(typeof showToast==='function') showToast("AI Hub Açılıyor...", "info", 1500);
        const overlay = document.getElementById('ai-hub-overlay');
        if(!overlay) {
            if(typeof showToast==='function') showToast("AI Hub HTML elementi bulunamadı!");
            return;
        }
        // Kesin çözüm: Class harici direkt CSS ile force display
        overlay.style.setProperty('display', 'flex', 'important');
        overlay.style.setProperty('opacity', '1', 'important');
        overlay.style.setProperty('z-index', '9999999', 'important');
        overlay.classList.add('show');
        
        backToAIMenu();
    } catch(e) {
        if(typeof showToast==='function') showToast("AI Hata: " + e.message);
    }
}
`;
    html = html.substring(0, aiHubStart) + newAiHub + html.substring(aiHubEnd);
}

// Ensure close AI Hub works with the new forced styles
html = html.replace("document.getElementById('ai-hub-overlay').classList.remove('show');", "document.getElementById('ai-hub-overlay').classList.remove('show'); document.getElementById('ai-hub-overlay').style.display = 'none';");

fs.writeFileSync('html_template.py', html);
console.log('Done!');
