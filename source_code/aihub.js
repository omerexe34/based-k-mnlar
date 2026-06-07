
// AI HUB LOGIC
let aiBuildMemory = [];

window.openAIHub = function() {
    try {
        if(typeof showToast==='function') showToast("AI Hub Açılıyor...", "info", 1500);
        const overlay = document.getElementById('ai-hub-overlay');
        if(!overlay) {
            if(typeof showToast==='function') showToast("AI Hub HTML elementi bulunamadı!");
            return;
        }
        
        // Ensure it's on top of everything and part of body directly
        document.body.appendChild(overlay);
        
        // Kesin çözüm: Class harici direkt CSS ile force display
        overlay.style.setProperty('display', 'flex', 'important');
        overlay.style.setProperty('opacity', '1', 'important');
        overlay.style.setProperty('visibility', 'visible', 'important');
        overlay.style.setProperty('z-index', '9999999', 'important');
        overlay.style.setProperty('pointer-events', 'auto', 'important');
        
        // Fallback for older browsers
        overlay.style.setProperty('position', 'fixed', 'important');
        overlay.style.setProperty('top', '0', 'important');
        overlay.style.setProperty('left', '0', 'important');
        overlay.style.setProperty('width', '100%', 'important');
        overlay.style.setProperty('height', '100%', 'important');
        
        overlay.classList.add('show');
        
        if(typeof backToAIMenu === 'function') {
            backToAIMenu();
        }
    } catch(e) {
        if(typeof showToast==='function') showToast("AI Hata: " + e.message);
    }
}
function closeAIHub() {
    try {
        document.getElementById('ai-hub-overlay').classList.remove('show'); document.getElementById('ai-hub-overlay').style.display = 'none';
    } catch(e) {}
}
function backToAIMenu() {
    try {
        document.getElementById('ai-main-menu').style.display = 'block';
        document.querySelectorAll('.ai-screen').forEach(el => el.style.display = 'none');
        document.getElementById('ai-hub-title').innerText = 'AI Merkezi';
    } catch(e) {
        console.error("backToAIMenu Error:", e);
    }
}
function openAIScreen(type) {
    document.getElementById('ai-main-menu').style.display = 'none';
    document.querySelectorAll('.ai-screen').forEach(el => el.style.display = 'none');
    document.getElementById(`ai-screen-${type}`).style.display = 'flex';
    const titles = { 'analysis': 'Bisiklet Analizi', 'recommend': 'Akıllı Öneri', 'build': 'Custom Build', 'part': 'Parça İnceleme' };
    document.getElementById('ai-hub-title').innerText = titles[type];
}

function updateBuildProgress(count) {
    const steps = document.querySelectorAll('#ai-build-progress .build-step');
    steps.forEach((s, i) => {
        if(i < count) s.classList.add('active');
        else s.classList.remove('active');
    });
}

