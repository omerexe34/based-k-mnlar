import re

with open('html_template.py', 'r', encoding='utf-8') as f:
    content = f.read()

# First, let's extract the exact AI HUB LOGIC block from html_template.py
# It starts at "// AI HUB LOGIC" and ends before "// --- Onboarding Manager (Interactive App Tour) ---"

start_marker = "// AI HUB LOGIC"
end_marker = "// --- Onboarding Manager (Interactive App Tour) ---"

start_idx = content.find(start_marker)
end_idx = content.find(end_marker)

if start_idx == -1 or end_idx == -1:
    print("Could not find AI HUB LOGIC block.")
    exit(1)

# Here is the bulletproof rewrite:
bulletproof_ai_hub = """// AI HUB LOGIC - BULLETPROOF REWRITE
(function() {
    let aiBuildMemory = [];

    window.openAIHub = function() {
        try {
            if(typeof showToast==='function') showToast("AI Hub Açılıyor...", "info", 1500);
            const overlay = document.getElementById('ai-hub-overlay');
            if(!overlay) {
                if(typeof showToast==='function') showToast("AI Hub HTML elementi bulunamadı!");
                return;
            }
            document.body.appendChild(overlay);
            overlay.style.setProperty('display', 'flex', 'important');
            overlay.style.setProperty('opacity', '1', 'important');
            overlay.style.setProperty('visibility', 'visible', 'important');
            overlay.style.setProperty('z-index', '9999999', 'important');
            overlay.style.setProperty('pointer-events', 'auto', 'important');
            
            overlay.style.setProperty('position', 'fixed', 'important');
            overlay.style.setProperty('top', '0', 'important');
            overlay.style.setProperty('left', '0', 'important');
            overlay.style.setProperty('width', '100%', 'important');
            overlay.style.setProperty('height', '100%', 'important');
            
            overlay.classList.add('show');
            
            if(typeof window.backToAIMenu === 'function') {
                window.backToAIMenu();
            }
        } catch(e) {
            if(typeof showToast==='function') showToast("AI Hata: " + e.message);
        }
    };

    window.closeAIHub = function() {
        try {
            const overlay = document.getElementById('ai-hub-overlay');
            if(overlay) {
                overlay.classList.remove('show');
                overlay.style.display = 'none';
            }
        } catch(e) {}
    };

    window.backToAIMenu = function() {
        try {
            document.getElementById('ai-main-menu').style.display = 'block';
            document.querySelectorAll('.ai-screen').forEach(el => el.style.display = 'none');
            document.getElementById('ai-hub-title').innerText = 'AI Merkezi';
        } catch(e) {
            console.error("backToAIMenu Error:", e);
        }
    };

    window.openAIScreen = function(type) {
        document.getElementById('ai-main-menu').style.display = 'none';
        document.querySelectorAll('.ai-screen').forEach(el => el.style.display = 'none');
        document.getElementById(`ai-screen-${type}`).style.display = 'flex';
        const titles = { 'analysis': 'Bisiklet Analizi', 'recommend': 'Akıllı Öneri', 'build': 'Custom Build', 'part': 'Parça İnceleme' };
        document.getElementById('ai-hub-title').innerText = titles[type];
    };

    window.updateBuildProgress = function(count) {
        const steps = document.querySelectorAll('#ai-build-progress .build-step');
        steps.forEach((s, i) => {
            if(i < count) s.classList.add('active');
            else s.classList.remove('active');
        });
    };

    window.runAI = async function(type) {
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
                window.updateBuildProgress(aiBuildMemory.length);
                
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
    };

    window.aiResetBuild = function() {
        aiBuildMemory = [];
        document.getElementById('ai-res-build').innerHTML = '';
        document.getElementById('ai-build-summary-text').innerText = 'Hafıza temizlendi. Baştan başla.';
        window.updateBuildProgress(0);
    };

    console.log("AI HUB IIFE loaded successfully.");
})();
"""

new_content = content[:start_idx] + bulletproof_ai_hub + "\n" + content[end_idx:]

# Update the reset button to use window.aiResetBuild()
new_content = new_content.replace(
    "aiBuildMemory=[]; document.getElementById('ai-res-build').innerHTML=''; document.getElementById('ai-build-summary-text').innerText='Hafıza temizlendi. Baştan başla.'; updateBuildProgress(0);",
    "window.aiResetBuild();"
)

with open('html_template.py', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("AI HUB rewritten with bulletproof IIFE successfully.")
