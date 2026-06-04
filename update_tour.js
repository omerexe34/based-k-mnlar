const fs = require('fs');
let html = fs.readFileSync('html_template.py', 'utf8');
const startStr = 'startTour: function() {';
const endStr = 'markCompleted: function() {';
const startIdx = html.indexOf(startStr);
const endIdx = html.indexOf(endStr);

if(startIdx !== -1 && endIdx !== -1) {
    const newCode = `startTour: function() {
        if (this.isRunning) {
            this.isRunning = false;
            if(this.driverInstance) { try { this.driverInstance.reset(); } catch(e){} }
        }
        
        if (typeof window.Driver !== 'function') {
            alert('Tur sistemi kütüphanesi yüklenemedi! (İnternet bağlantınızı kontrol edin)');
            return; 
        }
        
        this.isRunning = true;

        try {
            this.driverInstance = new window.Driver({
                animate: true,
                opacity: 0.8,
                padding: 5,
                allowClose: true,
                overlayClickNext: false,
                doneBtnText: 'Bitir ✔',
                closeBtnText: 'Kapat',
                nextBtnText: 'İleri ➔',
                prevBtnText: '⬅ Geri',
                onReset: () => {
                    this.isRunning = false;
                    this.markCompleted();
                }
            });

            const steps = [
                {
                    element: 'header',
                    popover: {
                        title: 'Hoş Geldin! 🚴',
                        description: 'FreeriderTR\\'ye katıldığın için harika hissediyoruz. Uygulamayı en iyi şekilde kullanman için detaylı bir tura çıkalım.',
                        position: 'bottom'
                    }
                },
                {
                    element: '#map',
                    popover: {
                        title: '🗺️ Harita & Noktalar',
                        description: 'Buradan Türkiye\\'deki tüm trail, rampa ve bisikletçi noktalarını görebilirsin. Dilersen kendi noktalarını da ekleyebilirsin.',
                        position: 'bottom'
                    },
                    onNext: () => { try { switchTab(0); } catch(e){} }
                },
                {
                    element: '#bnav-9',
                    popover: {
                        title: '🎯 Görevler & XP',
                        description: 'Sürüş yaparak ve topluluğa katkı sağlayarak görevleri tamamla, XP kazan ve liderlik tablosunda yüksel!',
                        position: 'top'
                    },
                    onNext: () => { try { switchTab(9); } catch(e){} }
                },
                {
                    element: '#bnav-3',
                    popover: {
                        title: '📹 Reels & Videolar',
                        description: 'Topluluğun en iyi sürüş videolarını izle veya kendi aksiyon dolu anlarını paylaşarak ilham ol.',
                        position: 'top'
                    },
                    onNext: () => { try { switchTab(3); } catch(e){} }
                },
                {
                    element: '#bnav-ai',
                    popover: {
                        title: '🤖 AI Asistan',
                        description: 'Yapay zeka ile bisiklet topla, teknik destek al ve parçaların uyumluluğunu ücretsiz analiz et.',
                        position: 'top'
                    }
                },
                {
                    element: '#bnav-1',
                    popover: {
                        title: '💬 Sohbet Sistemi',
                        description: 'Diğer sürücülerle anlık mesajlaş, etkinliklere katıl ve toplulukla sürekli iletişimde kal.',
                        position: 'top'
                    },
                    onNext: () => { try { switchTab(1); } catch(e){} }
                },
                {
                    element: '#bnav-7',
                    popover: {
                        title: '👤 Profil & Garaj',
                        description: 'Kendine ait Dijital Garajını oluştur, başarımlarını takip et ve tüm ayarlarını buradan yönet.',
                        position: 'top'
                    },
                    onNext: () => { try { switchTab(7); } catch(e){} }
                }
            ];

            const validSteps = steps.filter(step => {
                try {
                    return document.querySelector(step.element) !== null;
                } catch(e) { return false; }
            });

            if (validSteps.length === 0) {
                alert('Tur için ekranda geçerli hiçbir element bulunamadı!');
                return;
            }

            this.driverInstance.defineSteps(validSteps);
            this.driverInstance.start();

        } catch(e) {
            console.error('Driver initialization error:', e);
            alert('Tur sistemi başlatılırken hata oluştu: ' + e.message);
        }
    },
    `;
    
    html = html.substring(0, startIdx) + newCode + html.substring(endIdx);
    fs.writeFileSync('html_template.py', html);
    console.log('Successfully replaced startTour!');
} else {
    console.log('Could not find start/end indices.');
}