async function runAI(type) {
    const loader = document.getElementById(`ai-loader-${type}`);
    const resBox = document.getElementById(`ai-res-${type}`);
    loader.style.display = 'block';
    resBox.innerHTML = '';
    
    let payload = { action: '' };
    
    if (type === 'analysis') {
        const val = document.getElementById('ai-inp-analysis').value;
        if(!val) return loader.style.display = 'none';
        payload = { action: 'ai_bike_analysis', data: { bike_info: val } };
    } 
    else if (type === 'recommend') {
        const b = document.getElementById('ai-inp-rec-budget').value;
        const s = document.getElementById('ai-inp-rec-style').value;
        const t = document.getElementById('ai-inp-rec-terrain').value;
        const l = document.getElementById('ai-inp-rec-level').value;
        if(!b || !s) return loader.style.display = 'none';
        payload = { action: 'ai_bike_recommendation', data: { budget: b, style: s, terrain: t, level: l } };
    }
    else if (type === 'build') {
        const req = document.getElementById('ai-inp-build').value;
        if(!req) return loader.style.display = 'none';
        payload = { action: 'ai_bike_build', data: { history: aiBuildMemory, new_request: req } };
    }
    else if (type === 'part') {
        const p = document.getElementById('ai-inp-part').value;
        if(!p) return loader.style.display = 'none';
        payload = { action: 'ai_part_analysis', data: { part_name: p } };
    }
    
    try {
        const r = await fetch('/api/data', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(payload)
        });
        const data = await r.json();
        loader.style.display = 'none';
        
        if (data.status === 'error') {
            resBox.innerHTML = `<div class="ai-result-box" style="border-color: #ef4444;"><div class="text-red-400 font-bold">${data.message}</div></div>`;
            return;
        }
        
        const d = data.data;
        let html = '';
        
        if (type === 'analysis') {
            html += `<div class="ai-result-box">
                <div class="ai-score-ring">${d.performance_score || 0}</div>
                <div class="text-center text-xs text-zinc-400 mb-6 font-bold tracking-widest uppercase">Performans Skoru</div>
                
                <div class="ai-stat-row"><span class="ai-stat-label">Kategori</span> <span class="ai-stat-val text-purple-400">${d.category || '-'}</span></div>
                <div class="ai-stat-row"><span class="ai-stat-label">Sürüş Tarzı</span> <span class="ai-stat-val">${d.riding_style || '-'}</span></div>
                <div class="ai-stat-row"><span class="ai-stat-label">Geometri</span> <span class="ai-stat-val">${d.geometry || '-'}</span></div>
                <div class="ai-stat-row"><span class="ai-stat-label">Süspansiyon</span> <span class="ai-stat-val">${d.suspension || '-'}</span></div>
                <div class="ai-stat-row"><span class="ai-stat-label">Lastikler</span> <span class="ai-stat-val">${d.tires || '-'}</span></div>
                
                <div class="mt-4 mb-2 font-bold text-sm text-green-400 uppercase tracking-widest border-b border-zinc-800 pb-1">Güçlü Yönler</div>
                <div>${(d.strengths||[]).map(s => `<span class="ai-tag green">${s}</span>`).join('')}</div>
                
                <div class="mt-4 mb-2 font-bold text-sm text-red-400 uppercase tracking-widest border-b border-zinc-800 pb-1">Zayıf Yönler</div>
                <div>${(d.weaknesses||[]).map(s => `<span class="ai-tag red">${s}</span>`).join('')}</div>
                
                <div class="mt-4 mb-2 font-bold text-sm text-yellow-400 uppercase tracking-widest border-b border-zinc-800 pb-1">Yükseltme Önerileri</div>
                <ul class="text-zinc-300 text-sm list-disc pl-4 space-y-1">${(d.upgrades||[]).map(s => `<li>${s}</li>`).join('')}</ul>
            </div>`;
        }
        else if (type === 'recommend') {
            html += `<div class="ai-result-box">
                <div class="text-center mb-6">
                    <div class="text-3xl mb-2">🚲</div>
                    <div class="font-black text-xl text-purple-400 uppercase tracking-wider">${d.bike_type || '-'}</div>
                    <div class="text-xs text-zinc-400 mt-1">${d.level_advice || ''}</div>
                </div>
                
                <div class="ai-stat-row"><span class="ai-stat-label">Geometri</span> <span class="ai-stat-val text-blue-300">${d.geometry || '-'}</span></div>
                <div class="ai-stat-row"><span class="ai-stat-label">Travel Önerisi</span> <span class="ai-stat-val text-yellow-400">${d.suspension_travel || '-'}</span></div>
                <div class="ai-stat-row"><span class="ai-stat-label">Teker Önerisi</span> <span class="ai-stat-val">${d.wheel_size || '-'}</span></div>
                
                <div class="mt-6 mb-2 font-bold text-sm text-white uppercase tracking-widest border-b border-zinc-800 pb-1">Örnek Modeller</div>
                <div class="flex flex-col gap-2 mt-3">
                    ${(d.models||[]).map(s => `<div class="bg-black/50 border border-zinc-700/50 p-3 rounded-lg font-bold text-sm text-zinc-200 border-l-4 border-l-purple-500">${s}</div>`).join('')}
                </div>
            </div>`;
        }
        else if (type === 'build') {
            aiBuildMemory.push(document.getElementById('ai-inp-build').value);
            document.getElementById('ai-inp-build').value = '';
            
            let warnHtml = '';
            if (d.compatibility_warning && d.compatibility_warning.length > 5) {
                warnHtml = `<div class="bg-red-900/30 border border-red-500/50 text-red-200 p-4 rounded-xl mb-4 text-sm shadow-[0_0_15px_rgba(239,68,68,0.3)]">⚠️ <b>Uyumsuzluk Uyarı:</b> ${d.compatibility_warning}</div>`;
            }
            
            document.getElementById('ai-build-summary-text').innerText = d.build_summary || 'Toplama devam ediyor...';
            updateBuildProgress(aiBuildMemory.length);
            
            html += `${warnHtml}<div class="ai-result-box">
                <div class="mt-2 mb-4 font-bold text-sm text-purple-400 uppercase tracking-widest border-b border-purple-900/50 pb-2">AI Sıradaki Önerileri</div>
                <ul class="text-zinc-200 text-sm list-disc pl-4 space-y-2 mb-4">
                    ${(d.suggestions||[]).map(s => `<li>${s}</li>`).join('')}
                </ul>
                <div class="bg-black/40 p-3 rounded-lg border border-zinc-800">
                    <div class="text-[10px] text-zinc-500 font-bold uppercase mb-2">Şu anki Build Geçmişin:</div>
                    <div class="text-xs text-zinc-300 leading-relaxed">${aiBuildMemory.join(' <b class="text-purple-500">→</b> ')}</div>
                </div>
            </div>`;
        }
        else if (type === 'part') {
            html += `<div class="ai-result-box">
                <div class="ai-score-ring" style="border-color:#38bdf8; box-shadow:0 0 20px rgba(56,189,248,0.5)">${d.performance_score || 0}</div>
                <div class="text-center text-xs text-zinc-400 mb-6 font-bold tracking-widest uppercase">Parça Skoru</div>
                
                <div class="ai-stat-row"><span class="ai-stat-label">Kategori</span> <span class="ai-stat-val text-blue-400">${d.category || '-'}</span></div>
                <div class="ai-stat-row"><span class="ai-stat-label">Seviye</span> <span class="ai-stat-val">${d.level || '-'}</span></div>
                <div class="ai-stat-row"><span class="ai-stat-label">Sertlik</span> <span class="ai-stat-val">${d.stiffness || '-'}</span></div>
                <div class="ai-stat-row"><span class="ai-stat-label">Dayanıklılık</span> <span class="ai-stat-val">${d.durability || '-'}</span></div>
                <div class="ai-stat-row"><span class="ai-stat-label">Fiyat/Performans</span> <span class="ai-stat-val text-green-400">${d.price_performance || '-'}</span></div>
                
                <div class="mt-4 mb-2 font-bold text-sm text-green-400 uppercase tracking-widest border-b border-zinc-800 pb-1">Güçlü Yönler</div>
                <div>${(d.strengths||[]).map(s => `<span class="ai-tag green">${s}</span>`).join('')}</div>
                
                <div class="mt-4 mb-2 font-bold text-sm text-red-400 uppercase tracking-widest border-b border-zinc-800 pb-1">Zayıf Yönler</div>
                <div>${(d.weaknesses||[]).map(s => `<span class="ai-tag red">${s}</span>`).join('')}</div>
                
                <div class="mt-4 p-3 bg-blue-900/20 border border-blue-500/30 rounded-lg text-sm text-blue-200 leading-relaxed">
                    <b>💡 Tavsiye:</b> ${d.usage_advice || '-'}
                </div>
            </div>`;
        }
        
        resBox.innerHTML = html;
        
    } catch(e) {
        loader.style.display = 'none';
        resBox.innerHTML = `<div class="ai-result-box" style="border-color: #ef4444;"><div class="text-red-400 font-bold">Bağlantı hatası oluştu.</div></div>`;
    }
}

