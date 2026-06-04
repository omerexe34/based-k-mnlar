import re

with open('html_template.py', 'r', encoding='utf-8') as f:
    content = f.read()

start_marker = "// AI HUB LOGIC - BULLETPROOF REWRITE\n(function() {"
end_marker = "console.log(\"AI HUB IIFE loaded successfully.\");\n})();"

start_idx = content.find(start_marker)
end_idx = content.find(end_marker)

if start_idx == -1 or end_idx == -1:
    print("Could not find IIFE block")
    exit(1)

new_iife = """// AI HUB LOGIC - BULLETPROOF REWRITE
(function() {
    const BUILD_STEPS = [
        { id: 'frame', name: 'Kadro (Frame)' },
        { id: 'headset', name: 'Furç Takımı (Headset)' },
        { id: 'fork', name: 'Maşa (Fork)' },
        { id: 'shock', name: 'Arka Şok (Rear Shock)' },
        { id: 'bb', name: 'Orta Göbek (Bottom Bracket)' },
        { id: 'crank', name: 'Aynakol (Crankset)' },
        { id: 'drivetrain', name: 'Vites Sistemi (Derailleur & Shifter)' },
        { id: 'cassette_chain', name: 'Ruble & Zincir (Cassette/Chain)' },
        { id: 'brakes', name: 'Fren Seti & Rotorlar (Brakes)' },
        { id: 'wheels', name: 'Jant Seti (Wheelset)' },
        { id: 'tires', name: 'Lastikler (Tires)' },
        { id: 'cockpit', name: 'Gidon & Boğaz (Bar & Stem)' },
        { id: 'grips', name: 'Elcik (Grips)' },
        { id: 'seatpost', name: 'Sele Borusu (Seatpost)' },
        { id: 'saddle', name: 'Sele (Saddle)' },
        { id: 'pedals', name: 'Pedallar (Pedals)' }
    ];
    let currentBuildStepIndex = 0;
    let aiBuildMemory = {};

    window.openAIHub = function() {
        try {
            if(typeof showToast==='function') showToast("AI Hub Açılıyor...", "info", 1500);
            const overlay = document.getElementById('ai-hub-overlay');
            if(!overlay) return;
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
            if(typeof window.backToAIMenu === 'function') window.backToAIMenu();
            window.updateBuildProgress(0); // Initialize build UI
        } catch(e) {}
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
        } catch(e) {}
    };

    window.openAIScreen = function(type) {
        document.getElementById('ai-main-menu').style.display = 'none';
        document.querySelectorAll('.ai-screen').forEach(el => el.style.display = 'none');
        document.getElementById(`ai-screen-${type}`).style.display = 'flex';
        const titles = { 'analysis': 'Bisiklet Analizi', 'recommend': 'Akıllı Öneri', 'build': 'Custom Build', 'part': 'Parça İnceleme' };
        document.getElementById('ai-hub-title').innerText = titles[type];
    };

    window.updateBuildProgress = function(forceStepIndex = -1) {
        if(forceStepIndex !== -1) currentBuildStepIndex = forceStepIndex;
        
        const isDone = currentBuildStepIndex >= BUILD_STEPS.length;
        
        const progContainer = document.getElementById('ai-build-progress');
        if(progContainer) {
            let dots = '';
            for(let i=0; i<BUILD_STEPS.length; i++) {
                if(i < currentBuildStepIndex) dots += '<div class="w-3 h-3 rounded-full bg-green-500 shrink-0"></div>';
                else if(i === currentBuildStepIndex) dots += '<div class="w-3 h-3 rounded-full bg-purple-500 shrink-0 border-2 border-white shadow-[0_0_10px_#a855f7]"></div>';
                else dots += '<div class="w-3 h-3 rounded-full bg-zinc-800 shrink-0"></div>';
            }
            progContainer.innerHTML = dots;
        }

        if(isDone) {
            document.getElementById('ai-build-input-area').style.display = 'none';
            document.getElementById('ai-build-complete-area').style.display = 'block';
            document.getElementById('ai-build-step-counter').innerText = 'TAMAMLANDI';
            document.getElementById('ai-build-step-title').innerText = '16 Parça Seçildi';
            document.getElementById('ai-build-summary-text').innerText = 'Tüm donanımlar hazır. Şimdi analiz et veya kopyala.';
        } else {
            document.getElementById('ai-build-input-area').style.display = 'block';
            document.getElementById('ai-build-complete-area').style.display = 'none';
            
            const step = BUILD_STEPS[currentBuildStepIndex];
            document.getElementById('ai-build-step-counter').innerText = `Adım ${currentBuildStepIndex + 1} / 16`;
            document.getElementById('ai-build-step-title').innerText = step.name;
            document.getElementById('ai-build-summary-text').innerText = `Sıradaki Parça: ${step.name}`;
            document.getElementById('ai-inp-build').placeholder = `${step.name} marka/modeli girin...`;
        }
    };

    window.aiUndoBuildStep = function() {
        if(currentBuildStepIndex > 0) {
            currentBuildStepIndex--;
            const stepId = BUILD_STEPS[currentBuildStepIndex].id;
            delete aiBuildMemory[stepId];
            window.updateBuildProgress();
            document.getElementById('ai-res-build').innerHTML = '';
        }
    };

    window.aiResetBuild = function() {
        aiBuildMemory = {};
        currentBuildStepIndex = 0;
        document.getElementById('ai-res-build').innerHTML = '';
        window.updateBuildProgress();
    };

    window.aiCopyBuild = function() {
        let text = "🚲 Benim Custom Build Projem:\\n";
        for(let i=0; i<BUILD_STEPS.length; i++) {
            const step = BUILD_STEPS[i];
            const part = aiBuildMemory[step.id] || '-';
            text += `✅ ${step.name}: ${part}\\n`;
        }
        navigator.clipboard.writeText(text).then(() => {
            if(typeof showToast==='function') showToast("Tasarım kopyalandı!", "success");
        });
    };

    window.aiAnalyzeFullBuild = async function() {
        const loader = document.getElementById(`ai-loader-build`);
        const resBox = document.getElementById(`ai-res-build`);
        loader.style.display = 'block';
        resBox.innerHTML = '';
        
        try {
            const r = await fetch('/api/data', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ action: 'ai_bike_build_final', data: { build_data: aiBuildMemory } })
            });
            const data = await r.json();
            loader.style.display = 'none';
            if (data.status === 'error') {
                resBox.innerHTML = `<div class="ai-result-box" style="border-color: #ef4444;"><div class="text-red-400 font-bold">${data.message}</div></div>`;
                return;
            }
            const d = data.data;
            resBox.innerHTML = `<div class="ai-result-box">
                <div class="ai-score-ring">${d.score || 0}</div>
                <div class="text-center text-xs text-zinc-400 mb-6 font-bold tracking-widest uppercase">Genel Uyum Skoru</div>
                <div class="ai-stat-row"><span class="ai-stat-label">Uygun Kategori</span> <span class="ai-stat-val text-purple-400">${d.category || '-'}</span></div>
                
                <div class="mt-4 mb-2 font-bold text-sm text-green-400 uppercase tracking-widest border-b border-zinc-800 pb-1">Genel Değerlendirme</div>
                <div class="text-sm text-zinc-200 leading-relaxed mb-4">${d.overall_review || '-'}</div>
                
                <div class="mt-4 mb-2 font-bold text-sm text-red-400 uppercase tracking-widest border-b border-zinc-800 pb-1">Zayıf Halka / Eksikler</div>
                <ul class="text-zinc-300 text-sm list-disc pl-4 space-y-1">${(d.weaknesses||[]).map(s => `<li>${s}</li>`).join('')}</ul>
                
                <div class="mt-4 mb-2 font-bold text-sm text-yellow-400 uppercase tracking-widest border-b border-zinc-800 pb-1">Tavsiyeler</div>
                <ul class="text-zinc-300 text-sm list-disc pl-4 space-y-1">${(d.recommendations||[]).map(s => `<li>${s}</li>`).join('')}</ul>
            </div>`;
        } catch(e) {
            loader.style.display = 'none';
            resBox.innerHTML = `<div class="ai-result-box" style="border-color: #ef4444;"><div class="text-red-400 font-bold">Analiz hatası oluştu.</div></div>`;
        }
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
            
            const currentStepDef = BUILD_STEPS[currentBuildStepIndex];
            payload = { 
                action: 'ai_bike_build', 
                data: { 
                    history: aiBuildMemory, 
                    new_request: req,
                    current_step: currentStepDef.name,
                    next_step: (currentBuildStepIndex + 1 < BUILD_STEPS.length) ? BUILD_STEPS[currentBuildStepIndex + 1].name : "Tamamlandı"
                } 
            };
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
            
            if (d.status === 'needs_info') {
                html += `<div class="ai-result-box" style="border-color: #eab308; box-shadow: 0 0 15px rgba(234,179,8,0.2);">
                    <div class="text-yellow-400 font-bold mb-2 uppercase tracking-widest text-sm">Eksik Bilgi Tespit Edildi</div>
                    <div class="text-zinc-200 text-sm leading-relaxed">${d.question || 'Lütfen daha detaylı bilgi verin.'}</div>
                </div>`;
                resBox.innerHTML = html;
                return;
            }
            
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
                // Save the approved part
                const currentStepDef = BUILD_STEPS[currentBuildStepIndex];
                aiBuildMemory[currentStepDef.id] = document.getElementById('ai-inp-build').value;
                document.getElementById('ai-inp-build').value = '';
                
                // Advance step
                currentBuildStepIndex++;
                window.updateBuildProgress();
                
                let warnHtml = '';
                if (d.compatibility_warning && d.compatibility_warning.length > 5) {
                    warnHtml = `<div class="bg-red-900/30 border border-red-500/50 text-red-200 p-4 rounded-xl mb-4 text-sm shadow-[0_0_15px_rgba(239,68,68,0.3)]">⚠️ <b>Uyumsuzluk Uyarısı:</b> ${d.compatibility_warning}</div>`;
                }
                
                html += `${warnHtml}<div class="ai-result-box">
                    <div class="mt-2 mb-4 font-bold text-sm text-green-400 uppercase tracking-widest border-b border-green-900/50 pb-2">✅ Parça Onaylandı!</div>
                    <div class="text-zinc-200 text-sm leading-relaxed mb-4">${d.compatibility || '-'}</div>
                    <div class="mt-2 mb-4 font-bold text-sm text-purple-400 uppercase tracking-widest border-b border-purple-900/50 pb-2">Sıradaki Adım Önerileri</div>
                    <ul class="text-zinc-200 text-sm list-disc pl-4 space-y-2 mb-4">
                        ${(d.suggestions||[]).map(s => `<li>${s}</li>`).join('')}
                    </ul>
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

    console.log("AI HUB IIFE loaded successfully.");
})();"""

new_content = content[:start_idx] + new_iife + content[end_idx + len(end_marker):]

with open('html_template.py', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("AI HUB IIFE replaced successfully with 16-step builder!")
