// Global Değişkenler
        // window.currentUser olarak tanımla — OneSignal init callback'i erişebilsin
        window.currentUser = null;
        let currentUser = null; 
        let map; 
        let markerCluster = null;
        let selectedMarkerCategory = "Rampa";
        let activeMarkerFilter = "Tümü";
        let isFetchingMarkers = false;
        let markerCache = new Map();
        
        let userLat = 39.0; 
        let userLng = 35.0; 
        let tempLat; 
        let tempLng;
        let db = { 
            users: [], 
            markers: [], 
            messages: [], 
            market: [], 
            events: [], 
            news: [], 
            reports: [], 
            banned: [], 
            dms: [], 
            maintenance: false, 
            pinned_message: {},
            total_users: 300,
            active_users: 0
        };
        // Reels global state
        let reelsData = [];
        let currentReelId = null;
        let reelFileData = null;
        let reelFileType = null;
        let _prevTab = 0; // Reels'ten önce hangi tab'daydık

        // ── Toast Bildirim Sistemi (Geliştirilmiş) ──────────────────────────────
        // showToast(message, type?, duration?)  →  ekranın altında kısa süreli bildirim
        // type: 'success' | 'error' | 'warning' | 'info'
        let _toastTimer = null;
        function showToast(message, typeOrDuration = 'info', duration = 3000) {
            // Geriye dönük uyumluluk: eski çağrılar showToast(msg, 3000) şeklinde
            let type = 'info';
            if (typeof typeOrDuration === 'number') {
                duration = typeOrDuration;
            } else if (typeof typeOrDuration === 'string') {
                type = typeOrDuration;
            }

            const icons = { success: '✅', error: '❌', warning: '⚠️', info: 'ℹ️' };
            const colors = {
                success: 'border-color:rgba(34,197,94,0.6);background:linear-gradient(135deg,rgba(20,83,45,0.95),rgba(24,24,27,0.97))',
                error:   'border-color:rgba(239,68,68,0.6);background:linear-gradient(135deg,rgba(127,29,29,0.95),rgba(24,24,27,0.97))',
                warning: 'border-color:rgba(234,179,8,0.6);background:linear-gradient(135deg,rgba(113,63,18,0.95),rgba(24,24,27,0.97))',
                info:    'border-color:rgba(59,130,246,0.6);background:linear-gradient(135deg,rgba(30,58,138,0.95),rgba(24,24,27,0.97))'
            };

            let toast = document.getElementById('__freerider_toast__');
            if (!toast) {
                toast = document.createElement('div');
                toast.id = '__freerider_toast__';
                document.body.appendChild(toast);
            }
            toast.innerHTML = `<span style="margin-right:8px;font-size:16px">${icons[type] || 'ℹ️'}</span><span>${message}</span>`;
            toast.style.cssText = [
                'position:fixed', 'bottom:80px', 'left:50%',
                'transform:translateX(-50%)', 'z-index:9999999',
                'color:#f4f4f5',
                'padding:14px 24px', 'border-radius:16px',
                'font-size:13px', 'font-weight:700',
                'box-shadow:0 8px 32px rgba(0,0,0,0.5)',
                'border:1px solid rgba(255,255,255,0.1)',
                'max-width:88vw', 'text-align:center',
                'pointer-events:none',
                'display:flex', 'align-items:center', 'justify-content:center',
                'gap:6px',
                colors[type] || colors.info,
                'animation:toastSlideIn 0.35s cubic-bezier(0.16,1,0.3,1) both'
            ].join(';');
            if (_toastTimer) clearTimeout(_toastTimer);
            _toastTimer = setTimeout(() => {
                toast.style.animation = 'toastSlideOut 0.3s ease-in forwards';
                setTimeout(() => { toast.style.display = 'none'; }, 300);
            }, duration);
        }
        let markerLayers = []; 
        let currentMessageCount = 0; 
        let currentEventId = null; 
        let currentMarketId = null; 
        let currentDmUser = null; 
        let currentMarkerId = null; 
        let mediaRecorder; 
        let audioChunks = [];
        let _voiceStopping = false; // Ses gönderim aşamasında tekrar tıklamayı engeller
        window.currentOwner = null; 
        let isAddingMarkerMode = false; 
        let isAddingEventMode = false; 
        let currentPhotoContext = 'group';
        let editingBikeIndex = null;

        let editingMarkerId = null;
        let editingMarkerLat = null;
        let editingMarkerLng = null;

        let currentLeaderboardTab = 'weekly'; 
        let verificationUsername = null;

        function checkFileSize(file, maxMB = 10) {
            if(!file) return true; 
            const fileSizeMB = file.size / (1024 * 1024);
            if (fileSizeMB > maxMB) {
                alert(`⚠️ Dosya çok büyük (${fileSizeMB.toFixed(2)} MB). Lütfen sistemi yormamak için ${maxMB}MB'dan küçük bir görsel seçin.`);
                return false;
            }
            return true;
        }
        
        // =====================================================
        // ŞANS ÇARKI - SABİT ÖDÜL LİSTESİ (backend ile eşleşir)
        // =====================================================
        window.WHEEL_PRIZES = [
            {id: "xp_100",      name: "100 XP",          color: "#38bdf8"},
            {id: "prem_dlx_1",  name: "1G Deluxe",        color: "#8b5cf6"},
            {id: "xp_200",      name: "200 XP",           color: "#f59e0b"},
            {id: "prem_ult_1",  name: "1G Ultra+",        color: "#eab308"},
            {id: "xp_300",      name: "300 XP",           color: "#10b981"},
            {id: "prem_std_7",  name: "7G Standart",      color: "#3b82f6"},
            {id: "xp_500",      name: "500 XP",           color: "#38bdf8"},
            {id: "prem_dlx_7",  name: "7G Deluxe",        color: "#8b5cf6"},
            {id: "xp_1000",     name: "1000 XP",          color: "#f59e0b"},
            {id: "prem_ult_7",  name: "7G Ultra+",        color: "#eab308"},
            {id: "xp_10000",    name: "10.000 XP",        color: "#10b981"},
            {id: "prem_std_30", name: "1Ay Standart",     color: "#3b82f6"},
            {id: "xp_100000",   name: "100.000 XP",       color: "#38bdf8"},
            {id: "prem_dlx_30", name: "1Ay Deluxe",       color: "#8b5cf6"},
            {id: "prem_ult_30", name: "1Ay Ultra+",       color: "#eab308"},
            {id: "prem_std_365",name: "1Yil Standart",    color: "#3b82f6"},
            {id: "prem_ult_365",name: "1Yil Ultra+",      color: "#eab308"},
            {id: "xp_200",      name: "200 XP",           color: "#f59e0b"},
        ];


        function checkRefCodeInput() {
            const val = document.getElementById("reg-ref-code").value.trim();
            const container = document.getElementById("reg-ref-reward-container");
            if(val.length > 0) {
                container.classList.remove("hidden");
                container.classList.add("scale-in-anim");
            } else {
                container.classList.add("hidden");
            }
        }

        // =========================================================
        // GİRİŞ VE KAYIT İŞLEMLERİ
        // =========================================================
        async function handleLogin() {
            const u = document.getElementById("login-username").value.trim();
            const p = document.getElementById("login-password").value;
            const rem = document.getElementById("remember-me").checked;
            
            if(!u || !p) return alert("Kullanıcı adı ve şifre zorunludur!");
            
            try {
                const res = await sendAction('login', { username: u, password: p });
                if(res.status === 'ok') {
                    currentUser = res.user;
                    window.currentUser = currentUser; // OneSignal callback için global'e de yaz
                    localStorage.setItem("fr_user", JSON.stringify(currentUser));
                    
                    if(rem) {
                        localStorage.setItem("fr_remembered_username", u);
                        localStorage.setItem("fr_remembered_password", btoa(unescape(encodeURIComponent(p))));
                    } else {
                        localStorage.removeItem("fr_remembered_username");
                        localStorage.removeItem("fr_remembered_password");
                    }
                    
                    if(res.user.just_got_daily) {
                        alert("🎉 Harika! Günlük giriş ödülü olarak +" + res.user.just_got_daily + " XP kazandın.");
                    }
                    
                    loginSuccess();
                }
            } catch(e) { }
        }

        async function handleRegister() {
            const name = document.getElementById("reg-name").value.trim();
            const username = document.getElementById("reg-username").value.trim();
            const city = document.getElementById("reg-city").value.trim();
            const password = document.getElementById("reg-password").value;
            const email = document.getElementById("reg-email").value.trim();
            const marketing = document.getElementById("reg-marketing").checked;
            const kvkk = document.getElementById("reg-kvkk").checked;
            const privacy = document.getElementById("reg-privacy").checked;
            const refCode = document.getElementById("reg-ref-code").value.trim();
            const refReward = document.getElementById("reg-ref-reward").value;
            
            if(!name || !username || !city || !password) return alert("Lütfen Ad Soyad, Kullanıcı Adı, Şehir ve Şifre alanlarını doldurun!");
            
            // Gmail zorunlu değil, ama girilmişse geçerli olmalı
            if(email && !email.toLowerCase().endsWith('@gmail.com')) return alert("Girdiğiniz e-posta @gmail.com uzantılı değil. Lütfen Gmail adresinizi girin ya da alanı boş bırakın.");
            
            // Referans kodu varsa Gmail zorunlu
            if(refCode && !email) return alert("Referans kodu kullanabilmek için @gmail.com adresinizi girmeniz zorunludur! (Spam koruması)");
            if(refCode && !email.toLowerCase().endsWith('@gmail.com')) return alert("Referans kodu kullanabilmek için @gmail.com uzantılı e-posta girmeniz zorunludur! (Spam koruması)");
            
            if(password.length < 4) return alert("Şifre en az 4 karakter olmalıdır!");
            if(!kvkk) return alert("Kayıt olmak için Kullanıcı Sözleşmesi ve KVKK metnini onaylamanız gerekmektedir!");
            if(!privacy) return alert("Kayıt olmak için Gizlilik Sözleşmesi ve Kullanım Şartları'nı onaylamanız gerekmektedir!");
            
            try {
                const payload = {
                    name: name,
                    username: username,
                    city: city,
                    password: password,
                    email: email,
                    marketing: marketing
                };
                
                if (refCode) {
                    payload.ref_code = refCode;
                    payload.ref_reward = refReward;
                }
                
                const res = await sendAction('register', payload);
                
                if(res.status === 'ok') {
                    alert("Kayıt başarılı! Aramıza hoş geldin. Şimdi giriş yapabilirsin.");
                    showLoginTab();
                    document.getElementById("login-username").value = username;
                } else if (res.status === 'needs_verification') {
                    verificationUsername = res.username;
                    document.getElementById("verify-code-input").value = "";
                    document.getElementById("email-verify-modal").classList.remove("hidden");
                    alert("Kayıt başarılı! E-posta adresinize bir doğrulama kodu gönderdik.");
                }
            } catch(e) { 
                console.error(e);
            }
        }

        function openKvkkModal() {
            document.getElementById("kvkk-modal").classList.remove("hidden");
        }

        function closeKvkkModal() {
            document.getElementById("kvkk-modal").classList.add("hidden");
            document.getElementById("reg-kvkk").checked = true;
        }

        function showLoginTab() {
            document.getElementById("login-form").classList.remove("hidden");
            document.getElementById("register-form").classList.add("hidden");
            document.getElementById("login-tab-btn").className = "flex-1 py-3 bg-gradient-to-r from-sky-700 to-sky-500 text-white rounded-lg font-black text-sm shadow-[0_0_15px_rgba(2,132,199,0.5)] tracking-widest uppercase transition-all scale-in-anim";
            document.getElementById("register-tab-btn").className = "flex-1 py-3 bg-transparent text-zinc-400 rounded-lg font-bold text-sm tracking-widest uppercase transition-all hover:text-white";
        }

        function showRegisterTab() {
            document.getElementById("login-form").classList.add("hidden");
            document.getElementById("register-form").classList.remove("hidden");
            document.getElementById("register-tab-btn").className = "flex-1 py-3 bg-gradient-to-r from-sky-700 to-sky-500 text-white rounded-lg font-black text-sm shadow-[0_0_15px_rgba(2,132,199,0.5)] tracking-widest uppercase transition-all scale-in-anim";
            document.getElementById("login-tab-btn").className = "flex-1 py-3 bg-transparent text-zinc-400 rounded-lg font-bold text-sm tracking-widest uppercase transition-all hover:text-white";
        }



        const TITLES = [
            {min:0,     max: 99,    name: "Acemi",        color: "text-zinc-500",  icon: "🌱", next: 100},
            {min:100,   max: 499,   name: "Çaylak",       color: "text-zinc-400",  icon: "🚲", next: 500},
            {min:500,   max: 999,   name: "Sürücü",       color: "text-sky-400",   icon: "🏔️", next: 1000},
            {min:1000,  max: 1999,  name: "Deneyimli",    color: "text-blue-400",  icon: "⚡", next: 2000},
            {min:2000,  max: 3999,  name: "Rampa Savaşçısı", color: "text-indigo-400",icon: "🛡️", next: 4000},
            {min:4000,  max: 6999,  name: "Usta",         color: "text-orange-400",icon: "🔥", next: 7000},
            {min:7000,  max: 9999,  name: "Elite",        color: "text-rose-400",  icon: "💥", next: 10000},
            {min:10000, max: 19999, name: "Şampiyon",     color: "text-yellow-400",icon: "🏆", next: 20000},
            {min:20000, max: 49999, name: "Efsane",       color: "text-sky-400",   icon: "👑", next: 50000},
            {min:50000, max: 999999,name: "Downhill Efsanesi", color: "text-prem-rainbow", icon: "🌟", next: null}
        ];

        function getTitle(xp) {
            return TITLES.find(t => xp >= t.min && xp <= t.max) || TITLES[TITLES.length - 1];
        }
        
        function getTitleProgress(xp) {
            const t = getTitle(xp);
            if (!t.next) return {percent: 100, xpLeft: 0, nextName: null};
            const range = t.next - t.min;
            const prog = xp - t.min;
            return {
                percent: Math.min(Math.round((prog / range) * 100), 100),
                xpLeft: t.next - xp,
                nextName: TITLES.find(tt => tt.min === t.next)?.name || null,
                nextIcon: TITLES.find(tt => tt.min === t.next)?.icon || ''
            };
        }
        
        const verifiedTick = `<svg class="w-4 h-4 inline-block text-blue-500 drop-shadow-[0_0_5px_rgba(59,130,246,0.8)]" fill="currentColor" viewBox="0 0 20 20"><path d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"></path></svg>`;

        // === KALICI GÖREVLER (bir kere tamamlanır) ===
        const MISSIONS = [
            { id: "m1",  title: "İlk Adım",      desc: "Uygulamaya ilk kez giriş yap.",          target: 1,   type: "login_streak",   xp: 50,   icon: "👋", badge: null },
            { id: "m2",  title: "Bağımlı",        desc: "7 gün üst üste giriş yap.",              target: 7,   type: "login_streak",   xp: 200,  icon: "🔥", badge: "Seri Girişçi" },
            { id: "m3",  title: "Sadık Üye",      desc: "30 gün üst üste giriş yap.",             target: 30,  type: "login_streak",   xp: 2000, icon: "💎", badge: "Demir Üye" },
            { id: "m4",  title: "Çılgın",         desc: "100 gün üst üste giriş yap.",            target: 100, type: "login_streak",   xp: 10000,icon: "⚡", badge: "100 Gün Ustası" },
            { id: "m5",  title: "Sohbete Katıl",  desc: "Gruba 1 mesaj gönder.",                  target: 1,   type: "total_messages", xp: 20,   icon: "💬", badge: null },
            { id: "m6",  title: "Geveze",         desc: "Gruba 50 mesaj gönder.",                 target: 50,  type: "total_messages", xp: 300,  icon: "🗣️", badge: "Sohbet Tutkunu" },
            { id: "m7",  title: "Chat Efsanesi",  desc: "Gruba 200 mesaj gönder.",                target: 200, type: "total_messages", xp: 1000, icon: "👑", badge: "Chat Efsanesi" },
            { id: "m8",  title: "Kâşif",          desc: "Haritaya 1 rampa ekle.",                 target: 1,   type: "markers",        xp: 50,   icon: "📍", badge: "Harita Kâşifi" },
            { id: "m9",  title: "Haritacı",       desc: "Haritaya 10 rampa ekle.",                target: 10,  type: "markers",        xp: 500,  icon: "🗺️", badge: "Haritacı" },
            { id: "m10", title: "İlk Satış",      desc: "Pazara 1 ilan ekle.",                    target: 1,   type: "market",         xp: 50,   icon: "🛒", badge: "Esnaf" },
            { id: "m11", title: "Pazar Ustası",   desc: "Pazara 5 ilan ekle.",                    target: 5,   type: "market",         xp: 300,  icon: "💰", badge: "Pazar Ustası" },
            { id: "m12", title: "Organizatör",    desc: "1 sürüş buluşması oluştur.",             target: 1,   type: "events",         xp: 100,  icon: "🤝", badge: "Organizatör" },
            { id: "m13", title: "Topluluk Lideri",desc: "5 sürüş buluşması oluştur.",             target: 5,   type: "events",         xp: 500,  icon: "🏆", badge: "Topluluk Lideri" },
        ];

        // === GÜNLÜK GÖREVLER (her gün sıfırlanır) ===
        function getDailyMissions() {
            // Güne göre deterministik görev seti (aynı gün herkes aynı görevi görür)
            const dayNum = Math.floor(Date.now() / 86400000);
            const todayKey = new Date().toISOString().split('T')[0];
            const sets = [
                [{ id: "d1", title: "Günlük Giriş",    desc: "Bugün giriş yap.",           target: 1,  type: "daily_login",   xp: 30,  icon: "☀️" },
                 { id: "d2", title: "Sohbet Et",        desc: "Bugün 3 mesaj gönder.",       target: 3,  type: "daily_msg",     xp: 50,  icon: "💬" },
                 { id: "d3", title: "Haritayı Keşfet",  desc: "Haritada 1 nokta ekle.",      target: 1,  type: "daily_marker",  xp: 80,  icon: "📍" }],
                [{ id: "d1", title: "Günlük Giriş",    desc: "Bugün giriş yap.",           target: 1,  type: "daily_login",   xp: 30,  icon: "☀️" },
                 { id: "d4", title: "AI Sor",           desc: "AI'a 1 soru sor.",            target: 1,  type: "daily_ai",      xp: 40,  icon: "🤖" },
                 { id: "d5", title: "Pazar Gez",        desc: "Bir ilana bak.",              target: 1,  type: "daily_market",  xp: 20,  icon: "🛒" }],
                [{ id: "d1", title: "Günlük Giriş",    desc: "Bugün giriş yap.",           target: 1,  type: "daily_login",   xp: 30,  icon: "☀️" },
                 { id: "d6", title: "Aktif Ol",         desc: "Bugün 5 mesaj gönder.",       target: 5,  type: "daily_msg",     xp: 70,  icon: "🔥" },
                 { id: "d7", title: "Sürüşe Çık",       desc: "Radar modunu aç.",            target: 1,  type: "daily_radar",   xp: 60,  icon: "📡" }],
            ];
            const todaySet = sets[dayNum % sets.length];
            return { missions: todaySet, key: todayKey };
        }

        // === HAFTALIK GÖREVLER (her Pazartesi sıfırlanır) ===
        function getWeeklyMissions() {
            const weekNum = Math.floor(Date.now() / (86400000 * 7));
            const now = new Date();
            const monday = new Date(now);
            monday.setDate(now.getDate() - ((now.getDay() + 6) % 7));
            const weekKey = monday.toISOString().split('T')[0];
            const sets = [
                [{ id: "w1", title: "Haftalık Konuşmacı", desc: "Bu hafta 20 mesaj gönder.",  target: 20, type: "weekly_msg",    xp: 200, icon: "💬" },
                 { id: "w2", title: "Harita Gezgini",     desc: "Bu hafta 2 rampa ekle.",      target: 2,  type: "weekly_marker", xp: 150, icon: "🗺️" }],
                [{ id: "w3", title: "Topluluk Üyesi",     desc: "Bu hafta 1 etkinlik oluştur.",target: 1,  type: "weekly_event",  xp: 250, icon: "📅" },
                 { id: "w4", title: "Aktif Tüccar",       desc: "Bu hafta 1 ilan ver.",        target: 1,  type: "weekly_market", xp: 150, icon: "🛒" }],
                [{ id: "w5", title: "Sürüş Ustası",       desc: "Bu hafta 3 kez radar aç.",    target: 3,  type: "weekly_radar",  xp: 200, icon: "🚴" },
                 { id: "w6", title: "Soru Sorular",        desc: "Bu hafta 5 AI sorusu sor.",   target: 5,  type: "weekly_ai",     xp: 180, icon: "🤖" }],
            ];
            return { missions: sets[weekNum % sets.length], key: weekKey };
        }

        function resizeImage(file, maxSize) {
            return new Promise((resolve) => {
                if(!file) { 
                    resolve(null); 
                    return; 
                }
                const reader = new FileReader();
                
                reader.onload = (e) => {
                    const img = new Image();
                    img.onload = () => {
                        const canvas = document.createElement('canvas');
                        let width = img.width; 
                        let height = img.height;
                        
                        if (width > height && width > maxSize) { 
                            height *= maxSize / width; 
                            width = maxSize; 
                        } else if (height > maxSize) { 
                            width *= maxSize / height; 
                            height = maxSize; 
                        }
                        
                        canvas.width = width; 
                        canvas.height = height;
                        
                        const ctx = canvas.getContext('2d'); 
                        ctx.drawImage(img, 0, 0, width, height);
                        
                        resolve(canvas.toDataURL('image/jpeg', 0.72)); 
                    };
                    img.onerror = () => resolve(null);
                    img.src = e.target.result;
                };
                reader.onerror = () => resolve(null);
                reader.readAsDataURL(file);
            });
        }

        const supaUrl = '{{ supabase_url }}';
        const supaKey = '{{ supabase_key }}';
        // DUZELTME #4: window.supabase CDN'den gecikmeli yuklenebilir.
        // Direkt createClient() cagrisi "window.supabase is not defined" hatasi verir
        // ve bu, sonraki TUM JS kodunun calismasini durdurur (butonlar donuyor).
        let supaClient = null;
        if(window.supabase) {
            supaClient = window.supabase.createClient(supaUrl, supaKey);
        } else {
            console.error("[FreeriderTR] Supabase JS SDK yuklenemedi. Realtime ozellikler calismiyor.");
            // Script hatasi tum sayfayi kilitlememesi icin devam et
        }

        // ==============================================================
        // ÇEVRİM İÇİ DURUM YARDIMCI FONKSİYONLARI
        // ==============================================================
        function getOnlineStatus(user) {
            if (!user || !user.stats) return { status: 'offline', label: '' };
            const ts = user.stats.last_seen_ts;
            if (!ts) return { status: 'offline', label: '' };
            const nowSec = Math.floor(Date.now() / 1000);
            const diff = nowSec - ts;
            if (diff < 300) return { status: 'online', label: 'Şu an aktif' };
            if (diff < 3600) {
                const mins = Math.floor(diff / 60);
                return { status: 'recent', label: `${mins} dk önce aktifti` };
            }
            if (diff < 86400) {
                const hrs = Math.floor(diff / 3600);
                return { status: 'today', label: `${hrs} saat önce` };
            }
            return { status: 'offline', label: '' };
        }

        function getOnlineHTML(user, showLabel = true) {
            const s = getOnlineStatus(user);
            if (s.status === 'online') {
                return showLabel
                    ? `<span class="online-dot-sm"></span><span class="online-label">${s.label}</span>`
                    : `<span class="online-dot-sm"></span>`;
            }
            if (s.status === 'recent') {
                return showLabel
                    ? `<span class="recent-dot"></span><span class="recent-label">${s.label}</span>`
                    : `<span class="recent-dot"></span>`;
            }
            return '';
        }

        // ==============================================================
        // GERÇEK ALEV & BUZ PARTİKÜL SİSTEMİ (Ultra+)
        // ==============================================================
        const _particleTimers = {};

        function startParticles(canvasId, type) {
            const canvas = document.getElementById(canvasId);
            if (!canvas) return;
            const ctx = canvas.getContext('2d');
            // Canvas wraps around the circular avatar
            const SIZE = canvas.width = canvas.height = 160;
            const CX = SIZE / 2, CY = SIZE / 2;
            const R = 68; // avatar radius
            let particles = [];
            let running = true;
            const isIce = type === 'ice';

            function mkFireParticle() {
                // Spawn along bottom arc of circle
                const angle = (Math.random() * Math.PI) + Math.PI; // bottom half: pi to 2pi
                const spawnR = R + 2;
                return {
                    x: CX + Math.cos(angle) * spawnR,
                    y: CY + Math.sin(angle) * spawnR,
                    vx: Math.cos(angle) * -(0.3 + Math.random()*0.5) + (Math.random()-0.5)*0.6,
                    vy: -(0.8 + Math.random()*1.4),
                    size: 4 + Math.random()*5,
                    life: 1,
                    decay: 0.022 + Math.random()*0.02,
                    phase: Math.random() * Math.PI * 2  // wobble phase
                };
            }

            function mkIceParticle() {
                // Spawn around full circle border
                const angle = Math.random() * Math.PI * 2;
                const spawnR = R + 1;
                return {
                    x: CX + Math.cos(angle) * spawnR,
                    y: CY + Math.sin(angle) * spawnR,
                    angle: angle,
                    vr: (Math.random()-0.5)*0.01,  // angular drift
                    r: spawnR + Math.random()*8,
                    size: 2 + Math.random()*3.5,
                    life: 1,
                    decay: 0.012 + Math.random()*0.015,
                    points: Math.floor(5 + Math.random()*3),
                    rotation: Math.random()*Math.PI
                };
            }

            function drawFireParticle(p) {
                const wobble = Math.sin(p.phase + performance.now()*0.004) * 1.2;
                p.x += p.vx + wobble * 0.15;
                p.y += p.vy;
                p.size *= 0.978;
                p.life -= p.decay;
                if(p.life <= 0) return false;
                const a = Math.max(0, p.life);
                const t = 1 - p.life;
                // fire color: deep red -> orange -> yellow at tip
                const h = 15 + t * 35;  // 15=red-orange, 50=yellow
                const l = 35 + t * 25;
                const grad = ctx.createRadialGradient(p.x,p.y,0,p.x,p.y,p.size);
                grad.addColorStop(0, `hsla(${h},100%,${l+20}%,${a*0.9})`);
                grad.addColorStop(0.4, `hsla(${h},100%,${l}%,${a*0.6})`);
                grad.addColorStop(1, `hsla(${h-5},90%,${l-10}%,0)`);
                ctx.beginPath();
                ctx.arc(p.x, p.y, Math.max(0.1,p.size), 0, Math.PI*2);
                ctx.fillStyle = grad;
                ctx.globalAlpha = a;
                ctx.fill();
                return true;
            }

            function drawIceParticle(p) {
                p.angle += p.vr;
                p.x = CX + Math.cos(p.angle) * p.r;
                p.y = CY + Math.sin(p.angle) * p.r;
                p.life -= p.decay;
                if(p.life <= 0) return false;
                const a = Math.max(0, p.life) * 0.85;
                ctx.save();
                ctx.translate(p.x, p.y);
                ctx.rotate(p.rotation + performance.now()*0.0008);
                ctx.globalAlpha = a;
                // Draw snowflake/crystal shape
                const n = p.points;
                const s = Math.max(0.5, p.size);
                ctx.beginPath();
                for(let i=0;i<n*2;i++){
                    const r2 = i%2===0 ? s : s*0.4;
                    const ang2 = (i/n)*Math.PI;
                    i===0 ? ctx.moveTo(Math.cos(ang2)*r2,Math.sin(ang2)*r2)
                           : ctx.lineTo(Math.cos(ang2)*r2,Math.sin(ang2)*r2);
                }
                ctx.closePath();
                ctx.fillStyle = `rgba(180,230,255,${a*0.7})`;
                ctx.strokeStyle = `rgba(200,245,255,${a})`;
                ctx.lineWidth = 0.5;
                ctx.fill(); ctx.stroke();
                ctx.restore();
                return true;
            }

            function frame() {
                if (!running) return;
                ctx.clearRect(0, 0, SIZE, SIZE);
                // Spawn
                const spawnRate = isIce ? 0.35 : 0.6;
                if(Math.random() < spawnRate) particles.push(isIce ? mkIceParticle() : mkFireParticle());
                if(Math.random() < spawnRate*0.5) particles.push(isIce ? mkIceParticle() : mkFireParticle());
                // Draw & filter
                particles = particles.filter(p => isIce ? drawIceParticle(p) : drawFireParticle(p));
                ctx.globalAlpha = 1;
                requestAnimationFrame(frame);
            }
            frame();
            return () => { running = false; };
        }

        function attachParticles(wrapId, canvasId, type) {
            // stop previous if exists
            if (_particleTimers[canvasId]) { _particleTimers[canvasId](); delete _particleTimers[canvasId]; }
            const stop = startParticles(canvasId, type);
            if (stop) _particleTimers[canvasId] = stop;
        }

        // Profil avatarına parçacık ekle/kaldır
        function applyAvatarEffect(effect) {
            const wrap = document.getElementById('profile-avatar-wrap');
            let canvas = document.getElementById('profile-particle-canvas');
            if (!wrap) return;
            if (effect === 'fire' || effect === 'ice') {
                if (!canvas) {
                    canvas = document.createElement('canvas');
                    canvas.id = 'profile-particle-canvas';
                    // Centered overlay, slightly larger than avatar (128px = w-32)
                    canvas.style.cssText = 'position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);width:160px;height:160px;pointer-events:none;z-index:50;';
                    canvas.width = 160; canvas.height = 160;
                    wrap.appendChild(canvas);
                }
                attachParticles('profile-avatar-wrap','profile-particle-canvas', effect);
            } else {
                if (canvas) { canvas.remove(); }
                if (_particleTimers['profile-particle-canvas']) { _particleTimers['profile-particle-canvas'](); }
            }
        }

        // Leaderboard/Chat avatarlarına da mini parçacık ekle
        function maybeAddMiniParticles(imgEl, username) {
            const u = db.users.find(x => x.username === username);
            if (!u || !u.stats) return;
            const effect = u.stats.avatar_effect || 'none';
            if (effect !== 'fire' && effect !== 'ice') return;
            const pid = 'pcanv-' + username.replace(/[^a-zA-Z0-9]/g,'');
            if (document.getElementById(pid)) return; // already added
            const wrap = imgEl.parentElement;
            if (!wrap) return;
            const origPos = wrap.style.position;
            wrap.style.position = 'relative';
            wrap.style.overflow = 'visible';
            const canvas = document.createElement('canvas');
            canvas.id = pid;
            canvas.style.cssText = 'position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);width:80px;height:80px;pointer-events:none;z-index:50;';
            canvas.width = 80; canvas.height = 80;
            wrap.appendChild(canvas);
            attachParticles(wrap.id || '', pid, effect);
        }

        // ==============================================================
        // Heartbeat — her dakikada sunucuya "burdayım" gönder + lokal güncelle
        async function sendHeartbeat() {
            if (!currentUser) return;
            const nowSec = Math.floor(Date.now() / 1000);
            // Lokal güncelle - anında yansısın
            if (currentUser.stats) currentUser.stats.last_seen_ts = nowSec;
            const me = db.users.find(u => u.username === currentUser.username);
            if (me && me.stats) me.stats.last_seen_ts = nowSec;
            // Sunucuya da gönder; üyelik süresi dolmuşsa UI'ı güncelle
            try {
                const hbRes = await fetch('/api/heartbeat', { method: 'POST' });
                if (hbRes.ok) {
                    const hbData = await hbRes.json();
                    if (hbData.premium_revoked) {
                        // Üyelik sona erdi – lokal state sıfırla
                        if (currentUser.stats) {
                            currentUser.stats.premium_tier = 0;
                            currentUser.stats.premium_color = '';
                            delete currentUser.stats.premium_expire_date;
                            delete currentUser.stats.expiry_ts;
                        }
                        if (me && me.stats) {
                            me.stats.premium_tier = 0;
                            me.stats.premium_color = '';
                            delete me.stats.premium_expire_date;
                            delete me.stats.expiry_ts;
                        }
                        showToast('⚠️ Üyeliğin sona erdi. Devam etmek için yenile!');
                    }
                }
            } catch(e) {}
        }

        // ==============================================================
        // ONESIGNAL PUSH BİLDİRİM
        // ==============================================================
        async function requestPushPermission() {
            try {
                // İzin zaten verilmişse tekrar sormadan login yap
                const alreadyGranted = Notification.permission === 'granted';
                let permission = alreadyGranted;
                if (!alreadyGranted) {
                    permission = await OneSignal.Notifications.requestPermission();
                    console.log('OneSignal bildirim izni:', permission);
                }
                if (permission) {
                    if (currentUser) {
                        window.OneSignalDeferred = window.OneSignalDeferred || [];
                        window.OneSignalDeferred.push(async function(OneSignal) {
                            try {
                                await OneSignal.login(currentUser.username);
                                console.log('✅ OneSignal login (izin sonrası):', currentUser.username);
                                // İzin verildi → subscription ID'yi hemen kaydet
                                await saveOneSignalPlayerId(OneSignal);
                            } catch(e) { console.error('OneSignal login hatası:', e); }
                        });
                    }
                }
                updateNotifBtnState();
            } catch(e) { console.error('OneSignal izin hatası:', e); }
        }

        // OneSignal subscription ID'sini backend'e kaydeder
        async function saveOneSignalPlayerId(OneSignal) {
            try {
                // Kisa bir bekleme — subscription aktif olana kadar
                await new Promise(r => setTimeout(r, 800));
                const subId = OneSignal.User.PushSubscription.id;
                if (!subId) {
                    console.warn('⚠️ OneSignal subscription ID henüz hazır değil');
                    return;
                }
                const resp = await fetch('/api/save_push_id', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ player_id: subId })
                });
                const result = await resp.json();
                if (result.status === 'ok') {
                    console.log('✅ OneSignal player_id kaydedildi:', subId.slice(0,20) + '...');
                } else {
                    console.warn('⚠️ player_id kaydedilemedi:', result);
                }
            } catch(e) {
                console.error('❌ saveOneSignalPlayerId hatası:', e);
            }
        }

        async function setOneSignalUser() {
            if(!currentUser) return;
            // OneSignalDeferred kuyruğunu kullan — SDK henüz init olmasa bile güvenli çalışır
            window.OneSignalDeferred = window.OneSignalDeferred || [];
            window.OneSignalDeferred.push(async function(OneSignal) {
                try {
                    await OneSignal.login(currentUser.username);
                    console.log('✅ OneSignal kullanıcı tanımlandı:', currentUser.username);
                    const permission = OneSignal.Notifications.permission;
                    console.log('🔔 OneSignal izin durumu:', permission);
                    // İzin varsa subscription ID'yi hemen kaydet
                    if (permission) {
                        await saveOneSignalPlayerId(OneSignal);
                    }
                } catch(e) {
                    console.error('❌ OneSignal login hatası:', e);
                }
            });
        }

        function getUserPremiumTier(username) { 
            const u = db.users.find(x => x.username === username); 
            if (!u || !u.stats) return 0; 
            return parseInt(u.stats.premium_tier) || 0; 
        }
        
        function getUserPremiumColor(username) { 
            const u = db.users.find(x => x.username === username); 
            if (!u || !u.stats || !u.stats.premium_tier) return null; 
            return u.stats.premium_color || 'std-blue'; 
        }
        
        function getPremiumTextClass(color) { 
            if(!color) return ''; 
            if(color.startsWith('#')) return ''; 
            
            const map = {
                'std-blue': 'text-blue-500 drop-shadow-[0_0_5px_rgba(59,130,246,0.6)]', 'std-yellow': 'text-yellow-500 drop-shadow-[0_0_5px_rgba(234,179,8,0.6)]', 'std-pink': 'text-pink-500 drop-shadow-[0_0_5px_rgba(236,72,153,0.6)]', 'std-green': 'text-green-500 drop-shadow-[0_0_5px_rgba(34,197,94,0.6)]',
                'dlx-blue': 'text-dlx-blue', 'dlx-yellow': 'text-dlx-yellow', 'dlx-pink': 'text-dlx-pink', 'dlx-green': 'text-dlx-green',
                'ult-gold': 'text-prem-gold', 'ult-rainbow': 'text-prem-rainbow',
                'ult-blue': 'text-prem-blue', 'ult-green': 'text-prem-green', 'ult-pink': 'text-prem-pink',
                'rainbow': 'text-prem-rainbow'
            };
            return map[color] || ''; 
        }

        function getPremiumInlineStyle(color) {
            if(color && color.startsWith('#')) {
                return `color: ${color} !important; text-shadow: 0 0 10px ${color}; font-weight: 800;`;
            }
            return '';
        }
        
        function getPremiumBorderClass(username) { 
            const u = db.users.find(x => x.username === username);
            if(!u || !u.stats) return 'border-zinc-700';
            
            let classes = "";
            let color = u.stats.premium_color || 'std-blue';
            let effect = u.stats.avatar_effect || 'none';

            if(effect === 'fire') classes += " effect-fire";
            if(effect === 'ice') classes += " effect-ice";

            if(!color.startsWith('#')) {
                const map = {
                    'std-blue': 'border-blue-500 shadow-[0_0_10px_rgba(59,130,246,0.5)]', 'std-yellow': 'border-yellow-500 shadow-[0_0_10px_rgba(234,179,8,0.5)]', 'std-pink': 'border-pink-500 shadow-[0_0_10px_rgba(236,72,153,0.5)]', 'std-green': 'border-green-500 shadow-[0_0_10px_rgba(34,197,94,0.5)]',
                    'dlx-blue': 'border-dlx-blue', 'dlx-yellow': 'border-dlx-yellow', 'dlx-pink': 'border-dlx-pink', 'dlx-green': 'border-dlx-green',
                    'ult-gold': 'border-prem-gold', 'ult-rainbow': 'border-prem-rainbow',
                    'ult-blue': 'border-prem-blue', 'ult-green': 'border-prem-green', 'ult-pink': 'border-prem-pink',
                    'rainbow': 'border-prem-rainbow'
                };
                classes += " " + (map[color] || 'border-zinc-700');
            }
            return classes.trim() || 'border-zinc-700'; 
        }

        function createColorBtn(id, label, current) {
            const isActive = id === current;
            return `<button onclick="changeColor('${id}')" class="px-3 py-1.5 rounded-lg text-[10px] uppercase tracking-widest font-bold ${isActive ? 'bg-white text-black shadow-[0_0_10px_rgba(255,255,255,0.5)]' : 'bg-zinc-800 text-zinc-300'} border border-zinc-700 hover:bg-zinc-700 transition">${label}</button>`;
        }

        function createEffectBtn(id, label, current) {
            const isActive = id === current;
            return `<button onclick="changeEffect('${id}')" class="px-3 py-1.5 rounded-lg text-[10px] uppercase tracking-widest font-bold ${isActive ? 'bg-white text-black shadow-[0_0_10px_rgba(255,255,255,0.5)]' : 'bg-zinc-800 text-zinc-300'} border border-zinc-700 hover:bg-zinc-700 transition">${label}</button>`;
        }

        async function changeColor(colorId) {
            await sendAction('update_premium_color', { color: colorId, effect: currentUser.stats.avatar_effect || 'none' });
            if(currentUser && currentUser.stats) {
                currentUser.stats.premium_color = colorId;
            }
            updateProfileUI();
        }

        async function applyCustomHex() {
            const hex = document.getElementById("custom-hex-color").value;
            await changeColor(hex);
            alert("Yeni renginiz uygulandı!");
        }

        async function changeEffect(effectId) {
            await sendAction('update_premium_color', { color: currentUser.stats.premium_color || 'std-blue', effect: effectId });
            if(currentUser && currentUser.stats) {
                currentUser.stats.avatar_effect = effectId;
            }
            updateProfileUI();
            alert("Profil efektiniz uygulandı!");
        }

        let _myLastRank = null;

        function checkLeaderboardPosition(oldRank) {
            if(!currentUser || !db.users) return;
            const sorted = [...db.users].sort((a,b) => (b.xp||0)-(a.xp||0));
            const newRank = sorted.findIndex(u => u.username === currentUser.username) + 1;
            if(newRank > 0) {
                if(oldRank && newRank < oldRank) {
                    showRankToast(newRank, oldRank, 'up');
                } else if(oldRank && newRank > oldRank) {
                    showRankToast(newRank, oldRank, 'down');
                }
                _myLastRank = newRank;
            }
        }

        function showRankToast(newRank, oldRank, dir) {
            const isUp = dir === 'up';
            const toast = document.createElement('div');
            toast.className = 'fixed top-20 left-1/2 -translate-x-1/2 z-[99999] px-5 py-3 rounded-2xl font-bold text-sm shadow-2xl flex items-center gap-3 scale-in-anim';
            toast.style.background = isUp ? 'linear-gradient(135deg,#16a34a,#15803d)' : 'linear-gradient(135deg,#0ea5e9,#0284c7)';
            toast.style.color = '#fff';
            toast.innerHTML = (isUp ? '📈' : '📉') +
                `<div><div class="text-[10px] uppercase tracking-widest opacity-80">${isUp ? 'Sıralama Yükseldi!' : 'Sıralama Düştü!'}</div>` +
                `<div>${oldRank}. sira -> ${newRank}. sıra</div></div>`;
            document.body.appendChild(toast);
            haptic(isUp ? [30,20,30,20,50] : [100,50,100]);
            setTimeout(() => { toast.style.opacity='0'; toast.style.transition='opacity 0.4s'; setTimeout(()=>toast.remove(),400); }, 3000);
        }

        // Mobil titreşim geri bildirimi
        function haptic(pattern = [10]) {
            if('vibrate' in navigator) { try { navigator.vibrate(pattern); } catch(e) {} }
        }

        // ==============================================================
        // BİLDİRİM İZİN YÖNETİMİ (PROFİL BUTONU)
        // ==============================================================
        async function handleNotifPermission() {
            if (!('Notification' in window)) {
                alert("Bu tarayıcı bildirimleri desteklemiyor.");
                return;
            }
            if (Notification.permission === 'denied') {
                alert("Bildirim izni engellendi. Lütfen tarayıcı ayarlarından FreeriderTR için bildirimlere izin verin.");
                return;
            }
            haptic([10, 50, 10]);
            await requestPushPermission();
        }

        function updateNotifBtnState() {
            const btn = document.getElementById('notif-perm-btn');
            const icon = document.getElementById('notif-btn-icon');
            const txt = document.getElementById('notif-btn-text');
            if (!btn || !('Notification' in window)) return;
            if (Notification.permission === 'granted') {
                btn.className = 'w-full bg-green-900/40 border border-green-600/50 text-green-400 py-4 rounded-xl font-bold text-sm mt-4 btn-premium-hover flex items-center justify-center gap-2 transition-all';
                if (icon) icon.textContent = '✅';
                if (txt) txt.textContent = 'Bildirimler Açık';
            } else if (Notification.permission === 'denied') {
                btn.className = 'w-full bg-red-950/40 border border-sky-800/50 text-sky-300 py-4 rounded-xl font-bold text-sm mt-4 flex items-center justify-center gap-2 transition-all cursor-not-allowed';
                if (icon) icon.textContent = '🔕';
                if (txt) txt.textContent = 'Bildirimler Engellendi';
            } else {
                btn.className = 'w-full bg-zinc-900 border border-zinc-700 hover:bg-zinc-800 transition text-zinc-300 py-4 rounded-xl font-bold text-sm mt-4 btn-premium-hover flex items-center justify-center gap-2';
                if (icon) icon.textContent = '🔔';
                if (txt) txt.textContent = 'Bildirimleri Aç';
            }
        }

        // DUZELTME #3: sendAction — silent parametre eklendi.
        // Onceki kodda alert() + throw() birlikte kullaniliyordu:
        //   - alert() kullaniciya popup gosterir
        //   - throw() cagrilan yerin catch blogu TEKRAR hata isliyordu
        // Bu cift-hata dongusu butonlara basilinca donmaya yol aciyordu.
        // silent=true gecilirse alert bastiriliyor, sadece exception firlatiliyor.
        async function sendAction(action, data, silent = false) {
            let res;
            try {
                res = await fetch('/api/data', { 
                    method: 'POST', 
                    headers: { 'Content-Type': 'application/json' }, 
                    body: JSON.stringify({ action: action, data: data }) 
                });
            } catch(networkErr) {
                if(!silent) alert("Sunucuya ulasilamiyor. Internet baglantini kontrol et.");
                throw networkErr;
            }
            const result = await res.json(); 
            if(result.status === 'error') { 
                if(result.message === 'Giris yapmaniz gerekiyor!' || result.message === 'Giris yapmalisiniz!') {
                    alert("Sunucu guncellendi veya oturumun suresi doldu. Lutfen tekrar giris yap.");
                    logout();
                    return;
                }
                if(!silent) alert(result.message); 
                throw new Error(result.message); 
            } 
            return result;
        }

        async function loadData(silent = false) {
            try {
                const res = await fetch('/api/data'); 
                const newData = await res.json();
                
                // Mevcut mesajları koru (realtime + cache)
                const existingMessages = db.messages || [];
                const existingDms = db.dms || [];
                
                db = newData;
                
                // Tüm array alanlarını garantile
                if(!db.stories)    db.stories    = [];
                if(!db.messages)   db.messages   = [];
                if(!db.dms)        db.dms        = [];
                if(!db.users)      db.users      = [];
                if(!db.markers)    db.markers    = [];
                if(!db.market)     db.market     = [];
                if(!db.events)     db.events     = [];
                if(!db.news)       db.news       = [];
                if(!db.banned)     db.banned     = [];
                if(!db.giveaways)  db.giveaways  = [];
                
                // Sunucu boş veya az dönerse mevcut mesajları koru
                existingMessages.forEach(m => {
                    if(!db.messages.find(x => x.id === m.id)) db.messages.push(m);
                });
                existingDms.forEach(m => {
                    if(!db.dms.find(x => x.id === m.id)) db.dms.push(m);
                });
                
                // Mesajları ID'ye göre sırala
                db.messages.sort((a,b) => (parseInt(a.id)||0) - (parseInt(b.id)||0));
                
                // LocalStorage'a yedekle
                try {
                    localStorage.setItem('fr_msg_cache', JSON.stringify(db.messages.slice(-50)));
                } catch(e) {}
                
                if (currentUser) {
                    const me = db.users.find(u => u.username === currentUser.username);
                    if (me) { 
                        const oldRank = _myLastRank;
                        // Admin koruması: role üzerine yazılmasını önle
                        const wasAdmin = (currentUser.role === 'Admin' || currentUser.username === 'Admin' || currentUser.username.toLowerCase() === 'admin');
                        currentUser = me;
                        if (wasAdmin) {
                            currentUser.role = 'Admin';
                        }
                        localStorage.setItem("fr_user", JSON.stringify(currentUser)); 
                        updateProfileUI(); 
                        checkMissions();
                        checkLeaderboardPosition(oldRank); 
                        
                        // Referans sekmesi açıksa hemen güncelle
                        if(!document.getElementById('screen-referral').classList.contains('hidden')) {
                            renderReferralTab();
                        }
                    }
                    if (db.banned.includes(currentUser.username) || (db.maintenance && currentUser.role !== 'Admin')) {
                        logout(); 
                    }
                }
                
                if(currentMarkerId && !document.getElementById("marker-sheet").classList.contains("hidden")) {
                    const m = db.markers.find(x => x.id === currentMarkerId);
                    if(m) showMarkerSheet(m, true);
                }
                if(currentEventId && !document.getElementById("event-sheet").classList.contains("hidden")) {
                    const e = db.events.find(x => x.id === currentEventId);
                    if(e) showEventSheet(e);
                }

                // Kullanıcı sayacı güncellemesi
                updateUserCountDisplays();
                
                if(!silent) syncMap();
                return true;
            } catch(e) { 
                console.error("Veri çekme hatası:", e);
                return false; 
            }
        }

        function updateUserCountDisplays() {
            const total = db.total_users || 300;
            const active = db.active_users || 0;
            // Login ekranı
            const la = document.getElementById('login-active-users');
            const lt = document.getElementById('login-total-users');
            if(la) la.textContent = active;
            if(lt) lt.textContent = total.toLocaleString('tr-TR');
            // Leaderboard
            const ra = document.getElementById('rank-active-users');
            const rt = document.getElementById('rank-total-users');
            if(ra) ra.textContent = active;
            if(rt) rt.textContent = total.toLocaleString('tr-TR');
        }
        
        async function fetchWeather(lat, lon) {
            try {
                const response = await fetch(`https://api.open-meteo.com/v1/forecast?latitude=${lat}&longitude=${lon}&current_weather=true&timezone=auto`);
                const data = await response.json();
                if (data && data.current_weather) {
                    const temp = Math.round(data.current_weather.temperature);
                    const code = data.current_weather.weathercode;
                    const weatherMap = {
                        0: {icon: "☀️", desc: "Açık"}, 1: {icon: "🌤️", desc: "Az Bulutlu"},
                        2: {icon: "⛅", desc: "Parçalı"}, 3: {icon: "☁️", desc: "Bulutlu"},
                        45: {icon: "🌫️", desc: "Sisli"}, 61: {icon: "🌧️", desc: "Yağmurlu"},
                        63: {icon: "🌧️", desc: "Yoğun Yağmur"}, 71: {icon: "❄️", desc: "Karlı"},
                        80: {icon: "🌦️", desc: "Sağanak"}, 95: {icon: "⛈️", desc: "Fırtına"}
                    };
                    const status = weatherMap[code] || {icon: "🌡️", desc: "Bilinmiyor"};
                    // Update sidebar weather
                    const sidebarW = document.getElementById("sidebar-weather");
                    if(sidebarW) {
                        sidebarW.classList.remove("hidden");
                        document.getElementById("sidebar-weather-icon").textContent = status.icon;
                        document.getElementById("sidebar-weather-temp").textContent = temp + "°C";
                        document.getElementById("sidebar-weather-desc").textContent = status.desc;
                    }
                    // Update missions ride card if it still exists
                    const rideCard = document.getElementById('weather-ride-card');
                    if(rideCard) {
                        updateWeatherWidget(temp, code);
                    }
                    // Also update old weather-widget if present
                    const widget = document.getElementById("weather-widget");
                    if(widget) { widget.style.display = "flex"; widget.classList.remove("hidden"); }
                    if(document.getElementById("weather-icon")) document.getElementById("weather-icon").innerText = status.icon;
                    if(document.getElementById("weather-desc")) document.getElementById("weather-desc").innerText = status.desc;
                }
            } catch (e) { console.log("Hava durumu hatası:", e); }
        }

        function updateMyLocation() {
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition((position) => {
                    const { latitude, longitude } = position.coords;
                    userLat = latitude;
                    userLng = longitude;
                    fetchWeather(latitude, longitude);
                    if(typeof sendLocationToSupabase === "function") {
                        sendLocationToSupabase(latitude, longitude);
                    }
                    if (currentUser && currentUser.stats && currentUser.stats.riding_until > Date.now()) {
                        sendAction('update_user', {
                            username: currentUser.username,
                            stats: { ...currentUser.stats, riding_lat: latitude, riding_lng: longitude }
                        }).catch(e => {});
                    }
                }, (error) => { console.log("Konum izni alinamadi."); });
            }
        }

        window.onload = async function() {
            const savedUsername = localStorage.getItem("fr_remembered_username");
            const savedPasswordEncoded = localStorage.getItem("fr_remembered_password");
            
            // Şifreyi decode et (base64) — eski düz metin kayıtları da çalışsın
            let savedPassword = null;
            if (savedPasswordEncoded) {
                try {
                    savedPassword = decodeURIComponent(escape(atob(savedPasswordEncoded)));
                } catch(e) {
                    // Eski düz metin kaydı ise direkt kullan (geçiş dönemi)
                    savedPassword = savedPasswordEncoded;
                }
            }
            
            if(savedUsername && savedPassword) { 
                document.getElementById("login-username").value = savedUsername; 
                document.getElementById("login-password").value = savedPassword; 
                document.getElementById("remember-me").checked = true; 
            }
            
            // DUZELTME #2: loadData hata firlatsa bile loading screen kapatilmali.
            // Onceki kodda await loadData() exception atarsa asagisi hic calismiyor,
            // ekran sonsuza kadar "Yukleniyor" modunda kaliyordu.
            try {
                await loadData(true);
            } catch(e) {
                console.error("[FreeriderTR] loadData basarisiz:", e);
            } finally {
                // Her durumda (hata olsa da) loading screen'i kapat
                const loadScreen = document.getElementById("app-loading-screen");
                if(loadScreen) {
                    loadScreen.style.opacity = "0";
                    setTimeout(() => { loadScreen.style.display = "none"; }, 500);
                }
            }
            
            if (savedUsername && savedPassword) {
                try {
                    const res = await sendAction('login', { username: savedUsername, password: savedPassword });
                    if(res && res.status === 'ok') {
                        currentUser = res.user;
                        window.currentUser = currentUser; // OneSignal callback için global'e de yaz
                        localStorage.setItem("fr_user", JSON.stringify(currentUser));
                        // Şifreyi güncel encode edilmiş haliyle tekrar kaydet
                        localStorage.setItem("fr_remembered_password", btoa(unescape(encodeURIComponent(savedPassword))));
                        if(res.user.just_got_daily) {
                            alert("🎉 Harika! Günlük giriş ödülü olarak +" + res.user.just_got_daily + " XP kazandın.");
                        }
                        loginSuccess();
                    } else {
                        // sendAction zaten throw ettiği için bu bloğa girilmez,
                        // ama olası geçiş için yine de bırakıldı (localStorage dokunulmaz)
                    }
                } catch(e) {
                    // Ağ hatası veya sunucu geçici kapalı — localStorage'ı SILME
                    // Sadece gerçek auth hatalarında (şifre yanlış mesajı) temizle
                    const msg = e && e.message ? e.message : '';
                    const isAuthError = msg.includes('Hatalı') || msg.includes('kullanıcı adı') || msg.includes('şifre') || msg.includes('bulunamadı') || msg.includes('banlan');
                    if (isAuthError) {
                        localStorage.removeItem("fr_remembered_username");
                        localStorage.removeItem("fr_remembered_password");
                        document.getElementById("login-username").value = "";
                        document.getElementById("login-password").value = "";
                        document.getElementById("remember-me").checked = false;
                    } else {
                        // Ağ/sunucu geçici hatası — bilgileri koru, sadece logla
                        console.warn('[Beni Hatırla] Geçici hata, bilgiler korunuyor:', e);
                    }
                }
            }

            // ============================================================
            // AKILLI REALTIME SİSTEMİ
            // Tek kanal = tek bağlantı = 200 limit yerine 1 slot kullanır
            // Sayfa arka plana geçince bağlantı kesilir, öne gelince tekrar açılır
            // ============================================================
            let _realtimeChannel = null;
            let _realtimePaused = false;

            function startRealtime() {
                if (_realtimeChannel) {
                    try { supaClient.removeChannel(_realtimeChannel); } catch(e) {}
                }
                _realtimeChannel = supaClient.channel('fr-main', {
                    config: { broadcast: { self: false } }
                })
                // ---- MESAJLAR ----
                .on('postgres_changes', { event: '*', schema: 'public', table: 'messages' }, async payload => {
                    if(!currentUser) return;
                    if(!db.messages) db.messages = [];
                    if (payload.eventType === 'INSERT' && payload.new) {
                        if (!db.messages.find(m => m.id === payload.new.id)) {
                            db.messages.push(payload.new);
                        }
                        if (payload.new.user && !db.users.find(u => u.username === payload.new.user) && !['Freerider AI', 'Moderatör AI', 'SİSTEM AI', 'Admin'].includes(payload.new.user)) {
                            try {
                                const { data } = await supaClient.from('users').select('username, name, bio, city, avatar, role, xp, stats, accepted_chat_rules').eq('username', payload.new.user).single();
                                if (data) db.users.push(data);
                            } catch(e) {}
                        }
                    } else if (payload.eventType === 'DELETE' && payload.old) {
                        db.messages = db.messages.filter(m => m.id !== payload.old.id);
                    } else if (payload.eventType === 'UPDATE' && payload.new) {
                        const idx = db.messages.findIndex(m => m.id === payload.new.id);
                        if (idx !== -1) {
                            // Eksik alanları eski veriden koru (REPLICA IDENTITY olmadan tam gelmiyor olabilir)
                            db.messages[idx] = { ...db.messages[idx], ...payload.new };
                        }
                    }
                    const chatVisible = !document.getElementById('screen-chat').classList.contains('hidden');
                    if (chatVisible) {
                        renderChat(true);
                        if (payload.eventType === 'INSERT' && payload.new && payload.new.user !== currentUser.username) {
                            try { document.getElementById("notif-sound").play().catch(e => {}); } catch(e) {}
                        }
                    } else if (payload.eventType === 'INSERT' && payload.new && payload.new.user !== currentUser.username) {
                        showChatBadge();
                        try { document.getElementById("notif-sound").play().catch(e => {}); } catch(e) {}
                    }
                })
                // ---- DM ----
                .on('postgres_changes', { event: '*', schema: 'public', table: 'dms' }, payload => {
                    if(!currentUser) return;
                    if (payload.eventType === 'INSERT') {
                        if (payload.new.participants && payload.new.participants.includes(currentUser.username)) {
                            if (!db.dms.find(m => m.id === payload.new.id)) db.dms.push(payload.new);
                            // DM badge göster (chat açık değilse)
                            const chatVisible = !document.getElementById('screen-chat').classList.contains('hidden');
                            if (!chatVisible && payload.new.sender !== currentUser.username) showChatBadge();
                        }
                    } else if (payload.eventType === 'DELETE') {
                        db.dms = db.dms.filter(m => m.id !== payload.old.id);
                    }
                    renderDmList();
                    if (currentDmUser) renderDmThread(currentDmUser);
                })
                // ---- HARİTA NOKTALARI ----
                .on('postgres_changes', { event: '*', schema: 'public', table: 'markers' }, payload => {
                    if(!currentUser) return;
                    if (payload.eventType === 'INSERT') {
                        if (!db.markers.find(m => m.id === payload.new.id)) db.markers.push(payload.new);
                    } else if (payload.eventType === 'DELETE') {
                        db.markers = db.markers.filter(m => m.id !== payload.old.id);
                    } else if (payload.eventType === 'UPDATE') {
                        const idx = db.markers.findIndex(m => m.id === payload.new.id);
                        if (idx !== -1) db.markers[idx] = payload.new;
                    }
                    if (map) syncMap();
                    if (payload.new && currentMarkerId === payload.new.id && !document.getElementById("marker-sheet").classList.contains("hidden")) {
                        showMarkerSheet(payload.new, true);
                    }
                })
                // ---- PAZAR ----
                .on('postgres_changes', { event: '*', schema: 'public', table: 'market' }, payload => {
                    if(!currentUser) return;
                    if (payload.eventType === 'INSERT') {
                        if (!db.market.find(m => m.id === payload.new.id)) db.market.unshift(payload.new);
                    } else if (payload.eventType === 'DELETE') {
                        db.market = db.market.filter(m => m.id !== payload.old.id);
                    } else if (payload.eventType === 'UPDATE') {
                        const idx = db.market.findIndex(m => m.id === payload.new.id);
                        if (idx !== -1) db.market[idx] = payload.new;
                    }
                    if (!document.getElementById('screen-market').classList.contains('hidden')) renderMarket();
                })
                // ---- ÇEKİLİŞLER ----
                .on('postgres_changes', { event: '*', schema: 'public', table: 'giveaways' }, payload => {
                    if(!db.giveaways) db.giveaways = [];
                    if (payload.eventType === 'INSERT') {
                        if (!db.giveaways.find(g => String(g.id) === String(payload.new.id))) db.giveaways.unshift(payload.new);
                    } else if (payload.eventType === 'DELETE') {
                        db.giveaways = db.giveaways.filter(g => String(g.id) !== String(payload.old.id));
                    } else if (payload.eventType === 'UPDATE') {
                        const idx = db.giveaways.findIndex(g => String(g.id) === String(payload.new.id));
                        if (idx !== -1) db.giveaways[idx] = payload.new;
                        else db.giveaways.unshift(payload.new);
                    }
                    const gwScreen = document.getElementById('screen-giveaway');
                    if (gwScreen && !gwScreen.classList.contains('hidden')) {
                        if(typeof window.renderGiveaways === 'function') window.renderGiveaways(db.giveaways);
                    }
                })
                // ---- STORY ----
                .on('postgres_changes', { event: '*', schema: 'public', table: 'stories' }, payload => {
                    if(!currentUser) return;
                    if(!db.stories) db.stories = [];
                    const now = Math.floor(Date.now()/1000);
                    if (payload.eventType === 'INSERT' && payload.new.expires_at > now) {
                        if (!db.stories.find(s => s.id === payload.new.id)) db.stories.unshift(payload.new);
                    } else if (payload.eventType === 'DELETE') {
                        db.stories = db.stories.filter(s => s.id !== payload.old.id);
                    }
                    if (!document.getElementById('screen-chat').classList.contains('hidden')) renderStoryBar();
                })
                // ---- ETKİNLİKLER ----
                .on('postgres_changes', { event: '*', schema: 'public', table: 'events' }, payload => {
                    if(!currentUser) return;
                    if (payload.eventType === 'INSERT') {
                        if (!db.events.find(e => e.id === payload.new.id)) db.events.push(payload.new);
                    } else if (payload.eventType === 'DELETE') {
                        db.events = db.events.filter(e => e.id !== payload.old.id);
                    } else if (payload.eventType === 'UPDATE') {
                        const idx = db.events.findIndex(e => e.id === payload.new.id);
                        if (idx !== -1) db.events[idx] = payload.new;
                    }
                    if (map) syncMap();
                    if (payload.new && currentEventId === payload.new.id && !document.getElementById("event-sheet").classList.contains("hidden")) {
                        showEventSheet(payload.new);
                    }
                })
                // ---- KULLANICILAR (XP, online, premium) ----
                .on('postgres_changes', { event: 'UPDATE', schema: 'public', table: 'users' }, payload => {
                    if(!currentUser) return;
                    const updated = payload.new;
                    const idx = db.users.findIndex(u => u.username === updated.username);
                    if (idx !== -1) {
                        // Kendi verimizi tam güncelle, başkalarının garage'ini alma
                        if (updated.username === currentUser.username) {
                            db.users[idx] = updated;
                            currentUser = updated;
                            localStorage.setItem("fr_user", JSON.stringify(currentUser));
                            updateProfileUI();
                            checkMissions();
                        } else {
                            // Başkası için sadece temel alanlar
                            db.users[idx] = {
                                ...db.users[idx],
                                xp: updated.xp,
                                stats: { ...(updated.stats || {}) },
                                avatar: updated.avatar,
                                role: updated.role
                            };
                        }
                    } else if (updated.username !== currentUser.username) {
                        db.users.push(updated);
                    }
                    // Lider tablosu açıksa güncelle
                    if (!document.getElementById('screen-rank').classList.contains('hidden')) renderLeaderboard();
                })
                // ---- YASAKLI KULLANICILAR ----
                .on('postgres_changes', { event: '*', schema: 'public', table: 'banned' }, payload => {
                    if(!currentUser) return;
                    if (payload.eventType === 'INSERT') {
                        if (!db.banned.includes(payload.new.username)) db.banned.push(payload.new.username);
                        // Kendi hesabım banlandıysa çıkış yap
                        if (payload.new.username === currentUser.username) {
                            alert("Hesabınız banlanmıştır!");
                            logout();
                        }
                    } else if (payload.eventType === 'DELETE') {
                        db.banned = db.banned.filter(u => u !== payload.old.username);
                    }
                })
                // ---- HABERLER ----
                .on('postgres_changes', { event: '*', schema: 'public', table: 'news' }, payload => {
                    if(!currentUser) return;
                    if (payload.eventType === 'INSERT') {
                        if (!db.news.find(n => n.id === payload.new.id)) db.news.unshift(payload.new);
                    } else if (payload.eventType === 'DELETE') {
                        db.news = db.news.filter(n => n.id !== payload.old.id);
                    }
                    if (!document.getElementById('screen-news').classList.contains('hidden')) renderNews();
                })
                // ---- AYARLAR (pinned mesaj, bakım modu) ----
                .on('postgres_changes', { event: '*', schema: 'public', table: 'settings' }, payload => {
                    if(!currentUser) return;
                    if (payload.new && payload.new.id === 'pinned_message') {
                        try {
                            db.pinned_message = JSON.parse(payload.new.value || '{}');
                            renderChat(true);
                        } catch(e) {}
                    }
                    if (payload.new && payload.new.id === 'maintenance') {
                        db.maintenance = payload.new.value === 'true';
                        if (db.maintenance && currentUser.role !== 'Admin' && currentUser.role !== 'SubAdmin') {
                            alert("Sistem bakım moduna alındı. Lütfen daha sonra tekrar deneyin.");
                            logout();
                        }
                    }
                })
                .subscribe((status) => {
                    if (status === 'SUBSCRIBED') {
                        console.log('✅ Realtime bağlantısı kuruldu');
                        _realtimePaused = false;
                    } else if (status === 'CHANNEL_ERROR' || status === 'TIMED_OUT') {
                        console.log('⚠️ Realtime bağlantısı kesildi, 5sn sonra tekrar denenecek...');
                        setTimeout(() => { if(!_realtimePaused) startRealtime(); }, 5000);
                    }
                });
            }

            // Sayfa görünürlüğü değişince bağlantıyı yönet (200 limit koruması)
            document.addEventListener('visibilitychange', () => {
                if (document.hidden) {
                    // Sayfa arka plana geçti - bağlantıyı kapat, slot serbest bırak
                    _realtimePaused = true;
                    if (_realtimeChannel) {
                        try { supaClient.removeChannel(_realtimeChannel); _realtimeChannel = null; } catch(e) {}
                    }
                } else {
                    // Sayfa öne geldi - yeniden bağlan ve son veriyi çek
                    _realtimePaused = false;
                    startRealtime();
                    loadData(true); // Arka planda kaçırılan güncellemeleri al
                }
            });

            // İlk bağlantıyı kur
            startRealtime();

            // ── Çevrimdışı / Çevrimiçi Bildirimi ──
            function showOfflineBanner() {
                let b = document.getElementById('offline-banner');
                if (!b) {
                    b = document.createElement('div');
                    b.id = 'offline-banner';
                    b.style.cssText = 'position:fixed;top:0;left:0;right:0;z-index:999999;background:#0284c7;color:#fff;text-align:center;padding:8px 16px;font-size:12px;font-weight:900;letter-spacing:0.05em;text-transform:uppercase;';
                    b.textContent = '📵 İnternet bağlantısı yok — Önbellek modunda çalışıyor';
                    document.body.appendChild(b);
                }
            }
            function hideOfflineBanner() {
                const b = document.getElementById('offline-banner');
                if (b) b.remove();
            }
            window.addEventListener('offline', showOfflineBanner);
            window.addEventListener('online', () => {
                hideOfflineBanner();
                loadData(true);
            });
            if (!navigator.onLine) showOfflineBanner();
        };

        // YANDAN AÇILIR MENÜ (SIDEBAR) FONKSİYONU
        function toggleSidebar() {
            const sidebar = document.getElementById("sidebar");
            const overlay = document.getElementById("sidebar-overlay");
            if(sidebar.classList.contains("-translate-x-full")) {
                sidebar.classList.remove("-translate-x-full");
                overlay.classList.remove("hidden");
                setTimeout(() => { overlay.style.opacity = "1"; }, 10);
            } else {
                sidebar.classList.add("-translate-x-full");
                overlay.style.opacity = "0";
                setTimeout(() => { overlay.classList.add("hidden"); }, 300);
            }
        }

        // =========================================================
        // MARKER UI & API HELPERS
        // =========================================================
        function openCategorySelectModal() {
            document.getElementById('category-select-modal').classList.remove('hidden');
        }

        function selectMarkerCategory(cat) {
            selectedMarkerCategory = cat;
            document.getElementById('category-select-modal').classList.add('hidden');
            
            // Set Add Marker Modal Title & Category Label
            document.getElementById('modal-marker-title').textContent = "📍 " + cat.toUpperCase() + " EKLE";
            document.getElementById('modal-marker-category-label').textContent = "Seçilen Tür: " + cat;
            
            if(tempLat && tempLng && !isAddingMarkerMode) {
                document.getElementById('add-marker-modal').classList.remove('hidden');
            } else {
                toggleAddMarkerMode();
            }
        }

        function closeMarkerModal() {
            document.getElementById('add-marker-modal').classList.add('hidden');
            if(isAddingMarkerMode) {
                toggleAddMarkerMode(); // Exit from adding state if open
            }
        }

        function toggleMarkerFilter(cat) {
            activeMarkerFilter = cat;
            
            // Update UI buttons
            const btns = document.querySelectorAll('.marker-filter-btn');
            btns.forEach(b => {
                b.classList.remove('bg-sky-600/30', 'text-sky-300', 'active');
                if(!b.classList.contains('hover:bg-zinc-800')) b.classList.add('hover:bg-zinc-800');
            });
            const activeBtn = document.getElementById('filter-' + cat);
            if(activeBtn) {
                activeBtn.classList.remove('hover:bg-zinc-800');
                activeBtn.classList.add('bg-sky-600/30', 'text-sky-300', 'active');
            }
            
            // Re-render markers
            syncMap();
        }

        // Viewport based marker loading removed        // =========================================================
        // HARİTA FONKSİYONU
        // =========================================================
        function initMap() {
            if(map) return;
            
            map = L.map('map', { 
                zoomControl: false,
                preferCanvas: true,
                tap: true,
                tapTolerance: 15,
                touchZoom: true,
                bounceAtZoomLimits: false,
                maxBoundsViscosity: 0.0
            }).setView([39.0, 35.0], 6);

            // Yol haritası — CartoDB Dark (temiz, koyu tema, MTB uyumlu)
            var roads = L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
                subdomains: 'abcd',
                maxZoom: 22,
                maxNativeZoom: 19,
                attribution: '© <a href="https://carto.com">CARTO</a> © <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
            });

            // Uydu görüntüsü — ESRI World Imagery + etiketler üst katman
            var satelliteBase = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
                maxZoom: 22,
                maxNativeZoom: 19,
                attribution: '© <a href="https://www.esri.com">Esri</a>, Maxar'
            });
            var satelliteLabels = L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_only_labels/{z}/{x}/{y}{r}.png', {
                subdomains: 'abcd',
                maxZoom: 22,
                maxNativeZoom: 19,
                opacity: 0.8,
                pane: 'shadowPane'
            });
            var satellite = L.layerGroup([satelliteBase, satelliteLabels]);

            satellite.addTo(map);

            var baseMaps = {
                "🛰️ Uydu + Etiketler": satellite,
                "🌑 Koyu Harita": roads
            };

            L.control.layers(baseMaps, null, { 
                collapsed: false, 
                position: 'topright' 
            }).addTo(map);

            // Zoom butonları — sağ alt, parmak dostu
            L.control.zoom({ position: 'bottomright' }).addTo(map);

            if (typeof L.Control.Geocoder !== 'undefined') {
                L.Control.geocoder({
                    defaultMarkGeocode: true,
                    placeholder: "Yer veya Rampa ara...",
                }).addTo(map);
            }
            syncMap();
            autoZoomToUserLocation();

            map.on('click', function(e) { 
                if(!isAddingMarkerMode && !isAddingEventMode) return;
                tempLat = e.latlng.lat; 
                tempLng = e.latlng.lng; 
                if (isAddingMarkerMode) { 
                    // Marker yerleştirildi, modal aç
                    document.getElementById('add-marker-modal').classList.remove('hidden');
                } else if (isAddingEventMode) { 
                    toggleAddEventMode(); 
                    openAddEventModal(); 
                } 
            });
        }

        // =========================================================
        // E-POSTA DOĞRULAMA FONKSİYONLARI
        // =========================================================
        function skipVerification() {
            document.getElementById("email-verify-modal").classList.add("hidden");
            if(!currentUser) {
                alert("Kayıt tamamlandı, ancak e-postanız henüz doğrulanmadı. Daha sonra 'Profil' menüsünden doğrulayabilirsiniz.");
                showLoginTab();
                document.getElementById("login-username").value = verificationUsername;
            }
        }

        async function submitVerificationCode() {
            const code = document.getElementById("verify-code-input").value;
            if(!code || code.length !== 6) return alert("Lütfen geçerli bir 6 haneli kod girin.");
            
            try {
                await sendAction('verify_email', { username: verificationUsername || currentUser?.username, code: code });
                alert("E-posta adresiniz başarıyla doğrulandı!");
                document.getElementById("email-verify-modal").classList.add("hidden");
                
                if(!currentUser) { 
                    showLoginTab();
                    document.getElementById("login-username").value = verificationUsername;
                } else { 
                    await loadData(true);
                    openSettingsModal();
                }
            } catch(e) {}
        }

        async function completeOnboarding() {
            document.getElementById("onboarding-modal").classList.add("hidden");
            if (currentUser && currentUser.stats) {
                currentUser.stats.onboarding = true;
                await sendAction('update_user', currentUser);
            }
        }

        async function checkMissions() {
            if(!currentUser || !currentUser.stats) return;
            let stats = currentUser.stats;
            if(!stats.missions)        stats.missions        = {};
            if(!stats.daily_missions)  stats.daily_missions  = {};
            if(!stats.weekly_missions) stats.weekly_missions = {};

            const dailyData  = getDailyMissions();
            const weeklyData = getWeeklyMissions();
            const todayKey   = dailyData.key;
            const weekKey    = weeklyData.key;

            // Günlük sıfırlama
            if(stats.daily_missions.date !== todayKey) {
                stats.daily_missions = { date: todayKey, daily_login: 1 };
            }
            // Haftalık sıfırlama
            if(stats.weekly_missions.week !== weekKey) {
                stats.weekly_missions = { week: weekKey };
            }

            // Sunucuya claim isteği gönderen yardımcı
            async function claimOnServer(mission_type, mission_id, xp) {
                try {
                    const res = await sendAction('claim_mission', { mission_type, mission_id, xp });
                    if(res && res.status === 'ok' && res.earned_xp > 0) {
                        currentUser.xp = res.new_xp;
                        stats.monthly_xp = (stats.monthly_xp || 0) + res.earned_xp;
                        stats.weekly_xp  = (stats.weekly_xp  || 0) + res.earned_xp;
                        return 'claimed';
                    }
                    if(res && res.status === 'ok' && res.already_done) return 'already_done';
                    if(res && res.status === 'ok' && res.not_ready) return 'not_ready';
                } catch(e) {}
                return 'error';
            }

            // --- Kalıcı görevler ---
            for(let m of MISSIONS) {
                if(!stats.missions[m.id]) {
                    let progress = stats[m.type] || 0;
                    if(progress >= m.target) {
                        const result = await claimOnServer('perm', m.id, m.xp);
                        if(result === 'claimed') {
                            stats.missions[m.id] = true;
                            if(m.badge) {
                                if(!stats.earned_badges) stats.earned_badges = [];
                                if(!stats.earned_badges.includes(m.badge)) stats.earned_badges.push(m.badge);
                            }
                            showMissionToast(m.title, m.xp, m.icon);
                        } else if(result === 'already_done') {
                            stats.missions[m.id] = true; // local senkronize et, toast yok
                        }
                    }
                }
            }

            // --- Günlük görevler ---
            for(let m of dailyData.missions) {
                const doneKey = 'done_' + m.id;
                if(!stats.daily_missions[doneKey]) {
                    let progress = m.type === 'daily_login' ? 1 : (stats.daily_missions[m.type] || 0);
                    if(progress >= m.target) {
                        const result = await claimOnServer('daily', m.id, m.xp);
                        if(result === 'claimed') {
                            stats.daily_missions[doneKey] = true;
                            showMissionToast(m.title + ' (Günlük)', m.xp, m.icon);
                        } else if(result === 'already_done') {
                            stats.daily_missions[doneKey] = true; // sessiz senkronize
                        }
                    }
                }
            }

            // --- Haftalık görevler ---
            for(let m of weeklyData.missions) {
                const doneKey = 'done_' + m.id;
                if(!stats.weekly_missions[doneKey]) {
                    let progress = stats.weekly_missions[m.type] || 0;
                    if(progress >= m.target) {
                        const result = await claimOnServer('weekly', m.id, m.xp);
                        if(result === 'claimed') {
                            stats.weekly_missions[doneKey] = true;
                            showMissionToast(m.title + ' (Haftalık)', m.xp, m.icon);
                        } else if(result === 'already_done') {
                            stats.weekly_missions[doneKey] = true; // sessiz senkronize
                        }
                    }
                }
            }

            updateProfileUI();
            renderMissions();
        }

        // ============================================================
        // STORY SİSTEMİ
        // ============================================================
        let _storyIndex = 0;
        let _storyList = [];
        let _storyTimer = null;

        function renderStoryBar() {
            const bar = document.getElementById('story-items');
            if(!bar || !db.stories) return;
            bar.innerHTML = '';
            const now = Math.floor(Date.now()/1000);
            const active = db.stories.filter(s => s.expires_at > now);
            if(active.length === 0) { bar.innerHTML = '<div class="text-[10px] text-zinc-600 flex items-center h-14 font-medium">Henuz story yok</div>'; return; }
            active.forEach((s, i) => {
                const u = db.users.find(x => x.username === s.user);
                const avatar = u ? u.avatar : 'https://cdn.freeridertr.com.tr/profil%20resmi/unnamed.jpg';
                const seen = s.viewers && s.viewers.includes(currentUser.username);
                const premBorder = getUserPremiumTier(s.user) > 0 ? getPremiumBorderClass(s.user) : '';
                bar.innerHTML += `
                <div onclick="viewStory(${i})" class="flex flex-col items-center gap-1 shrink-0 cursor-pointer">
                    <div class="w-14 h-14 rounded-full overflow-hidden ${seen ? 'story-seen' : 'story-ring'} ${premBorder}">
                        <img src="${avatar}" class="w-full h-full object-cover">
                    </div>
                    <span class="text-[9px] font-bold uppercase tracking-widest max-w-[56px] truncate ${seen ? 'text-zinc-600' : 'text-zinc-400'}">${s.user}</span>
                </div>`;
            });
        }

        function viewStory(startIndex) {
            _storyList = db.stories.filter(s => s.expires_at > Math.floor(Date.now()/1000));
            _storyIndex = startIndex;
            showCurrentStory();
            document.getElementById('story-view-modal').classList.remove('hidden');
        }

        function showCurrentStory() {
            if(_storyTimer) clearTimeout(_storyTimer);
            const s = _storyList[_storyIndex];
            if(!s) { closeStoryView(); return; }
            const u = db.users.find(x => x.username === s.user);
            const avatar = u ? u.avatar : 'https://cdn.freeridertr.com.tr/profil%20resmi/unnamed.jpg';
            document.getElementById('story-view-avatar').src = avatar;
            document.getElementById('story-view-username').textContent = s.user;
            const secsAgo = Math.floor(Date.now()/1000) - s.created_at;
            document.getElementById('story-view-time').textContent = secsAgo < 3600 ? Math.floor(secsAgo/60) + ' dk once' : Math.floor(secsAgo/3600) + ' saat once';
            const imgEl = document.getElementById('story-view-img');
            const txtEl = document.getElementById('story-view-text');
            if(s.image) { imgEl.src = s.image; imgEl.style.display='block'; txtEl.style.display='none'; }
            else { imgEl.style.display='none'; txtEl.style.display='flex'; document.getElementById('story-view-text-content').textContent = s.text; }
            const viewers = s.viewers || [];
            document.getElementById('story-viewer-count').textContent = viewers.length + ' kisi izledi';
            // Progress bars
            const pbContainer = document.getElementById('story-progress-bars');
            pbContainer.innerHTML = '';
            _storyList.forEach((_, i) => {
                const pb = document.createElement('div');
                pb.style.cssText = 'flex:1;height:3px;background:rgba(255,255,255,0.3);border-radius:3px;overflow:hidden;';
                const fill = document.createElement('div');
                fill.style.cssText = 'height:100%;background:#fff;border-radius:3px;';
                fill.style.width = i < _storyIndex ? '100%' : (i === _storyIndex ? '0%' : '0%');
                if(i === _storyIndex) { fill.style.transition = 'width 5s linear'; setTimeout(()=>fill.style.width='100%', 50); }
                pb.appendChild(fill); pbContainer.appendChild(pb);
            });
            // Show delete btn for own stories
            const delBtn = document.getElementById('story-delete-btn');
            if(delBtn) {
                if(s.user === currentUser.username || (currentUser.role === 'Admin')) {
                    delBtn.classList.remove('hidden');
                } else {
                    delBtn.classList.add('hidden');
                }
            }
            // Mark as viewed
            sendAction('view_story', {id: s.id}).catch(()=>{});
            // Auto advance
            _storyTimer = setTimeout(() => { _storyIndex++; showCurrentStory(); }, 5000);
        }

        async function deleteCurrentStory() {
            const s = _storyList[_storyIndex];
            if(!s) return;
            if(!confirm("Bu story'yi silmek istiyor musun?")) return;
            await sendAction('delete_story', { id: s.id });
            _storyList.splice(_storyIndex, 1);
            if(_storyList.length === 0) { closeStoryView(); return; }
            if(_storyIndex >= _storyList.length) _storyIndex = _storyList.length - 1;
            showCurrentStory();
        }

        function closeStoryView() {
            if(_storyTimer) clearTimeout(_storyTimer);
            document.getElementById('story-view-modal').classList.add('hidden');
            renderStoryBar();
        }

        document.addEventListener('DOMContentLoaded', () => { localStorage.removeItem('userCache'); localStorage.removeItem('fr_user_cache');
            const sv = document.getElementById('story-view-modal');
            if(sv) {
                sv.addEventListener('click', (e) => {
                    // DUZELTME #5: currentUser henuz null iken tiklanirsa race condition olusur
                    if(!currentUser) return;
                    const rect = sv.getBoundingClientRect();
                    if(e.clientX < rect.width/2) { _storyIndex = Math.max(0,_storyIndex-1); showCurrentStory(); }
                    else { _storyIndex++; showCurrentStory(); }
                });
            }
        });

        function openAddStoryModal() {
            const premTier = getUserPremiumTier(currentUser.username);
            if(premTier < 1) {
                alert('Story paylasabilmek icin Standart, Deluxe veya Ultra+ uyelik gereklidir!');
                switchTab(6); return;
            }
            document.getElementById('add-story-modal').classList.remove('hidden');
        }

        async function submitStory() {
            const text = document.getElementById('story-text-input').value.trim();
            const file = document.getElementById('story-photo-input').files[0];
            if(!text && !file) return alert('Lutfen bir metin veya fotograf ekleyin!');
            let img = '';
            if(file) { img = await resizeImage(file, 1200); }
            await sendAction('add_story', { text, image: img });
            document.getElementById('add-story-modal').classList.add('hidden');
            document.getElementById('story-text-input').value = '';
            document.getElementById('story-photo-input').value = '';
        }

        // ============================================================
        // YORUM SİSTEMİ
        // ============================================================
        let _commentTargetType = '';
        let _commentTargetId = '';

        async function openComments(targetType, targetId) {
            if(!targetId) return;
            _commentTargetType = targetType;
            _commentTargetId = targetId;
            const label = targetType === 'marker' ? 'Rampa Yorumları' : 'Etkinlik Yorumları';
            document.getElementById('comment-modal-title').innerHTML = '💬 ' + label;
            document.getElementById('comment-list').innerHTML = '<div class="text-zinc-500 text-xs text-center py-4 animate-pulse">Yorumlar yükleniyor...</div>';
            document.getElementById('comment-modal').classList.remove('hidden');
            try {
                const res = await sendAction('get_comments', { target_id: targetId });
                renderComments(res.comments || []);
            } catch(e) { document.getElementById('comment-list').innerHTML = '<div class="text-zinc-500 text-xs text-center py-4">Yorum yuklenemedi.</div>'; }
        }

        function renderComments(comments) {
            const c = document.getElementById('comment-list');
            if(comments.length === 0) {
                c.innerHTML = '<div class="text-zinc-600 text-xs italic text-center py-6">Henuz yorum yok. Ilk yorumu sen yaz!</div>';
                return;
            }
            c.innerHTML = '';
            comments.forEach(cm => {
                const u = db.users.find(x => x.username === cm.user);
                const avatar = u ? u.avatar : 'https://cdn.freeridertr.com.tr/profil%20resmi/unnamed.jpg';
                const isMe = cm.user === currentUser.username;
                const isAdmin2 = currentUser.role === 'Admin';
                const delBtn = (isMe || isAdmin2) ? `<button onclick="deleteComment('${cm.id}')" class="text-[9px] text-sky-400 hover:text-sky-300 ml-2">sil</button>` : '';
                const secsAgo = Math.floor(Date.now()/1000) - cm.created_at;
                const timeStr = secsAgo < 60 ? 'az once' : secsAgo < 3600 ? Math.floor(secsAgo/60)+' dk' : Math.floor(secsAgo/3600)+' saat';
                c.innerHTML += `<div class="flex gap-3 items-start slide-up-anim">
                    <img src="${avatar}" class="w-9 h-9 rounded-full object-cover border border-zinc-700 shrink-0 cursor-pointer" onclick="showOtherProfile('${cm.user}')">
                    <div class="flex-1 bg-black/40 rounded-2xl px-3 py-2 border border-zinc-800">
                        <div class="flex items-center justify-between">
                            <span class="text-xs font-bold text-white cursor-pointer hover:text-zinc-300" onclick="showOtherProfile('${cm.user}')">${cm.user}</span>
                            <span class="text-[9px] text-zinc-600">${timeStr} ${delBtn}</span>
                        </div>
                        <div class="text-sm text-zinc-300 mt-1 leading-relaxed">${cm.text}</div>
                    </div>
                </div>`;
            });
            c.scrollTop = c.scrollHeight;
        }

        async function submitComment() {
            const inp = document.getElementById('comment-input');
            const text = inp.value.trim();
            if(!text) return;
            inp.value = '';
            await sendAction('add_comment', { target_type: _commentTargetType, target_id: _commentTargetId, text });
            const res = await sendAction('get_comments', { target_id: _commentTargetId });
            renderComments(res.comments || []);
        }

        async function deleteComment(id) {
            await sendAction('delete_comment', { id });
            const res = await sendAction('get_comments', { target_id: _commentTargetId });
            renderComments(res.comments || []);
        }

        // ============================================================
        // SEVİYE ATLAMA KUTLAMA ANİMASYONU
        // ============================================================
        let _lastTitleName = null;

        function checkLevelUp() {
            if(!currentUser) return;
            const title = getTitle(currentUser.xp);
            if(_lastTitleName && _lastTitleName !== title.name) {
                showLevelUpAnimation(title);
            }
            _lastTitleName = title.name;
        }

        function showLevelUpAnimation(title) {
            const overlay = document.getElementById('levelup-overlay');
            const card = document.getElementById('levelup-card');
            document.getElementById('levelup-icon').textContent = title.icon;
            document.getElementById('levelup-name').textContent = title.name;
            document.getElementById('levelup-desc').textContent = 'Yeni unvanina ulastin!';
            overlay.classList.remove('hidden');
            overlay.style.pointerEvents = 'none';
            card.style.animation = 'none';
            card.offsetHeight;
            card.style.animation = 'levelUpPulse 0.7s cubic-bezier(0.34,1.56,0.64,1) both';
            haptic([100, 50, 100, 50, 300]);
            showSpinConfetti();
            setTimeout(() => overlay.classList.add('hidden'), 4000);
        }

        // ============================================================
        // HAVA DURUMU ROTA ÖNERİSİ
        // ============================================================
        function getWeatherRouteAdvice(weatherCode) {
            const good = [0, 1, 2];
            const ok   = [3, 45];
            const bad  = [61, 63, 71, 80, 81, 82, 95, 96, 99];
            if(good.includes(weatherCode)) return { emoji:'✅', text:'Harika hava! Suru icin ideal.', color:'text-green-400', ride: true };
            if(ok.includes(weatherCode))   return { emoji:'⚠️', text:'Bulutlu ama suru yapilabilir.', color:'text-yellow-400', ride: true };
            if(bad.includes(weatherCode))  return { emoji:'❌', text:'Yagmur/kar var! Suru tavsiye edilmez.', color:'text-sky-300', ride: false };
            return { emoji:'🌡️', text:'Hava durumu bilinmiyor.', color:'text-zinc-400', ride: false };
        }

        // Hava durumu widget'ına rota önerisi ekle
        function updateWeatherWidget(temp, weatherCode) {
            const advice = getWeatherRouteAdvice(weatherCode);
            document.getElementById('weather-temp').innerText = temp + 'degC';
            const adviceEl = document.getElementById('weather-advice');
            if(adviceEl) {
                adviceEl.innerHTML = `<span class="${advice.color} text-[9px] font-bold">${advice.emoji} ${advice.text}</span>`;
            }
            // Update ride card in missions screen
            const rideCard = document.getElementById('weather-ride-card');
            if(rideCard) {
                const bg = advice.ride ? 'from-green-900/60 to-emerald-900/40 border-green-600/40' : 'from-red-900/60 to-red-900/40 border-sky-500/40';
                const textColor = advice.ride ? 'text-green-400' : 'text-sky-300';
                rideCard.className = `rounded-3xl p-5 mb-4 border bg-gradient-to-r ${bg} relative overflow-hidden`;
                rideCard.innerHTML = `
                    <div class="absolute -right-4 -bottom-4 text-8xl opacity-10">${advice.emoji}</div>
                    <div class="text-[10px] font-black uppercase tracking-widest mb-1 ${textColor}">${advice.ride ? 'BUGÜN SÜRÜLEBİLİR' : 'BUGÜN SÜRÜŞ ÖNERİLMEZ'}</div>
                    <div class="text-white font-black text-2xl teko-font">${temp}°C · ${advice.emoji}</div>
                    <div class="${textColor} text-xs font-bold mt-1">${advice.text}</div>`;
            }
        }

        // ============================================================
        // TEMA & ARAYÜZ RENGİ (Premium)
        // ============================================================
        function applyTheme(themeName) {
            const premTier = getUserPremiumTier(currentUser.username);
            if(premTier < 1) { alert('Tema ozelligi Premium uyelerere ozgudur!'); switchTab(6); return; }
            document.body.className = document.body.className.replace(/theme-[a-z]+/g, '').trim();
            document.body.classList.add('theme-' + themeName);
            localStorage.setItem('fr_theme', themeName);
            if(currentUser.stats) {
                currentUser.stats.ui_theme = themeName;
                sendAction('update_user', { username: currentUser.username, stats: currentUser.stats }).catch(()=>{});
            }
            haptic([20]);
        }

        function loadSavedTheme() {
            const saved = localStorage.getItem('fr_theme') || (currentUser && currentUser.stats && currentUser.stats.ui_theme);
            if(saved) {
                document.body.className = document.body.className.replace(/theme-[a-z]+/g, '').trim();
                document.body.classList.add('theme-' + saved);
            }
        }

        // ============================================================
        // DESTEK MODALI
        // ============================================================
        function openSupportModal() {
            const premTier = getUserPremiumTier(currentUser.username);
            const badge = document.getElementById('support-priority-badge');
            if(premTier >= 2) {
                badge.textContent = '🔴 Oncelikli Destek - 24 saat icinde cevaplanir';
                badge.className = 'mb-4 text-center py-2 rounded-xl text-xs font-black uppercase tracking-widest bg-red-900/40 text-sky-300 border border-sky-800/50';
            } else if(premTier === 1) {
                badge.textContent = '🟡 Normal Destek - 48-72 saat icinde cevaplanir';
                badge.className = 'mb-4 text-center py-2 rounded-xl text-xs font-black uppercase tracking-widest bg-yellow-900/40 text-yellow-400 border border-yellow-800/50';
            } else {
                badge.textContent = '⚪ Ucretsiz Destek - Yoğunluğa gore cevaplanir';
                badge.className = 'mb-4 text-center py-2 rounded-xl text-xs font-black uppercase tracking-widest bg-zinc-800 text-zinc-400 border border-zinc-700';
            }
            document.getElementById('support-message').value = '';
            document.getElementById('support-modal').classList.remove('hidden');
        }

        async function submitSupport() {
            const msg = document.getElementById('support-message').value.trim();
            if(!msg) return alert('Lutfen bir mesaj yazin!');
            await sendAction('send_support', { message: msg });
            document.getElementById('support-modal').classList.add('hidden');
            alert('Destek talebiniz alindi! En kisa surede cevaplayacagiz.');
        }

        // ============================================================
        // RAMPA PUANLAMA
        // ============================================================
        async function rateMarker(rating) {
            if(!currentMarkerId) return;
            haptic([20]);
            // Update stars UI
            const stars = document.querySelectorAll('#ms-stars span');
            stars.forEach((s,i) => {
                s.textContent = i < rating ? '⭐' : '☆';
                s.style.opacity = i < rating ? '1' : '0.4';
            });
            try {
                const m = db.markers.find(x=>x.id===currentMarkerId);
                await sendAction('rate_marker', {
                    marker_id: currentMarkerId,
                    marker_name: m ? m.name : '',
                    rating
                });
                showMissionToast('Puan Verildi!', 0, '⭐');
            } catch(e) {}
        }

        function updateMarkerRating(marker) {
            const avgEl = document.getElementById('ms-avg-rating');
            const stars = document.querySelectorAll('#ms-stars span');
            if(!avgEl || !stars.length) return;
            const ratings = marker.ratings || {};
            const myRating = ratings[currentUser.username] || 0;
            const avg = marker.avg_rating || 0;
            const count = Object.keys(ratings).length;
            avgEl.textContent = avg > 0 ? avg.toFixed(1) + ' (' + count + ' oy)' : 'Henuz oy yok';
            stars.forEach((s,i) => {
                s.textContent = i < myRating ? '⭐' : '☆';
                s.style.opacity = i < myRating ? '1' : '0.4';
            });
        }

        // ============================================================
        // TEHLİKE BİLDİRİMİ
        // ============================================================
        function openDangerReport() {
            document.getElementById('danger-reason-input').value = '';
            document.getElementById('danger-modal').classList.remove('hidden');
        }

        function setDangerReason(reason) {
            document.getElementById('danger-reason-input').value = reason;
        }

        async function submitDangerReport() {
            const reason = document.getElementById('danger-reason-input').value.trim();
            if(!reason) return alert('Lutfen bir sebep secin veya yazin!');
            const m = db.markers.find(x=>x.id===currentMarkerId);
            await sendAction('report_danger', {
                marker_id: currentMarkerId,
                marker_name: m ? m.name : '',
                reason
            });
            document.getElementById('danger-modal').classList.add('hidden');
            showMissionToast('Tehlike Bildirildi', 0, '⚠️');
        }

        // ============================================================
        // TAM EKRAN FOTOĞRAF GÖRÜNTÜLEYİCİ
        // ============================================================
        let _fsImages = [];
        let _fsIndex  = 0;

        function openFullscreen(imgs, startIndex) {
            _fsImages = Array.isArray(imgs) ? imgs : [imgs];
            _fsIndex = startIndex || 0;
            _showFullscreenImg();
            document.getElementById('fullscreen-img-modal').classList.remove('hidden');
            document.body.style.overflow = 'hidden';
        }

        function closeFullscreenImg() {
            document.getElementById('fullscreen-img-modal').classList.add('hidden');
            document.body.style.overflow = '';
        }

        function _showFullscreenImg() {
            document.getElementById('fullscreen-img').src = _fsImages[_fsIndex];
            const navEl = document.getElementById('fullscreen-nav');
            if(navEl) navEl.style.display = _fsImages.length > 1 ? 'flex' : 'none';
            const ctr = document.getElementById('fullscreen-counter');
            if(ctr) ctr.textContent = _fsImages.length > 1 ? (_fsIndex+1)+' / '+_fsImages.length : '';
        }

        function fullscreenNext() { _fsIndex = (_fsIndex+1) % _fsImages.length; _showFullscreenImg(); }
        function fullscreenPrev() { _fsIndex = (_fsIndex-1+_fsImages.length) % _fsImages.length; _showFullscreenImg(); }

        // Swipe support on fullscreen
        (function(){
            let startX = 0;
            document.addEventListener('touchstart', e => {
                if(document.getElementById('fullscreen-img-modal').classList.contains('hidden')) return;
                startX = e.touches[0].clientX;
            }, {passive:true});
            document.addEventListener('touchend', e => {
                if(document.getElementById('fullscreen-img-modal').classList.contains('hidden')) return;
                const dx = e.changedTouches[0].clientX - startX;
                if(Math.abs(dx) > 50) { dx < 0 ? fullscreenNext() : fullscreenPrev(); }
            }, {passive:true});
        })();

        // ============================================================
        // EMOJI REAKSİYONLARI
        // ============================================================
        async function addReaction(msgId, emoji) {
            haptic([10]);
            try {
                await sendAction('add_reaction', {msg_id: msgId, emoji});
                // Update local state
                const msg = db.messages.find(m=>m.id===msgId);
                if(msg) {
                    if(!msg.reactions) msg.reactions = {};
                    const users = msg.reactions[emoji] || [];
                    const idx = users.indexOf(currentUser.username);
                    if(idx >= 0) users.splice(idx,1); else users.push(currentUser.username);
                    msg.reactions[emoji] = users;
                    renderChat(true);
                }
            } catch(e) {}
        }

        function showTrialExpiredModal() {
            const modal = document.getElementById('trial-expired-modal');
            if(modal) modal.classList.remove('hidden');
            // Clear trial_expired flag so it doesn't show again
            if(currentUser && currentUser.stats) {
                currentUser.stats.trial_expired = false;
                sendAction('update_user', { username: currentUser.username, stats: currentUser.stats }).catch(()=>{});
            }
        }

        function showTrialBanner() {
            const existing = document.getElementById('trial-active-banner');
            if(existing) return;
            const banner = document.createElement('div');
            banner.id = 'trial-active-banner';
            banner.className = 'fixed top-16 left-0 right-0 z-[9998] flex justify-center px-4 trial-banner';
            const expDate = currentUser.stats && currentUser.stats.premium_expire_date ? currentUser.stats.premium_expire_date : '?';
            banner.innerHTML = `<div class="bg-gradient-to-r from-yellow-600 to-amber-500 text-black px-5 py-2.5 rounded-2xl font-black text-xs shadow-[0_0_20px_rgba(234,179,8,0.6)] flex items-center gap-3 max-w-sm w-full">
                <span class="text-lg">🎁</span>
                <span class="flex-1">3 Gun Ucretsiz Ultra+ Denemen Aktif! Bitis: ${expDate}</span>
                <button onclick="this.parentElement.parentElement.remove()" class="text-black/60 hover:text-black text-sm">✕</button>
            </div>`;
            document.body.appendChild(banner);
            setTimeout(() => { if(banner.parentElement) banner.remove(); }, 6000);
        }

        function showMissionToast(title, xp, icon) {
            const toast = document.createElement('div');
            toast.className = 'fixed top-20 left-1/2 -translate-x-1/2 z-[99999] bg-gradient-to-r from-yellow-600 to-orange-500 text-white px-6 py-3 rounded-2xl font-bold text-sm shadow-[0_0_30px_rgba(234,179,8,0.6)] flex items-center gap-3 scale-in-anim';
            toast.innerHTML = '<span class="text-2xl">' + icon + '</span><div><div class="text-[10px] uppercase tracking-widest opacity-80">Gorev Tamamlandi!</div><div>' + title + ' +' + xp + ' XP</div></div>';
            document.body.appendChild(toast);
            haptic([50, 30, 50]);
            setTimeout(() => { toast.style.opacity='0'; toast.style.transition='opacity 0.5s'; setTimeout(()=>toast.remove(),500); }, 3500);
        }
        function renderMissions() {
            const c = document.getElementById("missions-list");
            if(!c || !currentUser) return;
            const stats = currentUser.stats || {};

            const dailyData = getDailyMissions();
            const weeklyData = getWeeklyMissions();
            const dm = stats.daily_missions || {};
            const wm = stats.weekly_missions || {};
            const todayKey = dailyData.key;
            const weekKey = weeklyData.key;

            let html = '<div class="flex bg-zinc-950 rounded-xl p-1 mb-5 border border-zinc-800">';
            html += '<button onclick="setMissionTab(0)" id="mtab-0" class="flex-1 py-2 bg-zinc-800 text-white rounded-lg font-bold text-xs transition">Kalici</button>';
            html += '<button onclick="setMissionTab(1)" id="mtab-1" class="flex-1 py-2 text-zinc-500 rounded-lg font-bold text-xs transition">Gunluk</button>';
            html += '<button onclick="setMissionTab(2)" id="mtab-2" class="flex-1 py-2 text-zinc-500 rounded-lg font-bold text-xs transition">Haftalik</button>';
            html += '</div>';

            // === KALICI ===
            html += '<div id="m-perm">';
            MISSIONS.forEach(m => {
                let progress = stats[m.type] || 0;
                let isDone = stats.missions && stats.missions[m.id] === true;
                let percent = Math.min((progress / m.target) * 100, 100);
                let pbHtml = isDone ? '' : '<div class="progress-bar-bg mt-2"><div class="progress-bar-fill" style="width:' + percent + '%;"></div></div>';
                let btnHtml = isDone
                    ? '<span class="text-green-400 text-xs font-bold">TAMAM</span>'
                    : '<div class="text-right"><div class="text-white font-black teko-font text-lg">+' + m.xp + ' XP</div><div class="text-[9px] text-zinc-500">' + progress + '/' + m.target + '</div></div>';
                html += '<div class="glass-panel p-4 rounded-2xl border ' + (isDone ? 'border-green-800/40' : 'border-zinc-700') + ' flex items-center gap-3 mb-3 shadow-md">';
                html += '<div class="text-3xl w-12 h-12 flex items-center justify-center bg-black/50 rounded-xl border border-zinc-800 shrink-0">' + m.icon + '</div>';
                html += '<div class="flex-1 min-w-0"><div class="font-bold text-sm ' + (isDone ? 'text-green-400' : 'text-white') + '">' + m.title + '</div><div class="text-[10px] text-zinc-500 mt-0.5">' + m.desc + '</div>' + pbHtml + '</div>' + btnHtml + '</div>';
            });
            html += '</div>';

            // === GUNLUK ===
            html += '<div id="m-daily" class="hidden">';
            html += '<div class="text-[10px] text-zinc-500 uppercase tracking-widest font-bold mb-3">Bugunun Gorevleri: ' + todayKey + '</div>';
            dailyData.missions.forEach(m => {
                const doneKey = 'done_' + m.id;
                const isDone = dm.date === todayKey && dm[doneKey];
                const progress = m.type === 'daily_login' ? (dm.date === todayKey ? 1 : 0) : (dm.date === todayKey ? (dm[m.type] || 0) : 0);
                const percent = Math.min((progress / m.target) * 100, 100);
                let pbHtml = isDone ? '' : '<div class="progress-bar-bg mt-2"><div class="progress-bar-fill" style="width:' + percent + '%;"></div></div>';
                let btnHtml = isDone
                    ? '<span class="text-green-400 text-xs font-bold">TAMAM</span>'
                    : '<div class="text-right"><div class="text-white font-black teko-font text-lg">+' + m.xp + ' XP</div><div class="text-[9px] text-zinc-500">' + progress + '/' + m.target + '</div></div>';
                html += '<div class="glass-panel p-4 rounded-2xl border ' + (isDone ? 'border-green-800/40' : 'border-yellow-900/40') + ' flex items-center gap-3 mb-3 shadow-md">';
                html += '<div class="text-3xl w-12 h-12 flex items-center justify-center bg-black/50 rounded-xl border border-zinc-800 shrink-0">' + m.icon + '</div>';
                html += '<div class="flex-1 min-w-0"><div class="font-bold text-sm ' + (isDone ? 'text-green-400' : 'text-yellow-400') + '">' + m.title + '</div><div class="text-[10px] text-zinc-500 mt-0.5">' + m.desc + '</div>' + pbHtml + '</div>' + btnHtml + '</div>';
            });
            html += '</div>';

            // === HAFTALIK ===
            html += '<div id="m-weekly" class="hidden">';
            html += '<div class="text-[10px] text-zinc-500 uppercase tracking-widest font-bold mb-3">Bu Haftanin Gorevleri (Pzt: ' + weekKey + ')</div>';
            weeklyData.missions.forEach(m => {
                const doneKey = 'done_' + m.id;
                const isDone = wm.week === weekKey && wm[doneKey];
                const progress = wm.week === weekKey ? (wm[m.type] || 0) : 0;
                const percent = Math.min((progress / m.target) * 100, 100);
                let pbHtml = isDone ? '' : '<div class="progress-bar-bg mt-2"><div class="progress-bar-fill" style="background:linear-gradient(90deg,#7c3aed,#4f46e5);width:' + percent + '%;"></div></div>';
                let btnHtml = isDone
                    ? '<span class="text-green-400 text-xs font-bold">TAMAM</span>'
                    : '<div class="text-right"><div class="text-white font-black teko-font text-lg">+' + m.xp + ' XP</div><div class="text-[9px] text-zinc-500">' + progress + '/' + m.target + '</div></div>';
                html += '<div class="glass-panel p-4 rounded-2xl border ' + (isDone ? 'border-green-800/40' : 'border-purple-900/40') + ' flex items-center gap-3 mb-3 shadow-md">';
                html += '<div class="text-3xl w-12 h-12 flex items-center justify-center bg-black/50 rounded-xl border border-zinc-800 shrink-0">' + m.icon + '</div>';
                html += '<div class="flex-1 min-w-0"><div class="font-bold text-sm ' + (isDone ? 'text-green-400' : 'text-purple-400') + '">' + m.title + '</div><div class="text-[10px] text-zinc-500 mt-0.5">' + m.desc + '</div>' + pbHtml + '</div>' + btnHtml + '</div>';
            });
            html += '</div>';

            c.innerHTML = html;
            window._missionTab = window._missionTab || 0;
            setMissionTab(window._missionTab);
        }

        function setMissionTab(idx) {
            window._missionTab = idx;
            ['m-perm','m-daily','m-weekly'].forEach((id,i) => {
                const el = document.getElementById(id);
                if(el) el.classList.toggle('hidden', i !== idx);
            });
            [0,1,2].forEach(i => {
                const btn = document.getElementById('mtab-'+i);
                if(!btn) return;
                btn.className = i === idx
                    ? 'flex-1 py-2 bg-zinc-800 text-white rounded-lg font-bold text-xs transition'
                    : 'flex-1 py-2 text-zinc-500 rounded-lg font-bold text-xs transition';
            });
        }
        // ==============================================================
        // DAVET ET KAZAN (REFERANS) SEKMESİ İŞLEMLERİ
        // ==============================================================
        function renderReferralTab() {
            if(!currentUser) return;
            const stats = currentUser.stats || {};
            // Gerçek ref kodu stats'tan, yoksa fallback
            const refCode = stats.ref_code || currentUser.username;
            document.getElementById("my-ref-code").value = refCode;
            const refCount = stats.ref_count || 0;
            const claimable = stats.claimable_refs || 0;
            
            const maxRef = 10;
            const refPercent = Math.min((refCount / maxRef) * 100, 100);
            
            document.getElementById("ref-monthly-limit").innerText = `BU AYKİ KULLANIM: ${refCount} / ${maxRef}`;
            document.getElementById("ref-monthly-bar").style.width = `${refPercent}%`;
            document.getElementById("claimable-ref-count").innerText = claimable;
            
            const claimArea = document.getElementById("ref-claim-area");
            if(claimable > 0) {
                claimArea.style.opacity = "1";
                claimArea.style.pointerEvents = "auto";
                claimArea.style.filter = "none";
                claimArea.style.transform = "scale(1)";
                claimArea.style.transition = "all 0.3s ease";
            } else {
                claimArea.style.opacity = "0.35";
                claimArea.style.pointerEvents = "none";
                claimArea.style.filter = "grayscale(80%)";
                claimArea.style.transform = "scale(0.98)";
            }
        }

        function copyRefCode() {
            const code = document.getElementById("my-ref-code").value;
            navigator.clipboard.writeText(code);
            alert("Referans kodunuz başarıyla kopyalandı! Arkadaşlarınıza gönderebilirsiniz.");
        }

        async function claimRefReward() {
            const reward = document.getElementById("ref-reward-select").value;
            try {
                const res = await sendAction('claim_ref_reward', { reward_choice: reward });
                if(res.status === 'ok') {
                    alert("Tebrikler! Ödül başarıyla hesabınıza tanımlandı. Bol pedallı günler!");
                    loadData(true); 
                }
            } catch(e) {}
        }

        // ================================================================
        // REELS SİSTEMİ JS
        // ================================================================

        // ── Aktif IntersectionObserver listesi (eski kod uyumu — artık kullanılmıyor) ──
        const _reelObservers = [];

        // ──────────────────────────────────────────────────────────────
        // stopAllMedia() — Tüm video/ses medyayı durdurur, merkezi
        // feed observer'ı bağlantısını keser.
        // Sayfa geçişlerinde ve modal kapanışlarında çağrılır.
        // ──────────────────────────────────────────────────────────────
        function stopAllMedia() {
            document.querySelectorAll('video, audio').forEach(el => {
                try { el.pause(); } catch(_) {}
            });
            if(typeof _feedObserver !== 'undefined' && _feedObserver) {
                _feedObserver.disconnect();
                _feedObserver = null;
            }
        }

        // ──────────────────────────────────────────────────────────────
        // openReels(videoId) — Reels sayfasını açar ve belirtilen ID'li
        // videoya scroll ederek otomatik oynatır.
        // Profilden Reels'e ışınlanmak için kullanılır.
        // ──────────────────────────────────────────────────────────────
        window.openReels = async function(videoId) {
            stopAllMedia();
            // Tüm açık modalleri kapat
            ['other-profile-modal','reel-comment-modal','reel-upload-modal'].forEach(id => {
                const m = document.getElementById(id);
                if(m) m.classList.add('hidden');
            });
            // Reels ekranını aç
            const screenReels = document.getElementById('screen-reels');
            if(screenReels) {
                screenReels.style.display = 'flex';
                screenReels.style.flexDirection = 'column';
                screenReels.style.zIndex = '9990';
                screenReels.classList.remove('hidden');
            }
            const bottomNav = document.getElementById('bottom-nav');
            if(bottomNav) bottomNav.style.display = 'none';
            const soundBtn = document.getElementById('reel-sound-btn');
            if(soundBtn) { soundBtn.style.display = 'flex'; soundBtn.textContent = _reelMuted ? '🔇' : '🔊'; }
            const gridBtn = document.getElementById('grid-view-btn');
            if(gridBtn) gridBtn.style.display = 'flex';
            const uploadTopBtn = document.getElementById('reels-upload-top-btn');
            if(uploadTopBtn) uploadTopBtn.style.display = 'flex';

            // Her zaman yeniden yükle (feed güncel olsun, observer temiz başlasın)
            await loadReels();

            // loadReels render tamamlandıktan sonra scroll + oynat
            if(videoId && reelsData.length) {
                const idx = reelsData.findIndex(r => String(r.id) === String(videoId));
                const feed = document.getElementById('reels-feed');
                if(feed && idx >= 0) {
                    // 2 frame bekle: render + observer kurulumu tamamlansın
                    requestAnimationFrame(() => requestAnimationFrame(() => {
                        const cards = feed.querySelectorAll(':scope > div');
                        const targetCard = cards[idx];
                        if(!targetCard) return;
                        // observer'ı geçici durdur, scroll sırasında yanlış video çalmasın
                        if(_feedObserver) _feedObserver.disconnect();
                        // Tüm videolar durdurulmuş, scroll et
                        targetCard.scrollIntoView({ behavior: 'instant', block: 'start' });
                        // Scroll sonrası hedef videoyu oynat ve observer'ı yeniden kur
                        requestAnimationFrame(() => {
                            const video = targetCard.querySelector('video');
                            if(video) {
                                video.muted = _reelMuted;
                                video.play().catch(() => { video.muted = true; video.play().catch(() => {}); });
                            }
                            _setupFeedObserver();
                        });
                    }));
                }
            }
            history.pushState({ reelsOpen: true }, '');
        };

        function escapeHtml(str) {
            if(str == null) return '';
            return String(str)
                .replace(/&/g,'&amp;')
                .replace(/</g,'&lt;')
                .replace(/>/g,'&gt;')
                .replace(/"/g,'&quot;')
                .replace(/'/g,'&#39;');
        }

        let _reelMuted = false; // Varsayılan: ses açık

        // Reels'i kapat, önceki sekmeye dön
        function closeReels() {
            stopAllMedia(); // Hayalet ses önleme — tüm medyayı durdur
            const reelsEl = document.getElementById('screen-reels');
            if(reelsEl) {
                reelsEl.style.display = 'none';
                reelsEl.classList.add('hidden');
            }
            const bottomNav = document.getElementById('bottom-nav');
            if(bottomNav) bottomNav.style.display = '';
            const soundBtn = document.getElementById('reel-sound-btn');
            if(soundBtn) soundBtn.style.display = 'none';
            const gridBtn = document.getElementById('grid-view-btn');
            if(gridBtn) gridBtn.style.display = 'none';
            const uploadTopBtnC = document.getElementById('reels-upload-top-btn');
            if(uploadTopBtnC) uploadTopBtnC.style.display = 'none';
            document.querySelectorAll('#reels-feed video').forEach(v => v.pause());
            // Alt nav butonlarını güncelle
            const bnavIds = [0,1,9,3,7];
            bnavIds.forEach(i => {
                const btn = document.getElementById('bnav-' + i);
                if(!btn) return;
                if(i === _prevTab) {
                    btn.classList.add('text-white','bg-zinc-800/80','shadow-inner');
                    btn.classList.remove('text-zinc-500');
                } else {
                    btn.classList.remove('text-white','bg-zinc-800/80','shadow-inner');
                    btn.classList.add('text-zinc-500');
                }
            });
            // Önceki sekmeye geç (reels değilse)
            const target = (_prevTab === 9) ? 0 : _prevTab;
            const tabs = ['screen-map','screen-chat','screen-market','screen-rank','screen-news','screen-missions','screen-premium','screen-profile','screen-referral'];
            tabs.forEach((t, i) => {
                const el = document.getElementById(t);
                if(!el) return;
                if(i === target) {
                    el.style.display = 'flex';
                    el.style.flexDirection = 'column';
                    el.style.zIndex = '20';
                    el.classList.remove('hidden');
                } else {
                    el.style.display = 'none';
                    el.classList.add('hidden');
                }
            });
            if(target === 0 && map) map.invalidateSize();
        }

        function toggleReelSound() {
            _reelMuted = !_reelMuted;
            const btn = document.getElementById('reel-sound-btn');
            if(btn) btn.textContent = _reelMuted ? '🔇' : '🔊';
            document.querySelectorAll('#reels-feed video').forEach(v => { v.muted = _reelMuted; });
        }

        // ── TEK merkezi IntersectionObserver — tüm feed kartları için ──
        // Kart başına değil, feed render bittikten sonra tek seferde kurulur.
        let _feedObserver = null;
        function _setupFeedObserver() {
            if(_feedObserver) { _feedObserver.disconnect(); _feedObserver = null; }
            if(_reelsGridMode) return; // Grid modunda observer gerekmez
            const feed = document.getElementById('reels-feed');
            if(!feed) return;
            _feedObserver = new IntersectionObserver(entries => {
                entries.forEach(entry => {
                    const video = entry.target.querySelector('video');
                    if(!video) return;
                    if(_reelsGridMode) { video.pause(); return; }
                    if(entry.isIntersecting) {
                        // Diğer tüm feed videolarını durdur → sadece görünür kart çalar
                        document.querySelectorAll('#reels-feed video').forEach(v => {
                            if(v !== video) v.pause();
                        });
                        video.muted = _reelMuted;
                        video.play().catch(() => { video.muted = true; video.play().catch(() => {}); });
                    } else {
                        video.pause();
                    }
                });
            }, { threshold: 0.6, rootMargin: '0px' });
            feed.querySelectorAll(':scope > div').forEach(card => _feedObserver.observe(card));
        }

        async function loadReels() {
            // Observer ve medyayı temizle
            if(_feedObserver) { _feedObserver.disconnect(); _feedObserver = null; }
            document.querySelectorAll('#reels-feed video, #reels-feed audio').forEach(el => {
                try { el.pause(); el.removeAttribute('src'); el.load(); } catch(_) {}
            });
            reelsData = [];
            const feed = document.getElementById('reels-feed');
            const emptyEl = document.getElementById('reels-empty');
            const loadingEl = document.getElementById('reels-loading');
            if(!feed) return;

            if(loadingEl) loadingEl.style.display = 'flex';
            if(emptyEl) emptyEl.classList.add('hidden');

            try {
                const res = await sendAction('get_reels', { offset: 0 });
                if(res && res.reels) reelsData = res.reels;
            } catch(e) { console.error('Reel yükleme hatası:', e); }

            if(loadingEl) loadingEl.style.display = 'none';

            const soundBtn = document.getElementById('reel-sound-btn');
            if(soundBtn) { soundBtn.style.display = 'flex'; soundBtn.textContent = _reelMuted ? '🔇' : '🔊'; }

            if(!reelsData.length) {
                if(emptyEl) emptyEl.classList.remove('hidden');
                return;
            }

            // Feed'i temizle ve yeniden render et
            while(feed.firstChild) feed.removeChild(feed.firstChild);
            reelsData.forEach((reel) => {
                try { renderReelCard(reel, feed); }
                catch(e) { console.error('Reel render hatası:', reel?.id, e); }
            });

            // Tek merkezi observer'ı kur (render bittikten sonra)
            requestAnimationFrame(() => _setupFeedObserver());
        }

        function renderReelCard(reel, container) {
            if(!reel) return;
            const user = db.users.find(u => u.username === reel.user) || { username: reel.user, avatar: '' };
            const avatar = user.avatar || 'https://cdn.freeridertr.com.tr/profil%20resmi/unnamed.jpg';
            const isLiked = currentUser && (reel.likes || []).includes(currentUser.username);
            const likeCount = (reel.likes || []).length;
            const isOwner = currentUser && (currentUser.username === reel.user || currentUser.role === 'Admin' || currentUser.role === 'SubAdmin');

            // Story halkası: db.stories içinde aktif story var mı?
            const now = Math.floor(Date.now() / 1000);
            const hasActiveStory = db.stories && db.stories.some(s => s.user === reel.user && s.expires_at > now);
            const avatarRingClass = hasActiveStory ? 'story-ring' : 'border-2 border-white';
            
            const card = document.createElement('div');
            card.className = 'relative w-full shrink-0 bg-black flex items-center justify-center';
            card.style.cssText = 'height:100dvh;scroll-snap-align:start;scroll-snap-stop:always;';
            
            let mediaHtml = '';
            if(reel.media_type === 'video') {
                mediaHtml = `<video src="${escapeHtml(reel.media_url)}" class="w-full h-full object-contain" playsinline loop autoplay style="max-height:100%;"></video>`;
            } else {
                mediaHtml = `<img src="${escapeHtml(reel.media_url)}" class="w-full h-full object-contain" style="max-height:100%;" loading="lazy">`;
            }
            
            const timeAgo = formatTimeAgo(reel.created_at);
            
            card.innerHTML = `
                ${mediaHtml}
                <!-- Play/Pause flash ikonu -->
                <div class="reel-play-flash" style="pointer-events:none;">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 80 80" width="80" height="80">
                        <circle cx="40" cy="40" r="38" fill="rgba(255,255,255,0.22)" stroke="rgba(255,255,255,0.5)" stroke-width="2"/>
                        <polygon class="flash-play-icon" points="30,22 62,40 30,58" fill="white" style="display:none;"/>
                        <g class="flash-pause-icon" style="display:none;">
                            <rect x="24" y="22" width="10" height="36" rx="3" fill="white"/>
                            <rect x="46" y="22" width="10" height="36" rx="3" fill="white"/>
                        </g>
                    </svg>
                </div>
                <!-- Gradient overlay -->
                <div class="absolute inset-0 bg-gradient-to-t from-black/80 via-transparent to-transparent pointer-events-none"></div>
                <!-- Sol alt: kullanıcı + açıklama -->
                <div class="absolute bottom-4 left-4 right-16 z-10">
                    <div class="flex items-center gap-2 mb-2 cursor-pointer" onclick="window.openProfileOrStory('${escapeHtml(reel.user)}')">
                        <div class="w-9 h-9 rounded-full overflow-hidden ${avatarRingClass} shrink-0">
                            <img src="${escapeHtml(avatar)}" class="w-full h-full object-cover">
                        </div>
                        <span class="text-white font-black text-sm drop-shadow-md">${escapeHtml(reel.user)}</span>
                        <span class="text-zinc-400 text-xs">${timeAgo}</span>
                    </div>
                    ${reel.caption ? `<p class="text-white text-sm leading-snug drop-shadow-md break-words line-clamp-2">${escapeHtml(reel.caption)}</p>` : ''}
                </div>
                <!-- Sağ: aksiyonlar -->
                <div class="absolute right-3 bottom-8 z-10 flex flex-col items-center gap-5">
                    <button onclick="toggleReelLike('${reel.id}', this)" class="flex flex-col items-center gap-1">
                        <div class="w-10 h-10 rounded-full bg-black/50 backdrop-blur flex items-center justify-center text-xl border border-white/20 ${isLiked ? 'text-sky-400' : 'text-white'}">${isLiked ? '❤️' : '🤍'}</div>
                        <span class="text-white text-xs font-bold drop-shadow-md reel-like-count">${likeCount}</span>
                    </button>
                    <button onclick="openReelComments('${reel.id}')" class="flex flex-col items-center gap-1">
                        <div class="w-10 h-10 rounded-full bg-black/50 backdrop-blur flex items-center justify-center text-xl border border-white/20 text-white">💬</div>
                        <span class="text-white text-xs font-bold drop-shadow-md">${reel.comment_count || 0}</span>
                    </button>
                    ${isOwner ? `<button onclick="deleteReel('${reel.id}')" class="flex flex-col items-center gap-1">
                        <div class="w-10 h-10 rounded-full bg-red-900/60 backdrop-blur flex items-center justify-center text-xl border border-sky-400/30 text-white">🗑️</div>
                    </button>` : ''}
                </div>
            `;
            container.appendChild(card);

            // ── Video tap-to-pause: click → SVG flash ikonu ──
            if(reel.media_type === 'video') {
                const video = card.querySelector('video');
                const flashEl = card.querySelector('.reel-play-flash');
                video.muted = _reelMuted;
                if(video && flashEl) {
                    const playIcon  = flashEl.querySelector('.flash-play-icon');
                    const pauseIcon = flashEl.querySelector('.flash-pause-icon');
                    video.addEventListener('click', function(e) {
                        e.stopPropagation();
                        if(video.paused) {
                            // Diğer tüm feed videolarını önce durdur
                            document.querySelectorAll('#reels-feed video').forEach(v => { if(v !== video) v.pause(); });
                            video.play().catch(()=>{});
                            if(playIcon)  playIcon.style.display = 'none';
                            if(pauseIcon) pauseIcon.style.display = 'block';
                        } else {
                            video.pause();
                            if(playIcon)  playIcon.style.display = 'block';
                            if(pauseIcon) pauseIcon.style.display = 'none';
                        }
                        flashEl.classList.remove('show');
                        void flashEl.offsetWidth;
                        flashEl.classList.add('show');
                    });
                }
            }
            // NOT: IntersectionObserver artık kart başına DEĞİL,
            // loadReels() sonunda _setupFeedObserver() ile tek seferde kurulur.
        }

        async function toggleReelLike(reelId, btn) {
            if(!currentUser) { alert('Beğenmek için giriş yapın!'); return; }
            try {
                const res = await sendAction('like_reel', { reel_id: reelId });
                if(res && res.status === 'ok') {
                    const icon = btn.querySelector('div');
                    const count = btn.querySelector('.reel-like-count');
                    if(icon) { icon.textContent = res.liked ? '❤️' : '🤍'; icon.className = icon.className.replace(/text-(red|white)-\d+/, res.liked ? 'text-sky-400' : 'text-white'); }
                    if(count) count.textContent = res.likes;
                }
            } catch(e) {}
        }

        async function deleteReel(reelId) {
            if(!confirm("Bu Reels'i silmek istediğinize emin misiniz?")) return;
            await sendAction('delete_reel', { reel_id: reelId });
            loadReels();
        }

        async function openReelComments(reelId) {
            currentReelId = reelId;
            const modal = document.getElementById('reel-comment-modal');
            const list = document.getElementById('reel-comments-list');
            modal.classList.remove('hidden');
            list.innerHTML = '<div class="text-zinc-500 text-sm text-center py-4">Yorumlar yükleniyor...</div>';
            try {
                const res = await sendAction('get_comments', { target_id: reelId });
                const comments = res.comments || [];
                if(!comments.length) {
                    list.innerHTML = '<div class="text-zinc-500 text-sm text-center py-4">Henüz yorum yok. İlk yorumu sen yap!</div>';
                    return;
                }
                list.innerHTML = comments.map(c => {
                    const u = db.users.find(x => x.username === c.user) || {};
                    const av = u.avatar || 'https://cdn.freeridertr.com.tr/profil%20resmi/unnamed.jpg';
                    return `<div class="flex items-start gap-2">
                        <img src="${escapeHtml(av)}" class="w-8 h-8 rounded-full object-cover shrink-0 border border-zinc-700">
                        <div class="bg-zinc-900/80 rounded-xl px-3 py-2 flex-1">
                            <span class="text-pink-400 font-black text-xs">${escapeHtml(c.user)} </span>
                            <span class="text-white text-xs">${escapeHtml(c.text)}</span>
                        </div>
                    </div>`;
                }).join('');
            } catch(e) { list.innerHTML = '<div class="text-zinc-500 text-sm text-center py-4">Yorumlar yüklenemedi.</div>'; }
        }

        async function submitReelComment() {
            if(!currentUser) { alert('Yorum yapmak için giriş yapın!'); return; }
            const inp = document.getElementById('reel-comment-input');
            const text = inp.value.trim();
            if(!text) return;
            inp.value = '';
            await sendAction('comment_reel', { reel_id: currentReelId, text });
            openReelComments(currentReelId);
        }

        function openReelUploadModal() {
            if(!currentUser) { alert('Reel paylaşmak için giriş yapın!'); return; }
            const modal = document.getElementById('reel-upload-modal');
            const infoEl = document.getElementById('reel-limit-info');
            const tier = getMyTier();
            let infoText = '';
            if(tier === 0) infoText = '⚪ Ücretsiz: Günde <b>1 fotoğraf</b> paylaşabilirsiniz. Video için Standart üyelik gerekli.';
            else if(tier === 1) infoText = '⭐ Standart: Günde <b>1 fotoğraf veya video</b> paylaşabilirsiniz.';
            else infoText = '💎 Deluxe/Ultra+: Günde <b>2 Reel</b> paylaşabilirsiniz.';
            if(infoEl) infoEl.innerHTML = infoText;
            // Video butonunu ücretsizler için soluk göster ama tıklanabilir bırak
            const videoLabel = document.getElementById('reel-video-btn');
            if(videoLabel) {
                videoLabel.style.opacity = tier >= 1 ? '1' : '0.5';
                videoLabel.title = tier < 1 ? 'Video için Standart üyelik gerekli' : '';
            }
            clearReelFile();
            modal.classList.remove('hidden');
        }

        function clearReelFile() {
            reelFileData = null;
            reelFileType = null;
            const previewCont = document.getElementById('reel-preview-container');
            const previewImg = document.getElementById('reel-preview-img');
            const previewVid = document.getElementById('reel-preview-video');
            if(previewCont) previewCont.classList.add('hidden');
            if(previewImg) { previewImg.classList.add('hidden'); previewImg.src = ''; }
            if(previewVid) { previewVid.classList.add('hidden'); previewVid.src = ''; }
            const pi = document.getElementById('reel-photo-input');
            const vi = document.getElementById('reel-video-input');
            if(pi) pi.value = '';
            if(vi) vi.value = '';
        }

        function getMyTier() {
            if(!currentUser) return 0;
            if(currentUser.role === 'Admin') return 3;
            let st = currentUser.stats;
            if(typeof st === 'string') { try { st = JSON.parse(st); } catch(e) { st = {}; } }
            return parseInt((st || {}).premium_tier || 0);
        }

        async function handleReelFile(input, type) {
            const tier = getMyTier();
            const file = input.files[0];
            if(!file) return;

            if(type === 'video') {
                if(tier < 1) {
                    input.value = '';
                    if(confirm("Video paylaşmak için Standart üyelik gereklidir. Üyelik almak ister misin?")) {
                        document.getElementById('reel-upload-modal').classList.add('hidden');
                        switchTab(6);
                    }
                    return;
                }
                if(file.size > 50 * 1024 * 1024) {
                    alert('Video boyutu maksimum 50MB olmalıdır!');
                    input.value = '';
                    return;
                }
            }

            const previewCont = document.getElementById('reel-preview-container');
            const previewImg = document.getElementById('reel-preview-img');
            const previewVid = document.getElementById('reel-preview-video');
            const compressInfo = document.getElementById('reel-compress-info');
            previewCont.classList.remove('hidden');

            if(type === 'image') {
                const compressed = await compressImage(file, 960, 0.75);
                reelFileData = compressed;
                reelFileType = 'image';
                previewImg.src = compressed;
                previewImg.classList.remove('hidden');
                previewVid.classList.add('hidden');
                if(compressInfo) compressInfo.classList.remove('hidden');
            } else {
                previewImg.classList.add('hidden');
                previewVid.classList.remove('hidden');
                if(compressInfo) compressInfo.classList.add('hidden');
                const loadDiv = document.createElement('div');
                loadDiv.id = 'reel-vid-loading';
                loadDiv.className = 'absolute inset-0 flex items-center justify-center bg-black/70 text-white text-xs font-bold z-10';
                loadDiv.textContent = 'Video hazırlanıyor...';
                previewCont.style.position = 'relative';
                previewCont.appendChild(loadDiv);
                reelFileData = null; // FileReader bitene kadar null
                reelFileType = 'video';
                previewVid.src = URL.createObjectURL(file);
                const reader = new FileReader();
                reader.onload = e => {
                    reelFileData = e.target.result;
                    const ld = document.getElementById('reel-vid-loading');
                    if(ld) ld.remove();
                };
                reader.onerror = () => {
                    alert('Video okunamadi, lutfen tekrar deneyin.');
                    clearReelFile();
                };
                reader.readAsDataURL(file);
            }
        }

        async function compressImage(file, maxSize, quality) {
            return new Promise(resolve => {
                const img = new Image();
                const url = URL.createObjectURL(file);
                img.onload = () => {
                    let w = img.width, h = img.height;
                    if(w > maxSize || h > maxSize) {
                        if(w > h) { h = Math.round(h * maxSize / w); w = maxSize; }
                        else { w = Math.round(w * maxSize / h); h = maxSize; }
                    }
                    const canvas = document.createElement('canvas');
                    canvas.width = w; canvas.height = h;
                    const ctx = canvas.getContext('2d');
                    ctx.drawImage(img, 0, 0, w, h);
                    URL.revokeObjectURL(url);
                    resolve(canvas.toDataURL('image/jpeg', quality));
                };
                img.src = url;
            });
        }

        async function submitReel() {
            if(!currentUser) return;

            // Video henüz FileReader ile okunuyorsa bekle
            if(reelFileType === 'video' && !reelFileData) {
                alert('Video hâlâ hazırlanıyor, lütfen birkaç saniye bekleyin.');
                return;
            }
            if(!reelFileData) { alert('Önce bir fotoğraf veya video seçin!'); return; }

            const caption = document.getElementById('reel-caption').value.trim();
            const submitBtn = document.getElementById('reel-submit-btn');
            const progressDiv = document.getElementById('reel-upload-progress');
            const progressBar = document.getElementById('reel-progress-bar');
            const progressLabel = progressDiv ? progressDiv.querySelector('.text-xs') : null;

            submitBtn.disabled = true;
            submitBtn.textContent = 'Yükleniyor...';
            if(progressDiv) progressDiv.classList.remove('hidden');

            function setProgress(pct, label) {
                if(progressBar) progressBar.style.width = pct + '%';
                if(progressLabel) progressLabel.textContent = label;
            }

            try {
                setProgress(15, reelFileType === 'video' ? 'Video sunucuya yükleniyor...' : 'Fotoğraf yükleniyor...');

                // Adım 1: Medyayı R2'ye yükle
                const uploadRes = await fetch('/api/data', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ action: 'upload_media', data: { media_data: reelFileData, folder: 'reels' } })
                });

                if(!uploadRes.ok) throw new Error('Sunucu hatası: ' + uploadRes.status);
                const uploadData = await uploadRes.json();
                setProgress(80, 'Reel kaydediliyor...');

                if(!uploadData || !uploadData.url) {
                    // Oturum süresi dolmuşsa yeniden giriş iste
                    if(uploadData?.message === 'Giriş yapmalısınız!') {
                        alert('Oturumun süresi dolmuş, lütfen tekrar giriş yap.');
                        logout();
                        return;
                    }
                    throw new Error(uploadData?.message || 'Medya sunucuya yüklenemedi.');
                }

                // Adım 2: Sadece URL ile add_reel — küçük payload
                const res = await fetch('/api/data', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ action: 'add_reel', data: {
                        media_url: uploadData.url,
                        media_type: reelFileType,
                        caption: caption
                    }})
                });

                if(!res.ok) throw new Error('Kayıt hatası: ' + res.status);
                const resData = await res.json();
                setProgress(100, 'Tamamlandı!');

                if(resData && resData.status === 'ok') {
                    setTimeout(() => {
                        document.getElementById('reel-upload-modal').classList.add('hidden');
                        clearReelFile();
                        document.getElementById('reel-caption').value = '';
                        loadReels();
                    }, 400);
                } else {
                    if(resData?.message === 'Giriş yapmalısınız!') { alert('Oturumun süresi dolmuş, lütfen tekrar giriş yap.'); logout(); return; }
                    alert(resData?.message || 'Reel paylaşılamadı, tekrar deneyin.');
                }
            } catch(e) {
                console.error('Reel upload error:', e);
                alert('Yükleme hatası: ' + (e.message || 'Bilinmeyen hata. Lütfen tekrar deneyin.'));
            } finally {
                submitBtn.disabled = false;
                submitBtn.textContent = 'PAYLAŞ';
                if(progressDiv) setTimeout(() => progressDiv.classList.add('hidden'), 600);
            }
        }

        function formatTimeAgo(ts) {
            if(!ts) return '';
            const diff = Math.floor(Date.now() / 1000) - ts;
            if(diff < 60) return 'Az önce';
            if(diff < 3600) return Math.floor(diff/60) + 'dk';
            if(diff < 86400) return Math.floor(diff/3600) + 'sa';
            return Math.floor(diff/86400) + 'g';
        }
        // ── Herhangi bir reel objesini direkt tam ekran aç ──
        // Hem profil grid tıklamasından hem de ileride başka yerlerden çağrılabilir.
        window.openReelDirect = function(reel) {
            if(!reel || !reel.media_url) return;
            stopAllMedia(); // Önceki sesleri temizle

            // Önce reels sekmesini arka planda aktif et (butonlar görünsün diye)
            const screenReels = document.getElementById('screen-reels');
            if(screenReels) {
                screenReels.style.display = 'flex';
                screenReels.style.flexDirection = 'column';
                screenReels.style.zIndex = '9990';
                screenReels.classList.remove('hidden');
            }
            const bottomNav = document.getElementById('bottom-nav');
            if(bottomNav) bottomNav.style.display = 'none';
            const soundBtn = document.getElementById('reel-sound-btn');
            if(soundBtn) { soundBtn.style.display = 'flex'; soundBtn.textContent = _reelMuted ? '🔇' : '🔊'; }
            const gridBtn = document.getElementById('grid-view-btn');
            if(gridBtn) gridBtn.style.display = 'flex';
            const uploadTopBtn = document.getElementById('reels-upload-top-btn');
            if(uploadTopBtn) uploadTopBtn.style.display = 'flex';

            // Önceki overlay varsa temizle
            const oldOverlay = document.getElementById('reel-direct-overlay');
            if(oldOverlay) oldOverlay.remove();

            const user = (typeof db !== 'undefined' && db.users)
                ? (db.users.find(u => u.username === reel.user) || { username: reel.user, avatar: '' })
                : { username: reel.user, avatar: '' };
            const avatar = user.avatar || 'https://cdn.freeridertr.com.tr/profil%20resmi/unnamed.jpg';
            const likeCount = (reel.likes || []).length;
            const timeAgo = typeof formatTimeAgo === 'function' ? formatTimeAgo(reel.created_at) : '';

            const overlay = document.createElement('div');
            overlay.id = 'reel-direct-overlay';
            overlay.style.cssText = 'position:absolute;inset:0;z-index:500;background:#000;display:flex;align-items:center;justify-content:center;';

            // Medya
            let mediaEl;
            if(reel.media_type === 'video') {
                mediaEl = document.createElement('video');
                mediaEl.src = reel.media_url;
                mediaEl.style.cssText = 'width:100%;height:100%;object-fit:contain;max-height:100%;';
                mediaEl.setAttribute('playsinline', '');
                mediaEl.setAttribute('loop', '');
                mediaEl.muted = _reelMuted;
                mediaEl.autoplay = true;
            } else {
                mediaEl = document.createElement('img');
                mediaEl.src = reel.media_url;
                mediaEl.style.cssText = 'width:100%;height:100%;object-fit:contain;max-height:100%;';
            }

            // Gradient overlay
            const grad = document.createElement('div');
            grad.style.cssText = 'position:absolute;inset:0;background:linear-gradient(to top,rgba(0,0,0,0.8) 0%,transparent 50%);pointer-events:none;';

            // Kapat butonu (sağ üst — overlay'e özel)
            const closeBtn = document.createElement('button');
            closeBtn.innerHTML = '✕';
            closeBtn.style.cssText = 'position:absolute;top:calc(env(safe-area-inset-top, 0px) + 72px);right:16px;z-index:10;width:44px;height:44px;border-radius:50%;background:rgba(0,0,0,0.65);color:#fff;font-size:18px;font-weight:bold;border:1px solid rgba(255,255,255,0.25);display:flex;align-items:center;justify-content:center;cursor:pointer;backdrop-filter:blur(4px);';
            closeBtn.onclick = () => {
                if(mediaEl.tagName === 'VIDEO') {
                    mediaEl.pause();
                    mediaEl.removeAttribute('src');
                    mediaEl.load(); // tarayıcıyı tamamen sıfırla, ses kesilir
                }
                overlay.remove();
                closeReels();
            };

            // Sol alt: kullanıcı + açıklama
            const info = document.createElement('div');
            info.style.cssText = 'position:absolute;bottom:16px;left:16px;right:64px;z-index:10;';
            info.innerHTML = `
                <div style="display:flex;align-items:center;gap:8px;margin-bottom:8px;cursor:pointer;" onclick="showOtherProfile('${escapeHtml(reel.user)}')">
                    <div style="width:36px;height:36px;border-radius:50%;overflow:hidden;border:2px solid #fff;flex-shrink:0;">
                        <img src="${escapeHtml(avatar)}" style="width:100%;height:100%;object-fit:cover;">
                    </div>
                    <span style="color:#fff;font-weight:900;font-size:14px;text-shadow:0 1px 4px rgba(0,0,0,0.8);">${escapeHtml(reel.user)}</span>
                    <span style="color:#a1a1aa;font-size:12px;">${timeAgo}</span>
                </div>
                ${reel.caption ? `<p style="color:#fff;font-size:13px;line-height:1.4;word-break:break-word;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden;">${escapeHtml(reel.caption)}</p>` : ''}
            `;

            // Sağ: beğeni
            const actions = document.createElement('div');
            actions.style.cssText = 'position:absolute;right:12px;bottom:32px;z-index:10;display:flex;flex-direction:column;align-items:center;gap:16px;';
            const isLiked = (typeof currentUser !== 'undefined' && currentUser) && (reel.likes || []).includes(currentUser.username);
            actions.innerHTML = `
                <div style="display:flex;flex-direction:column;align-items:center;gap:4px;">
                    <div style="width:40px;height:40px;border-radius:50%;background:rgba(0,0,0,0.5);backdrop-filter:blur(4px);display:flex;align-items:center;justify-content:center;font-size:20px;border:1px solid rgba(255,255,255,0.2);">${isLiked ? '❤️' : '🤍'}</div>
                    <span style="color:#fff;font-size:12px;font-weight:bold;">${likeCount}</span>
                </div>
            `;

            overlay.appendChild(mediaEl);
            overlay.appendChild(grad);
            overlay.appendChild(closeBtn);
            overlay.appendChild(info);
            overlay.appendChild(actions);

            if(screenReels) screenReels.appendChild(overlay);
            if(mediaEl.tagName === 'VIDEO') mediaEl.play().catch(()=>{});

            history.pushState({ reelDirect: true }, '');
        };

        // ── Merkezi popstate yöneticisi — tüm reel geri tuşu durumları ──
        window.addEventListener('popstate', function _reelDirectPopstate(e) {
            const state = e.state || {};
            if(state.reelDirect) {
                stopAllMedia();
                const ov = document.getElementById('reel-direct-overlay');
                if(ov) ov.remove();
                closeReels();
            }
            if(state.reelsOpen) {
                stopAllMedia();
                closeReels();
            }
            // reelFullscreen: yukarıdaki ayrı listener zaten handle ediyor
        });

        // ================================================================
        // REELS — YENİ GLOBAL FONKSİYONLAR
        // ================================================================

        // 1. Story varsa story görüntüleyiciyi aç, yoksa profile git
        window.openProfileOrStory = async function(username) {
            if(!username) return;
            const now = Math.floor(Date.now() / 1000);
            const activeStories = (db.stories || []).filter(s => s.user === username && s.expires_at > now);
            if(activeStories.length > 0) {
                // Story viewer'ı o kullanıcının story'siyle aç
                _storyList = activeStories;
                _storyIndex = 0;
                showCurrentStory();
                const modal = document.getElementById('story-view-modal');
                if(modal) modal.classList.remove('hidden');
            } else {
                showOtherProfile(username);
            }
        };

        // 2. Grid ↔ Feed geçiş
        let _reelsGridMode = false;
        let _reelFullscreenIdx = -1;
        let _reelFullscreenOverlay = null;

        window.toggleReelsGridView = function() {
            const feed = document.getElementById('reels-feed');
            const gridBtn = document.getElementById('grid-view-btn');
            const soundBtn = document.getElementById('reel-sound-btn');
            if(!feed) return;

            _reelsGridMode = !_reelsGridMode;

            if(_reelsGridMode) {
                // Grid moda geç
                // Observer'ı durdur — grid'de video otomatik çalmasın
                if(_feedObserver) { _feedObserver.disconnect(); _feedObserver = null; }
                feed.classList.add('grid-mode');
                if(soundBtn) soundBtn.style.display = 'none';
                // Tüm videoları durdur ve sessize al
                feed.querySelectorAll('video').forEach(v => { v.pause(); v.muted = true; });
                // Grid kartlarına click ekle (duplicate önleme: data flag ile)
                feed.querySelectorAll(':scope > div').forEach((card, idx) => {
                    card.dataset.reelIdx = idx;
                    if(!card.dataset.gridClickBound) {
                        card.dataset.gridClickBound = '1';
                        card.addEventListener('click', _onGridCardClick);
                    }
                    card.style.cursor = 'pointer';
                });
                if(gridBtn) gridBtn.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="width:18px;height:18px;"><rect x="2" y="3" width="20" height="18" rx="2"/><line x1="2" y1="9" x2="22" y2="9"/><line x1="2" y1="15" x2="22" y2="15"/></svg>`;
            } else {
                // Feed moduna dön
                feed.classList.remove('grid-mode');
                if(soundBtn && reelsData.length) soundBtn.style.display = 'flex';
                // Grid click listener'larını kaldır ve flag'i temizle
                feed.querySelectorAll(':scope > div').forEach(card => {
                    card.removeEventListener('click', _onGridCardClick);
                    delete card.dataset.gridClickBound;
                });
                // Observer'ı yeniden kur, mevcut scroll pozisyonunda oynayan videoyu başlat
                _setupFeedObserver();
                if(gridBtn) gridBtn.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="width:18px;height:18px;"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/></svg>`;
            }
        };

        // Grid kart click handler (ayrı referans olmalı ki removeEventListener çalışsın)
        function _onGridCardClick(e) {
            const idx = parseInt(this.dataset.reelIdx);
            if(!isNaN(idx)) window.openReelsGridItem(idx);
        }

        // 3. Izgaradan bir video → tam ekran
        // 3. Izgaradan bir video/fotoğraf → tam ekran (body'e ekle → fixed parent sorunu yok)
        window.openReelsGridItem = function(idx) {
            if(!reelsData[idx]) return;
            const reel = reelsData[idx];

            // Önceki overlay varsa sessizce temizle
            window.exitReelFullscreen(true);

            _reelFullscreenIdx = idx;

            const overlay = document.createElement('div');
            overlay.id = 'reel-fs-overlay';
            // body'e fixed ekliyoruz — screenReels'e değil (fixed-in-fixed sorunu çözüldü)
            overlay.style.cssText = 'position:fixed;inset:0;z-index:999999;background:#000;display:flex;align-items:center;justify-content:center;overflow:hidden;';

            // Kapatma butonu
            const closeBtn = document.createElement('button');
            closeBtn.innerHTML = '✕';
            closeBtn.style.cssText = 'position:absolute;top:calc(env(safe-area-inset-top,0px) + 72px);right:16px;z-index:10;width:44px;height:44px;border-radius:50%;background:rgba(0,0,0,0.7);color:#fff;font-size:18px;font-weight:bold;border:1.5px solid rgba(255,255,255,0.35);display:flex;align-items:center;justify-content:center;cursor:pointer;backdrop-filter:blur(4px);box-shadow:0 2px 12px rgba(0,0,0,0.6);';
            closeBtn.onclick = (e) => { e.stopPropagation(); window.exitReelFullscreen(false); };

            if(reel.media_type === 'video') {
                const video = document.createElement('video');
                video.src = reel.media_url;
                video.style.cssText = 'width:100%;height:100%;object-fit:contain;max-height:100%;display:block;';
                video.setAttribute('playsinline', '');
                video.setAttribute('loop', '');
                video.muted = false;
                video.autoplay = true;
                video.addEventListener('click', () => {
                    if(video.paused) video.play().catch(()=>{});
                    else video.pause();
                });
                overlay.appendChild(video);
                video.play().catch(() => { video.muted = true; video.play().catch(() => {}); });
            } else {
                const img = document.createElement('img');
                img.src = reel.media_url;
                img.style.cssText = 'width:100%;height:100%;object-fit:contain;max-height:100%;display:block;';
                overlay.appendChild(img);
            }

            overlay.appendChild(closeBtn);
            document.body.appendChild(overlay);  // ← body'e ekle
            _reelFullscreenOverlay = overlay;

            // Geri tuşu desteği
            history.pushState({ reelFullscreen: true, reelIdx: idx }, '');
        };

        // 4. Tam ekranı kapat → grid görünümüne geri dön
        window.exitReelFullscreen = function(silent) {
            const ov = document.getElementById('reel-fs-overlay');
            if(ov) {
                const v = ov.querySelector('video');
                if(v) { try { v.pause(); v.removeAttribute('src'); v.load(); } catch(_){} }
                ov.remove();
            }
            _reelFullscreenOverlay = null;
            _reelFullscreenIdx = -1;
            // Grid modundaysa ses butonunu gizli tut
            if(_reelsGridMode) {
                const soundBtn = document.getElementById('reel-sound-btn');
                if(soundBtn) soundBtn.style.display = 'none';
            }
        };

        // 5. Geri tuşu / popstate → tam ekranı kapat, grid'e dön
        window.addEventListener('popstate', function(e) {
            if(e.state && e.state.reelFullscreen) {
                window.exitReelFullscreen(false);
                e.preventDefault && e.preventDefault();
            }
        });

        // ================================================================
        // REELS SİSTEMİ JS SONU
        // ================================================================

        async function toggleRidingMode() {
            if(!currentUser) return;
            
            let stats = currentUser.stats || {};
            const isCurrentlyRiding = stats.riding_until && stats.riding_until > Date.now();
            
            if(isCurrentlyRiding) {
                if(confirm("Sürüş modunu kapatmak istiyor musun? Haritadan gizleneceksin.")) {
                    stats.riding_until = 0;
                    await sendAction('update_user', currentUser);
                    
                    document.getElementById("radar-info").classList.add("hidden");
                    document.getElementById("btn-riding-mode").innerHTML = "📡 RADAR (SÜRÜŞTEYİM)";
                    document.getElementById("btn-riding-mode").className = "bg-green-600/90 backdrop-blur hover:bg-green-500 btn-premium-hover px-3 py-2 rounded-xl shadow-[0_0_15px_rgba(34,197,94,0.4)] flex items-center justify-center text-[10px] uppercase tracking-widest font-bold text-white border border-green-400/50 pointer-events-auto";
                    
                    syncMap();
                    alert("Sürüş modu kapatıldı.");
                }
            } else {
                if(!userLat || !userLng) return alert("Konumunuz henüz bulunamadı. Lütfen önce 🎯 butonuna basarak konum izni verin.");
                
                if(confirm("Konumun 3 saat boyunca haritada diğer sürücülere canlı olarak gösterilecek. Onaylıyor musun?")) {
                    stats.riding_until = Date.now() + (3 * 60 * 60 * 1000); 
                    stats.riding_lat = userLat;
                    stats.riding_lng = userLng;
                    
                    await sendAction('update_user', currentUser);
                    
                    document.getElementById("radar-info").classList.remove("hidden");
                    document.getElementById("btn-riding-mode").innerHTML = "🛑 SÜRÜŞÜ BİTİR";
                    document.getElementById("btn-riding-mode").className = "bg-sky-600/90 backdrop-blur hover:bg-red-500 btn-premium-hover px-3 py-2 rounded-xl shadow-[0_0_15px_rgba(14,165,233,0.4)] flex items-center justify-center text-[10px] uppercase tracking-widest font-bold text-white border border-red-400/50 pointer-events-auto";
                    
                    syncMap();
                    alert("Sürüş modu aktif! Artık haritada radar olarak parlıyorsun.");
                }
            }
        }

        // ==============================================================
        // BİSİKLET DÜZENLEME VE SİLME FONKSİYONLARI 
        // ==============================================================
        async function deleteBike(index) {
            if(!confirm("Bu bisikleti garajından kalıcı olarak silmek istediğine emin misin?")) return;
            
            currentUser.stats.garage.splice(index, 1); 
            await sendAction('update_user', currentUser);
            const meIdx2 = db.users.findIndex(u => u.username === currentUser.username);
            if(meIdx2 !== -1) db.users[meIdx2] = {...db.users[meIdx2], stats: currentUser.stats};
            renderGarage(currentUser.username, 'self'); 
            document.getElementById("bike-detail-modal").classList.add("hidden"); 
        }

        function editBike(index) {
            document.getElementById("bike-detail-modal").classList.add("hidden");
            editingBikeIndex = index;
            const b = currentUser.stats.garage[index];
            if(!b) return;

            // Fill all fields safely
            const sf = (id, val) => { const el=document.getElementById(id); if(el) el.value=val||""; };
            sf("bike-model",    b.model);
            sf("bike-type",     b.type);
            sf("bike-fork",     b.fork);
            sf("bike-shock",    b.shock);
            sf("bike-brakes",   b.brakes);
            sf("bike-rotor",    b.rotor);
            sf("bike-drivetrain",b.drivetrain);
            sf("bike-chain",    b.chain);
            sf("bike-crankset", b.crankset);
            sf("bike-cassette", b.cassette);
            sf("bike-wheelset", b.wheelset);
            sf("bike-tires",    b.tires);
            sf("bike-tire-size",b.tire_size);
            sf("bike-handlebar",b.handlebar);
            sf("bike-stem",     b.stem);
            sf("bike-grips",    b.grips);
            sf("bike-seatpost", b.seatpost);
            sf("bike-saddle",   b.saddle);
            sf("bike-pedals",   b.pedals);
            sf("bike-weight",   b.weight);
            sf("bike-desc",     b.desc);
            sf("bike-photo",    "");

            const premTier = getUserPremiumTier(currentUser.username);
            let maxPhotos = premTier>=3?10:premTier>=2?4:premTier>=1?2:1;
            const lbl = document.getElementById("bike-photo-label");
            if(lbl) lbl.textContent = `Yeni Fotograf (Maks ${maxPhotos}) - Bos birakırsan eskileri kalır`;

            document.getElementById("add-bike-modal").classList.remove("hidden");
        }

        function openAddBikeModal() {
            if(!currentUser) return;
            editingBikeIndex = null; 
            
            const premTier = getUserPremiumTier(currentUser.username); 
            const garage = currentUser.stats.garage || [];
            
            let maxBikes = 0; 
            let maxPhotos = 1;
            
            if(premTier === 1) { maxBikes = 1; maxPhotos = 2; }
            if(premTier === 2) { maxBikes = 2; maxPhotos = 4; }
            if(premTier === 3) { maxBikes = 4; maxPhotos = 10; }
            
            if(premTier === 0) {
                alert("Plus üyeliği olmayan kullanıcılar garaja bisiklet ekleyemez! Pazar veya Plus menüsünden üyeliğini yükselt.");
                switchTab(6);
                return;
            }
            if(garage.length >= maxBikes) {
                return alert(`Mevcut paketiniz garajınıza en fazla ${maxBikes} bisiklet eklemenize izin veriyor! Plus menüsünden paketinizi yükseltin.`);
            }

            document.getElementById("bike-model").value = ""; 
            document.getElementById("bike-fork").value = ""; 
            document.getElementById("bike-shock").value = ""; 
            document.getElementById("bike-brakes").value = ""; 
            document.getElementById("bike-desc").value = ""; 
            document.getElementById("bike-photo").value = "";
            document.getElementById("bike-photo-label").textContent = `Bisiklet Fotoğrafları (Maksimum ${maxPhotos} adet)`;
            document.getElementById("add-bike-modal").classList.remove("hidden");
        }
        
        async function saveBike() {
            const premTier = getUserPremiumTier(currentUser.username);
            const model = document.getElementById("bike-model").value.trim();
            const type = document.getElementById("bike-type").value;
            const files = document.getElementById("bike-photo").files;

            if(!model) return alert("Bisiklet marka/modelini giriniz!");

            for(let i=0; i<files.length; i++) {
                if(!checkFileSize(files[i], 10)) return;
            }
            let maxPhotos = premTier >= 3 ? 10 : premTier >= 2 ? 4 : premTier >= 1 ? 2 : 1;
            if(files.length > maxPhotos) return alert(`En fazla ${maxPhotos} fotograf ekleyebilirsiniz.`);

            const g = id => { const el=document.getElementById(id); return el?el.value.trim():""; };
            const bikeData = {
                model, type,
                fork:        g("bike-fork"),
                shock:       g("bike-shock"),
                brakes:      g("bike-brakes"),
                rotor:       g("bike-rotor"),
                drivetrain:  g("bike-drivetrain"),
                chain:       g("bike-chain"),
                crankset:    g("bike-crankset"),
                cassette:    g("bike-cassette"),
                wheelset:    g("bike-wheelset"),
                tires:       g("bike-tires"),
                tire_size:   g("bike-tire-size"),
                handlebar:   g("bike-handlebar"),
                stem:        g("bike-stem"),
                grips:       g("bike-grips"),
                seatpost:    g("bike-seatpost"),
                saddle:      g("bike-saddle"),
                pedals:      g("bike-pedals"),
                weight:      g("bike-weight"),
                desc:        g("bike-desc"),
            };

            document.getElementById("add-bike-modal").classList.add("hidden");

            let photoDataArray = [];
            for(let i=0; i<Math.min(files.length, maxPhotos); i++) {
                let b64 = await resizeImage(files[i], 800);
                if(b64) photoDataArray.push(b64);
            }

            if(editingBikeIndex !== null) {
                const existing = currentUser.stats.garage[editingBikeIndex];
                Object.assign(existing, bikeData);
                if(photoDataArray.length > 0) existing.image = photoDataArray;
                alert("Bisiklet guncellendi!");
            } else {
                if(photoDataArray.length === 0) photoDataArray = ["https://placehold.co/400x300/121214/FFF?text=FOTO+YOK"];
                if(!currentUser.stats) currentUser.stats = {};
                if(!currentUser.stats.garage) currentUser.stats.garage = [];
                bikeData.id = Date.now();
                bikeData.image = photoDataArray;
                currentUser.stats.garage.push(bikeData);
                alert("Bisiklet garaja eklendi!");
            }
            await sendAction('update_user', currentUser);
            // Lokal db'yi güncelle
            const meIdx = db.users.findIndex(u => u.username === currentUser.username);
            if(meIdx !== -1) db.users[meIdx] = {...db.users[meIdx], stats: currentUser.stats};
            renderGarage(currentUser.username, 'self');
            editingBikeIndex = null;
        }
        function viewBikeDetail(username, index) {
            const u = db.users.find(x => x.username === username);
            if(!u || !u.stats || !u.stats.garage || !u.stats.garage[index]) return;
            const b = u.stats.garage[index];

            const imgContainer = document.getElementById("bd-image-container");
            imgContainer.innerHTML = "";
            let images = Array.isArray(b.image) ? b.image : [b.image||"https://placehold.co/400x300/121214/FFF?text=FOTO+YOK"];
            images.forEach(img => {
                imgContainer.innerHTML += `<img src="${img}" onclick="openFullscreen(images,${imgContainer.children.length})" class="h-full w-auto object-contain shrink-0 rounded-xl scroll-snap-align-center cursor-pointer hover:opacity-90 transition-opacity">`;
            });

            // Basic
            document.getElementById("bd-model").textContent  = b.model || "-";
            document.getElementById("bd-type").textContent   = b.type  || "-";
            document.getElementById("bd-fork").textContent   = b.fork  || "Belirtilmemis";
            document.getElementById("bd-shock").textContent  = b.shock || "Belirtilmemis";
            document.getElementById("bd-brakes").textContent = b.brakes|| "Belirtilmemis";
            document.getElementById("bd-desc").textContent   = b.desc  || "Belirtilmemis";

            // Extended fields - add dynamically if container exists
            const extra = document.getElementById("bd-extra-specs");
            if(extra) {
                const fields = [
                    ["Disk Caplaari", b.rotor],
                    ["Vites Sistemi", b.drivetrain],
                    ["Zincir", b.chain],
                    ["Krank / BB", b.crankset],
                    ["Kasnak", b.cassette],
                    ["Jantlar", b.wheelset],
                    ["Lastikler", b.tires],
                    ["Lastik Boyutu", b.tire_size],
                    ["Gidon", b.handlebar],
                    ["Stem", b.stem],
                    ["Tutus", b.grips],
                    ["Seatpost", b.seatpost],
                    ["Sele", b.saddle],
                    ["Pedallar", b.pedals],
                    ["Agirlik", b.weight],
                ];
                let extraHtml = "";
                fields.forEach(([label, val]) => {
                    if(val) extraHtml += `<div class="flex justify-between py-2 border-b border-zinc-800/50">
                        <span class="text-[10px] text-zinc-500 font-bold uppercase tracking-wider">${label}</span>
                        <span class="text-xs text-zinc-200 font-medium text-right max-w-[55%]">${val}</span>
                    </div>`;
                });
                extra.innerHTML = extraHtml || "<div class='text-zinc-600 text-xs italic'>Ek detay girilmemis.</div>";
            }

            const actionsArea = document.getElementById("bd-actions-area");
            if(actionsArea) {
                if(username === currentUser.username) {
                    actionsArea.innerHTML = `
                        <button onclick="editBike(${index})" class="flex-1 bg-blue-900/50 hover:bg-blue-800 btn-premium-hover transition text-blue-400 border border-blue-500/50 py-3 rounded-xl font-bold text-xs uppercase tracking-widest shadow-lg">DUZENLE</button>
                        <button onclick="deleteBike(${index})" class="flex-1 bg-red-950/50 hover:bg-sky-900/80 btn-premium-hover transition text-sky-400 border border-sky-900/50 py-3 rounded-xl font-bold text-xs uppercase tracking-widest">SIL</button>`;
                } else {
                    actionsArea.innerHTML = "";
                }
            }
            document.getElementById("bike-detail-modal").classList.remove("hidden");
        }

        function renderGarage(username, targetDivId = 'self') {
            const isSelf = targetDivId === 'self'; 
            const container = document.getElementById(isSelf ? "garage-list" : "op-garage"); 
            
            if(!container) return;
            
            let u = isSelf ? currentUser : db.users.find(x => x.username === username);
            
            if(!u || !u.stats || !u.stats.garage || u.stats.garage.length === 0) { 
                container.innerHTML = "<div class='col-span-2 text-center text-xs text-zinc-500 italic py-4'>Garaj boş.</div>"; 
                return; 
            }
            
            container.innerHTML = "";
            
            u.stats.garage.forEach((b, index) => {
                let delBtn = isSelf 
                    ? `<button onclick="event.stopPropagation(); deleteBike(${index})" class="absolute top-1 right-1 bg-red-600 hover:bg-red-500 transition w-6 h-6 rounded-full flex items-center justify-center text-white text-xs shadow-md z-20 btn-premium-hover">✕</button>` 
                    : '';
                
                let mainImg = Array.isArray(b.image) ? b.image[0] : (b.image || "https://placehold.co/400x300/121214/FFF?text=FOTO+YOK");
                
                container.innerHTML += `
                <div onclick="viewBikeDetail('${u.username}', ${index})" class="bg-black/50 rounded-xl overflow-hidden border border-zinc-800 shadow-md relative group cursor-pointer hover:border-zinc-500 transition btn-premium-hover">
                    ${delBtn}
                    <img src="${mainImg}" class="w-full h-24 object-cover">
                    <div class="p-2">
                        <div class="font-bold text-white text-[11px] truncate tracking-wide">${b.model}</div>
                        <div class="text-zinc-500 text-[9px] mt-0.5 truncate uppercase font-bold tracking-widest">${b.type}</div>
                    </div>
                </div>`;
            });
        }

        async function logout() {
            if(confirm("Sistemden çıkış yapmak istediğine emin misin?")) {
                try {
                    await sendAction('logout', {});
                } catch(e) {
                    console.log("Sunucu çıkış hatası, yerel veriler temizleniyor...");
                }
                
                localStorage.removeItem("fr_user");
                currentUser = null;
                
                window.location.reload();
            }
        }
        
        function loginSuccess() { 
            document.getElementById("login-screen").classList.add("hidden"); 
            document.getElementById("main-app").classList.remove("hidden");
            const _bnav = document.getElementById("bottom-nav");
            if(_bnav) _bnav.style.display = '';
            // Önceki oturumdan mesaj cache'i yükle (anlık görünsün)
            try {
                const cached = localStorage.getItem('fr_msg_cache');
                if(cached) {
                    const msgs = JSON.parse(cached);
                    if(msgs && msgs.length > 0 && db.messages.length === 0) {
                        db.messages = msgs;
                    }
                }
            } catch(e) {}
            
            // Initialize Onboarding Tour if needed
            setTimeout(() => {
                if(typeof OnboardingManager !== 'undefined') OnboardingManager.init();
            }, 1000);
            
            // Trial bitti mi kontrol
            if(currentUser.stats && currentUser.stats.trial_expired) {
                setTimeout(() => showTrialExpiredModal(), 2000);
            }
            // Trial aktif - banner goster
            if(currentUser.stats && currentUser.stats.is_trial && currentUser.stats.premium_tier === 3) {
                setTimeout(() => showTrialBanner(), 800);
            } 
            
            updateProfileUI(); 
            initMap(); 
            switchTab(0); 
            renderChat(true);
            // Çarkı önceden çiz — sekmede açılınca zaten hazır olsun
            setTimeout(initWheel3D, 500); 

            // Popup triggers removed per user request
            
            currentMessageCount = db.messages.length; 
            
            if(currentUser.stats && currentUser.stats.riding_until > Date.now()) {
                document.getElementById("radar-info").classList.remove("hidden");
                document.getElementById("btn-riding-mode").innerHTML = "🛑 SÜRÜŞÜ BİTİR";
                document.getElementById("btn-riding-mode").className = "bg-sky-600/90 backdrop-blur hover:bg-red-500 btn-premium-hover transition px-3 py-2 rounded-xl shadow-[0_0_15px_rgba(14,165,233,0.4)] flex items-center justify-center text-[10px] uppercase tracking-widest font-bold text-white border border-red-400/50 pointer-events-auto";
            }
            
            if (currentUser.stats && currentUser.stats.onboarding === false) {
                // Deneme bitiş tarihini doldur
                const expDate = currentUser.stats.premium_expire_date || '';
                const trialDateEl = document.getElementById('onboarding-trial-date');
                if(trialDateEl && expDate) {
                    trialDateEl.textContent = '⏰ Deneme Bitiş Tarihi: ' + expDate;
                }
                document.getElementById("onboarding-modal").classList.remove("hidden");
            }

            updateMyLocation();
            sendHeartbeat();
            // Heartbeat: her 30 sn (çevrim içi doğruluk için)
            setInterval(sendHeartbeat, 60000);
            // Konum + radar: her 60 sn
            setInterval(() => {
                updateMyLocation();
                refreshRadars();
            }, 60000);
            // Push bildirim: Profil sayfasındaki butondan açılıyor
            updateNotifBtnState();
            loadSavedTheme();
            _lastTitleName = getTitle(currentUser.xp).name;
            // OneSignal: kullanıcı kimliğini set et (bildirim hedefleme için)
            // setTimeout yerine doğrudan çağır — setOneSignalUser içinde Deferred kuyruğu kullanılıyor
            setOneSignalUser();
        }

        // ── Modern Premium Bildirim Popup ──
        function showPremiumNotifPopup() {
            const overlay = document.createElement('div');
            overlay.className = 'notif-popup-overlay';
            overlay.id = 'premium-notif-popup';
            overlay.onclick = function(e) { if(e.target === overlay) closePremiumNotifPopup(); };
            overlay.innerHTML = `
                <div class="notif-popup-card">
                    <button onclick="closePremiumNotifPopup()" style="position:absolute;top:12px;right:14px;background:rgba(255,255,255,0.1);border:none;color:#999;width:28px;height:28px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:14px;cursor:pointer;transition:0.2s;z-index:10" onmouseover="this.style.background='rgba(255,255,255,0.2)';this.style.color='#fff'" onmouseout="this.style.background='rgba(255,255,255,0.1)';this.style.color='#999'">✕</button>
                    <div style="text-align:center;margin-bottom:18px">
                        <div style="font-size:32px;margin-bottom:8px">🚴‍♂️</div>
                        <div style="font-size:16px;font-weight:900;color:#fff;letter-spacing:0.5px">FreeriderTR Plus</div>
                        <div style="font-size:10px;color:#94a3b8;font-weight:600;text-transform:uppercase;letter-spacing:2px;margin-top:4px">Premium Deneyim</div>
                    </div>
                    <div style="background:linear-gradient(135deg,rgba(59,130,246,0.15),rgba(168,85,247,0.1));border:1px solid rgba(59,130,246,0.2);border-radius:12px;padding:14px 16px;margin-bottom:18px">
                        <div style="display:flex;flex-direction:column;gap:8px">
                            <div style="display:flex;align-items:center;gap:8px;font-size:12px;color:#e2e8f0;font-weight:600">
                                <span style="font-size:14px">🎨</span> Özel isim renkleri ve profil efektleri
                            </div>
                            <div style="display:flex;align-items:center;gap:8px;font-size:12px;color:#e2e8f0;font-weight:600">
                                <span style="font-size:14px">🏍️</span> 4 bisiklet garajı ve 10 fotoğraflı ilanlar
                            </div>
                            <div style="display:flex;align-items:center;gap:8px;font-size:12px;color:#e2e8f0;font-weight:600">
                                <span style="font-size:14px">✅</span> Onaylı profil rozeti
                            </div>
                            <div style="display:flex;align-items:center;gap:8px;font-size:12px;color:#e2e8f0;font-weight:600">
                                <span style="font-size:14px">🤖</span> Sınırsız AI sohbet
                            </div>
                        </div>
                    </div>
                    <button onclick="closePremiumNotifPopup();switchTab(6);" style="width:100%;padding:12px;border:none;border-radius:12px;background:linear-gradient(135deg,#3b82f6,#8b5cf6);color:#fff;font-size:13px;font-weight:800;cursor:pointer;letter-spacing:0.5px;transition:0.2s;box-shadow:0 4px 20px rgba(59,130,246,0.4)" onmouseover="this.style.transform='translateY(-1px)';this.style.boxShadow='0 6px 25px rgba(59,130,246,0.5)'" onmouseout="this.style.transform='';this.style.boxShadow='0 4px 20px rgba(59,130,246,0.4)'">Paketleri İncele →</button>
                    <div style="text-align:center;margin-top:10px;font-size:10px;color:#64748b;font-weight:500">3 gün ücretsiz deneme ile başla</div>
                </div>
            `;
            document.body.appendChild(overlay);
        }
        function closePremiumNotifPopup() {
            const el = document.getElementById('premium-notif-popup');
            if(el) { el.style.opacity = '0'; el.style.transition = 'opacity 0.25s'; setTimeout(() => el.remove(), 250); }
        }

        async function refreshRadars() {
            try {
                const now = Date.now();
                // stats bir JSONB kolon - nested select sözdizimi yanlış, direkt stats seç
                const { data, error } = await supaClient.from('users')
                    .select('username, stats');
                        
                if (data && !error) {
                    data.forEach(fetchedUser => {
                        const s = fetchedUser.stats;
                        if (!s) return;
                        let existingUser = db.users.find(u => u.username === fetchedUser.username);
                        if (existingUser) {
                            if(!existingUser.stats) existingUser.stats = {};
                            // Radar güncelle
                            existingUser.stats.riding_lat = s.riding_lat;
                            existingUser.stats.riding_lng = s.riding_lng;
                            existingUser.stats.riding_until = s.riding_until;
                            // ÇEVRİM İÇİ: last_seen_ts güncelle (kritik!)
                            if (s.last_seen_ts) existingUser.stats.last_seen_ts = s.last_seen_ts;
                        }
                    });
                    if (map) syncMap();
                }
            } catch(e) { console.error("Radar hatası:", e); }
        }

        function updateProfileUI() {
            if(!currentUser) return;
            checkLevelUp();
            
            const stats = currentUser.stats || { markers: 0, events: 0, market: 0, profile_views: 0 };
            const premTier = parseInt(stats.premium_tier) || 0; 
            const premColor = stats.premium_color || 'std-blue';
            
            const textCls = (premTier > 0) ? getPremiumTextClass(premColor) : ''; 
            const inlineStyle = (premTier > 0) ? getPremiumInlineStyle(premColor) : '';
            const borderCls = (premTier > 0) ? getPremiumBorderClass(currentUser.username) : 'border-zinc-700';
            
            let tick = (premTier === 3) ? verifiedTick : ''; 
            let adminTag = (currentUser.role === 'Admin') ? '<span class="ml-2 bg-red-600 text-white px-2 py-0.5 rounded text-[9px] tracking-widest uppercase shadow-[0_0_10px_red] relative z-50">👑 Yönetici</span>' : (currentUser.role === 'SubAdmin' ? '<span class="ml-2 bg-orange-800 text-orange-200 px-2 py-0.5 rounded text-[9px] uppercase font-bold tracking-widest">🛡️ Yrd. Admin</span>' : '');
            
            const topUserEl = document.getElementById("top-username");
            topUserEl.innerHTML = `${currentUser.username} ${tick} ${adminTag}`; 
            topUserEl.className = `font-bold text-sm flex items-center transition-all ${textCls ? textCls : 'text-white'}`;
            topUserEl.setAttribute("style", inlineStyle);

            document.getElementById("top-avatar").src = currentUser.avatar || `https://cdn.freeridertr.com.tr/profil%20resmi/unnamed.jpg`; 
            document.getElementById("top-avatar").className = `w-10 h-10 rounded-full object-cover border transition-all ${borderCls}`;
            
            const title = getTitle(currentUser.xp); 
            document.getElementById("top-title").textContent = title.name;
            
            const profileNameEl = document.getElementById("profile-name");
            profileNameEl.innerHTML = `${currentUser.username} ${tick} ${adminTag}`; 
            profileNameEl.className = `text-4xl font-bold break-all teko-font tracking-wide flex justify-center items-center gap-2 drop-shadow-md transition-all ${textCls ? textCls : 'text-white'}`;
            profileNameEl.setAttribute("style", inlineStyle);

            document.getElementById("profile-bio").textContent = currentUser.bio || "Biyografi eklenmemiş."; 
            document.getElementById("profile-xp").textContent = currentUser.xp;
            
            document.getElementById("profile-avatar").src = currentUser.avatar || `https://cdn.freeridertr.com.tr/profil%20resmi/unnamed.jpg`; 
            document.getElementById("profile-avatar").className = `w-32 h-32 mx-auto rounded-full object-cover cursor-pointer bg-zinc-900 border-4 transition-all duration-300 group-hover:scale-105 ${borderCls}`;
            // Parcacik efektini uygula
            const myEffect = (currentUser.stats && currentUser.stats.avatar_effect) || 'none';
            applyAvatarEffect(myEffect);

            // Streak freeze badge
            const freezeBadge = document.getElementById('streak-freeze-badge');
            const freezeCount = document.getElementById('streak-freeze-count');
            const freezeAmt = parseInt(stats.streak_freeze||0);
            if(freezeBadge) {
                if(freezeAmt > 0) {
                    freezeBadge.classList.remove('hidden');
                    if(freezeCount) freezeCount.textContent = freezeAmt + ' adet kalkaning var';
                } else {
                    freezeBadge.classList.add('hidden');
                }
            }

            // Profil goruntuleme butonu guncelle
            const viewerBtn = document.getElementById('profile-viewer-btn-text');
            if(viewerBtn) {
                const viewCount = stats.profile_views || 0;
                const viewers = stats.profile_viewer_log || [];
                viewerBtn.textContent = viewCount + ' Profil Goruntulemesi - Kimlerin Gordu?';
            }
            document.getElementById("profile-title").textContent = title.icon + " " + title.name;
            document.getElementById("profile-title").className = `text-lg font-bold mt-2 drop-shadow-sm transition-colors ${title.color}`;

            // XP ilerleme cubugu
            const prog = getTitleProgress(currentUser.xp);
            const xpBarEl = document.getElementById("profile-xp-progress");
            if(xpBarEl) {
                if(prog.nextName) {
                    xpBarEl.innerHTML = `
                    <div class="mt-3 px-2">
                        <div class="flex justify-between text-[10px] font-bold uppercase tracking-widest mb-1">
                            <span class="${title.color}">${title.icon} ${title.name}</span>
                            <span class="text-zinc-400">${prog.xpLeft} XP sonra ${prog.nextIcon} ${prog.nextName}</span>
                        </div>
                        <div class="w-full bg-zinc-800 rounded-full h-2 overflow-hidden border border-zinc-700">
                            <div class="h-full rounded-full transition-all duration-700" style="width:${prog.percent}%;background:linear-gradient(90deg,#0ea5e9,#f59e0b);box-shadow:0 0 8px rgba(14,165,233,0.5);"></div>
                        </div>
                        <div class="text-center text-[10px] text-zinc-500 mt-1 font-bold">${prog.percent}% tamamlandi</div>
                    </div>`;
                } else {
                    xpBarEl.innerHTML = `<div class="mt-2 text-center text-xs font-bold text-prem-rainbow">MAX SEVIYE 🌟</div>`;
                }
            }

            let badges = "";
            // Premium badges - all with explicit blocks to avoid else-if chain issues
            if(stats.is_trial) { badges += `<span class="bg-gradient-to-r from-yellow-500 to-amber-400 text-black px-3 py-1.5 rounded-lg text-[10px] font-black shadow-[0_0_15px_rgba(234,179,8,0.6)] uppercase tracking-widest scale-in-anim animate-pulse">🎁 3 Gun Deneme</span> `; }
            if(premTier === 3) { badges += `<span class="bg-yellow-500 text-black px-3 py-1.5 rounded-lg text-[10px] font-black shadow-[0_0_15px_rgba(234,179,8,0.5)] uppercase tracking-widest scale-in-anim">👑 Ultra+</span> `; }
            else if(premTier === 2) { badges += `<span class="bg-purple-600 text-white px-3 py-1.5 rounded-lg text-[10px] font-bold shadow-[0_0_15px_rgba(168,85,247,0.5)] uppercase tracking-widest scale-in-anim">🌟 Deluxe</span> `; }
            else if(premTier === 1) { badges += `<span class="bg-gradient-to-r from-blue-600 to-purple-600 text-white px-3 py-1.5 rounded-lg text-[10px] font-bold shadow-lg uppercase tracking-widest scale-in-anim">⭐ Standart</span> `; }
            // Activity badges
            if(stats.markers >= 10){ badges += `<span class="bg-emerald-900/50 text-emerald-300 border border-emerald-700 px-2 py-1 rounded-lg text-[10px] font-bold scale-in-anim">🗺️ Haritaci</span> `; }
            else if(stats.markers >= 1){ badges += `<span class="bg-zinc-800 text-zinc-300 border border-zinc-700 px-2 py-1 rounded-lg text-[10px] font-bold scale-in-anim">📍 Kasif</span> `; }
            if(stats.events >= 5){ badges += `<span class="bg-blue-900/50 text-blue-300 border border-blue-700 px-2 py-1 rounded-lg text-[10px] font-bold scale-in-anim">🏆 Topluluk Lideri</span> `; }
            else if(stats.events >= 1){ badges += `<span class="bg-zinc-800 text-zinc-300 border border-zinc-700 px-2 py-1 rounded-lg text-[10px] font-bold scale-in-anim">📅 Organizator</span> `; }
            if(stats.market >= 5){ badges += `<span class="bg-amber-900/50 text-amber-300 border border-amber-700 px-2 py-1 rounded-lg text-[10px] font-bold scale-in-anim">💰 Pazar Ustasi</span> `; }
            else if(stats.market >= 1){ badges += `<span class="bg-zinc-800 text-zinc-300 border border-zinc-700 px-2 py-1 rounded-lg text-[10px] font-bold scale-in-anim">🤝 Esnaf</span> `; }
            if(stats.login_streak >= 100){ badges += `<span class="bg-violet-900/50 text-violet-300 border border-violet-700 px-2 py-1 rounded-lg text-[10px] font-bold scale-in-anim">⚡ 100 Gun</span> `; }
            else if(stats.login_streak >= 30){ badges += `<span class="bg-indigo-900/50 text-indigo-300 border border-indigo-700 px-2 py-1 rounded-lg text-[10px] font-bold scale-in-anim">💎 Demir Uye</span> `; }
            else if(stats.login_streak >= 7){ badges += `<span class="bg-orange-900/50 text-orange-300 border border-orange-700 px-2 py-1 rounded-lg text-[10px] font-bold scale-in-anim">🔥 Seri Girisci</span> `; }
            if(stats.total_messages >= 200){ badges += `<span class="bg-cyan-900/50 text-cyan-300 border border-cyan-700 px-2 py-1 rounded-lg text-[10px] font-bold scale-in-anim">👑 Chat Efsanesi</span> `; }
            else if(stats.total_messages >= 50){ badges += `<span class="bg-zinc-800 text-zinc-300 border border-zinc-700 px-2 py-1 rounded-lg text-[10px] font-bold scale-in-anim">🗣️ Sohbet Tutkunu</span> `; }
            // XP level badges
            if(currentUser.xp >= 50000){ badges += `<span class="bg-gradient-to-r from-red-700 to-purple-700 text-white px-2 py-1 rounded-lg text-[10px] font-black scale-in-anim text-prem-rainbow">🌟 Downhill Efsanesi</span> `; }
            else if(currentUser.xp >= 20000){ badges += `<span class="bg-red-900/50 text-red-300 border border-sky-600 px-2 py-1 rounded-lg text-[10px] font-bold scale-in-anim">👑 Efsane</span> `; }
            else if(currentUser.xp >= 10000){ badges += `<span class="bg-yellow-900/50 text-yellow-300 border border-yellow-700 px-2 py-1 rounded-lg text-[10px] font-bold scale-in-anim">🏆 Sampiyon</span> `; }
            else if(currentUser.xp >= 7000){ badges += `<span class="bg-rose-900/50 text-rose-300 border border-rose-700 px-2 py-1 rounded-lg text-[10px] font-bold scale-in-anim">💥 Elite</span> `; }
            else if(currentUser.xp >= 4000){ badges += `<span class="bg-orange-900/50 text-orange-300 border border-orange-700 px-2 py-1 rounded-lg text-[10px] font-bold scale-in-anim">🔥 Usta</span> `; }
            // Earned mission badges
            const eb = stats.earned_badges || [];
            eb.forEach(b => { badges += `<span class="bg-zinc-800 text-zinc-200 border border-zinc-600 px-2 py-1 rounded-lg text-[10px] font-bold scale-in-anim">🏅 ${b}</span> `; });

            if(!badges.trim()) {
                badges = "<span class='text-zinc-600 text-xs italic font-medium'>Henuz kazanilmis bir rozet yok.</span>";
            }
            document.getElementById("profile-badges").innerHTML = badges;
            
            if (currentUser.role === 'Admin' || currentUser.role === 'SubAdmin' || currentUser.username === 'Admin' || currentUser.username.toLowerCase() === 'admin') {
                document.getElementById("admin-btn").classList.remove("hidden");
            } else {
                document.getElementById("admin-btn").classList.add("hidden");
            }
            
            if(premTier > 0) {
                document.getElementById("premium-buy-section").classList.add("hidden");
                document.getElementById("premium-settings-section").classList.remove("hidden");

                // Paket kartlarını gizle (zaten üye, tekrar satın alma görseli gösterme)
                const packageCardsWrap = document.querySelector('#screen-premium .space-y-4');
                if (packageCardsWrap) packageCardsWrap.classList.add('hidden');

                // Aktif plan kartını doldur
                const planNames = { 1: '⭐ Standart Paket', 2: '🌟 Deluxe Paket', 3: '👑 Ultra+ Paket' };
                const planColors = { 1: 'bg-blue-900/60 text-blue-300 border border-blue-700/50', 2: 'bg-purple-900/60 text-purple-300 border border-purple-700/50', 3: 'bg-yellow-900/60 text-yellow-300 border border-yellow-700/50' };
                const planNameEl = document.getElementById('current-plan-name');
                const planBadgeEl = document.getElementById('current-plan-badge');
                const planExpiryEl = document.getElementById('current-plan-expiry');
                if (planNameEl) planNameEl.textContent = planNames[premTier] || 'Plus Üye';
                if (planBadgeEl) { planBadgeEl.textContent = 'AKTİF'; planBadgeEl.className = 'text-xs font-black px-3 py-1 rounded-lg ' + (planColors[premTier] || ''); }
                if (planExpiryEl) {
                    const expDate = stats.premium_expire_date;
                    planExpiryEl.textContent = expDate ? '📅 Bitiş tarihi: ' + expDate : '♾️ Süresiz aktif';
                }

                // Yükselt butonu: Standart (1) veya Deluxe (2) kullanıcısına göster, Ultra+ (3) için gizle
                const upgradeSec = document.getElementById('upgrade-plan-section');
                const upgradeSelect = document.getElementById('upgrade-tier-select');
                const upgradeHint = document.getElementById('upgrade-hint-text');
                if (premTier < 3 && upgradeSec && upgradeSelect) {
                    upgradeSec.classList.remove('hidden');
                    upgradeSelect.innerHTML = '';
                    if (premTier === 1) {
                        upgradeSelect.innerHTML += '<option value="freeridertr_deluxe_pack_monthly">🌟 Deluxe Paket — 20 TL/Ay</option>';
                        upgradeSelect.innerHTML += '<option value="freeridertr_ultra_pack_monthly">👑 Ultra+ Paket — 30 TL/Ay</option>';
                        if (upgradeHint) upgradeHint.textContent = 'Deluxe veya Ultra+ a gecerek daha fazla ozellik ac.';
                    } else if (premTier === 2) {
                        upgradeSelect.innerHTML += '<option value="freeridertr_ultra_pack_monthly">👑 Ultra+ Paket — 30 TL/Ay</option>';
                        if (upgradeHint) upgradeHint.textContent = 'Ultra+ a gecerek tum ozelliklerin kilidini ac.';
                    }
                } else if (upgradeSec) {
                    upgradeSec.classList.add('hidden');
                }

                const colorContainer = document.getElementById("color-options");
                if(colorContainer) {
                    let html = "";
                    if (premTier >= 1) {
                        html += `<div class="w-full text-[10px] text-zinc-500 uppercase tracking-widest font-bold mb-1 mt-2">Standart Renkler:</div>`;
                        html += createColorBtn('std-blue', 'Mavi', premColor);
                        html += createColorBtn('std-yellow', 'Sarı', premColor);
                        html += createColorBtn('std-pink', 'Pembe', premColor);
                        html += createColorBtn('std-green', 'Yeşil', premColor);
                    }
                    if (premTier >= 2) {
                        html += `<div class="w-full text-[10px] text-yellow-500 uppercase tracking-widest font-bold mb-1 mt-3 border-t border-zinc-800 pt-3">Deluxe Renkler:</div>`;
                        html += createColorBtn('ult-gold', 'Altın', premColor);
                        html += createColorBtn('ult-rainbow', 'Gökkuşağı', premColor);
                        html += createColorBtn('dlx-blue', 'Simli Mavi', premColor);
                        html += createColorBtn('dlx-pink', 'Simli Pembe', premColor);
                        html += createColorBtn('dlx-green', 'Simli Yeşil', premColor);
                    }
                    if (premTier >= 3) {
                        html += `<div class="w-full text-[10px] text-sky-400 uppercase tracking-widest font-bold mb-1 mt-3 border-t border-zinc-800 pt-3">Ultra+ Özel Renk (Hex):</div>`;
                        html += `<div class="w-full flex gap-2 mb-2 items-center">
                                    <input type="color" id="custom-hex-color" class="w-12 h-10 rounded cursor-pointer bg-zinc-900 border border-zinc-700 shadow-inner" value="${premColor.startsWith('#') ? premColor : '#ff0000'}">
                                    <button onclick="applyCustomHex()" class="bg-white text-black px-4 py-2 rounded-lg text-xs font-bold shadow-lg hover:bg-gray-200 transition btn-premium-hover">Uygula</button>
                                 </div>`;
                        
                        html += `<div class="w-full text-[10px] text-sky-400 uppercase tracking-widest font-bold mb-1 mt-2">Ultra+ Profil Efekti:</div>`;
                        const currentEffect = stats.avatar_effect || 'none';
                        html += createEffectBtn('none', 'Efekt Yok', currentEffect);
                        html += createEffectBtn('fire', '🔥 Alev', currentEffect);
                        html += createEffectBtn('ice', '❄️ Buz', currentEffect);
                    }
                    colorContainer.innerHTML = html;
                }
            } else {
                document.getElementById("premium-buy-section").classList.remove("hidden");
                document.getElementById("premium-settings-section").classList.add("hidden");
                // Üye değilse paket kartlarını tekrar göster
                const packageCardsWrap = document.querySelector('#screen-premium .space-y-4');
                if (packageCardsWrap) packageCardsWrap.classList.remove('hidden');
            }
            
            renderGarage(currentUser.username, 'self');
        }

        // ── Google Play IAP Satın Alma Akışı ──────────────────────────────────────
        // ── Web / Tarayıcı Satın Alma Talebi ─────────────────────────────────────
        // Android/iOS yoksa admin'e DM + push bildirimi gönderir.
        async function _sendWebPurchaseRequest(productId) {
            const confirmed = window.confirm(
                'Web üzerinden alımlarda ödeme onayı için yönetici ile iletişime geçilecektir.\\n\\nDevam etmek istiyor musunuz?'
            );
            if (!confirmed) return;

            const btns = document.querySelectorAll('[onclick*="requestPremium"],[onclick*="requestUpgrade"],[onclick*="handleBuyButton"]');
            btns.forEach(b => { b.disabled = true; b.style.opacity = '0.6'; });

            try {
                const res = await fetch('/api/web_purchase_request', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    credentials: 'include',
                    body: JSON.stringify({ productId })
                });
                const data = await res.json();
                if (data.status === 'ok') {
                    showToast(data.message || '✅ Talebiniz yöneticiye iletildi!');
                } else if (data.status === 'wait') {
                    showToast(data.message || '⏳ Zaten bir talebiniz var, lütfen bekleyin.');
                } else {
                    showToast('❌ ' + (data.message || 'Bir hata oluştu, tekrar deneyin.'));
                }
            } catch(err) {
                console.error('[IAP] Web purchase request hatası:', err);
                showToast('❌ Bağlantı hatası. İnternet bağlantınızı kontrol edin.');
            } finally {
                btns.forEach(b => { b.disabled = false; b.style.opacity = '1'; });
            }
        }

        // requestPremium() fonksiyonu artık Google Play Billing Library'yi tetikler.
        // Mobil uygulama (WebView içinde), bu fonksiyonu çağıran JS Bridge üzerinden
        // Android uygulamasına productId'yi iletir ve satın alım akışını başlatır.
        // Satın alım tamamlandığında Android, verifyGooglePurchase() fonksiyonunu
        // çağırarak purchaseToken'ı backend'e doğrulama için gönderir.
        async function requestPremium() {
            const sel = document.getElementById("premium-tier-select");
            if (!sel) { showToast('⚠️ Ürün seçici bulunamadı.'); return; }
            const productId = sel.value;
            if (!productId) { showToast('⚠️ Lütfen bir paket seçin.'); return; }

            // ── Android WebView JS Bridge kontrolü ──────────────────────────────
            // window.Android nesnesi yoksa veya launchBilling metodu tanımlı değilse
            // uyarı göster; uygulamayı çökertme.
            if (typeof window.Android !== 'undefined' && window.Android !== null) {
                if (typeof window.Android.launchBilling === 'function') {
                    try {
                        window.Android.launchBilling(productId);
                    } catch(e) {
                        showToast('Google Play başlatılamadı. Lütfen tekrar deneyin.');
                        console.error('[IAP] launchBilling hatası:', e);
                    }
                    return;
                } else {
                    // window.Android var ama launchBilling metodu yok → eski uygulama sürümü
                    showToast("⚠️ Uygulama güncel değil. Lütfen Google Play'den güncelleyin.");
                    console.warn('[IAP] window.Android mevcut ama launchBilling metodu yok.');
                    return;
                }
            }

            // iOS WKWebView köprüsü (gelecekteki iOS desteği için)
            if (window.webkit && window.webkit.messageHandlers && window.webkit.messageHandlers.billing) {
                try {
                    window.webkit.messageHandlers.billing.postMessage({ productId });
                } catch(e) {
                    showToast('In-app satın alım başlatılamadı.');
                }
                return;
            }

            // Tarayıcı / web ortamı → admin'e satın alma talebi gönder
            await _sendWebPurchaseRequest(productId);
        }

        // ── Üyelik Yükseltme ─────────────────────────────────────────────────────
        async function requestUpgrade() {
            const sel = document.getElementById("upgrade-tier-select");
            if (!sel) { showToast('⚠️ Yükseltme seçici bulunamadı.'); return; }
            const productId = sel.value;
            if (!productId) { showToast('⚠️ Lütfen bir paket seçin.'); return; }

            if (typeof window.Android !== 'undefined' && window.Android !== null) {
                if (typeof window.Android.launchBilling === 'function') {
                    try {
                        window.Android.launchBilling(productId);
                    } catch(e) {
                        showToast('Google Play başlatılamadı. Lütfen tekrar deneyin.');
                        console.error('[IAP] launchBilling hatası:', e);
                    }
                    return;
                } else {
                    showToast("⚠️ Uygulama güncel değil. Lütfen Google Play'den güncelleyin.");
                    return;
                }
            }
            if (window.webkit && window.webkit.messageHandlers && window.webkit.messageHandlers.billing) {
                try { window.webkit.messageHandlers.billing.postMessage({ productId }); } catch(e) { showToast('In-app satın alım başlatılamadı.'); }
                return;
            }
            // Tarayıcı / web ortamı → admin'e satın alma talebi gönder
            await _sendWebPurchaseRequest(productId);
        }

        // Android uygulaması satın alım tamamlandığında bu fonksiyonu çağırır.
        // Android kodu: webView.evaluateJavascript("verifyGooglePurchase(...)", null);
        async function verifyGooglePurchase(purchaseToken, productId, purchaseType) {
            try {
                showToast('Ödeme doğrulanıyor...');
                const res = await fetch('/api/verify_google_purchase', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        purchaseToken: purchaseToken,
                        productId:     productId,
                        purchaseType:  purchaseType || 'subscription'
                    })
                });
                const json = await res.json();
                if (json.status === 'ok') {
                    showToast('✅ Aboneliğin aktive edildi! Hoş geldin.');
                    // Kullanıcı verilerini yenile
                    await loadMyData();
                    renderProfile();
                } else {
                    showToast('⚠️ Doğrulama hatası: ' + (json.message || 'Bilinmeyen hata'));
                }
            } catch(e) {
                showToast('Ağ hatası oluştu, lütfen tekrar deneyin.');
            }
        }

        async function showOtherProfile(targetUsername) {
            if(targetUsername === currentUser.username) { 
                switchTab(7); 
                document.getElementById('market-detail-modal').classList.add('hidden'); 
                return; 
            }
            
            let u = db.users.find(x => x.username === targetUsername); 
            if(!u) {
                try {
                    const { data, error } = await supaClient.from('users').select('*').eq('username', targetUsername).single();
                    if(data) {
                        u = data;
                        db.users.push(u);
                    } else {
                        return;
                    }
                } catch(e) { return; }
            }

            sendAction('increment_profile_view', { username: targetUsername }).catch(e => {});

            const stats = u.stats || { markers: 0, events: 0, market: 0, profile_views: 0 };
            const premTier = parseInt(stats.premium_tier) || 0; 
            const premColor = stats.premium_color || 'std-blue';
            
            const textCls = (premTier > 0) ? getPremiumTextClass(premColor) : ''; 
            const inlineStyle = (premTier > 0) ? getPremiumInlineStyle(premColor) : '';
            const borderCls = (premTier > 0) ? getPremiumBorderClass(u.username) : 'border-zinc-700';
            
            let tick = (premTier === 3) ? verifiedTick : ''; 
            let adminTag = (u.role === 'Admin') ? '<span class="ml-2 bg-red-600 text-white px-2 py-0.5 rounded text-[9px] uppercase font-bold tracking-widest shadow-[0_0_10px_red]">👑 Yönetici</span>' : (u.role === 'SubAdmin' ? '<span class="ml-2 bg-orange-800 text-orange-200 px-2 py-0.5 rounded text-[9px] uppercase font-bold tracking-widest">🛡️ Yrd. Admin</span>' : '');

            document.getElementById("op-avatar").src = u.avatar || `https://cdn.freeridertr.com.tr/profil%20resmi/unnamed.jpg`; 
            document.getElementById("op-avatar").className = `w-28 h-28 mx-auto rounded-full object-cover mt-6 bg-zinc-950 shadow-xl border-4 transition-all duration-300 ${borderCls}`;
            
            const badge = document.getElementById("op-premium-badge");
            if(premTier === 3) { 
                badge.classList.remove("hidden"); 
                badge.className = `mt-3 text-[10px] font-black uppercase tracking-widest text-yellow-500 drop-shadow-sm`; 
                badge.textContent = "👑 Ultra+"; 
            } else if (premTier === 2) { 
                badge.classList.remove("hidden"); 
                badge.className = `mt-3 text-[10px] font-bold uppercase tracking-widest text-purple-400 drop-shadow-sm`; 
                badge.textContent = "🌟 Deluxe"; 
            } else if (premTier === 1) { 
                badge.classList.remove("hidden"); 
                badge.className = `mt-3 text-[10px] font-bold uppercase tracking-widest drop-shadow-sm ${textCls}`; 
                badge.textContent = "⭐ Standart"; 
            } else { 
                badge.classList.add("hidden"); 
            }

            const opNameEl = document.getElementById("op-username");
            opNameEl.innerHTML = `${u.username} ${tick} ${adminTag}`; 
            opNameEl.className = `text-4xl font-bold break-all teko-font tracking-wide flex items-center justify-center drop-shadow-md transition-all ${textCls ? textCls : 'text-white'}`;
            opNameEl.setAttribute("style", inlineStyle);
            
            const tickBox = document.getElementById("op-verified-badge");
            if (premTier === 3) { 
                tickBox.innerHTML = verifiedTick; 
                tickBox.classList.remove("hidden"); 
            } else { 
                tickBox.classList.add("hidden"); 
            }
            
            document.getElementById("op-bio").textContent = u.bio || "Kullanıcı biyo girmemiş."; 
            document.getElementById("op-xp").textContent = u.xp;
            
            const title = getTitle(u.xp); 
            document.getElementById("op-title").textContent = title.name; 
            document.getElementById("op-title").className = `text-sm font-bold truncate uppercase mt-1 drop-shadow-sm ${title.color}`;
            
            const opOnlineEl = document.getElementById("op-online-status");
            if(opOnlineEl) {
                const s = getOnlineStatus(u);
                if(s.status === 'online') {
                    opOnlineEl.innerHTML = `<span class="online-dot-sm"></span><span class="online-label">${s.label}</span>`;
                    opOnlineEl.className = "flex items-center gap-2 justify-center mt-2";
                } else if(s.status === 'recent') {
                    opOnlineEl.innerHTML = `<span class="recent-dot"></span><span class="recent-label">${s.label}</span>`;
                    opOnlineEl.className = "flex items-center gap-2 justify-center mt-2";
                } else {
                    opOnlineEl.innerHTML = '';
                    opOnlineEl.className = "hidden";
                }
            }

            
            let badges = "";
            if(stats.markers >= 1){ badges += `<span class="bg-zinc-800 text-zinc-300 border border-zinc-700 px-3 py-1 rounded-lg text-[10px] font-bold shadow-sm">📍 Kâşif</span>`; }
            if(stats.events >= 1){ badges += `<span class="bg-zinc-800 text-zinc-300 border border-zinc-700 px-3 py-1 rounded-lg text-[10px] font-bold shadow-sm">📅 Organizatör</span>`; }
            if(stats.market >= 1){ badges += `<span class="bg-zinc-800 text-zinc-300 border border-zinc-700 px-3 py-1 rounded-lg text-[10px] font-bold shadow-sm">🤝 Esnaf</span>`; }
            if(u.xp > 1000){ badges += `<span class="bg-orange-900/50 text-orange-300 border border-orange-700 px-3 py-1 rounded-lg text-[10px] font-bold shadow-sm">🔥 Kıdemli</span>`; }
            
            if(badges === "") {
                badges = "<span class='text-zinc-500 text-xs italic font-medium'>Rozet yok.</span>";
            }
            document.getElementById("op-badges").innerHTML = badges;

            renderGarage(u.username, 'other');

            let actionsHtml = `<button onclick="startDm('${u.username}')" class="bg-white hover:bg-gray-200 transition text-black py-4 rounded-xl text-sm font-bold w-full shadow-[0_0_15px_rgba(255,255,255,0.3)] mb-3 btn-premium-hover">💬 ÖZEL MESAJ</button>`;
            
            // Engel durumunu kontrol et
            const myBlockedList = (currentUser.stats && currentUser.stats.blocked_users) ? currentUser.stats.blocked_users : [];
            const isBlocked = myBlockedList.includes(u.username);
            if(isBlocked) {
                actionsHtml += `<button onclick="unblockUser('${u.username}')" class="w-full bg-zinc-900 border border-zinc-700 hover:bg-zinc-800 transition text-zinc-400 py-3 rounded-xl font-bold text-xs uppercase tracking-widest mb-3 btn-premium-hover">✅ ENGELİ KALDIR</button>`;
            } else {
                actionsHtml += `<button onclick="blockUser('${u.username}')" class="w-full bg-black border border-sky-900/50 hover:bg-red-950/30 transition text-sky-400 py-3 rounded-xl font-bold text-xs uppercase tracking-widest mb-2 btn-premium-hover">🚫 ENGELLE</button>`;
            }
            actionsHtml += `<button onclick="openReportUserModal('${u.username}')" class="w-full bg-black border border-orange-900/50 hover:bg-orange-950/20 transition text-orange-400 py-3 rounded-xl font-bold text-xs uppercase tracking-widest mb-3 btn-premium-hover">🚨 ŞİKAYET ET</button>`;
            
            if(currentUser.role === 'Admin' || currentUser.username === 'Admin' || currentUser.username.toLowerCase() === 'admin') {
                actionsHtml += `
                <div class="rounded-2xl p-4 border border-zinc-700/60 mb-3" style="background:rgba(0,0,0,0.5)">
                    <div class="text-[10px] text-zinc-400 uppercase font-bold tracking-widest mb-3">👑 Ana Admin — Yönetim</div>
                    <div class="flex gap-2 mb-3">
                        <select id="admin-tier-select" class="flex-1 bg-zinc-900 border border-zinc-600 rounded-lg px-3 py-2 text-white text-xs outline-none cursor-pointer font-bold">
                            <option value="0" ${stats.premium_tier == 0 ? 'selected' : ''}>Ücretsiz (İptal)</option>
                            <option value="1" ${stats.premium_tier == 1 ? 'selected' : ''}>⭐ Standart</option>
                            <option value="2" ${stats.premium_tier == 2 ? 'selected' : ''}>🌟 Deluxe</option>
                            <option value="3" ${stats.premium_tier == 3 ? 'selected' : ''}>👑 Ultra+</option>
                        </select>
                        <button onclick="adminSetPremium('${u.username}')" class="bg-gradient-to-r from-purple-700 to-pink-700 hover:opacity-90 text-white py-2 px-4 rounded-lg text-[10px] font-bold transition uppercase tracking-widest btn-premium-hover">KAYDET</button>
                    </div>
                    <div class="flex gap-2 mb-3">
                        <input id="admin-xp-amount" type="number" placeholder="XP miktarı" class="w-1/2 bg-black/60 text-white rounded-xl px-4 py-3 text-sm border border-zinc-700 outline-none focus:border-white transition font-bold">
                        <button onclick="giveXP('${u.username}')" class="w-1/2 bg-zinc-800 hover:bg-zinc-700 transition text-white py-3 rounded-xl text-xs font-bold uppercase tracking-widest btn-premium-hover">XP VER</button>
                    </div>
                    <div class="grid grid-cols-2 gap-2">
                        <button onclick="openUserActivity('${u.username}')" class="bg-blue-950/50 hover:bg-blue-900/60 transition text-blue-400 py-3 rounded-xl text-xs font-bold uppercase tracking-widest border border-blue-800/50 btn-premium-hover">🔍 Aktivite</button>
                        <button onclick="banUser('${u.username}')" class="bg-red-950/50 hover:bg-sky-900/80 transition text-sky-400 py-3 rounded-xl text-xs font-bold uppercase tracking-widest border border-sky-800/50 btn-premium-hover">🚨 Banla</button>
                    </div>
                </div>`;
            } else if(currentUser.role === 'SubAdmin') {
                actionsHtml += `
                <div class="rounded-2xl p-4 border border-orange-900/40 mb-3" style="background:rgba(120,53,15,0.12)">
                    <div class="text-[10px] text-orange-400 uppercase font-bold tracking-widest mb-3">🛡️ Yrd. Admin İşlemleri</div>
                    <div class="grid grid-cols-2 gap-2">
                        <button onclick="openUserActivity('${u.username}')" class="bg-blue-950/50 hover:bg-blue-900/60 transition text-blue-400 py-3 rounded-xl text-xs font-bold uppercase tracking-widest border border-blue-800/50 btn-premium-hover">🔍 Aktivite</button>
                        <button onclick="banUser('${u.username}')" class="bg-red-950/50 hover:bg-sky-900/80 transition text-sky-400 py-3 rounded-xl text-xs font-bold uppercase tracking-widest border border-sky-800/50 btn-premium-hover">🚨 Banla</button>
                    </div>
                </div>`;
            }
            
            document.getElementById("op-actions").innerHTML = actionsHtml;

            // ── Profil Reels Sekmesi ──
            // op-actions altına reels tab ekle (varsa önce temizle)
            const existingReelsTab = document.getElementById('op-reels-section');
            if(existingReelsTab) existingReelsTab.remove();
            const reelsSection = document.createElement('div');
            reelsSection.id = 'op-reels-section';
            reelsSection.className = 'mt-4';
            reelsSection.innerHTML = `
                <div class="flex items-center gap-2 mb-3">
                    <button id="op-reels-tab-btn" onclick="window.loadOtherProfileReels('${escapeHtml(u.username)}')"
                        class="flex-1 flex items-center justify-center gap-2 py-2.5 rounded-xl bg-gradient-to-r from-pink-900/60 to-sky-900/40 border border-pink-700/40 text-white text-xs font-black uppercase tracking-widest hover:opacity-90 transition btn-premium-hover">
                        🎬 Reels'leri Gör
                    </button>
                </div>
                <div id="op-reels-grid" class="hidden grid grid-cols-3 gap-1 rounded-xl overflow-hidden"></div>
                <div id="op-reels-loading" class="hidden flex items-center justify-center py-6">
                    <div class="w-6 h-6 rounded-full border-2 border-pink-500 border-t-transparent animate-spin"></div>
                </div>
                <div id="op-reels-empty" class="hidden text-center text-zinc-500 text-xs py-4">Bu kullanıcının henüz Reels paylaşımı yok.</div>
            `;
            const opActionsEl = document.getElementById('op-actions');
            if(opActionsEl && opActionsEl.parentNode) {
                opActionsEl.parentNode.insertBefore(reelsSection, opActionsEl.nextSibling);
            }

            document.getElementById("other-profile-modal").classList.remove("hidden");
        }

        // ── Diğer Kullanıcının Reels'lerini Yükle ──
        window.loadOtherProfileReels = async function(profileUsername) {
            const grid    = document.getElementById('op-reels-grid');
            const loading = document.getElementById('op-reels-loading');
            const empty   = document.getElementById('op-reels-empty');
            const tabBtn  = document.getElementById('op-reels-tab-btn');
            if(!grid) return;

            // Butonu gizle, loading göster
            if(tabBtn) tabBtn.style.display = 'none';
            if(loading) { loading.classList.remove('hidden'); loading.style.display = 'flex'; }
            if(empty) empty.classList.add('hidden');
            grid.classList.add('hidden');
            grid.innerHTML = '';

            try {
                // Supabase'den doğrudan sorgula
                const { data, error } = await supaClient
                    .from('reels')
                    .select('id, media_url, media_type, caption, likes, created_at')
                    .eq('user', profileUsername)
                    .order('created_at', { ascending: false })
                    .limit(12);

                if(loading) { loading.classList.add('hidden'); loading.style.display = 'none'; }

                const reels = data || [];
                if(reels.length === 0) {
                    if(empty) empty.classList.remove('hidden');
                    return;
                }

                reels.forEach((r, idx) => {
                    const item = document.createElement('div');
                    item.className = 'relative aspect-square bg-zinc-900 overflow-hidden cursor-pointer';
                    item.style.cssText = 'border-radius:4px;';

                    if(r.media_type === 'video') {
                        item.innerHTML = `
                            <video src="${escapeHtml(r.media_url)}" class="w-full h-full object-cover" muted playsinline preload="metadata" style="pointer-events:none;"></video>
                            <div style="position:absolute;top:4px;right:4px;background:rgba(0,0,0,0.6);border-radius:6px;padding:2px 5px;">
                                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" width="12" height="12" fill="white"><path d="M3 2l10 6-10 6V2z"/></svg>
                            </div>
                            <div style="position:absolute;bottom:4px;left:4px;font-size:10px;color:rgba(255,255,255,0.8);font-weight:bold;">❤ ${(r.likes||[]).length}</div>`;
                    } else {
                        item.innerHTML = `
                            <img src="${escapeHtml(r.media_url)}" class="w-full h-full object-cover" loading="lazy" onerror="this.parentElement.innerHTML='<div style=\\'width:100%;height:100%;display:flex;align-items:center;justify-content:center;font-size:24px;color:#555\\'>📸</div>'">
                            <div style="position:absolute;bottom:4px;left:4px;font-size:10px;color:rgba(255,255,255,0.8);font-weight:bold;">❤ ${(r.likes||[]).length}</div>`;
                    }

                    // Tıklayınca Reels sayfasına ışın — direkt o videodan başlat
                    item.addEventListener('click', () => {
                        document.getElementById('other-profile-modal').classList.add('hidden');
                        window.openReels(r.id);
                    });

                    grid.appendChild(item);
                });

                grid.classList.remove('hidden');
                grid.style.display = 'grid';
            } catch(err) {
                if(loading) { loading.classList.add('hidden'); loading.style.display = 'none'; }
                if(empty) empty.classList.remove('hidden');
                console.error('Profil reels yükleme hatası:', err);
            }
        };

        async function adminSetPremium(target) {
            const tier = document.getElementById("admin-tier-select").value;
            await sendAction('admin_toggle_premium', { username: target, tier: tier });
            alert("Abonelik başarıyla güncellendi!");
            document.getElementById("other-profile-modal").classList.add("hidden");
        }

        async function giveXP(u) { 
            const a = document.getElementById("admin-xp-amount").value; 
            if(!a) return; 
            
            await sendAction('give_xp', { username: u, amount: a }); 
            alert("XP Başarıyla Eklendi!"); 
            document.getElementById("other-profile-modal").classList.add("hidden"); 
        }
        
        async function banUser(u) { 
            if(confirm("Bu kullanıcıyı kalıcı olarak banlamak istediğinize emin misiniz?")) { 
                await sendAction('add_ban', { username: u });
                db.banned.push(u);
            } 
        }

        async function blockUser(target) {
            if(!confirm(`${target} adlı kullanıcıyı engellemek istediğine emin misin? Engellenince seni göremez ve sana mesaj gönderemez.`)) return;
            const res = await sendAction('block_user', { target });
            if(res && res.status === 'ok') {
                if(!currentUser.stats) currentUser.stats = {};
                if(!currentUser.stats.blocked_users) currentUser.stats.blocked_users = [];
                if(!currentUser.stats.blocked_users.includes(target)) currentUser.stats.blocked_users.push(target);
                document.getElementById('other-profile-modal').classList.add('hidden');
                showToast(`🚫 ${target} engellendi.`);
            } else {
                alert(res?.message || 'Bir hata oluştu.');
            }
        }

        async function unblockUser(target) {
            const res = await sendAction('unblock_user', { target });
            if(res && res.status === 'ok') {
                if(currentUser.stats && currentUser.stats.blocked_users) {
                    currentUser.stats.blocked_users = currentUser.stats.blocked_users.filter(u => u !== target);
                }
                document.getElementById('other-profile-modal').classList.add('hidden');
                showToast(`✅ ${target} engeli kaldırıldı.`);
            } else {
                alert(res?.message || 'Bir hata oluştu.');
            }
        }

        function openDeleteAccountModal() {
            document.getElementById('settings-modal').classList.add('hidden');
            document.getElementById('delete-account-password').value = '';
            document.getElementById('delete-account-modal').classList.remove('hidden');
        }

        async function confirmDeleteAccount() {
            const pw = document.getElementById('delete-account-password').value.trim();
            if(!pw) { alert('Lütfen şifreni gir.'); return; }
            if(!confirm('Son onay: Hesabın ve TÜM verilerin kalıcı olarak silinecek. Devam etmek istiyor musun?')) return;
            const res = await sendAction('delete_account', { password: pw });
            if(res && res.status === 'ok') {
                alert('Hesabın başarıyla silindi. Görüşmek üzere! 🏔️');
                window.location.reload();
            } else {
                alert(res?.message || 'Bir hata oluştu.');
            }
        }

        // ---- KULLANICI RAPORLAMA ----
        let _reportUserTarget = '';
        let _reportUserReason = '';
        let _reportMsgId = '';
        let _reportMsgUser = '';
        let _reportMsgText = '';
        let _reportMsgReason = '';

        function openReportUserModal(username) {
            _reportUserTarget = username;
            _reportUserReason = '';
            document.getElementById('report-user-target-label').textContent = username;
            document.getElementById('report-user-detail').value = '';
            document.getElementById('other-profile-modal').classList.add('hidden');
            document.getElementById('report-user-modal').classList.remove('hidden');
        }

        function setReportReason(reason) {
            _reportUserReason = reason;
            document.querySelectorAll('#report-user-modal .grid button').forEach(b => {
                b.classList.toggle('border-orange-500', b.textContent.trim().includes(reason.split('/')[0].trim()));
            });
        }

        async function submitReportUser() {
            const detail = document.getElementById('report-user-detail').value.trim();
            const reason = _reportUserReason ? _reportUserReason + (detail ? ': ' + detail : '') : detail;
            if(!reason) { alert('Lütfen bir şikayet sebebi seçin.'); return; }
            const res = await sendAction('report_user', { target: _reportUserTarget, reason });
            document.getElementById('report-user-modal').classList.add('hidden');
            if(res && res.status === 'ok') {
                showToast('Şikayetiniz admin ekibine iletildi. Teşekkürler!');
            } else {
                alert(res?.message || 'Bir hata oluştu.');
            }
        }

        function openReportMsgModal(encodedId, encodedUser, encodedText) {
            try {
                _reportMsgId = decodeURIComponent(atob(encodedId));
                _reportMsgUser = decodeURIComponent(atob(encodedUser));
                _reportMsgText = decodeURIComponent(atob(encodedText));
            } catch(e) {
                _reportMsgId = encodedId;
                _reportMsgUser = encodedUser;
                _reportMsgText = encodedText;
            }
            _reportMsgReason = '';
            document.getElementById('report-msg-preview').textContent = _reportMsgText || '(Mesaj içeriği)';
            document.getElementById('report-msg-modal').classList.remove('hidden');
        }

        function setMsgReportReason(reason) {
            _reportMsgReason = reason;
            document.querySelectorAll('#report-msg-modal .grid button').forEach(b => {
                b.classList.toggle('border-orange-500', b.textContent.trim().includes(reason.split('/')[0].trim()));
            });
        }

        async function submitReportMsg() {
            if(!_reportMsgReason) { alert('Lütfen bir şikayet sebebi seçin.'); return; }
            document.getElementById('report-msg-modal').classList.add('hidden');
            try {
                // sendAction üzerinden /api/data'ya gönder — session yönetimi güvenilir
                const data = await sendAction('report_message', {
                    msg_id:   String(_reportMsgId),
                    msg_text: String(_reportMsgText),
                    msg_user: String(_reportMsgUser),
                    reason:   String(_reportMsgReason)
                }, true);
                if (data && data.status === 'ok') {
                    // Local state'i güncelle — sayfa yenilenmeden flag badge görünsün
                    const localMsg = db.messages.find(m => m.id === String(_reportMsgId));

                    if (data.message && typeof showToast === 'function') {
                        showToast(data.message);
                    }

                    if (data.should_remove) {
                        // flag_count >= 2 — mesaj otomatik silindi, local'den de kaldır
                        db.messages = db.messages.filter(m => m.id !== String(_reportMsgId));
                        _renderedMsgIds.delete(String(_reportMsgId));
                    } else if (localMsg && data.is_flagged === true) {
                        localMsg.is_flagged = true;
                        localMsg.flag_count = data.flag_count || (localMsg.flag_count || 0) + 1;
                    }
                    renderChat(true); // Tüm mesajları yeniden çiz (flag badge dahil)

                    // AI moderasyon uyarısı varsa sohbete ekle
                    if (data.warning && data.ai_chat_msg) {
                        try {
                            db.messages.push(data.ai_chat_msg);
                            const container = document.getElementById('chat-messages');
                            if (container) {
                                const msgHtml = buildMsgHTML(data.ai_chat_msg);
                                container.insertAdjacentHTML('beforeend', msgHtml);
                                container.scrollTo({ top: container.scrollHeight, behavior: 'smooth' });
                            }
                        } catch(e) { console.warn('[Moderasyon] AI mesaj ekleme hatası:', e); }
                    }

                    if (data.should_remove) {
                        showToast('🚫 Mesaj çok fazla şikayet aldı ve otomatik kaldırıldı.', 'error', 4000);
                    } else if (data.warning) {
                        showToast('⚠️ İçerik uygunsuz bulundu ve admin ekibine iletildi!', 'warning');
                    } else {
                        showToast('✅ Mesaj moderasyon ekibine iletildi. Teşekkürler!', 'success');
                    }
                } else {
                    showToast('❌ Bildirim gönderilemedi: ' + (data?.message || 'Hata'), 'error');
                }
            } catch(err) {
                console.error('[Moderasyon] Hata:', err);
                showToast('❌ Bağlantı hatası. Tekrar deneyin.');
            }
        }

        // Sohbet ekranına Freerider AI moderatör mesajı ekler
        function injectModerationSystemMessage(senderUsername, systemMsg) {
            const container = document.getElementById('chat-messages') || document.getElementById('dm-messages');
            if (!container) return;
            const aiMsg = {
                id: String(Date.now()) + '_mod',
                user: 'Freerider AI',
                text: '🛡️ ' + senderUsername + ', mesajın topluluk kurallarına aykırı bulundu ve admin ekibine bildirildi. Lütfen kurallara uygun davranın. Tekrarlayan ihlaller hesabınızın askıya alınmasına neden olabilir.',
                type: 'text'
            };
            db.messages.push(aiMsg);
            const msgHtml = buildMsgHTML(aiMsg);
            container.insertAdjacentHTML('beforeend', msgHtml);
            container.scrollTo({ top: container.scrollHeight, behavior: 'smooth' });
        }

        function toggleAddMarkerMode() { 
            if(isAddingEventMode) toggleAddEventMode(); 
            isAddingMarkerMode = !isAddingMarkerMode; 
            
            const btn = document.getElementById("btn-add-marker-mode"); 
            const mapContainer = document.getElementById("map"); 
            
            if(isAddingMarkerMode) { 
                btn.className = "bg-green-600 px-3 py-2 rounded-xl shadow-xl font-bold text-white animate-pulse text-[10px] uppercase tracking-widest pointer-events-auto shadow-[0_0_15px_rgba(34,197,94,0.6)]"; 
                btn.innerHTML = "❌ Haritadan Seç"; 
                mapContainer.classList.add("map-add-mode"); 
            } else { 
                btn.className = "bg-sky-600/90 backdrop-blur hover:bg-red-500 btn-premium-hover transition px-3 py-2 rounded-xl shadow-[0_0_15px_rgba(14,165,233,0.4)] font-bold text-white text-[10px] uppercase tracking-widest border border-red-400/50 pointer-events-auto"; 
                btn.innerHTML = "📍 RAMPA EKLE"; 
                mapContainer.classList.remove("map-add-mode"); 
            } 
        }
        
        function toggleAddEventMode() { 
            if(isAddingMarkerMode) toggleAddMarkerMode();
            isAddingEventMode = !isAddingEventMode; 
            
            const btn = document.getElementById("btn-add-event-mode"); 
            const mapContainer = document.getElementById("map"); 
            
            if(isAddingEventMode) { 
                btn.className = "bg-green-600 px-3 py-2 rounded-xl shadow-xl font-bold text-white animate-pulse text-[10px] uppercase tracking-widest pointer-events-auto shadow-[0_0_15px_rgba(34,197,94,0.6)]"; 
                btn.innerHTML = "❌ Haritadan Seç"; 
                mapContainer.classList.add("map-add-mode"); 
            } else { 
                btn.className = "bg-blue-600/90 backdrop-blur hover:bg-blue-500 btn-premium-hover transition px-3 py-2 rounded-xl shadow-[0_0_15px_rgba(59,130,246,0.4)] flex items-center justify-center text-[10px] uppercase tracking-widest font-bold text-white border border-blue-400/50 pointer-events-auto"; 
                btn.innerHTML = "📅 BULUŞMA EKLE"; 
                mapContainer.classList.remove("map-add-mode"); 
            } 
        }

        function useCurrentLocationForMarker() {
            if(!userLat || !userLng) {
                return alert("Konumunuz bulunamadı! Lütfen haritadaki GPS (🎯) butonuna tıklayıp konum izni verin.");
            }
            tempLat = userLat;
            tempLng = userLng;
            editingMarkerId = null;
            document.getElementById("modal-marker-title").textContent = "📍 " + selectedMarkerCategory.toUpperCase() + " EKLE (Şu Anki Konum)";
            showToast("Şu anki konumunuz başarıyla alındı! Detayları girip kaydedebilirsiniz.");
        }

        function quickAddMarkerCurrentLocation() {
            if(!userLat || !userLng) {
                return alert("Konumunuz bulunamadı! Lütfen haritadaki GPS (🎯) butonuna tıklayıp konum izni verin.");
            }
            tempLat = userLat;
            tempLng = userLng;
            editingMarkerId = null;
            
            document.getElementById("new-marker-name").value = "";
            document.getElementById("new-marker-desc").value = "";
            document.getElementById("new-marker-extranote").value = "";
            document.getElementById("new-marker-difficulty").value = "Orta";
            document.getElementById("new-marker-photo").value = "";
            
            openCategorySelectModal();
        }
        
        function editMarker(id) {
            const m = db.markers.find(x => x.id === id);
            if(!m) return;
            
            editingMarkerId = m.id;
            editingMarkerLat = m.lat;
            editingMarkerLng = m.lng;
            
            document.getElementById("modal-marker-title").textContent = "✏️ RAMPA DÜZENLE";
            document.getElementById("new-marker-name").value = m.name || "";
            document.getElementById("new-marker-desc").value = m.desc || "";
            document.getElementById("new-marker-difficulty").value = m.difficulty || "Orta";
            document.getElementById("new-marker-photo").value = ""; 
            
            if(getUserPremiumTier(currentUser.username) >= 2 || currentUser.role === 'Admin') {
                document.getElementById("new-marker-icon").classList.remove("hidden");
                document.getElementById("new-marker-icon").value = m.icon_type || "🚴";
            }
            
            closeMarkerSheet();
            document.getElementById("add-marker-modal").classList.remove("hidden");
        }
        
        async function deleteMarker(id) {
            if(confirm("Bu noktayı haritadan kalıcı olarak silmek istediğine emin misin?")) {
                closeMarkerSheet();
                await sendAction('delete_marker', {id: id});
                db.markers = db.markers.filter(m => m.id !== id);
                if(map) syncMap();
            }
        }

        function showMarkerSheet(m, updateOnly = false) {
            currentMarkerId = m.id;
            const sheet = document.getElementById("marker-sheet");
            
            if(!updateOnly) sheet.classList.remove("hidden");
            
            document.getElementById("ms-title").textContent = m.title || m.name;
            document.getElementById("ms-category").textContent = m.category || m.icon_type || "Rampa";
            document.getElementById("ms-difficulty").textContent = m.difficulty || "Orta";
            document.getElementById("ms-desc").textContent = m.desc || "Açıklama yok.";
            
            if (m.extra_note && m.extra_note.trim() !== "") {
                document.getElementById("ms-extranote-container").classList.remove("hidden");
                document.getElementById("ms-extranote").textContent = m.extra_note;
            } else {
                document.getElementById("ms-extranote-container").classList.add("hidden");
            }
            
            const imgContainer = document.getElementById("ms-image-container");
            if(m.image) {
                imgContainer.innerHTML = `<img src="${m.image}" onclick="openFullscreen(['${m.image}'],0)" class="w-full h-48 object-cover rounded-xl border border-zinc-800 shadow-md cursor-pointer hover:opacity-90 transition-opacity">`;
            } else {
                imgContainer.innerHTML = "";
            }
            
            let likesCount = m.likes ? m.likes.length : 0; 
            let dislikesCount = m.dislikes ? m.dislikes.length : 0;
            let isLiked = m.likes && m.likes.includes(currentUser.username);
            let isDisliked = m.dislikes && m.dislikes.includes(currentUser.username);
            
            document.getElementById("ms-likes-count").textContent = likesCount;
            document.getElementById("ms-dislikes-count").textContent = dislikesCount;
            
            const likeBtn = document.getElementById("ms-btn-like");
            const dislikeBtn = document.getElementById("ms-btn-dislike");
            
            if(isLiked) likeBtn.classList.add("bg-red-950/40", "border-sky-900/50"); else likeBtn.classList.remove("bg-red-950/40", "border-sky-900/50");
            if(isDisliked) dislikeBtn.classList.add("bg-zinc-800"); else dislikeBtn.classList.remove("bg-zinc-800");

            document.getElementById("ms-btn-directions").href = `https://maps.google.com/?q=${m.lat},${m.lng}`;
            updateMarkerRating(m);
            const dangerBanner = document.getElementById('ms-danger-banner');
            if(dangerBanner) {
                const dr = m.danger_reports || [];
                if(m.is_dangerous && dr.length > 0) { dangerBanner.classList.remove('hidden'); dangerBanner.innerHTML = '⚠️ ' + dr[dr.length-1].reason; }
                else { dangerBanner.classList.add('hidden'); }
            }

            const adminControls = document.getElementById("ms-admin-controls");
            if (currentUser && (currentUser.role === 'Admin' || currentUser.role === 'SubAdmin' || m.addedBy === currentUser.username)) {
                adminControls.classList.remove("hidden");
                document.getElementById("ms-btn-edit").onclick = () => editMarker(m.id);
                document.getElementById("ms-btn-delete").onclick = () => deleteMarker(m.id);
            } else {
                adminControls.classList.add("hidden");
            }
        }
        
        function closeMarkerSheet() {
            document.getElementById("marker-sheet").classList.add("hidden");
            currentMarkerId = null;
        }

        async function toggleMarkerInteraction(type) {
            if(!currentMarkerId) return;
            const m = db.markers.find(x => x.id === currentMarkerId);
            if(m) {
                if(!m.likes) m.likes = [];
                if(!m.dislikes) m.dislikes = [];
                
                if(type === 'like') {
                    if(m.likes.includes(currentUser.username)) m.likes = m.likes.filter(u => u !== currentUser.username);
                    else { m.likes.push(currentUser.username); m.dislikes = m.dislikes.filter(u => u !== currentUser.username); }
                } else {
                    if(m.dislikes.includes(currentUser.username)) m.dislikes = m.dislikes.filter(u => u !== currentUser.username);
                    else { m.dislikes.push(currentUser.username); m.likes = m.likes.filter(u => u !== currentUser.username); }
                }
                showMarkerSheet(m, true);
            }
            
            if(type === 'like') await sendAction('like_marker', {id: currentMarkerId});
            else await sendAction('dislike_marker', {id: currentMarkerId});
        }

        function openAddEventModal() { 
            if(!tempLat) { 
                alert("Lütfen önce harita üzerinden bir noktaya dokunarak yer seçin!"); 
                toggleAddEventMode(); 
                return; 
            } 
            document.getElementById("add-event-modal").classList.remove("hidden"); 
        }

        function syncMap() {
            markerLayers.forEach(l => map.removeLayer(l)); 
            markerLayers = [];
            
            const catIcons = {
                'Rampa': '<i data-lucide="mountain-snow" class="w-4 h-4"></i>',
                'Bisikletçi': '<i data-lucide="wrench" class="w-4 h-4"></i>',
                'Market': '<i data-lucide="shopping-cart" class="w-4 h-4"></i>',
                'Trail': '<i data-lucide="map" class="w-4 h-4"></i>',
                'Drop': '<i data-lucide="arrow-down-to-line" class="w-4 h-4"></i>',
                'Dirt Jump': '<i data-lucide="zap" class="w-4 h-4"></i>',
                'Tamir Noktası': '<i data-lucide="hammer" class="w-4 h-4"></i>',
                'Su Kaynağı': '<i data-lucide="droplet" class="w-4 h-4"></i>',
                'Toplanma Noktası': '<i data-lucide="map-pin" class="w-4 h-4"></i>',
                'Tehlikeli Bölge': '<i data-lucide="triangle-alert" class="w-4 h-4"></i>'
            };
            
            const catColors = {
                'Rampa': 'from-sky-500 to-sky-800 shadow-sky-500',
                'Bisikletçi': 'from-orange-500 to-orange-800 shadow-orange-500',
                'Market': 'from-green-500 to-green-800 shadow-green-500',
                'Trail': 'from-emerald-500 to-emerald-800 shadow-emerald-500',
                'Drop': 'from-purple-500 to-purple-800 shadow-purple-500',
                'Dirt Jump': 'from-yellow-500 to-yellow-800 shadow-yellow-500',
                'Tamir Noktası': 'from-blue-500 to-blue-800 shadow-blue-500',
                'Su Kaynağı': 'from-cyan-500 to-cyan-800 shadow-cyan-500',
                'Toplanma Noktası': 'from-pink-500 to-pink-800 shadow-pink-500',
                'Tehlikeli Bölge': 'from-red-500 to-red-800 shadow-red-500'
            };

            const markersToAdd = [];
            
            db.markers.forEach(m => {
                const cat = m.category || m.icon_type || 'Rampa';
                if(activeMarkerFilter !== 'Tümü' && activeMarkerFilter !== cat) return;
                
                const svgIcon = catIcons[cat] || catIcons['Rampa'];
                const colorClass = catColors[cat] || catColors['Rampa'];
                
                const iconHtml = `
                    <div class="relative flex items-center justify-center w-10 h-10 cursor-pointer transition hover:scale-110">
                        <div class="absolute w-full h-full bg-white rounded-full animate-ping opacity-20"></div>
                        <div class="relative bg-gradient-to-b ${colorClass} border-2 border-white text-white w-8 h-8 rounded-full flex items-center justify-center shadow-[0_0_15px_currentColor] text-lg">${svgIcon}</div>
                    </div>`;
                
                const icon = L.divIcon({ html: iconHtml, className: '', iconSize: [40,40], iconAnchor: [20,20] });
                const mk = L.marker([m.lat, m.lng], {icon: icon});
                
                mk.on('click', () => { showMarkerSheet(m); });
                mk.addTo(map);
                markerLayers.push(mk);
            });
            
            setTimeout(() => { if(typeof lucide !== 'undefined') lucide.createIcons(); }, 100);
            
            db.events.forEach(e => {
                const icon = L.divIcon({ 
                    html: `<div class="bg-gradient-to-b from-blue-500 to-blue-700 text-white w-10 h-10 rounded-full flex items-center justify-center border-2 border-white shadow-[0_0_15px_rgba(59,130,246,0.6)] font-bold text-lg cursor-pointer transition hover:scale-110">📅</div>`, 
                    className: '', 
                    iconSize: [40,40],
                    iconAnchor: [20,20]
                });
                const mk = L.marker([e.lat, e.lng], {icon: icon}).addTo(map); 
                mk.on('click', () => showEventSheet(e)); 
                markerLayers.push(mk);
            });
            
            const now = Date.now();
            db.users.forEach(u => {
                if(u.stats && u.stats.riding_until > now && u.stats.riding_lat && u.stats.riding_lng) {
                    const isMe = u.username === currentUser.username;
                    const avatar = u.avatar || `https://cdn.freeridertr.com.tr/profil%20resmi/unnamed.jpg`;
                    const premTier = getUserPremiumTier(u.username);
                    
                    let ringColor = 'bg-green-500'; 
                    let borderColor = isMe ? 'border-green-400' : 'border-zinc-300'; 
                    let shadowColor = 'rgba(34,197,94,0.8)'; 
                    let crownHtml = '';
                    
                    if(premTier === 3) { 
                        ringColor = 'bg-yellow-500'; 
                        borderColor = 'border-yellow-400'; 
                        shadowColor = 'rgba(234,179,8,0.8)'; 
                        crownHtml = `<div class="absolute -top-3 text-sm drop-shadow-[0_0_10px_rgba(234,179,8,0.8)] z-20 animate-bounce">👑</div>`; 
                    }
                    
                    const iconHtml = `
                        <div class="relative flex items-center justify-center w-12 h-12 flex-col cursor-pointer transition hover:scale-110">
                            ${crownHtml}
                            <div class="absolute w-full h-full ${ringColor} rounded-full animate-ping opacity-70 mt-1"></div>
                            <img src="${avatar}" class="relative w-10 h-10 rounded-full border-2 ${borderColor} object-cover shadow-[0_0_15px_${shadowColor}] mt-1">
                        </div>
                    `;
                    
                    const icon = L.divIcon({ html: iconHtml, className: '', iconSize: [48,48], iconAnchor: [24,24] });
                    const mk = L.marker([u.stats.riding_lat, u.stats.riding_lng], {icon: icon}).addTo(map);
                    mk.on('click', () => showOtherProfile(u.username));
                    markerLayers.push(mk);
                }
            });
        }
        
        function autoZoomToUserLocation() { 
            if(navigator.geolocation) { 
                navigator.geolocation.getCurrentPosition(pos => { 
                    userLat = pos.coords.latitude; 
                    userLng = pos.coords.longitude; 
                    if(map) map.setView([userLat, userLng], 14); 
                }); 
            } 
        }
        
        function showNearbyRoutes() { 
            if(!userLat || !userLng) return alert("Mevcut konumunuz henüz bulunamadı! Lütfen haritadaki GPS (🎯) butonuna tıklayıp konum izni verin.");
            
            const c = document.getElementById("nr-list");
            c.innerHTML = "";
            
            let withDist = db.markers.map(m => {
                let dLat = m.lat - userLat;
                let dLng = m.lng - userLng;
                let dist = Math.sqrt(dLat*dLat + dLng*dLng) * 111;
                return {...m, distance: dist};
            }).sort((a,b) => a.distance - b.distance);
            
            if(withDist.length === 0) {
                c.innerHTML = "<p class='text-zinc-500 text-xs italic text-center mt-5 font-medium'>Çevrenizde kayıtlı rampa veya rota bulunamadı.</p>";
            } else {
                withDist.slice(0, 10).forEach(m => {
                    let img = m.image ? `<img src="${m.image}" class="w-16 h-16 rounded-xl object-cover shrink-0 border border-zinc-700 shadow-sm">` : `<div class="w-16 h-16 rounded-xl bg-black/60 border border-zinc-700 shadow-inner flex items-center justify-center text-2xl shrink-0">${m.icon_type || '🚴'}</div>`;
                    c.innerHTML += `
                    <div class="bg-black/50 p-3 rounded-2xl border border-zinc-800 flex items-center gap-3 mb-3 cursor-pointer hover:bg-zinc-800 hover:border-zinc-600 transition-colors shadow-md group" onclick="map.setView([${m.lat}, ${m.lng}], 16); document.getElementById('nearby-routes-modal').classList.add('hidden');">
                        ${img}
                        <div class="overflow-hidden flex-1">
                            <div class="text-white font-bold text-sm tracking-wide truncate group-hover:text-blue-300 transition-colors">${m.name}</div>
                            <div class="text-sky-400 text-[10px] font-black uppercase tracking-widest mt-1">${m.distance.toFixed(1)} KM UZAKLIKTA</div>
                            <div class="text-zinc-500 text-[10px] font-bold uppercase tracking-widest mt-0.5">Seviye: ${m.difficulty}</div>
                        </div>
                        <div class="text-zinc-400 bg-zinc-900 border border-zinc-700 w-8 h-8 rounded-full flex items-center justify-center shrink-0 group-hover:bg-zinc-700 group-hover:text-white transition-colors">➜</div>
                    </div>`;
                });
            }
            
            document.getElementById("nearby-routes-modal").classList.remove("hidden"); 
        }
        
        async function saveNewMarker() { 
            const n = document.getElementById("new-marker-name").value;
            const d = document.getElementById("new-marker-desc").value; 
            const diff = document.getElementById("new-marker-difficulty").value; 
            const eNote = document.getElementById("new-marker-extranote").value;
            const photoFile = document.getElementById("new-marker-photo").files[0]; 
            
            if(!n) {
                showToast("📍 Başlık zorunludur!");
                return;
            }
            
            closeMarkerModal(); 
            
            let base64Photo = null; 
            if(photoFile) {
                base64Photo = await resizeImage(photoFile, 500); 
            }
            
            let targetId = editingMarkerId ? editingMarkerId : Date.now().toString();
            let targetLat = editingMarkerId ? editingMarkerLat : tempLat;
            let targetLng = editingMarkerId ? editingMarkerLng : tempLng;
            
            let finalImage = base64Photo;
            if(editingMarkerId && !base64Photo) {
                const existingMarker = db.markers.find(m => m.id === editingMarkerId);
                if(existingMarker) finalImage = existingMarker.image;
            }
            
            try { 
                const res = await sendAction('add_marker', { 
                    id: targetId, 
                    lat: targetLat, 
                    lng: targetLng, 
                    title: n, 
                    difficulty: diff, 
                    desc: d, 
                    extra_note: eNote,
                    category: selectedMarkerCategory,
                    image: finalImage 
                }); 
                
                if (res && res.success) {
                    showToast("✅ " + (editingMarkerId ? "Nokta güncellendi!" : "Nokta eklendi!"));
                    markerCache.clear();
                    loadMarkersByViewport();
                } else {
                    showToast(res?.message || "❌ Hata oluştu");
                }
                
                editingMarkerId = null;
                tempLat = null;
                tempLng = null;
                document.getElementById("new-marker-name").value = "";
                document.getElementById("new-marker-desc").value = "";
                document.getElementById("new-marker-extranote").value = "";
                document.getElementById("new-marker-photo").value = "";
                document.getElementById("modal-marker-title").textContent = "📍 NOKTA EKLE";
                document.getElementById("modal-marker-category-label").textContent = "";
            } catch(e) {
                console.error(e);
                showToast("❌ Ağ hatası.");
            }
        }

        
        async function saveEvent() { 
            const t = document.getElementById("ev-title").value; 
            const d = document.getElementById("ev-date").value; 
            const tm = document.getElementById("ev-time").value; 
            
            if(!t || !d || !tm) return alert("Tüm alanları doldurunuz!");
            
            await sendAction('add_event', { 
                id: Date.now(), 
                lat: tempLat, 
                lng: tempLng, 
                title: t, 
                datetime: `${d} ${tm}`, 
                max: document.getElementById("ev-max").value, 
                desc: document.getElementById("ev-desc").value 
            }); 
            
            document.getElementById("add-event-modal").classList.add("hidden");
        }
        
        function showEventSheet(e) { 
            currentEventId = e.id; 
            document.getElementById("event-sheet").classList.remove("hidden"); 
            document.getElementById("es-title").textContent = e.title; 
            document.getElementById("es-time").textContent = e.datetime; 
            document.getElementById("es-desc").textContent = e.desc || "Açıklama yok."; 
            
            const att = e.attendees || []; 
            
            const attContainer = document.getElementById("es-attendees");
            attContainer.innerHTML = "";
            if (att.length === 0) {
                attContainer.innerHTML = "<span class='text-zinc-500 text-xs italic font-medium'>Henüz katılan yok. İlk sen ol!</span>";
            } else {
                att.forEach(u => {
                    let isMe = u === currentUser.username;
                    attContainer.innerHTML += `<span class="bg-black/60 text-[10px] px-3 py-1.5 rounded-xl border ${isMe ? 'border-green-500 text-green-400 font-bold shadow-[0_0_10px_rgba(34,197,94,0.3)]' : 'border-zinc-700 text-zinc-300'} shadow-inner tracking-widest uppercase">${u}</span>`;
                });
            }

            const btn = document.getElementById("btn-join"); 
            btn.disabled = false;
            
            let maxCapacity = e.max ? parseInt(e.max) : 0;

            if(att.includes(currentUser.username)) {
                btn.textContent = "AYRIL"; 
                btn.className = "w-full bg-red-950/80 hover:bg-sky-900/80 btn-premium-hover transition text-sky-400 border border-sky-900/50 py-4 rounded-xl font-bold text-sm shadow-md mb-2";
            } else {
                if (maxCapacity > 0 && att.length >= maxCapacity) {
                    btn.textContent = `KAPASİTE DOLU (${att.length}/${maxCapacity})`;
                    btn.className = "w-full bg-black/50 text-zinc-500 py-4 rounded-xl font-bold text-sm cursor-not-allowed mb-2 border border-zinc-700 shadow-inner";
                    btn.disabled = true;
                } else {
                    let limitText = maxCapacity > 0 ? `KATIL (${att.length}/${maxCapacity} Kişi)` : `KATIL (${att.length} Kişi)`;
                    btn.textContent = limitText;
                    btn.className = "w-full bg-green-700 hover:bg-green-600 transition text-white py-4 rounded-xl font-bold text-sm shadow-[0_0_15px_rgba(34,197,94,0.5)] mb-2 btn-premium-hover";
                }
            }
            
            document.getElementById("btn-directions").href = `https://maps.google.com/?q=${e.lat},${e.lng}`;

            if(e.creator === currentUser.username || currentUser.role === 'Admin') {
                document.getElementById("btn-del-event").classList.remove("hidden");
            } else {
                document.getElementById("btn-del-event").classList.add("hidden");
            }
        }
        
        async function toggleJoinEvent() { 
            const ev = db.events.find(x => x.id == currentEventId); 
            if(!ev) return; 
            
            const att = ev.attendees || []; 
            document.getElementById("btn-join").disabled = true;

            if(att.includes(currentUser.username)) {
                await sendAction('leave_event', {id: ev.id}); 
            } else {
                let maxCapacity = ev.max ? parseInt(ev.max) : 0;
                if (maxCapacity > 0 && att.length >= maxCapacity) {
                    alert("Bu etkinliğin kapasitesi maalesef dolmuş!");
                    document.getElementById("btn-join").disabled = false;
                    return;
                }
                
                try {
                    await sendAction('join_event', {id: ev.id}); 
                } catch(e) {}
            }
            
            document.getElementById("event-sheet").classList.add("hidden");
        }

        async function deleteEvent() {
            if(confirm("Bu etkinliği silmek istediğinize emin misiniz?")) {
                await sendAction('delete_event', {id: currentEventId});
                db.events = db.events.filter(e => e.id !== currentEventId);
                document.getElementById("event-sheet").classList.add("hidden");
            }
        }

        // Bildirim badge fonksiyonları
        let chatBadgeCount = 0;
        function showChatBadge() {
            chatBadgeCount++;
            // Sidebar tab butonu
            const btn = document.getElementById('tab-btn-1');
            if(btn) {
                let badge = btn.querySelector('.notif-badge');
                if(!badge) {
                    badge = document.createElement('span');
                    badge.className = 'notif-badge absolute -top-1 -right-1 bg-red-600 text-white text-[9px] font-black rounded-full w-5 h-5 flex items-center justify-center shadow-[0_0_10px_rgba(14,165,233,0.8)] border border-sky-400';
                    btn.style.position = 'relative';
                    btn.appendChild(badge);
                }
                badge.textContent = chatBadgeCount > 9 ? '9+' : chatBadgeCount;
                badge.style.animation = 'none';
                badge.offsetHeight;
                badge.style.animation = 'notifBounce 0.4s ease';
            }
            // Alt nav chat butonu
            const bnavBtn = document.getElementById('bnav-1');
            if(bnavBtn) {
                let badge2 = bnavBtn.querySelector('.notif-badge');
                if(!badge2) {
                    badge2 = document.createElement('span');
                    badge2.className = 'notif-badge absolute -top-0.5 -right-0.5 bg-red-600 text-white text-[9px] font-black rounded-full w-4 h-4 flex items-center justify-center shadow-[0_0_8px_rgba(14,165,233,0.8)] border border-sky-400';
                    bnavBtn.style.position = 'relative';
                    bnavBtn.appendChild(badge2);
                }
                badge2.textContent = chatBadgeCount > 9 ? '9+' : chatBadgeCount;
                badge2.style.animation = 'none';
                badge2.offsetHeight;
                badge2.style.animation = 'notifBounce 0.4s ease';
            }
        }
        function clearChatBadge() {
            chatBadgeCount = 0;
            ['tab-btn-1', 'bnav-1'].forEach(id => {
                const btn = document.getElementById(id);
                if(!btn) return;
                const badge = btn.querySelector('.notif-badge');
                if(badge) badge.remove();
            });
        }

        function switchChatTab(type) {
            if(type === 'group') { 
                document.getElementById("chat-group-area").classList.remove("hidden"); 
                document.getElementById("chat-dm-list-area").classList.add("hidden"); 
                document.getElementById("chat-dm-thread-area").classList.add("hidden"); 
                
                document.getElementById("chat-tab-group").className = "flex-1 py-2 bg-zinc-800 text-white rounded font-bold text-xs transition shadow-sm"; 
                document.getElementById("chat-tab-dm").className = "flex-1 py-2 bg-transparent text-zinc-500 hover:text-white rounded font-bold text-xs transition"; 
                
                renderChat(true); 
            } else { 
                document.getElementById("chat-group-area").classList.add("hidden"); 
                document.getElementById("chat-dm-list-area").classList.remove("hidden"); 
                document.getElementById("chat-dm-thread-area").classList.add("hidden"); 
                
                document.getElementById("chat-tab-dm").className = "flex-1 py-2 bg-zinc-800 text-white rounded font-bold text-xs transition shadow-sm"; 
                document.getElementById("chat-tab-group").className = "flex-1 py-2 bg-transparent text-zinc-500 hover:text-white rounded font-bold text-xs transition"; 
                
                renderDmList(); 
            }
        }

        let _renderedMsgIds = new Set();

        function buildMsgHTML(msg) {

                const isMe = msg.user === currentUser.username; 
                const isAI = msg.user === 'Freerider AI' || msg.user === 'Moderatör AI';
                
                const premColor = getUserPremiumColor(msg.user); 
                const premTier = getUserPremiumTier(msg.user); 
                
                const textCls = (premTier > 0) ? getPremiumTextClass(premColor) : '';
                const inlineStyle = (premTier > 0) ? getPremiumInlineStyle(premColor) : '';
                const borderCls = (premTier > 0 && !isAI) ? getPremiumBorderClass(msg.user) : 'border-zinc-700';
                
                const isAdmin = msg.user === 'Admin' || (db.users.find(u => u.username === msg.user) && db.users.find(u => u.username === msg.user).role === 'Admin');
                const adminDel = (currentUser.role === 'Admin' || currentUser.role === 'SubAdmin' || isMe) ? `<button onclick="delMsg('${msg.id}')" class="text-[10px] bg-red-950/80 text-sky-300 px-2 py-1 rounded-lg ml-2 hover:bg-red-900 transition border border-sky-900/50 uppercase font-bold tracking-widest relative z-50 pointer-events-auto">SİL</button>` : '';
                const _encId = btoa(encodeURIComponent(msg.id)); const _encUser = btoa(encodeURIComponent(msg.user)); const _encText = btoa(encodeURIComponent((msg.text||'').substring(0,80)));
                const reportBtn = (!isMe && !isAI) ? `<button onclick="openReportMsgModal('${_encId}','${_encUser}','${_encText}')" class="text-[10px] bg-orange-950/60 text-orange-400 px-2 py-1 rounded-lg ml-1 hover:bg-orange-900/60 transition border border-orange-900/50 uppercase font-bold tracking-widest relative z-50 pointer-events-auto">🚨</button>` : '';
                
                const pinBtn = (isMe && getUserPremiumTier(currentUser.username) === 3 && msg.type === "text") ? `<button onclick="pinMsg('${msg.id}')" class="text-[10px] bg-yellow-900/50 text-yellow-500 px-2 py-1 rounded-lg ml-2 hover:bg-yellow-900 transition border border-yellow-700/50 uppercase font-bold tracking-widest relative z-50 pointer-events-auto">SABİTLE</button>` : '';

                // Flag göstergesi (DB'den gelen is_flagged + flag_count)
                const flagBadge = msg.is_flagged ? `<span class="text-[9px] bg-red-950/60 text-red-400 px-2 py-0.5 rounded-lg ml-1 border border-red-900/50 uppercase font-bold tracking-widest animate-pulse">🚩 ${msg.flag_count || 1}x</span>` : '';

                let tick = (premTier === 3) ? verifiedTick : ''; 
                let adminTag = isAdmin ? `<span class="ml-2 bg-red-600 text-white px-2 py-0.5 rounded text-[9px] tracking-widest uppercase shadow-[0_0_10px_red]">👑 Yönetici</span>` : '';
                let aiTag = isAI ? `<span class="ml-2 bg-cyan-500/20 border border-cyan-500/50 text-cyan-400 px-2 py-0.5 rounded-lg text-[9px] font-black tracking-widest uppercase shadow-[0_0_15px_rgba(6,182,212,0.4)] animate-pulse">🤖 YAPAY ZEKA</span>` : '';
                
                let msgDate = new Date(parseInt(msg.id));
                let timeStr = !isNaN(msgDate.getTime()) ? msgDate.getHours().toString().padStart(2, '0') + ":" + msgDate.getMinutes().toString().padStart(2, '0') : "";
                let timeHtml = `<span class="text-[9px] text-zinc-500 ml-2 font-bold tracking-widest bg-black/50 border border-zinc-800 px-1.5 py-0.5 rounded">${timeStr}</span>`;

                let avatarUrl = isAI ? 'https://cdn-icons-png.flaticon.com/512/4712/4712035.png' : (db.users.find(u => u.username === msg.user)?.avatar || 'https://cdn.freeridertr.com.tr/profil%20resmi/unnamed.jpg');
                let avatarHtml = `<img src="${avatarUrl}" class="w-8 h-8 rounded-full object-cover border shrink-0 ${isMe ? 'ml-2' : 'mr-2'} cursor-pointer hover:scale-110 transition-transform ${borderCls}" onclick="${isAI ? '' : `showOtherProfile('${msg.user}')`}">`;

                let content = ""; 
                let bubbleClass = isMe ? 'bg-white text-black' : 'bg-black/60 border border-zinc-800 text-zinc-300';
                
                if (isAI) {
                    // AI moderatör uyarı mesajları — özel kırmızı gradient stil
                    const isModMsg = (msg.id && msg.id.endsWith('_mod')) || msg.user === 'Moderatör AI';
                    if (isModMsg) {
                        content = `<div class="ai-moderator-msg px-4 py-3 rounded-2xl text-sm break-words mt-1 font-bold leading-relaxed relative overflow-hidden"><span class="relative z-10">🛡️ ${escapeHtml(msg.text)}</span></div>`;
                    } else {
                        content = `<div class="bg-black/80 border border-cyan-500/50 text-cyan-100 px-4 py-3 rounded-2xl text-sm break-words mt-1 shadow-[0_0_20px_rgba(6,182,212,0.2)] font-medium leading-relaxed relative overflow-hidden"><div class="absolute inset-0 bg-cyan-500/10 animate-pulse"></div><span class="relative z-10">${escapeHtml(msg.text)}</span></div>`;
                    }
                } else if (premTier >= 2) {
                    bubbleClass = isMe ? 'bg-gradient-to-r from-blue-600 to-purple-600 text-white shadow-[0_0_15px_rgba(168,85,247,0.5)]' : 'bg-gradient-to-r from-zinc-900 to-purple-950/40 border border-purple-500/50 text-white shadow-[0_0_15px_rgba(168,85,247,0.2)]';
                }
                
                if(!isAI) {
                    if (msg.type === "photo") {
                        content = `<img src="${msg.photo}" class="w-48 rounded-xl border border-zinc-700 shadow-lg mt-1 cursor-pointer hover:opacity-90 transition">`;
                    } else if (msg.type === "voice") {
                        content = `<div onclick="playVoice('${msg.audio}')" class="${bubbleClass} px-5 py-3 rounded-xl flex items-center gap-3 cursor-pointer mt-1 shadow-md hover:scale-105 transition"><span class="text-xl">🎙️</span><span class="font-bold text-xs uppercase tracking-widest">Ses Kaydı</span></div>`;
                    } else {
                        content = `<div class="${bubbleClass} px-4 py-2.5 rounded-2xl text-sm break-words mt-1 shadow-md font-medium leading-relaxed">${escapeHtml(msg.text)}</div>`;
                    }
                }
                
                let userDisplay = isAI ? `<span class="${msg.user === 'Moderatör AI' ? 'text-red-400' : 'text-cyan-400'} font-black tracking-widest drop-shadow-sm">${msg.user === 'Moderatör AI' ? '🛡️ Moderatör AI' : 'SİSTEM AI'}</span>` : `<span onclick="showOtherProfile('${msg.user}')" style="${inlineStyle}" class="cursor-pointer hover:text-white transition ${textCls ? textCls : 'text-zinc-400'}">${msg.user}</span>`;
                
                // Build reaction bar
                const reactions = msg.reactions || {};
                let reactBar = '<div class="flex flex-wrap gap-1 mt-1">';
                const emojiList = ['👍','🔥','😂','😮','❤️','💪'];
                emojiList.forEach(em => {
                    const users = reactions[em] || [];
                    const iReacted = users.includes(currentUser.username);
                    if(users.length > 0 || true) {
                        reactBar += `<button onclick="addReaction('${msg.id}','${em}')" class="flex items-center gap-0.5 text-xs px-2 py-0.5 rounded-full border transition-all ${iReacted ? 'bg-red-900/40 border-sky-600/60 text-white' : 'bg-black/30 border-zinc-700/50 text-zinc-500 hover:border-zinc-500'}">${em}${users.length > 0 ? `<span class="text-[10px] font-bold">${users.length}</span>` : ''}</button>`;
                    }
                });
                reactBar += '</div>';

                // İhlal durumuna göre mesaj görünümü
                const flagCount = msg.flag_count || 0;
                const isFlagged = msg.is_flagged && flagCount >= 1 && flagCount < 2;
                const isCollapsed = msg.is_flagged && flagCount >= 2;

                if (isCollapsed) {
                    // flag_count >= 2: tamamen collapse — tıklayınca açılabilir
                    return `
                    <div class="flex ${isMe ? "justify-end" : "justify-start"} items-start mb-4 w-full ${isMe ? 'slide-in-right' : 'slide-in-left'}">
                        ${!isMe ? avatarHtml : ''}
                        <div class="max-w-[80%] flex flex-col ${isMe ? 'items-end' : 'items-start'}">
                            <div class="flex items-center gap-1 text-[10px] uppercase font-bold tracking-widest mb-1">
                                ${userDisplay} ${tick} ${adminTag} ${flagBadge} ${timeHtml} ${adminDel}
                            </div>
                            <div class="msg-collapsed-wrap" onclick="this.querySelector('.msg-collapsed-content').classList.toggle('show')">
                                <div class="msg-collapsed-bar">🚫 Bu mesaj uygunsuz içerik içerdiği için gizlendi <span style='font-size:9px;opacity:0.6'>— görmek için tıkla</span></div>
                                <div class="msg-collapsed-content">${content}</div>
                            </div>
                        </div>
                        ${isMe ? avatarHtml : ''}
                    </div>`;
                }

                if (isFlagged) {
                    // flag_count 1: blur + overlay
                    return `
                    <div class="flex ${isMe ? "justify-end" : "justify-start"} items-start mb-4 w-full ${isMe ? 'slide-in-right' : 'slide-in-left'}" style="position:relative">
                        ${!isMe ? avatarHtml : ''}
                        <div class="max-w-[80%] flex flex-col ${isMe ? 'items-end' : 'items-start'}" style="position:relative">
                            <div class="flex items-center gap-1 text-[10px] uppercase font-bold tracking-widest mb-1">
                                ${userDisplay} ${tick} ${adminTag} ${flagBadge} ${timeHtml} ${adminDel} ${reportBtn}
                            </div>
                            <div class="flex flex-col gap-1 w-full">
                                <div class="msg-flagged-overlay"><span>🛡️ Bu mesaj uygunsuz içerik içerdiği için gizlendi</span></div>
                                <div class="msg-flagged">${content}</div>
                            </div>
                        </div>
                        ${isMe ? avatarHtml : ''}
                    </div>`;
                }

                return `
                <div class="flex ${isMe ? "justify-end" : "justify-start"} items-start mb-4 w-full ${isMe ? 'slide-in-right' : 'slide-in-left'}">
                    ${!isMe ? avatarHtml : ''}
                    <div class="max-w-[80%] flex flex-col ${isMe ? 'items-end' : 'items-start'}">
                        <div class="flex items-center gap-1 text-[10px] uppercase font-bold tracking-widest mb-1">
                            ${userDisplay}
                            ${tick} ${adminTag} ${aiTag} ${flagBadge} ${timeHtml} ${pinBtn} ${adminDel} ${reportBtn}
                        </div>
                        ${content}
                        ${reactBar}
                    </div>
                    ${isMe ? avatarHtml : ''}
                </div>`;
        }

        function renderChat(forceRedraw = false) {
            const container = document.getElementById("chat-messages");
            if(!container) return;
            if(!db.messages) db.messages = [];

            // Pinned mesaj
            const pinArea = document.getElementById("pinned-message-area"); 
            const pinText = document.getElementById("pinned-message-text");
            if(db.pinned_message && db.pinned_message.expires && db.pinned_message.expires > Date.now()) { 
                pinArea.classList.remove("hidden"); 
                pinText.textContent = `${db.pinned_message.user}: ${db.pinned_message.text}`; 
            } else { 
                pinArea.classList.add("hidden"); 
            }

            const wasAtBottom = container.scrollHeight - container.clientHeight <= container.scrollTop + 100;

            // Silinen mesaj var mı kontrol et
            const currentIds = new Set(db.messages.map(m => m.id));
            const hasDeleted = [..._renderedMsgIds].some(id => !currentIds.has(id));

            if (forceRedraw || hasDeleted) {
                // Silme veya zorla yenile - tüm container'ı yeniden çiz
                while(container.firstChild) container.removeChild(container.firstChild);
                _renderedMsgIds.clear();
            }

            // ── Empty State ──
            if (db.messages.length === 0) {
                const emptyEl = document.getElementById('_chat_empty_state_');
                if (!emptyEl) {
                    container.innerHTML = `
                        <div id="_chat_empty_state_" class="flex flex-col items-center justify-center h-full text-center py-16 fade-in-anim">
                            <div style="font-size:48px;margin-bottom:12px;opacity:0.6">💬</div>
                            <div class="text-zinc-400 text-sm font-bold mb-1">Henüz mesaj yok</div>
                            <div class="text-zinc-600 text-xs">İlk mesajı sen yaz! 🏔️</div>
                        </div>`;
                }
                return;
            }

            // Sadece yeni mesajları DOM'a ekle
            db.messages.forEach(msg => {
                if (!_renderedMsgIds.has(msg.id)) {
                    const div = document.createElement('div');
                    div.innerHTML = buildMsgHTML(msg);
                    const el = div.firstElementChild;
                    if(el) {
                        el.dataset.msgId = msg.id;
                        container.appendChild(el);
                    }
                    _renderedMsgIds.add(msg.id);
                }
            });

            if(wasAtBottom || _renderedMsgIds.size <= db.messages.length) {
                requestAnimationFrame(() => {
                    container.scrollTop = container.scrollHeight;
                });
            }
        }

        async function sendChatMessage() { 
            if(!currentUser.accepted_chat_rules) {
                return document.getElementById("chat-rules-modal").classList.remove("hidden");
            }
            const inp = document.getElementById("chat-input"); 
            if(!inp.value.trim()) return;
            haptic([8]);
            const t = inp.value; 
            inp.value = ""; 
            const id = Date.now().toString(); 

            // ── Optimistic UI: mesajı anında göster ──
            const optimisticMsg = { id, user: currentUser.username, text: t, type: 'text' };
            db.messages.push(optimisticMsg);
            renderChat();

            try {
                const result = await sendAction('add_message', { id: id, text: t, type: "text" }, true);

                if (result && result.warning) {
                    showToast(`⚠️ ${result.warning}`, 'warning', 5000);
                }

                // ── Proaktif AI moderasyon sonucu ──
                if (result && result.ai_flagged) {
                    // Mesajı flagged olarak güncelle
                    const localMsg = db.messages.find(m => m.id === id);
                    if (localMsg) {
                        localMsg.is_flagged = true;
                        localMsg.flag_count = 1;
                    }

                    // AI moderatör uyarı mesajını chat'e ekle
                    if (result.ai_moderation_msg) {
                        db.messages.push(result.ai_moderation_msg);
                    }

                    renderChat(true);

                    if (result.severity === 'high') {
                        showToast('🚫 İçeriğiniz topluluk kurallarını ihlal ediyor! Admin ekibine bildirildi.', 'error', 5000);
                    } else {
                        showToast('⚠️ Mesajınız uygunsuz içerik içeriyor ve işaretlendi.', 'warning', 4000);
                    }
                }
            } catch(err) {
                // Hata durumunda optimistic mesajı geri al
                db.messages = db.messages.filter(m => m.id !== id);
                renderChat(true);
                // err.message backend'den gelen "Çok fazla istek gönderdiniz" uyarısı olabilir
                const errMsg = err.message || 'Mesaj gönderilemedi. Tekrar deneyin.';
                showToast(`❌ ${errMsg}`, 'error');
                return;
            }

            // Daily/weekly mission counters
            if(currentUser.stats) {
                if(!currentUser.stats.daily_missions) currentUser.stats.daily_missions = {};
                if(!currentUser.stats.weekly_missions) currentUser.stats.weekly_missions = {};
                const todayKey = new Date().toISOString().split('T')[0];
                if(currentUser.stats.daily_missions.date !== todayKey) currentUser.stats.daily_missions = { date: todayKey };
                currentUser.stats.daily_missions.daily_msg = (currentUser.stats.daily_missions.daily_msg||0)+1;
                currentUser.stats.weekly_missions.weekly_msg = (currentUser.stats.weekly_missions.weekly_msg||0)+1;
                checkMissions();
            }
        }

        async function askAIGroup() {
            if(!currentUser.accepted_chat_rules) {
                return document.getElementById("chat-rules-modal").classList.remove("hidden");
            }
            const inp = document.getElementById("chat-input");
            const t = inp.value.trim();
            if(!t) return alert("Lutfen Freerider AI'a sormak istediginiz soruyu mesaj kutusuna yazin!");
            inp.value = "";
            await sendAction('ask_ai', { text: t });
            // Daily/weekly AI mission counter
            if(currentUser.stats) {
                if(!currentUser.stats.daily_missions) currentUser.stats.daily_missions = {};
                if(!currentUser.stats.weekly_missions) currentUser.stats.weekly_missions = {};
                const todayKey = new Date().toISOString().split('T')[0];
                if(currentUser.stats.daily_missions.date !== todayKey) currentUser.stats.daily_missions = { date: todayKey };
                currentUser.stats.daily_missions.daily_ai = (currentUser.stats.daily_missions.daily_ai||0)+1;
                currentUser.stats.weekly_missions.weekly_ai = (currentUser.stats.weekly_missions.weekly_ai||0)+1;
                checkMissions();
            }
        }

        function renderDmList() {
            const container = document.getElementById("dm-users-list");
            container.innerHTML = "";
            
            let uniqueUsers = new Set();
            db.dms.forEach(m => {
                if (m.participants && m.participants.includes(currentUser.username)) {
                    m.participants.forEach(p => { if (p !== currentUser.username) uniqueUsers.add(p); });
                }
            });

            uniqueUsers.add("Freerider AI");

            if(uniqueUsers.size === 0) {
                container.innerHTML = "<div class='text-zinc-500 text-xs italic text-center mt-5 font-medium'>Henüz kimseyle özel mesajlaşmadın.</div>";
                return;
            }

            Array.from(uniqueUsers).forEach(uName => {
                const u = db.users.find(x => x.username === uName);
                const isAI = uName === 'Freerider AI';
                
                let avatar = isAI ? 'https://cdn-icons-png.flaticon.com/512/4712/4712035.png' : (u ? u.avatar : 'https://cdn.freeridertr.com.tr/profil%20resmi/unnamed.jpg');
                
                let premColor = isAI ? '' : getUserPremiumColor(uName);
                let textCls = (getUserPremiumTier(uName) > 0) ? getPremiumTextClass(premColor) : '';
                let inlineStyle = (getUserPremiumTier(uName) > 0) ? getPremiumInlineStyle(premColor) : '';
                let nameHtml = isAI ? `<span class="text-cyan-400 font-black tracking-widest uppercase text-sm drop-shadow-[0_0_10px_cyan] animate-pulse">🤖 Freerider AI</span>` : `<span style="${inlineStyle}" class="font-bold text-sm tracking-wide ${textCls ? textCls : 'text-white'}">${uName}</span>`;

                const dmOnline = isAI ? '' : getOnlineHTML(u);
                container.innerHTML += `
                <div onclick="renderDmThread('${uName}')" class="bg-black/50 p-3 rounded-2xl border border-zinc-800 flex items-center gap-3 cursor-pointer hover:bg-zinc-800 hover:border-zinc-600 transition-all duration-200 shadow-sm mb-3 slide-up-anim">
                    <div class="relative">
                        <img src="${avatar}" class="w-12 h-12 rounded-full object-cover border border-zinc-700 shadow-inner">
                        ${!isAI && getOnlineStatus(u).status === 'online' ? '<span class="online-dot absolute bottom-0 right-0"></span>' : ''}
                    </div>
                    <div class="flex-1 overflow-hidden">
                        ${nameHtml}
                        <div class="flex items-center gap-2 mt-1">
                            ${dmOnline ? `<span class="flex items-center gap-1">${dmOnline}</span>` : `<span class="text-[10px] text-zinc-500 uppercase font-bold tracking-widest truncate">${isAI ? 'Özel Asistanın' : 'Görüntülemek için tıkla'}</span>`}
                        </div>
                    </div>
                    <div class="text-zinc-400 bg-zinc-900 w-8 h-8 rounded-full flex items-center justify-center border border-zinc-700">💬</div>
                </div>`;
            });
        }

        function startDm(targetUser) {
            document.getElementById("other-profile-modal").classList.add("hidden");
            switchTab(1);
            switchChatTab('dm');
            renderDmThread(targetUser);
        }

        function renderDmThread(targetUser) {
            currentDmUser = targetUser;
            document.getElementById("chat-dm-list-area").classList.add("hidden");
            document.getElementById("chat-dm-thread-area").classList.remove("hidden");
            document.getElementById("dm-thread-name").innerHTML = targetUser === 'Freerider AI' ? '<span class="text-cyan-400 drop-shadow-[0_0_10px_cyan] font-black tracking-widest">🤖 Freerider AI</span>' : targetUser;

            const container = document.getElementById("dm-messages");
            const isScrolled = container.scrollHeight - container.clientHeight <= container.scrollTop + 30;
            container.innerHTML = "";

            const threadMsgs = db.dms.filter(m => 
                m.participants && m.participants.includes(currentUser.username) && m.participants.includes(targetUser)
            ).sort((a,b) => parseInt(a.id) - parseInt(b.id));

            if(threadMsgs.length === 0) {
                container.innerHTML = `<div class="text-center text-xs text-zinc-500 mt-10 italic font-medium">Buradan sohbet edebilirsiniz. Mesajlar uçtan uca olmasa da izole şifrelenir.</div>`;
            }

            threadMsgs.forEach(msg => {
                const isMe = msg.sender === currentUser.username;
                const isAI = msg.sender === 'Freerider AI';
                let bubbleClass = isMe ? 'bg-white text-black' : 'bg-black/60 border border-zinc-800 text-zinc-300';
                
                if (isAI) {
                    bubbleClass = 'bg-black border border-cyan-500/50 text-cyan-100 shadow-[0_0_15px_rgba(6,182,212,0.3)] font-medium';
                }

                let content = "";
                if (msg.type === "photo") {
                    content = `<img src="${msg.photo}" onclick="openFullscreen(['${msg.photo}'],0)" class="w-48 rounded-xl border border-zinc-700 shadow-lg mt-1 cursor-pointer hover:opacity-90 transition-opacity">`;
                } else {
                    content = `<div class="${bubbleClass} px-4 py-2.5 rounded-2xl text-sm break-words mt-1 shadow-md leading-relaxed font-medium">${escapeHtml(msg.text)}</div>`;
                }

                let avatarUrl = isAI ? 'https://cdn-icons-png.flaticon.com/512/4712/4712035.png' : (db.users.find(u => u.username === msg.sender)?.avatar || 'https://cdn.freeridertr.com.tr/profil%20resmi/unnamed.jpg');
                let avatarHtml = `<img src="${avatarUrl}" class="w-8 h-8 rounded-full object-cover border border-zinc-700 shrink-0 ${isMe ? 'ml-2' : 'mr-2'}">`;

                const _dmEncId = btoa(encodeURIComponent(msg.id)); const _dmEncSender = btoa(encodeURIComponent(msg.sender)); const _dmEncText = btoa(encodeURIComponent((msg.text||'').substring(0,80)));
                const dmReportBtn = (!isMe && !isAI)
                    ? `<button onclick="openReportMsgModal('${_dmEncId}','${_dmEncSender}','${_dmEncText}')" class="text-[10px] bg-orange-950/60 text-orange-400 px-1.5 py-0.5 rounded-lg ml-1 hover:bg-orange-900/60 transition border border-orange-900/50 uppercase font-bold tracking-widest relative z-50 pointer-events-auto" title="Mesajı Bildir">🚩</button>`
                    : '';

                container.innerHTML += `
                <div class="flex ${isMe ? "justify-end" : "justify-start"} items-start mb-5 w-full slide-up-anim">
                    ${!isMe ? avatarHtml : ''}
                    <div class="max-w-[80%] flex flex-col ${isMe ? 'items-end' : 'items-start'}">
                        <div class="flex items-center gap-1 text-[10px] text-zinc-500 uppercase font-bold tracking-widest mb-1">
                            ${isMe ? 'Sen' : (isAI ? '<span class="text-cyan-400">AI</span>' : msg.sender)}
                            ${dmReportBtn}
                        </div>
                        ${content}
                    </div>
                    ${isMe ? avatarHtml : ''}
                </div>`;
            });

            if(isScrolled || container.scrollTop === 0) {
                container.scrollTop = container.scrollHeight;
            }
        }

        function closeDmThread() {
            currentDmUser = null;
            document.getElementById("chat-dm-thread-area").classList.add("hidden");
            document.getElementById("chat-dm-list-area").classList.remove("hidden");
        }

        async function sendDmMessage() {
            const inp = document.getElementById("dm-input");
            const t = inp.value.trim();
            if(!t || !currentDmUser) return;
            
            inp.value = "";
            const id = Date.now().toString();
            
            db.dms.push({ id: id, sender: currentUser.username, receiver: currentDmUser, participants: [currentUser.username, currentDmUser], text: t, type: 'text' });
            renderDmThread(currentDmUser);

            await sendAction('send_dm', { id: id, text: t, receiver: currentDmUser, type: "text" });
        }

        function openMarketModal() {
            document.getElementById("mk-title").value = "";
            document.getElementById("mk-price").value = "";
            document.getElementById("mk-contact").value = "";
            document.getElementById("mk-desc").value = "";
            document.getElementById("mk-photos").value = "";
            
            const tier = getUserPremiumTier(currentUser.username);
            let maxP = 1;
            if(tier >= 3) maxP = 10; else if(tier >= 2) maxP = 4; else if(tier >= 1) maxP = 2;
            document.getElementById("mk-photo-label").textContent = `Fotoğraf Ekle (Maksimum ${maxP} Adet)`;
            
            document.getElementById("market-modal").classList.remove("hidden");
        }

        async function saveMarketItem() {
            const t = document.getElementById("mk-title").value;
            const p = document.getElementById("mk-price").value;
            const c = document.getElementById("mk-contact").value;
            const d = document.getElementById("mk-desc").value;
            const files = document.getElementById("mk-photos").files;

           if(files[0] && !checkFileSize(files[0], 10)) return;
            
            if(!t || !p || !c) return alert("Başlık, Fiyat ve İletişim zorunludur!");
            
            const tier = getUserPremiumTier(currentUser.username);
            let maxP = 1;
            if(tier >= 3) maxP = 10; else if(tier >= 2) maxP = 4; else if(tier >= 1) maxP = 2;
            
            if(files.length > maxP) return alert(`Mevcut paketiniz ${maxP} fotoğraf yüklemenize izin veriyor.`);
            
            document.getElementById("market-modal").classList.add("hidden");
            
            let photoDataArray = [];
            for(let i=0; i<files.length; i++) {
                if(i < maxP) {
                    let b64 = await resizeImage(files[i], 800);
                    if(b64) photoDataArray.push(b64);
                }
            }
            if(photoDataArray.length === 0) photoDataArray = ["https://placehold.co/400x300/121214/FFF?text=FOTO+YOK"];
            
            await sendAction('add_market', { id: Date.now().toString(), title: t, price: p, contact: c, desc: d, image: photoDataArray });
        }

        function renderMarket() {
            const container = document.getElementById("market-list");
            container.innerHTML = "";
            
            if(!db.market || db.market.length === 0) {
                container.innerHTML = "<div class='col-span-2 text-center text-zinc-500 italic mt-10 font-medium'>Pazar şu an boş.</div>";
                return;
            }
            
            const sortedMarket = db.market.sort((a,b) => (b.bumped_at || 0) - (a.bumped_at || 0));

            sortedMarket.forEach(item => {
                let mainImg = Array.isArray(item.image) ? item.image[0] : (item.image || "https://placehold.co/400x300/121214/FFF?text=FOTO+YOK");
                
                const ownerTier = getUserPremiumTier(item.owner);
                let borderClass = ownerTier >= 2 ? "border-purple-500 shadow-[0_0_15px_rgba(168,85,247,0.3)]" : "border-zinc-800 shadow-sm";
                let premiumTag = ownerTier >= 2 ? `<div class="absolute top-0 right-0 bg-purple-600 text-white text-[8px] font-black px-2 py-1 rounded-bl-lg shadow-lg z-10 uppercase tracking-widest">Premium İlan</div>` : "";

                container.innerHTML += `
                <div onclick="openMarketDetail('${item.id}')" class="bg-black/40 rounded-2xl overflow-hidden border ${borderClass} relative cursor-pointer hover:border-zinc-500 transition-all duration-300 hover:scale-[1.02] flex flex-col group">
                    ${premiumTag}
                    <div class="h-32 w-full bg-zinc-950 relative border-b border-zinc-800">
                        <img src="${mainImg}" class="w-full h-full object-cover group-hover:opacity-90 transition-opacity">
                        <div class="absolute bottom-2 left-2 bg-black/80 backdrop-blur-md px-3 py-1.5 rounded-lg border border-zinc-700 text-green-400 font-black text-xs shadow-lg">${item.price} TL</div>
                    </div>
                    <div class="p-4 flex-1 flex flex-col">
                        <h3 class="text-white font-bold text-xs tracking-wide flex-1 leading-snug">${item.title}</h3>
                        <div class="text-[9px] text-zinc-500 font-bold uppercase tracking-widest mt-3 flex justify-between items-center border-t border-zinc-800 pt-2">
                            <span class="truncate pr-2">👤 ${item.owner}</span>
                            <span class="shrink-0">👁️ ${item.views || 0}</span>
                        </div>
                    </div>
                </div>`;
            });
        }

        // openMarketDetail: renderMarket kartlarından çağrılan alias — viewMarketDetail ile aynıdır
        function openMarketDetail(id) {
            const item = db.market.find(x => String(x.id) === String(id));
            if(!item) { console.warn('[Market] openMarketDetail: ID bulunamadı:', id); return; }
            viewMarketDetail(id);
        }

        function viewMarketDetail(id) {
            const item = db.market.find(x => String(x.id) === String(id));
            if(!item) { console.warn('Market item not found for id:', id); return; }
            
            currentMarketId = id;
            window.currentOwner = item.owner;
            
            if(item.owner !== currentUser.username) {
                sendAction('increment_market_view', { id: id }).catch(e=>{});
            }

            const imgContainer = document.getElementById("md-photos");
            imgContainer.innerHTML = "";
            let images = Array.isArray(item.image) ? item.image : [item.image || "https://placehold.co/400x300/121214/FFF?text=FOTO+YOK"];
            images.forEach(img => {
                imgContainer.innerHTML += `<img src="${img}" class="h-full w-auto object-contain shrink-0 scroll-snap-align-center rounded-xl">`;
            });

            document.getElementById("md-title").textContent = item.title;
            document.getElementById("md-price").textContent = `${item.price} TL`;
            
            if(getUserPremiumTier(currentUser.username) === 3 || item.owner === currentUser.username) {
                document.getElementById("md-views-badge").classList.remove("hidden");
                document.getElementById("md-views-badge").textContent = `👁️ ${item.views || 0} Görüntülenme`;
            } else {
                document.getElementById("md-views-badge").classList.add("hidden");
            }
            
            const ownerObj = db.users.find(u => u.username === item.owner);
            document.getElementById("md-owner-avatar").src = ownerObj ? ownerObj.avatar : "https://cdn.freeridertr.com.tr/profil%20resmi/unnamed.jpg";
            document.getElementById("md-owner").textContent = item.owner;
            
            document.getElementById("md-desc").textContent = item.desc || "Açıklama girilmemiş.";
            document.getElementById("md-contact").textContent = item.contact;

            let actionsHtml = "";
            if(item.owner !== currentUser.username) {
                actionsHtml += `<button onclick="startDm('${item.owner}')" class="bg-white hover:bg-gray-200 transition text-black py-4 rounded-xl font-bold text-sm w-full shadow-[0_0_15px_rgba(255,255,255,0.3)] btn-premium-hover">✉️ SATICIYA MESAJ AT</button>`;
            }
            
            if(item.owner === currentUser.username && getUserPremiumTier(currentUser.username) >= 2) {
                actionsHtml += `<button onclick="bumpMarket('${item.id}')" class="bg-purple-900/50 hover:bg-purple-800 transition text-purple-400 border border-purple-500/50 py-3.5 rounded-xl font-bold text-xs w-full mt-3 uppercase tracking-widest shadow-lg btn-premium-hover">🚀 İLANI EN ÜSTE TAŞI (BUMP)</button>`;
            }
            
            if(item.owner === currentUser.username || currentUser.role === 'Admin') {
                actionsHtml += `<button onclick="deleteMarket('${item.id}')" class="bg-red-950/50 hover:bg-sky-900/80 transition text-sky-400 border border-sky-900/50 py-3.5 rounded-xl font-bold text-xs w-full mt-3 uppercase tracking-widest btn-premium-hover shadow-md">İLANI SİL</button>`;
            }
            
            document.getElementById("md-actions-area").innerHTML = actionsHtml;
            document.getElementById("market-detail-modal").classList.remove("hidden");
        }

        async function bumpMarket(id) {
            await sendAction('bump_market', { id: id });
            alert("İlanınız başarıyla en üste taşındı!");
            document.getElementById("market-detail-modal").classList.add("hidden");
            renderMarket();
        }

        async function deleteMarket(id) {
            if(confirm("Bu ilanı silmek istediğinize emin misiniz?")) {
                await sendAction('delete_market', { id: id });
                db.market = db.market.filter(m => m.id !== id);
                document.getElementById("market-detail-modal").classList.add("hidden");
                renderMarket();
            }
        }

        function switchLeaderboard(tab) {
            currentLeaderboardTab = tab;
            document.getElementById("rank-tab-weekly").className = "flex-1 py-2 bg-transparent text-zinc-500 hover:text-white rounded font-bold text-xs transition";
            document.getElementById("rank-tab-month").className = "flex-1 py-2 bg-transparent text-zinc-500 hover:text-white rounded font-bold text-xs transition";
            document.getElementById("rank-tab-all").className = "flex-1 py-2 bg-transparent text-zinc-500 hover:text-white rounded font-bold text-xs transition";
            
            if(tab === 'weekly') {
                document.getElementById("rank-tab-weekly").className = "flex-1 py-2 bg-zinc-800 text-white rounded font-bold text-xs transition shadow-sm";
            } else if(tab === 'month') {
                document.getElementById("rank-tab-month").className = "flex-1 py-2 bg-zinc-800 text-white rounded font-bold text-xs transition shadow-sm";
            } else {
                document.getElementById("rank-tab-all").className = "flex-1 py-2 bg-zinc-800 text-white rounded font-bold text-xs transition shadow-sm";
            }
            renderLeaderboard();
        }


        function renderLeaderboard() {
            const container = document.getElementById("leaderboard");
            container.innerHTML = "";

            // Admin sıralamada gösterilmez
            const visibleUsers = db.users.filter(u => u.username !== 'Admin' && u.role !== 'Admin');

            let sortedUsers = [];
            if(currentLeaderboardTab === 'weekly') {
                sortedUsers = [...visibleUsers].sort((a,b) => ((b.stats&&b.stats.weekly_xp)||0) - ((a.stats&&a.stats.weekly_xp)||0)).slice(0,50);
            } else if(currentLeaderboardTab === 'month') {
                sortedUsers = [...visibleUsers].sort((a,b) => ((b.stats&&b.stats.monthly_xp)||0) - ((a.stats&&a.stats.monthly_xp)||0)).slice(0,50);
            } else {
                sortedUsers = [...visibleUsers].sort((a,b) => (b.xp||0) - (a.xp||0)).slice(0,50);
            }

            if(sortedUsers.length === 0) {
                container.innerHTML = "<div class='text-zinc-500 text-xs italic text-center py-8'>Henuz siralamada kimse yok.</div>";
                return;
            }

            // Champion banner (1st place highlight)
            const champ = sortedUsers[0];
            if(champ) {
                const champColor = getUserPremiumColor(champ.username);
                const champTextCls = getUserPremiumTier(champ.username) > 0 ? getPremiumTextClass(champColor) : 'text-yellow-400';
                const tabLabel = currentLeaderboardTab === 'weekly' ? 'Bu Haftanin Birincisi' : currentLeaderboardTab === 'month' ? 'Bu Ayin Birincisi' : 'Tum Zamanlarin Birincisi';
                const champVal = currentLeaderboardTab === 'weekly' ? ((champ.stats&&champ.stats.weekly_xp)||0) : currentLeaderboardTab === 'month' ? ((champ.stats&&champ.stats.monthly_xp)||0) : (champ.xp||0);
                container.innerHTML += `
                <div class="relative bg-gradient-to-r from-yellow-900/60 to-amber-900/40 rounded-3xl p-5 mb-5 border border-yellow-600/50 shadow-[0_0_30px_rgba(234,179,8,0.25)] overflow-hidden">
                    <div class="absolute inset-0 opacity-10 pointer-events-none" style="background:radial-gradient(circle at 70% 50%, #fbbf24 0%, transparent 70%);"></div>
                    <div class="text-[10px] text-yellow-500 font-black uppercase tracking-[0.15em] mb-2 flex items-center gap-2">
                        <span class="animate-pulse">👑</span> ${tabLabel}
                    </div>
                    <div class="flex items-center gap-4">
                        <div class="relative">
                            <img src="${champ.avatar||'https://cdn.freeridertr.com.tr/profil%20resmi/unnamed.jpg'}" class="w-16 h-16 rounded-full object-cover border-4 border-yellow-500 shadow-[0_0_20px_rgba(234,179,8,0.6)]">
                            <div class="absolute -bottom-1 -right-1 text-2xl">🥇</div>
                        </div>
                        <div class="flex-1">
                            <div class="font-black text-xl ${champTextCls} teko-font tracking-wide">${champ.username}</div>
                            <div class="text-yellow-400 font-black text-2xl teko-font">${champVal.toLocaleString()} XP</div>
                            <div class="text-[10px] text-zinc-400 mt-1">${currentLeaderboardTab === 'weekly' ? '🏆 1 Haftalik Ultra+ Odulu Kazanacak!' : currentLeaderboardTab === 'month' ? '🏆 1 Aylik Deluxe Odulu Kazanacak!' : ''}</div>
                        </div>
                    </div>
                </div>`;
            }

            sortedUsers.forEach((u, index) => {
                const title = getTitle(u.xp);
                const isMe = u.username === currentUser.username;
                let rankVisual = `<div class="w-8 h-8 rounded-full bg-black/60 border border-zinc-700 flex items-center justify-center font-black text-xs text-zinc-400">${index+1}</div>`;
                if(index === 0) rankVisual = `<div class="text-3xl drop-shadow-[0_0_15px_rgba(251,191,36,0.9)] animate-pulse">🥇</div>`;
                if(index === 1) rankVisual = `<div class="text-3xl drop-shadow-[0_0_12px_rgba(156,163,175,0.8)]">🥈</div>`;
                if(index === 2) rankVisual = `<div class="text-3xl drop-shadow-[0_0_12px_rgba(180,83,9,0.8)]">🥉</div>`;

                const premColor = getUserPremiumColor(u.username);
                const textCls = getUserPremiumTier(u.username)>0 ? getPremiumTextClass(premColor) : '';
                const inlineStyle = getUserPremiumTier(u.username)>0 ? getPremiumInlineStyle(premColor) : '';
                const borderCls = getUserPremiumTier(u.username)>0 ? getPremiumBorderClass(u.username) : 'border-zinc-700';
                const onlineHtml = getOnlineHTML(u);

                let val = currentLeaderboardTab==='weekly' ? ((u.stats&&u.stats.weekly_xp)||0)
                        : currentLeaderboardTab==='month' ? ((u.stats&&u.stats.monthly_xp)||0)
                        : (u.xp||0);

                // Reward badge for top 3
                let rewardTag = '';
                if(index === 0 && currentLeaderboardTab === 'weekly') rewardTag = '<span class="text-[9px] bg-yellow-600 text-black px-2 py-0.5 rounded font-black ml-1">1HFT ULTRA+</span>';
                else if((index===1||index===2) && currentLeaderboardTab==='weekly') rewardTag = '<span class="text-[9px] bg-purple-600 text-white px-2 py-0.5 rounded font-black ml-1">1HFT DLX</span>';
                else if(index<=2 && currentLeaderboardTab==='month') rewardTag = '<span class="text-[9px] bg-blue-600 text-white px-2 py-0.5 rounded font-black ml-1">1AY DLX</span>';

                container.innerHTML += `
                <div onclick="showOtherProfile('${u.username}')" class="bg-black/40 p-4 rounded-2xl border ${isMe?'border-zinc-400 shadow-[0_0_15px_rgba(255,255,255,0.15)]':'border-zinc-800'} flex items-center gap-4 cursor-pointer hover:bg-zinc-800/50 transition-all duration-200 shadow-sm group slide-up-anim mb-2">
                    <div class="w-10 flex justify-center shrink-0">${rankVisual}</div>
                    <div class="relative shrink-0">
                        <img src="${u.avatar||'https://cdn.freeridertr.com.tr/profil%20resmi/unnamed.jpg'}" class="w-11 h-11 rounded-full object-cover border-2 ${borderCls} shadow-md group-hover:scale-110 transition-transform">
                        ${getOnlineStatus(u).status==='online'?'<span class="online-dot absolute bottom-0 right-0"></span>':''}
                    </div>
                    <div class="flex-1 overflow-hidden">
                        <div class="flex items-center gap-1 flex-wrap">
                            <span style="${inlineStyle}" class="font-bold text-sm tracking-wide truncate ${textCls||'text-white'}">${u.username}</span>${rewardTag}
                        </div>
                        <div class="flex items-center gap-2 mt-0.5">
                            <span class="text-[9px] text-zinc-500 font-bold uppercase">${title.icon} ${title.name}</span>
                            ${onlineHtml?`<span class="flex items-center gap-1">${onlineHtml}</span>`:''}
                        </div>
                    </div>
                    <div class="text-right shrink-0 bg-zinc-950/50 px-3 py-2 rounded-xl border border-zinc-800">
                        <div class="text-white font-black text-lg teko-font tracking-widest">${val.toLocaleString()}</div>
                        <div class="text-[9px] text-zinc-500 uppercase font-bold">XP</div>
                    </div>
                </div>`;
            });
        }
        function renderNews() {
            const container = document.getElementById("news-list");
            container.innerHTML = "";
            db.news.forEach(n => {
                let imgHtml = n.image ? `<img src="${n.image}" class="w-full h-48 object-cover rounded-xl mt-4 border border-zinc-700 shadow-md">` : '';
                let delBtn = currentUser.role === 'Admin' ? `<button onclick="deleteNews('${n.id}')" class="mt-4 bg-red-950/50 hover:bg-sky-900/80 text-sky-400 px-5 py-2.5 rounded-xl text-xs font-bold border border-sky-900/50 transition btn-premium-hover uppercase tracking-widest shadow-md">Haberi Sil</button>` : '';
                
                container.innerHTML += `
                <div class="glass-panel p-6 rounded-3xl border border-zinc-800 shadow-xl mb-5 slide-up-anim">
                    <h3 class="text-2xl text-white font-bold tracking-wide drop-shadow-sm leading-tight">${n.title}</h3>
                    <div class="text-[10px] text-zinc-500 font-bold uppercase tracking-widest mt-2 flex items-center gap-2"><span class="animate-pulse">🕒</span> ${n.date}</div>
                    ${imgHtml}
                    <p class="text-sm text-zinc-300 mt-5 leading-relaxed whitespace-pre-wrap font-medium">${n.content}</p>
                    ${delBtn}
                </div>`;
            });
        }

        function openNewsAdminModal() { document.getElementById("news-admin-modal").classList.remove("hidden"); }
        
        async function saveNews() {
            const t = document.getElementById("news-title").value;
            const c = document.getElementById("news-content").value;
            const f = document.getElementById("news-photo").files[0];
            
            if(!t || !c) return alert("Başlık ve içerik zorunludur!");
            
            document.getElementById("news-admin-modal").classList.add("hidden");
            
            let imgData = null;
            if(f) imgData = await resizeImage(f, 800);
            
            await sendAction('add_news', { id: Date.now().toString(), title: t, content: c, image: imgData, date: new Date().toLocaleDateString() });
            renderNews();
        }
        
        async function deleteNews(id) {
            if(confirm("Haberi silmek istiyor musunuz?")) {
                await sendAction('delete_news', {id: id});
                db.news = db.news.filter(n => n.id !== id);
                renderNews();
            }
        }

        function switchTab(idx) {
            stopAllMedia(); // Hayalet ses önleme — tüm medyayı durdur
            // Popup triggers removed per user request
            if (idx !== 9) _prevTab = idx; // Reels dışındaki son sekmeyi hatırla
            const tabs = ['screen-map', 'screen-chat', 'screen-market', 'screen-rank', 'screen-news', 'screen-missions', 'screen-premium', 'screen-profile', 'screen-referral', 'screen-reels'];
            tabs.forEach((t, i) => {
                const el = document.getElementById(t);
                if(!el) return;
                if(i === idx) {
                    // Görünür yap - chat için innerHTML'e dokunmadan
                    el.style.display = 'flex';
                    el.style.flexDirection = 'column';
                    el.style.zIndex = '20';
                    el.style.opacity = '1';
                    el.style.pointerEvents = 'auto';
                    el.classList.remove('hidden');
                    el.style.animation = 'none';
                    el.offsetHeight;
                    el.style.animation = 'slideUpFade 0.38s cubic-bezier(0.16, 1, 0.3, 1) both';
                } else {
                    // Gizle ama innerHTML'e dokunma
                    el.style.display = 'none';
                    el.style.zIndex = '-1';
                    el.style.pointerEvents = 'none';
                    el.classList.add('hidden');
                    el.style.animation = 'none';
                }
            });
            
            document.querySelectorAll(".tab-btn").forEach((btn, i) => {
                if(i === idx) {
                    btn.classList.add("text-white", "scale-105", "opacity-100", "bg-zinc-800/80", "shadow-md");
                    btn.classList.remove("text-zinc-500", "opacity-70", "bg-zinc-900/50", "hover:bg-zinc-900/50");
                } else {
                    btn.classList.remove("text-white", "scale-105", "opacity-100", "bg-zinc-800/80", "shadow-md");
                    btn.classList.add("text-zinc-500", "opacity-70", "hover:bg-zinc-900/50");
                }
            });

            // Reels tam ekran: alt nav'ı gizle/göster
            const bottomNav = document.getElementById('bottom-nav');
            const soundBtn2 = document.getElementById('reel-sound-btn');
            const gridBtn2  = document.getElementById('grid-view-btn');
            const uploadTopBtn2 = document.getElementById('reels-upload-top-btn');
            if(idx === 9) {
                if(bottomNav) bottomNav.style.display = 'none';
                // Ses, ızgara ve yükleme butonlarını göster (loadReels bitmeden önce de görünsün)
                if(soundBtn2) { soundBtn2.style.display = 'flex'; soundBtn2.textContent = _reelMuted ? '🔇' : '🔊'; }
                if(gridBtn2)  gridBtn2.style.display = 'flex';
                if(uploadTopBtn2) uploadTopBtn2.style.display = 'flex';
                document.getElementById('screen-map') && (document.getElementById('screen-map').style.zIndex = '1');
            } else {
                if(bottomNav) bottomNav.style.display = '';
                if(soundBtn2) soundBtn2.style.display = 'none';
                if(gridBtn2)  gridBtn2.style.display = 'none';
                if(uploadTopBtn2) uploadTopBtn2.style.display = 'none';
                // stopAllMedia zaten başta çağrıldı, ek pause gerekmez
            }

            if(idx === 0) { if(map) { map.invalidateSize(); syncMap(); } }
            if(idx === 1) { renderChat(); renderDmList(); clearChatBadge(); renderStoryBar(); }
            if(idx === 2) renderMarket();
            if(idx === 3) renderLeaderboard();
            if(idx === 4) renderNews();
            if(idx === 5) { renderMissions(); updateSpinInfo(); setTimeout(initWheel3D, 150); }
            if(idx === 7) { updateProfileUI(); updateNotifBtnState(); }
            if(idx === 8) renderReferralTab();
            if(idx === 9) loadReels();
            
            // Alt nav güncelle (premium animasyonlu)
            const bnavIds = [0,1,9,3,7];
            bnavIds.forEach(i => {
                const btn = document.getElementById('bnav-' + i);
                if(!btn) return;
                const iconEl = btn.querySelector('span:first-child');
                const labelEl = btn.querySelector('span:last-child');
                if(i === idx) {
                    btn.classList.add('text-white');
                    btn.classList.remove('text-zinc-500');
                    btn.style.background = 'linear-gradient(135deg,rgba(2,132,199,0.3),rgba(3,105,161,0.15))';
                    btn.style.boxShadow = '0 0 16px rgba(14,165,233,0.25),inset 0 1px 0 rgba(255,255,255,0.05)';
                    if(iconEl) {
                        iconEl.style.transform = 'scale(1.18) translateY(-1px)';
                        iconEl.style.filter = 'drop-shadow(0 0 6px rgba(14,165,233,0.8))';
                    }
                    if(labelEl) {
                        labelEl.style.color = '#7dd3fc';
                        labelEl.style.opacity = '1';
                    }
                } else {
                    btn.classList.remove('text-white');
                    btn.classList.add('text-zinc-500');
                    btn.style.background = '';
                    btn.style.boxShadow = '';
                    if(iconEl) {
                        iconEl.style.transform = '';
                        iconEl.style.filter = '';
                    }
                    if(labelEl) {
                        labelEl.style.color = '';
                        labelEl.style.opacity = '';
                    }
                }
            });

            const sidebar = document.getElementById("sidebar");
            if(sidebar && !sidebar.classList.contains("-translate-x-full") && window.innerWidth < 768) {
                toggleSidebar();
            }
        }

        // ============================================================
        // PROMINENT DISCLOSURE — Fotoğraf (Google Play uyumu)
        // file input tetiklenmeden ÖNCE kullanıcıya amaç gösterilir.
        // ============================================================
        const _PD_PHOTO_CFG = {
            group:   { icon:'💬', title:'Sohbete Fotoğraf Ekle',   sub:'Grup Sohbeti',
                       desc:'Seçeceğin fotoğraf <strong class="text-white">grup sohbetine</strong> gönderilecek.',
                       items:['Fotoğraf yalnızca grup üyelerine görünür','Görsel otomatik boyutlandırılır (maks. 800px)','Yalnızca seçtiğin görsel paylaşılır'] },
            dm:      { icon:'✉️', title:'Mesaja Fotoğraf Ekle',     sub:'Özel Mesaj',
                       desc:'Seçeceğin fotoğraf <strong class="text-white">özel mesaj</strong> olarak gönderilecek.',
                       items:['Yalnızca mesaj gönderdiğin kişi görebilir','Görsel otomatik boyutlandırılır (maks. 800px)','Yalnızca seçtiğin görsel paylaşılır'] },
            profile: { icon:'👤', title:'Profil Fotoğrafı Güncelle', sub:'Profil Görseli',
                       desc:'Seçeceğin fotoğraf <strong class="text-white">profil resmin</strong> olarak ayarlanacak.',
                       items:['Tüm kullanıcılar profil fotoğrafını görebilir','Görsel otomatik kırpılır ve optimize edilir (400px)','Yalnızca seçtiğin görsel yüklenir'] },
            reel:    { icon:'🎬', title:'Reel Medya Seç',           sub:'Reel / Gönderi',
                       desc:'Seçeceğin fotoğraf veya video <strong class="text-white">reel olarak paylaşılacak</strong>.',
                       items:['Tüm topluluk üyeleri görebilir','Fotoğraflar optimize edilir, videolar maks. 50MB','Yalnızca seçtiğin dosya paylaşılır'] },
        };

        function _showPhotoDisclosure(context, onConfirm) {
            const cfg = _PD_PHOTO_CFG[context] || _PD_PHOTO_CFG.profile;
            document.getElementById('pd-photo-icon').textContent     = cfg.icon;
            document.getElementById('pd-photo-title').textContent    = cfg.title;
            document.getElementById('pd-photo-subtitle').textContent = cfg.sub;
            document.getElementById('pd-photo-desc').innerHTML       = cfg.desc;
            document.getElementById('pd-photo-list').innerHTML = cfg.items
                .map(t => `<li class="flex items-start gap-2"><span class="text-pink-400 shrink-0 mt-0.5">✔</span><span>${t}</span></li>`)
                .join('');
            const modal    = document.getElementById('pd-photo-modal');
            const allowBtn = document.getElementById('pd-photo-allow');
            const denyBtn  = document.getElementById('pd-photo-deny');
            modal.classList.remove('hidden');
            const cleanup = () => { allowBtn.removeEventListener('click', onAllow); denyBtn.removeEventListener('click', onDeny); };
            function onAllow() { modal.classList.add('hidden'); cleanup(); onConfirm(); }
            function onDeny()  { modal.classList.add('hidden'); cleanup(); }
            allowBtn.addEventListener('click', onAllow);
            denyBtn.addEventListener('click',  onDeny);
        }

        function openPhotoUpload(context) {
            currentPhotoContext = context;
            _showPhotoDisclosure(context, () => { document.getElementById("chat-photo-upload").click(); });
        }

        async function handleChatPhotoUpload(input) {
            if(!input.files[0]) return;
            const b64 = await resizeImage(input.files[0], 800);
            if(b64) {
                const id = Date.now().toString();
                if(currentPhotoContext === 'group') {
                    await sendAction('add_message', { id: id, photo: b64, type: "photo" });
                } else if(currentPhotoContext === 'dm' && currentDmUser) {
                    db.dms.push({ id: id, sender: currentUser.username, receiver: currentDmUser, participants: [currentUser.username, currentDmUser], photo: b64, type: 'photo' });
                    renderDmThread(currentDmUser);
                    await sendAction('send_dm', { id: id, photo: b64, receiver: currentDmUser, type: "photo" });
                }
            }
            input.value = "";
        }

        // ============================================================
        // PROMINENT DISCLOSURE — Mikrofon (Google Play uyumu)
        // getUserMedia() çağrısından ÖNCE kullanıcıya amaç gösterilir.
        // İzin zaten verildiyse modal atlanır, kayıt doğrudan başlar.
        // ============================================================
        async function toggleVoiceRecord(context) {
            if(getUserPremiumTier(currentUser.username) < 2) {
                return alert("Sesli mesaj gönderme özelliği Deluxe ve Ultra+ üyelerine özeldir!");
            }
            const btn = document.getElementById("voice-btn");

            // Aktif kayıt varsa durdur — disclosure gerektirmez
            // NOT: MediaRecorder.state değerleri: "inactive", "recording", "paused"
            // Önceki kodda "active" kullanılıyordu ki bu HİÇBİR ZAMAN true olmaz!
            if (mediaRecorder && mediaRecorder.state === "recording") {
                _voiceStopping = true;   // Blob işlenene kadar yeni kaydı engelle
                mediaRecorder.stop();
                // stop event handler içinde btn sıfırlanacak ve mediaRecorder = null yapılacak
                return;
            }

            // Blob henüz işleniyorsa (stop() sonrası kısa pencere) izin akışına düşme
            if (_voiceStopping) return;

            // İzin zaten verilmişse doğrudan kaydı başlat (modal gösterme)
            try {
                const perm = await navigator.permissions.query({ name: 'microphone' });
                if (perm.state === 'granted') { await _startVoiceCapture(context, btn); return; }
            } catch(_) { /* permissions API desteklenmiyor — modal göster */ }

            // Prominent Disclosure modal — sadece izin granted DEĞİLSE gösterilir
            const modal    = document.getElementById('pd-mic-modal');
            const allowBtn = document.getElementById('pd-mic-allow');
            const denyBtn  = document.getElementById('pd-mic-deny');
            modal.classList.remove('hidden');
            const cleanup = () => { allowBtn.removeEventListener('click', onAllow); denyBtn.removeEventListener('click', onDeny); };
            async function onAllow() { modal.classList.add('hidden'); cleanup(); await _startVoiceCapture(context, btn); }
            function onDeny()        { modal.classList.add('hidden'); cleanup(); }
            allowBtn.addEventListener('click', onAllow);
            denyBtn.addEventListener('click',  onDeny);
        }

        async function _startVoiceCapture(context, btn) {
            try {
                const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
                mediaRecorder = new MediaRecorder(stream);
                audioChunks = [];
                btn.className = "bg-red-600 w-10 h-10 md:w-12 md:h-12 rounded-xl text-lg flex items-center justify-center animate-pulse shadow-[0_0_20px_rgba(14,165,233,0.8)] border border-sky-400 transition-all";
                btn.innerHTML = "⏹️";
                mediaRecorder.addEventListener("dataavailable", ev => { audioChunks.push(ev.data); });
                mediaRecorder.addEventListener("stop", async () => {
                    // Ses verisini hazırla ve gönder
                    const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
                    const reader = new FileReader();
                    reader.readAsDataURL(audioBlob);
                    reader.onloadend = async function() {
                        const b64 = reader.result;
                        const id  = Date.now().toString();
                        if(context === 'group') await sendAction('add_message', { id, audio: b64, type: "voice" });
                    };
                    // Mikrofon stream'ini kapat
                    stream.getTracks().forEach(t => t.stop());
                    // Butonu sıfırla
                    btn.className = "bg-zinc-800/80 hover:bg-zinc-700 transition w-10 h-10 md:w-12 md:h-12 rounded-xl text-lg flex items-center justify-center border border-zinc-700 btn-premium-hover";
                    btn.innerHTML = "🎤";
                    // KRITIK: mediaRecorder'ı null yap ki sonraki tıklamada
                    // stale "inactive" state yüzünden yanlış dallanma olmasın
                    audioChunks = [];
                    mediaRecorder = null;
                    _voiceStopping = false; // Artık yeni kayda izin ver
                });
                // start() çağrısı event listener'lardan SONRA yapılmalı
                mediaRecorder.start();
            } catch(err) {
                console.error('Mikrofon hatası:', err);
                mediaRecorder = null;
                alert("Mikrofon izni alınamadı. Tarayıcı ayarlarından mikrofon iznini etkinleştir.");
            }
        }
        
        function playVoice(src) { const a = new Audio(src); a.play(); }

        // Premium modal animasyon yardımcısı
        function showModal(id) {
            const el = document.getElementById(id);
            if(!el) return;
            el.classList.remove('hidden');
            const inner = el.querySelector('.modal-inner, [class*="glass-panel"], [class*="bg-zinc"], [class*="bg-black"]');
            if(inner) {
                inner.style.animation = 'none';
                inner.offsetHeight;
                inner.style.animation = 'scaleInFade 0.32s cubic-bezier(0.34,1.56,0.64,1) both';
            }
        }
        function hideModal(id) {
            const el = document.getElementById(id);
            if(!el) return;
            el.classList.add('hidden');
        }

        function openSettingsModal() {
            document.getElementById("edit-name").value = currentUser.name || "";
            document.getElementById("edit-bio").value = currentUser.bio || "";
            document.getElementById("edit-password").value = "";
            
            const stats = currentUser.stats || {};
            document.getElementById("edit-email").value = stats.email || "";
            document.getElementById("edit-marketing").checked = stats.marketing_opt_in || false;
            
            const statusDiv = document.getElementById("profile-email-status");
            if(stats.email) {
                if(stats.email_verified) {
                    statusDiv.innerHTML = `<span class="bg-green-900/40 text-green-400 text-[10px] px-3 py-1.5 rounded-lg font-bold border border-green-800/50 shadow-sm uppercase tracking-widest inline-flex items-center gap-1"><span class="text-sm">✅</span> E-Posta Doğrulandı</span>`;
                } else {
                    statusDiv.innerHTML = `<span class="bg-yellow-900/40 text-yellow-500 text-[10px] px-3 py-1.5 rounded-lg font-bold border border-yellow-800/50 shadow-sm uppercase tracking-widest inline-flex items-center gap-1"><span class="text-sm">⚠️</span> E-Posta Doğrulanmadı</span>`;
                }
            } else {
                statusDiv.innerHTML = `<span class="bg-zinc-800 text-zinc-400 text-[10px] px-3 py-1.5 rounded-lg font-bold border border-zinc-700 uppercase tracking-widest inline-block">E-Posta Eklenmemiş</span>`;
            }

            checkEmailChange();
            document.getElementById("settings-modal").classList.remove("hidden");
        }

        function checkEmailChange() {
            const stats = currentUser.stats || {};
            const currentEmail = stats.email || "";
            const inputEmail = document.getElementById("edit-email").value.trim();
            const btn = document.getElementById("btn-verify-email");
            
            if (inputEmail !== "" && (inputEmail !== currentEmail || !stats.email_verified)) {
                btn.classList.remove("hidden");
            } else {
                btn.classList.add("hidden");
            }
        }

        function closeSettingsModal() { document.getElementById("settings-modal").classList.add("hidden"); }

        async function saveSettings() {
            const n = document.getElementById("edit-name").value;
            const b = document.getElementById("edit-bio").value;
            const p = document.getElementById("edit-password").value;
            
            const emailEl = document.getElementById("edit-email");
            const emailInput = emailEl ? emailEl.value.trim() : "";
            
            const stats = currentUser.stats || {};
            let emailChanged = false;
            
            const currentSavedEmail = (stats.email || "").trim().toLowerCase();
            const newEmailNorm = emailInput.toLowerCase();
            
            if (newEmailNorm !== currentSavedEmail && emailInput !== "") {
                // Gerçekten farklı bir email girildiyse değiştir
                emailChanged = true;
                stats.email = emailInput;
                stats.email_verified = false;
            } else if (emailInput === "") {
                // Email alanı boş bırakıldıysa mevcut emaili koru
                // stats.email değişmesin
            }
            // email aynıysa hiçbir şey yapma (email_verified korunur)

            if (p && p.trim() !== "") { 
                if (p.length < 4) return alert("Şifre en az 4 hane olmalı."); 
            }
            
            currentUser.name = n;
            currentUser.bio = b;
            
            const data = { username: currentUser.username, name: n, bio: b };
            if (p && p.trim() !== "") data.password = p;
            
            data.stats = stats;

            try {
                await sendAction('update_user', data);
                
                if (p && p.trim() !== "") {
                    if (localStorage.getItem("fr_remembered_username")) {
                        localStorage.setItem("fr_remembered_password", btoa(unescape(encodeURIComponent(p))));
                    }
                }

                currentUser.stats = stats;
                localStorage.setItem("fr_user", JSON.stringify(currentUser));

                updateProfileUI(); 
                
                if (emailChanged && emailInput !== "") {
                    alert("Profil güncellendi! E-posta adresiniz güncellendi ancak henüz ONAYLANMADI. 'Doğrulama Kodu Gönder' butonuyla e-postanızı onaylayın.");
                } else {
                    alert("Profil başarıyla güncellendi.");
                }
                closeSettingsModal(); 
            } catch(e) {
                alert("Hata oluştu: " + e.message);
            }
        }

        async function requestProfileEmailVerify() {
            const email = document.getElementById("edit-email").value.trim();
            const marketing = document.getElementById("edit-marketing").checked;
            if(!email) return alert("Lütfen bir e-posta adresi girin.");
            
            try {
                await sendAction('send_profile_verification', { email: email, marketing: marketing });
                
                document.getElementById("settings-modal").classList.add("hidden");
                verificationUsername = currentUser.username;
                
                document.getElementById("verify-code-input").value = ""; 
                document.getElementById("email-verify-modal").classList.remove("hidden");
                alert("Doğrulama kodu e-posta adresinize gönderildi!");
            } catch(e) { }
        }

        function openProfilePicUpload() {
            _showPhotoDisclosure('profile', () => { document.getElementById('pic-upload').click(); });
        }

        async function uploadProfilePic(input) {
            if(!input.files[0]) return;
            const b64 = await resizeImage(input.files[0], 400);
            if(b64) {
                currentUser.avatar = b64;
                await sendAction('update_user', { username: currentUser.username, avatar: b64 });
                updateProfileUI();
            }
        }

        // ==============================================================
        // READY PLAYER ME 3D AVATAR
        // ==============================================================
        function openRpmModal() {
            const modal = document.getElementById('rpm-modal');
            const iframe = document.getElementById('rpm-iframe');
            const loading = document.getElementById('rpm-loading');
            modal.classList.remove('hidden');
            loading.classList.remove('hidden');
            iframe.classList.add('hidden');
            // RPM partner subdomain — freeridertr için özel subdomain yoksa genel URL
            const rpmUrl = 'https://freeridertr.readyplayer.me/avatar?frameApi&clearCache';
            iframe.src = rpmUrl;
            iframe.onload = () => {
                loading.classList.add('hidden');
                iframe.classList.remove('hidden');
            };
        }

        function closeRpmModal() {
            const modal = document.getElementById('rpm-modal');
            const iframe = document.getElementById('rpm-iframe');
            modal.classList.add('hidden');
            iframe.src = '';
        }

        // RPM iframe'den mesaj dinle — avatar URL'i gelince kaydet
        window.addEventListener('message', async (event) => {
            if(!event.data || typeof event.data !== 'string') return;
            // RPM, avatar URL'ini JSON veya düz string olarak gönderir
            let avatarUrl = null;
            try {
                const parsed = JSON.parse(event.data);
                if(parsed.source === 'readyplayerme' && parsed.eventName === 'v1.avatar.exported') {
                    avatarUrl = parsed.data?.url;
                }
            } catch(e) {
                // Bazı sürümlerde düz URL gelir
                if(typeof event.data === 'string' && event.data.includes('models.readyplayer.me')) {
                    avatarUrl = event.data;
                }
            }
            if(avatarUrl && currentUser) {
                // PNG render URL'i oluştur (fullbody portrait)
                const renderUrl = avatarUrl.replace('.glb', '.png') + '?scene=fullbody-portrait-v1-transparent&background=transparent&quality=100';
                closeRpmModal();
                // Kaydet
                currentUser.avatar = renderUrl;
                document.getElementById('profile-avatar').src = renderUrl;
                try {
                    await sendAction('update_user', { username: currentUser.username, avatar: renderUrl });
                    localStorage.setItem("fr_user", JSON.stringify(currentUser));
                    updateProfileUI();
                    haptic([50, 30, 100]);
                    // Küçük kutlama toast
                    const t = document.createElement('div');
                    t.className = 'fixed top-20 left-1/2 -translate-x-1/2 z-[99999] bg-gradient-to-r from-purple-600 to-indigo-600 text-white px-6 py-3 rounded-2xl font-bold text-sm shadow-2xl flex items-center gap-3 scale-in-anim';
                    t.innerHTML = '<span style="font-size:20px">🎭</span><div><div style="font-size:10px;opacity:0.8;text-transform:uppercase;letter-spacing:0.1em">Avatar Kaydedildi!</div><div>3D avatarın profile eklendi</div></div>';
                    document.body.appendChild(t);
                    setTimeout(() => { t.style.opacity='0'; t.style.transition='opacity 0.5s'; setTimeout(()=>t.remove(),500); }, 3000);
                } catch(e) { alert('Avatar kaydedilemedi: ' + e.message); }
            }
        });

        async function acceptChatRules() {
            await sendAction('accept_chat_rules', {});
            currentUser.accepted_chat_rules = true;
            document.getElementById("chat-rules-modal").classList.add("hidden");
            alert("Kuralları kabul ettiniz, sisteme hoş geldiniz.");
        }

        // ===============================================================
        // GELİŞMİŞ ADMİN PANELİ - TAM SİSTEM
        // ===============================================================
        let _currentAdminTab = 'overview';
        let _uaCurrentUser = null;
        let _uaCurrentTab = 'messages';
        let _uaActivityData = null;

        function showAdminPanel() {
            const isMainAdmin = (currentUser && (currentUser.role === 'Admin' || currentUser.username === 'Admin' || currentUser.username.toLowerCase() === 'admin'));
            const isSubAdmin  = (currentUser && currentUser.role === 'SubAdmin');

            // Role label
            const roleTag = document.getElementById('admin-panel-role-tag');
            if(roleTag) roleTag.textContent = isMainAdmin ? '👑 Ana Yönetici' : '🛡️ Yardımcı Yönetici';

            // Ana admin only elements
            document.querySelectorAll('.admin-main-only').forEach(el => {
                el.style.display = isMainAdmin ? '' : 'none';
            });
            document.querySelectorAll('.admin-sub-only').forEach(el => {
                el.style.display = isSubAdmin ? '' : 'none';
            });

            // Ekip tab: sadece main admin
            const tabAdmins = document.getElementById('atab-admins');
            if(tabAdmins) tabAdmins.style.display = isMainAdmin ? '' : 'none';

            // Stats güncelle
            document.getElementById('astat-users').textContent = db.users.length;
            document.getElementById('astat-banned').textContent = db.banned.length;

            // Maintenance
            const maintChk = document.getElementById("admin-maintenance");
            if(maintChk) maintChk.checked = db.maintenance;

            // Google Play IAP — Bekleyen manuel onay listesi (main admin only)
            // NOT: Google Play IAP akışında satın alımlar /api/verify_google_purchase
            // üzerinden otomatik doğrulanır. Bu panel yalnızca otomatik doğrulaması
            // başarısız olan veya admin tarafından manuel onay gerektiren durumları gösterir.
            if(isMainAdmin) {
                const reqContainer = document.getElementById("admin-iap-requests");
                reqContainer.innerHTML = "";
                let hasReqs = false;
                db.users.forEach(u => {
                    // pending_premium: otomatik doğrulaması tamamlanamamış IAP'lar
                    if(u.stats && u.stats.pending_premium) {
                        hasReqs = true;
                        const tierNum = parseInt(u.stats.pending_premium);
                        const productId = u.stats.gp_product_id || '—';
                        const pName = tierNum === 3 ? "👑 Ultra+" : (tierNum === 2 ? "🌟 Deluxe" : "⭐ Standart");
                        const isAdminOverride = u.stats.gp_admin_override ? ' (Manuel)' : ' (IAP)';
                        reqContainer.innerHTML += `
                        <div class="rounded-xl p-3 border border-zinc-700/60 flex justify-between items-center admin-card-enter" style="background:rgba(0,0,0,0.5)">
                            <div>
                                <div class="font-bold text-white text-sm">${u.username}</div>
                                <div class="text-[10px] text-yellow-400 font-bold uppercase tracking-widest mt-0.5">${pName}${isAdminOverride}</div>
                                <div class="text-[9px] text-zinc-500 mt-0.5">Product: ${productId}</div>
                            </div>
                            <div class="flex gap-2">
                                <button onclick="approvePrem('${u.username}', ${tierNum})" class="bg-green-800/80 hover:bg-green-700 px-3 py-2 rounded-lg text-[10px] font-bold text-white transition">✓ Onayla</button>
                                <button onclick="rejectPrem('${u.username}')" class="bg-red-900/60 hover:bg-red-800/80 px-3 py-2 rounded-lg text-[10px] font-bold text-white transition">✕ Red</button>
                            </div>
                        </div>`;
                    }
                });
                if(!hasReqs) reqContainer.innerHTML = "<div class='text-zinc-600 text-xs italic py-1 font-medium'>✅ Bekleyen IAP onayı yok.</div>";
            }

            adminSwitchTab('overview');
            document.getElementById("admin-panel").classList.remove("hidden");

            // Load sub-admin count for stats
            loadSubAdminCount();
        }

        async function loadSubAdminCount() {
            try {
                const res = await sendAction('get_all_sub_admins', {});
                if(res && res.sub_admins) {
                    const el = document.getElementById('astat-admins');
                    if(el) { el.textContent = res.sub_admins.length; el.classList.add('count-up-anim'); }
                }
            } catch(e) {}
        }

        function adminSwitchTab(tab) {
            _currentAdminTab = tab;
            ['overview','users','commands','reports','reels','logs','admins'].forEach(t => {
                const btn = document.getElementById(`atab-${t}`);
                const content = document.getElementById(`admin-tab-${t}`);
                if(btn) btn.className = btn.className.replace(' active-admin-tab','').replace('active-admin-tab','') + (t === tab ? ' active-admin-tab' : '');
                if(content) content.classList.toggle('hidden', t !== tab);
            });
            if(tab === 'users') loadAllUsersForAdmin();
            if(tab === 'reports') loadAdminReports();
            if(tab === 'reels') loadAdminReels();
            if(tab === 'logs') loadAdminLogs();
            if(tab === 'admins') loadSubAdmins();
        }

        let _adminAllUsers = [];
        let _adminUserPage = 1;
        let _adminUserTotal = 0;

        async function loadAllUsersForAdmin(page = 1, search = '') {
            const container = document.getElementById('admin-user-list');
            if(!container) return;
            container.innerHTML = '<div class="text-center text-zinc-500 py-4 text-xs animate-pulse">Kullanıcılar yükleniyor...</div>';
            try {
                const res = await sendAction('get_all_users_admin', { page: page, per_page: 200, search: search });
                if (res && res.users) {
                    _adminAllUsers = res.users;
                    _adminUserPage = res.page || 1;
                    _adminUserTotal = res.total || res.users.length;
                    renderAdminUserList(res.users);
                    // Toplam kullanıcı sayısını stats'a yansıt
                    const statEl = document.getElementById('astat-users');
                    if(statEl) statEl.textContent = _adminUserTotal;
                } else {
                    renderAdminUserList(db.users);
                }
            } catch(e) {
                console.warn('Admin kullanıcı listesi yüklenemedi, fallback:', e);
                renderAdminUserList(db.users);
            }
        }

        function renderAdminUserList(users) {
            const container = document.getElementById('admin-user-list');
            if(!container) return;
            container.innerHTML = '';

            // Pagination info
            if(_adminUserTotal > 0) {
                container.innerHTML += `<div class="text-[10px] text-zinc-500 font-bold uppercase tracking-widest mb-2 px-1">Toplam: ${_adminUserTotal} kullanıcı (Sayfa ${_adminUserPage})</div>`;
            }

            (users || []).forEach((u, i) => {
                const isBanned = db.banned.includes(u.username);
                const premTier = (u.stats && u.stats.premium_tier) ? parseInt(u.stats.premium_tier) : 0;
                const roleLabel = u.role === 'Admin' ? '👑' : (u.role === 'SubAdmin' ? '🛡️' : '');
                const premBadge = premTier === 3 ? '<span class="text-yellow-400 text-[8px] font-black">ULTRA+</span>' : (premTier === 2 ? '<span class="text-purple-400 text-[8px] font-black">DLX</span>' : (premTier === 1 ? '<span class="text-blue-400 text-[8px] font-black">STD</span>' : ''));
                container.innerHTML += `
                <div class="rounded-xl p-3 border flex items-center gap-3 admin-card-enter transition-all hover:border-zinc-600 cursor-pointer" style="background:rgba(0,0,0,0.45);border-color:rgba(63,63,70,0.7);animation-delay:${i*0.03}s" onclick="openUserActivity('${u.username}')">
                    <img src="${u.avatar || 'https://cdn.freeridertr.com.tr/profil%20resmi/unnamed.jpg'}" class="w-10 h-10 rounded-full object-cover shrink-0 border-2 ${isBanned ? 'border-sky-600' : 'border-zinc-700'}">
                    <div class="flex-1 min-w-0">
                        <div class="flex items-center gap-1.5">
                            <span class="text-white font-bold text-sm truncate">${u.username}</span>
                            <span>${roleLabel}</span>
                            ${premBadge}
                            ${isBanned ? '<span class="ban-reason-badge">Banlı</span>' : ''}
                        </div>
                        <div class="text-zinc-500 text-[10px] font-bold truncate mt-0.5">${u.city || '—'} · ${u.xp || 0} XP</div>
                    </div>
                    <div class="shrink-0 text-zinc-600 text-xs">›</div>
                </div>`;
            });
            if(!users || users.length === 0) container.innerHTML = '<div class="text-zinc-600 text-xs italic text-center py-4">Kullanıcı bulunamadı.</div>';
        }

        function adminSearchUsers() {
            const q = document.getElementById('admin-user-search').value.toLowerCase().trim();
            const filtered = q ? db.users.filter(u => u.username.toLowerCase().includes(q) || (u.city||'').toLowerCase().includes(q)) : db.users;
            renderAdminUserList(filtered);
        }

        async function loadAdminReels() {
            const container = document.getElementById('admin-reels-list');
            if(!container) return;
            container.innerHTML = '<div class="text-zinc-600 text-xs italic text-center py-4 animate-pulse">Yükleniyor...</div>';
            try {
                const res = await sendAction('get_reels', {offset: 0});
                const reels = (res && res.reels) ? res.reels : [];
                container.innerHTML = '';
                if(!reels.length) { container.innerHTML = '<div class="text-zinc-600 text-xs italic text-center py-4">Reel bulunamadı.</div>'; return; }
                reels.forEach((r, i) => {
                    const isVideo = r.media_type === 'video';
                    const dt = r.created_at ? new Date(r.created_at * 1000).toLocaleDateString('tr-TR') : '—';
                    container.innerHTML += `
                    <div class="rounded-xl p-3 border border-zinc-800/70 flex items-center gap-3 admin-card-enter" style="background:rgba(0,0,0,0.5);animation-delay:${i*0.04}s">
                        <div class="w-14 h-14 rounded-xl overflow-hidden shrink-0 border border-zinc-700 bg-zinc-900 flex items-center justify-center">
                            ${isVideo ? `<span class="text-2xl">🎥</span>` : `<img src="${r.media_url}" class="w-full h-full object-cover">`}
                        </div>
                        <div class="flex-1 min-w-0">
                            <div class="text-white font-bold text-sm truncate">${r.user}</div>
                            <div class="text-zinc-500 text-[10px] font-bold mt-0.5 truncate">${r.caption || '(Açıklama yok)'}</div>
                            <div class="flex items-center gap-2 mt-1">
                                <span class="text-zinc-600 text-[9px] font-bold">${dt}</span>
                                <span class="text-pink-500 text-[9px] font-bold">❤ ${(r.likes||[]).length}</span>
                                <span class="text-zinc-500 text-[9px] font-bold">${isVideo ? '🎥 Video' : '📸 Foto'}</span>
                            </div>
                        </div>
                        <button onclick="adminDeleteReel('${r.id}', '${r.user}', this)" class="shrink-0 w-8 h-8 rounded-lg bg-red-900/40 border border-sky-800/50 text-sky-300 hover:bg-sky-800/60 flex items-center justify-center text-sm transition hover:scale-110">🗑</button>
                    </div>`;
                });
            } catch(e) {
                container.innerHTML = '<div class="text-sky-400 text-xs italic text-center py-4">Yüklenirken hata oluştu.</div>';
            }
        }

        async function adminDeleteReel(reelId, owner, btn) {
            if(!confirm(`${owner} adlı kullanıcının reelini silmek istediğine emin misin?`)) return;
            btn.disabled = true; btn.textContent = '...';
            const res = await sendAction('delete_reel', {reel_id: reelId});
            if(res && res.status === 'ok') {
                btn.closest('.rounded-xl').style.opacity = '0.3';
                btn.textContent = '✓';
                showToast(`🗑️ Reel silindi.`);
            }
        }

        async function loadAdminLogs() {
            const container = document.getElementById('admin-logs-list');
            if(!container) return;
            container.innerHTML = '<div class="text-zinc-600 text-xs italic text-center py-4 animate-pulse">Yükleniyor...</div>';
            try {
                const res = await sendAction('get_admin_logs', {});
                const logs = (res && res.logs) ? res.logs : [];
                container.innerHTML = '';
                if(!logs.length) { container.innerHTML = '<div class="text-zinc-600 text-xs italic text-center py-4">Henüz kayıt yok.</div>'; return; }
                const actionColors = { ban_user: 'log-ban', delete_reel: 'log-delete', delete_message: 'log-delete', delete_marker: 'log-delete', assign_admin: 'log-assign', revoke_admin: 'log-revoke', notify_main: 'log-notify' };
                const actionEmojis = { ban_user: '🚨', delete_reel: '🎬', delete_message: '💬', delete_marker: '📍', assign_admin: '✅', revoke_admin: '❌', notify_main: '📢' };
                logs.forEach((l, i) => {
                    const colorClass = actionColors[l.action] || 'log-default';
                    const emoji = actionEmojis[l.action] || '🔧';
                    const dt = l.ts ? new Date(l.ts * 1000).toLocaleString('tr-TR') : '—';
                    container.innerHTML += `
                    <div class="rounded-xl p-3 pl-4 admin-card-enter ${colorClass}" style="background:rgba(0,0,0,0.5);animation-delay:${i*0.03}s">
                        <div class="flex items-center justify-between gap-2">
                            <div class="flex items-center gap-2 min-w-0">
                                <span class="text-sm shrink-0">${emoji}</span>
                                <div class="min-w-0">
                                    <div class="text-white text-xs font-bold"><span class="text-red-300">${l.admin}</span> → <span class="text-zinc-300">${l.target || '—'}</span></div>
                                    <div class="text-zinc-500 text-[10px] font-bold truncate mt-0.5">${l.detail || l.action}</div>
                                </div>
                            </div>
                            <div class="text-zinc-600 text-[9px] font-bold shrink-0">${dt}</div>
                        </div>
                    </div>`;
                });
            } catch(e) {
                container.innerHTML = '<div class="text-sky-400 text-xs italic text-center py-4">Yüklenirken hata oluştu.</div>';
            }
        }

        async function loadSubAdmins() {
            const container = document.getElementById('sub-admin-list');
            if(!container) return;
            container.innerHTML = '<div class="text-zinc-600 text-xs italic text-center py-3 animate-pulse">Yükleniyor...</div>';
            try {
                const res = await sendAction('get_all_sub_admins', {});
                const admins = (res && res.sub_admins) ? res.sub_admins : [];
                const el2 = document.getElementById('astat-admins');
                if(el2) el2.textContent = admins.length;
                container.innerHTML = '';
                if(!admins.length) { container.innerHTML = '<div class="text-zinc-600 text-xs italic text-center py-3">Henüz yardımcı admin yok.</div>'; return; }
                admins.forEach((a, i) => {
                    container.innerHTML += `
                    <div class="flex items-center gap-3 p-2.5 rounded-xl admin-card-enter" style="background:rgba(0,0,0,0.4);animation-delay:${i*0.05}s">
                        <img src="${a.avatar || 'https://cdn.freeridertr.com.tr/profil%20resmi/unnamed.jpg'}" class="w-9 h-9 rounded-full object-cover border border-amber-700/60">
                        <div class="flex-1 min-w-0">
                            <div class="text-amber-300 font-bold text-sm truncate">${a.username}</div>
                            <div class="text-zinc-600 text-[10px] font-bold">${a.xp || 0} XP</div>
                        </div>
                        <button onclick="quickRevokeAdmin('${a.username}', this)" class="shrink-0 px-3 py-1.5 rounded-lg bg-sky-900/30 border border-sky-800/50 text-sky-300 hover:bg-sky-800/50 text-[10px] font-bold transition">Yetkiyi Al</button>
                    </div>`;
                });
            } catch(e) {
                container.innerHTML = '<div class="text-sky-400 text-xs italic text-center py-3">Yüklenirken hata oluştu.</div>';
            }
        }

        async function assignSubAdmin() {
            const uname = document.getElementById('assign-admin-username').value.trim();
            if(!uname) { showToast('Kullanıcı adı gir!'); return; }
            if(!confirm(`${uname} adlı kullanıcıya yardımcı admin yetkisi verilecek. Emin misin?`)) return;
            const res = await sendAction('assign_sub_admin', {username: uname});
            if(res && res.status === 'ok') {
                showToast(`✅ ${uname} artık yardımcı admin!`);
                document.getElementById('assign-admin-username').value = '';
                loadSubAdmins();
            } else {
                alert(res?.message || 'Hata oluştu.');
            }
        }

        async function revokeSubAdmin() {
            const uname = document.getElementById('revoke-admin-username').value.trim();
            if(!uname) { showToast('Kullanıcı adı gir!'); return; }
            if(!confirm(`${uname} adlı kullanıcının admin yetkisi alınacak. Emin misin?`)) return;
            const res = await sendAction('revoke_sub_admin', {username: uname});
            if(res && res.status === 'ok') {
                showToast(`❌ ${uname} yetkisi alındı.`);
                document.getElementById('revoke-admin-username').value = '';
                loadSubAdmins();
            } else {
                alert(res?.message || 'Hata oluştu.');
            }
        }

        async function quickRevokeAdmin(uname, btn) {
            if(!confirm(`${uname} yöneticilikten çıkarılsın mı?`)) return;
            btn.disabled = true; btn.textContent = '...';
            const res = await sendAction('revoke_sub_admin', {username: uname});
            if(res && res.status === 'ok') {
                btn.closest('.rounded-xl').style.opacity = '0.3';
                showToast(`❌ ${uname} yetkisi alındı.`);
                loadSubAdmins();
            }
        }

        async function adminNotifyMain() {
            const msg = document.getElementById('admin-notify-msg').value.trim();
            if(!msg) { showToast('Mesaj boş olamaz!'); return; }
            const res = await sendAction('admin_notify_main', {message: msg});
            if(res && res.status === 'ok') {
                document.getElementById('admin-notify-msg').value = '';
                showToast('📨 Ana admine bildirim gönderildi!');
            }
        }

        // ---- Kullanıcı Aktivite Modalı ----
        async function openUserActivity(username) {
            _uaCurrentUser = username;
            _uaActivityData = null;
            document.getElementById('ua-username-label').textContent = '@' + username;
            document.getElementById('ua-content').innerHTML = '<div class="text-zinc-600 text-xs italic text-center py-6 animate-pulse">Yükleniyor...</div>';
            document.getElementById('user-activity-modal').classList.remove('hidden');
            uaTab('messages');

            try {
                const res = await sendAction('get_user_activity', {username});
                if(res && res.activity) {
                    _uaActivityData = res.activity;
                    uaRender(_uaCurrentTab);
                }
            } catch(e) {
                document.getElementById('ua-content').innerHTML = '<div class="text-sky-300 text-xs italic text-center py-6">Yüklenirken hata oluştu.</div>';
            }
        }

        function uaTab(tab) {
            _uaCurrentTab = tab;
            ['messages','dms','reels','markers','manage'].forEach(t => {
                const btn = document.getElementById(`uatab-${t}`);
                if(btn) {
                    btn.className = btn.className.replace(' ua-active-tab','').replace('ua-active-tab','');
                    if(t === tab) btn.className += ' ua-active-tab';
                }
            });
            if(_uaActivityData) uaRender(tab);
        }

        function uaRender(tab) {
            const container = document.getElementById('ua-content');
            if(!container || !_uaActivityData) return;
            const data_ua = _uaActivityData[tab] || [];
            container.innerHTML = '';
            if(!data_ua.length && tab !== 'manage') {
                container.innerHTML = `<div class="text-zinc-600 text-xs italic text-center py-6">Bu kategoride içerik yok.</div>`;
                return;
            }
            if(tab === 'manage') {
                const isMainAdmin = (currentUser && (currentUser.role === 'Admin' || currentUser.username === 'Admin' || currentUser.username.toLowerCase() === 'admin'));
                if(!isMainAdmin) {
                    container.innerHTML = `<div class="text-zinc-600 text-xs italic text-center py-6">Bu sekmeye erişim yetkiniz yok.</div>`;
                    return;
                }
                const targetUser = db.users.find(u => u.username === _uaCurrentUser) || {username: _uaCurrentUser};
                const stat = targetUser.stats ? (typeof targetUser.stats === 'string' ? JSON.parse(targetUser.stats) : targetUser.stats) : {};
                const premTier = stat.premium_tier || 0;
                let premText = "Premium Yok";
                if(premTier === 1) premText = "Standart";
                if(premTier === 2) premText = "Deluxe";
                if(premTier === 3) premText = "Ultra+";

                container.innerHTML = `
                <div class="space-y-3">
                    <div class="p-4 rounded-xl border border-zinc-800" style="background:rgba(0,0,0,0.4)">
                        <div class="text-[10px] text-zinc-500 uppercase font-bold tracking-widest mb-3">Kullanıcı Detayları</div>
                        <div class="text-xs text-white mb-1"><span class="text-zinc-400">Şehir:</span> ${targetUser.city || 'Bilinmiyor'}</div>
                        <div class="text-xs text-white mb-1"><span class="text-zinc-400">XP:</span> ${targetUser.xp || 0}</div>
                        <div class="text-xs text-white mb-1"><span class="text-zinc-400">Rol:</span> ${targetUser.role || 'User'}</div>
                        <div class="text-xs text-white mb-3"><span class="text-zinc-400">Premium:</span> <span class="text-yellow-400 font-bold">${premText}</span></div>
                    </div>
                    <div class="p-4 rounded-xl border border-amber-900/30" style="background:rgba(120,53,15,0.1)">
                        <div class="text-[10px] text-amber-500 uppercase font-bold tracking-widest mb-3">Üyelik / Premium İşlemleri</div>
                        <div class="grid grid-cols-2 gap-2 mb-2">
                            <button onclick="execAdminCmd('${targetUser.username} standart gönder')" class="py-2 bg-blue-900/40 text-blue-300 text-[10px] font-bold rounded shadow-md hover:bg-blue-800/50 transition border border-blue-800/50">+ Standart Ver</button>
                            <button onclick="execAdminCmd('${targetUser.username} deluxe gönder')" class="py-2 bg-purple-900/40 text-purple-300 text-[10px] font-bold rounded shadow-md hover:bg-purple-800/50 transition border border-purple-800/50">+ Deluxe Ver</button>
                            <button onclick="execAdminCmd('${targetUser.username} ultra gönder')" class="py-2 bg-yellow-900/40 text-yellow-300 text-[10px] font-bold rounded shadow-md hover:bg-yellow-800/50 transition border border-yellow-800/50">+ Ultra+ Ver</button>
                            <button onclick="execAdminCmd('${targetUser.username} standart geri çek')" class="py-2 bg-red-900/40 text-red-300 text-[10px] font-bold rounded shadow-md hover:bg-red-800/50 transition border border-red-800/50">❌ Süre Sil</button>
                        </div>
                        <div class="text-[9px] text-zinc-500 font-bold">Not: Zaten premiumu varsa 'Ver' diyerek süresini uzatabilirsiniz.</div>
                    </div>
                    <div class="p-4 rounded-xl border border-zinc-800" style="background:rgba(0,0,0,0.4)">
                        <div class="text-[10px] text-zinc-500 uppercase font-bold tracking-widest mb-3">Tehlikeli İşlemler</div>
                        <div class="space-y-2">
                            <button onclick="adminResetPassword('${targetUser.username}')" class="w-full py-2 bg-zinc-800 text-zinc-300 text-xs font-bold rounded hover:bg-zinc-700 transition">🔑 Şifre Sıfırla (Rastgele)</button>
                            <button onclick="adminChangeUsername('${targetUser.username}')" class="w-full py-2 bg-zinc-800 text-zinc-300 text-xs font-bold rounded hover:bg-zinc-700 transition">✏️ İsim Değiştir</button>
                            <button onclick="adminDeleteUser('${targetUser.username}')" class="w-full py-2 bg-red-950/50 border border-sky-900/50 text-sky-400 text-xs font-bold rounded hover:bg-sky-900/40 transition">🗑️ Hesabı Kalıcı Sil</button>
                        </div>
                    </div>
                </div>`;
                return;
            }
            if(tab === 'messages') {
                data_ua.forEach((m, i) => {
                    const txt = m.text ? String(m.text).substring(0,120) : (m.type || '?');
                    container.innerHTML += `
                    <div class="rounded-xl p-3 border border-zinc-800/70 flex items-start gap-2 admin-card-enter" style="background:rgba(0,0,0,0.45);animation-delay:${i*0.03}s">
                        <div class="flex-1 min-w-0">
                            <div class="text-zinc-300 text-xs font-medium">${txt}</div>
                            ${m.image ? `<div class="text-[9px] text-zinc-600 mt-1">📸 Görsel içerik</div>` : ''}
                        </div>
                        <button onclick="adminDelMsg('${m.id}', this)" class="shrink-0 w-7 h-7 bg-sky-900/30 border border-red-800/40 rounded-lg text-sky-300 hover:bg-sky-800/50 flex items-center justify-center text-[10px] transition">🗑</button>
                    </div>`;
                });
            } else if(tab === 'dms') {
                data_ua.forEach((m, i) => {
                    const others = (m.participants || []).filter(p => p !== _uaCurrentUser);
                    const txt = m.text ? String(m.text).substring(0,100) : (m.type || '?');
                    container.innerHTML += `
                    <div class="rounded-xl p-3 border border-zinc-800/70 admin-card-enter" style="background:rgba(0,0,0,0.45);animation-delay:${i*0.03}s">
                        <div class="text-[10px] text-zinc-500 font-bold mb-1">↔ ${others.join(', ') || '?'}</div>
                        <div class="text-zinc-300 text-xs font-medium">${txt}</div>
                    </div>`;
                });
            } else if(tab === 'reels') {
                data_ua.forEach((r, i) => {
                    const isVideo = r.media_type === 'video';
                    container.innerHTML += `
                    <div class="rounded-xl p-3 border border-zinc-800/70 flex items-center gap-3 admin-card-enter" style="background:rgba(0,0,0,0.45);animation-delay:${i*0.04}s">
                        <div class="w-12 h-12 rounded-lg overflow-hidden shrink-0 bg-zinc-900 border border-zinc-800 flex items-center justify-center">
                            ${isVideo ? `<span class="text-xl">🎥</span>` : `<img src="${r.media_url}" class="w-full h-full object-cover" onerror="this.parentElement.innerHTML='📸'">`}
                        </div>
                        <div class="flex-1 min-w-0">
                            <div class="text-zinc-300 text-xs font-medium truncate">${r.caption || '(Açıklama yok)'}</div>
                            <div class="text-pink-400 text-[9px] font-bold mt-0.5">❤ ${(r.likes||[]).length}</div>
                        </div>
                        <button onclick="adminDeleteReel('${r.id}','${r.user}',this)" class="shrink-0 w-7 h-7 bg-sky-900/30 border border-red-800/40 rounded-lg text-sky-300 hover:bg-sky-800/50 flex items-center justify-center text-[10px] transition">🗑</button>
                    </div>`;
                });
            } else if(tab === 'markers') {
                data_ua.forEach((m, i) => {
                    container.innerHTML += `
                    <div class="rounded-xl p-3 border border-zinc-800/70 flex items-center gap-3 admin-card-enter" style="background:rgba(0,0,0,0.45);animation-delay:${i*0.04}s">
                        <div class="w-10 h-10 rounded-lg bg-sky-900/30 border border-red-800/40 flex items-center justify-center text-xl shrink-0">${m.icon_type || '🚴'}</div>
                        <div class="flex-1 min-w-0">
                            <div class="text-white text-sm font-bold truncate">${m.name || '—'}</div>
                            <div class="text-zinc-500 text-[10px] font-bold">${m.difficulty || '—'}</div>
                        </div>
                        <button onclick="adminDelMarker('${m.id}','${m.name}',this)" class="shrink-0 w-7 h-7 bg-sky-900/30 border border-red-800/40 rounded-lg text-sky-300 hover:bg-sky-800/50 flex items-center justify-center text-[10px] transition">🗑</button>
                    </div>`;
                });
            }
        }

        async function adminDelMsg(msgId, btn) {
            if(!confirm('Bu mesajı silmek istediğine emin misin?')) return;
            btn.disabled = true; btn.textContent = '...';
            const res = await sendAction('admin_delete_message_by_id', {msg_id: msgId});
            if(res && res.status === 'ok') {
                btn.closest('.rounded-xl').style.opacity = '0.2';
                showToast('💬 Mesaj silindi.');
            }
        }

        async function adminDelMarker(markerId, markerName, btn) {
            if(!confirm(`"${markerName}" yerini silmek istediğine emin misin?`)) return;
            btn.disabled = true; btn.textContent = '...';
            const res = await sendAction('admin_delete_marker_by_id', {marker_id: markerId});
            if(res && res.status === 'ok') {
                btn.closest('.rounded-xl').style.opacity = '0.2';
                showToast('📍 Yer silindi.');
            }
        }

        async function adminBanFromActivity() {
            if(!_uaCurrentUser) return;
            const reason = prompt(`${_uaCurrentUser} adlı kullanıcıyı banlamak için sebep gir:`);
            if(!reason) return;
            const res = await sendAction('admin_ban_user', {username: _uaCurrentUser, reason});
            if(res && res.status === 'ok') {
                db.banned.push(_uaCurrentUser);
                document.getElementById('user-activity-modal').classList.add('hidden');
                showToast(`🚨 ${_uaCurrentUser} banlandı.`);
                document.getElementById('astat-banned').textContent = db.banned.length;
            }
        }

        async function approvePrem(u, tier) { await sendAction('admin_approve_premium', {username: u, tier: tier}); showToast('✅ Abonelik onaylandı!'); showAdminPanel(); }
        async function rejectPrem(u) { await sendAction('admin_reject_premium', {username: u}); showToast('❌ Abonelik reddedildi.'); showAdminPanel(); }
        async function toggleMaintenance() { const chk = document.getElementById("admin-maintenance").checked; await sendAction('toggle_maintenance', {status: chk}); showToast(chk ? '🔧 Bakım modu açıldı' : '✅ Bakım modu kapatıldı'); }
        async function delMsg(id) { if(confirm("Mesajı sil?")) { await sendAction('delete_message', {id: id}); db.messages = db.messages.filter(m=>m.id!==id); renderChat(true); } }
        async function pinMsg(id) {
            const m = db.messages.find(x => x.id === id);
            if(m && m.type === "text") {
                await sendAction('pin_message', { text: m.text, user: m.user, expires: Date.now() + (24*60*60*1000) });
                showToast('📌 Mesaj 24 saat sabitlendi!');
            }
        }

        // ==== 3D ÇARK MOTORU ====
        let _wheelAngle = 0;
        let _wheelSpinning = false;
        let _winnerIndex = -1;

        function initWheel3D() {
            const canvas = document.getElementById('wheel-canvas-3d');
            if(!canvas) return;
            _winnerIndex = -1;
            _drawWheel3D(canvas, _wheelAngle);
        }

        function _drawWheel3D(canvas, angle) {
            const ctx = canvas.getContext('2d');
            const W = canvas.width, H = canvas.height;
            const cx = W/2, cy = H/2;
            const R = W/2 - 6;
            const prizes = window.WHEEL_PRIZES || [];
            const n = prizes.length;
            if(n === 0) return;
            const slice = (Math.PI * 2) / n;
            ctx.clearRect(0, 0, W, H);

            // Dış parlak halka
            const glowGrd = ctx.createRadialGradient(cx,cy,R-4,cx,cy,R+8);
            glowGrd.addColorStop(0,'rgba(234,179,8,0.0)');
            glowGrd.addColorStop(1,'rgba(234,179,8,0.35)');
            ctx.beginPath(); ctx.arc(cx,cy,R+6,0,Math.PI*2);
            ctx.fillStyle=glowGrd; ctx.fill();

            // Dilimleri çiz
            prizes.forEach((p, i) => {
                // İbre saat 12'de (üstte) → -Math.PI/2 offset
                const startA = angle + i * slice - Math.PI/2;
                const endA = startA + slice;
                const mid = startA + slice/2;

                const isWinner = (_winnerIndex === i);
                const baseColor = p.color || '#0ea5e9';

                // Dilim
                ctx.beginPath();
                ctx.moveTo(cx, cy);
                ctx.arc(cx, cy, R, startA, endA);
                ctx.closePath();
                if(isWinner) {
                    const winGrd = ctx.createRadialGradient(
                        cx + Math.cos(mid)*R*0.5, cy + Math.sin(mid)*R*0.5, 0,
                        cx + Math.cos(mid)*R*0.5, cy + Math.sin(mid)*R*0.5, R*0.7
                    );
                    winGrd.addColorStop(0,'#fffde7');
                    winGrd.addColorStop(0.5,'#fbbf24');
                    winGrd.addColorStop(1,'#b45309');
                    ctx.fillStyle = winGrd;
                } else {
                    ctx.fillStyle = baseColor;
                }
                ctx.fill();
                // Kenarlık
                ctx.strokeStyle = isWinner ? '#fbbf24' : 'rgba(0,0,0,0.35)';
                ctx.lineWidth = isWinner ? 4 : 1.5;
                ctx.stroke();

                // Parlaklık efekti
                const shineGrd = ctx.createRadialGradient(
                    cx + Math.cos(mid)*R*0.4, cy + Math.sin(mid)*R*0.4, 0,
                    cx + Math.cos(mid)*R*0.4, cy + Math.sin(mid)*R*0.4, R*0.6
                );
                shineGrd.addColorStop(0,'rgba(255,255,255,0.20)');
                shineGrd.addColorStop(1,'rgba(0,0,0,0.0)');
                ctx.beginPath();
                ctx.moveTo(cx,cy);
                ctx.arc(cx,cy,R,startA,endA);
                ctx.closePath();
                ctx.fillStyle = shineGrd;
                ctx.fill();

                // Metin
                ctx.save();
                ctx.translate(cx + Math.cos(mid)*(R*0.64), cy + Math.sin(mid)*(R*0.64));
                ctx.rotate(mid + Math.PI/2);
                ctx.fillStyle = isWinner ? '#1c0a00' : '#ffffff';
                ctx.textAlign = 'center';
                ctx.shadowColor = isWinner ? 'rgba(255,220,100,0.6)' : 'rgba(0,0,0,0.9)';
                ctx.shadowBlur = 4;
                const nameParts = (p.name || '').split(' ');
                if(nameParts.length >= 2) {
                    ctx.font = `bold ${isWinner ? '10' : '9'}px sans-serif`;
                    ctx.fillText(nameParts[0], 0, -5);
                    ctx.fillText(nameParts.slice(1).join(' '), 0, 6);
                } else {
                    ctx.font = `bold ${isWinner ? '11' : '10'}px sans-serif`;
                    ctx.fillText(p.name || '', 0, 2);
                }
                ctx.restore();
            });

            // Merkez daire
            const cGrd = ctx.createRadialGradient(cx-4,cy-4,0,cx,cy,26);
            cGrd.addColorStop(0,'#71717a');
            cGrd.addColorStop(1,'#18181b');
            ctx.beginPath(); ctx.arc(cx,cy,26,0,Math.PI*2);
            ctx.fillStyle=cGrd; ctx.fill();
            ctx.strokeStyle='rgba(255,255,255,0.15)'; ctx.lineWidth=2.5; ctx.stroke();

            // Dönüş hızı görsel — çark dönerken radyal çizgiler
            if(_wheelSpinning) {
                ctx.save();
                const lineCount = 18;
                for(let li = 0; li < lineCount; li++) {
                    const a = angle + li * (Math.PI*2/lineCount);
                    const opacity = (li % 2 === 0) ? 0.10 : 0.05;
                    ctx.strokeStyle = `rgba(255,255,255,${opacity})`;
                    ctx.lineWidth = 2;
                    ctx.beginPath();
                    ctx.moveTo(cx + Math.cos(a)*28, cy + Math.sin(a)*28);
                    ctx.lineTo(cx + Math.cos(a)*R, cy + Math.sin(a)*R);
                    ctx.stroke();
                }
                ctx.restore();
            }

            // Kazanan dilim etrafında parlayan halka
            if(!_wheelSpinning && _winnerIndex >= 0) {
                ctx.save();
                const wStartA = angle + _winnerIndex * slice - Math.PI/2;
                const wEndA = wStartA + slice;
                ctx.beginPath();
                ctx.moveTo(cx, cy);
                ctx.arc(cx, cy, R + 5, wStartA, wEndA);
                ctx.closePath();
                ctx.strokeStyle = 'rgba(251,191,36,0.85)';
                ctx.lineWidth = 5;
                ctx.shadowColor = '#fbbf24';
                ctx.shadowBlur = 18;
                ctx.stroke();
                ctx.restore();
            }
        }

        // Init wheel when spin modal opens


        function updateSpinInfo() {
            const el = document.getElementById('spin-inline-info');
            if(!el || !currentUser) return;
            const stats = currentUser.stats || {};
            const prem = parseInt(stats.premium_tier) || 0;
            const maxSpins = prem >= 2 ? 2 : 1;
            const today = new Date().toISOString().slice(0,10);
            const count = stats.last_spin_date === today ? (stats.spin_count || 0) : 0;
            const left = Math.max(0, maxSpins - count);
            el.textContent = left > 0 ? `${left} hak kaldı` : 'Bugün bitti';
            el.className = left > 0
                ? 'text-[10px] text-green-400 font-bold uppercase tracking-widest text-right'
                : 'text-[10px] text-sky-300 font-bold uppercase tracking-widest text-right';
        }

        async function spinWheelAction() {
            const btn = document.getElementById('spin-btn');
            if(btn.disabled || _wheelSpinning) return;
            btn.disabled = true;
            _wheelSpinning = true;
            btn.innerText = "DÖNÜYOR...";
            haptic([20,10,20,10,20]);

            try {
                const res = await sendAction('daily_spin', {});
                if(res.status !== 'ok') {
                    alert(res.message);
                    btn.disabled = false;
                    _wheelSpinning = false;
                    btn.innerText = "ÇARKI ÇEVİR";
                    return;
                }

                const prizes = window.WHEEL_PRIZES || [];
                const prizeIndex = prizes.findIndex(p => p.id === res.prize_id);
                const n = prizes.length;
                if(prizeIndex < 0 || n === 0) { alert("Hata: ödül bulunamadı."); return; }

                const sliceAngle = (Math.PI * 2) / n;

                // İbre üstte (saat 12 = -Math.PI/2).
                // Kazanan dilim index=prizeIndex, merkezinin açısı: prizeIndex*sliceAngle + sliceAngle/2
                // Bunu üste getirmek için: _wheelAngle = -(prizeIndex*sliceAngle + sliceAngle/2)
                // Ama mevcut _wheelAngle'dan devam etmeli + en az 8 tam tur dönsün
                const currentNorm = ((_wheelAngle % (Math.PI*2)) + Math.PI*2) % (Math.PI*2);
                const targetSliceCenter = prizeIndex * sliceAngle + sliceAngle / 2;
                // Hedef: çarkın açısı = -targetSliceCenter (yani o dilim tam üste gelsin)
                const targetNorm = ((-targetSliceCenter) % (Math.PI*2) + Math.PI*2) % (Math.PI*2);
                let delta = targetNorm - currentNorm;
                if(delta < 0) delta += Math.PI*2;
                // En az 8 tam tur + biraz daha
                const extraSpins = Math.PI * 2 * (8 + Math.floor(Math.random()*4));
                const finalAngle = _wheelAngle + extraSpins + delta;

                // Tick sound
                const tickSound = document.getElementById('spin-tick-sound');

                const canvas = document.getElementById('wheel-canvas-3d');
                const start = performance.now();
                const duration = 6500;
                const startAngle = _wheelAngle;
                const totalAngle = finalAngle - startAngle;
                let lastTickSlice = -1;

                // Çarkı dönerken parlat
                if(canvas) canvas.classList.add('wheel-spinning-canvas');

                function easeInOut(t) {
                    return t < 0.5
                        ? 4 * t * t * t
                        : 1 - Math.pow(-2 * t + 2, 3) / 2;
                }

                function animate(now) {
                    const elapsed = now - start;
                    const t = Math.min(elapsed / duration, 1);
                    const eased = easeInOut(t);
                    _wheelAngle = startAngle + totalAngle * eased;

                    // 3D tilt — sadece orta hızda belirgin, başta ve sonda sıfır
                    const tiltEnvelope = Math.sin(t * Math.PI); // 0→1→0
                    const tiltX = Math.sin(elapsed * 0.004) * tiltEnvelope * 12;
                    if(canvas) {
                        canvas.style.transform = `rotateX(${tiltX}deg)`;
                        _drawWheel3D(canvas, _wheelAngle);
                    }

                    // Slice sınırına göre tick sesi (gerçekçi tık-tık)
                    const tickSound = document.getElementById('spin-tick-sound');
                    const currentSlice = Math.floor(((_wheelAngle % (Math.PI*2) + Math.PI*2) % (Math.PI*2)) / sliceAngle);
                    if(currentSlice !== lastTickSlice && t > 0.05 && t < 0.97) {
                        lastTickSlice = currentSlice;
                        if(tickSound) {
                            tickSound.currentTime = 0;
                            try { tickSound.play().catch(()=>{}); } catch(e){}
                        }
                    }

                    if(t < 1) {
                        requestAnimationFrame(animate);
                    } else {
                        if(canvas) {
                            canvas.classList.remove('wheel-spinning-canvas');
                            canvas.style.transform = '';
                        }
                        // Kazanan dilimi vurgula + kısa pulse animasyonu
                        _winnerIndex = prizeIndex;
                        _drawWheel3D(canvas, _wheelAngle);

                        // Kazanan için 3 kez kısa parlama
                        let pulseCount = 0;
                        const pulseInterval = setInterval(() => {
                            pulseCount++;
                            if(canvas) {
                                canvas.style.boxShadow = pulseCount % 2 === 1
                                    ? '0 0 60px rgba(251,191,36,1), 0 0 120px rgba(251,191,36,0.6)'
                                    : '0 0 35px rgba(14,165,233,0.5), 0 0 60px rgba(234,179,8,0.2)';
                            }
                            if(pulseCount >= 6) {
                                clearInterval(pulseInterval);
                                if(canvas) canvas.style.boxShadow = '';
                            }
                        }, 180);
                        _wheelSpinning = false;
                        btn.disabled = false;
                        btn.innerText = "ÇARKI ÇEVİR";

                        // Win sound + confetti
                        const winSound = document.getElementById('spin-win-sound');
                        if(winSound) { winSound.currentTime=0; try{winSound.play().catch(()=>{});}catch(e){} }
                        haptic([100,50,100,50,200]);
                        showSpinConfetti();

                        setTimeout(async () => {
                            // Güzel sonuç banner'ı göster
                            showSpinResult(res.prize_name);
                            // loadData yerine sadece spin sayacını ve XP'yi local güncelle
                            if(currentUser && currentUser.stats) {
                                const today = new Date().toISOString().slice(0,10);
                                currentUser.stats.last_spin_date = today;
                                currentUser.stats.spin_count = (currentUser.stats.spin_count || 0) + 1;
                                localStorage.setItem("fr_user", JSON.stringify(currentUser));
                                updateProfileUI();
                                renderMissions();
                                updateSpinInfo();
                            }
                        }, 400);
                    }
                }
                requestAnimationFrame(animate);

            } catch(e) {
                btn.disabled = false;
                _wheelSpinning = false;
                btn.innerText = "ÇARKI ÇEVİR";
            }
        }

        function showSpinResult(prizeName) {
            // Varsa eski result div'i temizle
            const old = document.getElementById('spin-result-banner');
            if(old) old.remove();

            const banner = document.createElement('div');
            banner.id = 'spin-result-banner';
            banner.style.cssText = 'position:fixed;inset:0;z-index:999999;display:flex;align-items:center;justify-content:center;padding:20px;background:rgba(0,0,0,0.65);backdrop-filter:blur(4px);';
            banner.innerHTML = `
            <div style="background:linear-gradient(135deg,#1c1c1e,#2a1500);border:2px solid #eab308;border-radius:28px;padding:36px 28px;max-width:340px;width:100%;text-align:center;box-shadow:0 0 60px rgba(234,179,8,0.5),0 0 120px rgba(234,179,8,0.2);animation:scaleIn 0.4s cubic-bezier(0.16,1,0.3,1) both;">
                <div style="font-size:56px;margin-bottom:12px;display:inline-block;animation:bounce 0.55s ease-in-out infinite alternate;">🎉</div>
                <div style="color:#fbbf24;font-size:11px;font-weight:900;text-transform:uppercase;letter-spacing:0.2em;margin-bottom:6px;">Tebrikler!</div>
                <div style="color:#ffffff;font-size:32px;font-weight:900;letter-spacing:0.05em;text-shadow:0 0 20px rgba(234,179,8,0.8);">${prizeName}</div>
                <div style="color:#a1a1aa;font-size:11px;margin-top:8px;font-weight:600;">Hesabına eklendi!</div>
                <button onclick="document.getElementById('spin-result-banner').remove()" style="margin-top:24px;background:linear-gradient(135deg,#eab308,#b45309);color:#000;border:none;border-radius:14px;padding:14px 32px;font-size:15px;font-weight:900;cursor:pointer;text-transform:uppercase;letter-spacing:0.1em;width:100%;">HARIKA! ✓</button>
            </div>`;
            document.body.appendChild(banner);
            banner.addEventListener('click', (e) => { if(e.target === banner) banner.remove(); });
        }

        function showSpinConfetti() {
            const colors = ['#ff4444','#ffbb00','#44ff88','#4488ff','#ff44ff','#ffffff','#ff8800','#00ffcc'];
            const count = 70;
            for(let i = 0; i < count; i++) {
                const el = document.createElement('div');
                const color = colors[i % colors.length];
                const isRect = i % 3 !== 0;
                const size = 6 + Math.random() * 8;
                const delay = Math.random() * 0.6;
                const duration = 1.8 + Math.random() * 1.0;
                const startX = Math.random() * 100;
                if(isRect) {
                    el.style.cssText = `position:fixed;width:${size}px;height:${size * 0.45}px;border-radius:1px;background:${color};left:${startX}vw;top:-2vh;pointer-events:none;z-index:999999;animation:confettiRect ${duration}s ease-in ${delay}s forwards;`;
                } else {
                    el.style.cssText = `position:fixed;width:${size}px;height:${size}px;border-radius:50%;background:${color};left:${startX}vw;top:-2vh;pointer-events:none;z-index:999999;animation:confettiFall ${duration}s ease-in ${delay}s forwards;`;
                }
                document.body.appendChild(el);
                setTimeout(()=>el.remove(), (duration + delay + 0.2) * 1000);
            }
        }

        // Cark acilinca init et - window.onload sonrasi guvenli


        // ==============================================================
        // ŞİFRE SIFIRLAMA (FORGOT PASSWORD)
        // ==============================================================

        function openForgotPasswordModal() {
            const modal = document.getElementById("forgot-password-modal");
            if (modal) {
                document.getElementById("fp-step-1").classList.remove("hidden");
                document.getElementById("fp-step-2").classList.add("hidden");
                document.getElementById("fp-email").value = "";
                modal.classList.remove("hidden");
            }
        }

        function closeForgotPasswordModal() {
            const modal = document.getElementById("forgot-password-modal");
            if (modal) modal.classList.add("hidden");
        }

        async function requestPasswordReset() {
            const email = document.getElementById("fp-email").value.trim();
            if(!email) return alert("Lütfen kayıtlı e-posta adresinizi girin!");
            try {
                const res = await sendAction('request_reset', { email: email });
                if(res.status === 'ok') {
                    alert("Sıfırlama kodu e-postanıza gönderildi!");
                    document.getElementById("fp-step-1").classList.add("hidden");
                    document.getElementById("fp-step-2").classList.remove("hidden");
                }
            } catch(e) {}
        }

        async function submitNewPassword() {
            const email = document.getElementById("fp-email").value.trim();
            const code = document.getElementById("fp-code").value.trim();
            const newPw = document.getElementById("fp-new-password").value.trim();
            
            if(!code || !newPw) return alert("Kod ve yeni şifre boş bırakılamaz!");
            if(newPw.length < 4) return alert("Şifre en az 4 karakter olmalıdır.");
            
            try {
                await sendAction('reset_password_code', { email: email, code: code, new_password: newPw });
                
                // Kayıtlı kullanıcı varsa yeni şifreyi encode ederek güncelle
                if (localStorage.getItem("fr_remembered_username")) {
                    localStorage.setItem("fr_remembered_password", btoa(unescape(encodeURIComponent(newPw))));
                }
                const loginPassInput = document.getElementById("login-password");
                if(loginPassInput) loginPassInput.value = newPw;

                alert("Şifreniz başarıyla güncellendi! Artık yeni şifrenizle giriş yapabilirsiniz.");
                document.getElementById("forgot-password-modal").classList.add("hidden");
            } catch(e) { }
        }