// --- Onboarding Manager (Interactive App Tour) ---
const OnboardingManager = {
    isRunning: false,
    driverInstance: null,
    
    init: function() {
        const tourCompleted = localStorage.getItem('app_tour_completed');
        
        if (!tourCompleted && typeof currentUser !== 'undefined' && currentUser && currentUser.stats) {
            let stats = currentUser.stats;
            if (typeof stats === 'string') {
                try { stats = JSON.parse(stats); } catch(e) {}
            }
            if (stats.onboarding_completed) {
                localStorage.setItem('app_tour_completed', 'true');
                return;
            }
        }
        
        if (!tourCompleted) {
            let attempts = 0;
            const checkInterval = setInterval(() => {
                if (typeof window.Driver === 'function') {
                    clearInterval(checkInterval);
                    setTimeout(() => this.startTour(), 1500); 
                } else {
                    attempts++;
                    if(attempts > 20) { 
                        clearInterval(checkInterval); 
                        console.warn("Driver.js loading timed out."); 
                    }
                }
            }, 500);
        }
    },
    
    startTour: function() {
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
                        intro: 'FreeriderTR\'ye katıldığın için harika hissediyoruz. Uygulamayı en iyi şekilde kullanman için detaylı bir tura çıkalım.'
                    },
                    {
                        element: document.querySelector('#bnav-0'),
                        title: '🗺️ Harita',
                        intro: 'Buradan Türkiye\'deki tüm trail ve rampa noktalarını görebilirsin.'
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
    markCompleted: function() {
        localStorage.setItem('app_tour_v2_completed', 'true');
        
        if (typeof window.confetti === 'function') {
            window.confetti({ 
                particleCount: 150, 
                spread: 100, 
                origin: { y: 0.6 },
                colors: ['#38bdf8', '#818cf8', '#ffffff', '#ef4444'],
                disableForReducedMotion: true,
                zIndex: 9999999
            });
        }
        
        if (typeof currentUser !== 'undefined' && currentUser && currentUser.stats) {
            let stats = currentUser.stats;
            if (typeof stats === 'string') {
                try { stats = JSON.parse(stats); } catch(e) { stats = {}; }
            }
            if (!stats.onboarding_completed) {
                stats.onboarding_completed = true;
                if(typeof sendAction === 'function') {
                    sendAction('update_user_stats', { stats: stats });
                }
            }
        }
    }
};

// --- iOS PWA Install Prompt Logic ---
function closeIosPrompt() {
    document.getElementById('ios-pwa-prompt').classList.add('hidden');
    localStorage.setItem('iosPromptClosed', 'true');
}

document.addEventListener("DOMContentLoaded", () => {
    const isIos = () => {
        const userAgent = window.navigator.userAgent.toLowerCase();
        return /iphone|ipad|ipod/.test(userAgent);
    };
    const isStandalone = () => {
        return ('standalone' in window.navigator) && (window.navigator.standalone);
    };

    if (isIos() && !isStandalone()) {
        if (!localStorage.getItem('iosPromptClosed')) {
            setTimeout(() => {
                const prompt = document.getElementById('ios-pwa-prompt');
                if(prompt) {
                    prompt.classList.remove('hidden');
                    if(typeof lucide !== 'undefined') lucide.createIcons();
                }
            }, 3000);
        }
    }
});
