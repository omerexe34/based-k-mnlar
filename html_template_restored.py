HTML_CODE = '''\

<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    
    <!-- SEO Meta Tags -->
    <title>Freerider TÃ¼rkiye | TÃ¼rkiye'nin En BÃ¼yÃ¼k Downhill & Freeride DaÄŸ Bisikleti TopluluÄŸu</title>
    <meta name="description" content="TÃ¼rkiye'nin en bÃ¼yÃ¼k Downhill ve Freeride MTB daÄŸ bisikleti topluluÄŸu. Rotalar keÅŸfet, ikinci el parÃ§a al-sat, etkinliklere katÄ±l ve bisikletÃ§ilerle tanÄ±ÅŸ!">
    <meta name="keywords" content="Freeride, Downhill, MTB, DaÄŸ Bisikleti, Bisiklet TopluluÄŸu, Enduro, Ä°kinci El Bisiklet, Bisiklet RotalarÄ±, TÃ¼rkiye Bisiklet, Hardcore Freeride, MTB TÃ¼rkiye">
    <meta name="author" content="FreeriderTR">
    <meta name="robots" content="index, follow">
    <meta name="language" content="Turkish">
    
    <!-- Open Graph / Facebook -->
    <meta property="og:type" content="website">
    <meta property="og:url" content="https://freeridertr.com.tr/">
    <meta property="og:title" content="Freerider TÃ¼rkiye | Downhill & Freeride TopluluÄŸu">
    <meta property="og:description" content="TÃ¼rkiye'nin en bÃ¼yÃ¼k Downhill ve Freeride MTB daÄŸ bisikleti topluluÄŸu. Rotalar keÅŸfet, ikinci el parÃ§a al-sat, etkinliklere katÄ±l!">
    <meta property="og:image" content="https://cdn.freeridertr.com.tr/profil%20resmi/unnamed.jpg">
    <meta property="og:site_name" content="FreeriderTR">
    
    <!-- Twitter -->
    <meta property="twitter:card" content="summary_large_image">
    <meta property="twitter:url" content="https://freeridertr.com.tr/">
    <meta property="twitter:title" content="Freerider TÃ¼rkiye | Downhill & Freeride TopluluÄŸu">
    <meta property="twitter:description" content="TÃ¼rkiye'nin en bÃ¼yÃ¼k Downhill ve Freeride MTB daÄŸ bisikleti topluluÄŸu. Rotalar keÅŸfet, ikinci el parÃ§a al-sat, etkinliklere katÄ±l!">
    <meta property="twitter:image" content="https://cdn.freeridertr.com.tr/profil%20resmi/unnamed.jpg">

    <!-- Canonical URL -->
    <link rel="canonical" href="https://freeridertr.com.tr/">
    <link rel="manifest" href="/manifest.json">
    <meta name="theme-color" content="#000000">
    

    <!-- iOS PWA Support -->
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <meta name="apple-mobile-web-app-title" content="FreeriderTR">
    <link rel="apple-touch-icon" href="https://cdn.freeridertr.com.tr/profil%20resmi/unnamed.jpg">
    
    <!-- Onboarding System (Driver.js) & Canvas Confetti -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/intro.js/7.2.0/introjs.min.css"/>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/intro.js/7.2.0/intro.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"></script>
    
    <style>
        
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
        </style>
    
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <link rel="stylesheet" href="https://unpkg.com/leaflet.markercluster@1.5.3/dist/MarkerCluster.css" />
    <link rel="stylesheet" href="https://unpkg.com/leaflet.markercluster@1.5.3/dist/MarkerCluster.Default.css" />
    <script src="https://unpkg.com/leaflet.markercluster@1.5.3/dist/leaflet.markercluster.js"></script>
    <script src="https://unpkg.com/lucide@latest"></script>
    <script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
    <script src="https://cdn.onesignal.com/sdks/web/v16/OneSignalSDK.page.js" defer></script>
    <script>
      window.OneSignalDeferred = window.OneSignalDeferred || [];
      OneSignalDeferred.push(async function(OneSignal) {
        await OneSignal.init({
          appId: "{{ onesignal_app_id }}",
          serviceWorkerParam: { scope: "/" },
          serviceWorkerPath: "/OneSignalSDKWorker.js",
          notifyButton: { enable: false },
          allowLocalhostAsSecureOrigin: true,
          notificationClickHandlerMatch: "origin",
          notificationClickHandlerAction: "focus",
        });
        console.log('âœ… OneSignal SDK baÅŸarÄ±yla baÅŸlatÄ±ldÄ±');
        // SDK init olduktan sonra currentUser varsa hemen login yap + player_id kaydet
        if (window.currentUser && window.currentUser.username) {
          try {
            await OneSignal.login(window.currentUser.username);
            console.log('âœ… OneSignal otomatik login (init sonrasÄ±):', window.currentUser.username);
            // Ä°zin varsa subscription ID'yi de kaydet
            if (OneSignal.Notifications.permission) {
              // saveOneSignalPlayerId henÃ¼z tanÄ±mlanmamÄ±ÅŸ olabilir, defer et
              setTimeout(async () => {
                if (typeof saveOneSignalPlayerId === 'function') {
                  await saveOneSignalPlayerId(OneSignal);
                }
              }, 1000);
            }
          } catch(e) {
            console.error('OneSignal init-login hatasÄ±:', e);
          }
        }
      });
    </script>
    
    <link rel="stylesheet" href="https://unpkg.com/leaflet-control-geocoder/dist/Control.Geocoder.css" />
    <script src="https://unpkg.com/leaflet-control-geocoder/dist/Control.Geocoder.js"></script>
    
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;800;900&family=Teko:wght@500;700&display=swap');
        body { font-family: 'Outfit', sans-serif; background-color: #020b19; margin: 0; padding: 0; overscroll-behavior: none; color: #e4e4e7; touch-action: manipulation; }
        .teko-font { font-family: 'Teko', sans-serif; text-transform: uppercase; }
        #map { height: 100% !important; width: 100% !important; z-index: 10; touch-action: none; }
        ::-webkit-scrollbar { width: 0px; background: transparent; }
        .bg-glass { background: rgba(24, 24, 27, 0.7); backdrop-filter: blur(16px); -webkit-backdrop-filter: blur(16px); border: 1px solid rgba(255, 255, 255, 0.05); }
        .bg-darker { background-color: #030a16; }
        
        .leaflet-control-layers { margin-top: 70px !important; background: rgba(24, 24, 27, 0.7) !important; color: white !important; border: 1px solid rgba(255, 255, 255, 0.1) !important; border-radius: 8px !important; backdrop-filter: blur(8px); font-size: 10px !important; padding: 2px !important; }
        .leaflet-control-layers-toggle { width: 30px !important; height: 30px !important; background-size: 18px 18px !important; }
        .leaflet-control-layers-base label { margin-bottom: 2px !important; padding: 2px !important; cursor: pointer; }
        .leaflet-control-geocoder { margin-top: 15px !important; }
        
        /* Premium Animasyonlar & Efektler */
        @keyframes slideUpFade { 0% { opacity: 0; transform: translateY(40px) scale(0.97); } 60% { opacity: 1; } 100% { opacity: 1; transform: translateY(0) scale(1); } }
        @keyframes slideDownFade { 0% { opacity: 0; transform: translateY(-20px); } 100% { opacity: 1; transform: translateY(0); } }
        @keyframes scaleInFade { 0% { opacity: 0; transform: scale(0.90); } 70% { transform: scale(1.02); } 100% { opacity: 1; transform: scale(1); } }
        @keyframes fadeIn { 0% { opacity: 0; } 100% { opacity: 1; } }
        @keyframes shimmer { 0% { background-position: -200% 0; } 100% { background-position: 200% 0; } }
        @keyframes pulseGlow { 0%, 100% { box-shadow: 0 0 8px rgba(14,165,233,0.5); } 50% { box-shadow: 0 0 22px rgba(14,165,233,0.9); } }
        @keyframes onlinePulse { 0%, 100% { box-shadow: 0 0 0 0 rgba(34,197,94,0.7); transform: scale(1); } 50% { box-shadow: 0 0 0 6px rgba(34,197,94,0); transform: scale(1.1); } }
        @keyframes slideInRight { 0% { opacity: 0; transform: translateX(60px); } 100% { opacity: 1; transform: translateX(0); } }
        @keyframes slideInLeft { 0% { opacity: 0; transform: translateX(-60px); } 100% { opacity: 1; transform: translateX(0); } }
        @keyframes tabSwitch { 0% { opacity: 0; transform: translateY(12px); } 100% { opacity: 1; transform: translateY(0); } }
        @keyframes notifBounce { 0%,100%{transform:scale(1)} 30%{transform:scale(1.25)} 60%{transform:scale(0.9)} }
        @keyframes ripple { 0% { transform: scale(0); opacity: 0.6; } 100% { transform: scale(4); opacity: 0; } }

        /* â”€â”€ AI ModeratÃ¶r & Moderation UI â”€â”€ */
        @keyframes shake { 0%,100%{transform:translateX(0)} 10%,30%,50%,70%,90%{transform:translateX(-4px)} 20%,40%,60%,80%{transform:translateX(4px)} }
        @keyframes fadeInUp { 0%{opacity:0;transform:translateY(16px)} 100%{opacity:1;transform:translateY(0)} }
        @keyframes slideUp { 0%{opacity:0;transform:translateY(40px)} 100%{opacity:1;transform:translateY(0)} }
        @keyframes glowPulseRed { 0%,100%{box-shadow:0 0 12px rgba(239,68,68,0.3)} 50%{box-shadow:0 0 24px rgba(239,68,68,0.6)} }
        @keyframes toastSlideIn { 0%{opacity:0;transform:translateX(-50%) translateY(20px)} 100%{opacity:1;transform:translateX(-50%) translateY(0)} }
        @keyframes toastSlideOut { 0%{opacity:1;transform:translateX(-50%) translateY(0)} 100%{opacity:0;transform:translateX(-50%) translateY(20px)} }
        @keyframes skeletonPulse { 0%{opacity:0.4} 50%{opacity:0.8} 100%{opacity:0.4} }
        @keyframes premiumGlow { 0%,100%{box-shadow:0 0 20px rgba(234,179,8,0.3)} 50%{box-shadow:0 0 40px rgba(234,179,8,0.6)} }

        .ai-moderator-msg {
            background: linear-gradient(135deg, #dc2626, #991b1b) !important;
            border-left: 4px solid #ef4444 !important;
            border-color: #ef4444 !important;
            box-shadow: 0 0 20px rgba(239,68,68,0.3);
            animation: shake 0.5s ease-in-out, fadeInUp 0.4s ease-out, glowPulseRed 2s ease-in-out infinite;
            color: #fef2f2 !important;
        }
        /* Flagged mesaj: blur + overlay (flag_count < 2) */
        .msg-flagged {
            filter: blur(5px);
            opacity: 0.6;
            position: relative;
            transition: filter 0.3s, opacity 0.3s;
        }
        .msg-flagged-overlay {
            display: block; width: 100%; margin-bottom: 4px;
        }
        .msg-flagged-overlay span {
            font-size: 9px; font-weight: 800; color: #fca5a5;
            text-transform: uppercase; letter-spacing: 1px;
            padding: 4px 8px; border-radius: 6px;
            background: rgba(127,29,29,0.8); border: 1px solid rgba(239,68,68,0.4);
            display: inline-block;
        }
        /* Collapsed mesaj: flag_count >= 2, tÄ±klanabilir */
        .msg-collapsed-wrap { cursor: pointer; }
        .msg-collapsed-bar {
            display: flex; align-items: center; gap: 8px;
            padding: 8px 14px; border-radius: 12px;
            background: linear-gradient(135deg, rgba(127,29,29,0.4), rgba(0,0,0,0.6));
            border: 1px solid rgba(239,68,68,0.3);
            font-size: 11px; font-weight: 700; color: #fca5a5;
            letter-spacing: 0.5px;
        }
        .msg-collapsed-bar:hover { background: rgba(127,29,29,0.6); }
        .msg-collapsed-content { display: none; margin-top: 6px; }
        .msg-collapsed-content.show { display: block; filter: blur(2px); opacity: 0.5; }
        /* Notification popup */
        .notif-popup-overlay {
            position: fixed; inset: 0; z-index: 99999;
            background: rgba(0,0,0,0.6); backdrop-filter: blur(6px);
            display: flex; align-items: center; justify-content: center;
            animation: fadeIn 0.3s ease-out;
        }
        .notif-popup-card {
            background: linear-gradient(145deg, rgba(20,20,20,0.95), rgba(10,10,10,0.98));
            border: 1px solid rgba(59,130,246,0.3);
            border-radius: 20px; padding: 28px 24px;
            max-width: 340px; width: 90%; position: relative;
            box-shadow: 0 20px 60px rgba(0,0,0,0.8), 0 0 40px rgba(59,130,246,0.15);
            animation: slideUp 0.4s cubic-bezier(0.16,1,0.3,1);
        }
        @keyframes slideUp { from { transform: translateY(40px); opacity: 0; } to { transform: translateY(0); opacity: 1; } }
        @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
        .skeleton-loader {
            background: linear-gradient(90deg, #27272a 0%, #3f3f46 50%, #27272a 100%);
            background-size: 200% 100%;
            animation: skeletonPulse 1.5s ease-in-out infinite;
            border-radius: 12px;
        }
        .premium-popup-overlay {
            position: fixed; inset: 0; z-index: 999999;
            background: rgba(0,0,0,0.7); backdrop-filter: blur(8px);
            display: flex; align-items: center; justify-content: center;
            padding: 16px;
        }
        .premium-popup-card {
            background: linear-gradient(145deg, #18181b, #27272a);
            border: 1px solid rgba(234,179,8,0.3);
            border-radius: 20px; max-width: 400px; width: 100%;
            padding: 32px 24px; text-align: center;
            animation: slideUp 0.5s cubic-bezier(0.16,1,0.3,1) both;
            box-shadow: 0 20px 60px rgba(0,0,0,0.6);
        }

        /* .slide-up-anim ve .scale-in-anim â€” alt satÄ±rlardaki (683-684) tanÄ±mlar tarafÄ±ndan override edilir */
        .slide-down-anim { animation: slideDownFade 0.35s cubic-bezier(0.16, 1, 0.3, 1) both; }
        .fade-in-anim { animation: fadeIn 0.3s ease both; }
        .slide-in-right { animation: slideInRight 0.4s cubic-bezier(0.16, 1, 0.3, 1) both; }
        .slide-in-left { animation: slideInLeft 0.4s cubic-bezier(0.16, 1, 0.3, 1) both; }
        .tab-switch-anim { animation: tabSwitch 0.3s cubic-bezier(0.16, 1, 0.3, 1) both; }

        /* .btn-premium-hover tanÄ±mÄ± â€” alttaki (687) enhanced versiyon override eder */
        /* .glass-panel tanÄ±mÄ± â€” alttaki (559) enhanced versiyon override eder */
        
        /* Admin Panel Tab Styles */
        .admin-tab-btn { color: #71717a; }
        .active-admin-tab { background: rgba(12,74,110,0.4); color: #bae6fd; border: 1px solid rgba(12,74,110,0.6); }
        .ua-tab-btn { color: #71717a; }
        .ua-active-tab { background: rgba(39,39,42,0.8); color: #e4e4e7; border: 1px solid rgba(255,255,255,0.08); }

        /* Enhanced animations */
        @keyframes adminPulse { 0%,100%{box-shadow:0 0 15px rgba(14,165,233,0.3)} 50%{box-shadow:0 0 30px rgba(14,165,233,0.7)} }
        @keyframes logEntry { 0%{opacity:0;transform:translateX(-12px)} 100%{opacity:1;transform:translateX(0)} }
        @keyframes countUp { 0%{opacity:0;transform:translateY(8px)scale(0.9)} 100%{opacity:1;transform:translateY(0)scale(1)} }
        .admin-card-enter { animation: logEntry 0.3s ease both; }
        .count-up-anim { animation: countUp 0.4s cubic-bezier(0.34,1.56,0.64,1) both; }

        /* Scrollbar for admin panel */
        #admin-panel ::-webkit-scrollbar { width: 3px; }
        #admin-panel ::-webkit-scrollbar-track { background: transparent; }
        #admin-panel ::-webkit-scrollbar-thumb { background: rgba(12,74,110,0.6); border-radius: 4px; }

        /* Ban badge */
        .ban-reason-badge { background: rgba(12,74,110,0.25); border: 1px solid rgba(12,74,110,0.5); color: #bae6fd; font-size: 9px; font-weight: 800; padding: 2px 8px; border-radius: 6px; text-transform: uppercase; letter-spacing: 0.05em; }

        /* Log action colors */
        .log-ban { border-left: 3px solid #38bdf8; }
        .log-delete { border-left: 3px solid #f97316; }
        .log-assign { border-left: 3px solid #22c55e; }
        .log-revoke { border-left: 3px solid #eab308; }
        .log-notify { border-left: 3px solid #3b82f6; }
        .log-default { border-left: 3px solid #71717a; }

        /* Ã‡evrim iÃ§i gÃ¶stergesi */
        .online-dot { width: 10px; height: 10px; background: #22c55e; border-radius: 50%; border: 2px solid #09090b; animation: onlinePulse 2s infinite; display: inline-block; flex-shrink: 0; }
        .online-dot-sm { width: 8px; height: 8px; background: #22c55e; border-radius: 50%; border: 1.5px solid #09090b; animation: onlinePulse 2s infinite; display: inline-block; flex-shrink: 0; }
        .recent-dot { width: 8px; height: 8px; background: #eab308; border-radius: 50%; border: 1.5px solid #09090b; display: inline-block; flex-shrink: 0; }
        .offline-dot { width: 8px; height: 8px; background: #52525b; border-radius: 50%; border: 1.5px solid #09090b; display: inline-block; flex-shrink: 0; }
        .online-label { color: #22c55e; font-size: 9px; font-weight: 800; text-transform: uppercase; letter-spacing: 0.08em; }
        .recent-label { color: #eab308; font-size: 9px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; }
        
        @keyframes rainbow-text { 0% { background-position: 0% 50%; } 100% { background-position: 200% 50%; } }
        @keyframes rainbow-shadow {
            0% { box-shadow: 0 0 15px red; border-color: red; filter: drop-shadow(0 0 5px red); }
            20% { box-shadow: 0 0 15px orange; border-color: orange; filter: drop-shadow(0 0 5px orange); }
            40% { box-shadow: 0 0 15px yellow; border-color: yellow; filter: drop-shadow(0 0 5px yellow); }
            60% { box-shadow: 0 0 15px #00ff00; border-color: #00ff00; filter: drop-shadow(0 0 5px #00ff00); }
            80% { box-shadow: 0 0 15px #00a2ff; border-color: #00a2ff; filter: drop-shadow(0 0 5px #00a2ff); }
            100% { box-shadow: 0 0 15px red; border-color: red; filter: drop-shadow(0 0 5px red); }
        }
        /* GerÃ§ek alev efekti â€” parlayan border + Ã¼st parÃ§acÄ±klar */
        @keyframes fire-border {
            0%   { box-shadow: 0 0 10px 2px #c0390080, 0 0 20px 4px #e0500040; border-color: #c03900; }
            50%  { box-shadow: 0 0 16px 4px #d04000aa, 0 0 28px 6px #f0600055; border-color: #d04000; }
            100% { box-shadow: 0 0 10px 2px #c0390080, 0 0 20px 4px #e0500040; border-color: #c03900; }
        }
        @keyframes ice-border {
            0%   { box-shadow: 0 0 10px 2px #4488bb70, 0 0 20px 4px #2266aa30; border-color: #4488bb; }
            50%  { box-shadow: 0 0 16px 4px #5599cc90, 0 0 28px 6px #3377bb40; border-color: #5599cc; }
            100% { box-shadow: 0 0 10px 2px #4488bb70, 0 0 20px 4px #2266aa30; border-color: #4488bb; }
        }
        @keyframes fire-flicker { 0%,100%{filter:brightness(1)} 50%{filter:brightness(1.08)} }
        @keyframes ice-shimmer  { 0%,100%{filter:brightness(1)} 50%{filter:brightness(1.06) hue-rotate(5deg)} }
        @keyframes particle-rise { 0%{transform:translateY(0) translateX(0) scale(1);opacity:0.9} 100%{transform:translateY(-60px) translateX(var(--tx)) scale(0);opacity:0} }
        @keyframes particle-float { 0%{transform:translateY(0) translateX(0) scale(0.8);opacity:0.7} 100%{transform:translateY(40px) translateX(var(--tx)) scale(0.2);opacity:0} }

        .effect-fire {
            animation: fire-border 1.5s ease-in-out infinite, fire-flicker 2s ease-in-out infinite !important;
            border-width: 3px !important;
        }
        .effect-ice {
            animation: ice-border 2s ease-in-out infinite, ice-shimmer 2.5s ease-in-out infinite !important;
            border-width: 3px !important;
        }

        /* ParÃ§acÄ±k container */
        .avatar-particle-wrap { position: relative; display: inline-block; }
        .particle-canvas { position: absolute; top: -30px; left: 50%; transform: translateX(-50%); width: 120px; height: 80px; pointer-events: none; z-index: 50; }
        .text-prem-rainbow { background: linear-gradient(90deg, #ff0055, #ffaa00, #55ff00, #00eeff, #aa00ff, #ff0055); background-size: 200% auto; color: transparent; -webkit-background-clip: text; animation: rainbow-text 3s linear infinite; font-weight: 900 !important; filter: drop-shadow(0 0 5px rgba(255,255,255,0.5)); }
        .text-prem-gold { color: #fbbf24 !important; text-shadow: 0 0 15px rgba(251, 191, 36, 1), 0 0 5px #fbbf24 !important; font-weight: 900 !important; }
        .text-prem-blue { color: #3b82f6 !important; text-shadow: 0 0 15px rgba(59, 130, 246, 1), 0 0 5px #3b82f6 !important; font-weight: 900 !important; }
        .text-prem-green { color: #22c55e !important; text-shadow: 0 0 15px rgba(34, 197, 94, 1), 0 0 5px #22c55e !important; font-weight: 900 !important; }
        .text-prem-pink { color: #ec4899 !important; text-shadow: 0 0 15px rgba(236, 72, 153, 1), 0 0 5px #ec4899 !important; font-weight: 900 !important; }
        .border-prem-rainbow { animation: rainbow-shadow 2.5s linear infinite; border-width: 4px; border-style: solid; }
        .border-prem-gold { border: 4px solid #fbbf24; box-shadow: 0 0 20px #fbbf24, inset 0 0 10px #fbbf24; }
        .border-prem-blue { border: 4px solid #3b82f6; box-shadow: 0 0 20px #3b82f6, inset 0 0 10px #3b82f6; }
        .border-prem-green { border: 4px solid #22c55e; box-shadow: 0 0 20px #22c55e, inset 0 0 10px #22c55e; }
        .border-prem-pink { border: 4px solid #ec4899; box-shadow: 0 0 20px #ec4899, inset 0 0 10px #ec4899; }
        .text-dlx-blue { background: linear-gradient(45deg, #60a5fa, #bfdbfe, #3b82f6); -webkit-background-clip: text; color: transparent; font-weight: 800 !important; text-shadow: 0 0 5px rgba(59,130,246,0.5); }
        .text-dlx-yellow { background: linear-gradient(45deg, #fde047, #fef08a, #eab308); -webkit-background-clip: text; color: transparent; font-weight: 800 !important; text-shadow: 0 0 5px rgba(234,179,8,0.5); }
        .text-dlx-pink { background: linear-gradient(45deg, #f472b6, #fbcfe8, #ec4899); -webkit-background-clip: text; color: transparent; font-weight: 800 !important; text-shadow: 0 0 5px rgba(236,72,153,0.5); }
        .text-dlx-green { background: linear-gradient(45deg, #4ade80, #bbf7d0, #22c55e); -webkit-background-clip: text; color: transparent; font-weight: 800 !important; text-shadow: 0 0 5px rgba(34,197,94,0.5); }
        .border-dlx-blue { border: 3px solid #3b82f6; border-style: inset; box-shadow: 0 0 10px #3b82f6; }
        .border-dlx-yellow { border: 3px solid #eab308; border-style: inset; box-shadow: 0 0 10px #eab308; }
        .border-dlx-pink { border: 3px solid #ec4899; border-style: inset; box-shadow: 0 0 10px #ec4899; }
        .border-dlx-green { border: 3px solid #22c55e; border-style: inset; box-shadow: 0 0 10px #22c55e; }
        
        .tab-btn { transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1); }
        .market-img-scroll { display: flex; overflow-x: auto; scroll-snap-type: x mandatory; gap: 10px; }
        .market-img-scroll img { scroll-snap-align: center; max-width: 100%; border-radius: 8px; }
        .horizontal-scroll-container { display: flex; overflow-x: auto; scroll-behavior: smooth; -ms-overflow-style: none; scrollbar-width: none; }
        .horizontal-scroll-container::-webkit-scrollbar { display: none; }
        .custom-scrollbar::-webkit-scrollbar { width: 4px; }
        .custom-scrollbar::-webkit-scrollbar-thumb { background: #3f3f46; border-radius: 4px; }
        .map-add-mode { cursor: crosshair !important; }
        .progress-bar-bg { background-color: #27272a; border-radius: 9999px; height: 8px; width: 100%; overflow: hidden; margin-top: 8px; }
        .progress-bar-fill { background: linear-gradient(90deg, #0ea5e9, #0284c7); height: 100%; transition: width 0.5s ease; }
        
        /* Safe area padding for bottom nav */
        .pb-safe { padding-bottom: env(safe-area-inset-bottom, 8px); }
        #bottom-nav { padding-bottom: max(8px, env(safe-area-inset-bottom)); }
        
        /* Mobile tap highlight fix */
        * { -webkit-tap-highlight-color: transparent; }
        
        /* Premium input focus */
        input:focus, textarea:focus, select:focus { outline: none; }
        
        /* Smooth modal backdrop */
        .modal-backdrop { background: rgba(0,0,0,0.75); backdrop-filter: blur(8px); -webkit-backdrop-filter: blur(8px); }
        
        /* Seviye atlamasÄ± kutlama */
        @keyframes levelUpPulse {
            0%   { transform: scale(0.5) rotate(-5deg); opacity: 0; }
            40%  { transform: scale(1.15) rotate(3deg); opacity: 1; }
            70%  { transform: scale(0.95) rotate(-1deg); }
            100% { transform: scale(1) rotate(0deg); opacity: 1; }
        }
        @keyframes levelUpFloat {
            0%   { transform: translateY(0) scale(1); opacity: 1; }
            100% { transform: translateY(-80px) scale(0.5); opacity: 0; }
        }
        @keyframes storyRing {
            0%   { box-shadow: 0 0 0 3px #0ea5e9, 0 0 0 5px #0ea5e940; }
            50%  { box-shadow: 0 0 0 3px #f59e0b, 0 0 0 6px #f59e0b50; }
            100% { box-shadow: 0 0 0 3px #0ea5e9, 0 0 0 5px #0ea5e940; }
        }
        @keyframes igStoryRingSpin {
            0%   { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        .level-up-anim { animation: levelUpPulse 0.7s cubic-bezier(0.34,1.56,0.64,1) both; }
        /* Instagram gradient story ring */
        .story-ring {
            border-radius: 50%;
            position: relative;
            background: linear-gradient(45deg, #f09433, #e6683c, #dc2743, #cc2366, #bc1888) border-box;
            border: 2.5px solid transparent;
            background-clip: padding-box;
            box-shadow: 0 0 0 2.5px #f09433, 0 0 12px rgba(220,39,67,0.5);
            animation: storyRing 2.5s ease-in-out infinite;
        }
        .story-seen { opacity: 0.5; filter: grayscale(60%); }

        /* â”€â”€ REELS GRID VIEW â”€â”€ */
        #reels-feed.grid-mode {
            display: grid !important;
            grid-template-columns: repeat(4, 1fr);
            gap: 2px;
            overflow-y: auto;
            scroll-snap-type: none;
            height: 100%;
            align-content: start;
        }
        #reels-feed.grid-mode > div {
            height: 160px !important;
            cursor: pointer;
            scroll-snap-align: unset !important;
            position: relative;
        }
        #reels-feed.grid-mode > div > video,
        #reels-feed.grid-mode > div > img {
            object-fit: cover !important;
            width: 100% !important;
            height: 100% !important;
        }
        #reels-feed.grid-mode > div > .absolute { display: none !important; }
        #reels-feed.grid-mode > div > video { pointer-events: none; }
        .reel-fullscreen-overlay {
            position: fixed;
            inset: 0;
            z-index: 100;
            background: #000;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        /* Play/Pause flash icon */
        .reel-play-flash {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            pointer-events: none;
            z-index: 20;
            opacity: 0;
            transition: opacity 0.15s;
        }
        .reel-play-flash.show {
            opacity: 1;
            animation: flashFade 0.5s ease-out forwards;
        }
        @keyframes flashFade {
            0%   { opacity: 1; transform: translate(-50%,-50%) scale(1); }
            60%  { opacity: 0.7; transform: translate(-50%,-50%) scale(1.15); }
            100% { opacity: 0; transform: translate(-50%,-50%) scale(0.9); }
        }

        /* Ã–zel tema rengi */
        .theme-red    { --accent: #0ea5e9; --accent-light: #38bdf8; }
        .theme-blue   { --accent: #2563eb; --accent-light: #3b82f6; }
        .theme-green  { --accent: #16a34a; --accent-light: #22c55e; }
        .theme-purple { --accent: #7c3aed; --accent-light: #8b5cf6; }
        .theme-orange { --accent: #ea580c; --accent-light: #f97316; }
        .theme-pink   { --accent: #db2777; --accent-light: #ec4899; }
        body { --accent: #0ea5e9; --accent-light: #38bdf8; }

        @keyframes confettiFall {
            0%   { transform: translateY(0) rotate(0deg) scale(1); opacity: 1; }
            100% { transform: translateY(60vh) rotate(720deg) scale(0.3); opacity: 0; }
        }
        @keyframes scaleIn {
            0%   { opacity: 0; transform: scale(0.7); }
            70%  { transform: scale(1.04); }
            100% { opacity: 1; transform: scale(1); }
        }
        @keyframes bounce {
            0%   { transform: translateY(0px) scale(1); }
            100% { transform: translateY(-14px) scale(1.08); }
        }
        @keyframes wheelSpinGlow {
            0%,100% { box-shadow: 0 0 35px rgba(14,165,233,0.5), 0 0 60px rgba(234,179,8,0.2); }
            50%      { box-shadow: 0 0 55px rgba(234,179,8,0.9), 0 0 100px rgba(14,165,233,0.6), 0 0 8px rgba(255,255,255,0.4); }
        }
        @keyframes confettiRect {
            0%   { transform: translateY(0) rotate(0deg); opacity: 1; }
            100% { transform: translateY(70vh) rotate(900deg); opacity: 0; }
        }
        .wheel-spinning-canvas {
            animation: wheelSpinGlow 0.35s ease-in-out infinite !important;
        }
        @keyframes trialBanner {
            0%   { transform: translateY(-100%); opacity: 0; }
            15%  { transform: translateY(0); opacity: 1; }
            85%  { transform: translateY(0); opacity: 1; }
            100% { transform: translateY(-100%); opacity: 0; }
        }
        .trial-banner { animation: trialBanner 5s ease-in-out forwards; }
        .wheel-slice {
            position: absolute;
            top: 50%;
            left: 50%;
            width: 50%;
            height: 20px;
            transform-origin: 0% 50%;
            display: flex;
            align-items: center;
            justify-content: flex-end;
            padding-right: 15px;
            box-sizing: border-box;
            color: white;
            font-weight: 900;
            font-size: 10px;
            text-shadow: 1px 1px 3px black;
            text-transform: uppercase;
        }

        /* â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
           FREERIDER TR â€” BUZ CAM MAVÄ°SÄ° PREMIUM TEMA v3
           Ice Glass Blue Ultra Premium Edition
           â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â• */

        /* â”€â”€ Buz kristal doku efektleri â”€â”€ */
        @keyframes iceShimmer {
            0%   { background-position: -200% 0; }
            100% { background-position: 200% 0; }
        }
        @keyframes frostPulse {
            0%,100% { 
                box-shadow: 0 0 12px rgba(14,165,233,0.35), 0 0 24px rgba(56,189,248,0.12),
                            inset 0 0 20px rgba(56,189,248,0.04);
            }
            50% { 
                box-shadow: 0 0 24px rgba(14,165,233,0.55), 0 0 48px rgba(56,189,248,0.18),
                            inset 0 0 30px rgba(56,189,248,0.06);
            }
        }
        @keyframes iceGlow {
            0%,100% { filter: drop-shadow(0 0 4px rgba(56,189,248,0.6)); }
            50%      { filter: drop-shadow(0 0 10px rgba(56,189,248,0.9)); }
        }
        @keyframes crystalFloat {
            0%,100% { transform: translateY(0px) rotate(0deg); }
            33%     { transform: translateY(-4px) rotate(1deg); }
            66%     { transform: translateY(-2px) rotate(-1deg); }
        }
        @keyframes auroraShift {
            0%   { background-position: 0% 50%; }
            50%  { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        @keyframes frostLine {
            0%   { opacity: 0; transform: scaleX(0); }
            50%  { opacity: 1; transform: scaleX(1); }
            100% { opacity: 0; transform: scaleX(0); }
        }
        @keyframes iceRipple {
            0%   { transform: scale(0); opacity: 0.7; }
            100% { transform: scale(4); opacity: 0; }
        }
        @keyframes glacierPulse {
            0%,100% { opacity: 0.06; }
            50%     { opacity: 0.12; }
        }

        .ice-glow  { animation: iceGlow 2s ease-in-out infinite; }
        .frost-pulse { animation: frostPulse 3s ease-in-out infinite; }
        .crystal-float { animation: crystalFloat 4s ease-in-out infinite; }

        /* â”€â”€ Buz cam ultra glass panel (kaldÄ±rÄ±ldÄ± â€” line 559'daki son tanÄ±m aktif) â”€â”€ */

        /* â”€â”€ Buz shimmer efekti (Ã¶zel kartlar iÃ§in) â”€â”€ */
        .ice-shimmer-bg {
            background: linear-gradient(
                90deg,
                rgba(14,165,233,0.03) 0%,
                rgba(56,189,248,0.08) 30%,
                rgba(125,211,252,0.12) 50%,
                rgba(56,189,248,0.08) 70%,
                rgba(14,165,233,0.03) 100%
            );
            background-size: 200% 100%;
            animation: iceShimmer 4s linear infinite;
        }

        /* â”€â”€ Aurora arkaplan efekti â”€â”€ */
        body::before {
            content: '';
            position: fixed;
            inset: 0;
            background: 
                radial-gradient(ellipse 60% 40% at 20% 80%, rgba(14,165,233,0.04) 0%, transparent 60%),
                radial-gradient(ellipse 40% 30% at 80% 20%, rgba(56,189,248,0.03) 0%, transparent 60%);
            pointer-events: none;
            z-index: 0;
            animation: glacierPulse 6s ease-in-out infinite;
        }

        /* â”€â”€ Arka Plan Dokusu â”€â”€ */
        body {
            background:
                radial-gradient(ellipse 80% 50% at 50% -10%, rgba(2,132,199,0.18) 0%, transparent 60%),
                radial-gradient(ellipse 50% 30% at 85% 90%, rgba(120,0,0,0.12) 0%, transparent 50%),
                #000;
        }

        /* â”€â”€ GeliÅŸmiÅŸ Glass Panel â”€â”€ */
        .glass-panel {
            background: linear-gradient(135deg, rgba(18,18,22,0.92) 0%, rgba(10,10,14,0.96) 100%);
            backdrop-filter: blur(28px) saturate(200%);
            -webkit-backdrop-filter: blur(28px) saturate(200%);
            border: 1px solid rgba(255,255,255,0.06);
            box-shadow:
                0 24px 60px rgba(0,0,0,0.7),
                inset 0 1px 0 rgba(255,255,255,0.06),
                inset 0 -1px 0 rgba(0,0,0,0.4);
        }

        /* â”€â”€ App Header Gradient Border â”€â”€ */
        #main-app > div:first-child {
            background: linear-gradient(180deg, rgba(3,12,24,0.95) 0%, rgba(15,15,20,0.88) 100%);
            backdrop-filter: blur(20px);
            border-bottom: 1px solid transparent;
            background-clip: padding-box;
            box-shadow: 0 1px 0 rgba(14,165,233,0.35), 0 4px 20px rgba(0,0,0,0.5);
        }

        /* â”€â”€ FREERIDER markasÄ± parlar â”€â”€ */
        @keyframes brandPulse {
            0%,100% { text-shadow: 0 0 8px rgba(14,165,233,0.4); }
            50%      { text-shadow: 0 0 20px rgba(14,165,233,0.9), 0 0 40px rgba(14,165,233,0.3); }
        }
        #main-app .teko-font.text-2xl { animation: brandPulse 4s ease-in-out infinite; }

        /* â”€â”€ GeliÅŸmiÅŸ Bottom Nav (Floating Pill) â”€â”€ */
        #bottom-nav {
            background: linear-gradient(180deg, rgba(8,8,12,0.0) 0%, rgba(0,0,0,0.98) 100%) !important;
            border-top: none !important;
            box-shadow: none !important;
            padding-top: 4px;
            padding-bottom: max(12px, env(safe-area-inset-bottom));
        }
        #bottom-nav::before {
            content: '';
            position: absolute;
            inset: 0;
            border-top: 1px solid rgba(14,165,233,0.2);
            pointer-events: none;
        }
        #bottom-nav button {
            position: relative;
            border-radius: 14px;
            padding: 8px 10px 6px;
            transition: all 0.3s cubic-bezier(0.34,1.56,0.64,1);
        }
        #bottom-nav button.text-white {
            background: linear-gradient(135deg, rgba(2,132,199,0.35), rgba(120,0,0,0.2)) !important;
            box-shadow: 0 0 16px rgba(14,165,233,0.35), inset 0 1px 0 rgba(255,255,255,0.07);
        }
        #bottom-nav button.text-white span:first-child {
            filter: drop-shadow(0 0 6px rgba(14,165,233,0.8));
            transform: scale(1.15);
            display: inline-block;
        }
        #bottom-nav button span:first-child {
            transition: transform 0.3s cubic-bezier(0.34,1.56,0.64,1), filter 0.3s ease;
        }
        #bottom-nav button:active { transform: scale(0.88) !important; }

        /* â”€â”€ GeliÅŸmiÅŸ YÃ¼kleme EkranÄ± â”€â”€ */
        #app-loading-screen {
            background: radial-gradient(ellipse 70% 60% at 50% 40%, rgba(3,105,161,0.4) 0%, #000 70%);
        }

        /* â”€â”€ Animasyonlar â”€â”€ */
        @keyframes floatUp {
            0%,100% { transform: translateY(0px); }
            50%      { transform: translateY(-8px); }
        }
        @keyframes glowPulse {
            0%,100% { box-shadow: 0 0 15px rgba(14,165,233,0.4), 0 0 30px rgba(14,165,233,0.1); }
            50%      { box-shadow: 0 0 30px rgba(14,165,233,0.8), 0 0 60px rgba(14,165,233,0.3); }
        }
        @keyframes morphBorder {
            0%,100% { border-radius: 24px; }
            50%      { border-radius: 32px; }
        }
        @keyframes slideUpSpring {
            0%   { opacity:0; transform: translateY(32px) scale(0.95); }
            60%  { opacity:1; transform: translateY(-4px) scale(1.01); }
            100% { opacity:1; transform: translateY(0) scale(1); }
        }
        @keyframes fadeSlideLeft {
            0%   { opacity:0; transform: translateX(24px); }
            100% { opacity:1; transform: translateX(0); }
        }
        @keyframes fadeSlideRight {
            0%   { opacity:0; transform: translateX(-24px); }
            100% { opacity:1; transform: translateX(0); }
        }
        @keyframes cardEnter {
            0%   { opacity:0; transform: translateY(20px) scale(0.96); }
            70%  { opacity:1; transform: translateY(-2px) scale(1.01); }
            100% { opacity:1; transform: translateY(0) scale(1); }
        }
        @keyframes shimmerSweep {
            0%   { background-position: -200% 0; }
            100% { background-position: 200% 0; }
        }
        @keyframes neonBlink {
            0%,95%,100% { opacity:1; }
            97%          { opacity:0.6; }
        }
        @keyframes iconBounce {
            0%,100% { transform: translateY(0) rotate(0deg); }
            25%     { transform: translateY(-5px) rotate(-8deg); }
            75%     { transform: translateY(-3px) rotate(6deg); }
        }
        @keyframes scanline {
            0%   { transform: translateY(-100%); }
            100% { transform: translateY(100vh); }
        }
        @keyframes gradientShift {
            0%   { background-position: 0% 50%; }
            50%  { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        .float-anim   { animation: floatUp 3s ease-in-out infinite; }
        .glow-pulse   { animation: glowPulse 2.5s ease-in-out infinite; }
        .card-enter   { animation: cardEnter 0.45s cubic-bezier(0.34,1.56,0.64,1) both; }
        .slide-up-anim { animation: slideUpSpring 0.5s cubic-bezier(0.34,1.3,0.64,1) both; }
        .scale-in-anim { animation: slideUpSpring 0.4s cubic-bezier(0.34,1.56,0.64,1) both; }

        /* â”€â”€ GeliÅŸmiÅŸ Buton Hover â”€â”€ */
        .btn-premium-hover {
            transition: all 0.25s cubic-bezier(0.34,1.2,0.64,1);
            position: relative;
            overflow: hidden;
        }
        .btn-premium-hover::before {
            content: '';
            position: absolute;
            inset: 0;
            background: linear-gradient(135deg, rgba(255,255,255,0.06) 0%, transparent 50%, rgba(255,255,255,0.02) 100%);
            opacity: 0;
            transition: opacity 0.2s;
            pointer-events: none;
            border-radius: inherit;
        }
        .btn-premium-hover:hover::before { opacity: 1; }
        .btn-premium-hover:hover {
            transform: translateY(-2px) scale(1.02);
            box-shadow: 0 8px 24px rgba(14,165,233,0.4), 0 2px 8px rgba(0,0,0,0.4);
        }
        .btn-premium-hover:active {
            transform: translateY(1px) scale(0.97);
            box-shadow: 0 2px 8px rgba(14,165,233,0.2);
        }
        .btn-premium-hover::after {
            content: '';
            position: absolute;
            top: 50%; left: 50%;
            width: 4px; height: 4px;
            background: rgba(255,255,255,0.6);
            border-radius: 50%;
            transform: scale(0); opacity: 0;
            pointer-events: none;
        }
        .btn-premium-hover:active::after { animation: ripple 0.5s ease-out forwards; }

        /* â”€â”€ Shimmer Loading Skeleton â”€â”€ */
        .skeleton {
            background: linear-gradient(90deg, #0a1525 25%, #0d1e36 50%, #0a1525 75%);
            background-size: 200% 100%;
            animation: shimmerSweep 1.5s infinite;
            border-radius: 8px;
        }

        /* â”€â”€ Gradient Progress Bar â”€â”€ */
        .progress-bar-fill {
            background: linear-gradient(90deg, #0ea5e9, #f97316, #eab308) !important;
            background-size: 200% 100%;
            animation: gradientShift 2s ease infinite;
            box-shadow: 0 0 8px rgba(14,165,233,0.5);
        }

        /* â”€â”€ Kart Hover Efekti â”€â”€ */
        .hover-card {
            transition: all 0.3s cubic-bezier(0.4,0,0.2,1);
        }
        .hover-card:hover {
            transform: translateY(-3px) scale(1.01);
            box-shadow: 0 16px 40px rgba(0,0,0,0.5), 0 0 0 1px rgba(255,255,255,0.06);
        }

        /* â”€â”€ Modal Backdrop GeliÅŸmiÅŸ â”€â”€ */
        .modal-backdrop {
            background: rgba(0,0,0,0.82);
            backdrop-filter: blur(12px) saturate(150%);
            -webkit-backdrop-filter: blur(12px) saturate(150%);
        }

        /* â”€â”€ Ã–zel Scrollbar â”€â”€ */
        .custom-scrollbar::-webkit-scrollbar { width: 3px; }
        .custom-scrollbar::-webkit-scrollbar-track { background: rgba(0,0,0,0.2); }
        .custom-scrollbar::-webkit-scrollbar-thumb {
            background: linear-gradient(180deg, #0ea5e9, #0c4a6e);
            border-radius: 3px;
        }

        /* â”€â”€ Input Glow Focus â”€â”€ */
        input:focus, textarea:focus, select:focus {
            box-shadow: 0 0 0 2px rgba(14,165,233,0.3), 0 0 12px rgba(14,165,233,0.15) !important;
            border-color: rgba(14,165,233,0.7) !important;
        }

        /* â”€â”€ Sidebar GeliÅŸmiÅŸ â”€â”€ */
        #sidebar {
            background: linear-gradient(180deg, rgba(2,6,16,0.98) 0%, rgba(5,5,8,0.99) 100%) !important;
            border-right: 1px solid rgba(14,165,233,0.2) !important;
            box-shadow: 4px 0 40px rgba(0,0,0,0.8) !important;
        }
        #sidebar button.tab-btn {
            transition: all 0.25s cubic-bezier(0.4,0,0.2,1);
            border-left: 2px solid transparent;
        }
        #sidebar button.tab-btn:hover {
            background: rgba(14,165,233,0.08) !important;
            border-left-color: rgba(14,165,233,0.5);
            transform: translateX(3px);
        }
        #sidebar button.bg-zinc-900 {
            background: linear-gradient(135deg, rgba(2,132,199,0.25), rgba(3,105,161,0.15)) !important;
            border-left: 2px solid rgba(14,165,233,0.7);
            box-shadow: inset 0 1px 0 rgba(255,255,255,0.04);
        }

        /* â”€â”€ Profil KartÄ± Efekti â”€â”€ */
        #screen-profile .glass-panel {
            border: 1px solid rgba(255,255,255,0.07);
            transition: border-color 0.3s ease;
        }
        #screen-profile .glass-panel:hover {
            border-color: rgba(14,165,233,0.2);
        }

        /* â”€â”€ Leaderboard Row â”€â”€ */
        @keyframes goldShine {
            0%,100% { box-shadow: 0 0 10px rgba(251,191,36,0.3); }
            50%      { box-shadow: 0 0 20px rgba(251,191,36,0.7), 0 0 40px rgba(251,191,36,0.2); }
        }

        /* â”€â”€ Toast Bildirimleri â”€â”€ */
        @keyframes toastSlide {
            0%   { opacity:0; transform: translateX(-50%) translateY(-20px) scale(0.9); }
            60%  { opacity:1; transform: translateX(-50%) translateY(4px) scale(1.02); }
            100% { opacity:1; transform: translateX(-50%) translateY(0) scale(1); }
        }

        /* â”€â”€ Reel Kart Overlay Gradient â”€â”€ */
        #reels-feed .absolute.inset-0 {
            background: linear-gradient(
                to top,
                rgba(0,0,0,0.88) 0%,
                rgba(0,0,0,0.3) 40%,
                transparent 70%
            ) !important;
        }

        /* â”€â”€ Story Ring GeliÅŸmiÅŸ â”€â”€ */
        .story-ring {
            animation: storyRing 2.5s ease-in-out infinite;
            box-shadow: 0 0 12px rgba(14,165,233,0.4);
        }

        /* â”€â”€ bg-glass GeliÅŸmiÅŸ â”€â”€ */
        .bg-glass {
            background: rgba(4, 10, 24, 0.88) !important;
            backdrop-filter: blur(20px) saturate(180%) !important;
            -webkit-backdrop-filter: blur(20px) saturate(180%) !important;
            border-color: rgba(255,255,255,0.06) !important;
        }

        /* â”€â”€ bg-darker â”€â”€ */
        .bg-darker {
            background: linear-gradient(180deg, #03080f 0%, #020609 100%) !important;
        }

        /* â”€â”€ DalgalÄ± Separator â”€â”€ */
        .wave-sep {
            height: 1px;
            background: linear-gradient(90deg, transparent, rgba(14,165,233,0.5), rgba(251,191,36,0.3), rgba(14,165,233,0.5), transparent);
            margin: 16px 0;
        }

        /* â”€â”€ YÃ¼kleme Animasyonu GeliÅŸmiÅŸ â”€â”€ */
        @keyframes loadRing {
            0%   { transform: rotate(0deg) scale(1); }
            50%  { transform: rotate(180deg) scale(1.05); }
            100% { transform: rotate(360deg) scale(1); }
        }
        #app-loading-screen .animate-spin {
            animation: loadRing 1.2s cubic-bezier(0.4,0,0.6,1) infinite !important;
            box-shadow: 0 0 20px rgba(14,165,233,0.6);
        }

        /* â”€â”€ Harita Overlay Gradient â”€â”€ */
        #screen-map::after {
            content: '';
            position: absolute;
            bottom: 0; left: 0; right: 0;
            height: 60px;
            background: linear-gradient(to top, rgba(2,8,22,0.4), transparent);
            pointer-events: none;
            z-index: 5;
        }

        /* â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
           OVERFLOW & TAÅMA DÃœZELTMELERÄ°
           â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â• */

        /* Global overflow kontrol */
        *, *::before, *::after {
            box-sizing: border-box;
        }

        /* Flex child taÅŸma engelleyici */
        .flex > * { min-width: 0; }
        .flex-1   { min-width: 0; }

        /* Text taÅŸma Ã¶nleme */
        .truncate-safe {
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
            min-width: 0;
        }

        /* Ä°Ã§erik taÅŸma engel */
        #screen-chat, #screen-leaderboard, #screen-profile,
        #screen-market, #screen-news, #screen-missions,
        #screen-reels, #screen-plus, #screen-invite {
            overflow-x: hidden !important;
            overflow-y: auto !important;
        }

        /* Mesaj balonlarÄ± taÅŸma engeli */
        .chat-bubble-wrap {
            max-width: calc(100% - 60px) !important;
            overflow-wrap: break-word !important;
            word-break: break-word !important;
        }

        /* Resim taÅŸma engeli */
        img {
            max-width: 100%;
            height: auto;
        }

        /* Modal iÃ§i overflow */
        .glass-panel {
            max-width: calc(100vw - 32px) !important;
            overflow-x: hidden !important;
        }

        /* KullanÄ±cÄ± adÄ± taÅŸma */
        [id$="-username"], .username-text {
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
            max-width: 100%;
        }

        /* Yatay scroll container'lar */
        .horizontal-scroll-container {
            overflow-x: auto !important;
            overflow-y: hidden !important;
            max-width: 100% !important;
        }

        /* Grid ve flex taÅŸma */
        .grid { overflow: hidden; }

        /* Bottom nav gÃ¼venli alan */
        #bottom-nav {
            width: 100% !important;
            max-width: 100% !important;
            overflow: hidden !important;
        }

        /* Ana konteyner taÅŸma engeli */
        .max-w-md {
            overflow-x: hidden !important;
        }

        /* Toast overflow fix */
        #toast-notification {
            max-width: calc(100vw - 32px) !important;
            left: 50% !important;
            transform: translateX(-50%) !important;
        }
    </style>
</head>
<body class="h-[100dvh] w-full overflow-hidden bg-black relative">
    <!-- Premium YÃ¼kleme EkranÄ± v2 -->
    <div id="app-loading-screen" class="fixed inset-0 z-[9999] flex flex-col items-center justify-center" style="position: fixed; top: 0; left: 0; right: 0; bottom: 0; z-index: 9999; display: flex; flex-direction: column; align-items: center; justify-content: center; background: radial-gradient(ellipse 70% 60% at 50% 40%, rgba(3,105,161,0.5) 0%, #000 70%); transition: opacity 0.6s ease; background-color: #000;">
        <!-- Arka dekor halkalar - buz kristal efekti -->
        <div class="absolute w-96 h-96 rounded-full" style="border:1px solid rgba(56,189,248,0.06);animation:ping 4s cubic-bezier(0,0,0.2,1) infinite;animation-delay:0.6s"></div>
        <div class="absolute w-64 h-64 rounded-full border border-sky-700/20 animate-ping" style="animation-duration:2.5s;box-shadow:0 0 20px rgba(14,165,233,0.05)"></div>
        <div class="absolute w-48 h-48 rounded-full border border-sky-600/25 animate-ping" style="animation-duration:2s;animation-delay:0.3s;box-shadow:0 0 15px rgba(56,189,248,0.08)"></div>
        <!-- Logo container -->
        <div class="relative mb-8 z-10">
            <div class="w-24 h-24 rounded-full border-[3px] border-transparent" style="background:conic-gradient(from 0deg,#0ea5e9,#f97316,#eab308,#0ea5e9);padding:3px;border-radius:50%;box-shadow:0 0 40px rgba(14,165,233,0.6),0 0 80px rgba(14,165,233,0.2);">
                <div class="w-full h-full rounded-full bg-black flex items-center justify-center">
                    <span class="text-3xl" style="filter:drop-shadow(0 0 8px rgba(14,165,233,0.8))">ğŸ”ï¸</span>
                </div>
            </div>
            <!-- DÃ¶nen halkalar -->
            <div class="absolute inset-0 animate-spin" style="animation-duration:1.5s;">
                <div class="w-24 h-24 rounded-full border-t-2 border-r-2 border-sky-400/60 border-b-transparent border-l-transparent" style="filter:blur(0.5px)"></div>
            </div>
            <div class="absolute inset-0 animate-spin" style="animation-duration:2.2s;animation-direction:reverse;">
                <div class="w-24 h-24 rounded-full border-t-transparent border-r-transparent border-b-2 border-l-2 border-cyan-400/50" style="filter:blur(0.5px)"></div>
            </div>
        </div>
        <!-- Brand -->
        <div class="z-10 text-center">
            <div class="teko-font text-white text-5xl tracking-[0.15em] drop-shadow-xl" style="text-shadow:0 0 30px rgba(14,165,233,0.7)">FREERIDER<span style="color:#0ea5e9;text-shadow:0 0 20px #0ea5e9,0 0 40px #0ea5e9aa;">TR</span></div>
            <div class="flex items-center justify-center gap-2 mt-3">
                <div class="h-px w-12 bg-gradient-to-r from-transparent to-sky-500/60"></div>
                <div class="text-zinc-400 text-[10px] uppercase tracking-[0.3em] font-bold animate-pulse">YÃ¼kleniyor</div>
                <div class="h-px w-12 bg-gradient-to-l from-transparent to-sky-500/60"></div>
            </div>
            <div class="flex justify-center gap-1 mt-3">
                <div class="w-1.5 h-1.5 bg-sky-400 rounded-full animate-bounce" style="animation-delay:0s"></div>
                <div class="w-1.5 h-1.5 bg-sky-300 rounded-full animate-bounce" style="animation-delay:0.15s"></div>
                <div class="w-1.5 h-1.5 bg-cyan-300 rounded-full animate-bounce" style="animation-delay:0.3s"></div>
            </div>
        </div>
    </div>
    <audio id="notif-sound" src="https://cdn.freesound.org/previews/256/256113_3263906-lq.mp3" preload="auto"></audio>
    <input type="file" id="chat-photo-upload" accept="image/*" class="hidden" onchange="handleChatPhotoUpload(this)">

    <div id="sidebar-overlay" class="hidden fixed inset-0 modal-backdrop z-[1000] backdrop-blur-sm transition-opacity duration-300" onclick="toggleSidebar()"></div>
    <div id="sidebar" class="fixed inset-y-0 left-0 w-64 bg-zinc-950 border-r border-zinc-800 z-[1001] transform -translate-x-full transition-transform duration-500 cubic-bezier(0.16, 1, 0.3, 1) flex flex-col shadow-2xl glass-panel">
        <div class="p-5 border-b border-zinc-800 flex items-center gap-3 shrink-0">
            <span class="text-3xl drop-shadow-lg">ğŸ”ï¸</span>
            <span class="teko-font text-white text-3xl tracking-widest font-bold mt-1">MENÃœ</span>
          <button onclick="toggleSidebar()" class="bg-zinc-800/80 hover:bg-zinc-700 transition px-3 py-1 rounded-xl text-white text-2xl mr-2 border border-zinc-700 focus:outline-none shadow-md">â˜°</button>
        </div>
        <div class="flex-1 overflow-y-auto py-4 flex flex-col gap-2 px-3 custom-scrollbar">
            <button id="tab-btn-0" onclick="switchTab(0)" class="w-full py-3 px-4 flex items-center gap-4 text-white bg-zinc-900 rounded-xl tab-btn font-bold transition-all"><span class="text-xl w-6 text-center">ğŸ—ºï¸</span> Harita</button>
            <button id="tab-btn-1" onclick="switchTab(1)" class="w-full py-3 px-4 flex items-center gap-4 text-zinc-500 hover:bg-zinc-900/50 rounded-xl tab-btn font-bold transition-all"><span class="text-xl w-6 text-center">ğŸ’¬</span> Chat</button>
            <button id="tab-btn-2" onclick="switchTab(2)" class="w-full py-3 px-4 flex items-center gap-4 text-zinc-500 hover:bg-zinc-900/50 rounded-xl tab-btn font-bold transition-all"><span class="text-xl w-6 text-center">ğŸ›’</span> Pazar</button>
            <button id="tab-btn-3" onclick="switchTab(3)" class="w-full py-3 px-4 flex items-center gap-4 text-zinc-500 hover:bg-zinc-900/50 rounded-xl tab-btn font-bold transition-all"><span class="text-xl w-6 text-center">ğŸ†</span> Lider Tablosu</button>
            <button id="tab-btn-4" onclick="switchTab(4)" class="w-full py-3 px-4 flex items-center gap-4 text-zinc-500 hover:bg-zinc-900/50 rounded-xl tab-btn font-bold transition-all"><span class="text-xl w-6 text-center">ğŸ“°</span> Haberler</button>
            <button id="tab-btn-5" onclick="switchTab(5)" class="w-full py-3 px-4 flex items-center gap-4 text-zinc-500 hover:bg-zinc-900/50 rounded-xl tab-btn font-bold transition-all"><span class="text-xl w-6 text-center">ğŸ¯</span> GÃ¶revler ve Ã‡ark</button>
            <button id="tab-btn-9" onclick="switchTab(9)" class="w-full py-3 px-4 flex items-center gap-4 text-pink-400 hover:bg-pink-900/20 border border-transparent hover:border-pink-500/30 rounded-xl tab-btn font-bold transition-all"><span class="text-xl w-6 text-center">ğŸ¬</span> Reels</button>
            <button id="tab-btn-8" onclick="switchTab(8)" class="w-full py-3 px-4 flex items-center gap-4 text-purple-400 hover:bg-purple-900/30 border border-transparent hover:border-purple-500/30 rounded-xl tab-btn font-bold transition-all"><span class="text-xl w-6 text-center drop-shadow-[0_0_10px_purple]">ğŸ¤</span> Davet Et Kazan</button>
            <button id="tab-btn-6" onclick="switchTab(6)" class="w-full py-3 px-4 flex items-center gap-4 text-yellow-500 hover:bg-yellow-900/30 border border-transparent hover:border-yellow-500/30 rounded-xl tab-btn font-bold transition-all"><span class="text-xl w-6 text-center drop-shadow-[0_0_10px_yellow]">ğŸŒŸ</span> Freerider Plus</button>
            <button id="tab-btn-7" onclick="switchTab(7)" class="w-full py-3 px-4 flex items-center gap-4 text-zinc-500 hover:bg-zinc-900/50 rounded-xl tab-btn font-bold transition-all"><span class="text-xl w-6 text-center">ğŸ‘¤</span> Profilim</button>
        </div>
        <div id="sidebar-weather" class="mx-3 mb-2 rounded-2xl px-4 py-3 border border-zinc-800 bg-zinc-900/60 hidden">
            <div class="text-[9px] font-black uppercase tracking-widest text-zinc-500 mb-1">HAVA DURUMU</div>
            <div id="sidebar-weather-content" class="flex items-center gap-2">
                <span id="sidebar-weather-icon" class="text-2xl">â³</span>
                <div>
                    <div id="sidebar-weather-temp" class="text-white font-black text-sm teko-font"></div>
                    <div id="sidebar-weather-desc" class="text-zinc-400 text-[10px] font-bold"></div>
                </div>
            </div>
        </div>
        <div class="p-4 border-t border-zinc-800 flex flex-col gap-2">
                <button onclick="document.getElementById('social-modal').classList.remove('hidden'); toggleSidebar();" class="w-full bg-zinc-900 border border-pink-700/40 hover:bg-pink-900/20 transition text-pink-400 py-3 rounded-xl font-bold text-xs tracking-widest flex items-center justify-center gap-2">
                    <span>ğŸ“¸</span> HesaplarÄ±mÄ±zÄ± Takip Et
                </button>
                <button onclick="window.open('https://whatsapp.com/channel/0029VbCTLFCJUM2kLBD7TC1Z', '_blank')" class="w-full bg-zinc-900 border border-green-700/40 hover:bg-green-900/20 transition text-green-400 py-3 rounded-xl font-bold text-xs tracking-widest flex items-center justify-center gap-2">
                    <span>ğŸ’¬</span> WP KanalÄ±
                </button>
                <button onclick="openSupportModal(); toggleSidebar();" class="w-full bg-zinc-900 border border-blue-700/40 hover:bg-blue-900/20 transition text-blue-400 py-3 rounded-xl font-bold text-xs tracking-widest flex items-center justify-center gap-2">
                    <span>ğŸ§</span> Destek & Geri Bildirim
                </button>

            </div>
    </div>

    <div class="max-w-md mx-auto h-[100dvh] flex flex-col shadow-2xl bg-darker border-x border-zinc-900/50 relative overflow-x-hidden">
        <div id="login-screen" class="flex-1 flex flex-col overflow-y-auto z-50 relative slide-up-anim">
            <video autoplay loop muted playsinline class="absolute inset-0 w-full h-full object-cover z-0 opacity-40">
                <source src="https://cdn.freeridertr.com.tr/video%20ana/istockphoto-2221026101-640_adpp_is.mp4">
            </video>
            
            <div class="absolute inset-0 bg-gradient-to-b from-black/90 via-black/60 to-[#020b19] z-0"></div>

            <div class="flex flex-col items-center justify-center pt-16 pb-8 relative z-10 shrink-0">
                <a href="https://instagram.com/om3r_10fr" target="_blank" class="absolute top-4 right-4 bg-sky-900/80 text-white text-[11px] font-bold py-2 px-4 rounded-full flex items-center gap-2 z-20 border border-sky-400/50 shadow-[0_0_15px_rgba(14,165,233,0.5)] btn-premium-hover">
                    <span class="text-white">ğŸ“¸</span> Takip Et
                </a>
                
                <div class="text-center flex flex-col items-center scale-in-anim">
                    <div class="w-24 h-24 mx-auto rounded-full overflow-hidden border-4 border-sky-500 shadow-[0_0_40px_rgba(14,165,233,0.8)] relative mb-4 bg-zinc-950 flex justify-center items-center">
                        <span class="text-5xl drop-shadow-lg">ğŸ”ï¸</span>
                    </div>
                    <h1 class="teko-font text-6xl text-white tracking-widest drop-shadow-[0_10px_10px_rgba(0,0,0,1)]">FREERIDER<span class="text-sky-500">TR</span></h1>
                    <p class="text-zinc-300 text-xs uppercase tracking-widest mt-2 font-black drop-shadow-md">HARDCORE DOWNHILL TOPLULUÄU</p>
                </div>
            </div>
            
            <!-- KullanÄ±cÄ± Ä°statistikleri Ã‡ubuÄŸu -->
            <div class="relative z-10 px-6 mb-3">
                <div class="flex items-center justify-center gap-4 bg-black/60 border border-zinc-800 rounded-2xl px-5 py-3 backdrop-blur-md">
                    <div class="flex items-center gap-2">
                        <div class="w-2 h-2 rounded-full bg-green-500 animate-pulse shadow-[0_0_6px_rgba(34,197,94,0.8)]"></div>
                        <div class="text-center">
                            <div id="login-active-users" class="text-green-400 font-black text-lg teko-font leading-none">--</div>
                            <div class="text-[9px] text-zinc-500 uppercase tracking-widest font-bold">Aktif</div>
                        </div>
                    </div>
                    <div class="w-px h-8 bg-zinc-700"></div>
                    <div class="flex items-center gap-2">
                        <span class="text-lg">ğŸ‘¥</span>
                        <div class="text-center">
                            <div id="login-total-users" class="text-white font-black text-lg teko-font leading-none">--</div>
                            <div class="text-[9px] text-zinc-500 uppercase tracking-widest font-bold">Toplam Ãœye</div>
                        </div>
                    </div>
                    <div class="w-px h-8 bg-zinc-700"></div>
                    <div class="flex items-center gap-2">
                        <span class="text-lg">ğŸ”ï¸</span>
                        <div class="text-center">
                            <div class="text-sky-300 font-black text-lg teko-font leading-none">TR#1</div>
                            <div class="text-[9px] text-zinc-500 uppercase tracking-widest font-bold">Platform</div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="p-6 flex-1 relative z-10 flex flex-col justify-end pb-12">
                <div class="glass-panel p-6 rounded-3xl">
                    <div class="flex bg-zinc-900/80 rounded-xl p-1 mb-8 shadow-inner border border-zinc-800">
                        <button onclick="showLoginTab()" id="login-tab-btn" class="flex-1 py-3 bg-gradient-to-r from-sky-700 to-sky-500 text-white rounded-lg font-black text-sm shadow-[0_0_15px_rgba(2,132,199,0.5)] tracking-widest uppercase transition-all">GÄ°RÄ°Å YAP</button>
                        <button onclick="showRegisterTab()" id="register-tab-btn" class="flex-1 py-3 bg-transparent text-zinc-400 rounded-lg font-bold text-sm tracking-widest uppercase transition-all hover:text-white">KAYIT OL</button>
                    </div>
                    
                    <div id="login-form" class="scale-in-anim">
                        <input id="login-username" type="text" placeholder="KullanÄ±cÄ± AdÄ±" class="w-full bg-black/50 border border-zinc-700 rounded-xl px-5 py-4 mb-3 outline-none text-white focus:border-sky-500 focus:bg-black/80 transition-all font-bold">
                        <input id="login-password" type="password" placeholder="Åifre" class="w-full bg-black/50 border border-zinc-700 rounded-xl px-5 py-4 mb-4 outline-none text-white focus:border-sky-500 focus:bg-black/80 transition-all font-bold">
                        
                        <div class="flex justify-between items-center mb-8 px-1">
                            <div class="flex items-center gap-2">
                                <input type="checkbox" id="remember-me" class="w-4 h-4 accent-sky-500 rounded cursor-pointer" checked>
                                <label for="remember-me" class="text-xs text-zinc-400 font-bold cursor-pointer uppercase tracking-wider">SavaÅŸa HazÄ±r (HatÄ±rla)</label>
                            </div>
                            <a href="javascript:void(0)" onclick="openForgotPasswordModal()" class="text-xs text-blue-400 hover:text-blue-300 transition hover:underline">Åifremi Unuttum?</a>
                        </div>
                        
                        <button onclick="handleLogin()" class="w-full bg-gradient-to-r from-sky-700 to-sky-500 btn-premium-hover text-white py-4 rounded-xl font-black shadow-[0_0_20px_rgba(14,165,233,0.6)] text-lg tracking-widest">SÄ°STEME DAL</button>
                    </div>
                    
                    <div id="register-form" class="hidden scale-in-anim">
                        <input id="reg-name" type="text" placeholder="Ad Soyad" class="w-full bg-black/50 border border-zinc-700 rounded-xl px-5 py-4 mb-3 outline-none text-white focus:border-sky-500 transition-all font-bold">
                        <input id="reg-username" type="text" placeholder="KullanÄ±cÄ± AdÄ±" class="w-full bg-black/50 border border-zinc-700 rounded-xl px-5 py-4 mb-3 outline-none text-white focus:border-sky-500 transition-all font-bold">
                        <input id="reg-city" type="text" placeholder="Åehir" class="w-full bg-black/50 border border-zinc-700 rounded-xl px-5 py-4 mb-3 outline-none text-white focus:border-sky-500 transition-all font-bold">
                        <input id="reg-password" type="password" placeholder="Åifre" class="w-full bg-black/50 border border-zinc-700 rounded-xl px-5 py-4 mb-3 outline-none text-white focus:border-sky-500 transition-all font-bold">
                        
                        <input id="reg-email" type="email" placeholder="E-posta (@gmail.com â€” Ä°steÄŸe BaÄŸlÄ±)" class="w-full bg-black/50 border border-zinc-700 rounded-xl px-5 py-4 mb-1 outline-none text-white focus:border-sky-500 transition-all font-bold">
                        <div class="mb-3 px-1 space-y-1">
                            <p class="text-[10px] text-yellow-400/80 leading-tight">âš ï¸ <b>Gmail girmezsen ÅŸifreni sÄ±fÄ±rlayamazsÄ±n.</b> Daha sonra profil ayarlarÄ±ndan ekleyebilirsin.</p>
                            <p class="text-[10px] text-zinc-500 leading-tight">Referans kodu kullanmak iÃ§in @gmail.com zorunludur.</p>
                        </div>

                        <input id="reg-ref-code" type="text" placeholder="Referans Kodu (Ä°steÄŸe BaÄŸlÄ±)" class="w-full bg-black/50 border border-purple-500/50 rounded-xl px-5 py-4 mb-3 outline-none text-purple-100 focus:border-purple-400 focus:shadow-[0_0_15px_rgba(168,85,247,0.3)] transition-all font-bold" oninput="checkRefCodeInput()">
                        
                        <div id="reg-ref-reward-container" class="hidden mb-3 p-4 bg-purple-900/30 border border-purple-500/50 rounded-xl backdrop-blur-sm">
                            <p class="text-[10px] text-purple-300 font-bold uppercase tracking-widest mb-2 flex items-center gap-2"><span class="animate-pulse">ğŸ</span> Referans Ã–dÃ¼lÃ¼nÃ¼ SeÃ§</p>
                            <select id="reg-ref-reward" class="w-full bg-black/80 border border-purple-700 rounded-lg px-3 py-3 text-white text-sm outline-none focus:border-purple-400 transition cursor-pointer">
                                <option value="xp_500">ğŸŒŸ 500 BaÅŸlangÄ±Ã§ XP'si</option>
                                <option value="prem_dlx_2">ğŸ”¥ 2 GÃ¼n Deluxe Premium</option>
                                <option value="prem_ult_1">ğŸ‘‘ 1 GÃ¼n Ultra+ Premium</option>
                                <option value="prem_std_7">â­ 1 Hafta Standart Premium</option>
                            </select>
                        </div>
                        
                        <div class="flex items-start gap-2 mb-3 px-1">
                            <input type="checkbox" id="reg-marketing" class="w-4 h-4 mt-0.5 accent-sky-500 rounded cursor-pointer">
                            <label for="reg-marketing" class="text-xs text-zinc-400 font-medium cursor-pointer hover:text-white transition">
                                Haberlerden ve gÃ¼ncellemelerden haberdar olmak istiyorum.
                            </label>
                        </div>
                        
                        <div class="flex items-start gap-2 mb-3 px-1 border-t border-zinc-800 pt-3">
                            <input type="checkbox" id="reg-kvkk" class="w-4 h-4 mt-0.5 accent-sky-500 rounded cursor-pointer">
                            <label for="reg-kvkk" class="text-xs text-zinc-400 font-medium cursor-pointer hover:text-white transition">
                                <a onclick="openKvkkModal()" class="text-sky-400 hover:text-sky-300 underline font-bold transition">KullanÄ±cÄ± SÃ¶zleÅŸmesi ve KVKK</a> metnini okudum, kabul ediyorum.
                            </label>
                        </div>
                        <div class="flex items-start gap-2 mb-6 px-1">
                            <input type="checkbox" id="reg-privacy" class="w-4 h-4 mt-0.5 accent-sky-500 rounded cursor-pointer">
                            <label for="reg-privacy" class="text-xs text-zinc-400 font-medium cursor-pointer hover:text-white transition">
                                <a href="/privacy-policy" target="_blank" class="text-blue-400 hover:text-blue-300 underline font-bold transition">Gizlilik SÃ¶zleÅŸmesi</a> ve <a href="/terms" target="_blank" class="text-blue-400 hover:text-blue-300 underline font-bold transition">KullanÄ±m ÅartlarÄ±</a>'nÄ± okudum, kabul ediyorum.
                            </label>
                        </div>
                        
                        <button onclick="handleRegister()" class="w-full bg-gradient-to-r from-sky-700 to-sky-500 btn-premium-hover text-white py-4 rounded-xl font-black shadow-[0_0_20px_rgba(14,165,233,0.6)] text-lg tracking-widest">ARAMIZA KATIL</button>
                    </div>


                    
                </div>
            </div>
        </div>

        <div id="main-app" class="hidden flex flex-col h-[100dvh] w-full slide-up-anim">
            <!-- â”€â”€ PREMIUM HEADER â”€â”€ -->
            <div class="px-4 py-2.5 flex items-center justify-between z-[100] shrink-0 gap-2" style="background:linear-gradient(180deg,rgba(2,8,18,0.97) 0%,rgba(8,8,12,0.95) 100%);backdrop-filter:blur(20px);-webkit-backdrop-filter:blur(20px);border-bottom:1px solid rgba(14,165,233,0.2);box-shadow:0 1px 0 rgba(14,165,233,0.1),0 4px 24px rgba(0,0,0,0.5);">
                <!-- Sol: Hamburger + Logo -->
                <div class="flex items-center gap-2 min-w-0 flex-1">
                    <button onclick="toggleSidebar()" class="w-9 h-9 flex items-center justify-center rounded-xl text-zinc-300 hover:text-white transition-all hover:bg-white/5 active:scale-90 shrink-0" style="font-size:18px">â˜°</button>
                    <div class="flex items-center gap-1 ml-0.5 min-w-0">
                        <span class="text-lg shrink-0" style="filter:drop-shadow(0 0 6px rgba(14,165,233,0.7))">ğŸ”ï¸</span>
                        <span class="teko-font text-white tracking-widest font-bold truncate" style="font-size:19px;letter-spacing:0.10em;text-shadow:0 0 15px rgba(14,165,233,0.4)">FREERIDER<span style="color:#38bdf8;text-shadow:0 0 10px #38bdf8">TR</span></span>
                    </div>
                </div>
                <!-- SaÄŸ: KullanÄ±cÄ± AdÄ± + Avatar (shrink-0 ile ezilmez) -->
                <div onclick="switchTab(7)" class="flex items-center gap-2 cursor-pointer group shrink-0" style="transition:all 0.2s">
                    <div class="text-right group-hover:opacity-80 transition-opacity">
                        <div id="top-username" class="font-bold text-sm text-white transition-all leading-tight truncate max-w-[90px]"></div>
                        <div id="top-title" class="text-[9px] font-black uppercase text-zinc-500 tracking-widest leading-tight"></div>
                    </div>
                    <div class="relative shrink-0">
                        <div class="w-9 h-9 rounded-full overflow-hidden shadow-lg transition-all group-hover:scale-105" style="border:2px solid rgba(14,165,233,0.5);box-shadow:0 0 12px rgba(14,165,233,0.3);">
                            <img id="top-avatar" src="" class="w-full h-full object-cover" onerror="this.src='https://cdn.freeridertr.com.tr/profil%20resmi/unnamed.jpg'">
                        </div>
                    </div>
                </div>
            </div>

            <div class="flex-1 relative overflow-hidden bg-zinc-950 z-0">
                <div id="screen-map" class="absolute inset-0 flex flex-col z-10 slide-up-anim">
                    <div class="absolute top-4 left-4 flex flex-col gap-2 z-[999]">
                        <button onclick="showNearbyRoutes()" title="YakÄ±n Rotalar"
                            class="bg-glass rounded-full border border-zinc-700/50 shadow-xl backdrop-blur-md hover:bg-zinc-800 btn-premium-hover flex items-center gap-1.5 px-3 py-2 mb-2"><span class="text-lg">ğŸ“</span><span class="text-[9px] text-white font-bold uppercase tracking-widest">YakÄ±n Rotalar</span></button>
                        
                        <!-- Map Filter UI KaldÄ±rÄ±ldÄ± (KullanÄ±cÄ± talebi) -->
                    </div>

                    <!-- Hava durumu widget haritadan kaldÄ±rÄ±ldÄ± â€” sidebar'da gÃ¶rÃ¼nÃ¼yor -->
                    <div id="weather-widget" style="display:none!important;" class="hidden">
                        <div id="weather-icon"></div>
                        <div>
                            <div id="weather-temp"></div>
                            <div id="weather-desc"></div>
                            <div id="weather-advice"></div>
                        </div>
                    </div>
                    
                    <div id="radar-info" class="hidden absolute top-16 left-4 right-4 bg-green-900/90 border border-green-500/70 p-3 rounded-2xl z-[999] flex items-center justify-between backdrop-blur-md shadow-[0_0_20px_rgba(34,197,94,0.3)] slide-up-anim">
                        <div class="flex items-center gap-2">
                            <span class="text-green-400 animate-pulse text-xl drop-shadow-md">ğŸ“¡</span>
                            <div>
                                <div class="text-white text-xs font-bold tracking-wide">SÃ¼rÃ¼ÅŸ Modu Aktif</div>
                                <div class="text-green-300 text-[9px] uppercase tracking-widest font-bold">Konumun diÄŸerlerine gÃ¶zÃ¼kÃ¼yor</div>
                            </div>
                        </div>
                        <button onclick="toggleRidingMode()" class="bg-green-700 hover:bg-green-600 text-white text-[10px] px-3 py-1.5 rounded-lg font-bold btn-premium-hover">BÄ°TÄ°R</button>
                    </div>
                    
                    <div id="map" class="flex-1 w-full h-full"></div>
                    
                    <div class="absolute bottom-6 right-4 flex flex-col gap-2 z-[999] items-end pointer-events-none">
                        <button onclick="autoZoomToUserLocation()" class="bg-glass w-10 h-10 rounded-full text-lg border border-zinc-700/50 shadow-xl flex items-center justify-center pointer-events-auto mb-1 btn-premium-hover">ğŸ¯</button>
                        <button onclick="toggleRidingMode()" id="btn-riding-mode" class="bg-green-600/90 backdrop-blur hover:bg-green-500 btn-premium-hover px-3 py-2 rounded-xl shadow-[0_0_15px_rgba(34,197,94,0.4)] flex items-center justify-center text-[10px] uppercase tracking-widest font-bold text-white border border-green-400/50 pointer-events-auto">ğŸ“¡ RADAR (SÃœRÃœÅTEYÄ°M)</button>
                        <button onclick="toggleAddEventMode()" id="btn-add-event-mode" class="bg-blue-600/90 backdrop-blur hover:bg-blue-500 btn-premium-hover px-3 py-2 rounded-xl shadow-[0_0_15px_rgba(59,130,246,0.4)] flex items-center justify-center text-[10px] uppercase tracking-widest font-bold text-white border border-blue-400/50 pointer-events-auto">ğŸ“… BULUÅMA EKLE</button>
                        <button onclick="openCategorySelectModal()" id="btn-add-marker-mode" class="bg-sky-600/90 backdrop-blur hover:bg-red-500 btn-premium-hover px-3 py-2 rounded-xl shadow-[0_0_15px_rgba(14,165,233,0.4)] flex items-center justify-center text-[10px] uppercase tracking-widest font-bold text-white border border-red-400/50 pointer-events-auto">ğŸ“ YER EKLE</button>
                        <button onclick="quickAddMarkerCurrentLocation()" id="btn-add-marker-current" class="bg-orange-600/90 backdrop-blur hover:bg-orange-500 btn-premium-hover px-3 py-2 rounded-xl shadow-[0_0_15px_rgba(234,88,12,0.4)] flex items-center justify-center text-[10px] uppercase tracking-widest font-bold text-white border border-orange-400/50 pointer-events-auto">ğŸ¯ KENDÄ° KONUMUMU EKLE</button>
                    </div>
                </div>

                <div id="screen-chat" class="hidden absolute inset-0 flex flex-col z-20 bg-darker slide-up-anim">
                    <div class="bg-zinc-900/50 p-2 flex justify-between items-center border-b border-zinc-800 shrink-0 z-10">
                        <div class="flex w-full bg-zinc-950 rounded-lg p-1">
                            <button onclick="switchChatTab('group')" id="chat-tab-group" class="flex-1 py-2 bg-zinc-800 text-white rounded font-bold text-xs transition-all shadow-sm">GRUP SOHBETÄ°</button>
                            <button onclick="switchChatTab('dm')" id="chat-tab-dm" class="flex-1 py-2 text-zinc-500 rounded font-bold text-xs transition-all hover:text-white">Ã–ZEL (DM)</button>
                        </div>
                    </div>
                    
                    <!-- Story Bar -->
                    <div id="story-bar" class="flex gap-3 overflow-x-auto px-4 py-3 shrink-0 border-b border-zinc-800/50 bg-black/20" style="scrollbar-width:none;-ms-overflow-style:none;">
                        <!-- Add story button -->
                        <div onclick="openAddStoryModal()" class="flex flex-col items-center gap-1 shrink-0 cursor-pointer">
                            <div class="w-14 h-14 rounded-full bg-zinc-900 border-2 border-dashed border-zinc-600 flex items-center justify-center text-2xl hover:border-sky-400 transition-colors">+</div>
                            <span class="text-[9px] text-zinc-500 font-bold uppercase tracking-widest">Story</span>
                        </div>
                        <div id="story-items" class="flex gap-3 items-center"></div>
                    </div>

                    <div id="chat-group-area" class="flex-1 flex flex-col overflow-hidden relative">
                        <div id="pinned-message-area" class="hidden bg-gradient-to-r from-yellow-600 to-yellow-500 text-black px-4 py-2 font-bold text-xs flex justify-between items-center z-20 shadow-md border-b border-yellow-400">
                            <div class="flex items-center gap-2 truncate">
                                <span class="animate-bounce">ğŸ“Œ</span> <span id="pinned-message-text" class="truncate drop-shadow-sm"></span>
                            </div>
                        </div>

                        <div id="chat-messages" class="flex-1 overflow-y-auto p-4 space-y-4 custom-scrollbar scroll-smooth"></div>
                        
                        <div class="bg-glass p-2 flex flex-wrap items-center gap-1 border-t border-zinc-800 shrink-0 pb-safe">
                            <button onclick="openPhotoUpload('group')" class="bg-zinc-800/80 hover:bg-zinc-700 transition w-10 h-10 md:w-12 md:h-12 rounded-xl text-lg flex items-center justify-center border border-zinc-700 btn-premium-hover">ğŸ“¸</button>
                            <button onclick="toggleVoiceRecord('group')" id="voice-btn" class="bg-zinc-800/80 hover:bg-zinc-700 transition w-10 h-10 md:w-12 md:h-12 rounded-xl text-lg flex items-center justify-center border border-zinc-700 btn-premium-hover">ğŸ¤</button>
                            <input id="chat-input" type="text" placeholder="Mesaj veya AI'a soru..." class="flex-1 w-full bg-zinc-950/80 backdrop-blur border border-zinc-700 rounded-xl px-4 py-3 text-sm text-white outline-none focus:border-zinc-400 transition min-w-[120px] shadow-inner">
                            <button onclick="askAIGroup()" class="bg-gradient-to-r from-cyan-600 to-blue-600 hover:opacity-80 transition text-white px-3 md:px-4 py-3 rounded-xl font-bold text-[10px] md:text-xs shadow-[0_0_15px_rgba(6,182,212,0.5)] btn-premium-hover">ğŸ¤– AI SOR</button>
                            <button onclick="sendChatMessage()" class="bg-white hover:bg-gray-200 transition text-black px-3 md:px-5 py-3 rounded-xl font-bold text-[10px] md:text-xs shadow-md btn-premium-hover">GÃ–NDER</button>
                        </div>
                    </div>

                    <div id="chat-dm-list-area" class="hidden flex-1 overflow-y-auto p-4 custom-scrollbar slide-up-anim">
                        <div class="text-[10px] text-zinc-500 mb-4 font-bold uppercase tracking-widest border-b border-zinc-800 pb-2">Mesaj Kutun</div>
                        <div id="dm-users-list" class="space-y-2"></div>
                    </div>
                    
                    <div id="chat-dm-thread-area" class="hidden flex-1 flex flex-col overflow-hidden bg-darker absolute inset-0 z-30 slide-up-anim">
                        <div class="glass-panel p-3 flex items-center gap-3 border-b border-zinc-800 shrink-0 z-10">
                            <button onclick="closeDmThread()" class="text-zinc-400 bg-zinc-900 w-8 h-8 rounded-full flex items-center justify-center hover:text-white transition hover:scale-110">â†</button>
                            <div class="font-bold text-white flex-1 text-sm tracking-wide drop-shadow-md" id="dm-thread-name"></div>
                        </div>
                        
                        <div id="dm-messages" class="flex-1 overflow-y-auto p-4 space-y-4 custom-scrollbar scroll-smooth"></div>
                        
                        <div class="glass-panel p-2 flex items-center gap-1 border-t border-zinc-800 shrink-0 pb-safe">
                            <button onclick="openPhotoUpload('dm')" class="bg-zinc-800/80 hover:bg-zinc-700 transition w-12 h-12 rounded-xl text-xl flex items-center justify-center border border-zinc-700 btn-premium-hover">ğŸ“¸</button>
                            <input id="dm-input" type="text" placeholder="Ã–zel mesaj yaz..." class="flex-1 w-full bg-zinc-950 border border-zinc-700 rounded-xl px-4 py-3 text-sm text-white outline-none focus:border-zinc-400 transition shadow-inner">
                            <button onclick="sendDmMessage()" class="bg-white hover:bg-gray-200 transition text-black px-5 py-3 rounded-xl font-bold text-sm btn-premium-hover shadow-md">GÃ–NDER</button>
                        </div>
                    </div>
                </div>

                <div id="screen-market" class="hidden absolute inset-0 bg-darker overflow-y-auto p-4 z-20 custom-scrollbar slide-up-anim">
                    <div class="flex justify-between items-center mb-6 border-b border-zinc-800 pb-3">
                        <h2 class="text-3xl teko-font tracking-wide text-white drop-shadow-md">EKÄ°PMAN PAZARI</h2>
                        <button onclick="openMarketModal()" class="bg-white hover:bg-gray-200 transition text-black text-xs px-4 py-2 rounded-lg font-bold shadow-lg btn-premium-hover">+ Ä°LAN VER</button>
                    </div>
                    <div id="market-list" class="grid grid-cols-2 gap-3 pb-10"></div>
                </div>

                <div id="screen-rank" class="hidden absolute inset-0 bg-darker overflow-y-auto p-4 z-20 custom-scrollbar slide-up-anim">
                    <!-- KullanÄ±cÄ± SayacÄ± BandÄ± -->
                    <div class="flex gap-3 mb-4">
                        <div class="flex-1 bg-zinc-900/80 border border-zinc-800 rounded-xl p-3 flex items-center gap-2">
                            <div class="w-2 h-2 rounded-full bg-green-500 animate-pulse"></div>
                            <div>
                                <div id="rank-active-users" class="text-green-400 font-black text-base teko-font leading-none">--</div>
                                <div class="text-[9px] text-zinc-500 uppercase tracking-widest font-bold">Aktif KullanÄ±cÄ±</div>
                            </div>
                        </div>
                        <div class="flex-1 bg-zinc-900/80 border border-zinc-800 rounded-xl p-3 flex items-center gap-2">
                            <span class="text-base">ğŸ‘¥</span>
                            <div>
                                <div id="rank-total-users" class="text-white font-black text-base teko-font leading-none">--</div>
                                <div class="text-[9px] text-zinc-500 uppercase tracking-widest font-bold">Toplam Ãœye</div>
                            </div>
                        </div>
                    </div>
                    <div class="flex justify-between items-center mb-4">
                        <h2 class="text-3xl teko-font tracking-wide text-white drop-shadow-md">ğŸ† LÄ°DER TABLOSU</h2>
                        <button onclick="document.getElementById('rewards-modal').classList.remove('hidden')" class="bg-gradient-to-r from-yellow-600 to-orange-500 hover:opacity-90 transition text-white px-4 py-2 rounded-xl text-[10px] font-black tracking-widest uppercase shadow-md btn-premium-hover flex items-center gap-1">
                            <span class="text-sm">ğŸ</span> Ã–DÃœLLER
                        </button>
                    </div>
                    <div class="flex w-full bg-zinc-950 rounded-lg p-1 mb-6 border border-zinc-800 shadow-inner">
                        <button onclick="switchLeaderboard('weekly')" id="rank-tab-weekly" class="flex-1 py-2 bg-zinc-800 text-white rounded font-bold text-xs transition-all shadow-sm">HAFTALIK</button>
                        <button onclick="switchLeaderboard('month')" id="rank-tab-month" class="flex-1 py-2 text-zinc-500 rounded font-bold text-xs transition-all hover:text-white">AYLIK</button>
                        <button onclick="switchLeaderboard('all')" id="rank-tab-all" class="flex-1 py-2 text-zinc-500 rounded font-bold text-xs transition-all hover:text-white">TÃœM ZAMANLAR</button>
                    </div>
                    <div id="leaderboard" class="space-y-3 pb-10"></div>
                </div>
                
                <div id="screen-news" class="hidden absolute inset-0 bg-darker overflow-y-auto p-4 z-20 custom-scrollbar slide-up-anim">
                    <h2 class="text-3xl mb-6 text-white teko-font tracking-wide border-b border-zinc-800 pb-3 drop-shadow-md">ğŸ“° HABERLER & DUYURULAR</h2>
                    <div id="news-list" class="space-y-4 pb-10"></div>
                </div>

                <div id="screen-missions" class="hidden absolute inset-0 bg-darker flex flex-col z-20 slide-up-anim">

                    <!-- INLINE ÅANS Ã‡ARKI â€” sabit Ã¼st bÃ¶lge, kaydÄ±rmaz -->
                    <div class="glass-panel rounded-3xl p-5 border border-yellow-700/40 shadow-[0_0_30px_rgba(234,179,8,0.15)] shrink-0 mx-4 mt-4">
                        <div class="flex items-center justify-between mb-3">
                            <h2 class="text-2xl text-yellow-400 teko-font tracking-wide drop-shadow-[0_0_8px_rgba(234,179,8,0.5)]">ğŸ¡ ÅANS Ã‡ARKI</h2>
                            <p id="spin-inline-info" class="text-[10px] text-zinc-500 font-bold uppercase tracking-widest text-right"></p>
                        </div>
                        <div class="flex flex-col items-center">
                            <div class="relative mb-4" style="perspective:800px;">
                                <canvas id="wheel-canvas-3d" width="260" height="260" style="border-radius:50%;box-shadow:0 0 35px rgba(14,165,233,0.5),0 0 60px rgba(234,179,8,0.2);cursor:pointer;" onclick="spinWheelAction()"></canvas>
                                <!-- Pointer (ibre) -->
                                <div class="absolute top-0 left-1/2 z-20" style="transform:translateX(-50%) translateY(-4px);width:0;height:0;border-left:13px solid transparent;border-right:13px solid transparent;border-top:28px solid #ffffff;filter:drop-shadow(0 3px 8px rgba(0,0,0,1)) drop-shadow(0 0 6px rgba(234,179,8,0.8));"></div>
                                <!-- Center cap -->
                                <div class="absolute inset-0 flex items-center justify-center pointer-events-none">
                                    <div class="w-12 h-12 rounded-full bg-gradient-to-br from-zinc-700 to-zinc-900 border-4 border-zinc-600 shadow-[0_0_15px_rgba(0,0,0,0.8)] z-30 flex items-center justify-center text-xl">ğŸ¯</div>
                                </div>
                            </div>
                            <!-- Sesler: base64 data URI yerine gÃ¼venilir CDN -->
                            <audio id="spin-tick-sound" preload="auto">
                                <source src="https://cdn.freesound.org/previews/220/220173_4100837-lq.mp3" type="audio/mpeg">
                            </audio>
                            <audio id="spin-win-sound" preload="auto">
                                <source src="https://cdn.freesound.org/previews/270/270404_5123851-lq.mp3" type="audio/mpeg">
                            </audio>
                            <button id="spin-btn" onclick="spinWheelAction()" class="w-full bg-gradient-to-r from-yellow-600 to-sky-500 hover:opacity-90 transition-all text-white py-4 rounded-xl font-black shadow-[0_0_25px_rgba(234,179,8,0.5)] text-lg tracking-widest btn-premium-hover">Ã‡ARKI Ã‡EVÄ°R</button>
                            <p class="text-[10px] text-zinc-600 font-bold uppercase tracking-widest text-center mt-2">TÃ¼m hesaplamalar sunucuda gÃ¼venli yapÄ±lÄ±r.</p>
                        </div>
                    </div>  <!-- glass-panel Ã§ark sonu -->

                    <!-- KaydÄ±rÄ±labilir gÃ¶rev listesi -->
                    <div class="flex-1 overflow-y-auto custom-scrollbar px-4 pt-4 pb-10">
                        <div class="bg-gradient-to-r from-sky-700 to-sky-500 rounded-3xl p-6 mb-6 relative overflow-hidden shadow-[0_0_20px_rgba(14,165,233,0.3)]">
                            <div class="absolute -right-4 -bottom-4 text-8xl opacity-20">ğŸ¯</div>
                            <h2 class="text-3xl text-white teko-font tracking-wide mb-1 relative z-10 drop-shadow-md">GÃ–REVLER VE Ã–DÃœLLER</h2>
                            <p class="text-xs text-white/90 relative z-10 font-medium">Aktivite yap, gÃ¶revleri tamamla ve XP kazan!</p>
                        </div>
                        <div id="missions-list" class="space-y-3"></div>
                    </div>
                </div>
                
                <div id="screen-referral" class="hidden absolute inset-0 bg-darker overflow-y-auto p-4 z-20 custom-scrollbar slide-up-anim" style="max-width:100%;box-sizing:border-box;">
                    <div class="bg-gradient-to-r from-purple-800 to-indigo-900 rounded-3xl p-6 mb-6 relative overflow-hidden shadow-[0_0_30px_rgba(88,28,135,0.4)] border border-purple-500/50">
                        <div class="absolute -right-4 -bottom-4 text-8xl opacity-20">ğŸ¤</div>
                        <h2 class="text-4xl text-white teko-font tracking-wide mb-1 relative z-10 drop-shadow-md">DAVET ET, KAZAN!</h2>
                        <p class="text-xs text-zinc-200 relative z-10 font-medium leading-relaxed">ArkadaÅŸlarÄ±nÄ± FreeriderTR'ye davet et, ikiniz de <b class="text-yellow-400 font-bold">XP veya Premium Ã¶dÃ¼l</b> kazanÄ±n! <br><br><span class="bg-black/40 px-2 py-1 rounded border border-purple-500/30 text-[10px] uppercase tracking-wider inline-block">Spam KorumasÄ±: KayÄ±t olan kiÅŸi @gmail.com kullanmalÄ±dÄ±r.</span></p>
                    </div>
                    
                    <div class="glass-panel p-5 rounded-2xl border border-zinc-800 shadow-xl mb-6">
                        <h3 class="text-sm text-purple-400 font-bold uppercase tracking-widest mb-3 flex items-center gap-2"><span class="animate-pulse">ğŸ“Œ</span> Senin Referans Kodun</h3>
                        <div class="flex items-center gap-3">
                            <input type="text" id="my-ref-code" readonly class="flex-1 min-w-0 bg-black/60 border border-purple-900/50 rounded-xl px-4 py-3 text-white text-lg font-black tracking-widest text-center shadow-inner overflow-hidden" value="">
                            <button onclick="copyRefCode()" class="bg-white hover:bg-gray-200 text-black px-5 py-3 rounded-xl font-bold transition-all shadow-md btn-premium-hover">KOPYALA</button>
                        </div>
                        <div class="mt-4 bg-zinc-900/50 rounded-lg p-3 border border-zinc-800/50">
                            <p id="ref-monthly-limit" class="text-xs text-zinc-400 text-center uppercase tracking-widest font-bold"></p>
                            <div class="w-full bg-zinc-800 h-1.5 rounded-full mt-2 overflow-hidden">
                                <div id="ref-monthly-bar" class="bg-gradient-to-r from-purple-600 to-indigo-500 h-full transition-all duration-500" style="width: 0%;"></div>
                            </div>
                        </div>
                    </div>

                    <div class="glass-panel p-5 rounded-2xl border border-yellow-900/50 shadow-[0_0_20px_rgba(161,98,7,0.2)]">
                        <h3 class="text-sm text-yellow-500 font-bold uppercase tracking-widest mb-3 flex justify-between items-center">
                            <span>ğŸ AlÄ±nabilir Ã–dÃ¼llerin</span>
                            <span id="claimable-ref-count" class="bg-gradient-to-r from-yellow-500 to-yellow-600 text-black px-3 py-1 rounded-lg text-xs font-black shadow-md">0</span>
                        </h3>
                        
                        <div id="ref-claim-area" class="mt-4 transition-all duration-300">
                            <select id="ref-reward-select" class="w-full bg-black/80 border border-yellow-900/50 rounded-xl px-4 py-4 mb-4 text-white text-sm outline-none focus:border-yellow-500 transition shadow-inner cursor-pointer font-medium">
                                <option value="xp_500">ğŸŒŸ 500 XP (AnÄ±nda HesabÄ±na YÃ¼klenir)</option>
                                <option value="prem_dlx_2">ğŸ”¥ 2 GÃ¼n Deluxe Premium Ãœyelik</option>
                                <option value="prem_ult_1">ğŸ‘‘ 1 GÃ¼n Ultra+ Premium Ãœyelik</option>
                                <option value="prem_std_7">â­ 1 Hafta Standart Premium Ãœyelik</option>
                            </select>
                            <button onclick="claimRefReward()" class="w-full bg-gradient-to-r from-yellow-600 to-yellow-500 hover:opacity-90 transition-all text-black py-4 rounded-xl font-black text-sm shadow-[0_0_15px_rgba(234,179,8,0.5)] tracking-widest btn-premium-hover flex items-center justify-center gap-2">
                                <span>Ã–DÃœLÃœ AL</span> <span class="text-lg">ğŸ¯</span>
                            </button>
                        </div>
                    </div>
                </div>

                <div id="screen-premium" class="hidden absolute inset-0 bg-darker overflow-y-auto p-4 z-20 custom-scrollbar slide-up-anim">
                    <div class="glass-panel rounded-3xl p-6 border border-zinc-800 text-center mt-4 shadow-2xl">
                        <div class="text-6xl mb-2 drop-shadow-[0_0_20px_rgba(255,255,255,0.4)] animate-bounce">ğŸŒŸ</div>
                        <h2 class="text-5xl text-prem-rainbow teko-font tracking-wide mb-2 drop-shadow-md">FREERIDER PLUS</h2>
                        <p class="text-[11px] text-zinc-300 mb-6 px-2 leading-relaxed font-medium">Sunucu maliyetlerini karÅŸÄ±lamak ve sizlere <b class="text-white">tamamen reklamsÄ±z bir deneyim</b> sunabilmek iÃ§in abonelik sistemi yapÄ±lmÄ±ÅŸtÄ±r. AnlayÄ±ÅŸÄ±nÄ±z ve desteÄŸiniz iÃ§in teÅŸekkÃ¼r ederiz. ğŸ™</p>
                        
                        <!-- Ä°ndirim Banner -->
                        <div class="bg-gradient-to-r from-red-900/60 to-orange-900/60 border border-red-500/50 rounded-2xl px-4 py-3 mb-5 flex items-center gap-3 shadow-[0_0_20px_rgba(239,68,68,0.3)]">
                            <span class="text-2xl animate-bounce">ğŸ”¥</span>
                            <div>
                                <div class="text-red-300 font-black text-sm uppercase tracking-widest">Ã–ZEL LANSMAN Ä°NDÄ°RÄ°MÄ°!</div>
                                <div class="text-zinc-300 text-[10px] font-medium">TÃ¼m paketlerde %80 indirim â€” sÄ±nÄ±rlÄ± sÃ¼re!</div>
                            </div>
                            <span class="ml-auto text-red-400 font-black text-xs bg-red-900/60 px-2 py-1 rounded-lg border border-red-700/50">-80%</span>
                        </div>

                        <div class="space-y-4 mb-6">

                            <!-- STANDART PAKETÄ° -->
                            <div class="text-left bg-zinc-950 p-5 rounded-2xl border border-blue-900/30 transition hover:bg-zinc-900 hover:border-blue-500/50 hover:shadow-[0_0_20px_rgba(59,130,246,0.2)]">
                                <div class="flex justify-between items-center mb-3">
                                    <h3 class="font-bold text-blue-400 text-lg flex items-center gap-2"><span>â­</span> Standart Paket</h3>
                                    <div class="flex flex-col items-end gap-1">
                                        <div class="flex items-center gap-2">
                                            <span class="text-zinc-500 text-[10px] line-through font-bold">50 TL / Ay</span>
                                            <span class="bg-red-500/20 text-red-400 border border-red-500/50 px-2 py-0.5 rounded-md text-[9px] font-black uppercase tracking-wider animate-pulse">%80 Ä°NDÄ°RÄ°M (40 TL TASARRUF)</span>
                                        </div>
                                        <span class="bg-blue-900/40 text-blue-200 px-3 py-1.5 rounded-lg text-xs font-bold border border-blue-500/30 shadow-md">10 TL / Ay</span>
                                    </div>
                                </div>
                                <ul class="text-xs text-zinc-400 space-y-2 mt-3 leading-relaxed">
                                    <li class="flex gap-2"><span>ğŸ’</span> <span><b class="text-white">Ä°sim Rengi:</b> Profilinde ve her mesajÄ±nÄ±n yanÄ±nda 4 farklÄ± Ã¶zel renk seÃ§eneÄŸi. ArtÄ±k herkes seni tanÄ±yacak!</span></li>
                                    <li class="flex gap-2"><span>ğŸ¤–</span> <span><b class="text-white">SÄ±nÄ±rsÄ±z Freerider AI:</b> Ãœcretsiz Ã¼yelikte gÃ¼nde yalnÄ±zca 10 soru hakkÄ±n var. Standart ile bisiklet sorularÄ±, parÃ§a tavsiyeleri ve rota Ã¶nerileri iÃ§in gÃ¼nde sÄ±nÄ±rsÄ±z AI eriÅŸimi.</span></li>
                                    <li class="flex gap-2"><span>ğŸ¬</span> <span><b class="text-white">Video Reels PaylaÅŸÄ±mÄ±:</b> Reels sekmesinde yalnÄ±zca Standart ve Ã¼zeri Ã¼yeler video yÃ¼kleyebilir. SÃ¼rÃ¼ÅŸ videolarÄ±nÄ± topluluÄŸa gÃ¶ster!</span></li>
                                    <li class="flex gap-2"><span>ğŸ“¸</span> <span><b class="text-white">Zengin Pazaryeri Ä°lanlarÄ±:</b> Bisiklet veya parÃ§a satarken ilanÄ±na <b>2 fotoÄŸraf</b> ekleyebilirsin. Ãœcretsiz Ã¼yeler yalnÄ±zca 1 fotoÄŸraf ekleyebilir.</span></li>
                                    <li class="flex gap-2"><span>ğŸš²</span> <span><b class="text-white">Dijital Garaj (1 Bisiklet):</b> Profilinde "Bisikletlerim" bÃ¶lÃ¼mÃ¼nde bisikletini Ã§oklu fotoÄŸrafla sergile. Marka, model, vites, jant, lastik â€” tÃ¼m detaylarÄ± ekle.</span></li>
                                    <li class="flex gap-2"><span>ğŸ“</span> <span><b class="text-white">Haritaya Rampa / Rota Ekleme:</b> KeÅŸfettiÄŸin veya bildiÄŸin parkurlarÄ± haritaya iÅŸaretle. TÃ¼m TÃ¼rkiye'deki sÃ¼rÃ¼cÃ¼ler gÃ¶rebilir.</span></li>
                                    <li class="flex gap-2"><span>ğŸ¡</span> <span><b class="text-white">GÃ¼nlÃ¼k Åans Ã‡arkÄ±:</b> Her gÃ¼n Ã¼cretsiz 1 Ã§ark hakkÄ±n var. Standart Ã¼yeler gÃ¼nde <b>2 Ã§ark</b> Ã§evirebilir! XP, premium sÃ¼re, Ã¶zel Ã¶dÃ¼ller kazanabilirsin.</span></li>
                                    <li class="flex gap-2"><span>ğŸ†</span> <span><b class="text-white">HaftalÄ±k / AylÄ±k Liderlik Ã–dÃ¼lÃ¼:</b> HaftalÄ±k XP yarÄ±ÅŸmasÄ±nda ilk 3'e girersen otomatik olarak 1 haftalÄ±k premium Ã¶dÃ¼l kazanÄ±rsÄ±n.</span></li>
                                    <li class="flex gap-2"><span>ğŸ’¬</span> <span><b class="text-white">Grup Sohbeti & Ã–zel Mesaj:</b> TopluluÄŸun tÃ¼m sohbetlerine, Ã¶zel DM'lere ve Freerider AI ile bire bir sohbete sÄ±nÄ±rsÄ±z eriÅŸim.</span></li>
                                    <li class="flex gap-2"><span>ğŸ—“ï¸</span> <span><b class="text-white">Etkinlik OluÅŸturma:</b> Kendi dÃ¼zenlediÄŸin buluÅŸmalarÄ±, yarÄ±ÅŸmalarÄ± veya sÃ¼rÃ¼ÅŸ gÃ¼nlerini etkinlik takviminde paylaÅŸabilirsin.</span></li>
                                    <li class="flex gap-2"><span>ğŸ›’</span> <span><b class="text-white">Pazaryeri AlÄ±m-SatÄ±m:</b> SÄ±nÄ±rsÄ±z ilan aÃ§ma ve tÃ¼m ilanlarÄ± gÃ¶rme. TÃ¼rkiye'nin en bÃ¼yÃ¼k MTB ikinci el pazarÄ±na eriÅŸim.</span></li>
                                    <li class="flex gap-2"><span>ğŸŒ</span> <span><b class="text-white">ReklamsÄ±z Deneyim:</b> Uygulama tamamen reklamsÄ±zdÄ±r. HiÃ§bir banner, pop-up veya reklam yok â€” sadece saf topluluk deneyimi.</span></li>
                                    <li class="flex gap-2"><span>ğŸ“Š</span> <span><b class="text-white">XP & Rozet Sistemi:</b> Mesaj at, rota ekle, etkinliÄŸe katÄ±l, AI kullan â€” her aktivite XP kazandÄ±rÄ±r. UnvanÄ±nÄ± yÃ¼kselt, rozet topla.</span></li>
                                    <li class="flex gap-2"><span>ğŸ””</span> <span><b class="text-white">AnlÄ±k Push Bildirimleri:</b> Biri sana DM attÄ±ÄŸÄ±nda, ilanÄ±na ilgi gÃ¶sterildiÄŸinde veya katÄ±lmak istediÄŸin etkinlik baÅŸlamadan Ã¶nce bildirim alÄ±rsÄ±n.</span></li>
                                </ul>
                                <div class="mt-4 bg-blue-950/40 border border-blue-800/50 rounded-xl p-3">
                                    <div class="text-blue-300 text-[10px] font-black uppercase tracking-widest mb-1">ğŸ’¡ Standart iÃ§in Kimler Uygun?</div>
                                    <div class="text-zinc-400 text-[10px] leading-relaxed">UygulamayÄ± aktif kullanan, AI'ya soru soran, reels paylaÅŸmak isteyen ve bisikletini dijital garajda sergilemek isteyen her sÃ¼rÃ¼cÃ¼ iÃ§in mÃ¼kemmel baÅŸlangÄ±Ã§ paketi.</div>
                                </div>
                            </div>

                            <!-- DELUXE PAKETÄ° -->
                            <div class="text-left bg-zinc-950 p-5 rounded-2xl border border-purple-900/50 shadow-[0_0_15px_rgba(168,85,247,0.1)] transition hover:bg-zinc-900 hover:border-purple-500/70 hover:shadow-[0_0_25px_rgba(168,85,247,0.3)]">
                                <div class="flex justify-between items-center mb-3">
                                    <h3 class="font-bold text-purple-400 text-lg flex items-center gap-2"><span>ğŸŒŸ</span> Deluxe Paket</h3>
                                    <div class="flex flex-col items-end gap-1">
                                        <div class="flex items-center gap-2">
                                            <span class="text-zinc-500 text-[10px] line-through font-bold">100 TL / Ay</span>
                                            <span class="bg-purple-500/20 text-purple-400 border border-purple-500/50 px-2 py-0.5 rounded-md text-[9px] font-black uppercase tracking-wider animate-pulse">%80 Ä°NDÄ°RÄ°M (80 TL TASARRUF)</span>
                                        </div>
                                        <span class="bg-purple-900/50 text-purple-100 px-3 py-1.5 rounded-lg text-xs font-bold border border-purple-500/50 shadow-md">20 TL / Ay</span>
                                    </div>
                                </div>
                                <div class="text-[9px] text-purple-300 font-bold uppercase tracking-widest mb-3 bg-purple-900/20 rounded-lg px-3 py-1.5 border border-purple-700/30">âœ¨ Standart'taki HER ÅEY dahil + aÅŸaÄŸÄ±daki ekstralar:</div>
                                <ul class="text-xs text-zinc-400 space-y-2.5 mt-1 leading-relaxed">
                                   <li class="flex gap-2"><span>ğŸ‘‘</span> <span><b class="text-white">Elite Rozeti:</b> Profilinde ve chatte parlayan Deluxe Ã§erÃ§eve.</span></li>
                                   <li class="flex gap-2"><span>ğŸ¨</span> <span><b class="text-white">Simli Renkler:</b> Hareketli ve simli isim renkleri.</span></li>
                                   <li class="flex gap-2"><span>ğŸš€</span> <span><b class="text-white">Pazar Bump:</b> Ä°lanlarÄ±nÄ± tek tuÅŸla listenin en Ã¼stÃ¼ne taÅŸÄ±ma.</span></li>
                                   <li class="flex gap-2"><span>ğŸ“¸</span> <span><b class="text-white">GeliÅŸmiÅŸ Ä°lan:</b> Her bir ilanÄ±na 4 fotoÄŸraf.</span></li>
                                   <li class="flex gap-2"><span>âš™ï¸</span> <span><b class="text-white">DetaylÄ± DonanÄ±m:</b> Bisiklet eklerken MaÅŸa, Åok ve Fren detaylarÄ±.</span></li>
                                   <li class="flex gap-2"><span>ğŸ”¥</span> <span><b class="text-white">Ã–zel Ä°konlar:</b> Rampa eklerken ğŸ’€, ğŸ”¥, ğŸ‘‘ gibi ikonlar.</span></li>
                                   <li class="flex gap-2"><span>ğŸš²</span> <span><b class="text-white">GeniÅŸ Garaj:</b> 2 farklÄ± bisikleti garaja ekleme.</span></li>
                                   <li class="flex gap-2"><span>ğŸ™ï¸</span> <span><b class="text-white">Sesli Mesaj:</b> Grup sohbetinde ses kaydÄ± gÃ¶nderme.</span></li>
                                </ul>
                            </div>

                            <!-- ULTRA+ PAKETÄ° -->
                            <div class="text-left bg-zinc-950 p-5 rounded-2xl border border-yellow-500/60 relative overflow-hidden shadow-[0_0_20px_rgba(234,179,8,0.2)] transition hover:bg-zinc-900 hover:shadow-[0_0_30px_rgba(234,179,8,0.4)] hover:border-yellow-400">
                                <div class="absolute -right-7 top-4 bg-yellow-500 text-black font-black text-[9px] py-1.5 px-10 rotate-45 shadow-lg tracking-widest uppercase">V.I.P LOUNGE</div>
                                <div class="flex justify-between items-center mb-3">
                                    <h3 class="font-bold text-yellow-500 text-lg flex items-center gap-2"><span>ğŸ‘‘</span> Ultra+ Paket</h3>
                                    <div class="flex flex-col items-end gap-1 mr-8">
                                        <div class="flex items-center gap-2">
                                            <span class="text-zinc-500 text-[10px] line-through font-bold">150 TL / Ay</span>
                                            <span class="bg-yellow-500/20 text-yellow-400 border border-yellow-500/50 px-2 py-0.5 rounded-md text-[9px] font-black uppercase tracking-wider animate-pulse">%80 Ä°NDÄ°RÄ°M (120 TL TASARRUF)</span>
                                        </div>
                                        <span class="bg-gradient-to-r from-yellow-400 to-yellow-600 text-black px-3 py-1.5 rounded-lg text-xs font-black shadow-lg">30 TL / Ay</span>
                                    </div>
                                </div>
                                <div class="text-[9px] text-yellow-300 font-bold uppercase tracking-widest mb-3 bg-yellow-900/20 rounded-lg px-3 py-1.5 border border-yellow-700/30">ğŸ‘‘ Deluxe'teki HER ÅEY dahil + aÅŸaÄŸÄ±daki ekstralar:</div>
                                <ul class="text-xs text-zinc-400 space-y-2.5 mt-1 leading-relaxed">
                                  <li class="flex gap-2"><span>âš¡</span> <span><b class="text-white">Sistem Efsanesi:</b> En Ã¼st dÃ¼zey rÃ¼tbe ve altÄ±n parÄ±ltÄ±lÄ± kart.</span></li>
                                  <li class="flex gap-2"><span>ğŸ”¥</span> <span><b class="text-white">CanlÄ± Efektler:</b> Alev veya Buz animasyonlarÄ±.</span></li>
                                  <li class="flex gap-2"><span>ğŸ¨</span> <span><b class="text-white">Renk Ã–zgÃ¼rlÃ¼ÄŸÃ¼:</b> Ä°stediÄŸin HEX koduyla renk belirleme.</span></li>
                                  <li class="flex gap-2"><span>ğŸ“Œ</span> <span><b class="text-white">Mesaj Sabitleme:</b> Gruptaki mesajlarÄ±nÄ± sabitleme.</span></li>
                                  <li class="flex gap-2"><span>ğŸ‘ï¸</span> <span><b class="text-white">GÃ¶rÃ¼ntÃ¼lenme Analizi:</b> Profil/ilan tÄ±klanma istatistikleri.</span></li>
                                  <li class="flex gap-2"><span>ğŸŒˆ</span> <span><b class="text-white">GÃ¶kkuÅŸaÄŸÄ± Radar:</b> Haritada taÃ§lÄ±/gÃ¶kkuÅŸaÄŸÄ± radar.</span></li>
                                  <li class="flex gap-2"><span>âœ…</span> <span><b class="text-white">Mavi Onay Tiki:</b> DoÄŸrulanmÄ±ÅŸ (Verified) rozeti.</span></li>
                                  <li class="flex gap-2"><span>ğŸš²</span> <span><b class="text-white">Koleksiyoner GarajÄ±:</b> Tam 4 adet bisiklet ekleme hakkÄ±.</span></li>
                                  <li class="flex gap-2"><span>ğŸ“¸</span> <span><b class="text-white">Maksimum Galeri:</b> Ä°lanlara 10 fotoÄŸraf.</span></li>
                                </ul>
                            </div>
                        </div>
                        
                        <!-- SATIN ALMA BÃ–LÃœMÃœ: Ã¼yelik yoksa gÃ¶ster -->
                        <div id="premium-buy-section">
                            <select id="premium-tier-select" class="w-full bg-black border border-zinc-700 rounded-xl px-5 py-4 mb-4 outline-none text-white text-sm focus:border-zinc-400 transition font-bold shadow-inner cursor-pointer">
                                <option value="freeridertr_standard_pack_monthly">â­ Standart Paket â€” 10 TL/Ay (Ä°ndirimli)</option>
                                <option value="freeridertr_deluxe_pack_monthly">ğŸŒŸ Deluxe Paket â€” 20 TL/Ay (Ä°ndirimli)</option>
                                <option value="freeridertr_ultra_pack_monthly">ğŸ‘‘ Ultra+ Paket â€” 30 TL/Ay (Ä°ndirimli)</option>
                            </select>
                            <button onclick="requestPremium()" class="w-full bg-gradient-to-r from-green-700 to-emerald-500 hover:opacity-90 transition py-4 rounded-xl font-bold text-white text-lg shadow-[0_0_20px_rgba(34,197,94,0.35)] tracking-wide btn-premium-hover flex items-center justify-center gap-2">
                                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" style="width:22px;height:22px;"><path d="M3.18 23.76c.3.17.64.24.99.2l12.45-12.45L12.6 7.5 3.18 23.76zm17.01-10.7-3.45-1.99-3.62 3.62 3.62 3.62 3.44-1.98c.98-.57.98-2.1.01-2.67zM3.54.32C3.22.13 2.84.08 2.51.25L14.98 12.7l-3.62 3.62 3.45-1.99.01-.01z"/></svg>
                                SATIN AL
                            </button>
                            <p class="text-[10px] text-zinc-500 mt-4 text-center font-medium">SatÄ±n alÄ±m mobil uygulama Ã¼zerinden gerÃ§ekleÅŸtirilir ve otomatik aktive edilir.</p>
                        </div>

                        <!-- AKTÄ°F ÃœYELÄ°K BÃ–LÃœMÃœ: Ã¼yelik varsa gÃ¶ster -->
                        <div id="premium-settings-section" class="hidden scale-in-anim">

                            <!-- Mevcut Ã¼yelik durum kartÄ± -->
                            <div id="current-plan-card" class="glass-panel p-5 rounded-2xl border border-zinc-700 shadow-xl mt-2 mb-4">
                                <div class="flex items-center justify-between mb-1">
                                    <span class="text-[10px] text-zinc-500 uppercase tracking-widest font-bold">Aktif Paketiniz</span>
                                    <span id="current-plan-badge" class="text-xs font-black px-3 py-1 rounded-lg"></span>
                                </div>
                                <div id="current-plan-name" class="text-xl font-black text-white mb-1"></div>
                                <div id="current-plan-expiry" class="text-[11px] text-zinc-400 font-medium"></div>
                            </div>

                            <!-- YÃ¼kselt butonu: Standart veya Deluxe kullanÄ±cÄ±sÄ±na gÃ¶ster -->
                            <div id="upgrade-plan-section" class="hidden mb-4">
                                <div class="bg-gradient-to-r from-yellow-900/40 to-amber-900/30 border border-yellow-700/50 rounded-2xl p-4 mb-3 flex items-center gap-3">
                                    <span class="text-2xl">â¬†ï¸</span>
                                    <div>
                                        <div class="text-yellow-400 font-black text-sm">ÃœyeliÄŸini YÃ¼kselt!</div>
                                        <div id="upgrade-hint-text" class="text-[11px] text-zinc-400 mt-0.5"></div>
                                    </div>
                                </div>
                                <select id="upgrade-tier-select" class="w-full bg-black border border-yellow-700/60 rounded-xl px-5 py-4 mb-3 outline-none text-white text-sm focus:border-yellow-500 transition font-bold shadow-inner cursor-pointer"></select>
                                <button onclick="requestUpgrade()" class="w-full bg-gradient-to-r from-yellow-600 to-amber-500 hover:opacity-90 transition py-4 rounded-xl font-black text-black text-sm shadow-[0_0_20px_rgba(234,179,8,0.4)] tracking-widest btn-premium-hover flex items-center justify-center gap-2">
                                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" style="width:18px;height:18px;"><path d="M3.18 23.76c.3.17.64.24.99.2l12.45-12.45L12.6 7.5 3.18 23.76zm17.01-10.7-3.45-1.99-3.62 3.62 3.62 3.62 3.44-1.98c.98-.57.98-2.1.01-2.67zM3.54.32C3.22.13 2.84.08 2.51.25L14.98 12.7l-3.62 3.62 3.45-1.99.01-.01z"/></svg>
                                    ÃœYELÄ°ÄÄ° YÃœKSELT
                                </button>
                            </div>

                            <!-- Renk & efekt ayarlarÄ± -->
                            <div class="glass-panel p-5 rounded-2xl border border-zinc-700 shadow-xl text-left">
                                <h3 class="text-white font-bold mb-3 text-sm flex items-center gap-2"><span class="animate-pulse">ğŸ¨</span> Plus Profil AyarlarÄ±</h3>
                                <div id="color-options" class="flex flex-wrap gap-2"></div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- ============================================================ -->
                <!-- REELS EKRANI (TikTok/Instagram tarzÄ±) -->
                <!-- ============================================================ -->
                <div id="screen-reels" class="hidden fixed inset-0 bg-black z-[9990] flex flex-col">
                    <!-- Tam ekran feed -->
                    <div id="reels-feed" class="w-full h-full overflow-y-auto snap-y snap-mandatory custom-scrollbar" style="scroll-snap-type:y mandatory;">
                        <div id="reels-loading" class="flex items-center justify-center h-full">
                            <div class="text-center">
                                <div class="w-10 h-10 rounded-full border-4 border-pink-900/40 border-t-pink-500 animate-spin mx-auto mb-3"></div>
                                <p class="text-zinc-400 text-sm font-bold">Reels yÃ¼kleniyor...</p>
                            </div>
                        </div>
                    </div>
                    <!-- Overlay butonlar â€” position:absolute (screen-reels zaten inset-0) -->
                    <!-- âœ• Kapat â€” Ã§entikten 20px daha aÅŸaÄŸÄ± (72px) -->
                    <button onclick="closeReels()" style="position:absolute;top:calc(env(safe-area-inset-top, 0px) + 72px);right:16px;z-index:9999;width:44px;height:44px;border-radius:50%;background:rgba(0,0,0,0.65);color:#fff;font-size:18px;font-weight:bold;border:1px solid rgba(255,255,255,0.25);display:flex;align-items:center;justify-content:center;box-shadow:0 2px 12px rgba(0,0,0,0.5);backdrop-filter:blur(4px);cursor:pointer;">âœ•</button>
                    <!-- ğŸ”Š Ses -->
                    <button id="reel-sound-btn" onclick="toggleReelSound()" style="position:absolute;top:calc(env(safe-area-inset-top, 0px) + 72px);right:68px;z-index:9999;width:44px;height:44px;border-radius:50%;background:rgba(0,0,0,0.65);font-size:22px;border:1px solid rgba(255,255,255,0.25);display:flex;align-items:center;justify-content:center;box-shadow:0 2px 12px rgba(0,0,0,0.5);backdrop-filter:blur(4px);cursor:pointer;">ğŸ”Š</button>
                    <!-- ğŸ“·+ Reels PaylaÅŸ â€” ses butonunun hemen yanÄ±nda, belirgin kamera ikonu -->
                    <button id="reels-upload-top-btn" onclick="openReelUploadModal()" title="Reels PaylaÅŸ"
                        style="position:absolute;top:calc(env(safe-area-inset-top, 0px) + 72px);right:120px;z-index:9999;width:44px;height:44px;border-radius:50%;background:rgba(0,0,0,0.5);border:1.5px solid rgba(236,72,153,0.6);display:flex;align-items:center;justify-content:center;box-shadow:0 0 12px rgba(236,72,153,0.4),0 2px 8px rgba(0,0,0,0.5);backdrop-filter:blur(4px);cursor:pointer;font-size:18px;">
                        ğŸ“·<span style="position:absolute;top:-3px;right:-3px;width:15px;height:15px;background:#e91e8c;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:10px;font-weight:900;color:#fff;border:1.5px solid #000;line-height:1;">+</span>
                    </button>
                    <!-- âŠ Grid/Feed geÃ§iÅŸ butonu -->
                    <button id="grid-view-btn" onclick="window.toggleReelsGridView()" style="position:absolute;top:calc(env(safe-area-inset-top, 0px) + 72px);right:172px;z-index:9999;width:44px;height:44px;border-radius:50%;background:rgba(0,0,0,0.65);border:1px solid rgba(255,255,255,0.25);display:flex;align-items:center;justify-content:center;box-shadow:0 2px 12px rgba(0,0,0,0.5);backdrop-filter:blur(4px);cursor:pointer;" title="Izgara GÃ¶rÃ¼nÃ¼mÃ¼">
                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="width:18px;height:18px;"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/></svg>
                    </button>
                    <!-- Reels FAB: sol alt kÃ¶ÅŸe, navigasyonun hemen Ã¼stÃ¼ -->
                    <button onclick="openReelUploadModal()" id="reels-fab-btn"
                        class="fixed z-[9999] btn-premium-hover"
                        title="Reel PaylaÅŸ"
                        style="bottom:calc(70px + env(safe-area-inset-bottom, 0px));left:16px;width:48px;height:48px;border-radius:50%;background:linear-gradient(135deg,#be185d,#0ea5e9);display:flex;align-items:center;justify-content:center;box-shadow:0 0 20px rgba(236,72,153,0.65),0 4px 14px rgba(0,0,0,0.5);border:1.5px solid rgba(255,255,255,0.18);backdrop-filter:blur(6px);">
                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" style="width:22px;height:22px;">
                            <path d="M23 7l-7 5 7 5V7z"/><rect x="1" y="5" width="15" height="14" rx="2" ry="2"/>
                        </svg>
                    </button>
                    <!-- BoÅŸ durum -->
                    <div id="reels-empty" class="hidden fixed inset-0 flex flex-col items-center justify-center gap-4 z-[9991]">
                        <div class="text-6xl">ğŸ¬</div>
                        <p class="text-white font-black teko-font text-2xl tracking-widest">Ä°lk Reels'i Sen PaylaÅŸ!</p>
                        <p class="text-zinc-400 text-sm text-center px-8">Bisiklet videolarÄ±nÄ± ve fotoÄŸraflarÄ±nÄ± toplulukla paylaÅŸ!</p>
                        <button onclick="openReelUploadModal()" class="bg-gradient-to-r from-pink-700 to-sky-500 text-white px-6 py-3 rounded-xl font-black text-sm tracking-widest btn-premium-hover">+ REEL PAYLAÅ</button>
                    </div>
                </div>

                <div id="screen-profile" class="hidden absolute inset-0 bg-darker overflow-y-auto z-20 custom-scrollbar slide-up-anim">
                    <div class="p-6 text-center pb-20">
                        <div class="relative inline-block mt-4 group">
                            <div id="profile-avatar-wrap" class="avatar-particle-wrap relative inline-block">
                            <img id="profile-avatar" src="" class="w-32 h-32 mx-auto rounded-full object-cover cursor-pointer bg-zinc-900 transition-all duration-300 group-hover:opacity-80 group-hover:scale-105 shadow-xl" onclick="openProfilePicUpload()">
                            </div>
                            <div class="absolute inset-0 bg-black/50 rounded-full flex items-center justify-center opacity-0 group-hover:opacity-100 pointer-events-none transition-opacity duration-300">
                                <span class="text-2xl text-white drop-shadow-md">ğŸ“¸</span>
                            </div>
                            <input id="pic-upload" type="file" accept="image/*" class="hidden" onchange="uploadProfilePic(this)">
                        </div>

                        <!-- Avatar seÃ§im butonlarÄ± -->
                        <div class="flex gap-2 justify-center mt-3">
                            <button onclick="openRpmModal()" class="bg-gradient-to-r from-purple-700 to-indigo-700 hover:opacity-90 text-white text-[10px] font-black px-4 py-2 rounded-xl shadow-[0_0_15px_rgba(139,92,246,0.4)] btn-premium-hover flex items-center gap-2 tracking-widest">
                                <span>ğŸ­</span> 3D AVATAR OLUÅTUR
                            </button>
                            <button onclick="openProfilePicUpload()" class="bg-zinc-800 hover:bg-zinc-700 text-zinc-300 text-[10px] font-bold px-4 py-2 rounded-xl border border-zinc-700 btn-premium-hover flex items-center gap-2 tracking-widest">
                                <span>ğŸ“¸</span> FOTOÄRAF
                            </button>
                        </div>
                        <p class="text-[9px] text-zinc-600 mt-1 font-bold uppercase tracking-widest">Ãœcretsiz Â· Hesap gerekmez</p>
                        
                        <div id="profile-name-container" class="flex justify-center items-center gap-2 mt-5">
                            <div id="profile-name" class="text-4xl font-bold text-white teko-font tracking-wide drop-shadow-md transition-all"></div>
                            <div id="profile-verified-badge" class="hidden"></div>
                        </div>
                        
                        <div id="profile-bio" class="text-zinc-300 mt-2 text-sm font-medium px-4 leading-relaxed"></div>
                        
                        <div class="flex flex-wrap justify-center gap-3 mt-8 px-2">
                            <div class="glass-panel p-4 rounded-2xl border border-zinc-800/50 flex-1 min-w-[120px] max-w-[160px] shadow-lg hover:border-zinc-600 transition-all duration-300">
                                <div id="profile-xp" class="text-4xl teko-font text-white tracking-wide drop-shadow-sm leading-tight">0</div>
                                <div class="text-[10px] text-zinc-400 font-bold uppercase tracking-widest mt-1">Toplanan XP</div>
                            </div>
                            <div class="glass-panel p-4 rounded-2xl border border-zinc-800/50 flex-1 min-w-[120px] max-w-[160px] shadow-lg hover:border-zinc-600 transition-all duration-300">
                                <div id="profile-title" class="text-base font-bold mt-1 drop-shadow-sm transition-colors leading-snug break-words">Ã‡aylak</div>
                            <div id="profile-xp-progress" class="w-full mt-1"></div>
                                <div class="text-[10px] text-zinc-400 font-bold uppercase tracking-widest mt-1.5">Mevcut Ãœnvan</div>
                            </div>
                        </div>
                        
                                
                        <div class="mt-4 text-left glass-panel p-4 rounded-2xl border border-zinc-800/50">
                            <div class="flex justify-between items-center mb-4">
                                <h3 class="text-xs font-bold text-zinc-400 uppercase tracking-widest flex items-center gap-2"><span>ğŸš²</span> GarajÄ±m</h3>
                                <button onclick="openAddBikeModal()" class="bg-zinc-800 hover:bg-zinc-700 transition text-white text-[10px] px-3 py-1.5 rounded-lg font-bold shadow-md btn-premium-hover">+ Yeni Ekle</button>
                            </div>
                            <div id="garage-list" class="grid grid-cols-2 gap-3"></div>
                        </div>

                        <div class="mt-3 text-left glass-panel p-4 rounded-2xl border border-zinc-800/50">
                            <h3 class="text-xs font-bold text-zinc-400 mb-4 uppercase tracking-widest flex items-center gap-2"><span>ğŸ…</span> KazanÄ±lan Rozetler</h3>
                            <div id="profile-badges" class="flex flex-wrap gap-2"></div>
                        </div>

                        <div class="mt-4 space-y-2">
                            
                            <button onclick="openSettingsModal()" class="w-full bg-zinc-900 hover:bg-zinc-800 transition py-4 rounded-xl font-bold text-white text-sm border border-zinc-700 shadow-md btn-premium-hover">âš™ï¸ PROFÄ°LÄ° DÃœZENLE</button>

                            
                            <button onclick="logout()" class="w-full bg-black hover:bg-red-950/40 transition text-sky-400 py-4 rounded-xl font-bold text-sm border border-sky-900/50 shadow-md btn-premium-hover mt-4">SÄ°STEMDEN Ã‡IKIÅ YAP</button>

                                                        <button id="notif-perm-btn" onclick="handleNotifPermission()" class="w-full bg-zinc-900 border border-zinc-700 hover:bg-zinc-800 transition text-zinc-300 py-4 rounded-xl font-bold text-sm mt-4 btn-premium-hover flex items-center justify-center gap-2">
                                <span id="notif-btn-icon">ğŸ””</span>
                                <span id="notif-btn-text">Bildirimleri AÃ§</span>
                            </button>

                            <div id="streak-freeze-badge" class="hidden mt-3 bg-blue-950/50 border border-blue-700/50 rounded-xl px-4 py-3 flex items-center gap-3">
                                <span class="text-2xl">ğŸ›¡ï¸</span>
                                <div><div class="text-blue-300 font-black text-sm">Seri Koruma Kalkani</div><div id="streak-freeze-count" class="text-[10px] text-zinc-400 font-bold">0 adet</div></div>
                            </div>
                            <button id="admin-btn" onclick="showAdminPanel()" class="hidden w-full bg-gradient-to-r from-sky-800 to-zinc-900 hover:opacity-90 transition text-white py-4 rounded-xl font-bold text-sm shadow-[0_0_20px_rgba(14,165,233,0.4)] mt-6 btn-premium-hover border border-sky-800/60">ğŸ‘‘ YÃ–NETÄ°CÄ° PANELÄ°</button>
                        </div>
                    </div>
                </div>
            </div>

        </div>

        <div id="social-modal" class="hidden fixed inset-0 modal-backdrop flex items-center justify-center z-[9999] px-4 backdrop-blur-md">
            <div class="glass-panel w-full max-w-sm rounded-3xl p-6 border border-zinc-700 relative text-center scale-in-anim">
                <button onclick="document.getElementById('social-modal').classList.add('hidden')" class="absolute top-4 right-4 bg-black/50 backdrop-blur border border-zinc-700 hover:bg-zinc-700 transition w-8 h-8 rounded-full flex items-center justify-center text-zinc-300 hover:text-white z-10 hover:scale-110">âœ•</button>
                <h3 class="text-3xl text-white mb-6 teko-font tracking-wide">ğŸ“¸ INSTAGRAM HESAPLARIMIZ</h3>
                <div class="space-y-3">
                    <button onclick="window.open('https://instagram.com/om3r_10fr', '_blank')" class="w-full bg-gradient-to-r from-pink-600 to-orange-500 py-4 rounded-xl font-bold text-white shadow-md btn-premium-hover">@om3r_10fr</button>
                    <button onclick="window.open('https://instagram.com/om3r10_fr', '_blank')" class="w-full bg-gradient-to-r from-pink-600 to-orange-500 py-4 rounded-xl font-bold text-white shadow-md btn-premium-hover">@om3r10_fr</button>
                    <button onclick="window.open('https://instagram.com/freeridertr1', '_blank')" class="w-full bg-gradient-to-r from-pink-600 to-orange-500 py-4 rounded-xl font-bold text-white shadow-md btn-premium-hover">@freeridertr1</button>
                </div>
            </div>
        </div>

        <div id="rewards-modal" class="hidden fixed inset-0 modal-backdrop flex items-center justify-center z-[9999] px-4 backdrop-blur-md">
            <div class="glass-panel w-full max-w-sm rounded-3xl p-6 border border-zinc-700 relative text-center scale-in-anim">
                <button onclick="document.getElementById('rewards-modal').classList.add('hidden')" class="absolute top-4 right-4 bg-black/50 backdrop-blur border border-zinc-700 hover:bg-zinc-700 transition w-8 h-8 rounded-full flex items-center justify-center text-zinc-300 hover:text-white z-10 hover:scale-110">âœ•</button>
                <h3 class="text-4xl text-white mb-2 teko-font tracking-wide text-yellow-500 drop-shadow-md">ğŸ SIRALAMA Ã–DÃœLLERÄ°</h3>
                <p class="text-xs text-zinc-300 mb-6 font-medium">SÄ±ralamada ilk 3'e giren pedalÅŸÃ¶rler yÃ¶neticiler tarafÄ±ndan Ã¶dÃ¼llendirilir.</p>
                
                <div class="bg-black/50 border border-zinc-700 rounded-2xl p-4 mb-4 text-left shadow-inner">
                    <h4 class="text-sm font-bold text-blue-400 mb-2 uppercase tracking-widest border-b border-zinc-800 pb-2">ğŸ“… HaftalÄ±k YarÄ±ÅŸ</h4>
                    <div class="space-y-2 text-xs text-white">
                        <p class="flex justify-between items-center"><span>ğŸ¥‡ 1. Olan:</span> <span class="bg-yellow-500 text-black px-2 py-0.5 rounded font-bold shadow-md">1 Hafta Ultra+</span></p>
                        <p class="flex justify-between items-center"><span>ğŸ¥ˆ 2. Olan:</span> <span class="bg-purple-600 text-white px-2 py-0.5 rounded font-bold shadow-md">1 Hafta Deluxe</span></p>
                        <p class="flex justify-between items-center"><span>ğŸ¥‰ 3. Olan:</span> <span class="bg-purple-600 text-white px-2 py-0.5 rounded font-bold shadow-md">1 Hafta Deluxe</span></p>
                    </div>
                </div>
                
                <div class="bg-black/50 border border-zinc-700 rounded-2xl p-4 text-left shadow-inner">
                    <h4 class="text-sm font-bold text-orange-400 mb-2 uppercase tracking-widest border-b border-zinc-800 pb-2">ğŸ† AylÄ±k YarÄ±ÅŸ</h4>
                    <div class="space-y-2 text-xs text-white">
                        <p class="flex justify-between items-center"><span>ğŸ¥‡ 1. Olan:</span> <span class="bg-purple-600 text-white px-2 py-0.5 rounded font-bold shadow-md">1 Ay Deluxe</span></p>
                        <p class="flex justify-between items-center"><span>ğŸ¥ˆ 2. Olan:</span> <span class="bg-purple-600 text-white px-2 py-0.5 rounded font-bold shadow-md">1 Ay Deluxe</span></p>
                        <p class="flex justify-between items-center"><span>ğŸ¥‰ 3. Olan:</span> <span class="bg-purple-600 text-white px-2 py-0.5 rounded font-bold shadow-md">1 Ay Deluxe</span></p>
                    </div>
                </div>
            </div>
        </div>
        
        <div id="onboarding-modal" class="hidden fixed inset-0 modal-backdrop flex items-center justify-center z-[9999] px-4 backdrop-blur-md transition-opacity">
            <div class="glass-panel w-full max-w-md rounded-3xl p-6 border border-zinc-700 shadow-[0_0_40px_rgba(0,0,0,0.8)] relative text-center scale-in-anim overflow-y-auto max-h-[92dvh]">
                <div class="text-6xl mb-3 drop-shadow-[0_0_15px_rgba(255,255,255,0.3)] animate-bounce">ğŸ‘‹</div>
                <h2 class="text-4xl text-white mb-2 teko-font tracking-wide drop-shadow-md">FREERIDER<span class="text-sky-500">TR</span>'YE HOÅ GELDÄ°N!</h2>
                <p class="text-xs text-zinc-300 mb-4 font-medium">TÃ¼rkiye'nin en bÃ¼yÃ¼k Hardcore Downhill & Freeride topluluÄŸundasÄ±n.</p>

                <div class="bg-gradient-to-r from-yellow-600/20 to-amber-500/20 border border-yellow-500/50 rounded-2xl p-4 mb-4 text-left">
                    <div class="flex items-center gap-2 mb-2">
                        <span class="text-2xl">ğŸ</span>
                        <span class="text-yellow-400 font-black text-sm uppercase tracking-widest">3 GÃ¼nlÃ¼k Ãœcretsiz Ultra+ Aktif!</span>
                    </div>
                    <p class="text-xs text-zinc-300 leading-relaxed">SÄ±nÄ±rsÄ±z AI, Ã¶zel isim rengi, alev efekti, ÅŸans Ã§arkÄ± ve tÃ¼m premium Ã¶zellikler <b class="text-yellow-300">3 gÃ¼n boyunca tamamen Ã¼cretsiz</b>. Denemen bitince Plus sayfasÄ±ndan devam edebilirsin.</p>
                    <div id="onboarding-trial-date" class="mt-2 text-[10px] text-yellow-500 font-bold uppercase tracking-widest"></div>
                </div>

                <div class="space-y-2 text-left mb-5">
                    <div class="bg-zinc-950/80 p-3 rounded-xl border border-zinc-800 flex items-start gap-3">
                        <span class="text-xl mt-0.5 shrink-0">ğŸ—ºï¸</span>
                        <div><div class="text-white font-bold text-xs teko-font tracking-widest mb-0.5">HARÄ°TA & RADAR</div><p class="text-[10px] text-zinc-400 leading-relaxed">Ã‡evrendeki rampalarÄ± keÅŸfet! Radar modunu aÃ§arsan seni canlÄ± haritada gÃ¶rÃ¼rler.</p></div>
                    </div>
                    <div class="bg-zinc-950/80 p-3 rounded-xl border border-zinc-800 flex items-start gap-3">
                        <span class="text-xl mt-0.5 shrink-0">ğŸ’¬</span>
                        <div><div class="text-white font-bold text-xs teko-font tracking-widest mb-0.5">SOHBET & AI</div><p class="text-[10px] text-zinc-400 leading-relaxed">Toplulukla kaynaÅŸ, DM at, Freerider AI'a bisiklet sorularÄ± sor.</p></div>
                    </div>
                    <div class="bg-zinc-950/80 p-3 rounded-xl border border-zinc-800 flex items-start gap-3">
                        <span class="text-xl mt-0.5 shrink-0">ğŸ¯</span>
                        <div><div class="text-white font-bold text-xs teko-font tracking-widest mb-0.5">GÃ–REVLER & ÅANS Ã‡ARKI</div><p class="text-[10px] text-zinc-400 leading-relaxed">Her gÃ¼n gÃ¶rev tamamla, Ã§arkÄ± Ã§evir ve XP ile Ã¶dÃ¼ller kazan!</p></div>
                    </div>
                </div>

                <button onclick="completeOnboarding()" class="w-full bg-gradient-to-r from-yellow-600 to-sky-500 btn-premium-hover text-white py-4 rounded-xl font-black shadow-[0_0_20px_rgba(234,179,8,0.5)] text-lg tracking-widest">ğŸš´ DENEMEYÄ° BAÅLAT!</button>
                <p class="text-[10px] text-zinc-600 mt-2">Kredi kartÄ± gerekmez Â· Otomatik Ã¼cretlendirme yok</p>
            </div>
        </div>

        <div id="email-verify-modal" class="hidden fixed inset-0 modal-backdrop flex items-center justify-center z-[10000] px-4 backdrop-blur-md">
            <div class="glass-panel w-full max-w-md rounded-3xl p-6 border border-zinc-700 shadow-2xl text-center scale-in-anim">
                <h3 class="text-4xl text-white mb-2 teko-font tracking-wide drop-shadow-md">ğŸ“§ E-POSTA DOÄRULAMA</h3>
                <p class="text-xs text-zinc-300 mb-6 font-medium">E-posta adresinize 6 haneli bir doÄŸrulama kodu gÃ¶nderdik. LÃ¼tfen kodu aÅŸaÄŸÄ±ya girin.</p>
                <input id="verify-code-input" type="text" placeholder="6 Haneli Kod" class="w-full bg-black/60 border border-zinc-600 rounded-xl px-5 py-4 mb-6 text-white text-center text-2xl tracking-widest outline-none focus:border-white transition shadow-inner font-bold" maxlength="6">
                <div class="grid grid-cols-2 gap-3">
                    <button onclick="skipVerification()" class="py-4 bg-zinc-800 hover:bg-zinc-700 transition rounded-xl font-bold text-white text-sm shadow-md btn-premium-hover">SONRA YAP</button>
                    <button onclick="submitVerificationCode()" class="py-4 bg-sky-700 hover:bg-sky-600 transition rounded-xl font-bold text-white text-sm shadow-[0_0_15px_rgba(14,165,233,0.4)] btn-premium-hover">DOÄRULA</button>
                </div>
            </div>
        </div>

        <div id="forgot-password-modal" class="hidden fixed inset-0 modal-backdrop flex items-center justify-center z-[10000] px-4 backdrop-blur-md">
            <div class="glass-panel w-full max-w-md rounded-3xl p-6 border border-zinc-700 shadow-2xl scale-in-anim">
                <div class="flex justify-between items-center mb-6">
                    <h3 class="text-4xl text-white teko-font tracking-wide drop-shadow-md">ğŸ” ÅÄ°FREMÄ° UNUTTUM</h3>
                    <button onclick="closeForgotPasswordModal()" class="text-zinc-400 hover:text-white w-8 h-8 flex items-center justify-center bg-zinc-800 rounded-full transition hover:scale-110">âœ•</button>
                </div>
                
                <div id="fp-step-1" class="slide-up-anim">
                    <p class="text-xs text-zinc-300 mb-5 leading-relaxed font-medium">Sisteme kayÄ±tlÄ± ve doÄŸrulanmÄ±ÅŸ e-posta adresinizi girin. Size bir sÄ±fÄ±rlama kodu gÃ¶ndereceÄŸiz.</p>
                    <input id="fp-email" type="email" placeholder="E-posta Adresiniz" class="w-full bg-black/60 border border-zinc-600 rounded-xl px-5 py-4 mb-5 text-white text-sm outline-none focus:border-white transition shadow-inner font-bold">
                    <button onclick="requestPasswordReset()" class="w-full bg-white hover:bg-gray-200 transition text-black py-4 rounded-xl font-bold shadow-[0_0_15px_rgba(255,255,255,0.3)] text-sm tracking-wide btn-premium-hover">KOD GÃ–NDER</button>
                </div>
                
                <div id="fp-step-2" class="hidden slide-up-anim">
                    <p class="text-xs text-zinc-300 mb-4 font-medium">E-postanÄ±za gelen 6 haneli kodu ve yeni ÅŸifrenizi girin.</p>
                    <input id="fp-code" type="text" placeholder="6 Haneli Kod" class="w-full bg-black/60 border border-zinc-600 rounded-xl px-5 py-4 mb-3 text-white text-center tracking-widest text-lg outline-none focus:border-white transition font-bold shadow-inner" maxlength="6">
                    <input id="fp-new-password" type="password" placeholder="Yeni Åifreniz" class="w-full bg-black/60 border border-zinc-600 rounded-xl px-5 py-4 mb-6 text-white text-sm outline-none focus:border-white transition font-bold shadow-inner">
                    <button onclick="submitNewPassword()" class="w-full bg-sky-700 hover:bg-sky-600 transition text-white py-4 rounded-xl font-bold shadow-[0_0_15px_rgba(2,132,199,0.5)] text-sm tracking-wide btn-premium-hover">ÅÄ°FREYÄ° GÃœNCELLE</button>
                </div>
            </div>
        </div>

        <div id="add-bike-modal" class="hidden fixed inset-0 modal-backdrop flex items-center justify-center z-[9999] px-4 backdrop-blur-md">
            <div class="glass-panel w-full max-w-md rounded-3xl border border-zinc-700 shadow-2xl scale-in-anim max-h-[92vh] flex flex-col">
                <div class="p-5 border-b border-zinc-800 shrink-0 flex items-center justify-between">
                    <h3 class="text-3xl text-white teko-font tracking-wide">ğŸš² BÄ°SÄ°KLET EKLE</h3>
                    <button onclick="document.getElementById('add-bike-modal').classList.add('hidden')" class="w-8 h-8 bg-zinc-800 rounded-full text-zinc-400 hover:text-white flex items-center justify-center">âœ•</button>
                </div>
                <div class="overflow-y-auto p-5 flex-1 custom-scrollbar space-y-3">
                    <!-- Temel bilgiler -->
                    <div class="text-[10px] text-sky-300 font-bold uppercase tracking-widest mb-1">Temel Bilgiler *</div>
                    <input id="bike-model" type="text" placeholder="Marka ve Model (Ã–rn: Trek Session 8)" class="w-full bg-black/60 border border-zinc-700 rounded-xl px-4 py-3 text-white text-sm outline-none focus:border-sky-400 transition font-bold">
                    <select id="bike-type" class="w-full bg-black/60 border border-zinc-700 rounded-xl px-4 py-3 text-white text-sm outline-none focus:border-zinc-400 transition font-bold cursor-pointer">
                        <option value="Downhill">Downhill</option>
                        <option value="Freeride">Freeride</option>
                        <option value="Enduro">Enduro</option>
                        <option value="Dirt Jump">Dirt Jump</option>
                        <option value="Trail">Trail / XC</option>
                        <option value="Diger">DiÄŸer</option>
                    </select>

                    <!-- SÃ¼spansiyon -->
                    <div class="text-[10px] text-zinc-500 font-bold uppercase tracking-widest pt-2 border-t border-zinc-800">SÃ¼spansiyon</div>
                    <input id="bike-fork" type="text" placeholder="MaÅŸa (Ã–rn: Fox 40 Performance)" class="w-full bg-black/60 border border-zinc-700 rounded-xl px-4 py-3 text-white text-sm outline-none focus:border-zinc-400 transition">
                    <input id="bike-shock" type="text" placeholder="Arka Åok (Ã–rn: Fox Float X2)" class="w-full bg-black/60 border border-zinc-700 rounded-xl px-4 py-3 text-white text-sm outline-none focus:border-zinc-400 transition">

                    <!-- Fren sistemi -->
                    <div class="text-[10px] text-zinc-500 font-bold uppercase tracking-widest pt-2 border-t border-zinc-800">Fren Sistemi</div>
                    <input id="bike-brakes" type="text" placeholder="Frenler (Ã–rn: Shimano Saint 4-Piston)" class="w-full bg-black/60 border border-zinc-700 rounded-xl px-4 py-3 text-white text-sm outline-none focus:border-zinc-400 transition">
                    <input id="bike-rotor" type="text" placeholder="Disk Ã‡apÄ± (Ã–rn: 200mm/200mm)" class="w-full bg-black/60 border border-zinc-700 rounded-xl px-4 py-3 text-white text-sm outline-none focus:border-zinc-400 transition">

                    <!-- Aktarma -->
                    <div class="text-[10px] text-zinc-500 font-bold uppercase tracking-widest pt-2 border-t border-zinc-800">Aktarma Sistemi</div>
                    <input id="bike-drivetrain" type="text" placeholder="Vites Sistemi (Ã–rn: Shimano Deore 12V)" class="w-full bg-black/60 border border-zinc-700 rounded-xl px-4 py-3 text-white text-sm outline-none focus:border-zinc-400 transition">
                    <input id="bike-chain" type="text" placeholder="Zincir (Ã–rn: KMC e12 Turbo)" class="w-full bg-black/60 border border-zinc-700 rounded-xl px-4 py-3 text-white text-sm outline-none focus:border-zinc-400 transition">
                    <input id="bike-crankset" type="text" placeholder="Krank / BB (Ã–rn: Race Face Next R 170mm)" class="w-full bg-black/60 border border-zinc-700 rounded-xl px-4 py-3 text-white text-sm outline-none focus:border-zinc-400 transition">
                    <input id="bike-cassette" type="text" placeholder="Kasnak (Ã–rn: Shimano CS-M7100 10-51T)" class="w-full bg-black/60 border border-zinc-700 rounded-xl px-4 py-3 text-white text-sm outline-none focus:border-zinc-400 transition">

                    <!-- Tekerlek -->
                    <div class="text-[10px] text-zinc-500 font-bold uppercase tracking-widest pt-2 border-t border-zinc-800">Tekerlek</div>
                    <input id="bike-wheelset" type="text" placeholder="Jantlar (Ã–rn: Stan's Flow MK4 27.5)" class="w-full bg-black/60 border border-zinc-700 rounded-xl px-4 py-3 text-white text-sm outline-none focus:border-zinc-400 transition">
                    <input id="bike-tires" type="text" placeholder="Lastikler (Ã–rn: Maxxis Assegai 27.5x2.5 WT)" class="w-full bg-black/60 border border-zinc-700 rounded-xl px-4 py-3 text-white text-sm outline-none focus:border-zinc-400 transition">
                    <input id="bike-tire-size" type="text" placeholder="Lastik Boyutu / Hava BasÄ±ncÄ±" class="w-full bg-black/60 border border-zinc-700 rounded-xl px-4 py-3 text-white text-sm outline-none focus:border-zinc-400 transition">

                    <!-- Cockpit -->
                    <div class="text-[10px] text-zinc-500 font-bold uppercase tracking-widest pt-2 border-t border-zinc-800">Kokpit</div>
                    <input id="bike-handlebar" type="text" placeholder="Gidon (Ã–rn: Race Face Atlas 800mm 20mm rise)" class="w-full bg-black/60 border border-zinc-700 rounded-xl px-4 py-3 text-white text-sm outline-none focus:border-zinc-400 transition">
                    <input id="bike-stem" type="text" placeholder="Stem (Ã–rn: Race Face Ride 50mm)" class="w-full bg-black/60 border border-zinc-700 rounded-xl px-4 py-3 text-white text-sm outline-none focus:border-zinc-400 transition">
                    <input id="bike-grips" type="text" placeholder="Gidon TutuÅŸ (Ã–rn: ODI Ruffian Slim)" class="w-full bg-black/60 border border-zinc-700 rounded-xl px-4 py-3 text-white text-sm outline-none focus:border-zinc-400 transition">
                    <input id="bike-seatpost" type="text" placeholder="Seatpost / Tele (Ã–rn: BikeYoke Revive 160mm)" class="w-full bg-black/60 border border-zinc-700 rounded-xl px-4 py-3 text-white text-sm outline-none focus:border-zinc-400 transition">
                    <input id="bike-saddle" type="text" placeholder="Sele (Ã–rn: SDG Bel-Air 3.0)" class="w-full bg-black/60 border border-zinc-700 rounded-xl px-4 py-3 text-white text-sm outline-none focus:border-zinc-400 transition">
                    <input id="bike-pedals" type="text" placeholder="Pedallar (Ã–rn: Crankbrothers Stamp 7)" class="w-full bg-black/60 border border-zinc-700 rounded-xl px-4 py-3 text-white text-sm outline-none focus:border-zinc-400 transition">

                    <!-- Ekstra -->
                    <div class="text-[10px] text-zinc-500 font-bold uppercase tracking-widest pt-2 border-t border-zinc-800">AÄŸÄ±rlÄ±k & Notlar</div>
                    <input id="bike-weight" type="text" placeholder="Bisiklet AÄŸÄ±rlÄ±ÄŸÄ± (Ã–rn: 15.2 kg)" class="w-full bg-black/60 border border-zinc-700 rounded-xl px-4 py-3 text-white text-sm outline-none focus:border-zinc-400 transition">
                    <textarea id="bike-desc" placeholder="Ã–zel notlar, modifikasyonlar..." class="w-full bg-black/60 border border-zinc-700 rounded-xl px-4 py-3 h-20 text-white text-sm outline-none focus:border-zinc-400 transition custom-scrollbar"></textarea>

                    <!-- Gizli premium icon -->
                    <select id="new-marker-icon" class="hidden w-full bg-black/60 border border-zinc-700 rounded-xl px-4 py-3 text-white text-sm outline-none font-bold"></select>

                    <!-- FotoÄŸraf -->
                    <div id="bike-photo-label" class="text-[10px] text-zinc-400 font-bold uppercase tracking-widest mt-2">Bisiklet FotoÄŸraflarÄ±</div>
                    <input id="bike-photo" type="file" accept="image/*" multiple class="w-full bg-black/60 border border-zinc-700 rounded-xl px-3 py-3 text-xs text-zinc-300 cursor-pointer">
                    <div class="grid grid-cols-2 gap-3 pb-4">
                        <button onclick="document.getElementById('add-bike-modal').classList.add('hidden')" class="bg-zinc-900 border border-zinc-700 hover:bg-zinc-800 transition text-zinc-300 py-3 rounded-xl font-bold text-sm btn-premium-hover">Ä°ptal</button>
                        <button onclick="saveBike()" class="bg-gradient-to-r from-sky-700 to-sky-500 hover:opacity-90 transition text-white py-3 rounded-xl font-bold text-sm shadow-[0_0_15px_rgba(14,165,233,0.4)] btn-premium-hover">KAYDET</button>
                    </div>
                </div>
            </div>
        </div>

        <div id="bike-detail-modal" class="hidden fixed inset-0 modal-backdrop flex items-center justify-center z-[10000] px-4 backdrop-blur-md">
            <div class="glass-panel w-full max-w-md rounded-3xl p-6 border border-zinc-700 shadow-[0_0_40px_rgba(0,0,0,0.6)] relative max-h-[90dvh] overflow-y-auto custom-scrollbar scale-in-anim">
                <button onclick="document.getElementById('bike-detail-modal').classList.add('hidden')" class="absolute top-4 right-4 bg-black/50 backdrop-blur border border-zinc-700 hover:bg-zinc-700 transition w-8 h-8 rounded-full flex items-center justify-center text-zinc-300 hover:text-white z-10 hover:scale-110">âœ•</button>
                
                <div id="bd-image-container" class="market-img-scroll mb-4 shrink-0 h-48 bg-black/80 rounded-xl items-center custom-scrollbar border border-zinc-700 shadow-inner"></div>
                
                <h3 id="bd-model" class="text-4xl text-white mb-1 teko-font tracking-wide drop-shadow-md"></h3>
                <div id="bd-type" class="text-xs font-bold text-zinc-400 uppercase tracking-widest mb-6 bg-zinc-800/50 inline-block px-3 py-1 rounded-lg border border-zinc-700"></div>
                
                <div class="space-y-3 bg-black/50 p-5 rounded-2xl border border-zinc-700 shadow-inner">
                    <div>
                        <div class="text-[9px] text-zinc-500 font-bold uppercase tracking-widest mb-1">MaÅŸa / SÃ¼spansiyon</div>
                        <div id="bd-fork" class="text-sm text-white font-medium drop-shadow-sm">BelirtilmemiÅŸ</div>
                    </div>
                    <div class="border-t border-zinc-800 pt-3 mt-1">
                        <div class="text-[9px] text-zinc-500 font-bold uppercase tracking-widest mb-1">Arka Åok</div>
                        <div id="bd-shock" class="text-sm text-white font-medium drop-shadow-sm">BelirtilmemiÅŸ</div>
                    </div>
                    <div class="border-t border-zinc-800 pt-3 mt-1">
                        <div class="text-[9px] text-zinc-500 font-bold uppercase tracking-widest mb-1">Fren Sistemi</div>
                        <div id="bd-brakes" class="text-sm text-white font-medium drop-shadow-sm">BelirtilmemiÅŸ</div>
                    </div>
                    <div class="border-t border-zinc-800 pt-3 mt-1">
                        <div class="text-[9px] text-zinc-500 font-bold uppercase tracking-widest mb-1">AÃ§Ä±klama / Notlar</div>
                        <div id="bd-desc" class="text-sm text-zinc-300 italic leading-relaxed">BelirtilmemiÅŸ</div>
                    </div>
                    <div class="border-t border-zinc-800 pt-3 mt-1">
                        <div class="text-[9px] text-zinc-500 font-bold uppercase tracking-widest mb-2">Tum Parcalar</div>
                        <div id="bd-extra-specs" class="space-y-0"></div>
                    </div>
                </div>
                
                <div id="bd-actions-area" class="mt-5 flex gap-3"></div>
                
            </div>
        </div>

        <!-- Premium Alt Navigasyon Ã‡ubuÄŸu -->
        <!-- â”€â”€ PREMIUM FLOATING BOTTOM NAV â”€â”€ -->
        <div id="bottom-nav" class="relative shrink-0 z-[200]" style="display:none;background:linear-gradient(180deg,rgba(0,0,0,0) 0%,rgba(0,0,0,0.98) 100%);padding:6px 8px max(14px,env(safe-area-inset-bottom)) 8px;">
            <!-- Gradient separator line -->
            <div style="position:absolute;top:0;left:16px;right:16px;height:1px;background:linear-gradient(90deg,transparent,rgba(14,165,233,0.4),rgba(251,191,36,0.2),rgba(14,165,233,0.4),transparent);"></div>
            <div class="flex justify-around items-center">
                <button onclick="switchTab(0)" id="bnav-0" class="flex flex-col items-center gap-0.5 px-3 py-2 rounded-2xl transition-all duration-300 text-zinc-500" style="min-width:48px">
                    <span class="text-[22px] leading-none" style="transition:transform 0.3s cubic-bezier(0.34,1.56,0.64,1),filter 0.3s ease">ğŸ—ºï¸</span>
                    <span class="text-[9px] font-black uppercase tracking-widest mt-0.5" style="transition:all 0.2s">Harita</span>
                </button>
                <button onclick="switchTab(1)" id="bnav-1" class="flex flex-col items-center gap-0.5 px-3 py-2 rounded-2xl transition-all duration-300 text-zinc-500 relative" style="min-width:48px">
                    <span class="text-[22px] leading-none" style="transition:transform 0.3s cubic-bezier(0.34,1.56,0.64,1),filter 0.3s ease">ğŸ’¬</span>
                    <span class="text-[9px] font-black uppercase tracking-widest mt-0.5" style="transition:all 0.2s">Chat</span>
                </button>
                <!-- Reels - Merkez Ã–zel Buton -->
                <button onclick="switchTab(9)" id="bnav-9" class="flex flex-col items-center gap-0.5 px-3 py-2 rounded-2xl transition-all duration-300 text-zinc-500 relative" style="min-width:52px">
                    <div class="relative">
                        <span class="text-[24px] leading-none block" style="transition:transform 0.3s cubic-bezier(0.34,1.56,0.64,1),filter 0.3s ease">ğŸ¬</span>
                    </div>
                    <span class="text-[9px] font-black uppercase tracking-widest mt-0.5" style="transition:all 0.2s">Reels</span>
                </button>
                <button onclick="if(window.openAIHub) { window.openAIHub(); } else { alert('Hata: AI Hub kodu yuklenmedi!'); }" ontouchend="if(window.openAIHub) window.openAIHub();" id="bnav-ai" class="flex flex-col items-center gap-0.5 px-3 py-2 rounded-2xl transition-all duration-300 text-purple-400" style="min-width:48px; pointer-events: auto !important; position: relative; z-index: 9999999 !important;"><span class="text-[22px] leading-none" style="transition:transform 0.3s cubic-bezier(0.34,1.56,0.64,1),filter 0.3s ease">??</span><span class="text-[9px] font-black uppercase tracking-widest mt-0.5" style="transition:all 0.2s">AI Hub</span></button>
<button onclick="switchTab(3)" id="bnav-3" class="flex flex-col items-center gap-0.5 px-3 py-2 rounded-2xl transition-all duration-300 text-zinc-500" style="min-width:48px">
                    <span class="text-[22px] leading-none" style="transition:transform 0.3s cubic-bezier(0.34,1.56,0.64,1),filter 0.3s ease">ğŸ†</span>
                    <span class="text-[9px] font-black uppercase tracking-widest mt-0.5" style="transition:all 0.2s">SÄ±ra</span>
                </button>
                <button onclick="switchTab(7)" id="bnav-7" class="flex flex-col items-center gap-0.5 px-3 py-2 rounded-2xl transition-all duration-300 text-zinc-500" style="min-width:48px">
                    <span class="text-[22px] leading-none" style="transition:transform 0.3s cubic-bezier(0.34,1.56,0.64,1),filter 0.3s ease">ğŸ‘¤</span>
                    <span class="text-[9px] font-black uppercase tracking-widest mt-0.5" style="transition:all 0.2s">Profil</span>
                </button>
            </div>
        </div>

        <div id="settings-modal" class="hidden fixed inset-0 modal-backdrop flex items-center justify-center z-[9999] px-4 backdrop-blur-md">
            <div class="glass-panel w-full max-w-md rounded-3xl p-6 border border-zinc-700 shadow-2xl max-h-[90vh] overflow-y-auto custom-scrollbar relative scale-in-anim">
                <h3 class="text-4xl text-white mb-5 teko-font tracking-wide drop-shadow-md">âš™ï¸ PROFÄ°LÄ° DÃœZENLE</h3>
                <input id="edit-name" type="text" placeholder="Ä°sim" class="w-full bg-black/60 border border-zinc-700 rounded-xl px-5 py-4 mb-3 text-white text-sm outline-none focus:border-white transition font-bold shadow-inner">
                <input id="edit-bio" type="text" placeholder="KÄ±sa Bio..." class="w-full bg-black/60 border border-zinc-700 rounded-xl px-5 py-4 mb-3 text-white text-sm outline-none focus:border-white transition font-bold shadow-inner">
                <input id="edit-password" type="password" placeholder="Yeni ÅŸifre (DeÄŸiÅŸmeyecekse boÅŸ bÄ±rak)" class="w-full bg-black/60 border border-zinc-700 rounded-xl px-5 py-4 text-white text-sm outline-none focus:border-white transition font-bold shadow-inner">
                
                <div class="mt-5 border-t border-zinc-700 pt-5 mb-5">
                    <h4 class="text-[10px] text-zinc-400 uppercase tracking-widest font-bold mb-3">E-Posta & GÃ¼venlik</h4>
                    <div id="profile-email-status" class="mb-3"></div>
                   <input id="edit-email" type="email" placeholder="E-posta Adresi" oninput="checkEmailChange()" class="w-full bg-black/60 border border-zinc-700 rounded-xl px-5 py-4 mb-3 text-white text-sm outline-none focus:border-white transition font-bold shadow-inner">
                    <div class="flex items-start gap-2 mb-4 px-1">
                        <input type="checkbox" id="edit-marketing" class="w-4 h-4 mt-0.5 accent-sky-500 rounded cursor-pointer">
                        <label for="edit-marketing" class="text-[10px] text-zinc-400 font-medium cursor-pointer hover:text-white transition">Haberlerden ve gÃ¼ncellemelerden haberdar olmak istiyorum.</label>
                    </div>
                    <button onclick="requestProfileEmailVerify()" id="btn-verify-email" class="w-full bg-zinc-800 hover:bg-zinc-700 transition py-4 rounded-xl font-bold text-white text-xs border border-zinc-600 hidden uppercase tracking-widest shadow-md btn-premium-hover">DOÄRULAMA KODU GÃ–NDER</button>
                </div>

                <div class="grid grid-cols-2 gap-3 mt-2">
                    <button onclick="closeSettingsModal()" class="py-4 bg-zinc-800 hover:bg-zinc-700 transition rounded-xl font-bold text-white text-sm shadow-md btn-premium-hover">Ä°PTAL</button>
                    <button onclick="saveSettings()" class="py-4 bg-white hover:bg-gray-200 transition rounded-xl font-bold text-black text-sm shadow-[0_0_15px_rgba(255,255,255,0.3)] btn-premium-hover">KAYDET</button>
                </div>

                <div class="mt-6 pt-5 border-t border-zinc-800">
                    <p class="text-[10px] text-zinc-500 mb-3 uppercase tracking-widest font-bold">Uygulama Turu</p>
                    <button onclick="closeSettingsModal(); setTimeout(() => OnboardingManager.startTour(), 300);" class="w-full bg-zinc-900 border border-zinc-700 hover:bg-zinc-800 transition text-zinc-300 py-3 rounded-xl font-bold text-xs uppercase tracking-widest shadow-md">ğŸš€ Uygulama Turunu Yeniden BaÅŸlat</button>
                </div>

                <div class="mt-6 pt-5 border-t border-zinc-800">
                    <p class="text-[10px] text-zinc-500 mb-3 uppercase tracking-widest font-bold">Tehlikeli BÃ¶lge</p>
                    <button onclick="openDeleteAccountModal()" class="w-full bg-black border border-sky-900/60 hover:bg-red-950/40 transition text-sky-400 py-3 rounded-xl font-bold text-xs uppercase tracking-widest btn-premium-hover">ğŸ—‘ï¸ HesabÄ±mÄ± KalÄ±cÄ± Olarak Sil</button>
                </div>
            </div>
        </div>

        <!-- HESAP SÄ°LME ONAY MODALI -->
        <div id="delete-account-modal" class="hidden fixed inset-0 modal-backdrop flex items-center justify-center z-[99999] px-4 backdrop-blur-md">
            <div class="glass-panel w-full max-w-sm rounded-3xl p-6 border border-sky-900/50 shadow-2xl scale-in-anim">
                <div class="text-center mb-5">
                    <div class="text-5xl mb-3">âš ï¸</div>
                    <h3 class="text-2xl text-sky-300 teko-font tracking-wide">HESABI SÄ°L</h3>
                    <p class="text-xs text-zinc-400 mt-2 leading-relaxed">Bu iÅŸlem <b class="text-sky-300">geri alÄ±namaz.</b> Profilin, gÃ¶nderilerin, ilanlarÄ±n ve tÃ¼m verilen kalÄ±cÄ± olarak silinir.</p>
                </div>
                <input id="delete-account-password" type="password" placeholder="Onaylamak iÃ§in ÅŸifreni gir" class="w-full bg-black/60 border border-sky-800/60 rounded-xl px-4 py-3 text-white text-sm outline-none focus:border-sky-400 transition font-bold mb-4">
                <div class="grid grid-cols-2 gap-3">
                    <button onclick="document.getElementById('delete-account-modal').classList.add('hidden')" class="bg-zinc-900 border border-zinc-700 text-zinc-400 py-3 rounded-xl font-bold text-sm">VazgeÃ§</button>
                    <button onclick="confirmDeleteAccount()" class="bg-sky-800 hover:bg-sky-700 text-white py-3 rounded-xl font-bold text-sm btn-premium-hover uppercase tracking-widest">HESABI SÄ°L</button>
                </div>
            </div>
        </div>

        <div id="other-profile-modal" class="hidden fixed inset-0 modal-backdrop flex items-center justify-center z-[9999] px-4 backdrop-blur-md">
            <div class="glass-panel w-full max-w-sm rounded-3xl p-6 border border-zinc-700 relative text-center overflow-y-auto max-h-[90dvh] custom-scrollbar shadow-[0_0_40px_rgba(0,0,0,0.6)] scale-in-anim">
                <button onclick="document.getElementById('other-profile-modal').classList.add('hidden')" class="absolute top-4 right-4 bg-black/50 backdrop-blur border border-zinc-700 hover:bg-zinc-700 transition text-zinc-300 hover:text-white w-8 h-8 rounded-full flex items-center justify-center hover:scale-110 z-10">âœ•</button>
                
                <img id="op-avatar" src="" class="w-28 h-28 mx-auto rounded-full object-cover mt-6 bg-zinc-950 shadow-xl border-4 transition-all duration-300">
                <div id="op-premium-badge" class="hidden mt-3 text-xs font-bold uppercase tracking-widest"></div>
                            <div id="op-online-status" class="hidden flex items-center gap-2 justify-center mt-2"></div>
                
                <div id="op-username-container" class="flex justify-center items-center gap-1 mt-3">
                    <div id="op-username" class="text-4xl font-bold text-white break-all teko-font tracking-wide drop-shadow-md transition-all"></div>
                    <div id="op-verified-badge" class="hidden"></div>
                </div>
                
                <div id="op-bio" class="text-zinc-300 mt-2 text-sm font-medium px-2 leading-relaxed"></div>
                
                <div class="flex justify-center gap-4 mt-8">
                    <div class="bg-black/50 p-4 rounded-2xl w-28 border border-zinc-700 shadow-inner">
                        <div id="op-xp" class="text-3xl text-white teko-font tracking-wide drop-shadow-sm"></div>
                        <div class="text-[9px] text-zinc-500 mt-1 font-bold uppercase tracking-widest">XP</div>
                    </div>
                    <div class="bg-black/50 p-4 rounded-2xl w-28 border border-zinc-700 shadow-inner">
                        <div id="op-title" class="text-sm font-bold text-zinc-300 truncate uppercase mt-1 drop-shadow-sm"></div>
                        <div class="text-[9px] text-zinc-500 mt-2 font-bold uppercase tracking-widest">ÃœNVAN</div>
                    </div>
                </div>
                                
                <div class="mt-8 text-left pb-4 bg-black/40 p-5 rounded-2xl border border-zinc-700/50 shadow-inner">
                    <h3 class="text-[10px] font-bold text-zinc-400 mb-4 uppercase tracking-widest flex items-center gap-2"><span>ğŸš²</span> GarajÄ±</h3>
                    <div id="op-garage" class="grid grid-cols-2 gap-3"></div>
                </div>
                
                <div class="mt-6 text-left pb-4 bg-black/40 p-5 rounded-2xl border border-zinc-700/50 shadow-inner">
                    <h3 class="text-[10px] font-bold text-zinc-400 mb-4 uppercase tracking-widest flex items-center gap-2"><span>ğŸ…</span> KazanÄ±lan Rozetler</h3>
                    <div id="op-badges" class="flex flex-wrap gap-2"></div>
                </div>
                
                <div id="op-actions" class="border-t border-zinc-700/50 pt-6 mt-6 space-y-3"></div>
            </div>
        </div>

        <div id="chat-rules-modal" class="hidden fixed inset-0 modal-backdrop flex items-center justify-center z-[9999] px-4 py-10 backdrop-blur-md">
            <div class="glass-panel w-full max-w-md rounded-3xl p-6 border border-zinc-700 flex flex-col shadow-2xl scale-in-anim">
                <h2 class="text-4xl text-white mb-4 teko-font tracking-wide drop-shadow-md">ğŸ“œ TOPLULUK KURALLARI</h2>
                <div class="overflow-y-auto flex-1 text-sm text-zinc-300 space-y-4 mb-5 custom-scrollbar pr-2 bg-black/50 p-5 rounded-2xl border border-zinc-700 shadow-inner leading-relaxed font-medium">
                    <ul class="list-disc pl-5 space-y-3">
                        <li><b>+18 ve Cinsel Ä°Ã§erik Kesinlikle YasaktÄ±r:</b> Gruba gÃ¶nderilen her tÃ¼rlÃ¼ cinsel iÃ§erik kalÄ±cÄ± olarak engellenir.</li>
                        <li><b>Taciz ve ZorbalÄ±k YasaktÄ±r:</b> DiÄŸer Ã¼yeleri Ã¶zelden veya gruptan rahatsÄ±z etmek affedilmez.</li>
                        <li><b>AyrÄ±mcÄ±lÄ±k ve Nefret SÃ¶ylemi:</b> Din, dil, Ä±rk, mezhep ayrÄ±mcÄ±lÄ±ÄŸÄ± yapmak yasaktÄ±r. Bizi birleÅŸtiren ÅŸey bisiklet tutkusudur.</li>
                        <li><b>Spam ve Reklam YasaktÄ±r:</b> Ä°zin alÄ±nmadan yapÄ±lan ticari reklamlar yasaktÄ±r. Pazar sekmesini kullanÄ±n.</li>
                    </ul>
                    <p class="text-xs text-sky-300 font-bold mt-5 border-t border-zinc-800 pt-4">Ã–NEMLÄ°: KurallarÄ± ihlal eden Ã¼yeler uyarÄ±sÄ±z olarak sistemden KALICI olarak uzaklaÅŸtÄ±rÄ±lÄ±r.</p>
                </div>
                <div class="flex flex-col gap-3 shrink-0">
                    <button onclick="acceptChatRules()" class="w-full bg-white hover:bg-gray-200 transition text-black py-4 rounded-xl font-bold text-sm shadow-[0_0_15px_rgba(255,255,255,0.3)] btn-premium-hover">OKUDUM, KABUL EDÄ°YORUM</button>
                    <button onclick="switchTab(0)" class="w-full bg-zinc-800 hover:bg-zinc-700 transition py-4 rounded-xl font-bold text-zinc-300 text-sm shadow-md btn-premium-hover">VazgeÃ§ ve Geri DÃ¶n</button>
                </div>
            </div>
        </div>

        <div id="market-modal" class="hidden fixed inset-0 modal-backdrop flex items-center justify-center z-[9999] px-4 overflow-y-auto py-10 backdrop-blur-md">
            <div class="glass-panel w-full max-w-md rounded-3xl p-6 border border-zinc-700 my-auto shadow-[0_0_40px_rgba(0,0,0,0.6)] scale-in-anim">
                <h2 class="text-4xl text-white mb-6 teko-font tracking-wide drop-shadow-md">ğŸ›’ YENÄ° Ä°LAN</h2>
                <input id="mk-title" type="text" placeholder="ÃœrÃ¼n AdÄ±" class="w-full bg-black/60 border border-zinc-700 rounded-xl px-5 py-4 mb-3 text-white text-sm outline-none focus:border-white transition font-bold shadow-inner">
                <input id="mk-price" type="number" placeholder="Fiyat (TL)" class="w-full bg-black/60 border border-zinc-700 rounded-xl px-5 py-4 mb-3 text-white text-sm outline-none focus:border-white transition font-bold shadow-inner">
                <input id="mk-contact" type="text" placeholder="Ä°letiÅŸim Bilgisi (Tel/Insta)" class="w-full bg-black/60 border border-zinc-700 rounded-xl px-5 py-4 mb-3 text-white text-sm outline-none focus:border-white transition font-bold shadow-inner">
                <textarea id="mk-desc" placeholder="AÃ§Ä±klama..." class="w-full bg-black/60 border border-zinc-700 rounded-xl px-5 py-4 h-24 mb-5 text-white text-sm outline-none focus:border-white transition custom-scrollbar font-bold shadow-inner"></textarea>
                
                <label id="mk-photo-label" class="block text-[10px] text-zinc-400 mb-2 uppercase font-bold tracking-widest">FotoÄŸraf Ekle</label>
                <input id="mk-photos" type="file" accept="image/*" multiple class="w-full bg-black/60 border border-zinc-700 rounded-xl px-3 py-3 mb-5 text-xs text-zinc-300 focus:border-white transition cursor-pointer">
                
                <div class="grid grid-cols-2 gap-3 mt-2">
                    <button onclick="document.getElementById('market-modal').classList.add('hidden')" class="py-4 bg-zinc-800 hover:bg-zinc-700 transition rounded-xl font-bold text-white text-sm shadow-md btn-premium-hover">Ä°PTAL</button>
                    <button onclick="saveMarketItem()" class="py-4 bg-white hover:bg-gray-200 transition rounded-xl font-bold text-black text-sm shadow-[0_0_15px_rgba(255,255,255,0.3)] btn-premium-hover">Ä°LANI YAYINLA</button>
                </div>
            </div>
        </div>
        
        <div id="market-detail-modal" class="hidden fixed inset-0 modal-backdrop flex items-center justify-center z-[9999] px-4 backdrop-blur-md">
            <div class="glass-panel w-full max-w-md rounded-3xl p-6 border border-zinc-700 relative flex flex-col max-h-[90dvh] shadow-[0_0_40px_rgba(0,0,0,0.6)] scale-in-anim">
                <button onclick="document.getElementById('market-detail-modal').classList.add('hidden')" class="absolute top-4 right-4 bg-black/50 backdrop-blur border border-zinc-700 hover:bg-zinc-700 transition w-8 h-8 rounded-full flex items-center justify-center text-zinc-300 hover:text-white z-10 hover:scale-110">âœ•</button>
                
                <div id="md-photos" class="market-img-scroll mb-5 shrink-0 h-48 bg-black/80 rounded-xl items-center custom-scrollbar border border-zinc-700 shadow-inner"></div>
                
                <div class="overflow-y-auto flex-1 pr-2 custom-scrollbar">
                    <h3 id="md-title" class="text-4xl text-white mb-2 teko-font tracking-wide drop-shadow-md"></h3>
                    <div id="md-price" class="text-2xl font-black text-green-400 mb-3 bg-green-950/40 inline-block px-4 py-1.5 rounded-xl border border-green-800/50 shadow-md"></div>
                    <div id="md-views-badge" class="hidden text-xs font-bold text-yellow-400 mb-6 bg-yellow-900/30 inline-block px-3 py-1.5 rounded-xl border border-yellow-700/50 ml-2 shadow-md"></div>
                    
                    <div class="flex items-center gap-4 mb-6 bg-black/50 p-4 rounded-2xl cursor-pointer hover:bg-zinc-800 transition-colors border border-zinc-700 shadow-inner group" onclick="if(window.currentOwner) showOtherProfile(window.currentOwner)">
                        <img id="md-owner-avatar" class="w-14 h-14 rounded-full object-cover border-2 border-zinc-600 group-hover:border-zinc-400 transition-colors shadow-md">
                        <div>
                            <div class="text-[10px] text-zinc-400 uppercase font-bold tracking-widest mb-1">SatÄ±cÄ±</div>
                            <div id="md-owner" class="text-base font-bold text-white tracking-wide group-hover:text-blue-300 transition-colors"></div>
                        </div>
                    </div>
                    
                    <p id="md-desc" class="text-sm text-zinc-300 mb-6 whitespace-pre-wrap break-all leading-relaxed font-medium bg-black/30 p-4 rounded-xl border border-zinc-800/50"></p>
                    
                    <div class="bg-blue-950/30 border border-blue-800/50 p-5 rounded-2xl mb-4 text-center shadow-inner">
                        <div class="text-[10px] text-blue-300 mb-2 uppercase font-bold tracking-widest flex justify-center items-center gap-2"><span class="animate-pulse">ğŸ“</span> Ä°letiÅŸim Bilgisi</div>
                        <div id="md-contact" class="font-black text-white text-xl break-all drop-shadow-sm"></div>
                    </div>
                </div>
                
                <div id="md-actions-area" class="mt-5 shrink-0 space-y-3"></div>
            </div>
        </div>

        <!-- CATEGORY SELECT MODAL -->
        <div id="category-select-modal" class="hidden fixed inset-0 modal-backdrop flex items-center justify-center z-[9999] px-4 backdrop-blur-md">
            <div class="glass-panel w-full max-w-md rounded-3xl p-6 border border-zinc-700 shadow-[0_0_40px_rgba(0,0,0,0.6)] scale-in-anim">
                <h2 class="text-4xl text-white mb-2 teko-font tracking-wide drop-shadow-md text-center">ğŸ“ KATEGORÄ° SEÃ‡Ä°N</h2>
                <p class="text-zinc-400 text-xs text-center mb-6 font-bold">Haritaya eklemek istediÄŸiniz nokta tÃ¼rÃ¼nÃ¼ seÃ§in.</p>
                <div class="grid grid-cols-2 gap-3 mb-6">
                    <button onclick="selectMarkerCategory('Rampa')" class="bg-black/40 border border-zinc-700 rounded-xl p-3 flex flex-col items-center gap-2 hover:bg-zinc-800 transition btn-premium-hover">
                        <i data-lucide="mountain-snow" class="text-sky-400"></i>
                        <span class="text-white text-xs font-bold">Rampa</span>
                    </button>
                    <button onclick="selectMarkerCategory('BisikletÃ§i')" class="bg-black/40 border border-zinc-700 rounded-xl p-3 flex flex-col items-center gap-2 hover:bg-zinc-800 transition btn-premium-hover">
                        <i data-lucide="wrench" class="text-orange-400"></i>
                        <span class="text-white text-xs font-bold">BisikletÃ§i</span>
                    </button>
                    <button onclick="selectMarkerCategory('Market')" class="bg-black/40 border border-zinc-700 rounded-xl p-3 flex flex-col items-center gap-2 hover:bg-zinc-800 transition btn-premium-hover">
                        <i data-lucide="shopping-cart" class="text-green-400"></i>
                        <span class="text-white text-xs font-bold">Market</span>
                    </button>
                    <button onclick="selectMarkerCategory('Trail')" class="bg-black/40 border border-zinc-700 rounded-xl p-3 flex flex-col items-center gap-2 hover:bg-zinc-800 transition btn-premium-hover">
                        <i data-lucide="map" class="text-emerald-500"></i>
                        <span class="text-white text-xs font-bold">Trail</span>
                    </button>
                    <button onclick="selectMarkerCategory('Drop')" class="bg-black/40 border border-zinc-700 rounded-xl p-3 flex flex-col items-center gap-2 hover:bg-zinc-800 transition btn-premium-hover">
                        <i data-lucide="arrow-down-to-line" class="text-purple-400"></i>
                        <span class="text-white text-xs font-bold">Drop</span>
                    </button>
                    <button onclick="selectMarkerCategory('Dirt Jump')" class="bg-black/40 border border-zinc-700 rounded-xl p-3 flex flex-col items-center gap-2 hover:bg-zinc-800 transition btn-premium-hover">
                        <i data-lucide="zap" class="text-yellow-400"></i>
                        <span class="text-white text-xs font-bold">Dirt Jump</span>
                    </button>
                    <button onclick="selectMarkerCategory('Tamir NoktasÄ±')" class="bg-black/40 border border-zinc-700 rounded-xl p-3 flex flex-col items-center gap-2 hover:bg-zinc-800 transition btn-premium-hover">
                        <i data-lucide="hammer" class="text-blue-400"></i>
                        <span class="text-white text-xs font-bold">Tamir NoktasÄ±</span>
                    </button>
                    <button onclick="selectMarkerCategory('Su KaynaÄŸÄ±')" class="bg-black/40 border border-zinc-700 rounded-xl p-3 flex flex-col items-center gap-2 hover:bg-zinc-800 transition btn-premium-hover">
                        <i data-lucide="droplet" class="text-cyan-400"></i>
                        <span class="text-white text-xs font-bold">Su KaynaÄŸÄ±</span>
                    </button>
                    <button onclick="selectMarkerCategory('Toplanma NoktasÄ±')" class="bg-black/40 border border-zinc-700 rounded-xl p-3 flex flex-col items-center gap-2 hover:bg-zinc-800 transition btn-premium-hover">
                        <i data-lucide="map-pin" class="text-pink-400"></i>
                        <span class="text-white text-xs font-bold">Toplanma NoktasÄ±</span>
                    </button>
                    <button onclick="selectMarkerCategory('Tehlikeli BÃ¶lge')" class="bg-black/40 border border-zinc-700 rounded-xl p-3 flex flex-col items-center gap-2 hover:bg-zinc-800 transition btn-premium-hover">
                        <i data-lucide="triangle-alert" class="text-red-500"></i>
                        <span class="text-white text-xs font-bold">Tehlikeli BÃ¶lge</span>
                    </button>
                </div>
                <button onclick="document.getElementById('category-select-modal').classList.add('hidden')" class="w-full py-4 bg-zinc-800 hover:bg-zinc-700 transition rounded-xl font-bold text-white text-sm shadow-md btn-premium-hover">Ä°PTAL</button>
            </div>
        </div>

        <div id="add-marker-modal" class="hidden fixed inset-0 modal-backdrop flex items-center justify-center z-[9999] px-4 backdrop-blur-md">
            <div class="glass-panel w-full max-w-md rounded-3xl p-6 border border-zinc-700 shadow-[0_0_40px_rgba(0,0,0,0.6)] scale-in-anim">
                <h2 id="modal-marker-title" class="text-4xl text-white mb-2 teko-font tracking-wide drop-shadow-md">ğŸ“ NOKTA EKLE</h2>
                <p id="modal-marker-category-label" class="text-sky-400 text-xs mb-5 font-bold uppercase tracking-wider"></p>
                <input id="new-marker-name" type="text" placeholder="BaÅŸlÄ±k" class="w-full bg-black/60 border border-zinc-700 rounded-xl px-5 py-4 mb-3 text-white text-sm outline-none focus:border-white transition font-bold shadow-inner">
                
                <div class="flex gap-3 mb-3">
                    <select id="new-marker-difficulty" class="flex-1 bg-black/60 border border-zinc-700 rounded-xl px-4 py-4 text-white font-bold text-xs outline-none focus:border-white transition shadow-inner cursor-pointer">
                        <option value="Kolay">ğŸŸ¢ Kolay Seviye</option>
                        <option value="Orta" selected>ğŸŸ¡ Orta Seviye</option>
                        <option value="Zor">ğŸ”´ Zor Seviye</option>
                        <option value="Tehlike">ğŸ’€ Ã‡ok Tehlikeli</option>
                    </select>
                </div>
                
                <textarea id="new-marker-desc" placeholder="AÃ§Ä±klama / NasÄ±l Gidilir?" class="w-full bg-black/60 border border-zinc-700 rounded-xl px-5 py-3 h-20 mb-3 text-white text-sm outline-none focus:border-white transition custom-scrollbar font-bold shadow-inner"></textarea>
                <textarea id="new-marker-extranote" placeholder="Ekstra Not / UyarÄ±lar..." class="w-full bg-black/60 border border-zinc-700 rounded-xl px-5 py-3 h-16 mb-4 text-white text-sm outline-none focus:border-white transition custom-scrollbar font-bold shadow-inner"></textarea>
                
                <label class="block text-[10px] text-zinc-400 mb-2 uppercase font-bold tracking-widest">FotoÄŸraf (Ä°steÄŸe BaÄŸlÄ±)</label>
                <input id="new-marker-photo" type="file" accept="image/*" class="w-full bg-black/60 border border-zinc-700 rounded-xl px-3 py-3 mb-6 text-xs text-zinc-300 focus:border-white transition cursor-pointer">
                
                <div class="grid grid-cols-2 gap-3">
                    <button onclick="closeMarkerModal()" class="py-4 bg-zinc-800 hover:bg-zinc-700 transition rounded-xl font-bold text-white text-sm shadow-md btn-premium-hover">Ä°PTAL</button>
                    <button onclick="saveNewMarker()" class="py-4 bg-white hover:bg-gray-200 transition rounded-xl font-bold text-black text-sm shadow-[0_0_15px_rgba(255,255,255,0.3)] btn-premium-hover">KAYDET</button>
                </div>
            </div>
        </div>

        <div id="add-event-modal" class="hidden fixed inset-0 modal-backdrop flex items-center justify-center z-[9999] px-4 backdrop-blur-md">
            <div class="glass-panel w-full max-w-md rounded-3xl p-6 border border-zinc-700 shadow-[0_0_40px_rgba(0,0,0,0.6)] scale-in-anim">
                <h2 class="text-4xl text-white mb-5 teko-font tracking-wide drop-shadow-md">ğŸ“… BULUÅMA EKLE</h2>
                <input id="ev-title" type="text" placeholder="BaÅŸlÄ±k (Ã–rn: Sabah AntrenmanÄ±)" class="w-full bg-black/60 border border-zinc-700 rounded-xl px-5 py-4 mb-3 text-white text-sm outline-none focus:border-white transition font-bold shadow-inner">
                
                <div class="flex gap-3 mb-3">
                    <input id="ev-date" type="date" class="flex-1 bg-black/60 border border-zinc-700 rounded-xl px-4 py-4 outline-none text-sm text-white font-bold focus:border-white transition shadow-inner">
                    <input id="ev-time" type="time" class="w-28 bg-black/60 border border-zinc-700 rounded-xl px-3 py-4 outline-none text-sm text-white font-bold focus:border-white transition shadow-inner">
                </div>
                
                <input id="ev-max" type="number" placeholder="KiÅŸi SÄ±nÄ±rÄ± (Opsiyonel)" class="w-full bg-black/60 border border-zinc-700 rounded-xl px-5 py-4 mb-3 text-white text-sm outline-none focus:border-white transition font-bold shadow-inner">
                <textarea id="ev-desc" placeholder="AÃ§Ä±klama..." class="w-full bg-black/60 border border-zinc-700 rounded-xl px-5 py-4 h-24 mb-6 text-white text-sm outline-none focus:border-white transition custom-scrollbar font-bold shadow-inner"></textarea>
                
                <div class="grid grid-cols-2 gap-3">
                    <button onclick="document.getElementById('add-event-modal').classList.add('hidden')" class="py-4 bg-zinc-800 hover:bg-zinc-700 transition rounded-xl font-bold text-white text-sm shadow-md btn-premium-hover">Ä°PTAL</button>
                    <button onclick="saveEvent()" class="py-4 bg-white hover:bg-gray-200 transition rounded-xl font-bold text-black text-sm shadow-[0_0_15px_rgba(255,255,255,0.3)] btn-premium-hover">OLUÅTUR</button>
                </div>
            </div>
        </div>
        
        <div id="marker-sheet" class="hidden fixed glass-panel border-t border-zinc-700 rounded-t-3xl shadow-[0_-20px_50px_rgba(0,0,0,0.8)] p-5 z-[9999] max-h-[88vh] flex flex-col slide-up-anim overflow-hidden" style="bottom:0;left:0;right:0;width:100%;max-width:100%;margin-left:auto;margin-right:auto;box-sizing:border-box;transform:none;">
            <div id="ms-danger-banner" class="hidden bg-red-950/70 border border-sky-700/50 text-red-300 text-xs font-bold px-4 py-2 rounded-xl mb-3 flex items-center gap-2 shrink-0"></div>
            <div class="flex justify-between items-start mb-5 border-b border-zinc-700 pb-4 shrink-0">
                <div class="flex-1 pr-4">
                    <h3 id="ms-title" class="text-4xl text-white teko-font tracking-wide break-words drop-shadow-md"></h3>
                    <div class="flex gap-2 flex-wrap mt-2">
                        <span id="ms-category" class="text-[10px] bg-sky-600/30 text-sky-300 border border-sky-500/30 px-3 py-1.5 rounded-lg inline-block uppercase tracking-widest font-bold shadow-inner"></span>
                        <span id="ms-difficulty" class="text-[10px] bg-zinc-800 text-zinc-300 border border-zinc-700 px-3 py-1.5 rounded-lg inline-block uppercase tracking-widest font-bold shadow-inner"></span>
                    </div>
                </div>
                <button onclick="closeMarkerSheet()" class="bg-black/50 hover:bg-zinc-700 transition w-10 h-10 rounded-full flex items-center justify-center text-zinc-300 hover:text-white shrink-0 border border-zinc-700 hover:scale-110 shadow-md">âœ•</button>
            </div>
            
            <div class="overflow-y-auto custom-scrollbar flex-1 pb-4">
                <div id="ms-image-container" class="mb-5"></div>
                <p id="ms-desc" class="text-sm text-zinc-300 bg-black/40 p-5 rounded-2xl border border-zinc-700 mb-5 whitespace-pre-wrap break-words font-medium leading-relaxed shadow-inner"></p>
                <div id="ms-extranote-container" class="hidden text-sm text-sky-200 bg-sky-900/20 p-4 rounded-xl border border-sky-800/50 mb-5 whitespace-pre-wrap break-words font-medium leading-relaxed shadow-inner">
                    <div class="text-[10px] text-sky-400 font-bold uppercase tracking-widest mb-1">Ekstra Not</div>
                    <span id="ms-extranote"></span>
                </div>
                
                <div class="flex justify-between gap-3 mb-5">
                    <button id="ms-btn-like" onclick="toggleMarkerInteraction('like')" class="flex-1 bg-black/50 border border-zinc-700 hover:bg-zinc-800 transition py-4 rounded-xl flex items-center justify-center gap-2 font-bold text-base text-white shadow-md btn-premium-hover">
                        <span class="text-xl">ğŸ‘</span> <span id="ms-likes-count">0</span>
                    </button>
                    <button id="ms-btn-dislike" onclick="toggleMarkerInteraction('dislike')" class="flex-1 bg-black/50 border border-zinc-700 hover:bg-zinc-800 transition py-4 rounded-xl flex items-center justify-center gap-2 font-bold text-base text-white shadow-md btn-premium-hover">
                        <span class="text-xl">ğŸ‘</span> <span id="ms-dislikes-count">0</span>
                    </button>
                </div>

                <a id="ms-btn-directions" href="#" target="_blank" class="w-full flex items-center justify-center gap-2 bg-blue-600/20 hover:bg-blue-600/40 border border-blue-500/50 transition text-blue-300 py-4 rounded-xl font-bold text-sm shadow-lg mb-3 uppercase tracking-widest btn-premium-hover"><span class="text-lg">ğŸ—ºï¸</span> YOL TARÄ°FÄ° AL</a>
                
                <!-- Puan verme -->
                <div id="ms-rating" class="mt-3 mb-2">
                    <div class="text-[10px] text-zinc-500 font-bold uppercase tracking-widest mb-2">RampayÄ± Puan Ver</div>
                    <div class="flex items-center gap-2">
                        <div id="ms-stars" class="flex gap-1">
                            <span onclick="rateMarker(1)" class="text-2xl cursor-pointer hover:scale-125 transition-transform">â­</span>
                            <span onclick="rateMarker(2)" class="text-2xl cursor-pointer hover:scale-125 transition-transform">â­</span>
                            <span onclick="rateMarker(3)" class="text-2xl cursor-pointer hover:scale-125 transition-transform">â­</span>
                            <span onclick="rateMarker(4)" class="text-2xl cursor-pointer hover:scale-125 transition-transform">â­</span>
                            <span onclick="rateMarker(5)" class="text-2xl cursor-pointer hover:scale-125 transition-transform">â­</span>
                        </div>
                        <span id="ms-avg-rating" class="text-xs text-zinc-400 font-bold"></span>
                    </div>
                </div>
                <button onclick="openDangerReport()" class="w-full bg-red-950/40 border border-sky-800/50 hover:bg-sky-900/30 transition text-sky-300 py-2.5 rounded-xl font-bold text-xs mb-2 btn-premium-hover flex items-center justify-center gap-2">
                    <span>âš ï¸</span> Tehlike Bildir
                </button>
                <button onclick="openComments('marker', currentMarkerId)" class="w-full bg-zinc-900/80 border border-zinc-700 hover:bg-zinc-800 transition text-zinc-300 py-3 rounded-xl font-bold text-sm mb-3 btn-premium-hover flex items-center justify-center gap-2 mt-1">
                    <span>ğŸ’¬</span> Yorumlar
                </button>
                <div id="ms-admin-controls" class="hidden flex gap-3 mt-5 pt-5 border-t border-zinc-700">
                    <button id="ms-btn-edit" class="flex-1 bg-blue-950/50 hover:bg-blue-900/80 transition text-blue-400 py-3.5 rounded-xl text-xs font-bold border border-blue-800/50 shadow-md btn-premium-hover">DÃœZENLE</button>
                    <button id="ms-btn-delete" class="flex-1 bg-red-950/50 hover:bg-sky-900/80 transition text-sky-400 py-3.5 rounded-xl text-xs font-bold border border-sky-800/50 shadow-md btn-premium-hover">SÄ°L</button>
                </div>
            </div>
        </div>

        <div id="event-sheet" class="hidden fixed bottom-0 inset-x-0 glass-panel border-t border-zinc-700 rounded-t-3xl shadow-[0_-20px_50px_rgba(0,0,0,0.8)] p-5 z-[9999] overflow-y-auto max-h-[88vh] slide-up-anim">
            <div class="flex justify-between items-start mb-5 border-b border-zinc-700 pb-4">
                <div>
                    <h3 id="es-title" class="text-4xl text-white teko-font tracking-wide drop-shadow-md"></h3>
                    <p id="es-time" class="text-[11px] text-blue-400 font-bold mt-2 uppercase tracking-widest bg-blue-950/30 inline-block px-2 py-1 rounded border border-blue-900/50"></p>
                </div>
                <button onclick="document.getElementById('event-sheet').classList.add('hidden')" class="bg-black/50 hover:bg-zinc-700 transition w-10 h-10 rounded-full flex items-center justify-center text-zinc-300 hover:text-white border border-zinc-700 shadow-md hover:scale-110">âœ•</button>
            </div>
            
            <p id="es-desc" class="text-sm text-zinc-300 mb-6 bg-black/40 p-5 rounded-2xl border border-zinc-700 font-medium leading-relaxed shadow-inner"></p>
            
            <div class="mb-6 bg-zinc-900/30 p-4 rounded-2xl border border-zinc-800/50">
                <h4 class="text-[10px] font-bold text-zinc-400 mb-3 uppercase tracking-widest flex items-center gap-2"><span>ğŸ‘¥</span> KatÄ±lacaklar</h4>
                <div id="es-attendees" class="flex flex-wrap gap-2"></div>
            </div>
            
            <button id="btn-join" onclick="toggleJoinEvent()" class="w-full bg-zinc-800 hover:bg-zinc-700 transition text-white py-4 rounded-xl font-bold text-sm shadow-lg mb-3 btn-premium-hover"></button>
            <a id="btn-directions" href="#" target="_blank" class="w-full flex items-center justify-center gap-2 bg-black hover:bg-zinc-900 border border-zinc-700 transition text-white py-4 rounded-xl font-bold text-sm shadow-lg mb-3 uppercase tracking-widest btn-premium-hover"><span class="text-lg">ğŸ—ºï¸</span> YOL TARÄ°FÄ° AL</a>
            <button onclick="openComments('event', currentEventId)" class="w-full bg-zinc-900/80 border border-zinc-700 hover:bg-zinc-800 transition text-zinc-300 py-3 rounded-xl font-bold text-xs mb-2 btn-premium-hover flex items-center justify-center gap-2">
                <span>ğŸ’¬</span> Yorumlar
            </button>
            <button id="btn-del-event" onclick="deleteEvent()" class="hidden w-full bg-red-950/50 hover:bg-sky-900/80 transition text-sky-400 py-3.5 rounded-xl text-xs font-bold mt-2 border border-sky-800/50 shadow-md btn-premium-hover">ETKÄ°NLÄ°ÄÄ° SÄ°L</button>
        </div>

        <div id="nearby-routes-modal" class="hidden fixed inset-0 modal-backdrop flex items-center justify-center z-[9999] px-4 backdrop-blur-md">
            <div class="glass-panel w-full max-w-md rounded-3xl p-6 border border-zinc-700 relative max-h-[80dvh] flex flex-col shadow-[0_0_40px_rgba(0,0,0,0.6)] scale-in-anim">
                <button onclick="document.getElementById('nearby-routes-modal').classList.add('hidden')" class="absolute top-4 right-4 bg-black/50 backdrop-blur border border-zinc-700 hover:bg-zinc-700 transition w-8 h-8 rounded-full flex items-center justify-center text-zinc-300 hover:text-white z-10 hover:scale-110">âœ•</button>
                <h2 class="text-4xl text-white mb-5 teko-font tracking-wide border-b border-zinc-700 pb-3 drop-shadow-md">ğŸ“ YAKIN ROTALAR</h2>
                <div id="nr-list" class="flex-1 overflow-y-auto pr-2 space-y-3 custom-scrollbar"></div>
            </div>
        </div>

        <div id="kvkk-modal" class="hidden fixed inset-0 modal-backdrop flex items-center justify-center z-[9999] px-4 py-10 backdrop-blur-md">
            <div class="glass-panel w-full max-w-md rounded-3xl p-6 border border-sky-900/50 flex flex-col shadow-[0_0_40px_rgba(14,165,233,0.3)] scale-in-anim">
                <h2 class="text-3xl text-white mb-4 teko-font tracking-wide text-sky-400 drop-shadow-md flex items-center gap-2"><span class="animate-pulse">âš ï¸</span> KULLANICI SÃ–ZLEÅMESÄ°</h2>
                <div class="overflow-y-auto flex-1 text-xs text-zinc-300 space-y-5 mb-5 custom-scrollbar pr-3 bg-black/50 p-5 rounded-2xl border border-zinc-700 shadow-inner leading-relaxed">
                    <p><b class="text-white text-sm">1. GÃœVENLÄ°K VE SORUMLULUK REDDÄ° (WAIVER)</b><br>
                    Downhill ve Freeride daÄŸ bisikleti, doÄŸasÄ± gereÄŸi yÃ¼ksek Ã¶lÃ¼m ve aÄŸÄ±r yaralanma riski taÅŸÄ±yan ekstrem bir spordur. FreeriderTR platformunda (haritada) paylaÅŸÄ±lan rampalar, atlayÄ±ÅŸ noktalarÄ± ve rotalar tamamen kullanÄ±cÄ±lar tarafÄ±ndan eklenmektedir. 
                    <br><br>Bu noktalarda sÃ¼rÃ¼ÅŸ yaparken oluÅŸabilecek <b>hiÃ§bir kazadan, fiziksel yaralanmadan, ekipman hasarÄ±ndan veya Ã¶lÃ¼mden FreeriderTR yÃ¶netimi sorumlu tutulamaz.</b> SÃ¼rÃ¼ÅŸ esnasÄ±nda <i>Tam kapalÄ± kask (Full-face), boyunluk (Neck brace), gÃ¶ÄŸÃ¼s/sÄ±rt zÄ±rhÄ± ve dizlik</i> kullanmak tamamen sizin bireysel sorumluluÄŸunuzdadÄ±r.</p>
                    
                    <p><b class="text-white text-sm">2. KÄ°ÅÄ°SEL VERÄ°LER (KVKK)</b><br>
                    6698 sayÄ±lÄ± KiÅŸisel Verilerin KorunmasÄ± Kanunu kapsamÄ±nda; uygulamaya kayÄ±t olurken verdiÄŸiniz isim, ÅŸehir bilgileri, yÃ¼klediÄŸiniz fotoÄŸraflar, pazar ilanlarÄ±nÄ±z ve mesajlarÄ±nÄ±z sunucularÄ±mÄ±zda saklanmaktadÄ±r. <b>"Radar (SÃ¼rÃ¼ÅŸteyim)"</b> modunu aÃ§tÄ±ÄŸÄ±nÄ±zda anlÄ±k GPS konumunuz diÄŸer kullanÄ±cÄ±lara aÃ§Ä±k hale gelir. Verileriniz ticari amaÃ§la 3. ÅŸahÄ±slara satÄ±lmaz, sadece topluluk iÃ§i etkileÅŸim iÃ§in kullanÄ±lÄ±r.</p>
                    
                    <p><b class="text-white text-sm">3. TOPLULUK KURALLARI</b><br>
                    Uygulama iÃ§i sohbetlerde, pazar ilanlarÄ±nda ve profil sayfalarÄ±nda kÃ¼fÃ¼r, hakaret, yasa dÄ±ÅŸÄ± madde ticareti ve mÃ¼stehcen (+18) iÃ§erik paylaÅŸÄ±mÄ± kesinlikle yasaktÄ±r. Ä°hlal durumunda hesabÄ±nÄ±z kalÄ±cÄ± olarak (IP ve Cihaz banÄ± ile) sistemden uzaklaÅŸtÄ±rÄ±lÄ±r.</p>
                </div>
                <div class="shrink-0 mt-2">
                    <button onclick="closeKvkkModal()" class="w-full bg-sky-700 hover:bg-sky-600 transition text-white py-4 rounded-xl font-black text-sm shadow-[0_0_20px_rgba(2,132,199,0.5)] tracking-widest btn-premium-hover">OKUDUM VE ANLADIM</button>
                </div>
            </div>
        </div>

        <!-- ============================================================ -->
        <!-- GELÄ°ÅMÄ°Å YÃ–NETÄ°CÄ° PANELÄ° -->
        <!-- ============================================================ -->
        <div id="admin-panel" class="hidden fixed inset-0 z-[9999] flex items-center justify-center px-3" style="background:rgba(0,0,0,0.85);backdrop-filter:blur(20px)">
            <div class="w-full max-w-lg h-[92dvh] rounded-3xl flex flex-col overflow-hidden shadow-[0_0_60px_rgba(14,165,233,0.3)] border border-sky-900/40 scale-in-anim" style="background:linear-gradient(160deg,#0f0f12 0%,#130d0d 60%,#0a0a0f 100%)">

                <!-- Header -->
                <div class="shrink-0 px-5 pt-5 pb-4 border-b border-sky-900/30" style="background:linear-gradient(90deg,rgba(12,74,110,0.25),rgba(0,0,0,0))">
                    <div class="flex items-center justify-between">
                        <div class="flex items-center gap-3">
                            <div class="w-10 h-10 rounded-xl flex items-center justify-center text-xl shadow-[0_0_20px_rgba(14,165,233,0.6)]" style="background:linear-gradient(135deg,#0c4a6e,#0369a1)">ğŸ‘‘</div>
                            <div>
                                <h2 class="text-2xl text-white teko-font tracking-widest leading-none">YÃ–NETÄ°M MERKEZÄ°</h2>
                                <div id="admin-panel-role-tag" class="text-[10px] font-black uppercase tracking-widest text-sky-300 mt-0.5">Ana YÃ¶netici</div>
                            </div>
                        </div>
                        <button onclick="document.getElementById('admin-panel').classList.add('hidden')" class="w-9 h-9 rounded-xl flex items-center justify-center text-zinc-400 hover:text-white border border-zinc-700 hover:border-sky-600 transition-all hover:scale-105" style="background:rgba(0,0,0,0.5)">âœ•</button>
                    </div>

                    <!-- Tab Navigation -->
                    <div class="flex gap-1 mt-4 p-1 rounded-xl" style="background:rgba(0,0,0,0.4)">
                        <button onclick="adminSwitchTab('overview')" id="atab-overview" class="admin-tab-btn flex-1 py-2 rounded-lg text-[11px] font-black uppercase tracking-wider transition-all active-admin-tab">ğŸ“Š Genel</button>
                        <button onclick="adminSwitchTab('users')" id="atab-users" class="admin-tab-btn flex-1 py-2 rounded-lg text-[11px] font-black uppercase tracking-wider transition-all">ğŸ‘¥ KullanÄ±cÄ±</button>
                        <button onclick="adminSwitchTab('reels')" id="atab-reels" class="admin-tab-btn flex-1 py-2 rounded-lg text-[11px] font-black uppercase tracking-wider transition-all">ğŸ¬ Reels</button>
                        <button onclick="adminSwitchTab('commands')" id="atab-commands" class="admin-tab-btn flex-1 py-2 rounded-lg text-[11px] font-black uppercase tracking-wider transition-all">ğŸš€ Ä°ÅŸlemler</button>
                        <button onclick="adminSwitchTab('reports')" id="atab-reports" class="admin-tab-btn flex-1 py-2 rounded-lg text-[11px] font-black uppercase tracking-wider transition-all">ğŸ›¡ï¸ Raporlar</button>
                        <button onclick="adminSwitchTab('logs')" id="atab-logs" class="admin-tab-btn flex-1 py-2 rounded-lg text-[11px] font-black uppercase tracking-wider transition-all">ğŸ“‹ KayÄ±t</button>
                        <button onclick="adminSwitchTab('admins')" id="atab-admins" class="admin-tab-btn admin-main-only flex-1 py-2 rounded-lg text-[11px] font-black uppercase tracking-wider transition-all">ğŸ›¡ï¸ Ekip</button>
                    </div>
                </div>

                <!-- Content Area -->
                <div class="flex-1 overflow-y-auto custom-scrollbar p-4 space-y-4">

                    <!-- ===== GENEL TAB ===== -->
                    <div id="admin-tab-overview" class="space-y-4">
                        <!-- Stats Cards -->
                        <div class="grid grid-cols-3 gap-2">
                            <div class="rounded-2xl p-3 text-center border border-zinc-800/80" style="background:rgba(0,0,0,0.5)">
                                <div id="astat-users" class="text-2xl font-black text-white teko-font">â€”</div>
                                <div class="text-[9px] text-zinc-500 uppercase font-bold tracking-wider mt-1">KullanÄ±cÄ±</div>
                            </div>
                            <div class="rounded-2xl p-3 text-center border border-zinc-800/80" style="background:rgba(0,0,0,0.5)">
                                <div id="astat-banned" class="text-2xl font-black text-sky-300 teko-font">â€”</div>
                                <div class="text-[9px] text-zinc-500 uppercase font-bold tracking-wider mt-1">BanlÄ±</div>
                            </div>
                            <div class="rounded-2xl p-3 text-center border border-zinc-800/80" style="background:rgba(0,0,0,0.5)">
                                <div id="astat-admins" class="text-2xl font-black text-amber-400 teko-font">â€”</div>
                                <div class="text-[9px] text-zinc-500 uppercase font-bold tracking-wider mt-1">Yrd. Admin</div>
                            </div>
                        </div>

                        <!-- Google Play IAP DoÄŸrulamalarÄ± -->
                        <div class="rounded-2xl border border-zinc-800/80 overflow-hidden admin-main-only">
                            <div class="px-4 py-3 flex items-center gap-2 border-b border-zinc-800/50" style="background:rgba(0,0,0,0.4)">
                                <span class="animate-pulse text-sm">ğŸ“±</span>
                                <span class="text-white font-black text-xs uppercase tracking-widest">Google Play IAP â€” Bekleyen Onaylar</span>
                            </div>
                            <div id="admin-iap-requests" class="p-3 space-y-2 text-zinc-500 text-xs italic font-medium">YÃ¼kleniyor...</div>
                        </div>

                        <!-- Maintenance + News: Main Admin only -->
                        <div class="rounded-2xl border border-zinc-800/80 overflow-hidden admin-main-only">
                            <div class="px-4 py-3 flex items-center justify-between border-b border-zinc-800/50" style="background:rgba(0,0,0,0.4)">
                                <span class="text-white font-black text-xs uppercase tracking-widest">âš™ï¸ Sistem AyarlarÄ±</span>
                            </div>
                            <div class="p-4 space-y-3">
                                <div class="flex items-center justify-between">
                                    <span class="text-zinc-300 text-sm font-bold">ğŸ”§ BakÄ±m Modu</span>
                                    <input type="checkbox" id="admin-maintenance" onchange="toggleMaintenance()" class="w-6 h-6 accent-sky-500 cursor-pointer">
                                </div>
                                <button onclick="openNewsAdminModal()" class="w-full py-3 rounded-xl text-xs font-black uppercase tracking-widest border border-zinc-700 hover:border-white text-zinc-300 hover:text-white transition-all btn-premium-hover" style="background:rgba(0,0,0,0.4)">ğŸ“° Haber / Duyuru Ekle</button>
                            </div>
                        </div>

                        <!-- Sub-admin notify main -->
                        <div class="rounded-2xl border border-amber-900/40 overflow-hidden admin-sub-only" style="display:none">
                            <div class="px-4 py-3 border-b border-amber-900/30" style="background:rgba(120,53,15,0.15)">
                                <span class="text-amber-300 font-black text-xs uppercase tracking-widest">ğŸ“¢ Ana Admine Bildirim GÃ¶nder</span>
                            </div>
                            <div class="p-4">
                                <textarea id="admin-notify-msg" placeholder="Ana admine iletmek istediÄŸin mesajÄ± yaz..." class="w-full rounded-xl px-4 py-3 text-sm text-white border border-zinc-700 outline-none focus:border-amber-500 transition resize-none h-20 font-medium" style="background:rgba(0,0,0,0.5)"></textarea>
                                <button onclick="adminNotifyMain()" class="mt-2 w-full py-3 rounded-xl text-xs font-black uppercase tracking-widest border border-amber-700/60 text-amber-300 hover:bg-amber-900/30 transition-all btn-premium-hover">ğŸ“¨ GÃ¶nder</button>
                            </div>
                        </div>
                    </div>

                    <!-- ===== KULLANICI TAB ===== -->
                    <div id="admin-tab-users" class="hidden space-y-3">
                        <div class="relative">
                            <input id="admin-user-search" type="text" placeholder="KullanÄ±cÄ± ara..." oninput="adminSearchUsers()" class="w-full rounded-2xl px-5 py-3.5 text-sm text-white border border-zinc-700 outline-none focus:border-sky-500 transition font-medium" style="background:rgba(0,0,0,0.6)">
                            <span class="absolute right-4 top-1/2 -translate-y-1/2 text-zinc-500">ğŸ”</span>
                        </div>
                        <div id="admin-user-list" class="space-y-2">
                            <!-- Doldurulacak -->
                        </div>
                    </div>

                    <!-- ===== KOMUTLAR TAB ===== -->
                    <div id="admin-tab-commands" class="hidden space-y-4">
                        <div class="rounded-2xl border border-zinc-800/80 overflow-hidden" style="background:rgba(0,0,0,0.6)">
                            <div class="px-4 py-3 border-b border-zinc-800/50 flex justify-between items-center" style="background:rgba(0,0,0,0.4)">
                                <span class="text-white font-black text-xs uppercase tracking-widest">ğŸ” KullanÄ±cÄ± Sorgulama</span>
                            </div>
                            <div class="p-4 space-y-3">
                                <div class="relative">
                                    <input id="admin-action-username" type="text" placeholder="KullanÄ±cÄ± adÄ± girin..." onkeyup="if(event.key==='Enter') adminCheckUserDetails()" class="w-full rounded-xl pl-10 pr-4 py-3 text-sm text-white border border-zinc-700 outline-none focus:border-sky-500 transition font-medium" style="background:rgba(0,0,0,0.5)">
                                    <span class="absolute left-4 top-1/2 -translate-y-1/2 text-zinc-500">ğŸ‘¤</span>
                                </div>
                                <button onclick="adminCheckUserDetails()" class="w-full py-3 rounded-xl text-xs font-black uppercase tracking-widest bg-sky-900/30 border border-sky-800/50 text-sky-300 hover:bg-sky-800/50 transition-all shadow-md btn-premium-hover">KullanÄ±cÄ±yÄ± Bul</button>
                            </div>
                        </div>

                        <div id="admin-action-result" class="hidden space-y-4 slide-down-anim">
                            <!-- KullanÄ±cÄ± Detay KartÄ± -->
                            <div class="rounded-2xl border border-zinc-700 overflow-hidden" style="background:rgba(15,15,20,0.8)">
                                <div class="px-4 py-3 border-b border-zinc-800/50">
                                    <span class="text-zinc-400 font-black text-[10px] uppercase tracking-widest">ğŸ“‹ KullanÄ±cÄ± Bilgileri</span>
                                </div>
                                <div class="p-4 text-xs text-white space-y-2 font-medium">
                                    <div class="flex justify-between"><span class="text-zinc-500">KullanÄ±cÄ± AdÄ±:</span> <span id="aa-username" class="font-bold text-sky-400"></span></div>
                                    <div class="flex justify-between"><span class="text-zinc-500">E-posta:</span> <span id="aa-email"></span></div>
                                    <div class="flex justify-between"><span class="text-zinc-500">KayÄ±t Tarihi:</span> <span id="aa-date"></span></div>
                                    <div class="flex justify-between"><span class="text-zinc-500">Åehir / XP:</span> <span id="aa-cityxp"></span></div>
                                    <div class="flex justify-between"><span class="text-zinc-500">Mevcut Rol:</span> <span id="aa-role" class="font-bold"></span></div>
                                    <div class="flex justify-between"><span class="text-zinc-500">Durum:</span> <span id="aa-banned" class="font-bold"></span></div>
                                </div>
                            </div>

                            <!-- Premium Bilgileri KartÄ± -->
                            <div class="rounded-2xl border border-amber-900/40 overflow-hidden" style="background:rgba(120,53,15,0.1)">
                                <div class="px-4 py-3 border-b border-amber-900/30">
                                    <span class="text-amber-500 font-black text-[10px] uppercase tracking-widest">ğŸ‘‘ Ãœyelik Durumu</span>
                                </div>
                                <div class="p-4 text-xs text-white space-y-2 font-medium">
                                    <div class="flex justify-between"><span class="text-zinc-500">Paket:</span> <span id="aa-tier" class="font-bold text-yellow-400"></span></div>
                                    <div class="flex justify-between"><span class="text-zinc-500">BitiÅŸ Tarihi:</span> <span id="aa-expire"></span></div>
                                    <div class="flex justify-between"><span class="text-zinc-500">Edinme Yolu:</span> <span id="aa-source"></span></div>
                                </div>
                            </div>

                            <!-- Aksiyon ButonlarÄ± -->
                            <div class="space-y-2">
                                <div class="text-[10px] text-zinc-500 font-bold uppercase tracking-widest px-1">ğŸ’ Premium Ver / Uzat</div>
                                <div class="grid grid-cols-3 gap-2">
                                    <button onclick="adminActionExec('standart gÃ¶nder')" class="py-3 bg-blue-900/30 border border-blue-800/50 text-blue-300 text-[10px] font-black rounded-xl hover:bg-blue-800/50 transition">Std Ver</button>
                                    <button onclick="adminActionExec('deluxe gÃ¶nder')" class="py-3 bg-purple-900/30 border border-purple-800/50 text-purple-300 text-[10px] font-black rounded-xl hover:bg-purple-800/50 transition">Dlx Ver</button>
                                    <button onclick="adminActionExec('ultra gÃ¶nder')" class="py-3 bg-yellow-900/30 border border-yellow-800/50 text-yellow-300 text-[10px] font-black rounded-xl hover:bg-yellow-800/50 transition">Ult+ Ver</button>
                                </div>
                                <div class="grid grid-cols-3 gap-2 mt-2">
                                    <button onclick="adminActionExec('standart geri Ã§ek')" class="py-3 bg-zinc-800/50 border border-zinc-700 text-zinc-400 text-[10px] font-black rounded-xl hover:bg-zinc-700 transition">Std DÃ¼ÅŸÃ¼r</button>
                                    <button onclick="adminActionExec('deluxe geri Ã§ek')" class="py-3 bg-zinc-800/50 border border-zinc-700 text-zinc-400 text-[10px] font-black rounded-xl hover:bg-zinc-700 transition">Dlx DÃ¼ÅŸÃ¼r</button>
                                    <button onclick="adminActionExec('ultra geri Ã§ek')" class="py-3 bg-red-900/30 border border-red-800/50 text-red-300 text-[10px] font-black rounded-xl hover:bg-red-800/50 transition">ÃœyeliÄŸi Sil</button>
                                </div>
                            </div>

                            <!-- DiÄŸer Ä°ÅŸlemler -->
                            <div class="space-y-2 mt-4 mb-8">
                                <div class="text-[10px] text-zinc-500 font-bold uppercase tracking-widest px-1">âš ï¸ Hesap Ä°ÅŸlemleri</div>
                                <div class="grid grid-cols-2 gap-2">
                                    <button onclick="adminResetPassword(document.getElementById('aa-username').textContent)" class="py-3 bg-zinc-800 border border-zinc-700 text-zinc-300 text-[10px] font-black rounded-xl hover:bg-zinc-700 transition">ğŸ”‘ Åifre SÄ±fÄ±rla</button>
                                    <button onclick="adminChangeUsername(document.getElementById('aa-username').textContent); adminCheckUserDetails();" class="py-3 bg-zinc-800 border border-zinc-700 text-zinc-300 text-[10px] font-black rounded-xl hover:bg-zinc-700 transition">âœï¸ Ä°sim DeÄŸiÅŸ</button>
                                    <button id="aa-btn-ban" onclick="adminActionBanToggle()" class="py-3 bg-orange-950/40 border border-orange-900/50 text-orange-400 text-[10px] font-black rounded-xl hover:bg-orange-900/40 transition">ğŸš« Banla</button>
                                    <button onclick="adminDeleteUser(document.getElementById('aa-username').textContent)" class="py-3 bg-red-950/50 border border-red-900/50 text-red-400 text-[10px] font-black rounded-xl hover:bg-red-900/50 transition">ğŸ—‘ï¸ HesabÄ± Sil</button>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- ===== RAPORLAR TAB ===== -->
                    <div id="admin-tab-reports" class="hidden space-y-3">
                        <div class="flex items-center justify-between">
                            <span class="text-zinc-400 text-xs font-bold uppercase tracking-widest">ğŸ›¡ï¸ Bekleyen Raporlar</span>
                            <button onclick="loadAdminReports()" class="text-[10px] text-sky-300 font-bold border border-sky-900/40 px-3 py-1.5 rounded-lg hover:bg-sky-900/20 transition">ğŸ”„ Yenile</button>
                        </div>
                        <div class="flex gap-2 mb-2">
                            <select id="admin-report-status" onchange="loadAdminReports()" class="bg-black/60 border border-zinc-700 rounded-lg px-2 py-2 text-white text-[10px] font-bold outline-none">
                                <option value="pending">â³ Bekleyen</option>
                                <option value="all">ğŸ“‹ TÃ¼mÃ¼</option>
                                <option value="reviewed">âœ… Ä°ncelendi</option>
                                <option value="dismissed">âŒ Reddedildi</option>
                            </select>
                            <select id="admin-report-severity" onchange="loadAdminReports()" class="bg-black/60 border border-zinc-700 rounded-lg px-2 py-2 text-white text-[10px] font-bold outline-none">
                                <option value="all">TÃ¼m Åiddetler</option>
                                <option value="high">ğŸ”´ YÃ¼ksek</option>
                                <option value="medium">ğŸŸ  Orta</option>
                                <option value="low">ğŸŸ¡ DÃ¼ÅŸÃ¼k</option>
                            </select>
                        </div>
                        <div id="admin-reports-list" class="space-y-2">
                            <div class="text-zinc-600 text-xs italic font-medium text-center py-4">YÃ¼kleniyor...</div>
                        </div>
                        <div id="admin-reports-pagination" class="flex justify-center gap-2 mt-2"></div>
                    </div>

                    <!-- ===== REELS TAB ===== -->
                    <div id="admin-tab-reels" class="hidden space-y-3">
                        <div class="flex items-center justify-between">
                            <span class="text-zinc-400 text-xs font-bold uppercase tracking-widest">Son 50 Reel</span>
                            <button onclick="loadAdminReels()" class="text-[10px] text-sky-300 font-bold border border-sky-900/40 px-3 py-1.5 rounded-lg hover:bg-sky-900/20 transition">ğŸ”„ Yenile</button>
                        </div>
                        <div id="admin-reels-list" class="space-y-2">
                            <div class="text-zinc-600 text-xs italic font-medium text-center py-4">YÃ¼kleniyor...</div>
                        </div>
                    </div>

                    <!-- ===== LOGLAR TAB ===== -->
                    <div id="admin-tab-logs" class="hidden space-y-3">
                        <div class="flex items-center justify-between">
                            <span class="text-zinc-400 text-xs font-bold uppercase tracking-widest">Admin Eylem KayÄ±tlarÄ±</span>
                            <button onclick="loadAdminLogs()" class="text-[10px] text-blue-400 font-bold border border-blue-900/40 px-3 py-1.5 rounded-lg hover:bg-blue-900/20 transition">ğŸ”„ Yenile</button>
                        </div>
                        <div id="admin-logs-list" class="space-y-2">
                            <div class="text-zinc-600 text-xs italic font-medium text-center py-4">YÃ¼kleniyor...</div>
                        </div>
                    </div>

                    <!-- ===== EKIP (ADMÄ°NLER) TAB ===== -->
                    <div id="admin-tab-admins" class="hidden space-y-4 admin-main-only">
                        <div class="rounded-2xl border border-zinc-800/80 overflow-hidden">
                            <div class="px-4 py-3 border-b border-zinc-800/50" style="background:rgba(0,0,0,0.4)">
                                <span class="text-white font-black text-xs uppercase tracking-widest">â• YardÄ±mcÄ± Admin Ata</span>
                            </div>
                            <div class="p-4 space-y-3">
                                <input id="assign-admin-username" type="text" placeholder="KullanÄ±cÄ± adÄ± gir..." class="w-full rounded-xl px-4 py-3 text-sm text-white border border-zinc-700 outline-none focus:border-amber-500 transition font-medium" style="background:rgba(0,0,0,0.5)">
                                <button onclick="assignSubAdmin()" class="w-full py-3 rounded-xl text-xs font-black uppercase tracking-widest border border-amber-700/60 text-amber-300 hover:bg-amber-900/30 transition-all btn-premium-hover">ğŸ‘‘ YardÄ±mcÄ± Admin Yap</button>
                            </div>
                        </div>

                        <div class="rounded-2xl border border-zinc-800/80 overflow-hidden">
                            <div class="px-4 py-3 flex items-center justify-between border-b border-zinc-800/50" style="background:rgba(0,0,0,0.4)">
                                <span class="text-white font-black text-xs uppercase tracking-widest">ğŸ›¡ï¸ Mevcut YardÄ±mcÄ± Adminler</span>
                                <button onclick="loadSubAdmins()" class="text-[10px] text-zinc-400 font-bold hover:text-white transition">ğŸ”„</button>
                            </div>
                            <div id="sub-admin-list" class="p-3 space-y-2">
                                <div class="text-zinc-600 text-xs italic font-medium text-center py-3">YÃ¼kleniyor...</div>
                            </div>
                        </div>

                        <div class="rounded-2xl border border-sky-900/30 overflow-hidden">
                            <div class="px-4 py-3 border-b border-sky-900/25" style="background:rgba(12,74,110,0.1)">
                                <span class="text-sky-300 font-black text-xs uppercase tracking-widest">ğŸš« Yetki Al</span>
                            </div>
                            <div class="p-4 space-y-3">
                                <input id="revoke-admin-username" type="text" placeholder="Admin kullanÄ±cÄ± adÄ±..." class="w-full rounded-xl px-4 py-3 text-sm text-white border border-zinc-700 outline-none focus:border-sky-500 transition font-medium" style="background:rgba(0,0,0,0.5)">
                                <button onclick="revokeSubAdmin()" class="w-full py-3 rounded-xl text-xs font-black uppercase tracking-widest border border-sky-800/60 text-sky-300 hover:bg-sky-900/20 transition-all btn-premium-hover">âŒ AdminliÄŸi Geri Al</button>
                            </div>
                        </div>
                    </div>

                </div>
            </div>
        </div>

        <!-- KullanÄ±cÄ± Aktivite ModalÄ± -->
        <div id="user-activity-modal" class="hidden fixed inset-0 z-[99999] flex items-center justify-center px-3" style="background:rgba(0,0,0,0.9);backdrop-filter:blur(16px)">
            <div class="w-full max-w-md h-[88dvh] rounded-3xl flex flex-col overflow-hidden border border-zinc-700 shadow-2xl scale-in-anim" style="background:#0c0c10">
                <div class="shrink-0 px-5 py-4 border-b border-zinc-800 flex items-center justify-between">
                    <div>
                        <h3 class="text-xl text-white teko-font tracking-wide">ğŸ” KullanÄ±cÄ± Aktivitesi</h3>
                        <div id="ua-username-label" class="text-xs text-zinc-500 font-bold mt-0.5"></div>
                    </div>
                    <button onclick="document.getElementById('user-activity-modal').classList.add('hidden')" class="w-9 h-9 rounded-xl bg-zinc-900 border border-zinc-700 text-zinc-400 hover:text-white flex items-center justify-center transition">âœ•</button>
                </div>
                <div class="flex gap-1 p-3 border-b border-zinc-800" style="background:rgba(0,0,0,0.3)">
                    <button onclick="uaTab('messages')" id="uatab-messages" class="ua-tab-btn flex-1 py-2 rounded-lg text-[10px] font-black uppercase tracking-wider transition-all ua-active-tab">ğŸ’¬ Mesajlar</button>
                    <button onclick="uaTab('dms')" id="uatab-dms" class="ua-tab-btn flex-1 py-2 rounded-lg text-[10px] font-black uppercase tracking-wider transition-all">ğŸ“© DM</button>
                    <button onclick="uaTab('reels')" id="uatab-reels" class="ua-tab-btn flex-1 py-2 rounded-lg text-[10px] font-black uppercase tracking-wider transition-all">ğŸ¬ Reels</button>
                    <button onclick="uaTab('markers')" id="uatab-markers" class="ua-tab-btn flex-1 py-2 rounded-lg text-[10px] font-black uppercase tracking-wider transition-all">ğŸ“ Yerler</button>
                    <button onclick="uaTab('manage')" id="uatab-manage" class="ua-tab-btn flex-1 py-2 rounded-lg text-[10px] font-black uppercase tracking-wider transition-all admin-main-only text-sky-400">âš™ï¸ YÃ¶net</button>
                </div>
                <div class="flex-1 overflow-y-auto custom-scrollbar p-3 space-y-2" id="ua-content">
                    <div class="text-zinc-600 text-xs italic text-center py-6">YÃ¼kleniyor...</div>
                </div>
                <div class="shrink-0 p-3 border-t border-zinc-800 grid grid-cols-2 gap-2">
                    <button id="ua-ban-btn" onclick="adminBanFromActivity()" class="py-3 rounded-xl text-xs font-black uppercase tracking-widest border border-sky-800/60 text-sky-300 hover:bg-sky-900/20 transition">ğŸš¨ Banla</button>
                    <button onclick="document.getElementById('user-activity-modal').classList.add('hidden')" class="py-3 rounded-xl text-xs font-black uppercase tracking-widest border border-zinc-700 text-zinc-400 hover:bg-zinc-800 transition">Kapat</button>
                </div>
            </div>
        </div>
        
        <div id="news-admin-modal" class="hidden fixed inset-0 modal-backdrop flex items-center justify-center z-[9999] px-4 backdrop-blur-md">
            <div class="glass-panel w-full max-w-md rounded-3xl p-6 border border-zinc-700 shadow-2xl scale-in-anim">
                <h2 class="text-4xl text-white mb-6 teko-font tracking-wide drop-shadow-md">ğŸ“° YENÄ° HABER</h2>
                <input id="news-title" type="text" placeholder="Haber BaÅŸlÄ±ÄŸÄ±" class="w-full bg-black/60 p-4 rounded-xl mb-4 text-white font-bold border border-zinc-700 outline-none focus:border-white transition shadow-inner">
                <textarea id="news-content" placeholder="Haber Ä°Ã§eriÄŸi..." class="w-full bg-black/60 p-4 rounded-xl h-28 mb-4 text-white font-medium border border-zinc-700 outline-none focus:border-white transition custom-scrollbar shadow-inner"></textarea>
                
                <label class="block text-[10px] text-zinc-400 mb-2 uppercase font-bold tracking-widest">Haber GÃ¶rseli (Ä°steÄŸe BaÄŸlÄ±)</label>
                <input id="news-photo" type="file" accept="image/*" class="w-full bg-black/60 border border-zinc-700 rounded-xl px-3 py-3 mb-6 text-xs text-zinc-300 focus:border-white transition cursor-pointer shadow-inner">
                
                <div class="flex gap-3">
                    <button onclick="document.getElementById('news-admin-modal').classList.add('hidden')" class="flex-1 bg-zinc-800 hover:bg-zinc-700 transition py-4 rounded-xl text-white font-bold shadow-md btn-premium-hover">Ä°ptal</button>
                    <button onclick="saveNews()" class="flex-1 bg-white hover:bg-gray-200 transition py-4 rounded-xl text-black font-bold shadow-[0_0_15px_rgba(255,255,255,0.3)] btn-premium-hover">YAYINLA</button>
                </div>
            </div>
        </div>

        <!-- spin sesleri missions screen'de inline -->

    <script>
        // Global DeÄŸiÅŸkenler
        // window.currentUser olarak tanÄ±mla â€” OneSignal init callback'i eriÅŸebilsin
        window.currentUser = null;
        let currentUser = null; 
        let map; 
        let markerCluster = null;
        let selectedMarkerCategory = "Rampa";
        let activeMarkerFilter = "TÃ¼mÃ¼";
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
        let _prevTab = 0; // Reels'ten Ã¶nce hangi tab'daydÄ±k

        // â”€â”€ Toast Bildirim Sistemi (GeliÅŸtirilmiÅŸ) â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
        // showToast(message, type?, duration?)  â†’  ekranÄ±n altÄ±nda kÄ±sa sÃ¼reli bildirim
        // type: 'success' | 'error' | 'warning' | 'info'
        let _toastTimer = null;
        function showToast(message, typeOrDuration = 'info', duration = 3000) {
            // Geriye dÃ¶nÃ¼k uyumluluk: eski Ã§aÄŸrÄ±lar showToast(msg, 3000) ÅŸeklinde
            let type = 'info';
            if (typeof typeOrDuration === 'number') {
                duration = typeOrDuration;
            } else if (typeof typeOrDuration === 'string') {
                type = typeOrDuration;
            }

            const icons = { success: 'âœ…', error: 'âŒ', warning: 'âš ï¸', info: 'â„¹ï¸' };
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
            toast.innerHTML = `<span style="margin-right:8px;font-size:16px">${icons[type] || 'â„¹ï¸'}</span><span>${message}</span>`;
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
        let _voiceStopping = false; // Ses gÃ¶nderim aÅŸamasÄ±nda tekrar tÄ±klamayÄ± engeller
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
                alert(`âš ï¸ Dosya Ã§ok bÃ¼yÃ¼k (${fileSizeMB.toFixed(2)} MB). LÃ¼tfen sistemi yormamak iÃ§in ${maxMB}MB'dan kÃ¼Ã§Ã¼k bir gÃ¶rsel seÃ§in.`);
                return false;
            }
            return true;
        }
        
        // =====================================================
        // ÅANS Ã‡ARKI - SABÄ°T Ã–DÃœL LÄ°STESÄ° (backend ile eÅŸleÅŸir)
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
        // GÄ°RÄ°Å VE KAYIT Ä°ÅLEMLERÄ°
        // =========================================================
        async function handleLogin() {
            const u = document.getElementById("login-username").value.trim();
            const p = document.getElementById("login-password").value;
            const rem = document.getElementById("remember-me").checked;
            
            if(!u || !p) return alert("KullanÄ±cÄ± adÄ± ve ÅŸifre zorunludur!");
            
            try {
                const res = await sendAction('login', { username: u, password: p });
                if(res.status === 'ok') {
                    currentUser = res.user;
                    window.currentUser = currentUser; // OneSignal callback iÃ§in global'e de yaz
                    localStorage.setItem("fr_user", JSON.stringify(currentUser));
                    
                    if(rem) {
                        localStorage.setItem("fr_remembered_username", u);
                        localStorage.setItem("fr_remembered_password", btoa(unescape(encodeURIComponent(p))));
                    } else {
                        localStorage.removeItem("fr_remembered_username");
                        localStorage.removeItem("fr_remembered_password");
                    }
                    
                    if(res.user.just_got_daily) {
                        alert("ğŸ‰ Harika! GÃ¼nlÃ¼k giriÅŸ Ã¶dÃ¼lÃ¼ olarak +" + res.user.just_got_daily + " XP kazandÄ±n.");
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
            
            if(!name || !username || !city || !password) return alert("LÃ¼tfen Ad Soyad, KullanÄ±cÄ± AdÄ±, Åehir ve Åifre alanlarÄ±nÄ± doldurun!");
            
            // Gmail zorunlu deÄŸil, ama girilmiÅŸse geÃ§erli olmalÄ±
            if(email && !email.toLowerCase().endsWith('@gmail.com')) return alert("GirdiÄŸiniz e-posta @gmail.com uzantÄ±lÄ± deÄŸil. LÃ¼tfen Gmail adresinizi girin ya da alanÄ± boÅŸ bÄ±rakÄ±n.");
            
            // Referans kodu varsa Gmail zorunlu
            if(refCode && !email) return alert("Referans kodu kullanabilmek iÃ§in @gmail.com adresinizi girmeniz zorunludur! (Spam korumasÄ±)");
            if(refCode && !email.toLowerCase().endsWith('@gmail.com')) return alert("Referans kodu kullanabilmek iÃ§in @gmail.com uzantÄ±lÄ± e-posta girmeniz zorunludur! (Spam korumasÄ±)");
            
            if(password.length < 4) return alert("Åifre en az 4 karakter olmalÄ±dÄ±r!");
            if(!kvkk) return alert("KayÄ±t olmak iÃ§in KullanÄ±cÄ± SÃ¶zleÅŸmesi ve KVKK metnini onaylamanÄ±z gerekmektedir!");
            if(!privacy) return alert("KayÄ±t olmak iÃ§in Gizlilik SÃ¶zleÅŸmesi ve KullanÄ±m ÅartlarÄ±'nÄ± onaylamanÄ±z gerekmektedir!");
            
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
                    alert("KayÄ±t baÅŸarÄ±lÄ±! AramÄ±za hoÅŸ geldin. Åimdi giriÅŸ yapabilirsin.");
                    showLoginTab();
                    document.getElementById("login-username").value = username;
                } else if (res.status === 'needs_verification') {
                    verificationUsername = res.username;
                    document.getElementById("verify-code-input").value = "";
                    document.getElementById("email-verify-modal").classList.remove("hidden");
                    alert("KayÄ±t baÅŸarÄ±lÄ±! E-posta adresinize bir doÄŸrulama kodu gÃ¶nderdik.");
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
            {min:0,     max: 99,    name: "Acemi",        color: "text-zinc-500",  icon: "ğŸŒ±", next: 100},
            {min:100,   max: 499,   name: "Ã‡aylak",       color: "text-zinc-400",  icon: "ğŸš²", next: 500},
            {min:500,   max: 999,   name: "SÃ¼rÃ¼cÃ¼",       color: "text-sky-400",   icon: "ğŸ”ï¸", next: 1000},
            {min:1000,  max: 1999,  name: "Deneyimli",    color: "text-blue-400",  icon: "âš¡", next: 2000},
            {min:2000,  max: 3999,  name: "Rampa SavaÅŸÃ§Ä±sÄ±", color: "text-indigo-400",icon: "ğŸ›¡ï¸", next: 4000},
            {min:4000,  max: 6999,  name: "Usta",         color: "text-orange-400",icon: "ğŸ”¥", next: 7000},
            {min:7000,  max: 9999,  name: "Elite",        color: "text-rose-400",  icon: "ğŸ’¥", next: 10000},
            {min:10000, max: 19999, name: "Åampiyon",     color: "text-yellow-400",icon: "ğŸ†", next: 20000},
            {min:20000, max: 49999, name: "Efsane",       color: "text-sky-400",   icon: "ğŸ‘‘", next: 50000},
            {min:50000, max: 999999,name: "Downhill Efsanesi", color: "text-prem-rainbow", icon: "ğŸŒŸ", next: null}
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

        // === KALICI GÃ–REVLER (bir kere tamamlanÄ±r) ===
        const MISSIONS = [
            { id: "m1",  title: "Ä°lk AdÄ±m",      desc: "Uygulamaya ilk kez giriÅŸ yap.",          target: 1,   type: "login_streak",   xp: 50,   icon: "ğŸ‘‹", badge: null },
            { id: "m2",  title: "BaÄŸÄ±mlÄ±",        desc: "7 gÃ¼n Ã¼st Ã¼ste giriÅŸ yap.",              target: 7,   type: "login_streak",   xp: 200,  icon: "ğŸ”¥", badge: "Seri GiriÅŸÃ§i" },
            { id: "m3",  title: "SadÄ±k Ãœye",      desc: "30 gÃ¼n Ã¼st Ã¼ste giriÅŸ yap.",             target: 30,  type: "login_streak",   xp: 2000, icon: "ğŸ’", badge: "Demir Ãœye" },
            { id: "m4",  title: "Ã‡Ä±lgÄ±n",         desc: "100 gÃ¼n Ã¼st Ã¼ste giriÅŸ yap.",            target: 100, type: "login_streak",   xp: 10000,icon: "âš¡", badge: "100 GÃ¼n UstasÄ±" },
            { id: "m5",  title: "Sohbete KatÄ±l",  desc: "Gruba 1 mesaj gÃ¶nder.",                  target: 1,   type: "total_messages", xp: 20,   icon: "ğŸ’¬", badge: null },
            { id: "m6",  title: "Geveze",         desc: "Gruba 50 mesaj gÃ¶nder.",                 target: 50,  type: "total_messages", xp: 300,  icon: "ğŸ—£ï¸", badge: "Sohbet Tutkunu" },
            { id: "m7",  title: "Chat Efsanesi",  desc: "Gruba 200 mesaj gÃ¶nder.",                target: 200, type: "total_messages", xp: 1000, icon: "ğŸ‘‘", badge: "Chat Efsanesi" },
            { id: "m8",  title: "KÃ¢ÅŸif",          desc: "Haritaya 1 rampa ekle.",                 target: 1,   type: "markers",        xp: 50,   icon: "ğŸ“", badge: "Harita KÃ¢ÅŸifi" },
            { id: "m9",  title: "HaritacÄ±",       desc: "Haritaya 10 rampa ekle.",                target: 10,  type: "markers",        xp: 500,  icon: "ğŸ—ºï¸", badge: "HaritacÄ±" },
            { id: "m10", title: "Ä°lk SatÄ±ÅŸ",      desc: "Pazara 1 ilan ekle.",                    target: 1,   type: "market",         xp: 50,   icon: "ğŸ›’", badge: "Esnaf" },
            { id: "m11", title: "Pazar UstasÄ±",   desc: "Pazara 5 ilan ekle.",                    target: 5,   type: "market",         xp: 300,  icon: "ğŸ’°", badge: "Pazar UstasÄ±" },
            { id: "m12", title: "OrganizatÃ¶r",    desc: "1 sÃ¼rÃ¼ÅŸ buluÅŸmasÄ± oluÅŸtur.",             target: 1,   type: "events",         xp: 100,  icon: "ğŸ¤", badge: "OrganizatÃ¶r" },
            { id: "m13", title: "Topluluk Lideri",desc: "5 sÃ¼rÃ¼ÅŸ buluÅŸmasÄ± oluÅŸtur.",             target: 5,   type: "events",         xp: 500,  icon: "ğŸ†", badge: "Topluluk Lideri" },
        ];

        // === GÃœNLÃœK GÃ–REVLER (her gÃ¼n sÄ±fÄ±rlanÄ±r) ===
        function getDailyMissions() {
            // GÃ¼ne gÃ¶re deterministik gÃ¶rev seti (aynÄ± gÃ¼n herkes aynÄ± gÃ¶revi gÃ¶rÃ¼r)
            const dayNum = Math.floor(Date.now() / 86400000);
            const todayKey = new Date().toISOString().split('T')[0];
            const sets = [
                [{ id: "d1", title: "GÃ¼nlÃ¼k GiriÅŸ",    desc: "BugÃ¼n giriÅŸ yap.",           target: 1,  type: "daily_login",   xp: 30,  icon: "â˜€ï¸" },
                 { id: "d2", title: "Sohbet Et",        desc: "BugÃ¼n 3 mesaj gÃ¶nder.",       target: 3,  type: "daily_msg",     xp: 50,  icon: "ğŸ’¬" },
                 { id: "d3", title: "HaritayÄ± KeÅŸfet",  desc: "Haritada 1 nokta ekle.",      target: 1,  type: "daily_marker",  xp: 80,  icon: "ğŸ“" }],
                [{ id: "d1", title: "GÃ¼nlÃ¼k GiriÅŸ",    desc: "BugÃ¼n giriÅŸ yap.",           target: 1,  type: "daily_login",   xp: 30,  icon: "â˜€ï¸" },
                 { id: "d4", title: "AI Sor",           desc: "AI'a 1 soru sor.",            target: 1,  type: "daily_ai",      xp: 40,  icon: "ğŸ¤–" },
                 { id: "d5", title: "Pazar Gez",        desc: "Bir ilana bak.",              target: 1,  type: "daily_market",  xp: 20,  icon: "ğŸ›’" }],
                [{ id: "d1", title: "GÃ¼nlÃ¼k GiriÅŸ",    desc: "BugÃ¼n giriÅŸ yap.",           target: 1,  type: "daily_login",   xp: 30,  icon: "â˜€ï¸" },
                 { id: "d6", title: "Aktif Ol",         desc: "BugÃ¼n 5 mesaj gÃ¶nder.",       target: 5,  type: "daily_msg",     xp: 70,  icon: "ğŸ”¥" },
                 { id: "d7", title: "SÃ¼rÃ¼ÅŸe Ã‡Ä±k",       desc: "Radar modunu aÃ§.",            target: 1,  type: "daily_radar",   xp: 60,  icon: "ğŸ“¡" }],
            ];
            const todaySet = sets[dayNum % sets.length];
            return { missions: todaySet, key: todayKey };
        }

        // === HAFTALIK GÃ–REVLER (her Pazartesi sÄ±fÄ±rlanÄ±r) ===
        function getWeeklyMissions() {
            const weekNum = Math.floor(Date.now() / (86400000 * 7));
            const now = new Date();
            const monday = new Date(now);
            monday.setDate(now.getDate() - ((now.getDay() + 6) % 7));
            const weekKey = monday.toISOString().split('T')[0];
            const sets = [
                [{ id: "w1", title: "HaftalÄ±k KonuÅŸmacÄ±", desc: "Bu hafta 20 mesaj gÃ¶nder.",  target: 20, type: "weekly_msg",    xp: 200, icon: "ğŸ’¬" },
                 { id: "w2", title: "Harita Gezgini",     desc: "Bu hafta 2 rampa ekle.",      target: 2,  type: "weekly_marker", xp: 150, icon: "ğŸ—ºï¸" }],
                [{ id: "w3", title: "Topluluk Ãœyesi",     desc: "Bu hafta 1 etkinlik oluÅŸtur.",target: 1,  type: "weekly_event",  xp: 250, icon: "ğŸ“…" },
                 { id: "w4", title: "Aktif TÃ¼ccar",       desc: "Bu hafta 1 ilan ver.",        target: 1,  type: "weekly_market", xp: 150, icon: "ğŸ›’" }],
                [{ id: "w5", title: "SÃ¼rÃ¼ÅŸ UstasÄ±",       desc: "Bu hafta 3 kez radar aÃ§.",    target: 3,  type: "weekly_radar",  xp: 200, icon: "ğŸš´" },
                 { id: "w6", title: "Soru Sorular",        desc: "Bu hafta 5 AI sorusu sor.",   target: 5,  type: "weekly_ai",     xp: 180, icon: "ğŸ¤–" }],
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
        // Ã‡EVRÄ°M Ä°Ã‡Ä° DURUM YARDIMCI FONKSÄ°YONLARI
        // ==============================================================
        function getOnlineStatus(user) {
            if (!user || !user.stats) return { status: 'offline', label: '' };
            const ts = user.stats.last_seen_ts;
            if (!ts) return { status: 'offline', label: '' };
            const nowSec = Math.floor(Date.now() / 1000);
            const diff = nowSec - ts;
            if (diff < 300) return { status: 'online', label: 'Åu an aktif' };
            if (diff < 3600) {
                const mins = Math.floor(diff / 60);
                return { status: 'recent', label: `${mins} dk Ã¶nce aktifti` };
            }
            if (diff < 86400) {
                const hrs = Math.floor(diff / 3600);
                return { status: 'today', label: `${hrs} saat Ã¶nce` };
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
        // GERÃ‡EK ALEV & BUZ PARTÄ°KÃœL SÄ°STEMÄ° (Ultra+)
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

        // Profil avatarÄ±na parÃ§acÄ±k ekle/kaldÄ±r
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

        // Leaderboard/Chat avatarlarÄ±na da mini parÃ§acÄ±k ekle
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
        // Heartbeat â€” her dakikada sunucuya "burdayÄ±m" gÃ¶nder + lokal gÃ¼ncelle
        async function sendHeartbeat() {
            if (!currentUser) return;
            const nowSec = Math.floor(Date.now() / 1000);
            // Lokal gÃ¼ncelle - anÄ±nda yansÄ±sÄ±n
            if (currentUser.stats) currentUser.stats.last_seen_ts = nowSec;
            const me = db.users.find(u => u.username === currentUser.username);
            if (me && me.stats) me.stats.last_seen_ts = nowSec;
            // Sunucuya da gÃ¶nder; Ã¼yelik sÃ¼resi dolmuÅŸsa UI'Ä± gÃ¼ncelle
            try {
                const hbRes = await fetch('/api/heartbeat', { method: 'POST' });
                if (hbRes.ok) {
                    const hbData = await hbRes.json();
                    if (hbData.premium_revoked) {
                        // Ãœyelik sona erdi â€“ lokal state sÄ±fÄ±rla
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
                        showToast('âš ï¸ ÃœyeliÄŸin sona erdi. Devam etmek iÃ§in yenile!');
                    }
                }
            } catch(e) {}
        }

        // ==============================================================
        // ONESIGNAL PUSH BÄ°LDÄ°RÄ°M
        // ==============================================================
        async function requestPushPermission() {
            try {
                // Ä°zin zaten verilmiÅŸse tekrar sormadan login yap
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
                                console.log('âœ… OneSignal login (izin sonrasÄ±):', currentUser.username);
                                // Ä°zin verildi â†’ subscription ID'yi hemen kaydet
                                await saveOneSignalPlayerId(OneSignal);
                            } catch(e) { console.error('OneSignal login hatasÄ±:', e); }
                        });
                    }
                }
                updateNotifBtnState();
            } catch(e) { console.error('OneSignal izin hatasÄ±:', e); }
        }

        // OneSignal subscription ID'sini backend'e kaydeder
        async function saveOneSignalPlayerId(OneSignal) {
            try {
                // Kisa bir bekleme â€” subscription aktif olana kadar
                await new Promise(r => setTimeout(r, 800));
                const subId = OneSignal.User.PushSubscription.id;
                if (!subId) {
                    console.warn('âš ï¸ OneSignal subscription ID henÃ¼z hazÄ±r deÄŸil');
                    return;
                }
                const resp = await fetch('/api/save_push_id', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ player_id: subId })
                });
                const result = await resp.json();
                if (result.status === 'ok') {
                    console.log('âœ… OneSignal player_id kaydedildi:', subId.slice(0,20) + '...');
                } else {
                    console.warn('âš ï¸ player_id kaydedilemedi:', result);
                }
            } catch(e) {
                console.error('âŒ saveOneSignalPlayerId hatasÄ±:', e);
            }
        }

        async function setOneSignalUser() {
            if(!currentUser) return;
            // OneSignalDeferred kuyruÄŸunu kullan â€” SDK henÃ¼z init olmasa bile gÃ¼venli Ã§alÄ±ÅŸÄ±r
            window.OneSignalDeferred = window.OneSignalDeferred || [];
            window.OneSignalDeferred.push(async function(OneSignal) {
                try {
                    await OneSignal.login(currentUser.username);
                    console.log('âœ… OneSignal kullanÄ±cÄ± tanÄ±mlandÄ±:', currentUser.username);
                    const permission = OneSignal.Notifications.permission;
                    console.log('ğŸ”” OneSignal izin durumu:', permission);
                    // Ä°zin varsa subscription ID'yi hemen kaydet
                    if (permission) {
                        await saveOneSignalPlayerId(OneSignal);
                    }
                } catch(e) {
                    console.error('âŒ OneSignal login hatasÄ±:', e);
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
            alert("Yeni renginiz uygulandÄ±!");
        }

        async function changeEffect(effectId) {
            await sendAction('update_premium_color', { color: currentUser.stats.premium_color || 'std-blue', effect: effectId });
            if(currentUser && currentUser.stats) {
                currentUser.stats.avatar_effect = effectId;
            }
            updateProfileUI();
            alert("Profil efektiniz uygulandÄ±!");
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
            toast.innerHTML = (isUp ? 'ğŸ“ˆ' : 'ğŸ“‰') +
                `<div><div class="text-[10px] uppercase tracking-widest opacity-80">${isUp ? 'SÄ±ralama YÃ¼kseldi!' : 'SÄ±ralama DÃ¼ÅŸtÃ¼!'}</div>` +
                `<div>${oldRank}. sira -> ${newRank}. sÄ±ra</div></div>`;
            document.body.appendChild(toast);
            haptic(isUp ? [30,20,30,20,50] : [100,50,100]);
            setTimeout(() => { toast.style.opacity='0'; toast.style.transition='opacity 0.4s'; setTimeout(()=>toast.remove(),400); }, 3000);
        }

        // Mobil titreÅŸim geri bildirimi
        function haptic(pattern = [10]) {
            if('vibrate' in navigator) { try { navigator.vibrate(pattern); } catch(e) {} }
        }

        // ==============================================================
        // BÄ°LDÄ°RÄ°M Ä°ZÄ°N YÃ–NETÄ°MÄ° (PROFÄ°L BUTONU)
        // ==============================================================
        async function handleNotifPermission() {
            if (!('Notification' in window)) {
                alert("Bu tarayÄ±cÄ± bildirimleri desteklemiyor.");
                return;
            }
            if (Notification.permission === 'denied') {
                alert("Bildirim izni engellendi. LÃ¼tfen tarayÄ±cÄ± ayarlarÄ±ndan FreeriderTR iÃ§in bildirimlere izin verin.");
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
                if (icon) icon.textContent = 'âœ…';
                if (txt) txt.textContent = 'Bildirimler AÃ§Ä±k';
            } else if (Notification.permission === 'denied') {
                btn.className = 'w-full bg-red-950/40 border border-sky-800/50 text-sky-300 py-4 rounded-xl font-bold text-sm mt-4 flex items-center justify-center gap-2 transition-all cursor-not-allowed';
                if (icon) icon.textContent = 'ğŸ”•';
                if (txt) txt.textContent = 'Bildirimler Engellendi';
            } else {
                btn.className = 'w-full bg-zinc-900 border border-zinc-700 hover:bg-zinc-800 transition text-zinc-300 py-4 rounded-xl font-bold text-sm mt-4 btn-premium-hover flex items-center justify-center gap-2';
                if (icon) icon.textContent = 'ğŸ””';
                if (txt) txt.textContent = 'Bildirimleri AÃ§';
            }
        }

        // DUZELTME #3: sendAction â€” silent parametre eklendi.
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
                
                // Mevcut mesajlarÄ± koru (realtime + cache)
                const existingMessages = db.messages || [];
                const existingDms = db.dms || [];
                
                db = newData;
                
                // TÃ¼m array alanlarÄ±nÄ± garantile
                if(!db.stories)  db.stories  = [];
                if(!db.messages) db.messages = [];
                if(!db.dms)      db.dms      = [];
                if(!db.users)    db.users    = [];
                if(!db.markers)  db.markers  = [];
                if(!db.market)   db.market   = [];
                if(!db.events)   db.events   = [];
                if(!db.news)     db.news     = [];
                if(!db.banned)   db.banned   = [];
                
                // Sunucu boÅŸ veya az dÃ¶nerse mevcut mesajlarÄ± koru
                existingMessages.forEach(m => {
                    if(!db.messages.find(x => x.id === m.id)) db.messages.push(m);
                });
                existingDms.forEach(m => {
                    if(!db.dms.find(x => x.id === m.id)) db.dms.push(m);
                });
                
                // MesajlarÄ± ID'ye gÃ¶re sÄ±rala
                db.messages.sort((a,b) => (parseInt(a.id)||0) - (parseInt(b.id)||0));
                
                // LocalStorage'a yedekle
                try {
                    localStorage.setItem('fr_msg_cache', JSON.stringify(db.messages.slice(-50)));
                } catch(e) {}
                
                if (currentUser) {
                    const me = db.users.find(u => u.username === currentUser.username);
                    if (me) { 
                        const oldRank = _myLastRank;
                        // Admin korumasÄ±: role Ã¼zerine yazÄ±lmasÄ±nÄ± Ã¶nle
                        const wasAdmin = (currentUser.role === 'Admin' || currentUser.username === 'Admin' || currentUser.username.toLowerCase() === 'admin');
                        currentUser = me;
                        if (wasAdmin) {
                            currentUser.role = 'Admin';
                        }
                        localStorage.setItem("fr_user", JSON.stringify(currentUser)); 
                        updateProfileUI(); 
                        checkMissions();
                        checkLeaderboardPosition(oldRank); 
                        
                        // Referans sekmesi aÃ§Ä±ksa hemen gÃ¼ncelle
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

                // KullanÄ±cÄ± sayacÄ± gÃ¼ncellemesi
                updateUserCountDisplays();
                
                if(!silent) syncMap();
                return true;
            } catch(e) { 
                console.error("Veri Ã§ekme hatasÄ±:", e);
                return false; 
            }
        }

        function updateUserCountDisplays() {
            const total = db.total_users || 300;
            const active = db.active_users || 0;
            // Login ekranÄ±
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
                        0: {icon: "â˜€ï¸", desc: "AÃ§Ä±k"}, 1: {icon: "ğŸŒ¤ï¸", desc: "Az Bulutlu"},
                        2: {icon: "â›…", desc: "ParÃ§alÄ±"}, 3: {icon: "â˜ï¸", desc: "Bulutlu"},
                        45: {icon: "ğŸŒ«ï¸", desc: "Sisli"}, 61: {icon: "ğŸŒ§ï¸", desc: "YaÄŸmurlu"},
                        63: {icon: "ğŸŒ§ï¸", desc: "YoÄŸun YaÄŸmur"}, 71: {icon: "â„ï¸", desc: "KarlÄ±"},
                        80: {icon: "ğŸŒ¦ï¸", desc: "SaÄŸanak"}, 95: {icon: "â›ˆï¸", desc: "FÄ±rtÄ±na"}
                    };
                    const status = weatherMap[code] || {icon: "ğŸŒ¡ï¸", desc: "Bilinmiyor"};
                    // Update sidebar weather
                    const sidebarW = document.getElementById("sidebar-weather");
                    if(sidebarW) {
                        sidebarW.classList.remove("hidden");
                        document.getElementById("sidebar-weather-icon").textContent = status.icon;
                        document.getElementById("sidebar-weather-temp").textContent = temp + "Â°C";
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
            } catch (e) { console.log("Hava durumu hatasÄ±:", e); }
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
            
            // Åifreyi decode et (base64) â€” eski dÃ¼z metin kayÄ±tlarÄ± da Ã§alÄ±ÅŸsÄ±n
            let savedPassword = null;
            if (savedPasswordEncoded) {
                try {
                    savedPassword = decodeURIComponent(escape(atob(savedPasswordEncoded)));
                } catch(e) {
                    // Eski dÃ¼z metin kaydÄ± ise direkt kullan (geÃ§iÅŸ dÃ¶nemi)
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
                        window.currentUser = currentUser; // OneSignal callback iÃ§in global'e de yaz
                        localStorage.setItem("fr_user", JSON.stringify(currentUser));
                        // Åifreyi gÃ¼ncel encode edilmiÅŸ haliyle tekrar kaydet
                        localStorage.setItem("fr_remembered_password", btoa(unescape(encodeURIComponent(savedPassword))));
                        if(res.user.just_got_daily) {
                            alert("ğŸ‰ Harika! GÃ¼nlÃ¼k giriÅŸ Ã¶dÃ¼lÃ¼ olarak +" + res.user.just_got_daily + " XP kazandÄ±n.");
                        }
                        loginSuccess();
                    } else {
                        // Åifre deÄŸiÅŸmiÅŸ veya hatalÄ± â€” kayÄ±tlÄ± bilgileri temizle
                        localStorage.removeItem("fr_remembered_username");
                        localStorage.removeItem("fr_remembered_password");
                        document.getElementById("login-username").value = "";
                        document.getElementById("login-password").value = "";
                        document.getElementById("remember-me").checked = false;
                    }
                } catch(e) {
                    // Hata durumunda da temizle
                    localStorage.removeItem("fr_remembered_username");
                    localStorage.removeItem("fr_remembered_password");
                    document.getElementById("login-username").value = "";
                    document.getElementById("login-password").value = "";
                    document.getElementById("remember-me").checked = false;
                }
            }

            // ============================================================
            // AKILLI REALTIME SÄ°STEMÄ°
            // Tek kanal = tek baÄŸlantÄ± = 200 limit yerine 1 slot kullanÄ±r
            // Sayfa arka plana geÃ§ince baÄŸlantÄ± kesilir, Ã¶ne gelince tekrar aÃ§Ä±lÄ±r
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
                        if (payload.new.user && !db.users.find(u => u.username === payload.new.user) && !['Freerider AI', 'ModeratÃ¶r AI', 'SÄ°STEM AI', 'Admin'].includes(payload.new.user)) {
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
                            // Eksik alanlarÄ± eski veriden koru (REPLICA IDENTITY olmadan tam gelmiyor olabilir)
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
                            // DM badge gÃ¶ster (chat aÃ§Ä±k deÄŸilse)
                            const chatVisible = !document.getElementById('screen-chat').classList.contains('hidden');
                            if (!chatVisible && payload.new.sender !== currentUser.username) showChatBadge();
                        }
                    } else if (payload.eventType === 'DELETE') {
                        db.dms = db.dms.filter(m => m.id !== payload.old.id);
                    }
                    renderDmList();
                    if (currentDmUser) renderDmThread(currentDmUser);
                })
                // ---- HARÄ°TA NOKTALARI ----
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
                // ---- ETKÄ°NLÄ°KLER ----
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
                        // Kendi verimizi tam gÃ¼ncelle, baÅŸkalarÄ±nÄ±n garage'ini alma
                        if (updated.username === currentUser.username) {
                            db.users[idx] = updated;
                            currentUser = updated;
                            localStorage.setItem("fr_user", JSON.stringify(currentUser));
                            updateProfileUI();
                            checkMissions();
                        } else {
                            // BaÅŸkasÄ± iÃ§in sadece temel alanlar
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
                    // Lider tablosu aÃ§Ä±ksa gÃ¼ncelle
                    if (!document.getElementById('screen-rank').classList.contains('hidden')) renderLeaderboard();
                })
                // ---- YASAKLI KULLANICILAR ----
                .on('postgres_changes', { event: '*', schema: 'public', table: 'banned' }, payload => {
                    if(!currentUser) return;
                    if (payload.eventType === 'INSERT') {
                        if (!db.banned.includes(payload.new.username)) db.banned.push(payload.new.username);
                        // Kendi hesabÄ±m banlandÄ±ysa Ã§Ä±kÄ±ÅŸ yap
                        if (payload.new.username === currentUser.username) {
                            alert("HesabÄ±nÄ±z banlanmÄ±ÅŸtÄ±r!");
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
                // ---- AYARLAR (pinned mesaj, bakÄ±m modu) ----
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
                            alert("Sistem bakÄ±m moduna alÄ±ndÄ±. LÃ¼tfen daha sonra tekrar deneyin.");
                            logout();
                        }
                    }
                })
                .subscribe((status) => {
                    if (status === 'SUBSCRIBED') {
                        console.log('âœ… Realtime baÄŸlantÄ±sÄ± kuruldu');
                        _realtimePaused = false;
                    } else if (status === 'CHANNEL_ERROR' || status === 'TIMED_OUT') {
                        console.log('âš ï¸ Realtime baÄŸlantÄ±sÄ± kesildi, 5sn sonra tekrar denenecek...');
                        setTimeout(() => { if(!_realtimePaused) startRealtime(); }, 5000);
                    }
                });
            }

            // Sayfa gÃ¶rÃ¼nÃ¼rlÃ¼ÄŸÃ¼ deÄŸiÅŸince baÄŸlantÄ±yÄ± yÃ¶net (200 limit korumasÄ±)
            document.addEventListener('visibilitychange', () => {
                if (document.hidden) {
                    // Sayfa arka plana geÃ§ti - baÄŸlantÄ±yÄ± kapat, slot serbest bÄ±rak
                    _realtimePaused = true;
                    if (_realtimeChannel) {
                        try { supaClient.removeChannel(_realtimeChannel); _realtimeChannel = null; } catch(e) {}
                    }
                } else {
                    // Sayfa Ã¶ne geldi - yeniden baÄŸlan ve son veriyi Ã§ek
                    _realtimePaused = false;
                    startRealtime();
                    loadData(true); // Arka planda kaÃ§Ä±rÄ±lan gÃ¼ncellemeleri al
                }
            });

            // Ä°lk baÄŸlantÄ±yÄ± kur
            startRealtime();

            // â”€â”€ Ã‡evrimdÄ±ÅŸÄ± / Ã‡evrimiÃ§i Bildirimi â”€â”€
            function showOfflineBanner() {
                let b = document.getElementById('offline-banner');
                if (!b) {
                    b = document.createElement('div');
                    b.id = 'offline-banner';
                    b.style.cssText = 'position:fixed;top:0;left:0;right:0;z-index:999999;background:#0284c7;color:#fff;text-align:center;padding:8px 16px;font-size:12px;font-weight:900;letter-spacing:0.05em;text-transform:uppercase;';
                    b.textContent = 'ğŸ“µ Ä°nternet baÄŸlantÄ±sÄ± yok â€” Ã–nbellek modunda Ã§alÄ±ÅŸÄ±yor';
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

        // YANDAN AÃ‡ILIR MENÃœ (SIDEBAR) FONKSÄ°YONU
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
            document.getElementById('modal-marker-title').textContent = "ğŸ“ " + cat.toUpperCase() + " EKLE";
            document.getElementById('modal-marker-category-label').textContent = "SeÃ§ilen TÃ¼r: " + cat;
            
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
        // HARÄ°TA FONKSÄ°YONU
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

            // Yol haritasÄ± â€” CartoDB Dark (temiz, koyu tema, MTB uyumlu)
            var roads = L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
                subdomains: 'abcd',
                maxZoom: 22,
                maxNativeZoom: 19,
                attribution: 'Â© <a href="https://carto.com">CARTO</a> Â© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
            });

            // Uydu gÃ¶rÃ¼ntÃ¼sÃ¼ â€” ESRI World Imagery + etiketler Ã¼st katman
            var satelliteBase = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
                maxZoom: 22,
                maxNativeZoom: 19,
                attribution: 'Â© <a href="https://www.esri.com">Esri</a>, Maxar'
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
                "ğŸ›°ï¸ Uydu + Etiketler": satellite,
                "ğŸŒ‘ Koyu Harita": roads
            };

            L.control.layers(baseMaps, null, { 
                collapsed: false, 
                position: 'topright' 
            }).addTo(map);

            // Zoom butonlarÄ± â€” saÄŸ alt, parmak dostu
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
                    // Marker yerleÅŸtirildi, modal aÃ§
                    document.getElementById('add-marker-modal').classList.remove('hidden');
                } else if (isAddingEventMode) { 
                    toggleAddEventMode(); 
                    openAddEventModal(); 
                } 
            });
        }

        // =========================================================
        // E-POSTA DOÄRULAMA FONKSÄ°YONLARI
        // =========================================================
        function skipVerification() {
            document.getElementById("email-verify-modal").classList.add("hidden");
            if(!currentUser) {
                alert("KayÄ±t tamamlandÄ±, ancak e-postanÄ±z henÃ¼z doÄŸrulanmadÄ±. Daha sonra 'Profil' menÃ¼sÃ¼nden doÄŸrulayabilirsiniz.");
                showLoginTab();
                document.getElementById("login-username").value = verificationUsername;
            }
        }

        async function submitVerificationCode() {
            const code = document.getElementById("verify-code-input").value;
            if(!code || code.length !== 6) return alert("LÃ¼tfen geÃ§erli bir 6 haneli kod girin.");
            
            try {
                await sendAction('verify_email', { username: verificationUsername || currentUser?.username, code: code });
                alert("E-posta adresiniz baÅŸarÄ±yla doÄŸrulandÄ±!");
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

            // GÃ¼nlÃ¼k sÄ±fÄ±rlama
            if(stats.daily_missions.date !== todayKey) {
                stats.daily_missions = { date: todayKey, daily_login: 1 };
            }
            // HaftalÄ±k sÄ±fÄ±rlama
            if(stats.weekly_missions.week !== weekKey) {
                stats.weekly_missions = { week: weekKey };
            }

            // Sunucuya claim isteÄŸi gÃ¶nderen yardÄ±mcÄ±
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

            // --- KalÄ±cÄ± gÃ¶revler ---
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

            // --- GÃ¼nlÃ¼k gÃ¶revler ---
            for(let m of dailyData.missions) {
                const doneKey = 'done_' + m.id;
                if(!stats.daily_missions[doneKey]) {
                    let progress = m.type === 'daily_login' ? 1 : (stats.daily_missions[m.type] || 0);
                    if(progress >= m.target) {
                        const result = await claimOnServer('daily', m.id, m.xp);
                        if(result === 'claimed') {
                            stats.daily_missions[doneKey] = true;
                            showMissionToast(m.title + ' (GÃ¼nlÃ¼k)', m.xp, m.icon);
                        } else if(result === 'already_done') {
                            stats.daily_missions[doneKey] = true; // sessiz senkronize
                        }
                    }
                }
            }

            // --- HaftalÄ±k gÃ¶revler ---
            for(let m of weeklyData.missions) {
                const doneKey = 'done_' + m.id;
                if(!stats.weekly_missions[doneKey]) {
                    let progress = stats.weekly_missions[m.type] || 0;
                    if(progress >= m.target) {
                        const result = await claimOnServer('weekly', m.id, m.xp);
                        if(result === 'claimed') {
                            stats.weekly_missions[doneKey] = true;
                            showMissionToast(m.title + ' (HaftalÄ±k)', m.xp, m.icon);
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
        // STORY SÄ°STEMÄ°
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
        // YORUM SÄ°STEMÄ°
        // ============================================================
        let _commentTargetType = '';
        let _commentTargetId = '';

        async function openComments(targetType, targetId) {
            if(!targetId) return;
            _commentTargetType = targetType;
            _commentTargetId = targetId;
            const label = targetType === 'marker' ? 'Rampa YorumlarÄ±' : 'Etkinlik YorumlarÄ±';
            document.getElementById('comment-modal-title').innerHTML = 'ğŸ’¬ ' + label;
            document.getElementById('comment-list').innerHTML = '<div class="text-zinc-500 text-xs text-center py-4 animate-pulse">Yorumlar yÃ¼kleniyor...</div>';
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
        // SEVÄ°YE ATLAMA KUTLAMA ANÄ°MASYONU
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
        // HAVA DURUMU ROTA Ã–NERÄ°SÄ°
        // ============================================================
        function getWeatherRouteAdvice(weatherCode) {
            const good = [0, 1, 2];
            const ok   = [3, 45];
            const bad  = [61, 63, 71, 80, 81, 82, 95, 96, 99];
            if(good.includes(weatherCode)) return { emoji:'âœ…', text:'Harika hava! Suru icin ideal.', color:'text-green-400', ride: true };
            if(ok.includes(weatherCode))   return { emoji:'âš ï¸', text:'Bulutlu ama suru yapilabilir.', color:'text-yellow-400', ride: true };
            if(bad.includes(weatherCode))  return { emoji:'âŒ', text:'Yagmur/kar var! Suru tavsiye edilmez.', color:'text-sky-300', ride: false };
            return { emoji:'ğŸŒ¡ï¸', text:'Hava durumu bilinmiyor.', color:'text-zinc-400', ride: false };
        }

        // Hava durumu widget'Ä±na rota Ã¶nerisi ekle
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
                    <div class="text-[10px] font-black uppercase tracking-widest mb-1 ${textColor}">${advice.ride ? 'BUGÃœN SÃœRÃœLEBÄ°LÄ°R' : 'BUGÃœN SÃœRÃœÅ Ã–NERÄ°LMEZ'}</div>
                    <div class="text-white font-black text-2xl teko-font">${temp}Â°C Â· ${advice.emoji}</div>
                    <div class="${textColor} text-xs font-bold mt-1">${advice.text}</div>`;
            }
        }

        // ============================================================
        // TEMA & ARAYÃœZ RENGÄ° (Premium)
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
                badge.textContent = 'ğŸ”´ Oncelikli Destek - 24 saat icinde cevaplanir';
                badge.className = 'mb-4 text-center py-2 rounded-xl text-xs font-black uppercase tracking-widest bg-red-900/40 text-sky-300 border border-sky-800/50';
            } else if(premTier === 1) {
                badge.textContent = 'ğŸŸ¡ Normal Destek - 48-72 saat icinde cevaplanir';
                badge.className = 'mb-4 text-center py-2 rounded-xl text-xs font-black uppercase tracking-widest bg-yellow-900/40 text-yellow-400 border border-yellow-800/50';
            } else {
                badge.textContent = 'âšª Ucretsiz Destek - YoÄŸunluÄŸa gore cevaplanir';
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
                s.textContent = i < rating ? 'â­' : 'â˜†';
                s.style.opacity = i < rating ? '1' : '0.4';
            });
            try {
                const m = db.markers.find(x=>x.id===currentMarkerId);
                await sendAction('rate_marker', {
                    marker_id: currentMarkerId,
                    marker_name: m ? m.name : '',
                    rating
                });
                showMissionToast('Puan Verildi!', 0, 'â­');
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
                s.textContent = i < myRating ? 'â­' : 'â˜†';
                s.style.opacity = i < myRating ? '1' : '0.4';
            });
        }

        // ============================================================
        // TEHLÄ°KE BÄ°LDÄ°RÄ°MÄ°
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
            showMissionToast('Tehlike Bildirildi', 0, 'âš ï¸');
        }

        // ============================================================
        // TAM EKRAN FOTOÄRAF GÃ–RÃœNTÃœLEYÄ°CÄ°
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
        // EMOJI REAKSÄ°YONLARI
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
                <span class="text-lg">ğŸ</span>
                <span class="flex-1">3 Gun Ucretsiz Ultra+ Denemen Aktif! Bitis: ${expDate}</span>
                <button onclick="this.parentElement.parentElement.remove()" class="text-black/60 hover:text-black text-sm">âœ•</button>
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
        // DAVET ET KAZAN (REFERANS) SEKMESÄ° Ä°ÅLEMLERÄ°
        // ==============================================================
        function renderReferralTab() {
            if(!currentUser) return;
            const stats = currentUser.stats || {};
            // GerÃ§ek ref kodu stats'tan, yoksa fallback
            const refCode = stats.ref_code || currentUser.username;
            document.getElementById("my-ref-code").value = refCode;
            const refCount = stats.ref_count || 0;
            const claimable = stats.claimable_refs || 0;
            
            const maxRef = 10;
            const refPercent = Math.min((refCount / maxRef) * 100, 100);
            
            document.getElementById("ref-monthly-limit").innerText = `BU AYKÄ° KULLANIM: ${refCount} / ${maxRef}`;
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
            alert("Referans kodunuz baÅŸarÄ±yla kopyalandÄ±! ArkadaÅŸlarÄ±nÄ±za gÃ¶nderebilirsiniz.");
        }

        async function claimRefReward() {
            const reward = document.getElementById("ref-reward-select").value;
            try {
                const res = await sendAction('claim_ref_reward', { reward_choice: reward });
                if(res.status === 'ok') {
                    alert("Tebrikler! Ã–dÃ¼l baÅŸarÄ±yla hesabÄ±nÄ±za tanÄ±mlandÄ±. Bol pedallÄ± gÃ¼nler!");
                    loadData(true); 
                }
            } catch(e) {}
        }

        // ================================================================
        // REELS SÄ°STEMÄ° JS
        // ================================================================

        // â”€â”€ Aktif IntersectionObserver listesi (eski kod uyumu â€” artÄ±k kullanÄ±lmÄ±yor) â”€â”€
        const _reelObservers = [];

        // â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
        // stopAllMedia() â€” TÃ¼m video/ses medyayÄ± durdurur, merkezi
        // feed observer'Ä± baÄŸlantÄ±sÄ±nÄ± keser.
        // Sayfa geÃ§iÅŸlerinde ve modal kapanÄ±ÅŸlarÄ±nda Ã§aÄŸrÄ±lÄ±r.
        // â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
        function stopAllMedia() {
            document.querySelectorAll('video, audio').forEach(el => {
                try { el.pause(); } catch(_) {}
            });
            if(typeof _feedObserver !== 'undefined' && _feedObserver) {
                _feedObserver.disconnect();
                _feedObserver = null;
            }
        }

        // â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
        // openReels(videoId) â€” Reels sayfasÄ±nÄ± aÃ§ar ve belirtilen ID'li
        // videoya scroll ederek otomatik oynatÄ±r.
        // Profilden Reels'e Ä±ÅŸÄ±nlanmak iÃ§in kullanÄ±lÄ±r.
        // â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
        window.openReels = async function(videoId) {
            stopAllMedia();
            // TÃ¼m aÃ§Ä±k modalleri kapat
            ['other-profile-modal','reel-comment-modal','reel-upload-modal'].forEach(id => {
                const m = document.getElementById(id);
                if(m) m.classList.add('hidden');
            });
            // Reels ekranÄ±nÄ± aÃ§
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
            if(soundBtn) { soundBtn.style.display = 'flex'; soundBtn.textContent = _reelMuted ? 'ğŸ”‡' : 'ğŸ”Š'; }
            const gridBtn = document.getElementById('grid-view-btn');
            if(gridBtn) gridBtn.style.display = 'flex';
            const uploadTopBtn = document.getElementById('reels-upload-top-btn');
            if(uploadTopBtn) uploadTopBtn.style.display = 'flex';

            // Her zaman yeniden yÃ¼kle (feed gÃ¼ncel olsun, observer temiz baÅŸlasÄ±n)
            await loadReels();

            // loadReels render tamamlandÄ±ktan sonra scroll + oynat
            if(videoId && reelsData.length) {
                const idx = reelsData.findIndex(r => String(r.id) === String(videoId));
                const feed = document.getElementById('reels-feed');
                if(feed && idx >= 0) {
                    // 2 frame bekle: render + observer kurulumu tamamlansÄ±n
                    requestAnimationFrame(() => requestAnimationFrame(() => {
                        const cards = feed.querySelectorAll(':scope > div');
                        const targetCard = cards[idx];
                        if(!targetCard) return;
                        // observer'Ä± geÃ§ici durdur, scroll sÄ±rasÄ±nda yanlÄ±ÅŸ video Ã§almasÄ±n
                        if(_feedObserver) _feedObserver.disconnect();
                        // TÃ¼m videolar durdurulmuÅŸ, scroll et
                        targetCard.scrollIntoView({ behavior: 'instant', block: 'start' });
                        // Scroll sonrasÄ± hedef videoyu oynat ve observer'Ä± yeniden kur
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

        let _reelMuted = false; // VarsayÄ±lan: ses aÃ§Ä±k

        // Reels'i kapat, Ã¶nceki sekmeye dÃ¶n
        function closeReels() {
            stopAllMedia(); // Hayalet ses Ã¶nleme â€” tÃ¼m medyayÄ± durdur
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
            // Alt nav butonlarÄ±nÄ± gÃ¼ncelle
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
            // Ã–nceki sekmeye geÃ§ (reels deÄŸilse)
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
            if(btn) btn.textContent = _reelMuted ? 'ğŸ”‡' : 'ğŸ”Š';
            document.querySelectorAll('#reels-feed video').forEach(v => { v.muted = _reelMuted; });
        }

        // â”€â”€ TEK merkezi IntersectionObserver â€” tÃ¼m feed kartlarÄ± iÃ§in â”€â”€
        // Kart baÅŸÄ±na deÄŸil, feed render bittikten sonra tek seferde kurulur.
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
                        // DiÄŸer tÃ¼m feed videolarÄ±nÄ± durdur â†’ sadece gÃ¶rÃ¼nÃ¼r kart Ã§alar
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
            // Observer ve medyayÄ± temizle
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
            } catch(e) { console.error('Reel yÃ¼kleme hatasÄ±:', e); }

            if(loadingEl) loadingEl.style.display = 'none';

            const soundBtn = document.getElementById('reel-sound-btn');
            if(soundBtn) { soundBtn.style.display = 'flex'; soundBtn.textContent = _reelMuted ? 'ğŸ”‡' : 'ğŸ”Š'; }

            if(!reelsData.length) {
                if(emptyEl) emptyEl.classList.remove('hidden');
                return;
            }

            // Feed'i temizle ve yeniden render et
            while(feed.firstChild) feed.removeChild(feed.firstChild);
            reelsData.forEach((reel) => {
                try { renderReelCard(reel, feed); }
                catch(e) { console.error('Reel render hatasÄ±:', reel?.id, e); }
            });

            // Tek merkezi observer'Ä± kur (render bittikten sonra)
            requestAnimationFrame(() => _setupFeedObserver());
        }

        function renderReelCard(reel, container) {
            if(!reel) return;
            const user = db.users.find(u => u.username === reel.user) || { username: reel.user, avatar: '' };
            const avatar = user.avatar || 'https://cdn.freeridertr.com.tr/profil%20resmi/unnamed.jpg';
            const isLiked = currentUser && (reel.likes || []).includes(currentUser.username);
            const likeCount = (reel.likes || []).length;
            const isOwner = currentUser && (currentUser.username === reel.user || currentUser.role === 'Admin' || currentUser.role === 'SubAdmin');

            // Story halkasÄ±: db.stories iÃ§inde aktif story var mÄ±?
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
                <!-- Sol alt: kullanÄ±cÄ± + aÃ§Ä±klama -->
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
                <!-- SaÄŸ: aksiyonlar -->
                <div class="absolute right-3 bottom-8 z-10 flex flex-col items-center gap-5">
                    <button onclick="toggleReelLike('${reel.id}', this)" class="flex flex-col items-center gap-1">
                        <div class="w-10 h-10 rounded-full bg-black/50 backdrop-blur flex items-center justify-center text-xl border border-white/20 ${isLiked ? 'text-sky-400' : 'text-white'}">${isLiked ? 'â¤ï¸' : 'ğŸ¤'}</div>
                        <span class="text-white text-xs font-bold drop-shadow-md reel-like-count">${likeCount}</span>
                    </button>
                    <button onclick="openReelComments('${reel.id}')" class="flex flex-col items-center gap-1">
                        <div class="w-10 h-10 rounded-full bg-black/50 backdrop-blur flex items-center justify-center text-xl border border-white/20 text-white">ğŸ’¬</div>
                        <span class="text-white text-xs font-bold drop-shadow-md">${reel.comment_count || 0}</span>
                    </button>
                    ${isOwner ? `<button onclick="deleteReel('${reel.id}')" class="flex flex-col items-center gap-1">
                        <div class="w-10 h-10 rounded-full bg-red-900/60 backdrop-blur flex items-center justify-center text-xl border border-sky-400/30 text-white">ğŸ—‘ï¸</div>
                    </button>` : ''}
                </div>
            `;
            container.appendChild(card);

            // â”€â”€ Video tap-to-pause: click â†’ SVG flash ikonu â”€â”€
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
                            // DiÄŸer tÃ¼m feed videolarÄ±nÄ± Ã¶nce durdur
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
            // NOT: IntersectionObserver artÄ±k kart baÅŸÄ±na DEÄÄ°L,
            // loadReels() sonunda _setupFeedObserver() ile tek seferde kurulur.
        }

        async function toggleReelLike(reelId, btn) {
            if(!currentUser) { alert('BeÄŸenmek iÃ§in giriÅŸ yapÄ±n!'); return; }
            try {
                const res = await sendAction('like_reel', { reel_id: reelId });
                if(res && res.status === 'ok') {
                    const icon = btn.querySelector('div');
                    const count = btn.querySelector('.reel-like-count');
                    if(icon) { icon.textContent = res.liked ? 'â¤ï¸' : 'ğŸ¤'; icon.className = icon.className.replace(/text-(red|white)-\d+/, res.liked ? 'text-sky-400' : 'text-white'); }
                    if(count) count.textContent = res.likes;
                }
            } catch(e) {}
        }

        async function deleteReel(reelId) {
            if(!confirm("Bu Reels'i silmek istediÄŸinize emin misiniz?")) return;
            await sendAction('delete_reel', { reel_id: reelId });
            loadReels();
        }

        async function openReelComments(reelId) {
            currentReelId = reelId;
            const modal = document.getElementById('reel-comment-modal');
            const list = document.getElementById('reel-comments-list');
            modal.classList.remove('hidden');
            list.innerHTML = '<div class="text-zinc-500 text-sm text-center py-4">Yorumlar yÃ¼kleniyor...</div>';
            try {
                const res = await sendAction('get_comments', { target_id: reelId });
                const comments = res.comments || [];
                if(!comments.length) {
                    list.innerHTML = '<div class="text-zinc-500 text-sm text-center py-4">HenÃ¼z yorum yok. Ä°lk yorumu sen yap!</div>';
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
            } catch(e) { list.innerHTML = '<div class="text-zinc-500 text-sm text-center py-4">Yorumlar yÃ¼klenemedi.</div>'; }
        }

        async function submitReelComment() {
            if(!currentUser) { alert('Yorum yapmak iÃ§in giriÅŸ yapÄ±n!'); return; }
            const inp = document.getElementById('reel-comment-input');
            const text = inp.value.trim();
            if(!text) return;
            inp.value = '';
            await sendAction('comment_reel', { reel_id: currentReelId, text });
            openReelComments(currentReelId);
        }

        function openReelUploadModal() {
            if(!currentUser) { alert('Reel paylaÅŸmak iÃ§in giriÅŸ yapÄ±n!'); return; }
            const modal = document.getElementById('reel-upload-modal');
            const infoEl = document.getElementById('reel-limit-info');
            const tier = getMyTier();
            let infoText = '';
            if(tier === 0) infoText = 'âšª Ãœcretsiz: GÃ¼nde <b>1 fotoÄŸraf</b> paylaÅŸabilirsiniz. Video iÃ§in Standart Ã¼yelik gerekli.';
            else if(tier === 1) infoText = 'â­ Standart: GÃ¼nde <b>1 fotoÄŸraf veya video</b> paylaÅŸabilirsiniz.';
            else infoText = 'ğŸ’ Deluxe/Ultra+: GÃ¼nde <b>2 Reel</b> paylaÅŸabilirsiniz.';
            if(infoEl) infoEl.innerHTML = infoText;
            // Video butonunu Ã¼cretsizler iÃ§in soluk gÃ¶ster ama tÄ±klanabilir bÄ±rak
            const videoLabel = document.getElementById('reel-video-btn');
            if(videoLabel) {
                videoLabel.style.opacity = tier >= 1 ? '1' : '0.5';
                videoLabel.title = tier < 1 ? 'Video iÃ§in Standart Ã¼yelik gerekli' : '';
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
                    if(confirm("Video paylaÅŸmak iÃ§in Standart Ã¼yelik gereklidir. Ãœyelik almak ister misin?")) {
                        document.getElementById('reel-upload-modal').classList.add('hidden');
                        switchTab(6);
                    }
                    return;
                }
                if(file.size > 50 * 1024 * 1024) {
                    alert('Video boyutu maksimum 50MB olmalÄ±dÄ±r!');
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
                loadDiv.textContent = 'Video hazÄ±rlanÄ±yor...';
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

            // Video henÃ¼z FileReader ile okunuyorsa bekle
            if(reelFileType === 'video' && !reelFileData) {
                alert('Video hÃ¢lÃ¢ hazÄ±rlanÄ±yor, lÃ¼tfen birkaÃ§ saniye bekleyin.');
                return;
            }
            if(!reelFileData) { alert('Ã–nce bir fotoÄŸraf veya video seÃ§in!'); return; }

            const caption = document.getElementById('reel-caption').value.trim();
            const submitBtn = document.getElementById('reel-submit-btn');
            const progressDiv = document.getElementById('reel-upload-progress');
            const progressBar = document.getElementById('reel-progress-bar');
            const progressLabel = progressDiv ? progressDiv.querySelector('.text-xs') : null;

            submitBtn.disabled = true;
            submitBtn.textContent = 'YÃ¼kleniyor...';
            if(progressDiv) progressDiv.classList.remove('hidden');

            function setProgress(pct, label) {
                if(progressBar) progressBar.style.width = pct + '%';
                if(progressLabel) progressLabel.textContent = label;
            }

            try {
                setProgress(15, reelFileType === 'video' ? 'Video sunucuya yÃ¼kleniyor...' : 'FotoÄŸraf yÃ¼kleniyor...');

                // AdÄ±m 1: MedyayÄ± R2'ye yÃ¼kle
                const uploadRes = await fetch('/api/data', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ action: 'upload_media', data: { media_data: reelFileData, folder: 'reels' } })
                });

                if(!uploadRes.ok) throw new Error('Sunucu hatasÄ±: ' + uploadRes.status);
                const uploadData = await uploadRes.json();
                setProgress(80, 'Reel kaydediliyor...');

                if(!uploadData || !uploadData.url) {
                    // Oturum sÃ¼resi dolmuÅŸsa yeniden giriÅŸ iste
                    if(uploadData?.message === 'GiriÅŸ yapmalÄ±sÄ±nÄ±z!') {
                        alert('Oturumun sÃ¼resi dolmuÅŸ, lÃ¼tfen tekrar giriÅŸ yap.');
                        logout();
                        return;
                    }
                    throw new Error(uploadData?.message || 'Medya sunucuya yÃ¼klenemedi.');
                }

                // AdÄ±m 2: Sadece URL ile add_reel â€” kÃ¼Ã§Ã¼k payload
                const res = await fetch('/api/data', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ action: 'add_reel', data: {
                        media_url: uploadData.url,
                        media_type: reelFileType,
                        caption: caption
                    }})
                });

                if(!res.ok) throw new Error('KayÄ±t hatasÄ±: ' + res.status);
                const resData = await res.json();
                setProgress(100, 'TamamlandÄ±!');

                if(resData && resData.status === 'ok') {
                    setTimeout(() => {
                        document.getElementById('reel-upload-modal').classList.add('hidden');
                        clearReelFile();
                        document.getElementById('reel-caption').value = '';
                        loadReels();
                    }, 400);
                } else {
                    if(resData?.message === 'GiriÅŸ yapmalÄ±sÄ±nÄ±z!') { alert('Oturumun sÃ¼resi dolmuÅŸ, lÃ¼tfen tekrar giriÅŸ yap.'); logout(); return; }
                    alert(resData?.message || 'Reel paylaÅŸÄ±lamadÄ±, tekrar deneyin.');
                }
            } catch(e) {
                console.error('Reel upload error:', e);
                alert('YÃ¼kleme hatasÄ±: ' + (e.message || 'Bilinmeyen hata. LÃ¼tfen tekrar deneyin.'));
            } finally {
                submitBtn.disabled = false;
                submitBtn.textContent = 'PAYLAÅ';
                if(progressDiv) setTimeout(() => progressDiv.classList.add('hidden'), 600);
            }
        }

        function formatTimeAgo(ts) {
            if(!ts) return '';
            const diff = Math.floor(Date.now() / 1000) - ts;
            if(diff < 60) return 'Az Ã¶nce';
            if(diff < 3600) return Math.floor(diff/60) + 'dk';
            if(diff < 86400) return Math.floor(diff/3600) + 'sa';
            return Math.floor(diff/86400) + 'g';
        }
        // â”€â”€ Herhangi bir reel objesini direkt tam ekran aÃ§ â”€â”€
        // Hem profil grid tÄ±klamasÄ±ndan hem de ileride baÅŸka yerlerden Ã§aÄŸrÄ±labilir.
        window.openReelDirect = function(reel) {
            if(!reel || !reel.media_url) return;
            stopAllMedia(); // Ã–nceki sesleri temizle

            // Ã–nce reels sekmesini arka planda aktif et (butonlar gÃ¶rÃ¼nsÃ¼n diye)
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
            if(soundBtn) { soundBtn.style.display = 'flex'; soundBtn.textContent = _reelMuted ? 'ğŸ”‡' : 'ğŸ”Š'; }
            const gridBtn = document.getElementById('grid-view-btn');
            if(gridBtn) gridBtn.style.display = 'flex';
            const uploadTopBtn = document.getElementById('reels-upload-top-btn');
            if(uploadTopBtn) uploadTopBtn.style.display = 'flex';

            // Ã–nceki overlay varsa temizle
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

            // Kapat butonu (saÄŸ Ã¼st â€” overlay'e Ã¶zel)
            const closeBtn = document.createElement('button');
            closeBtn.innerHTML = 'âœ•';
            closeBtn.style.cssText = 'position:absolute;top:calc(env(safe-area-inset-top, 0px) + 72px);right:16px;z-index:10;width:44px;height:44px;border-radius:50%;background:rgba(0,0,0,0.65);color:#fff;font-size:18px;font-weight:bold;border:1px solid rgba(255,255,255,0.25);display:flex;align-items:center;justify-content:center;cursor:pointer;backdrop-filter:blur(4px);';
            closeBtn.onclick = () => {
                if(mediaEl.tagName === 'VIDEO') {
                    mediaEl.pause();
                    mediaEl.removeAttribute('src');
                    mediaEl.load(); // tarayÄ±cÄ±yÄ± tamamen sÄ±fÄ±rla, ses kesilir
                }
                overlay.remove();
                closeReels();
            };

            // Sol alt: kullanÄ±cÄ± + aÃ§Ä±klama
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

            // SaÄŸ: beÄŸeni
            const actions = document.createElement('div');
            actions.style.cssText = 'position:absolute;right:12px;bottom:32px;z-index:10;display:flex;flex-direction:column;align-items:center;gap:16px;';
            const isLiked = (typeof currentUser !== 'undefined' && currentUser) && (reel.likes || []).includes(currentUser.username);
            actions.innerHTML = `
                <div style="display:flex;flex-direction:column;align-items:center;gap:4px;">
                    <div style="width:40px;height:40px;border-radius:50%;background:rgba(0,0,0,0.5);backdrop-filter:blur(4px);display:flex;align-items:center;justify-content:center;font-size:20px;border:1px solid rgba(255,255,255,0.2);">${isLiked ? 'â¤ï¸' : 'ğŸ¤'}</div>
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

        // â”€â”€ Merkezi popstate yÃ¶neticisi â€” tÃ¼m reel geri tuÅŸu durumlarÄ± â”€â”€
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
            // reelFullscreen: yukarÄ±daki ayrÄ± listener zaten handle ediyor
        });

        // ================================================================
        // REELS â€” YENÄ° GLOBAL FONKSÄ°YONLAR
        // ================================================================

        // 1. Story varsa story gÃ¶rÃ¼ntÃ¼leyiciyi aÃ§, yoksa profile git
        window.openProfileOrStory = async function(username) {
            if(!username) return;
            const now = Math.floor(Date.now() / 1000);
            const activeStories = (db.stories || []).filter(s => s.user === username && s.expires_at > now);
            if(activeStories.length > 0) {
                // Story viewer'Ä± o kullanÄ±cÄ±nÄ±n story'siyle aÃ§
                _storyList = activeStories;
                _storyIndex = 0;
                showCurrentStory();
                const modal = document.getElementById('story-view-modal');
                if(modal) modal.classList.remove('hidden');
            } else {
                showOtherProfile(username);
            }
        };

        // 2. Grid â†” Feed geÃ§iÅŸ
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
                // Grid moda geÃ§
                // Observer'Ä± durdur â€” grid'de video otomatik Ã§almasÄ±n
                if(_feedObserver) { _feedObserver.disconnect(); _feedObserver = null; }
                feed.classList.add('grid-mode');
                if(soundBtn) soundBtn.style.display = 'none';
                // TÃ¼m videolarÄ± durdur ve sessize al
                feed.querySelectorAll('video').forEach(v => { v.pause(); v.muted = true; });
                // Grid kartlarÄ±na click ekle (duplicate Ã¶nleme: data flag ile)
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
                // Feed moduna dÃ¶n
                feed.classList.remove('grid-mode');
                if(soundBtn && reelsData.length) soundBtn.style.display = 'flex';
                // Grid click listener'larÄ±nÄ± kaldÄ±r ve flag'i temizle
                feed.querySelectorAll(':scope > div').forEach(card => {
                    card.removeEventListener('click', _onGridCardClick);
                    delete card.dataset.gridClickBound;
                });
                // Observer'Ä± yeniden kur, mevcut scroll pozisyonunda oynayan videoyu baÅŸlat
                _setupFeedObserver();
                if(gridBtn) gridBtn.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="width:18px;height:18px;"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/></svg>`;
            }
        };

        // Grid kart click handler (ayrÄ± referans olmalÄ± ki removeEventListener Ã§alÄ±ÅŸsÄ±n)
        function _onGridCardClick(e) {
            const idx = parseInt(this.dataset.reelIdx);
            if(!isNaN(idx)) window.openReelsGridItem(idx);
        }

        // 3. Izgaradan bir video â†’ tam ekran
        // 3. Izgaradan bir video/fotoÄŸraf â†’ tam ekran (body'e ekle â†’ fixed parent sorunu yok)
        window.openReelsGridItem = function(idx) {
            if(!reelsData[idx]) return;
            const reel = reelsData[idx];

            // Ã–nceki overlay varsa sessizce temizle
            window.exitReelFullscreen(true);

            _reelFullscreenIdx = idx;

            const overlay = document.createElement('div');
            overlay.id = 'reel-fs-overlay';
            // body'e fixed ekliyoruz â€” screenReels'e deÄŸil (fixed-in-fixed sorunu Ã§Ã¶zÃ¼ldÃ¼)
            overlay.style.cssText = 'position:fixed;inset:0;z-index:999999;background:#000;display:flex;align-items:center;justify-content:center;overflow:hidden;';

            // Kapatma butonu
            const closeBtn = document.createElement('button');
            closeBtn.innerHTML = 'âœ•';
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
            document.body.appendChild(overlay);  // â† body'e ekle
            _reelFullscreenOverlay = overlay;

            // Geri tuÅŸu desteÄŸi
            history.pushState({ reelFullscreen: true, reelIdx: idx }, '');
        };

        // 4. Tam ekranÄ± kapat â†’ grid gÃ¶rÃ¼nÃ¼mÃ¼ne geri dÃ¶n
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

        // 5. Geri tuÅŸu / popstate â†’ tam ekranÄ± kapat, grid'e dÃ¶n
        window.addEventListener('popstate', function(e) {
            if(e.state && e.state.reelFullscreen) {
                window.exitReelFullscreen(false);
                e.preventDefault && e.preventDefault();
            }
        });

        // ================================================================
        // REELS SÄ°STEMÄ° JS SONU
        // ================================================================

        async function toggleRidingMode() {
            if(!currentUser) return;
            
            let stats = currentUser.stats || {};
            const isCurrentlyRiding = stats.riding_until && stats.riding_until > Date.now();
            
            if(isCurrentlyRiding) {
                if(confirm("SÃ¼rÃ¼ÅŸ modunu kapatmak istiyor musun? Haritadan gizleneceksin.")) {
                    stats.riding_until = 0;
                    await sendAction('update_user', currentUser);
                    
                    document.getElementById("radar-info").classList.add("hidden");
                    document.getElementById("btn-riding-mode").innerHTML = "ğŸ“¡ RADAR (SÃœRÃœÅTEYÄ°M)";
                    document.getElementById("btn-riding-mode").className = "bg-green-600/90 backdrop-blur hover:bg-green-500 btn-premium-hover px-3 py-2 rounded-xl shadow-[0_0_15px_rgba(34,197,94,0.4)] flex items-center justify-center text-[10px] uppercase tracking-widest font-bold text-white border border-green-400/50 pointer-events-auto";
                    
                    syncMap();
                    alert("SÃ¼rÃ¼ÅŸ modu kapatÄ±ldÄ±.");
                }
            } else {
                if(!userLat || !userLng) return alert("Konumunuz henÃ¼z bulunamadÄ±. LÃ¼tfen Ã¶nce ğŸ¯ butonuna basarak konum izni verin.");
                
                if(confirm("Konumun 3 saat boyunca haritada diÄŸer sÃ¼rÃ¼cÃ¼lere canlÄ± olarak gÃ¶sterilecek. OnaylÄ±yor musun?")) {
                    stats.riding_until = Date.now() + (3 * 60 * 60 * 1000); 
                    stats.riding_lat = userLat;
                    stats.riding_lng = userLng;
                    
                    await sendAction('update_user', currentUser);
                    
                    document.getElementById("radar-info").classList.remove("hidden");
                    document.getElementById("btn-riding-mode").innerHTML = "ğŸ›‘ SÃœRÃœÅÃœ BÄ°TÄ°R";
                    document.getElementById("btn-riding-mode").className = "bg-sky-600/90 backdrop-blur hover:bg-red-500 btn-premium-hover px-3 py-2 rounded-xl shadow-[0_0_15px_rgba(14,165,233,0.4)] flex items-center justify-center text-[10px] uppercase tracking-widest font-bold text-white border border-red-400/50 pointer-events-auto";
                    
                    syncMap();
                    alert("SÃ¼rÃ¼ÅŸ modu aktif! ArtÄ±k haritada radar olarak parlÄ±yorsun.");
                }
            }
        }

        // ==============================================================
        // BÄ°SÄ°KLET DÃœZENLEME VE SÄ°LME FONKSÄ°YONLARI 
        // ==============================================================
        async function deleteBike(index) {
            if(!confirm("Bu bisikleti garajÄ±ndan kalÄ±cÄ± olarak silmek istediÄŸine emin misin?")) return;
            
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
            if(lbl) lbl.textContent = `Yeni Fotograf (Maks ${maxPhotos}) - Bos birakÄ±rsan eskileri kalÄ±r`;

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
                alert("Plus Ã¼yeliÄŸi olmayan kullanÄ±cÄ±lar garaja bisiklet ekleyemez! Pazar veya Plus menÃ¼sÃ¼nden Ã¼yeliÄŸini yÃ¼kselt.");
                switchTab(6);
                return;
            }
            if(garage.length >= maxBikes) {
                return alert(`Mevcut paketiniz garajÄ±nÄ±za en fazla ${maxBikes} bisiklet eklemenize izin veriyor! Plus menÃ¼sÃ¼nden paketinizi yÃ¼kseltin.`);
            }

            document.getElementById("bike-model").value = ""; 
            document.getElementById("bike-fork").value = ""; 
            document.getElementById("bike-shock").value = ""; 
            document.getElementById("bike-brakes").value = ""; 
            document.getElementById("bike-desc").value = ""; 
            document.getElementById("bike-photo").value = "";
            document.getElementById("bike-photo-label").textContent = `Bisiklet FotoÄŸraflarÄ± (Maksimum ${maxPhotos} adet)`;
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
            // Lokal db'yi gÃ¼ncelle
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
                container.innerHTML = "<div class='col-span-2 text-center text-xs text-zinc-500 italic py-4'>Garaj boÅŸ.</div>"; 
                return; 
            }
            
            container.innerHTML = "";
            
            u.stats.garage.forEach((b, index) => {
                let delBtn = isSelf 
                    ? `<button onclick="event.stopPropagation(); deleteBike(${index})" class="absolute top-1 right-1 bg-red-600 hover:bg-red-500 transition w-6 h-6 rounded-full flex items-center justify-center text-white text-xs shadow-md z-20 btn-premium-hover">âœ•</button>` 
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
            if(confirm("Sistemden Ã§Ä±kÄ±ÅŸ yapmak istediÄŸine emin misin?")) {
                try {
                    await sendAction('logout', {});
                } catch(e) {
                    console.log("Sunucu Ã§Ä±kÄ±ÅŸ hatasÄ±, yerel veriler temizleniyor...");
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
            // Ã–nceki oturumdan mesaj cache'i yÃ¼kle (anlÄ±k gÃ¶rÃ¼nsÃ¼n)
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
            // Ã‡arkÄ± Ã¶nceden Ã§iz â€” sekmede aÃ§Ä±lÄ±nca zaten hazÄ±r olsun
            setTimeout(initWheel3D, 500); 

            // Popup triggers removed per user request
            
            currentMessageCount = db.messages.length; 
            
            if(currentUser.stats && currentUser.stats.riding_until > Date.now()) {
                document.getElementById("radar-info").classList.remove("hidden");
                document.getElementById("btn-riding-mode").innerHTML = "ğŸ›‘ SÃœRÃœÅÃœ BÄ°TÄ°R";
                document.getElementById("btn-riding-mode").className = "bg-sky-600/90 backdrop-blur hover:bg-red-500 btn-premium-hover transition px-3 py-2 rounded-xl shadow-[0_0_15px_rgba(14,165,233,0.4)] flex items-center justify-center text-[10px] uppercase tracking-widest font-bold text-white border border-red-400/50 pointer-events-auto";
            }
            
            if (currentUser.stats && currentUser.stats.onboarding === false) {
                // Deneme bitiÅŸ tarihini doldur
                const expDate = currentUser.stats.premium_expire_date || '';
                const trialDateEl = document.getElementById('onboarding-trial-date');
                if(trialDateEl && expDate) {
                    trialDateEl.textContent = 'â° Deneme BitiÅŸ Tarihi: ' + expDate;
                }
                document.getElementById("onboarding-modal").classList.remove("hidden");
            }

            updateMyLocation();
            sendHeartbeat();
            // Heartbeat: her 30 sn (Ã§evrim iÃ§i doÄŸruluk iÃ§in)
            setInterval(sendHeartbeat, 60000);
            // Konum + radar: her 60 sn
            setInterval(() => {
                updateMyLocation();
                refreshRadars();
            }, 60000);
            // Push bildirim: Profil sayfasÄ±ndaki butondan aÃ§Ä±lÄ±yor
            updateNotifBtnState();
            loadSavedTheme();
            _lastTitleName = getTitle(currentUser.xp).name;
            // OneSignal: kullanÄ±cÄ± kimliÄŸini set et (bildirim hedefleme iÃ§in)
            // setTimeout yerine doÄŸrudan Ã§aÄŸÄ±r â€” setOneSignalUser iÃ§inde Deferred kuyruÄŸu kullanÄ±lÄ±yor
            setOneSignalUser();
        }

        // â”€â”€ Modern Premium Bildirim Popup â”€â”€
        function showPremiumNotifPopup() {
            const overlay = document.createElement('div');
            overlay.className = 'notif-popup-overlay';
            overlay.id = 'premium-notif-popup';
            overlay.onclick = function(e) { if(e.target === overlay) closePremiumNotifPopup(); };
            overlay.innerHTML = `
                <div class="notif-popup-card">
                    <button onclick="closePremiumNotifPopup()" style="position:absolute;top:12px;right:14px;background:rgba(255,255,255,0.1);border:none;color:#999;width:28px;height:28px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:14px;cursor:pointer;transition:0.2s;z-index:10" onmouseover="this.style.background='rgba(255,255,255,0.2)';this.style.color='#fff'" onmouseout="this.style.background='rgba(255,255,255,0.1)';this.style.color='#999'">âœ•</button>
                    <div style="text-align:center;margin-bottom:18px">
                        <div style="font-size:32px;margin-bottom:8px">ğŸš´â€â™‚ï¸</div>
                        <div style="font-size:16px;font-weight:900;color:#fff;letter-spacing:0.5px">FreeriderTR Plus</div>
                        <div style="font-size:10px;color:#94a3b8;font-weight:600;text-transform:uppercase;letter-spacing:2px;margin-top:4px">Premium Deneyim</div>
                    </div>
                    <div style="background:linear-gradient(135deg,rgba(59,130,246,0.15),rgba(168,85,247,0.1));border:1px solid rgba(59,130,246,0.2);border-radius:12px;padding:14px 16px;margin-bottom:18px">
                        <div style="display:flex;flex-direction:column;gap:8px">
                            <div style="display:flex;align-items:center;gap:8px;font-size:12px;color:#e2e8f0;font-weight:600">
                                <span style="font-size:14px">ğŸ¨</span> Ã–zel isim renkleri ve profil efektleri
                            </div>
                            <div style="display:flex;align-items:center;gap:8px;font-size:12px;color:#e2e8f0;font-weight:600">
                                <span style="font-size:14px">ğŸï¸</span> 4 bisiklet garajÄ± ve 10 fotoÄŸraflÄ± ilanlar
                            </div>
                            <div style="display:flex;align-items:center;gap:8px;font-size:12px;color:#e2e8f0;font-weight:600">
                                <span style="font-size:14px">âœ…</span> OnaylÄ± profil rozeti
                            </div>
                            <div style="display:flex;align-items:center;gap:8px;font-size:12px;color:#e2e8f0;font-weight:600">
                                <span style="font-size:14px">ğŸ¤–</span> SÄ±nÄ±rsÄ±z AI sohbet
                            </div>
                        </div>
                    </div>
                    <button onclick="closePremiumNotifPopup();switchTab(6);" style="width:100%;padding:12px;border:none;border-radius:12px;background:linear-gradient(135deg,#3b82f6,#8b5cf6);color:#fff;font-size:13px;font-weight:800;cursor:pointer;letter-spacing:0.5px;transition:0.2s;box-shadow:0 4px 20px rgba(59,130,246,0.4)" onmouseover="this.style.transform='translateY(-1px)';this.style.boxShadow='0 6px 25px rgba(59,130,246,0.5)'" onmouseout="this.style.transform='';this.style.boxShadow='0 4px 20px rgba(59,130,246,0.4)'">Paketleri Ä°ncele â†’</button>
                    <div style="text-align:center;margin-top:10px;font-size:10px;color:#64748b;font-weight:500">3 gÃ¼n Ã¼cretsiz deneme ile baÅŸla</div>
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
                // stats bir JSONB kolon - nested select sÃ¶zdizimi yanlÄ±ÅŸ, direkt stats seÃ§
                const { data, error } = await supaClient.from('users')
                    .select('username, stats');
                        
                if (data && !error) {
                    data.forEach(fetchedUser => {
                        const s = fetchedUser.stats;
                        if (!s) return;
                        let existingUser = db.users.find(u => u.username === fetchedUser.username);
                        if (existingUser) {
                            if(!existingUser.stats) existingUser.stats = {};
                            // Radar gÃ¼ncelle
                            existingUser.stats.riding_lat = s.riding_lat;
                            existingUser.stats.riding_lng = s.riding_lng;
                            existingUser.stats.riding_until = s.riding_until;
                            // Ã‡EVRÄ°M Ä°Ã‡Ä°: last_seen_ts gÃ¼ncelle (kritik!)
                            if (s.last_seen_ts) existingUser.stats.last_seen_ts = s.last_seen_ts;
                        }
                    });
                    if (map) syncMap();
                }
            } catch(e) { console.error("Radar hatasÄ±:", e); }
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
            let adminTag = (currentUser.role === 'Admin') ? '<span class="ml-2 bg-red-600 text-white px-2 py-0.5 rounded text-[9px] tracking-widest uppercase shadow-[0_0_10px_red] relative z-50">ğŸ‘‘ YÃ¶netici</span>' : (currentUser.role === 'SubAdmin' ? '<span class="ml-2 bg-orange-800 text-orange-200 px-2 py-0.5 rounded text-[9px] uppercase font-bold tracking-widest">ğŸ›¡ï¸ Yrd. Admin</span>' : '');
            
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

            document.getElementById("profile-bio").textContent = currentUser.bio || "Biyografi eklenmemiÅŸ."; 
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
                    xpBarEl.innerHTML = `<div class="mt-2 text-center text-xs font-bold text-prem-rainbow">MAX SEVIYE ğŸŒŸ</div>`;
                }
            }

            let badges = "";
            // Premium badges - all with explicit blocks to avoid else-if chain issues
            if(stats.is_trial) { badges += `<span class="bg-gradient-to-r from-yellow-500 to-amber-400 text-black px-3 py-1.5 rounded-lg text-[10px] font-black shadow-[0_0_15px_rgba(234,179,8,0.6)] uppercase tracking-widest scale-in-anim animate-pulse">ğŸ 3 Gun Deneme</span> `; }
            if(premTier === 3) { badges += `<span class="bg-yellow-500 text-black px-3 py-1.5 rounded-lg text-[10px] font-black shadow-[0_0_15px_rgba(234,179,8,0.5)] uppercase tracking-widest scale-in-anim">ğŸ‘‘ Ultra+</span> `; }
            else if(premTier === 2) { badges += `<span class="bg-purple-600 text-white px-3 py-1.5 rounded-lg text-[10px] font-bold shadow-[0_0_15px_rgba(168,85,247,0.5)] uppercase tracking-widest scale-in-anim">ğŸŒŸ Deluxe</span> `; }
            else if(premTier === 1) { badges += `<span class="bg-gradient-to-r from-blue-600 to-purple-600 text-white px-3 py-1.5 rounded-lg text-[10px] font-bold shadow-lg uppercase tracking-widest scale-in-anim">â­ Standart</span> `; }
            // Activity badges
            if(stats.markers >= 10){ badges += `<span class="bg-emerald-900/50 text-emerald-300 border border-emerald-700 px-2 py-1 rounded-lg text-[10px] font-bold scale-in-anim">ğŸ—ºï¸ Haritaci</span> `; }
            else if(stats.markers >= 1){ badges += `<span class="bg-zinc-800 text-zinc-300 border border-zinc-700 px-2 py-1 rounded-lg text-[10px] font-bold scale-in-anim">ğŸ“ Kasif</span> `; }
            if(stats.events >= 5){ badges += `<span class="bg-blue-900/50 text-blue-300 border border-blue-700 px-2 py-1 rounded-lg text-[10px] font-bold scale-in-anim">ğŸ† Topluluk Lideri</span> `; }
            else if(stats.events >= 1){ badges += `<span class="bg-zinc-800 text-zinc-300 border border-zinc-700 px-2 py-1 rounded-lg text-[10px] font-bold scale-in-anim">ğŸ“… Organizator</span> `; }
            if(stats.market >= 5){ badges += `<span class="bg-amber-900/50 text-amber-300 border border-amber-700 px-2 py-1 rounded-lg text-[10px] font-bold scale-in-anim">ğŸ’° Pazar Ustasi</span> `; }
            else if(stats.market >= 1){ badges += `<span class="bg-zinc-800 text-zinc-300 border border-zinc-700 px-2 py-1 rounded-lg text-[10px] font-bold scale-in-anim">ğŸ¤ Esnaf</span> `; }
            if(stats.login_streak >= 100){ badges += `<span class="bg-violet-900/50 text-violet-300 border border-violet-700 px-2 py-1 rounded-lg text-[10px] font-bold scale-in-anim">âš¡ 100 Gun</span> `; }
            else if(stats.login_streak >= 30){ badges += `<span class="bg-indigo-900/50 text-indigo-300 border border-indigo-700 px-2 py-1 rounded-lg text-[10px] font-bold scale-in-anim">ğŸ’ Demir Uye</span> `; }
            else if(stats.login_streak >= 7){ badges += `<span class="bg-orange-900/50 text-orange-300 border border-orange-700 px-2 py-1 rounded-lg text-[10px] font-bold scale-in-anim">ğŸ”¥ Seri Girisci</span> `; }
            if(stats.total_messages >= 200){ badges += `<span class="bg-cyan-900/50 text-cyan-300 border border-cyan-700 px-2 py-1 rounded-lg text-[10px] font-bold scale-in-anim">ğŸ‘‘ Chat Efsanesi</span> `; }
            else if(stats.total_messages >= 50){ badges += `<span class="bg-zinc-800 text-zinc-300 border border-zinc-700 px-2 py-1 rounded-lg text-[10px] font-bold scale-in-anim">ğŸ—£ï¸ Sohbet Tutkunu</span> `; }
            // XP level badges
            if(currentUser.xp >= 50000){ badges += `<span class="bg-gradient-to-r from-red-700 to-purple-700 text-white px-2 py-1 rounded-lg text-[10px] font-black scale-in-anim text-prem-rainbow">ğŸŒŸ Downhill Efsanesi</span> `; }
            else if(currentUser.xp >= 20000){ badges += `<span class="bg-red-900/50 text-red-300 border border-sky-600 px-2 py-1 rounded-lg text-[10px] font-bold scale-in-anim">ğŸ‘‘ Efsane</span> `; }
            else if(currentUser.xp >= 10000){ badges += `<span class="bg-yellow-900/50 text-yellow-300 border border-yellow-700 px-2 py-1 rounded-lg text-[10px] font-bold scale-in-anim">ğŸ† Sampiyon</span> `; }
            else if(currentUser.xp >= 7000){ badges += `<span class="bg-rose-900/50 text-rose-300 border border-rose-700 px-2 py-1 rounded-lg text-[10px] font-bold scale-in-anim">ğŸ’¥ Elite</span> `; }
            else if(currentUser.xp >= 4000){ badges += `<span class="bg-orange-900/50 text-orange-300 border border-orange-700 px-2 py-1 rounded-lg text-[10px] font-bold scale-in-anim">ğŸ”¥ Usta</span> `; }
            // Earned mission badges
            const eb = stats.earned_badges || [];
            eb.forEach(b => { badges += `<span class="bg-zinc-800 text-zinc-200 border border-zinc-600 px-2 py-1 rounded-lg text-[10px] font-bold scale-in-anim">ğŸ… ${b}</span> `; });

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

                // Paket kartlarÄ±nÄ± gizle (zaten Ã¼ye, tekrar satÄ±n alma gÃ¶rseli gÃ¶sterme)
                const packageCardsWrap = document.querySelector('#screen-premium .space-y-4');
                if (packageCardsWrap) packageCardsWrap.classList.add('hidden');

                // Aktif plan kartÄ±nÄ± doldur
                const planNames = { 1: 'â­ Standart Paket', 2: 'ğŸŒŸ Deluxe Paket', 3: 'ğŸ‘‘ Ultra+ Paket' };
                const planColors = { 1: 'bg-blue-900/60 text-blue-300 border border-blue-700/50', 2: 'bg-purple-900/60 text-purple-300 border border-purple-700/50', 3: 'bg-yellow-900/60 text-yellow-300 border border-yellow-700/50' };
                const planNameEl = document.getElementById('current-plan-name');
                const planBadgeEl = document.getElementById('current-plan-badge');
                const planExpiryEl = document.getElementById('current-plan-expiry');
                if (planNameEl) planNameEl.textContent = planNames[premTier] || 'Plus Ãœye';
                if (planBadgeEl) { planBadgeEl.textContent = 'AKTÄ°F'; planBadgeEl.className = 'text-xs font-black px-3 py-1 rounded-lg ' + (planColors[premTier] || ''); }
                if (planExpiryEl) {
                    const expDate = stats.premium_expire_date;
                    planExpiryEl.textContent = expDate ? 'ğŸ“… BitiÅŸ tarihi: ' + expDate : 'â™¾ï¸ SÃ¼resiz aktif';
                }

                // YÃ¼kselt butonu: Standart (1) veya Deluxe (2) kullanÄ±cÄ±sÄ±na gÃ¶ster, Ultra+ (3) iÃ§in gizle
                const upgradeSec = document.getElementById('upgrade-plan-section');
                const upgradeSelect = document.getElementById('upgrade-tier-select');
                const upgradeHint = document.getElementById('upgrade-hint-text');
                if (premTier < 3 && upgradeSec && upgradeSelect) {
                    upgradeSec.classList.remove('hidden');
                    upgradeSelect.innerHTML = '';
                    if (premTier === 1) {
                        upgradeSelect.innerHTML += '<option value="freeridertr_deluxe_pack_monthly">ğŸŒŸ Deluxe Paket â€” 20 TL/Ay</option>';
                        upgradeSelect.innerHTML += '<option value="freeridertr_ultra_pack_monthly">ğŸ‘‘ Ultra+ Paket â€” 30 TL/Ay</option>';
                        if (upgradeHint) upgradeHint.textContent = 'Deluxe veya Ultra+ a gecerek daha fazla ozellik ac.';
                    } else if (premTier === 2) {
                        upgradeSelect.innerHTML += '<option value="freeridertr_ultra_pack_monthly">ğŸ‘‘ Ultra+ Paket â€” 30 TL/Ay</option>';
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
                        html += createColorBtn('std-yellow', 'SarÄ±', premColor);
                        html += createColorBtn('std-pink', 'Pembe', premColor);
                        html += createColorBtn('std-green', 'YeÅŸil', premColor);
                    }
                    if (premTier >= 2) {
                        html += `<div class="w-full text-[10px] text-yellow-500 uppercase tracking-widest font-bold mb-1 mt-3 border-t border-zinc-800 pt-3">Deluxe Renkler:</div>`;
                        html += createColorBtn('ult-gold', 'AltÄ±n', premColor);
                        html += createColorBtn('ult-rainbow', 'GÃ¶kkuÅŸaÄŸÄ±', premColor);
                        html += createColorBtn('dlx-blue', 'Simli Mavi', premColor);
                        html += createColorBtn('dlx-pink', 'Simli Pembe', premColor);
                        html += createColorBtn('dlx-green', 'Simli YeÅŸil', premColor);
                    }
                    if (premTier >= 3) {
                        html += `<div class="w-full text-[10px] text-sky-400 uppercase tracking-widest font-bold mb-1 mt-3 border-t border-zinc-800 pt-3">Ultra+ Ã–zel Renk (Hex):</div>`;
                        html += `<div class="w-full flex gap-2 mb-2 items-center">
                                    <input type="color" id="custom-hex-color" class="w-12 h-10 rounded cursor-pointer bg-zinc-900 border border-zinc-700 shadow-inner" value="${premColor.startsWith('#') ? premColor : '#ff0000'}">
                                    <button onclick="applyCustomHex()" class="bg-white text-black px-4 py-2 rounded-lg text-xs font-bold shadow-lg hover:bg-gray-200 transition btn-premium-hover">Uygula</button>
                                 </div>`;
                        
                        html += `<div class="w-full text-[10px] text-sky-400 uppercase tracking-widest font-bold mb-1 mt-2">Ultra+ Profil Efekti:</div>`;
                        const currentEffect = stats.avatar_effect || 'none';
                        html += createEffectBtn('none', 'Efekt Yok', currentEffect);
                        html += createEffectBtn('fire', 'ğŸ”¥ Alev', currentEffect);
                        html += createEffectBtn('ice', 'â„ï¸ Buz', currentEffect);
                    }
                    colorContainer.innerHTML = html;
                }
            } else {
                document.getElementById("premium-buy-section").classList.remove("hidden");
                document.getElementById("premium-settings-section").classList.add("hidden");
                // Ãœye deÄŸilse paket kartlarÄ±nÄ± tekrar gÃ¶ster
                const packageCardsWrap = document.querySelector('#screen-premium .space-y-4');
                if (packageCardsWrap) packageCardsWrap.classList.remove('hidden');
            }
            
            renderGarage(currentUser.username, 'self');
        }

        // â”€â”€ Google Play IAP SatÄ±n Alma AkÄ±ÅŸÄ± â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
        // â”€â”€ Web / TarayÄ±cÄ± SatÄ±n Alma Talebi â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
        // Android/iOS yoksa admin'e DM + push bildirimi gÃ¶nderir.
        async function _sendWebPurchaseRequest(productId) {
            const confirmed = window.confirm(
                'Web Ã¼zerinden alÄ±mlarda Ã¶deme onayÄ± iÃ§in yÃ¶netici ile iletiÅŸime geÃ§ilecektir.\n\nDevam etmek istiyor musunuz?'
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
                    showToast(data.message || 'âœ… Talebiniz yÃ¶neticiye iletildi!');
                } else if (data.status === 'wait') {
                    showToast(data.message || 'â³ Zaten bir talebiniz var, lÃ¼tfen bekleyin.');
                } else {
                    showToast('âŒ ' + (data.message || 'Bir hata oluÅŸtu, tekrar deneyin.'));
                }
            } catch(err) {
                console.error('[IAP] Web purchase request hatasÄ±:', err);
                showToast('âŒ BaÄŸlantÄ± hatasÄ±. Ä°nternet baÄŸlantÄ±nÄ±zÄ± kontrol edin.');
            } finally {
                btns.forEach(b => { b.disabled = false; b.style.opacity = '1'; });
            }
        }

        // requestPremium() fonksiyonu artÄ±k Google Play Billing Library'yi tetikler.
        // Mobil uygulama (WebView iÃ§inde), bu fonksiyonu Ã§aÄŸÄ±ran JS Bridge Ã¼zerinden
        // Android uygulamasÄ±na productId'yi iletir ve satÄ±n alÄ±m akÄ±ÅŸÄ±nÄ± baÅŸlatÄ±r.
        // SatÄ±n alÄ±m tamamlandÄ±ÄŸÄ±nda Android, verifyGooglePurchase() fonksiyonunu
        // Ã§aÄŸÄ±rarak purchaseToken'Ä± backend'e doÄŸrulama iÃ§in gÃ¶nderir.
        async function requestPremium() {
            const sel = document.getElementById("premium-tier-select");
            if (!sel) { showToast('âš ï¸ ÃœrÃ¼n seÃ§ici bulunamadÄ±.'); return; }
            const productId = sel.value;
            if (!productId) { showToast('âš ï¸ LÃ¼tfen bir paket seÃ§in.'); return; }

            // â”€â”€ Android WebView JS Bridge kontrolÃ¼ â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
            // window.Android nesnesi yoksa veya launchBilling metodu tanÄ±mlÄ± deÄŸilse
            // uyarÄ± gÃ¶ster; uygulamayÄ± Ã§Ã¶kertme.
            if (typeof window.Android !== 'undefined' && window.Android !== null) {
                if (typeof window.Android.launchBilling === 'function') {
                    try {
                        window.Android.launchBilling(productId);
                    } catch(e) {
                        showToast('Google Play baÅŸlatÄ±lamadÄ±. LÃ¼tfen tekrar deneyin.');
                        console.error('[IAP] launchBilling hatasÄ±:', e);
                    }
                    return;
                } else {
                    // window.Android var ama launchBilling metodu yok â†’ eski uygulama sÃ¼rÃ¼mÃ¼
                    showToast("âš ï¸ Uygulama gÃ¼ncel deÄŸil. LÃ¼tfen Google Play'den gÃ¼ncelleyin.");
                    console.warn('[IAP] window.Android mevcut ama launchBilling metodu yok.');
                    return;
                }
            }

            // iOS WKWebView kÃ¶prÃ¼sÃ¼ (gelecekteki iOS desteÄŸi iÃ§in)
            if (window.webkit && window.webkit.messageHandlers && window.webkit.messageHandlers.billing) {
                try {
                    window.webkit.messageHandlers.billing.postMessage({ productId });
                } catch(e) {
                    showToast('In-app satÄ±n alÄ±m baÅŸlatÄ±lamadÄ±.');
                }
                return;
            }

            // TarayÄ±cÄ± / web ortamÄ± â†’ admin'e satÄ±n alma talebi gÃ¶nder
            await _sendWebPurchaseRequest(productId);
        }

        // â”€â”€ Ãœyelik YÃ¼kseltme â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
        async function requestUpgrade() {
            const sel = document.getElementById("upgrade-tier-select");
            if (!sel) { showToast('âš ï¸ YÃ¼kseltme seÃ§ici bulunamadÄ±.'); return; }
            const productId = sel.value;
            if (!productId) { showToast('âš ï¸ LÃ¼tfen bir paket seÃ§in.'); return; }

            if (typeof window.Android !== 'undefined' && window.Android !== null) {
                if (typeof window.Android.launchBilling === 'function') {
                    try {
                        window.Android.launchBilling(productId);
                    } catch(e) {
                        showToast('Google Play baÅŸlatÄ±lamadÄ±. LÃ¼tfen tekrar deneyin.');
                        console.error('[IAP] launchBilling hatasÄ±:', e);
                    }
                    return;
                } else {
                    showToast("âš ï¸ Uygulama gÃ¼ncel deÄŸil. LÃ¼tfen Google Play'den gÃ¼ncelleyin.");
                    return;
                }
            }
            if (window.webkit && window.webkit.messageHandlers && window.webkit.messageHandlers.billing) {
                try { window.webkit.messageHandlers.billing.postMessage({ productId }); } catch(e) { showToast('In-app satÄ±n alÄ±m baÅŸlatÄ±lamadÄ±.'); }
                return;
            }
            // TarayÄ±cÄ± / web ortamÄ± â†’ admin'e satÄ±n alma talebi gÃ¶nder
            await _sendWebPurchaseRequest(productId);
        }

        // Android uygulamasÄ± satÄ±n alÄ±m tamamlandÄ±ÄŸÄ±nda bu fonksiyonu Ã§aÄŸÄ±rÄ±r.
        // Android kodu: webView.evaluateJavascript("verifyGooglePurchase(...)", null);
        async function verifyGooglePurchase(purchaseToken, productId, purchaseType) {
            try {
                showToast('Ã–deme doÄŸrulanÄ±yor...');
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
                    showToast('âœ… AboneliÄŸin aktive edildi! HoÅŸ geldin.');
                    // KullanÄ±cÄ± verilerini yenile
                    await loadMyData();
                    renderProfile();
                } else {
                    showToast('âš ï¸ DoÄŸrulama hatasÄ±: ' + (json.message || 'Bilinmeyen hata'));
                }
            } catch(e) {
                showToast('AÄŸ hatasÄ± oluÅŸtu, lÃ¼tfen tekrar deneyin.');
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
            let adminTag = (u.role === 'Admin') ? '<span class="ml-2 bg-red-600 text-white px-2 py-0.5 rounded text-[9px] uppercase font-bold tracking-widest shadow-[0_0_10px_red]">ğŸ‘‘ YÃ¶netici</span>' : (u.role === 'SubAdmin' ? '<span class="ml-2 bg-orange-800 text-orange-200 px-2 py-0.5 rounded text-[9px] uppercase font-bold tracking-widest">ğŸ›¡ï¸ Yrd. Admin</span>' : '');

            document.getElementById("op-avatar").src = u.avatar || `https://cdn.freeridertr.com.tr/profil%20resmi/unnamed.jpg`; 
            document.getElementById("op-avatar").className = `w-28 h-28 mx-auto rounded-full object-cover mt-6 bg-zinc-950 shadow-xl border-4 transition-all duration-300 ${borderCls}`;
            
            const badge = document.getElementById("op-premium-badge");
            if(premTier === 3) { 
                badge.classList.remove("hidden"); 
                badge.className = `mt-3 text-[10px] font-black uppercase tracking-widest text-yellow-500 drop-shadow-sm`; 
                badge.textContent = "ğŸ‘‘ Ultra+"; 
            } else if (premTier === 2) { 
                badge.classList.remove("hidden"); 
                badge.className = `mt-3 text-[10px] font-bold uppercase tracking-widest text-purple-400 drop-shadow-sm`; 
                badge.textContent = "ğŸŒŸ Deluxe"; 
            } else if (premTier === 1) { 
                badge.classList.remove("hidden"); 
                badge.className = `mt-3 text-[10px] font-bold uppercase tracking-widest drop-shadow-sm ${textCls}`; 
                badge.textContent = "â­ Standart"; 
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
            
            document.getElementById("op-bio").textContent = u.bio || "KullanÄ±cÄ± biyo girmemiÅŸ."; 
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
            if(stats.markers >= 1){ badges += `<span class="bg-zinc-800 text-zinc-300 border border-zinc-700 px-3 py-1 rounded-lg text-[10px] font-bold shadow-sm">ğŸ“ KÃ¢ÅŸif</span>`; }
            if(stats.events >= 1){ badges += `<span class="bg-zinc-800 text-zinc-300 border border-zinc-700 px-3 py-1 rounded-lg text-[10px] font-bold shadow-sm">ğŸ“… OrganizatÃ¶r</span>`; }
            if(stats.market >= 1){ badges += `<span class="bg-zinc-800 text-zinc-300 border border-zinc-700 px-3 py-1 rounded-lg text-[10px] font-bold shadow-sm">ğŸ¤ Esnaf</span>`; }
            if(u.xp > 1000){ badges += `<span class="bg-orange-900/50 text-orange-300 border border-orange-700 px-3 py-1 rounded-lg text-[10px] font-bold shadow-sm">ğŸ”¥ KÄ±demli</span>`; }
            
            if(badges === "") {
                badges = "<span class='text-zinc-500 text-xs italic font-medium'>Rozet yok.</span>";
            }
            document.getElementById("op-badges").innerHTML = badges;

            renderGarage(u.username, 'other');

            let actionsHtml = `<button onclick="startDm('${u.username}')" class="bg-white hover:bg-gray-200 transition text-black py-4 rounded-xl text-sm font-bold w-full shadow-[0_0_15px_rgba(255,255,255,0.3)] mb-3 btn-premium-hover">ğŸ’¬ Ã–ZEL MESAJ</button>`;
            
            // Engel durumunu kontrol et
            const myBlockedList = (currentUser.stats && currentUser.stats.blocked_users) ? currentUser.stats.blocked_users : [];
            const isBlocked = myBlockedList.includes(u.username);
            if(isBlocked) {
                actionsHtml += `<button onclick="unblockUser('${u.username}')" class="w-full bg-zinc-900 border border-zinc-700 hover:bg-zinc-800 transition text-zinc-400 py-3 rounded-xl font-bold text-xs uppercase tracking-widest mb-3 btn-premium-hover">âœ… ENGELÄ° KALDIR</button>`;
            } else {
                actionsHtml += `<button onclick="blockUser('${u.username}')" class="w-full bg-black border border-sky-900/50 hover:bg-red-950/30 transition text-sky-400 py-3 rounded-xl font-bold text-xs uppercase tracking-widest mb-2 btn-premium-hover">ğŸš« ENGELLE</button>`;
            }
            actionsHtml += `<button onclick="openReportUserModal('${u.username}')" class="w-full bg-black border border-orange-900/50 hover:bg-orange-950/20 transition text-orange-400 py-3 rounded-xl font-bold text-xs uppercase tracking-widest mb-3 btn-premium-hover">ğŸš¨ ÅÄ°KAYET ET</button>`;
            
            if(currentUser.role === 'Admin' || currentUser.username === 'Admin' || currentUser.username.toLowerCase() === 'admin') {
                actionsHtml += `
                <div class="rounded-2xl p-4 border border-zinc-700/60 mb-3" style="background:rgba(0,0,0,0.5)">
                    <div class="text-[10px] text-zinc-400 uppercase font-bold tracking-widest mb-3">ğŸ‘‘ Ana Admin â€” YÃ¶netim</div>
                    <div class="flex gap-2 mb-3">
                        <select id="admin-tier-select" class="flex-1 bg-zinc-900 border border-zinc-600 rounded-lg px-3 py-2 text-white text-xs outline-none cursor-pointer font-bold">
                            <option value="0" ${stats.premium_tier == 0 ? 'selected' : ''}>Ãœcretsiz (Ä°ptal)</option>
                            <option value="1" ${stats.premium_tier == 1 ? 'selected' : ''}>â­ Standart</option>
                            <option value="2" ${stats.premium_tier == 2 ? 'selected' : ''}>ğŸŒŸ Deluxe</option>
                            <option value="3" ${stats.premium_tier == 3 ? 'selected' : ''}>ğŸ‘‘ Ultra+</option>
                        </select>
                        <button onclick="adminSetPremium('${u.username}')" class="bg-gradient-to-r from-purple-700 to-pink-700 hover:opacity-90 text-white py-2 px-4 rounded-lg text-[10px] font-bold transition uppercase tracking-widest btn-premium-hover">KAYDET</button>
                    </div>
                    <div class="flex gap-2 mb-3">
                        <input id="admin-xp-amount" type="number" placeholder="XP miktarÄ±" class="w-1/2 bg-black/60 text-white rounded-xl px-4 py-3 text-sm border border-zinc-700 outline-none focus:border-white transition font-bold">
                        <button onclick="giveXP('${u.username}')" class="w-1/2 bg-zinc-800 hover:bg-zinc-700 transition text-white py-3 rounded-xl text-xs font-bold uppercase tracking-widest btn-premium-hover">XP VER</button>
                    </div>
                    <div class="grid grid-cols-2 gap-2">
                        <button onclick="openUserActivity('${u.username}')" class="bg-blue-950/50 hover:bg-blue-900/60 transition text-blue-400 py-3 rounded-xl text-xs font-bold uppercase tracking-widest border border-blue-800/50 btn-premium-hover">ğŸ” Aktivite</button>
                        <button onclick="banUser('${u.username}')" class="bg-red-950/50 hover:bg-sky-900/80 transition text-sky-400 py-3 rounded-xl text-xs font-bold uppercase tracking-widest border border-sky-800/50 btn-premium-hover">ğŸš¨ Banla</button>
                    </div>
                </div>`;
            } else if(currentUser.role === 'SubAdmin') {
                actionsHtml += `
                <div class="rounded-2xl p-4 border border-orange-900/40 mb-3" style="background:rgba(120,53,15,0.12)">
                    <div class="text-[10px] text-orange-400 uppercase font-bold tracking-widest mb-3">ğŸ›¡ï¸ Yrd. Admin Ä°ÅŸlemleri</div>
                    <div class="grid grid-cols-2 gap-2">
                        <button onclick="openUserActivity('${u.username}')" class="bg-blue-950/50 hover:bg-blue-900/60 transition text-blue-400 py-3 rounded-xl text-xs font-bold uppercase tracking-widest border border-blue-800/50 btn-premium-hover">ğŸ” Aktivite</button>
                        <button onclick="banUser('${u.username}')" class="bg-red-950/50 hover:bg-sky-900/80 transition text-sky-400 py-3 rounded-xl text-xs font-bold uppercase tracking-widest border border-sky-800/50 btn-premium-hover">ğŸš¨ Banla</button>
                    </div>
                </div>`;
            }
            
            document.getElementById("op-actions").innerHTML = actionsHtml;

            // â”€â”€ Profil Reels Sekmesi â”€â”€
            // op-actions altÄ±na reels tab ekle (varsa Ã¶nce temizle)
            const existingReelsTab = document.getElementById('op-reels-section');
            if(existingReelsTab) existingReelsTab.remove();
            const reelsSection = document.createElement('div');
            reelsSection.id = 'op-reels-section';
            reelsSection.className = 'mt-4';
            reelsSection.innerHTML = `
                <div class="flex items-center gap-2 mb-3">
                    <button id="op-reels-tab-btn" onclick="window.loadOtherProfileReels('${escapeHtml(u.username)}')"
                        class="flex-1 flex items-center justify-center gap-2 py-2.5 rounded-xl bg-gradient-to-r from-pink-900/60 to-sky-900/40 border border-pink-700/40 text-white text-xs font-black uppercase tracking-widest hover:opacity-90 transition btn-premium-hover">
                        ğŸ¬ Reels'leri GÃ¶r
                    </button>
                </div>
                <div id="op-reels-grid" class="hidden grid grid-cols-3 gap-1 rounded-xl overflow-hidden"></div>
                <div id="op-reels-loading" class="hidden flex items-center justify-center py-6">
                    <div class="w-6 h-6 rounded-full border-2 border-pink-500 border-t-transparent animate-spin"></div>
                </div>
                <div id="op-reels-empty" class="hidden text-center text-zinc-500 text-xs py-4">Bu kullanÄ±cÄ±nÄ±n henÃ¼z Reels paylaÅŸÄ±mÄ± yok.</div>
            `;
            const opActionsEl = document.getElementById('op-actions');
            if(opActionsEl && opActionsEl.parentNode) {
                opActionsEl.parentNode.insertBefore(reelsSection, opActionsEl.nextSibling);
            }

            document.getElementById("other-profile-modal").classList.remove("hidden");
        }

        // â”€â”€ DiÄŸer KullanÄ±cÄ±nÄ±n Reels'lerini YÃ¼kle â”€â”€
        window.loadOtherProfileReels = async function(profileUsername) {
            const grid    = document.getElementById('op-reels-grid');
            const loading = document.getElementById('op-reels-loading');
            const empty   = document.getElementById('op-reels-empty');
            const tabBtn  = document.getElementById('op-reels-tab-btn');
            if(!grid) return;

            // Butonu gizle, loading gÃ¶ster
            if(tabBtn) tabBtn.style.display = 'none';
            if(loading) { loading.classList.remove('hidden'); loading.style.display = 'flex'; }
            if(empty) empty.classList.add('hidden');
            grid.classList.add('hidden');
            grid.innerHTML = '';

            try {
                // Supabase'den doÄŸrudan sorgula
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
                            <div style="position:absolute;bottom:4px;left:4px;font-size:10px;color:rgba(255,255,255,0.8);font-weight:bold;">â¤ ${(r.likes||[]).length}</div>`;
                    } else {
                        item.innerHTML = `
                            <img src="${escapeHtml(r.media_url)}" class="w-full h-full object-cover" loading="lazy" onerror="this.parentElement.innerHTML='<div style=\'width:100%;height:100%;display:flex;align-items:center;justify-content:center;font-size:24px;color:#555\'>ğŸ“¸</div>'">
                            <div style="position:absolute;bottom:4px;left:4px;font-size:10px;color:rgba(255,255,255,0.8);font-weight:bold;">â¤ ${(r.likes||[]).length}</div>`;
                    }

                    // TÄ±klayÄ±nca Reels sayfasÄ±na Ä±ÅŸÄ±n â€” direkt o videodan baÅŸlat
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
                console.error('Profil reels yÃ¼kleme hatasÄ±:', err);
            }
        };

        async function adminSetPremium(target) {
            const tier = document.getElementById("admin-tier-select").value;
            await sendAction('admin_toggle_premium', { username: target, tier: tier });
            alert("Abonelik baÅŸarÄ±yla gÃ¼ncellendi!");
            document.getElementById("other-profile-modal").classList.add("hidden");
        }

        async function giveXP(u) { 
            const a = document.getElementById("admin-xp-amount").value; 
            if(!a) return; 
            
            await sendAction('give_xp', { username: u, amount: a }); 
            alert("XP BaÅŸarÄ±yla Eklendi!"); 
            document.getElementById("other-profile-modal").classList.add("hidden"); 
        }
        
        async function banUser(u) { 
            if(confirm("Bu kullanÄ±cÄ±yÄ± kalÄ±cÄ± olarak banlamak istediÄŸinize emin misiniz?")) { 
                await sendAction('add_ban', { username: u });
                db.banned.push(u);
            } 
        }

        async function blockUser(target) {
            if(!confirm(`${target} adlÄ± kullanÄ±cÄ±yÄ± engellemek istediÄŸine emin misin? Engellenince seni gÃ¶remez ve sana mesaj gÃ¶nderemez.`)) return;
            const res = await sendAction('block_user', { target });
            if(res && res.status === 'ok') {
                if(!currentUser.stats) currentUser.stats = {};
                if(!currentUser.stats.blocked_users) currentUser.stats.blocked_users = [];
                if(!currentUser.stats.blocked_users.includes(target)) currentUser.stats.blocked_users.push(target);
                document.getElementById('other-profile-modal').classList.add('hidden');
                showToast(`ğŸš« ${target} engellendi.`);
            } else {
                alert(res?.message || 'Bir hata oluÅŸtu.');
            }
        }

        async function unblockUser(target) {
            const res = await sendAction('unblock_user', { target });
            if(res && res.status === 'ok') {
                if(currentUser.stats && currentUser.stats.blocked_users) {
                    currentUser.stats.blocked_users = currentUser.stats.blocked_users.filter(u => u !== target);
                }
                document.getElementById('other-profile-modal').classList.add('hidden');
                showToast(`âœ… ${target} engeli kaldÄ±rÄ±ldÄ±.`);
            } else {
                alert(res?.message || 'Bir hata oluÅŸtu.');
            }
        }

        function openDeleteAccountModal() {
            document.getElementById('settings-modal').classList.add('hidden');
            document.getElementById('delete-account-password').value = '';
            document.getElementById('delete-account-modal').classList.remove('hidden');
        }

        async function confirmDeleteAccount() {
            const pw = document.getElementById('delete-account-password').value.trim();
            if(!pw) { alert('LÃ¼tfen ÅŸifreni gir.'); return; }
            if(!confirm('Son onay: HesabÄ±n ve TÃœM verilerin kalÄ±cÄ± olarak silinecek. Devam etmek istiyor musun?')) return;
            const res = await sendAction('delete_account', { password: pw });
            if(res && res.status === 'ok') {
                alert('HesabÄ±n baÅŸarÄ±yla silindi. GÃ¶rÃ¼ÅŸmek Ã¼zere! ğŸ”ï¸');
                window.location.reload();
            } else {
                alert(res?.message || 'Bir hata oluÅŸtu.');
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
            if(!reason) { alert('LÃ¼tfen bir ÅŸikayet sebebi seÃ§in.'); return; }
            const res = await sendAction('report_user', { target: _reportUserTarget, reason });
            document.getElementById('report-user-modal').classList.add('hidden');
            if(res && res.status === 'ok') {
                showToast('Åikayetiniz admin ekibine iletildi. TeÅŸekkÃ¼rler!');
            } else {
                alert(res?.message || 'Bir hata oluÅŸtu.');
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
            document.getElementById('report-msg-preview').textContent = _reportMsgText || '(Mesaj iÃ§eriÄŸi)';
            document.getElementById('report-msg-modal').classList.remove('hidden');
        }

        function setMsgReportReason(reason) {
            _reportMsgReason = reason;
            document.querySelectorAll('#report-msg-modal .grid button').forEach(b => {
                b.classList.toggle('border-orange-500', b.textContent.trim().includes(reason.split('/')[0].trim()));
            });
        }

        async function submitReportMsg() {
            if(!_reportMsgReason) { alert('LÃ¼tfen bir ÅŸikayet sebebi seÃ§in.'); return; }
            document.getElementById('report-msg-modal').classList.add('hidden');
            try {
                // sendAction Ã¼zerinden /api/data'ya gÃ¶nder â€” session yÃ¶netimi gÃ¼venilir
                const data = await sendAction('report_message', {
                    msg_id:   String(_reportMsgId),
                    msg_text: String(_reportMsgText),
                    msg_user: String(_reportMsgUser),
                    reason:   String(_reportMsgReason)
                }, true);
                if (data && data.status === 'ok') {
                    // Local state'i gÃ¼ncelle â€” sayfa yenilenmeden flag badge gÃ¶rÃ¼nsÃ¼n
                    const localMsg = db.messages.find(m => m.id === String(_reportMsgId));

                    if (data.message && typeof showToast === 'function') {
                        showToast(data.message);
                    }

                    if (data.should_remove) {
                        // flag_count >= 2 â€” mesaj otomatik silindi, local'den de kaldÄ±r
                        db.messages = db.messages.filter(m => m.id !== String(_reportMsgId));
                        _renderedMsgIds.delete(String(_reportMsgId));
                    } else if (localMsg && data.is_flagged === true) {
                        localMsg.is_flagged = true;
                        localMsg.flag_count = data.flag_count || (localMsg.flag_count || 0) + 1;
                    }
                    renderChat(true); // TÃ¼m mesajlarÄ± yeniden Ã§iz (flag badge dahil)

                    // AI moderasyon uyarÄ±sÄ± varsa sohbete ekle
                    if (data.warning && data.ai_chat_msg) {
                        try {
                            db.messages.push(data.ai_chat_msg);
                            const container = document.getElementById('chat-messages');
                            if (container) {
                                const msgHtml = buildMsgHTML(data.ai_chat_msg);
                                container.insertAdjacentHTML('beforeend', msgHtml);
                                container.scrollTo({ top: container.scrollHeight, behavior: 'smooth' });
                            }
                        } catch(e) { console.warn('[Moderasyon] AI mesaj ekleme hatasÄ±:', e); }
                    }

                    if (data.should_remove) {
                        showToast('ğŸš« Mesaj Ã§ok fazla ÅŸikayet aldÄ± ve otomatik kaldÄ±rÄ±ldÄ±.', 'error', 4000);
                    } else if (data.warning) {
                        showToast('âš ï¸ Ä°Ã§erik uygunsuz bulundu ve admin ekibine iletildi!', 'warning');
                    } else {
                        showToast('âœ… Mesaj moderasyon ekibine iletildi. TeÅŸekkÃ¼rler!', 'success');
                    }
                } else {
                    showToast('âŒ Bildirim gÃ¶nderilemedi: ' + (data?.message || 'Hata'), 'error');
                }
            } catch(err) {
                console.error('[Moderasyon] Hata:', err);
                showToast('âŒ BaÄŸlantÄ± hatasÄ±. Tekrar deneyin.');
            }
        }

        // Sohbet ekranÄ±na Freerider AI moderatÃ¶r mesajÄ± ekler
        function injectModerationSystemMessage(senderUsername, systemMsg) {
            const container = document.getElementById('chat-messages') || document.getElementById('dm-messages');
            if (!container) return;
            const aiMsg = {
                id: String(Date.now()) + '_mod',
                user: 'Freerider AI',
                text: 'ğŸ›¡ï¸ ' + senderUsername + ', mesajÄ±n topluluk kurallarÄ±na aykÄ±rÄ± bulundu ve admin ekibine bildirildi. LÃ¼tfen kurallara uygun davranÄ±n. Tekrarlayan ihlaller hesabÄ±nÄ±zÄ±n askÄ±ya alÄ±nmasÄ±na neden olabilir.',
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
                btn.innerHTML = "âŒ Haritadan SeÃ§"; 
                mapContainer.classList.add("map-add-mode"); 
            } else { 
                btn.className = "bg-sky-600/90 backdrop-blur hover:bg-red-500 btn-premium-hover transition px-3 py-2 rounded-xl shadow-[0_0_15px_rgba(14,165,233,0.4)] font-bold text-white text-[10px] uppercase tracking-widest border border-red-400/50 pointer-events-auto"; 
                btn.innerHTML = "ğŸ“ RAMPA EKLE"; 
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
                btn.innerHTML = "âŒ Haritadan SeÃ§"; 
                mapContainer.classList.add("map-add-mode"); 
            } else { 
                btn.className = "bg-blue-600/90 backdrop-blur hover:bg-blue-500 btn-premium-hover transition px-3 py-2 rounded-xl shadow-[0_0_15px_rgba(59,130,246,0.4)] flex items-center justify-center text-[10px] uppercase tracking-widest font-bold text-white border border-blue-400/50 pointer-events-auto"; 
                btn.innerHTML = "ğŸ“… BULUÅMA EKLE"; 
                mapContainer.classList.remove("map-add-mode"); 
            } 
        }

        function useCurrentLocationForMarker() {
            if(!userLat || !userLng) {
                return alert("Konumunuz bulunamadÄ±! LÃ¼tfen haritadaki GPS (ğŸ¯) butonuna tÄ±klayÄ±p konum izni verin.");
            }
            tempLat = userLat;
            tempLng = userLng;
            editingMarkerId = null;
            document.getElementById("modal-marker-title").textContent = "ğŸ“ " + selectedMarkerCategory.toUpperCase() + " EKLE (Åu Anki Konum)";
            showToast("Åu anki konumunuz baÅŸarÄ±yla alÄ±ndÄ±! DetaylarÄ± girip kaydedebilirsiniz.");
        }

        function quickAddMarkerCurrentLocation() {
            if(!userLat || !userLng) {
                return alert("Konumunuz bulunamadÄ±! LÃ¼tfen haritadaki GPS (ğŸ¯) butonuna tÄ±klayÄ±p konum izni verin.");
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
            
            document.getElementById("modal-marker-title").textContent = "âœï¸ RAMPA DÃœZENLE";
            document.getElementById("new-marker-name").value = m.name || "";
            document.getElementById("new-marker-desc").value = m.desc || "";
            document.getElementById("new-marker-difficulty").value = m.difficulty || "Orta";
            document.getElementById("new-marker-photo").value = ""; 
            
            if(getUserPremiumTier(currentUser.username) >= 2 || currentUser.role === 'Admin') {
                document.getElementById("new-marker-icon").classList.remove("hidden");
                document.getElementById("new-marker-icon").value = m.icon_type || "ğŸš´";
            }
            
            closeMarkerSheet();
            document.getElementById("add-marker-modal").classList.remove("hidden");
        }
        
        async function deleteMarker(id) {
            if(confirm("Bu noktayÄ± haritadan kalÄ±cÄ± olarak silmek istediÄŸine emin misin?")) {
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
            document.getElementById("ms-desc").textContent = m.desc || "AÃ§Ä±klama yok.";
            
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
                if(m.is_dangerous && dr.length > 0) { dangerBanner.classList.remove('hidden'); dangerBanner.innerHTML = 'âš ï¸ ' + dr[dr.length-1].reason; }
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
                alert("LÃ¼tfen Ã¶nce harita Ã¼zerinden bir noktaya dokunarak yer seÃ§in!"); 
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
                'BisikletÃ§i': '<i data-lucide="wrench" class="w-4 h-4"></i>',
                'Market': '<i data-lucide="shopping-cart" class="w-4 h-4"></i>',
                'Trail': '<i data-lucide="map" class="w-4 h-4"></i>',
                'Drop': '<i data-lucide="arrow-down-to-line" class="w-4 h-4"></i>',
                'Dirt Jump': '<i data-lucide="zap" class="w-4 h-4"></i>',
                'Tamir NoktasÄ±': '<i data-lucide="hammer" class="w-4 h-4"></i>',
                'Su KaynaÄŸÄ±': '<i data-lucide="droplet" class="w-4 h-4"></i>',
                'Toplanma NoktasÄ±': '<i data-lucide="map-pin" class="w-4 h-4"></i>',
                'Tehlikeli BÃ¶lge': '<i data-lucide="triangle-alert" class="w-4 h-4"></i>'
            };
            
            const catColors = {
                'Rampa': 'from-sky-500 to-sky-800 shadow-sky-500',
                'BisikletÃ§i': 'from-orange-500 to-orange-800 shadow-orange-500',
                'Market': 'from-green-500 to-green-800 shadow-green-500',
                'Trail': 'from-emerald-500 to-emerald-800 shadow-emerald-500',
                'Drop': 'from-purple-500 to-purple-800 shadow-purple-500',
                'Dirt Jump': 'from-yellow-500 to-yellow-800 shadow-yellow-500',
                'Tamir NoktasÄ±': 'from-blue-500 to-blue-800 shadow-blue-500',
                'Su KaynaÄŸÄ±': 'from-cyan-500 to-cyan-800 shadow-cyan-500',
                'Toplanma NoktasÄ±': 'from-pink-500 to-pink-800 shadow-pink-500',
                'Tehlikeli BÃ¶lge': 'from-red-500 to-red-800 shadow-red-500'
            };

            const markersToAdd = [];
            
            db.markers.forEach(m => {
                const cat = m.category || m.icon_type || 'Rampa';
                if(activeMarkerFilter !== 'TÃ¼mÃ¼' && activeMarkerFilter !== cat) return;
                
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
                    html: `<div class="bg-gradient-to-b from-blue-500 to-blue-700 text-white w-10 h-10 rounded-full flex items-center justify-center border-2 border-white shadow-[0_0_15px_rgba(59,130,246,0.6)] font-bold text-lg cursor-pointer transition hover:scale-110">ğŸ“…</div>`, 
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
                        crownHtml = `<div class="absolute -top-3 text-sm drop-shadow-[0_0_10px_rgba(234,179,8,0.8)] z-20 animate-bounce">ğŸ‘‘</div>`; 
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
            if(!userLat || !userLng) return alert("Mevcut konumunuz henÃ¼z bulunamadÄ±! LÃ¼tfen haritadaki GPS (ğŸ¯) butonuna tÄ±klayÄ±p konum izni verin.");
            
            const c = document.getElementById("nr-list");
            c.innerHTML = "";
            
            let withDist = db.markers.map(m => {
                let dLat = m.lat - userLat;
                let dLng = m.lng - userLng;
                let dist = Math.sqrt(dLat*dLat + dLng*dLng) * 111;
                return {...m, distance: dist};
            }).sort((a,b) => a.distance - b.distance);
            
            if(withDist.length === 0) {
                c.innerHTML = "<p class='text-zinc-500 text-xs italic text-center mt-5 font-medium'>Ã‡evrenizde kayÄ±tlÄ± rampa veya rota bulunamadÄ±.</p>";
            } else {
                withDist.slice(0, 10).forEach(m => {
                    let img = m.image ? `<img src="${m.image}" class="w-16 h-16 rounded-xl object-cover shrink-0 border border-zinc-700 shadow-sm">` : `<div class="w-16 h-16 rounded-xl bg-black/60 border border-zinc-700 shadow-inner flex items-center justify-center text-2xl shrink-0">${m.icon_type || 'ğŸš´'}</div>`;
                    c.innerHTML += `
                    <div class="bg-black/50 p-3 rounded-2xl border border-zinc-800 flex items-center gap-3 mb-3 cursor-pointer hover:bg-zinc-800 hover:border-zinc-600 transition-colors shadow-md group" onclick="map.setView([${m.lat}, ${m.lng}], 16); document.getElementById('nearby-routes-modal').classList.add('hidden');">
                        ${img}
                        <div class="overflow-hidden flex-1">
                            <div class="text-white font-bold text-sm tracking-wide truncate group-hover:text-blue-300 transition-colors">${m.name}</div>
                            <div class="text-sky-400 text-[10px] font-black uppercase tracking-widest mt-1">${m.distance.toFixed(1)} KM UZAKLIKTA</div>
                            <div class="text-zinc-500 text-[10px] font-bold uppercase tracking-widest mt-0.5">Seviye: ${m.difficulty}</div>
                        </div>
                        <div class="text-zinc-400 bg-zinc-900 border border-zinc-700 w-8 h-8 rounded-full flex items-center justify-center shrink-0 group-hover:bg-zinc-700 group-hover:text-white transition-colors">âœ</div>
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
                showToast("ğŸ“ BaÅŸlÄ±k zorunludur!");
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
                    showToast("âœ… " + (editingMarkerId ? "Nokta gÃ¼ncellendi!" : "Nokta eklendi!"));
                    markerCache.clear();
                    loadMarkersByViewport();
                } else {
                    showToast(res?.message || "âŒ Hata oluÅŸtu");
                }
                
                editingMarkerId = null;
                tempLat = null;
                tempLng = null;
                document.getElementById("new-marker-name").value = "";
                document.getElementById("new-marker-desc").value = "";
                document.getElementById("new-marker-extranote").value = "";
                document.getElementById("new-marker-photo").value = "";
                document.getElementById("modal-marker-title").textContent = "ğŸ“ NOKTA EKLE";
                document.getElementById("modal-marker-category-label").textContent = "";
            } catch(e) {
                console.error(e);
                showToast("âŒ AÄŸ hatasÄ±.");
            }
        }

        
        async function saveEvent() { 
            const t = document.getElementById("ev-title").value; 
            const d = document.getElementById("ev-date").value; 
            const tm = document.getElementById("ev-time").value; 
            
            if(!t || !d || !tm) return alert("TÃ¼m alanlarÄ± doldurunuz!");
            
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
            document.getElementById("es-desc").textContent = e.desc || "AÃ§Ä±klama yok."; 
            
            const att = e.attendees || []; 
            
            const attContainer = document.getElementById("es-attendees");
            attContainer.innerHTML = "";
            if (att.length === 0) {
                attContainer.innerHTML = "<span class='text-zinc-500 text-xs italic font-medium'>HenÃ¼z katÄ±lan yok. Ä°lk sen ol!</span>";
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
                    btn.textContent = `KAPASÄ°TE DOLU (${att.length}/${maxCapacity})`;
                    btn.className = "w-full bg-black/50 text-zinc-500 py-4 rounded-xl font-bold text-sm cursor-not-allowed mb-2 border border-zinc-700 shadow-inner";
                    btn.disabled = true;
                } else {
                    let limitText = maxCapacity > 0 ? `KATIL (${att.length}/${maxCapacity} KiÅŸi)` : `KATIL (${att.length} KiÅŸi)`;
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
                    alert("Bu etkinliÄŸin kapasitesi maalesef dolmuÅŸ!");
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
            if(confirm("Bu etkinliÄŸi silmek istediÄŸinize emin misiniz?")) {
                await sendAction('delete_event', {id: currentEventId});
                db.events = db.events.filter(e => e.id !== currentEventId);
                document.getElementById("event-sheet").classList.add("hidden");
            }
        }

        // Bildirim badge fonksiyonlarÄ±
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
                const isAI = msg.user === 'Freerider AI' || msg.user === 'ModeratÃ¶r AI';
                
                const premColor = getUserPremiumColor(msg.user); 
                const premTier = getUserPremiumTier(msg.user); 
                
                const textCls = (premTier > 0) ? getPremiumTextClass(premColor) : '';
                const inlineStyle = (premTier > 0) ? getPremiumInlineStyle(premColor) : '';
                const borderCls = (premTier > 0 && !isAI) ? getPremiumBorderClass(msg.user) : 'border-zinc-700';
                
                const isAdmin = msg.user === 'Admin' || (db.users.find(u => u.username === msg.user) && db.users.find(u => u.username === msg.user).role === 'Admin');
                const adminDel = (currentUser.role === 'Admin' || currentUser.role === 'SubAdmin' || isMe) ? `<button onclick="delMsg('${msg.id}')" class="text-[10px] bg-red-950/80 text-sky-300 px-2 py-1 rounded-lg ml-2 hover:bg-red-900 transition border border-sky-900/50 uppercase font-bold tracking-widest relative z-50 pointer-events-auto">SÄ°L</button>` : '';
                const _encId = btoa(encodeURIComponent(msg.id)); const _encUser = btoa(encodeURIComponent(msg.user)); const _encText = btoa(encodeURIComponent((msg.text||'').substring(0,80)));
                const reportBtn = (!isMe && !isAI) ? `<button onclick="openReportMsgModal('${_encId}','${_encUser}','${_encText}')" class="text-[10px] bg-orange-950/60 text-orange-400 px-2 py-1 rounded-lg ml-1 hover:bg-orange-900/60 transition border border-orange-900/50 uppercase font-bold tracking-widest relative z-50 pointer-events-auto">ğŸš¨</button>` : '';
                
                const pinBtn = (isMe && getUserPremiumTier(currentUser.username) === 3 && msg.type === "text") ? `<button onclick="pinMsg('${msg.id}')" class="text-[10px] bg-yellow-900/50 text-yellow-500 px-2 py-1 rounded-lg ml-2 hover:bg-yellow-900 transition border border-yellow-700/50 uppercase font-bold tracking-widest relative z-50 pointer-events-auto">SABÄ°TLE</button>` : '';

                // Flag gÃ¶stergesi (DB'den gelen is_flagged + flag_count)
                const flagBadge = msg.is_flagged ? `<span class="text-[9px] bg-red-950/60 text-red-400 px-2 py-0.5 rounded-lg ml-1 border border-red-900/50 uppercase font-bold tracking-widest animate-pulse">ğŸš© ${msg.flag_count || 1}x</span>` : '';

                let tick = (premTier === 3) ? verifiedTick : ''; 
                let adminTag = isAdmin ? `<span class="ml-2 bg-red-600 text-white px-2 py-0.5 rounded text-[9px] tracking-widest uppercase shadow-[0_0_10px_red]">ğŸ‘‘ YÃ¶netici</span>` : '';
                let aiTag = isAI ? `<span class="ml-2 bg-cyan-500/20 border border-cyan-500/50 text-cyan-400 px-2 py-0.5 rounded-lg text-[9px] font-black tracking-widest uppercase shadow-[0_0_15px_rgba(6,182,212,0.4)] animate-pulse">ğŸ¤– YAPAY ZEKA</span>` : '';
                
                let msgDate = new Date(parseInt(msg.id));
                let timeStr = !isNaN(msgDate.getTime()) ? msgDate.getHours().toString().padStart(2, '0') + ":" + msgDate.getMinutes().toString().padStart(2, '0') : "";
                let timeHtml = `<span class="text-[9px] text-zinc-500 ml-2 font-bold tracking-widest bg-black/50 border border-zinc-800 px-1.5 py-0.5 rounded">${timeStr}</span>`;

                let avatarUrl = isAI ? 'https://cdn-icons-png.flaticon.com/512/4712/4712035.png' : (db.users.find(u => u.username === msg.user)?.avatar || 'https://cdn.freeridertr.com.tr/profil%20resmi/unnamed.jpg');
                let avatarHtml = `<img src="${avatarUrl}" class="w-8 h-8 rounded-full object-cover border shrink-0 ${isMe ? 'ml-2' : 'mr-2'} cursor-pointer hover:scale-110 transition-transform ${borderCls}" onclick="${isAI ? '' : `showOtherProfile('${msg.user}')`}">`;

                let content = ""; 
                let bubbleClass = isMe ? 'bg-white text-black' : 'bg-black/60 border border-zinc-800 text-zinc-300';
                
                if (isAI) {
                    // AI moderatÃ¶r uyarÄ± mesajlarÄ± â€” Ã¶zel kÄ±rmÄ±zÄ± gradient stil
                    const isModMsg = (msg.id && msg.id.endsWith('_mod')) || msg.user === 'ModeratÃ¶r AI';
                    if (isModMsg) {
                        content = `<div class="ai-moderator-msg px-4 py-3 rounded-2xl text-sm break-words mt-1 font-bold leading-relaxed relative overflow-hidden"><span class="relative z-10">ğŸ›¡ï¸ ${escapeHtml(msg.text)}</span></div>`;
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
                        content = `<div onclick="playVoice('${msg.audio}')" class="${bubbleClass} px-5 py-3 rounded-xl flex items-center gap-3 cursor-pointer mt-1 shadow-md hover:scale-105 transition"><span class="text-xl">ğŸ™ï¸</span><span class="font-bold text-xs uppercase tracking-widest">Ses KaydÄ±</span></div>`;
                    } else {
                        content = `<div class="${bubbleClass} px-4 py-2.5 rounded-2xl text-sm break-words mt-1 shadow-md font-medium leading-relaxed">${escapeHtml(msg.text)}</div>`;
                    }
                }
                
                let userDisplay = isAI ? `<span class="${msg.user === 'ModeratÃ¶r AI' ? 'text-red-400' : 'text-cyan-400'} font-black tracking-widest drop-shadow-sm">${msg.user === 'ModeratÃ¶r AI' ? 'ğŸ›¡ï¸ ModeratÃ¶r AI' : 'SÄ°STEM AI'}</span>` : `<span onclick="showOtherProfile('${msg.user}')" style="${inlineStyle}" class="cursor-pointer hover:text-white transition ${textCls ? textCls : 'text-zinc-400'}">${msg.user}</span>`;
                
                // Build reaction bar
                const reactions = msg.reactions || {};
                let reactBar = '<div class="flex flex-wrap gap-1 mt-1">';
                const emojiList = ['ğŸ‘','ğŸ”¥','ğŸ˜‚','ğŸ˜®','â¤ï¸','ğŸ’ª'];
                emojiList.forEach(em => {
                    const users = reactions[em] || [];
                    const iReacted = users.includes(currentUser.username);
                    if(users.length > 0 || true) {
                        reactBar += `<button onclick="addReaction('${msg.id}','${em}')" class="flex items-center gap-0.5 text-xs px-2 py-0.5 rounded-full border transition-all ${iReacted ? 'bg-red-900/40 border-sky-600/60 text-white' : 'bg-black/30 border-zinc-700/50 text-zinc-500 hover:border-zinc-500'}">${em}${users.length > 0 ? `<span class="text-[10px] font-bold">${users.length}</span>` : ''}</button>`;
                    }
                });
                reactBar += '</div>';

                // Ä°hlal durumuna gÃ¶re mesaj gÃ¶rÃ¼nÃ¼mÃ¼
                const flagCount = msg.flag_count || 0;
                const isFlagged = msg.is_flagged && flagCount >= 1 && flagCount < 2;
                const isCollapsed = msg.is_flagged && flagCount >= 2;

                if (isCollapsed) {
                    // flag_count >= 2: tamamen collapse â€” tÄ±klayÄ±nca aÃ§Ä±labilir
                    return `
                    <div class="flex ${isMe ? "justify-end" : "justify-start"} items-start mb-4 w-full ${isMe ? 'slide-in-right' : 'slide-in-left'}">
                        ${!isMe ? avatarHtml : ''}
                        <div class="max-w-[80%] flex flex-col ${isMe ? 'items-end' : 'items-start'}">
                            <div class="flex items-center gap-1 text-[10px] uppercase font-bold tracking-widest mb-1">
                                ${userDisplay} ${tick} ${adminTag} ${flagBadge} ${timeHtml} ${adminDel}
                            </div>
                            <div class="msg-collapsed-wrap" onclick="this.querySelector('.msg-collapsed-content').classList.toggle('show')">
                                <div class="msg-collapsed-bar">ğŸš« Bu mesaj uygunsuz iÃ§erik iÃ§erdiÄŸi iÃ§in gizlendi <span style='font-size:9px;opacity:0.6'>â€” gÃ¶rmek iÃ§in tÄ±kla</span></div>
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
                                <div class="msg-flagged-overlay"><span>ğŸ›¡ï¸ Bu mesaj uygunsuz iÃ§erik iÃ§erdiÄŸi iÃ§in gizlendi</span></div>
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

            // Silinen mesaj var mÄ± kontrol et
            const currentIds = new Set(db.messages.map(m => m.id));
            const hasDeleted = [..._renderedMsgIds].some(id => !currentIds.has(id));

            if (forceRedraw || hasDeleted) {
                // Silme veya zorla yenile - tÃ¼m container'Ä± yeniden Ã§iz
                while(container.firstChild) container.removeChild(container.firstChild);
                _renderedMsgIds.clear();
            }

            // â”€â”€ Empty State â”€â”€
            if (db.messages.length === 0) {
                const emptyEl = document.getElementById('_chat_empty_state_');
                if (!emptyEl) {
                    container.innerHTML = `
                        <div id="_chat_empty_state_" class="flex flex-col items-center justify-center h-full text-center py-16 fade-in-anim">
                            <div style="font-size:48px;margin-bottom:12px;opacity:0.6">ğŸ’¬</div>
                            <div class="text-zinc-400 text-sm font-bold mb-1">HenÃ¼z mesaj yok</div>
                            <div class="text-zinc-600 text-xs">Ä°lk mesajÄ± sen yaz! ğŸ”ï¸</div>
                        </div>`;
                }
                return;
            }

            // Sadece yeni mesajlarÄ± DOM'a ekle
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

            // â”€â”€ Optimistic UI: mesajÄ± anÄ±nda gÃ¶ster â”€â”€
            const optimisticMsg = { id, user: currentUser.username, text: t, type: 'text' };
            db.messages.push(optimisticMsg);
            renderChat();

            try {
                const result = await sendAction('add_message', { id: id, text: t, type: "text" }, true);

                if (result && result.warning) {
                    showToast(`âš ï¸ ${result.warning}`, 'warning', 5000);
                }

                // â”€â”€ Proaktif AI moderasyon sonucu â”€â”€
                if (result && result.ai_flagged) {
                    // MesajÄ± flagged olarak gÃ¼ncelle
                    const localMsg = db.messages.find(m => m.id === id);
                    if (localMsg) {
                        localMsg.is_flagged = true;
                        localMsg.flag_count = 1;
                    }

                    // AI moderatÃ¶r uyarÄ± mesajÄ±nÄ± chat'e ekle
                    if (result.ai_moderation_msg) {
                        db.messages.push(result.ai_moderation_msg);
                    }

                    renderChat(true);

                    if (result.severity === 'high') {
                        showToast('ğŸš« Ä°Ã§eriÄŸiniz topluluk kurallarÄ±nÄ± ihlal ediyor! Admin ekibine bildirildi.', 'error', 5000);
                    } else {
                        showToast('âš ï¸ MesajÄ±nÄ±z uygunsuz iÃ§erik iÃ§eriyor ve iÅŸaretlendi.', 'warning', 4000);
                    }
                }
            } catch(err) {
                // Hata durumunda optimistic mesajÄ± geri al
                db.messages = db.messages.filter(m => m.id !== id);
                renderChat(true);
                // err.message backend'den gelen "Ã‡ok fazla istek gÃ¶nderdiniz" uyarÄ±sÄ± olabilir
                const errMsg = err.message || 'Mesaj gÃ¶nderilemedi. Tekrar deneyin.';
                showToast(`âŒ ${errMsg}`, 'error');
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
                container.innerHTML = "<div class='text-zinc-500 text-xs italic text-center mt-5 font-medium'>HenÃ¼z kimseyle Ã¶zel mesajlaÅŸmadÄ±n.</div>";
                return;
            }

            Array.from(uniqueUsers).forEach(uName => {
                const u = db.users.find(x => x.username === uName);
                const isAI = uName === 'Freerider AI';
                
                let avatar = isAI ? 'https://cdn-icons-png.flaticon.com/512/4712/4712035.png' : (u ? u.avatar : 'https://cdn.freeridertr.com.tr/profil%20resmi/unnamed.jpg');
                
                let premColor = isAI ? '' : getUserPremiumColor(uName);
                let textCls = (getUserPremiumTier(uName) > 0) ? getPremiumTextClass(premColor) : '';
                let inlineStyle = (getUserPremiumTier(uName) > 0) ? getPremiumInlineStyle(premColor) : '';
                let nameHtml = isAI ? `<span class="text-cyan-400 font-black tracking-widest uppercase text-sm drop-shadow-[0_0_10px_cyan] animate-pulse">ğŸ¤– Freerider AI</span>` : `<span style="${inlineStyle}" class="font-bold text-sm tracking-wide ${textCls ? textCls : 'text-white'}">${uName}</span>`;

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
                            ${dmOnline ? `<span class="flex items-center gap-1">${dmOnline}</span>` : `<span class="text-[10px] text-zinc-500 uppercase font-bold tracking-widest truncate">${isAI ? 'Ã–zel AsistanÄ±n' : 'GÃ¶rÃ¼ntÃ¼lemek iÃ§in tÄ±kla'}</span>`}
                        </div>
                    </div>
                    <div class="text-zinc-400 bg-zinc-900 w-8 h-8 rounded-full flex items-center justify-center border border-zinc-700">ğŸ’¬</div>
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
            document.getElementById("dm-thread-name").innerHTML = targetUser === 'Freerider AI' ? '<span class="text-cyan-400 drop-shadow-[0_0_10px_cyan] font-black tracking-widest">ğŸ¤– Freerider AI</span>' : targetUser;

            const container = document.getElementById("dm-messages");
            const isScrolled = container.scrollHeight - container.clientHeight <= container.scrollTop + 30;
            container.innerHTML = "";

            const threadMsgs = db.dms.filter(m => 
                m.participants && m.participants.includes(currentUser.username) && m.participants.includes(targetUser)
            ).sort((a,b) => parseInt(a.id) - parseInt(b.id));

            if(threadMsgs.length === 0) {
                container.innerHTML = `<div class="text-center text-xs text-zinc-500 mt-10 italic font-medium">Buradan sohbet edebilirsiniz. Mesajlar uÃ§tan uca olmasa da izole ÅŸifrelenir.</div>`;
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
                    ? `<button onclick="openReportMsgModal('${_dmEncId}','${_dmEncSender}','${_dmEncText}')" class="text-[10px] bg-orange-950/60 text-orange-400 px-1.5 py-0.5 rounded-lg ml-1 hover:bg-orange-900/60 transition border border-orange-900/50 uppercase font-bold tracking-widest relative z-50 pointer-events-auto" title="MesajÄ± Bildir">ğŸš©</button>`
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
            document.getElementById("mk-photo-label").textContent = `FotoÄŸraf Ekle (Maksimum ${maxP} Adet)`;
            
            document.getElementById("market-modal").classList.remove("hidden");
        }

        async function saveMarketItem() {
            const t = document.getElementById("mk-title").value;
            const p = document.getElementById("mk-price").value;
            const c = document.getElementById("mk-contact").value;
            const d = document.getElementById("mk-desc").value;
            const files = document.getElementById("mk-photos").files;

           if(files[0] && !checkFileSize(files[0], 10)) return;
            
            if(!t || !p || !c) return alert("BaÅŸlÄ±k, Fiyat ve Ä°letiÅŸim zorunludur!");
            
            const tier = getUserPremiumTier(currentUser.username);
            let maxP = 1;
            if(tier >= 3) maxP = 10; else if(tier >= 2) maxP = 4; else if(tier >= 1) maxP = 2;
            
            if(files.length > maxP) return alert(`Mevcut paketiniz ${maxP} fotoÄŸraf yÃ¼klemenize izin veriyor.`);
            
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
                container.innerHTML = "<div class='col-span-2 text-center text-zinc-500 italic mt-10 font-medium'>Pazar ÅŸu an boÅŸ.</div>";
                return;
            }
            
            const sortedMarket = db.market.sort((a,b) => (b.bumped_at || 0) - (a.bumped_at || 0));

            sortedMarket.forEach(item => {
                let mainImg = Array.isArray(item.image) ? item.image[0] : (item.image || "https://placehold.co/400x300/121214/FFF?text=FOTO+YOK");
                
                const ownerTier = getUserPremiumTier(item.owner);
                let borderClass = ownerTier >= 2 ? "border-purple-500 shadow-[0_0_15px_rgba(168,85,247,0.3)]" : "border-zinc-800 shadow-sm";
                let premiumTag = ownerTier >= 2 ? `<div class="absolute top-0 right-0 bg-purple-600 text-white text-[8px] font-black px-2 py-1 rounded-bl-lg shadow-lg z-10 uppercase tracking-widest">Premium Ä°lan</div>` : "";

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
                            <span class="truncate pr-2">ğŸ‘¤ ${item.owner}</span>
                            <span class="shrink-0">ğŸ‘ï¸ ${item.views || 0}</span>
                        </div>
                    </div>
                </div>`;
            });
        }

        // openMarketDetail: renderMarket kartlarÄ±ndan Ã§aÄŸrÄ±lan alias â€” viewMarketDetail ile aynÄ±dÄ±r
        function openMarketDetail(id) {
            const item = db.market.find(x => String(x.id) === String(id));
            if(!item) { console.warn('[Market] openMarketDetail: ID bulunamadÄ±:', id); return; }
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
                document.getElementById("md-views-badge").textContent = `ğŸ‘ï¸ ${item.views || 0} GÃ¶rÃ¼ntÃ¼lenme`;
            } else {
                document.getElementById("md-views-badge").classList.add("hidden");
            }
            
            const ownerObj = db.users.find(u => u.username === item.owner);
            document.getElementById("md-owner-avatar").src = ownerObj ? ownerObj.avatar : "https://cdn.freeridertr.com.tr/profil%20resmi/unnamed.jpg";
            document.getElementById("md-owner").textContent = item.owner;
            
            document.getElementById("md-desc").textContent = item.desc || "AÃ§Ä±klama girilmemiÅŸ.";
            document.getElementById("md-contact").textContent = item.contact;

            let actionsHtml = "";
            if(item.owner !== currentUser.username) {
                actionsHtml += `<button onclick="startDm('${item.owner}')" class="bg-white hover:bg-gray-200 transition text-black py-4 rounded-xl font-bold text-sm w-full shadow-[0_0_15px_rgba(255,255,255,0.3)] btn-premium-hover">âœ‰ï¸ SATICIYA MESAJ AT</button>`;
            }
            
            if(item.owner === currentUser.username && getUserPremiumTier(currentUser.username) >= 2) {
                actionsHtml += `<button onclick="bumpMarket('${item.id}')" class="bg-purple-900/50 hover:bg-purple-800 transition text-purple-400 border border-purple-500/50 py-3.5 rounded-xl font-bold text-xs w-full mt-3 uppercase tracking-widest shadow-lg btn-premium-hover">ğŸš€ Ä°LANI EN ÃœSTE TAÅI (BUMP)</button>`;
            }
            
            if(item.owner === currentUser.username || currentUser.role === 'Admin') {
                actionsHtml += `<button onclick="deleteMarket('${item.id}')" class="bg-red-950/50 hover:bg-sky-900/80 transition text-sky-400 border border-sky-900/50 py-3.5 rounded-xl font-bold text-xs w-full mt-3 uppercase tracking-widest btn-premium-hover shadow-md">Ä°LANI SÄ°L</button>`;
            }
            
            document.getElementById("md-actions-area").innerHTML = actionsHtml;
            document.getElementById("market-detail-modal").classList.remove("hidden");
        }

        async function bumpMarket(id) {
            await sendAction('bump_market', { id: id });
            alert("Ä°lanÄ±nÄ±z baÅŸarÄ±yla en Ã¼ste taÅŸÄ±ndÄ±!");
            document.getElementById("market-detail-modal").classList.add("hidden");
            renderMarket();
        }

        async function deleteMarket(id) {
            if(confirm("Bu ilanÄ± silmek istediÄŸinize emin misiniz?")) {
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

            // Admin sÄ±ralamada gÃ¶sterilmez
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
                        <span class="animate-pulse">ğŸ‘‘</span> ${tabLabel}
                    </div>
                    <div class="flex items-center gap-4">
                        <div class="relative">
                            <img src="${champ.avatar||'https://cdn.freeridertr.com.tr/profil%20resmi/unnamed.jpg'}" class="w-16 h-16 rounded-full object-cover border-4 border-yellow-500 shadow-[0_0_20px_rgba(234,179,8,0.6)]">
                            <div class="absolute -bottom-1 -right-1 text-2xl">ğŸ¥‡</div>
                        </div>
                        <div class="flex-1">
                            <div class="font-black text-xl ${champTextCls} teko-font tracking-wide">${champ.username}</div>
                            <div class="text-yellow-400 font-black text-2xl teko-font">${champVal.toLocaleString()} XP</div>
                            <div class="text-[10px] text-zinc-400 mt-1">${currentLeaderboardTab === 'weekly' ? 'ğŸ† 1 Haftalik Ultra+ Odulu Kazanacak!' : currentLeaderboardTab === 'month' ? 'ğŸ† 1 Aylik Deluxe Odulu Kazanacak!' : ''}</div>
                        </div>
                    </div>
                </div>`;
            }

            sortedUsers.forEach((u, index) => {
                const title = getTitle(u.xp);
                const isMe = u.username === currentUser.username;
                let rankVisual = `<div class="w-8 h-8 rounded-full bg-black/60 border border-zinc-700 flex items-center justify-center font-black text-xs text-zinc-400">${index+1}</div>`;
                if(index === 0) rankVisual = `<div class="text-3xl drop-shadow-[0_0_15px_rgba(251,191,36,0.9)] animate-pulse">ğŸ¥‡</div>`;
                if(index === 1) rankVisual = `<div class="text-3xl drop-shadow-[0_0_12px_rgba(156,163,175,0.8)]">ğŸ¥ˆ</div>`;
                if(index === 2) rankVisual = `<div class="text-3xl drop-shadow-[0_0_12px_rgba(180,83,9,0.8)]">ğŸ¥‰</div>`;

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
                    <div class="text-[10px] text-zinc-500 font-bold uppercase tracking-widest mt-2 flex items-center gap-2"><span class="animate-pulse">ğŸ•’</span> ${n.date}</div>
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
            
            if(!t || !c) return alert("BaÅŸlÄ±k ve iÃ§erik zorunludur!");
            
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
            stopAllMedia(); // Hayalet ses Ã¶nleme â€” tÃ¼m medyayÄ± durdur
            // Popup triggers removed per user request
            if (idx !== 9) _prevTab = idx; // Reels dÄ±ÅŸÄ±ndaki son sekmeyi hatÄ±rla
            const tabs = ['screen-map', 'screen-chat', 'screen-market', 'screen-rank', 'screen-news', 'screen-missions', 'screen-premium', 'screen-profile', 'screen-referral', 'screen-reels'];
            tabs.forEach((t, i) => {
                const el = document.getElementById(t);
                if(!el) return;
                if(i === idx) {
                    // GÃ¶rÃ¼nÃ¼r yap - chat iÃ§in innerHTML'e dokunmadan
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

            // Reels tam ekran: alt nav'Ä± gizle/gÃ¶ster
            const bottomNav = document.getElementById('bottom-nav');
            const soundBtn2 = document.getElementById('reel-sound-btn');
            const gridBtn2  = document.getElementById('grid-view-btn');
            const uploadTopBtn2 = document.getElementById('reels-upload-top-btn');
            if(idx === 9) {
                if(bottomNav) bottomNav.style.display = 'none';
                // Ses, Ä±zgara ve yÃ¼kleme butonlarÄ±nÄ± gÃ¶ster (loadReels bitmeden Ã¶nce de gÃ¶rÃ¼nsÃ¼n)
                if(soundBtn2) { soundBtn2.style.display = 'flex'; soundBtn2.textContent = _reelMuted ? 'ğŸ”‡' : 'ğŸ”Š'; }
                if(gridBtn2)  gridBtn2.style.display = 'flex';
                if(uploadTopBtn2) uploadTopBtn2.style.display = 'flex';
                document.getElementById('screen-map') && (document.getElementById('screen-map').style.zIndex = '1');
            } else {
                if(bottomNav) bottomNav.style.display = '';
                if(soundBtn2) soundBtn2.style.display = 'none';
                if(gridBtn2)  gridBtn2.style.display = 'none';
                if(uploadTopBtn2) uploadTopBtn2.style.display = 'none';
                // stopAllMedia zaten baÅŸta Ã§aÄŸrÄ±ldÄ±, ek pause gerekmez
            }

            if(idx === 0) { if(map) map.invalidateSize(); }
            if(idx === 1) { renderChat(); renderDmList(); clearChatBadge(); renderStoryBar(); }
            if(idx === 2) renderMarket();
            if(idx === 3) renderLeaderboard();
            if(idx === 4) renderNews();
            if(idx === 5) { renderMissions(); updateSpinInfo(); setTimeout(initWheel3D, 150); }
            if(idx === 7) { updateProfileUI(); updateNotifBtnState(); }
            if(idx === 8) renderReferralTab();
            if(idx === 9) loadReels();
            
            // Alt nav gÃ¼ncelle (premium animasyonlu)
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
        // PROMINENT DISCLOSURE â€” FotoÄŸraf (Google Play uyumu)
        // file input tetiklenmeden Ã–NCE kullanÄ±cÄ±ya amaÃ§ gÃ¶sterilir.
        // ============================================================
        const _PD_PHOTO_CFG = {
            group:   { icon:'ğŸ’¬', title:'Sohbete FotoÄŸraf Ekle',   sub:'Grup Sohbeti',
                       desc:'SeÃ§eceÄŸin fotoÄŸraf <strong class="text-white">grup sohbetine</strong> gÃ¶nderilecek.',
                       items:['FotoÄŸraf yalnÄ±zca grup Ã¼yelerine gÃ¶rÃ¼nÃ¼r','GÃ¶rsel otomatik boyutlandÄ±rÄ±lÄ±r (maks. 800px)','YalnÄ±zca seÃ§tiÄŸin gÃ¶rsel paylaÅŸÄ±lÄ±r'] },
            dm:      { icon:'âœ‰ï¸', title:'Mesaja FotoÄŸraf Ekle',     sub:'Ã–zel Mesaj',
                       desc:'SeÃ§eceÄŸin fotoÄŸraf <strong class="text-white">Ã¶zel mesaj</strong> olarak gÃ¶nderilecek.',
                       items:['YalnÄ±zca mesaj gÃ¶nderdiÄŸin kiÅŸi gÃ¶rebilir','GÃ¶rsel otomatik boyutlandÄ±rÄ±lÄ±r (maks. 800px)','YalnÄ±zca seÃ§tiÄŸin gÃ¶rsel paylaÅŸÄ±lÄ±r'] },
            profile: { icon:'ğŸ‘¤', title:'Profil FotoÄŸrafÄ± GÃ¼ncelle', sub:'Profil GÃ¶rseli',
                       desc:'SeÃ§eceÄŸin fotoÄŸraf <strong class="text-white">profil resmin</strong> olarak ayarlanacak.',
                       items:['TÃ¼m kullanÄ±cÄ±lar profil fotoÄŸrafÄ±nÄ± gÃ¶rebilir','GÃ¶rsel otomatik kÄ±rpÄ±lÄ±r ve optimize edilir (400px)','YalnÄ±zca seÃ§tiÄŸin gÃ¶rsel yÃ¼klenir'] },
            reel:    { icon:'ğŸ¬', title:'Reel Medya SeÃ§',           sub:'Reel / GÃ¶nderi',
                       desc:'SeÃ§eceÄŸin fotoÄŸraf veya video <strong class="text-white">reel olarak paylaÅŸÄ±lacak</strong>.',
                       items:['TÃ¼m topluluk Ã¼yeleri gÃ¶rebilir','FotoÄŸraflar optimize edilir, videolar maks. 50MB','YalnÄ±zca seÃ§tiÄŸin dosya paylaÅŸÄ±lÄ±r'] },
        };

        function _showPhotoDisclosure(context, onConfirm) {
            const cfg = _PD_PHOTO_CFG[context] || _PD_PHOTO_CFG.profile;
            document.getElementById('pd-photo-icon').textContent     = cfg.icon;
            document.getElementById('pd-photo-title').textContent    = cfg.title;
            document.getElementById('pd-photo-subtitle').textContent = cfg.sub;
            document.getElementById('pd-photo-desc').innerHTML       = cfg.desc;
            document.getElementById('pd-photo-list').innerHTML = cfg.items
                .map(t => `<li class="flex items-start gap-2"><span class="text-pink-400 shrink-0 mt-0.5">âœ”</span><span>${t}</span></li>`)
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
        // PROMINENT DISCLOSURE â€” Mikrofon (Google Play uyumu)
        // getUserMedia() Ã§aÄŸrÄ±sÄ±ndan Ã–NCE kullanÄ±cÄ±ya amaÃ§ gÃ¶sterilir.
        // Ä°zin zaten verildiyse modal atlanÄ±r, kayÄ±t doÄŸrudan baÅŸlar.
        // ============================================================
        async function toggleVoiceRecord(context) {
            if(getUserPremiumTier(currentUser.username) < 2) {
                return alert("Sesli mesaj gÃ¶nderme Ã¶zelliÄŸi Deluxe ve Ultra+ Ã¼yelerine Ã¶zeldir!");
            }
            const btn = document.getElementById("voice-btn");

            // Aktif kayÄ±t varsa durdur â€” disclosure gerektirmez
            // NOT: MediaRecorder.state deÄŸerleri: "inactive", "recording", "paused"
            // Ã–nceki kodda "active" kullanÄ±lÄ±yordu ki bu HÄ°Ã‡BÄ°R ZAMAN true olmaz!
            if (mediaRecorder && mediaRecorder.state === "recording") {
                _voiceStopping = true;   // Blob iÅŸlenene kadar yeni kaydÄ± engelle
                mediaRecorder.stop();
                // stop event handler iÃ§inde btn sÄ±fÄ±rlanacak ve mediaRecorder = null yapÄ±lacak
                return;
            }

            // Blob henÃ¼z iÅŸleniyorsa (stop() sonrasÄ± kÄ±sa pencere) izin akÄ±ÅŸÄ±na dÃ¼ÅŸme
            if (_voiceStopping) return;

            // Ä°zin zaten verilmiÅŸse doÄŸrudan kaydÄ± baÅŸlat (modal gÃ¶sterme)
            try {
                const perm = await navigator.permissions.query({ name: 'microphone' });
                if (perm.state === 'granted') { await _startVoiceCapture(context, btn); return; }
            } catch(_) { /* permissions API desteklenmiyor â€” modal gÃ¶ster */ }

            // Prominent Disclosure modal â€” sadece izin granted DEÄÄ°LSE gÃ¶sterilir
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
                btn.innerHTML = "â¹ï¸";
                mediaRecorder.addEventListener("dataavailable", ev => { audioChunks.push(ev.data); });
                mediaRecorder.addEventListener("stop", async () => {
                    // Ses verisini hazÄ±rla ve gÃ¶nder
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
                    // Butonu sÄ±fÄ±rla
                    btn.className = "bg-zinc-800/80 hover:bg-zinc-700 transition w-10 h-10 md:w-12 md:h-12 rounded-xl text-lg flex items-center justify-center border border-zinc-700 btn-premium-hover";
                    btn.innerHTML = "ğŸ¤";
                    // KRITIK: mediaRecorder'Ä± null yap ki sonraki tÄ±klamada
                    // stale "inactive" state yÃ¼zÃ¼nden yanlÄ±ÅŸ dallanma olmasÄ±n
                    audioChunks = [];
                    mediaRecorder = null;
                    _voiceStopping = false; // ArtÄ±k yeni kayda izin ver
                });
                // start() Ã§aÄŸrÄ±sÄ± event listener'lardan SONRA yapÄ±lmalÄ±
                mediaRecorder.start();
            } catch(err) {
                console.error('Mikrofon hatasÄ±:', err);
                mediaRecorder = null;
                alert("Mikrofon izni alÄ±namadÄ±. TarayÄ±cÄ± ayarlarÄ±ndan mikrofon iznini etkinleÅŸtir.");
            }
        }
        
        function playVoice(src) { const a = new Audio(src); a.play(); }

        // Premium modal animasyon yardÄ±mcÄ±sÄ±
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
                    statusDiv.innerHTML = `<span class="bg-green-900/40 text-green-400 text-[10px] px-3 py-1.5 rounded-lg font-bold border border-green-800/50 shadow-sm uppercase tracking-widest inline-flex items-center gap-1"><span class="text-sm">âœ…</span> E-Posta DoÄŸrulandÄ±</span>`;
                } else {
                    statusDiv.innerHTML = `<span class="bg-yellow-900/40 text-yellow-500 text-[10px] px-3 py-1.5 rounded-lg font-bold border border-yellow-800/50 shadow-sm uppercase tracking-widest inline-flex items-center gap-1"><span class="text-sm">âš ï¸</span> E-Posta DoÄŸrulanmadÄ±</span>`;
                }
            } else {
                statusDiv.innerHTML = `<span class="bg-zinc-800 text-zinc-400 text-[10px] px-3 py-1.5 rounded-lg font-bold border border-zinc-700 uppercase tracking-widest inline-block">E-Posta EklenmemiÅŸ</span>`;
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
                // GerÃ§ekten farklÄ± bir email girildiyse deÄŸiÅŸtir
                emailChanged = true;
                stats.email = emailInput;
                stats.email_verified = false;
            } else if (emailInput === "") {
                // Email alanÄ± boÅŸ bÄ±rakÄ±ldÄ±ysa mevcut emaili koru
                // stats.email deÄŸiÅŸmesin
            }
            // email aynÄ±ysa hiÃ§bir ÅŸey yapma (email_verified korunur)

            if (p && p.trim() !== "") { 
                if (p.length < 4) return alert("Åifre en az 4 hane olmalÄ±."); 
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
                    alert("Profil gÃ¼ncellendi! E-posta adresiniz gÃ¼ncellendi ancak henÃ¼z ONAYLANMADI. 'DoÄŸrulama Kodu GÃ¶nder' butonuyla e-postanÄ±zÄ± onaylayÄ±n.");
                } else {
                    alert("Profil baÅŸarÄ±yla gÃ¼ncellendi.");
                }
                closeSettingsModal(); 
            } catch(e) {
                alert("Hata oluÅŸtu: " + e.message);
            }
        }

        async function requestProfileEmailVerify() {
            const email = document.getElementById("edit-email").value.trim();
            const marketing = document.getElementById("edit-marketing").checked;
            if(!email) return alert("LÃ¼tfen bir e-posta adresi girin.");
            
            try {
                await sendAction('send_profile_verification', { email: email, marketing: marketing });
                
                document.getElementById("settings-modal").classList.add("hidden");
                verificationUsername = currentUser.username;
                
                document.getElementById("verify-code-input").value = ""; 
                document.getElementById("email-verify-modal").classList.remove("hidden");
                alert("DoÄŸrulama kodu e-posta adresinize gÃ¶nderildi!");
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
            // RPM partner subdomain â€” freeridertr iÃ§in Ã¶zel subdomain yoksa genel URL
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

        // RPM iframe'den mesaj dinle â€” avatar URL'i gelince kaydet
        window.addEventListener('message', async (event) => {
            if(!event.data || typeof event.data !== 'string') return;
            // RPM, avatar URL'ini JSON veya dÃ¼z string olarak gÃ¶nderir
            let avatarUrl = null;
            try {
                const parsed = JSON.parse(event.data);
                if(parsed.source === 'readyplayerme' && parsed.eventName === 'v1.avatar.exported') {
                    avatarUrl = parsed.data?.url;
                }
            } catch(e) {
                // BazÄ± sÃ¼rÃ¼mlerde dÃ¼z URL gelir
                if(typeof event.data === 'string' && event.data.includes('models.readyplayer.me')) {
                    avatarUrl = event.data;
                }
            }
            if(avatarUrl && currentUser) {
                // PNG render URL'i oluÅŸtur (fullbody portrait)
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
                    // KÃ¼Ã§Ã¼k kutlama toast
                    const t = document.createElement('div');
                    t.className = 'fixed top-20 left-1/2 -translate-x-1/2 z-[99999] bg-gradient-to-r from-purple-600 to-indigo-600 text-white px-6 py-3 rounded-2xl font-bold text-sm shadow-2xl flex items-center gap-3 scale-in-anim';
                    t.innerHTML = '<span style="font-size:20px">ğŸ­</span><div><div style="font-size:10px;opacity:0.8;text-transform:uppercase;letter-spacing:0.1em">Avatar Kaydedildi!</div><div>3D avatarÄ±n profile eklendi</div></div>';
                    document.body.appendChild(t);
                    setTimeout(() => { t.style.opacity='0'; t.style.transition='opacity 0.5s'; setTimeout(()=>t.remove(),500); }, 3000);
                } catch(e) { alert('Avatar kaydedilemedi: ' + e.message); }
            }
        });

        async function acceptChatRules() {
            await sendAction('accept_chat_rules', {});
            currentUser.accepted_chat_rules = true;
            document.getElementById("chat-rules-modal").classList.add("hidden");
            alert("KurallarÄ± kabul ettiniz, sisteme hoÅŸ geldiniz.");
        }

        // ===============================================================
        // GELÄ°ÅMÄ°Å ADMÄ°N PANELÄ° - TAM SÄ°STEM
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
            if(roleTag) roleTag.textContent = isMainAdmin ? 'ğŸ‘‘ Ana YÃ¶netici' : 'ğŸ›¡ï¸ YardÄ±mcÄ± YÃ¶netici';

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

            // Stats gÃ¼ncelle
            document.getElementById('astat-users').textContent = db.users.length;
            document.getElementById('astat-banned').textContent = db.banned.length;

            // Maintenance
            const maintChk = document.getElementById("admin-maintenance");
            if(maintChk) maintChk.checked = db.maintenance;

            // Google Play IAP â€” Bekleyen manuel onay listesi (main admin only)
            // NOT: Google Play IAP akÄ±ÅŸÄ±nda satÄ±n alÄ±mlar /api/verify_google_purchase
            // Ã¼zerinden otomatik doÄŸrulanÄ±r. Bu panel yalnÄ±zca otomatik doÄŸrulamasÄ±
            // baÅŸarÄ±sÄ±z olan veya admin tarafÄ±ndan manuel onay gerektiren durumlarÄ± gÃ¶sterir.
            if(isMainAdmin) {
                const reqContainer = document.getElementById("admin-iap-requests");
                reqContainer.innerHTML = "";
                let hasReqs = false;
                db.users.forEach(u => {
                    // pending_premium: otomatik doÄŸrulamasÄ± tamamlanamamÄ±ÅŸ IAP'lar
                    if(u.stats && u.stats.pending_premium) {
                        hasReqs = true;
                        const tierNum = parseInt(u.stats.pending_premium);
                        const productId = u.stats.gp_product_id || 'â€”';
                        const pName = tierNum === 3 ? "ğŸ‘‘ Ultra+" : (tierNum === 2 ? "ğŸŒŸ Deluxe" : "â­ Standart");
                        const isAdminOverride = u.stats.gp_admin_override ? ' (Manuel)' : ' (IAP)';
                        reqContainer.innerHTML += `
                        <div class="rounded-xl p-3 border border-zinc-700/60 flex justify-between items-center admin-card-enter" style="background:rgba(0,0,0,0.5)">
                            <div>
                                <div class="font-bold text-white text-sm">${u.username}</div>
                                <div class="text-[10px] text-yellow-400 font-bold uppercase tracking-widest mt-0.5">${pName}${isAdminOverride}</div>
                                <div class="text-[9px] text-zinc-500 mt-0.5">Product: ${productId}</div>
                            </div>
                            <div class="flex gap-2">
                                <button onclick="approvePrem('${u.username}', ${tierNum})" class="bg-green-800/80 hover:bg-green-700 px-3 py-2 rounded-lg text-[10px] font-bold text-white transition">âœ“ Onayla</button>
                                <button onclick="rejectPrem('${u.username}')" class="bg-red-900/60 hover:bg-red-800/80 px-3 py-2 rounded-lg text-[10px] font-bold text-white transition">âœ• Red</button>
                            </div>
                        </div>`;
                    }
                });
                if(!hasReqs) reqContainer.innerHTML = "<div class='text-zinc-600 text-xs italic py-1 font-medium'>âœ… Bekleyen IAP onayÄ± yok.</div>";
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
            container.innerHTML = '<div class="text-center text-zinc-500 py-4 text-xs animate-pulse">KullanÄ±cÄ±lar yÃ¼kleniyor...</div>';
            try {
                const res = await sendAction('get_all_users_admin', { page: page, per_page: 200, search: search });
                if (res && res.users) {
                    _adminAllUsers = res.users;
                    _adminUserPage = res.page || 1;
                    _adminUserTotal = res.total || res.users.length;
                    renderAdminUserList(res.users);
                    // Toplam kullanÄ±cÄ± sayÄ±sÄ±nÄ± stats'a yansÄ±t
                    const statEl = document.getElementById('astat-users');
                    if(statEl) statEl.textContent = _adminUserTotal;
                } else {
                    renderAdminUserList(db.users);
                }
            } catch(e) {
                console.warn('Admin kullanÄ±cÄ± listesi yÃ¼klenemedi, fallback:', e);
                renderAdminUserList(db.users);
            }
        }

        function renderAdminUserList(users) {
            const container = document.getElementById('admin-user-list');
            if(!container) return;
            container.innerHTML = '';

            // Pagination info
            if(_adminUserTotal > 0) {
                container.innerHTML += `<div class="text-[10px] text-zinc-500 font-bold uppercase tracking-widest mb-2 px-1">Toplam: ${_adminUserTotal} kullanÄ±cÄ± (Sayfa ${_adminUserPage})</div>`;
            }

            (users || []).forEach((u, i) => {
                const isBanned = db.banned.includes(u.username);
                const premTier = (u.stats && u.stats.premium_tier) ? parseInt(u.stats.premium_tier) : 0;
                const roleLabel = u.role === 'Admin' ? 'ğŸ‘‘' : (u.role === 'SubAdmin' ? 'ğŸ›¡ï¸' : '');
                const premBadge = premTier === 3 ? '<span class="text-yellow-400 text-[8px] font-black">ULTRA+</span>' : (premTier === 2 ? '<span class="text-purple-400 text-[8px] font-black">DLX</span>' : (premTier === 1 ? '<span class="text-blue-400 text-[8px] font-black">STD</span>' : ''));
                container.innerHTML += `
                <div class="rounded-xl p-3 border flex items-center gap-3 admin-card-enter transition-all hover:border-zinc-600 cursor-pointer" style="background:rgba(0,0,0,0.45);border-color:rgba(63,63,70,0.7);animation-delay:${i*0.03}s" onclick="openUserActivity('${u.username}')">
                    <img src="${u.avatar || 'https://cdn.freeridertr.com.tr/profil%20resmi/unnamed.jpg'}" class="w-10 h-10 rounded-full object-cover shrink-0 border-2 ${isBanned ? 'border-sky-600' : 'border-zinc-700'}">
                    <div class="flex-1 min-w-0">
                        <div class="flex items-center gap-1.5">
                            <span class="text-white font-bold text-sm truncate">${u.username}</span>
                            <span>${roleLabel}</span>
                            ${premBadge}
                            ${isBanned ? '<span class="ban-reason-badge">BanlÄ±</span>' : ''}
                        </div>
                        <div class="text-zinc-500 text-[10px] font-bold truncate mt-0.5">${u.city || 'â€”'} Â· ${u.xp || 0} XP</div>
                    </div>
                    <div class="shrink-0 text-zinc-600 text-xs">â€º</div>
                </div>`;
            });
            if(!users || users.length === 0) container.innerHTML = '<div class="text-zinc-600 text-xs italic text-center py-4">KullanÄ±cÄ± bulunamadÄ±.</div>';
        }

        function adminSearchUsers() {
            const q = document.getElementById('admin-user-search').value.toLowerCase().trim();
            const filtered = q ? db.users.filter(u => u.username.toLowerCase().includes(q) || (u.city||'').toLowerCase().includes(q)) : db.users;
            renderAdminUserList(filtered);
        }

        async function loadAdminReels() {
            const container = document.getElementById('admin-reels-list');
            if(!container) return;
            container.innerHTML = '<div class="text-zinc-600 text-xs italic text-center py-4 animate-pulse">YÃ¼kleniyor...</div>';
            try {
                const res = await sendAction('get_reels', {offset: 0});
                const reels = (res && res.reels) ? res.reels : [];
                container.innerHTML = '';
                if(!reels.length) { container.innerHTML = '<div class="text-zinc-600 text-xs italic text-center py-4">Reel bulunamadÄ±.</div>'; return; }
                reels.forEach((r, i) => {
                    const isVideo = r.media_type === 'video';
                    const dt = r.created_at ? new Date(r.created_at * 1000).toLocaleDateString('tr-TR') : 'â€”';
                    container.innerHTML += `
                    <div class="rounded-xl p-3 border border-zinc-800/70 flex items-center gap-3 admin-card-enter" style="background:rgba(0,0,0,0.5);animation-delay:${i*0.04}s">
                        <div class="w-14 h-14 rounded-xl overflow-hidden shrink-0 border border-zinc-700 bg-zinc-900 flex items-center justify-center">
                            ${isVideo ? `<span class="text-2xl">ğŸ¥</span>` : `<img src="${r.media_url}" class="w-full h-full object-cover">`}
                        </div>
                        <div class="flex-1 min-w-0">
                            <div class="text-white font-bold text-sm truncate">${r.user}</div>
                            <div class="text-zinc-500 text-[10px] font-bold mt-0.5 truncate">${r.caption || '(AÃ§Ä±klama yok)'}</div>
                            <div class="flex items-center gap-2 mt-1">
                                <span class="text-zinc-600 text-[9px] font-bold">${dt}</span>
                                <span class="text-pink-500 text-[9px] font-bold">â¤ ${(r.likes||[]).length}</span>
                                <span class="text-zinc-500 text-[9px] font-bold">${isVideo ? 'ğŸ¥ Video' : 'ğŸ“¸ Foto'}</span>
                            </div>
                        </div>
                        <button onclick="adminDeleteReel('${r.id}', '${r.user}', this)" class="shrink-0 w-8 h-8 rounded-lg bg-red-900/40 border border-sky-800/50 text-sky-300 hover:bg-sky-800/60 flex items-center justify-center text-sm transition hover:scale-110">ğŸ—‘</button>
                    </div>`;
                });
            } catch(e) {
                container.innerHTML = '<div class="text-sky-400 text-xs italic text-center py-4">YÃ¼klenirken hata oluÅŸtu.</div>';
            }
        }

        async function adminDeleteReel(reelId, owner, btn) {
            if(!confirm(`${owner} adlÄ± kullanÄ±cÄ±nÄ±n reelini silmek istediÄŸine emin misin?`)) return;
            btn.disabled = true; btn.textContent = '...';
            const res = await sendAction('delete_reel', {reel_id: reelId});
            if(res && res.status === 'ok') {
                btn.closest('.rounded-xl').style.opacity = '0.3';
                btn.textContent = 'âœ“';
                showToast(`ğŸ—‘ï¸ Reel silindi.`);
            }
        }

        async function loadAdminLogs() {
            const container = document.getElementById('admin-logs-list');
            if(!container) return;
            container.innerHTML = '<div class="text-zinc-600 text-xs italic text-center py-4 animate-pulse">YÃ¼kleniyor...</div>';
            try {
                const res = await sendAction('get_admin_logs', {});
                const logs = (res && res.logs) ? res.logs : [];
                container.innerHTML = '';
                if(!logs.length) { container.innerHTML = '<div class="text-zinc-600 text-xs italic text-center py-4">HenÃ¼z kayÄ±t yok.</div>'; return; }
                const actionColors = { ban_user: 'log-ban', delete_reel: 'log-delete', delete_message: 'log-delete', delete_marker: 'log-delete', assign_admin: 'log-assign', revoke_admin: 'log-revoke', notify_main: 'log-notify' };
                const actionEmojis = { ban_user: 'ğŸš¨', delete_reel: 'ğŸ¬', delete_message: 'ğŸ’¬', delete_marker: 'ğŸ“', assign_admin: 'âœ…', revoke_admin: 'âŒ', notify_main: 'ğŸ“¢' };
                logs.forEach((l, i) => {
                    const colorClass = actionColors[l.action] || 'log-default';
                    const emoji = actionEmojis[l.action] || 'ğŸ”§';
                    const dt = l.ts ? new Date(l.ts * 1000).toLocaleString('tr-TR') : 'â€”';
                    container.innerHTML += `
                    <div class="rounded-xl p-3 pl-4 admin-card-enter ${colorClass}" style="background:rgba(0,0,0,0.5);animation-delay:${i*0.03}s">
                        <div class="flex items-center justify-between gap-2">
                            <div class="flex items-center gap-2 min-w-0">
                                <span class="text-sm shrink-0">${emoji}</span>
                                <div class="min-w-0">
                                    <div class="text-white text-xs font-bold"><span class="text-red-300">${l.admin}</span> â†’ <span class="text-zinc-300">${l.target || 'â€”'}</span></div>
                                    <div class="text-zinc-500 text-[10px] font-bold truncate mt-0.5">${l.detail || l.action}</div>
                                </div>
                            </div>
                            <div class="text-zinc-600 text-[9px] font-bold shrink-0">${dt}</div>
                        </div>
                    </div>`;
                });
            } catch(e) {
                container.innerHTML = '<div class="text-sky-400 text-xs italic text-center py-4">YÃ¼klenirken hata oluÅŸtu.</div>';
            }
        }

        async function loadSubAdmins() {
            const container = document.getElementById('sub-admin-list');
            if(!container) return;
            container.innerHTML = '<div class="text-zinc-600 text-xs italic text-center py-3 animate-pulse">YÃ¼kleniyor...</div>';
            try {
                const res = await sendAction('get_all_sub_admins', {});
                const admins = (res && res.sub_admins) ? res.sub_admins : [];
                const el2 = document.getElementById('astat-admins');
                if(el2) el2.textContent = admins.length;
                container.innerHTML = '';
                if(!admins.length) { container.innerHTML = '<div class="text-zinc-600 text-xs italic text-center py-3">HenÃ¼z yardÄ±mcÄ± admin yok.</div>'; return; }
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
                container.innerHTML = '<div class="text-sky-400 text-xs italic text-center py-3">YÃ¼klenirken hata oluÅŸtu.</div>';
            }
        }

        async function assignSubAdmin() {
            const uname = document.getElementById('assign-admin-username').value.trim();
            if(!uname) { showToast('KullanÄ±cÄ± adÄ± gir!'); return; }
            if(!confirm(`${uname} adlÄ± kullanÄ±cÄ±ya yardÄ±mcÄ± admin yetkisi verilecek. Emin misin?`)) return;
            const res = await sendAction('assign_sub_admin', {username: uname});
            if(res && res.status === 'ok') {
                showToast(`âœ… ${uname} artÄ±k yardÄ±mcÄ± admin!`);
                document.getElementById('assign-admin-username').value = '';
                loadSubAdmins();
            } else {
                alert(res?.message || 'Hata oluÅŸtu.');
            }
        }

        async function revokeSubAdmin() {
            const uname = document.getElementById('revoke-admin-username').value.trim();
            if(!uname) { showToast('KullanÄ±cÄ± adÄ± gir!'); return; }
            if(!confirm(`${uname} adlÄ± kullanÄ±cÄ±nÄ±n admin yetkisi alÄ±nacak. Emin misin?`)) return;
            const res = await sendAction('revoke_sub_admin', {username: uname});
            if(res && res.status === 'ok') {
                showToast(`âŒ ${uname} yetkisi alÄ±ndÄ±.`);
                document.getElementById('revoke-admin-username').value = '';
                loadSubAdmins();
            } else {
                alert(res?.message || 'Hata oluÅŸtu.');
            }
        }

        async function quickRevokeAdmin(uname, btn) {
            if(!confirm(`${uname} yÃ¶neticilikten Ã§Ä±karÄ±lsÄ±n mÄ±?`)) return;
            btn.disabled = true; btn.textContent = '...';
            const res = await sendAction('revoke_sub_admin', {username: uname});
            if(res && res.status === 'ok') {
                btn.closest('.rounded-xl').style.opacity = '0.3';
                showToast(`âŒ ${uname} yetkisi alÄ±ndÄ±.`);
                loadSubAdmins();
            }
        }

        async function adminNotifyMain() {
            const msg = document.getElementById('admin-notify-msg').value.trim();
            if(!msg) { showToast('Mesaj boÅŸ olamaz!'); return; }
            const res = await sendAction('admin_notify_main', {message: msg});
            if(res && res.status === 'ok') {
                document.getElementById('admin-notify-msg').value = '';
                showToast('ğŸ“¨ Ana admine bildirim gÃ¶nderildi!');
            }
        }

        // ---- KullanÄ±cÄ± Aktivite ModalÄ± ----
        async function openUserActivity(username) {
            _uaCurrentUser = username;
            _uaActivityData = null;
            document.getElementById('ua-username-label').textContent = '@' + username;
            document.getElementById('ua-content').innerHTML = '<div class="text-zinc-600 text-xs italic text-center py-6 animate-pulse">YÃ¼kleniyor...</div>';
            document.getElementById('user-activity-modal').classList.remove('hidden');
            uaTab('messages');

            try {
                const res = await sendAction('get_user_activity', {username});
                if(res && res.activity) {
                    _uaActivityData = res.activity;
                    uaRender(_uaCurrentTab);
                }
            } catch(e) {
                document.getElementById('ua-content').innerHTML = '<div class="text-sky-300 text-xs italic text-center py-6">YÃ¼klenirken hata oluÅŸtu.</div>';
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
                container.innerHTML = `<div class="text-zinc-600 text-xs italic text-center py-6">Bu kategoride iÃ§erik yok.</div>`;
                return;
            }
            if(tab === 'manage') {
                const isMainAdmin = (currentUser && (currentUser.role === 'Admin' || currentUser.username === 'Admin' || currentUser.username.toLowerCase() === 'admin'));
                if(!isMainAdmin) {
                    container.innerHTML = `<div class="text-zinc-600 text-xs italic text-center py-6">Bu sekmeye eriÅŸim yetkiniz yok.</div>`;
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
                        <div class="text-[10px] text-zinc-500 uppercase font-bold tracking-widest mb-3">KullanÄ±cÄ± DetaylarÄ±</div>
                        <div class="text-xs text-white mb-1"><span class="text-zinc-400">Åehir:</span> ${targetUser.city || 'Bilinmiyor'}</div>
                        <div class="text-xs text-white mb-1"><span class="text-zinc-400">XP:</span> ${targetUser.xp || 0}</div>
                        <div class="text-xs text-white mb-1"><span class="text-zinc-400">Rol:</span> ${targetUser.role || 'User'}</div>
                        <div class="text-xs text-white mb-3"><span class="text-zinc-400">Premium:</span> <span class="text-yellow-400 font-bold">${premText}</span></div>
                    </div>
                    <div class="p-4 rounded-xl border border-amber-900/30" style="background:rgba(120,53,15,0.1)">
                        <div class="text-[10px] text-amber-500 uppercase font-bold tracking-widest mb-3">Ãœyelik / Premium Ä°ÅŸlemleri</div>
                        <div class="grid grid-cols-2 gap-2 mb-2">
                            <button onclick="execAdminCmd('${targetUser.username} standart gÃ¶nder')" class="py-2 bg-blue-900/40 text-blue-300 text-[10px] font-bold rounded shadow-md hover:bg-blue-800/50 transition border border-blue-800/50">+ Standart Ver</button>
                            <button onclick="execAdminCmd('${targetUser.username} deluxe gÃ¶nder')" class="py-2 bg-purple-900/40 text-purple-300 text-[10px] font-bold rounded shadow-md hover:bg-purple-800/50 transition border border-purple-800/50">+ Deluxe Ver</button>
                            <button onclick="execAdminCmd('${targetUser.username} ultra gÃ¶nder')" class="py-2 bg-yellow-900/40 text-yellow-300 text-[10px] font-bold rounded shadow-md hover:bg-yellow-800/50 transition border border-yellow-800/50">+ Ultra+ Ver</button>
                            <button onclick="execAdminCmd('${targetUser.username} standart geri Ã§ek')" class="py-2 bg-red-900/40 text-red-300 text-[10px] font-bold rounded shadow-md hover:bg-red-800/50 transition border border-red-800/50">âŒ SÃ¼re Sil</button>
                        </div>
                        <div class="text-[9px] text-zinc-500 font-bold">Not: Zaten premiumu varsa 'Ver' diyerek sÃ¼resini uzatabilirsiniz.</div>
                    </div>
                    <div class="p-4 rounded-xl border border-zinc-800" style="background:rgba(0,0,0,0.4)">
                        <div class="text-[10px] text-zinc-500 uppercase font-bold tracking-widest mb-3">Tehlikeli Ä°ÅŸlemler</div>
                        <div class="space-y-2">
                            <button onclick="adminResetPassword('${targetUser.username}')" class="w-full py-2 bg-zinc-800 text-zinc-300 text-xs font-bold rounded hover:bg-zinc-700 transition">ğŸ”‘ Åifre SÄ±fÄ±rla (Rastgele)</button>
                            <button onclick="adminChangeUsername('${targetUser.username}')" class="w-full py-2 bg-zinc-800 text-zinc-300 text-xs font-bold rounded hover:bg-zinc-700 transition">âœï¸ Ä°sim DeÄŸiÅŸtir</button>
                            <button onclick="adminDeleteUser('${targetUser.username}')" class="w-full py-2 bg-red-950/50 border border-sky-900/50 text-sky-400 text-xs font-bold rounded hover:bg-sky-900/40 transition">ğŸ—‘ï¸ HesabÄ± KalÄ±cÄ± Sil</button>
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
                            ${m.image ? `<div class="text-[9px] text-zinc-600 mt-1">ğŸ“¸ GÃ¶rsel iÃ§erik</div>` : ''}
                        </div>
                        <button onclick="adminDelMsg('${m.id}', this)" class="shrink-0 w-7 h-7 bg-sky-900/30 border border-red-800/40 rounded-lg text-sky-300 hover:bg-sky-800/50 flex items-center justify-center text-[10px] transition">ğŸ—‘</button>
                    </div>`;
                });
            } else if(tab === 'dms') {
                data_ua.forEach((m, i) => {
                    const others = (m.participants || []).filter(p => p !== _uaCurrentUser);
                    const txt = m.text ? String(m.text).substring(0,100) : (m.type || '?');
                    container.innerHTML += `
                    <div class="rounded-xl p-3 border border-zinc-800/70 admin-card-enter" style="background:rgba(0,0,0,0.45);animation-delay:${i*0.03}s">
                        <div class="text-[10px] text-zinc-500 font-bold mb-1">â†” ${others.join(', ') || '?'}</div>
                        <div class="text-zinc-300 text-xs font-medium">${txt}</div>
                    </div>`;
                });
            } else if(tab === 'reels') {
                data_ua.forEach((r, i) => {
                    const isVideo = r.media_type === 'video';
                    container.innerHTML += `
                    <div class="rounded-xl p-3 border border-zinc-800/70 flex items-center gap-3 admin-card-enter" style="background:rgba(0,0,0,0.45);animation-delay:${i*0.04}s">
                        <div class="w-12 h-12 rounded-lg overflow-hidden shrink-0 bg-zinc-900 border border-zinc-800 flex items-center justify-center">
                            ${isVideo ? `<span class="text-xl">ğŸ¥</span>` : `<img src="${r.media_url}" class="w-full h-full object-cover" onerror="this.parentElement.innerHTML='ğŸ“¸'">`}
                        </div>
                        <div class="flex-1 min-w-0">
                            <div class="text-zinc-300 text-xs font-medium truncate">${r.caption || '(AÃ§Ä±klama yok)'}</div>
                            <div class="text-pink-400 text-[9px] font-bold mt-0.5">â¤ ${(r.likes||[]).length}</div>
                        </div>
                        <button onclick="adminDeleteReel('${r.id}','${r.user}',this)" class="shrink-0 w-7 h-7 bg-sky-900/30 border border-red-800/40 rounded-lg text-sky-300 hover:bg-sky-800/50 flex items-center justify-center text-[10px] transition">ğŸ—‘</button>
                    </div>`;
                });
            } else if(tab === 'markers') {
                data_ua.forEach((m, i) => {
                    container.innerHTML += `
                    <div class="rounded-xl p-3 border border-zinc-800/70 flex items-center gap-3 admin-card-enter" style="background:rgba(0,0,0,0.45);animation-delay:${i*0.04}s">
                        <div class="w-10 h-10 rounded-lg bg-sky-900/30 border border-red-800/40 flex items-center justify-center text-xl shrink-0">${m.icon_type || 'ğŸš´'}</div>
                        <div class="flex-1 min-w-0">
                            <div class="text-white text-sm font-bold truncate">${m.name || 'â€”'}</div>
                            <div class="text-zinc-500 text-[10px] font-bold">${m.difficulty || 'â€”'}</div>
                        </div>
                        <button onclick="adminDelMarker('${m.id}','${m.name}',this)" class="shrink-0 w-7 h-7 bg-sky-900/30 border border-red-800/40 rounded-lg text-sky-300 hover:bg-sky-800/50 flex items-center justify-center text-[10px] transition">ğŸ—‘</button>
                    </div>`;
                });
            }
        }

        async function adminDelMsg(msgId, btn) {
            if(!confirm('Bu mesajÄ± silmek istediÄŸine emin misin?')) return;
            btn.disabled = true; btn.textContent = '...';
            const res = await sendAction('admin_delete_message_by_id', {msg_id: msgId});
            if(res && res.status === 'ok') {
                btn.closest('.rounded-xl').style.opacity = '0.2';
                showToast('ğŸ’¬ Mesaj silindi.');
            }
        }

        async function adminDelMarker(markerId, markerName, btn) {
            if(!confirm(`"${markerName}" yerini silmek istediÄŸine emin misin?`)) return;
            btn.disabled = true; btn.textContent = '...';
            const res = await sendAction('admin_delete_marker_by_id', {marker_id: markerId});
            if(res && res.status === 'ok') {
                btn.closest('.rounded-xl').style.opacity = '0.2';
                showToast('ğŸ“ Yer silindi.');
            }
        }

        async function adminBanFromActivity() {
            if(!_uaCurrentUser) return;
            const reason = prompt(`${_uaCurrentUser} adlÄ± kullanÄ±cÄ±yÄ± banlamak iÃ§in sebep gir:`);
            if(!reason) return;
            const res = await sendAction('admin_ban_user', {username: _uaCurrentUser, reason});
            if(res && res.status === 'ok') {
                db.banned.push(_uaCurrentUser);
                document.getElementById('user-activity-modal').classList.add('hidden');
                showToast(`ğŸš¨ ${_uaCurrentUser} banlandÄ±.`);
                document.getElementById('astat-banned').textContent = db.banned.length;
            }
        }

        async function approvePrem(u, tier) { await sendAction('admin_approve_premium', {username: u, tier: tier}); showToast('âœ… Abonelik onaylandÄ±!'); showAdminPanel(); }
        async function rejectPrem(u) { await sendAction('admin_reject_premium', {username: u}); showToast('âŒ Abonelik reddedildi.'); showAdminPanel(); }
        async function toggleMaintenance() { const chk = document.getElementById("admin-maintenance").checked; await sendAction('toggle_maintenance', {status: chk}); showToast(chk ? 'ğŸ”§ BakÄ±m modu aÃ§Ä±ldÄ±' : 'âœ… BakÄ±m modu kapatÄ±ldÄ±'); }
        async function delMsg(id) { if(confirm("MesajÄ± sil?")) { await sendAction('delete_message', {id: id}); db.messages = db.messages.filter(m=>m.id!==id); renderChat(true); } }
        async function pinMsg(id) {
            const m = db.messages.find(x => x.id === id);
            if(m && m.type === "text") {
                await sendAction('pin_message', { text: m.text, user: m.user, expires: Date.now() + (24*60*60*1000) });
                showToast('ğŸ“Œ Mesaj 24 saat sabitlendi!');
            }
        }

        // ==== 3D Ã‡ARK MOTORU ====
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

            // DÄ±ÅŸ parlak halka
            const glowGrd = ctx.createRadialGradient(cx,cy,R-4,cx,cy,R+8);
            glowGrd.addColorStop(0,'rgba(234,179,8,0.0)');
            glowGrd.addColorStop(1,'rgba(234,179,8,0.35)');
            ctx.beginPath(); ctx.arc(cx,cy,R+6,0,Math.PI*2);
            ctx.fillStyle=glowGrd; ctx.fill();

            // Dilimleri Ã§iz
            prizes.forEach((p, i) => {
                // Ä°bre saat 12'de (Ã¼stte) â†’ -Math.PI/2 offset
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
                // KenarlÄ±k
                ctx.strokeStyle = isWinner ? '#fbbf24' : 'rgba(0,0,0,0.35)';
                ctx.lineWidth = isWinner ? 4 : 1.5;
                ctx.stroke();

                // ParlaklÄ±k efekti
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

            // DÃ¶nÃ¼ÅŸ hÄ±zÄ± gÃ¶rsel â€” Ã§ark dÃ¶nerken radyal Ã§izgiler
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

            // Kazanan dilim etrafÄ±nda parlayan halka
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
            el.textContent = left > 0 ? `${left} hak kaldÄ±` : 'BugÃ¼n bitti';
            el.className = left > 0
                ? 'text-[10px] text-green-400 font-bold uppercase tracking-widest text-right'
                : 'text-[10px] text-sky-300 font-bold uppercase tracking-widest text-right';
        }

        async function spinWheelAction() {
            const btn = document.getElementById('spin-btn');
            if(btn.disabled || _wheelSpinning) return;
            btn.disabled = true;
            _wheelSpinning = true;
            btn.innerText = "DÃ–NÃœYOR...";
            haptic([20,10,20,10,20]);

            try {
                const res = await sendAction('daily_spin', {});
                if(res.status !== 'ok') {
                    alert(res.message);
                    btn.disabled = false;
                    _wheelSpinning = false;
                    btn.innerText = "Ã‡ARKI Ã‡EVÄ°R";
                    return;
                }

                const prizes = window.WHEEL_PRIZES || [];
                const prizeIndex = prizes.findIndex(p => p.id === res.prize_id);
                const n = prizes.length;
                if(prizeIndex < 0 || n === 0) { alert("Hata: Ã¶dÃ¼l bulunamadÄ±."); return; }

                const sliceAngle = (Math.PI * 2) / n;

                // Ä°bre Ã¼stte (saat 12 = -Math.PI/2).
                // Kazanan dilim index=prizeIndex, merkezinin aÃ§Ä±sÄ±: prizeIndex*sliceAngle + sliceAngle/2
                // Bunu Ã¼ste getirmek iÃ§in: _wheelAngle = -(prizeIndex*sliceAngle + sliceAngle/2)
                // Ama mevcut _wheelAngle'dan devam etmeli + en az 8 tam tur dÃ¶nsÃ¼n
                const currentNorm = ((_wheelAngle % (Math.PI*2)) + Math.PI*2) % (Math.PI*2);
                const targetSliceCenter = prizeIndex * sliceAngle + sliceAngle / 2;
                // Hedef: Ã§arkÄ±n aÃ§Ä±sÄ± = -targetSliceCenter (yani o dilim tam Ã¼ste gelsin)
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

                // Ã‡arkÄ± dÃ¶nerken parlat
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

                    // 3D tilt â€” sadece orta hÄ±zda belirgin, baÅŸta ve sonda sÄ±fÄ±r
                    const tiltEnvelope = Math.sin(t * Math.PI); // 0â†’1â†’0
                    const tiltX = Math.sin(elapsed * 0.004) * tiltEnvelope * 12;
                    if(canvas) {
                        canvas.style.transform = `rotateX(${tiltX}deg)`;
                        _drawWheel3D(canvas, _wheelAngle);
                    }

                    // Slice sÄ±nÄ±rÄ±na gÃ¶re tick sesi (gerÃ§ekÃ§i tÄ±k-tÄ±k)
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
                        // Kazanan dilimi vurgula + kÄ±sa pulse animasyonu
                        _winnerIndex = prizeIndex;
                        _drawWheel3D(canvas, _wheelAngle);

                        // Kazanan iÃ§in 3 kez kÄ±sa parlama
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
                        btn.innerText = "Ã‡ARKI Ã‡EVÄ°R";

                        // Win sound + confetti
                        const winSound = document.getElementById('spin-win-sound');
                        if(winSound) { winSound.currentTime=0; try{winSound.play().catch(()=>{});}catch(e){} }
                        haptic([100,50,100,50,200]);
                        showSpinConfetti();

                        setTimeout(async () => {
                            // GÃ¼zel sonuÃ§ banner'Ä± gÃ¶ster
                            showSpinResult(res.prize_name);
                            // loadData yerine sadece spin sayacÄ±nÄ± ve XP'yi local gÃ¼ncelle
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
                btn.innerText = "Ã‡ARKI Ã‡EVÄ°R";
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
                <div style="font-size:56px;margin-bottom:12px;display:inline-block;animation:bounce 0.55s ease-in-out infinite alternate;">ğŸ‰</div>
                <div style="color:#fbbf24;font-size:11px;font-weight:900;text-transform:uppercase;letter-spacing:0.2em;margin-bottom:6px;">Tebrikler!</div>
                <div style="color:#ffffff;font-size:32px;font-weight:900;letter-spacing:0.05em;text-shadow:0 0 20px rgba(234,179,8,0.8);">${prizeName}</div>
                <div style="color:#a1a1aa;font-size:11px;margin-top:8px;font-weight:600;">HesabÄ±na eklendi!</div>
                <button onclick="document.getElementById('spin-result-banner').remove()" style="margin-top:24px;background:linear-gradient(135deg,#eab308,#b45309);color:#000;border:none;border-radius:14px;padding:14px 32px;font-size:15px;font-weight:900;cursor:pointer;text-transform:uppercase;letter-spacing:0.1em;width:100%;">HARIKA! âœ“</button>
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
        // ÅÄ°FRE SIFIRLAMA (FORGOT PASSWORD)
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
            if(!email) return alert("LÃ¼tfen kayÄ±tlÄ± e-posta adresinizi girin!");
            try {
                const res = await sendAction('request_reset', { email: email });
                if(res.status === 'ok') {
                    alert("SÄ±fÄ±rlama kodu e-postanÄ±za gÃ¶nderildi!");
                    document.getElementById("fp-step-1").classList.add("hidden");
                    document.getElementById("fp-step-2").classList.remove("hidden");
                }
            } catch(e) {}
        }

        async function submitNewPassword() {
            const email = document.getElementById("fp-email").value.trim();
            const code = document.getElementById("fp-code").value.trim();
            const newPw = document.getElementById("fp-new-password").value.trim();
            
            if(!code || !newPw) return alert("Kod ve yeni ÅŸifre boÅŸ bÄ±rakÄ±lamaz!");
            if(newPw.length < 4) return alert("Åifre en az 4 karakter olmalÄ±dÄ±r.");
            
            try {
                await sendAction('reset_password_code', { email: email, code: code, new_password: newPw });
                
                // KayÄ±tlÄ± kullanÄ±cÄ± varsa yeni ÅŸifreyi encode ederek gÃ¼ncelle
                if (localStorage.getItem("fr_remembered_username")) {
                    localStorage.setItem("fr_remembered_password", btoa(unescape(encodeURIComponent(newPw))));
                }
                const loginPassInput = document.getElementById("login-password");
                if(loginPassInput) loginPassInput.value = newPw;

                alert("Åifreniz baÅŸarÄ±yla gÃ¼ncellendi! ArtÄ±k yeni ÅŸifrenizle giriÅŸ yapabilirsiniz.");
                document.getElementById("forgot-password-modal").classList.add("hidden");
            } catch(e) { }
        }

    </script>

    <!-- ============================================================ -->
    <!-- STORY MODALLARI -->
    <!-- ============================================================ -->
    <div id="story-view-modal" class="hidden fixed inset-0 bg-black z-[99998] flex flex-col">
        <div class="absolute top-4 left-4 right-4 flex gap-1 z-10" id="story-progress-bars"></div>
        <button onclick="closeStoryView()" class="absolute top-10 right-4 z-20 w-10 h-10 bg-black/60 rounded-full text-white text-xl flex items-center justify-center">âœ•</button>
        <div id="story-view-user" class="absolute top-12 left-4 flex items-center gap-3 z-20">
            <img id="story-view-avatar" class="w-10 h-10 rounded-full border-2 border-sky-400 object-cover" src="">
            <div>
                <div id="story-view-username" class="text-white font-bold text-sm"></div>
                <div id="story-view-time" class="text-zinc-400 text-[10px]"></div>
            </div>
        </div>
        <img id="story-view-img" class="w-full h-full object-contain" src="" style="display:none;">
        <div id="story-view-text" class="flex-1 flex items-center justify-center p-8 text-center">
            <div id="story-view-text-content" class="text-white text-xl font-bold leading-relaxed"></div>
        </div>
        <div id="story-view-viewers" class="absolute bottom-6 left-0 right-0 flex flex-col items-center gap-2">
            <div class="bg-black/60 backdrop-blur px-4 py-2 rounded-full text-zinc-400 text-xs font-bold" id="story-viewer-count"></div>
            <button id="story-delete-btn" onclick="deleteCurrentStory()" class="hidden bg-sky-700/80 backdrop-blur px-5 py-2 rounded-full text-white text-xs font-bold border border-sky-400/50">ğŸ—‘ï¸ Story'yi Sil</button>
        </div>
    </div>

    <div id="add-story-modal" class="hidden fixed inset-0 modal-backdrop flex items-center justify-center z-[9999] px-4">
        <div class="glass-panel w-full max-w-sm rounded-3xl p-6 border border-zinc-700 shadow-2xl scale-in-anim">
            <div class="flex items-center justify-between mb-5">
                <h3 class="text-3xl text-white teko-font tracking-wide">ğŸ“¸ Story PaylaÅŸ</h3>
                <button onclick="document.getElementById('add-story-modal').classList.add('hidden')" class="w-8 h-8 bg-zinc-800 rounded-full text-zinc-400 hover:text-white flex items-center justify-center">âœ•</button>
            </div>
            <p class="text-[10px] text-yellow-500 font-bold uppercase tracking-widest mb-4 flex items-center gap-1"><span class="animate-pulse">â­</span> Standart, Deluxe ve Ultra+ Ã¼yelere Ã¶zel Â· 24 saat sonra silinir</p>
            <textarea id="story-text-input" placeholder="Ne dÃ¼ÅŸÃ¼nÃ¼yorsun? Nerede sÃ¼rdÃ¼n?" class="w-full bg-black/60 border border-zinc-700 rounded-xl px-4 py-3 h-24 text-white text-sm outline-none focus:border-sky-400 transition custom-scrollbar mb-3" maxlength="200"></textarea>
            <input id="story-photo-input" type="file" accept="image/*" class="w-full bg-black/60 border border-zinc-700 rounded-xl px-3 py-3 text-xs text-zinc-300 cursor-pointer mb-4">
            <div class="grid grid-cols-2 gap-3">
                <button onclick="document.getElementById('add-story-modal').classList.add('hidden')" class="bg-zinc-900 border border-zinc-700 text-zinc-400 py-3 rounded-xl font-bold text-sm transition hover:bg-zinc-800">Ä°ptal</button>
                <button onclick="submitStory()" class="bg-gradient-to-r from-sky-700 to-sky-500 text-white py-3 rounded-xl font-bold text-sm btn-premium-hover shadow-[0_0_15px_rgba(14,165,233,0.4)]">PAYLAÅ</button>
            </div>
        </div>
    </div>

    <!-- YORUM MODALI -->
    <div id="comment-modal" class="hidden fixed inset-0 modal-backdrop flex items-center justify-center z-[9999] px-4">
        <div class="glass-panel w-full max-w-md rounded-3xl border border-zinc-700 shadow-2xl scale-in-anim max-h-[80vh] flex flex-col">
            <div class="p-5 border-b border-zinc-800 flex items-center justify-between shrink-0">
                <h3 class="text-2xl text-white teko-font tracking-wide" id="comment-modal-title">ğŸ’¬ Yorumlar</h3>
                <button onclick="document.getElementById('comment-modal').classList.add('hidden')" class="w-8 h-8 bg-zinc-800 rounded-full text-zinc-400 hover:text-white flex items-center justify-center">âœ•</button>
            </div>
            <div id="comment-list" class="flex-1 overflow-y-auto p-4 space-y-3 custom-scrollbar"></div>
            <div class="p-3 border-t border-zinc-800 shrink-0 flex gap-2">
                <input id="comment-input" type="text" placeholder="Yorumunu yaz..." maxlength="200" class="flex-1 bg-black/60 border border-zinc-700 rounded-xl px-4 py-3 text-white text-sm outline-none focus:border-sky-400 transition">
                <button onclick="submitComment()" class="bg-white hover:bg-gray-200 text-black px-4 py-3 rounded-xl font-bold text-sm btn-premium-hover">GÃ¶nder</button>
            </div>
        </div>
    </div>

    <!-- SEVÄ°YE ATLAMA KUTLAMA OVERLAYÄ° -->
    <div id="levelup-overlay" class="hidden fixed inset-0 pointer-events-none z-[99997] flex items-center justify-center">
        <div id="levelup-card" class="bg-gradient-to-br from-yellow-600/90 to-amber-500/90 backdrop-blur-md rounded-3xl p-8 text-center border border-yellow-400/50 shadow-[0_0_60px_rgba(234,179,8,0.8)] level-up-anim max-w-xs w-full mx-4">
            <div class="text-6xl mb-3" id="levelup-icon">ğŸ†</div>
            <div class="text-white text-[10px] font-black uppercase tracking-[0.2em] mb-1">SEVÄ°YE ATLAMA!</div>
            <div class="text-black font-black text-3xl teko-font tracking-wide" id="levelup-name">Åampiyon</div>
            <div class="text-black/70 text-xs mt-2 font-bold" id="levelup-desc">Tebrikler! Yeni Ã¼nvanÄ±na ulaÅŸtÄ±n.</div>
        </div>
    </div>

    <!-- Ã–NCELÄ°KLÄ° DESTEK MODALI -->
    <div id="support-modal" class="hidden fixed inset-0 modal-backdrop flex items-center justify-center z-[9999] px-4">
        <div class="glass-panel w-full max-w-sm rounded-3xl p-6 border border-zinc-700 shadow-2xl scale-in-anim">
            <div class="flex items-center justify-between mb-5">
                <h3 class="text-2xl text-white teko-font tracking-wide">ğŸ§ Destek</h3>
                <button onclick="document.getElementById('support-modal').classList.add('hidden')" class="w-8 h-8 bg-zinc-800 rounded-full text-zinc-400 hover:text-white flex items-center justify-center">âœ•</button>
            </div>
            <div id="support-priority-badge" class="mb-4 text-center py-2 rounded-xl text-xs font-black uppercase tracking-widest"></div>
            <textarea id="support-message" placeholder="Sorununu veya Ã¶nerini yaz..." class="w-full bg-black/60 border border-zinc-700 rounded-xl px-4 py-3 h-28 text-white text-sm outline-none focus:border-sky-400 transition custom-scrollbar mb-4"></textarea>
            <div class="grid grid-cols-2 gap-3">
                <button onclick="document.getElementById('support-modal').classList.add('hidden')" class="bg-zinc-900 border border-zinc-700 text-zinc-400 py-3 rounded-xl font-bold text-sm">Ä°ptal</button>
                <button onclick="submitSupport()" class="bg-gradient-to-r from-sky-700 to-sky-500 text-white py-3 rounded-xl font-bold text-sm btn-premium-hover">GÃ–NDER</button>
            </div>
        </div>
    </div>

    <!-- TEHLÄ°KE BÄ°LDÄ°R MODALI -->
    <div id="danger-modal" class="hidden fixed inset-0 modal-backdrop flex items-center justify-center z-[9999] px-4">
        <div class="glass-panel w-full max-w-sm rounded-3xl p-6 border border-sky-900/50 shadow-2xl scale-in-anim">
            <div class="flex items-center justify-between mb-4">
                <h3 class="text-2xl text-sky-300 teko-font tracking-wide">âš ï¸ Tehlike Bildir</h3>
                <button onclick="document.getElementById('danger-modal').classList.add('hidden')" class="w-8 h-8 bg-zinc-800 rounded-full text-zinc-400 hover:text-white flex items-center justify-center">âœ•</button>
            </div>
            <p class="text-xs text-zinc-400 mb-4">Bu rampada bir tehlike mi var? KapalÄ± mÄ±, hasar mÄ± var? Bildirin, topluluk uyarÄ±lsÄ±n.</p>
            <div class="grid grid-cols-2 gap-2 mb-4">
                <button onclick="setDangerReason('Rampa kapalÄ±')" class="bg-zinc-900 border border-zinc-700 hover:border-sky-500 transition text-zinc-300 py-2.5 rounded-xl text-xs font-bold">ğŸš« KapalÄ±</button>
                <button onclick="setDangerReason('Hasar var / tehlikeli')" class="bg-zinc-900 border border-zinc-700 hover:border-sky-500 transition text-zinc-300 py-2.5 rounded-xl text-xs font-bold">ğŸ’¥ HasarlÄ±</button>
                <button onclick="setDangerReason('YÃ¼zey Ä±slak / kaygan')" class="bg-zinc-900 border border-zinc-700 hover:border-sky-500 transition text-zinc-300 py-2.5 rounded-xl text-xs font-bold">ğŸ’§ Kaygan</button>
                <button onclick="setDangerReason('Engel var / yol kapalÄ±')" class="bg-zinc-900 border border-zinc-700 hover:border-sky-500 transition text-zinc-300 py-2.5 rounded-xl text-xs font-bold">ğŸš§ Engel</button>
            </div>
            <textarea id="danger-reason-input" placeholder="Detay ekle (isteÄŸe baÄŸlÄ±)..." class="w-full bg-black/60 border border-zinc-700 rounded-xl px-4 py-3 h-20 text-white text-sm outline-none focus:border-sky-400 transition custom-scrollbar mb-4"></textarea>
            <div class="grid grid-cols-2 gap-3">
                <button onclick="document.getElementById('danger-modal').classList.add('hidden')" class="bg-zinc-900 border border-zinc-700 text-zinc-400 py-3 rounded-xl font-bold text-sm">Ä°ptal</button>
                <button onclick="submitDangerReport()" class="bg-sky-800 hover:bg-sky-700 text-white py-3 rounded-xl font-bold text-sm btn-premium-hover">BÄ°LDÄ°R</button>
            </div>
        </div>
    </div>

    <!-- KULLANICI ÅÄ°KAYET MODALI -->
    <div id="report-user-modal" class="hidden fixed inset-0 modal-backdrop flex items-center justify-center z-[99999] px-4">
        <div class="glass-panel w-full max-w-sm rounded-3xl p-6 border border-orange-900/50 shadow-2xl scale-in-anim">
            <div class="flex items-center justify-between mb-4">
                <h3 class="text-2xl text-orange-400 teko-font tracking-wide">&#128680; KullanÄ±cÄ± Sikayet Et</h3>
                <button onclick="document.getElementById('report-user-modal').classList.add('hidden')" class="w-8 h-8 bg-zinc-800 rounded-full text-zinc-400 hover:text-white flex items-center justify-center">&#10005;</button>
            </div>
            <p class="text-xs text-zinc-400 mb-4"><b id="report-user-target-label" class="text-orange-400"></b> adli kullaniciyi neden sikayet ediyorsunuz?</p>
            <div class="grid grid-cols-2 gap-2 mb-4">
                <button onclick="setReportReason('Taciz / Zorbalik')" class="bg-zinc-900 border border-zinc-700 hover:border-orange-600 transition text-zinc-300 py-2.5 rounded-xl text-xs font-bold">Taciz</button>
                <button onclick="setReportReason('Uygunsuz Icerik')" class="bg-zinc-900 border border-zinc-700 hover:border-orange-600 transition text-zinc-300 py-2.5 rounded-xl text-xs font-bold">Uygunsuz</button>
                <button onclick="setReportReason('Spam / Bot')" class="bg-zinc-900 border border-zinc-700 hover:border-orange-600 transition text-zinc-300 py-2.5 rounded-xl text-xs font-bold">Spam</button>
                <button onclick="setReportReason('Sahte Hesap')" class="bg-zinc-900 border border-zinc-700 hover:border-orange-600 transition text-zinc-300 py-2.5 rounded-xl text-xs font-bold">Sahte Hesap</button>
                <button onclick="setReportReason('Nefret Soylemi')" class="bg-zinc-900 border border-zinc-700 hover:border-orange-600 transition text-zinc-300 py-2.5 rounded-xl text-xs font-bold">Nefret Soylemi</button>
                <button onclick="setReportReason('Diger')" class="bg-zinc-900 border border-zinc-700 hover:border-orange-600 transition text-zinc-300 py-2.5 rounded-xl text-xs font-bold">Diger</button>
            </div>
            <textarea id="report-user-detail" placeholder="Ek aciklama (istege bagli)..." class="w-full bg-black/60 border border-zinc-700 rounded-xl px-4 py-3 h-16 text-white text-sm outline-none focus:border-orange-500 transition custom-scrollbar mb-4"></textarea>
            <div class="grid grid-cols-2 gap-3">
                <button onclick="document.getElementById('report-user-modal').classList.add('hidden')" class="bg-zinc-900 border border-zinc-700 text-zinc-400 py-3 rounded-xl font-bold text-sm">Iptal</button>
                <button onclick="submitReportUser()" class="bg-orange-800 hover:bg-orange-700 text-white py-3 rounded-xl font-bold text-sm btn-premium-hover">SIKAYET ET</button>
            </div>
        </div>
    </div>

    <!-- MESAJ SIKAYET MODALI -->
    <div id="report-msg-modal" class="hidden fixed inset-0 modal-backdrop flex items-center justify-center z-[99999] px-4">
        <div class="glass-panel w-full max-w-sm rounded-3xl p-6 border border-orange-900/50 shadow-2xl scale-in-anim">
            <div class="flex items-center justify-between mb-4">
                <h3 class="text-2xl text-orange-400 teko-font tracking-wide">&#128680; Mesaji Sikayet Et</h3>
                <button onclick="document.getElementById('report-msg-modal').classList.add('hidden')" class="w-8 h-8 bg-zinc-800 rounded-full text-zinc-400 hover:text-white flex items-center justify-center">&#10005;</button>
            </div>
            <div id="report-msg-preview" class="bg-black/60 border border-zinc-700 rounded-xl p-3 mb-4 text-zinc-300 text-xs italic break-words"></div>
            <div class="grid grid-cols-2 gap-2 mb-4">
                <button onclick="setMsgReportReason('Taciz / Zorbalik')" class="bg-zinc-900 border border-zinc-700 hover:border-orange-600 transition text-zinc-300 py-2.5 rounded-xl text-xs font-bold">Taciz</button>
                <button onclick="setMsgReportReason('Uygunsuz Icerik')" class="bg-zinc-900 border border-zinc-700 hover:border-orange-600 transition text-zinc-300 py-2.5 rounded-xl text-xs font-bold">Uygunsuz</button>
                <button onclick="setMsgReportReason('Spam / Reklam')" class="bg-zinc-900 border border-zinc-700 hover:border-orange-600 transition text-zinc-300 py-2.5 rounded-xl text-xs font-bold">Spam</button>
                <button onclick="setMsgReportReason('Nefret Soylemi')" class="bg-zinc-900 border border-zinc-700 hover:border-orange-600 transition text-zinc-300 py-2.5 rounded-xl text-xs font-bold">Nefret</button>
            </div>
            <div class="grid grid-cols-2 gap-3">
                <button onclick="document.getElementById('report-msg-modal').classList.add('hidden')" class="bg-zinc-900 border border-zinc-700 text-zinc-400 py-3 rounded-xl font-bold text-sm">Iptal</button>
                <button onclick="submitReportMsg()" class="bg-orange-800 hover:bg-orange-700 text-white py-3 rounded-xl font-bold text-sm btn-premium-hover">SIKAYET ET</button>
            </div>
        </div>
    </div>

    <!-- TAM EKRAN FOTOGRAF GORUNTULEME -->
    <div id="fullscreen-img-modal" class="hidden fixed inset-0 bg-black z-[99999] flex items-center justify-center" onclick="closeFullscreenImg()">
        <button class="absolute top-4 right-4 z-10 w-10 h-10 bg-black/60 rounded-full text-white text-xl flex items-center justify-center border border-zinc-700">âœ•</button>
        <div class="absolute top-4 left-4 flex gap-2 z-10" id="fullscreen-nav">
            <button onclick="event.stopPropagation(); fullscreenPrev()" class="w-10 h-10 bg-black/60 rounded-full text-white text-lg flex items-center justify-center border border-zinc-700">â€¹</button>
            <button onclick="event.stopPropagation(); fullscreenNext()" class="w-10 h-10 bg-black/60 rounded-full text-white text-lg flex items-center justify-center border border-zinc-700">â€º</button>
        </div>
        <img id="fullscreen-img" src="" class="max-w-full max-h-full object-contain select-none" style="touch-action:pinch-zoom;">
        <div id="fullscreen-counter" class="absolute bottom-6 left-1/2 -translate-x-1/2 bg-black/60 text-white text-xs px-3 py-1 rounded-full font-bold"></div>
    </div>

    <!-- REEL YÃœKLEME MODALI -->
    <div id="reel-upload-modal" class="hidden fixed inset-0 modal-backdrop flex items-center justify-center z-[99999] px-4 backdrop-blur-md">
        <div class="glass-panel w-full max-w-sm rounded-3xl p-6 border border-pink-900/50 shadow-2xl scale-in-anim">
            <div class="flex items-center justify-between mb-5">
                <h3 class="text-3xl text-white teko-font tracking-wide">ğŸ¬ REEL PAYLAÅ</h3>
                <button onclick="document.getElementById('reel-upload-modal').classList.add('hidden')" class="w-8 h-8 bg-zinc-800 rounded-full text-zinc-400 hover:text-white flex items-center justify-center">âœ•</button>
            </div>

            <!-- Ãœyelik bilgisi -->
            <div id="reel-limit-info" class="bg-zinc-900/80 border border-zinc-700 rounded-xl p-3 mb-4 text-xs text-zinc-400 font-bold"></div>

            <!-- Medya seÃ§imi -->
            <div class="grid grid-cols-2 gap-3 mb-4">
                <!-- Reel medya seÃ§imi â€” Prominent Disclosure ile aÃ§Ä±lÄ±r -->
                <button id="reel-photo-btn" onclick="_showPhotoDisclosure('reel', () => document.getElementById('reel-photo-input').click())" class="flex flex-col items-center justify-center gap-2 bg-zinc-900 border-2 border-pink-600/50 rounded-xl p-4 cursor-pointer hover:bg-pink-900/20 transition">
                    <span class="text-3xl">ğŸ“¸</span>
                    <span class="text-xs font-black text-white uppercase tracking-widest">FotoÄŸraf</span>
                </button>
                <input type="file" id="reel-photo-input" accept="image/*" class="hidden" onchange="handleReelFile(this,'image')">
                <button id="reel-video-btn" onclick="_showPhotoDisclosure('reel', () => document.getElementById('reel-video-input').click())" class="flex flex-col items-center justify-center gap-2 bg-zinc-900 border-2 border-zinc-700 rounded-xl p-4 cursor-pointer hover:bg-zinc-800 transition">
                    <span class="text-3xl">ğŸ¥</span>
                    <span class="text-xs font-black text-white uppercase tracking-widest">Video</span>
                    <span class="text-[9px] text-zinc-500 font-bold">Standart+ gerekli</span>
                </button>
                <input type="file" id="reel-video-input" accept="video/*" class="hidden" onchange="handleReelFile(this,'video')">
            </div>

            <!-- Ã–nizleme -->
            <div id="reel-preview-container" class="hidden mb-4 rounded-xl overflow-hidden bg-black border border-zinc-700 relative" style="max-height:200px">
                <img id="reel-preview-img" class="hidden w-full object-cover" style="max-height:200px">
                <video id="reel-preview-video" class="hidden w-full" style="max-height:200px" controls muted playsinline></video>
                <button onclick="clearReelFile()" class="absolute top-2 right-2 w-7 h-7 bg-black/70 rounded-full text-white text-xs flex items-center justify-center border border-zinc-600">âœ•</button>
                <div id="reel-compress-info" class="absolute bottom-2 left-2 bg-black/70 text-green-400 text-[9px] font-bold px-2 py-1 rounded-lg hidden">âœ“ Optimize edildi</div>
            </div>

            <textarea id="reel-caption" placeholder="AÃ§Ä±klama ekle... #downhill #freeride" class="w-full bg-black/60 border border-zinc-700 rounded-xl px-4 py-3 h-16 text-white text-sm outline-none focus:border-pink-500 transition custom-scrollbar mb-4 font-medium resize-none"></textarea>

            <div id="reel-upload-progress" class="hidden mb-3">
                <div class="text-xs text-zinc-400 font-bold mb-1 text-center">YÃ¼kleniyor...</div>
                <div class="w-full bg-zinc-800 rounded-full h-2"><div id="reel-progress-bar" class="bg-gradient-to-r from-pink-600 to-sky-400 h-2 rounded-full transition-all" style="width:0%"></div></div>
            </div>

            <div class="grid grid-cols-2 gap-3">
                <button onclick="document.getElementById('reel-upload-modal').classList.add('hidden')" class="bg-zinc-900 border border-zinc-700 text-zinc-400 py-3 rounded-xl font-bold text-sm">Ä°ptal</button>
                <button onclick="submitReel()" id="reel-submit-btn" class="bg-gradient-to-r from-pink-700 to-sky-500 hover:opacity-90 text-white py-3 rounded-xl font-black text-sm tracking-widest btn-premium-hover shadow-[0_0_15px_rgba(236,72,153,0.4)]">PAYLAÅ</button>
            </div>
        </div>
    </div>

    <!-- Reel Yorum Modali -->
    <div id="reel-comment-modal" class="hidden fixed inset-0 modal-backdrop flex items-end justify-center z-[99999]">
        <div class="glass-panel w-full max-w-md rounded-t-3xl p-5 border-t border-zinc-700 shadow-2xl" style="max-height:70vh;display:flex;flex-direction:column;">
            <div class="flex items-center justify-between mb-4 shrink-0">
                <h3 class="text-xl text-white teko-font tracking-wide">ğŸ’¬ Yorumlar</h3>
                <button onclick="document.getElementById('reel-comment-modal').classList.add('hidden')" class="w-8 h-8 bg-zinc-800 rounded-full text-zinc-400 hover:text-white flex items-center justify-center">âœ•</button>
            </div>
            <div id="reel-comments-list" class="flex-1 overflow-y-auto custom-scrollbar space-y-3 mb-4 pr-1"></div>
            <div class="flex gap-2 shrink-0">
                <input id="reel-comment-input" type="text" placeholder="Yorum yaz..." class="flex-1 bg-black/60 border border-zinc-700 rounded-xl px-4 py-3 text-white text-sm outline-none focus:border-pink-500 transition font-medium">
                <button onclick="submitReelComment()" class="bg-pink-700 hover:bg-pink-600 text-white px-5 py-3 rounded-xl font-black text-sm btn-premium-hover">GÃ–NDER</button>
            </div>
        </div>
    </div>

    <!-- Trial Bitti Modali -->
    <div id="trial-expired-modal" class="hidden fixed inset-0 modal-backdrop flex items-center justify-center z-[99999] px-4">
        <div class="glass-panel w-full max-w-sm rounded-3xl p-7 border border-yellow-600/50 shadow-[0_0_50px_rgba(234,179,8,0.3)] text-center scale-in-anim">
            <div class="text-6xl mb-4">ğŸ”ï¸</div>
            <h2 class="text-3xl text-white teko-font tracking-wide mb-2">3 Gunluk Denemen Bitti!</h2>
            <p class="text-zinc-300 text-sm mb-2 leading-relaxed">Ultra+ deneyimin nasÄ±ldÄ±? SÄ±nÄ±rsÄ±z AI, Ã¶zel renkler, alev efekti ve Ã§ok daha fazlasÄ± seni bekliyor!</p>
            <div class="bg-black/40 rounded-2xl p-4 mb-5 border border-yellow-900/40">
                <div class="text-yellow-400 font-black text-sm uppercase tracking-widest mb-2">Ultra+ ile Neler KazanÄ±rsÄ±n?</div>
                <div class="text-left text-xs text-zinc-300 space-y-1">
                    <div>ğŸ‘‘ Ã–zel isim rengi ve efekt</div>
                    <div>ğŸ¤– SÄ±nÄ±rsÄ±z Freerider AI</div>
                    <div>ğŸ”¥ Alev/Buz profil efekti</div>
                    <div>ğŸ“ Sapphire harita ikonlarÄ±</div>
                    <div>ğŸ“¸ 10 bisiklet fotoÄŸrafÄ±</div>
                    <div>ğŸ“Œ Mesaj sabitleme</div>
                </div>
            </div>
            <button onclick="document.getElementById('trial-expired-modal').classList.add('hidden'); switchTab(6);" class="w-full bg-gradient-to-r from-yellow-600 to-amber-500 hover:opacity-90 text-black py-4 rounded-xl font-black text-base tracking-widest btn-premium-hover shadow-[0_0_20px_rgba(234,179,8,0.5)] mb-3">ğŸ‘‘ PLUS ALMAK Ä°STÄ°YORUM!</button>
            <button onclick="document.getElementById('trial-expired-modal').classList.add('hidden')" class="w-full bg-zinc-900 border border-zinc-700 hover:bg-zinc-800 text-zinc-400 py-3 rounded-xl font-bold text-sm transition">Daha Sonra</button>
        </div>
    </div>

    <!-- READY PLAYER ME AVATAR MODAL -->
    <div id="rpm-modal" class="hidden fixed inset-0 z-[99999] flex flex-col" style="background:#000;">
        <div class="flex items-center justify-between px-4 py-3 bg-zinc-950 border-b border-zinc-800 shrink-0">
            <div class="flex items-center gap-3">
                <span class="text-xl">ğŸ­</span>
                <span class="text-white font-black text-sm teko-font tracking-widest">3D AVATAR OLUÅTUR</span>
            </div>
            <button onclick="closeRpmModal()" class="w-9 h-9 bg-zinc-800 rounded-full text-zinc-400 hover:text-white flex items-center justify-center text-lg border border-zinc-700">âœ•</button>
        </div>
        <div id="rpm-loading" class="flex flex-col items-center justify-center flex-1 gap-4">
            <div class="w-12 h-12 rounded-full border-4 border-purple-900/40 border-t-purple-500 animate-spin"></div>
            <p class="text-zinc-400 text-sm font-bold">Avatar editÃ¶rÃ¼ yÃ¼kleniyor...</p>
        </div>
        <iframe id="rpm-iframe" class="hidden flex-1 w-full border-none" allow="camera *; microphone *"></iframe>
        <div class="px-4 py-3 bg-zinc-950 border-t border-zinc-800 shrink-0">
            <p class="text-[10px] text-zinc-500 text-center font-bold uppercase tracking-widest">AvatarÄ±nÄ± oluÅŸturduktan sonra "Kullan" butonuna bas â€” otomatik kaydedilir</p>
        </div>
    </div>

    <!-- ================================================================ -->
    <!-- GOOGLE PLAY PROMINENT DISCLOSURE â€” MÄ°KROFON Ä°ZNÄ° MODALI         -->
    <!-- Politika: getUserMedia() Ã§aÄŸrÄ±sÄ±ndan Ã–NCE gÃ¶sterilmesi zorunlu   -->
    <!-- ================================================================ -->
    <div id="pd-mic-modal" class="hidden fixed inset-0 z-[999999] flex items-center justify-center px-4" style="background:rgba(0,0,0,0.75);backdrop-filter:blur(6px)">
        <div class="glass-panel w-full max-w-sm rounded-3xl p-7 border border-sky-700/60 shadow-[0_0_50px_rgba(14,165,233,0.2)] scale-in-anim">
            <div class="flex flex-col items-center text-center gap-4">
                <div class="w-16 h-16 rounded-2xl bg-sky-900/60 border border-sky-600/50 flex items-center justify-center text-4xl shadow-lg">ğŸ¤</div>
                <div>
                    <h2 class="text-2xl text-white font-black tracking-wide mb-1">Mikrofon Ä°zni</h2>
                    <p class="text-xs text-sky-400 font-bold uppercase tracking-widest">Sesli Mesaj Ã–zelliÄŸi</p>
                </div>
                <div class="bg-black/50 rounded-2xl p-4 border border-zinc-700 text-left w-full space-y-2">
                    <p class="text-sm text-zinc-200 leading-relaxed">FreeriderTR, <strong class="text-white">sesli mesaj kaydedip gÃ¶ndermek</strong> iÃ§in mikrofonuna eriÅŸmek istiyor.</p>
                    <ul class="text-xs text-zinc-400 space-y-1.5 pt-1">
                        <li class="flex items-start gap-2"><span class="text-sky-400 shrink-0 mt-0.5">âœ”</span><span>Ses yalnÄ±zca kayÄ±t dÃ¼ÄŸmesine bastÄ±ÄŸÄ±nda alÄ±nÄ±r</span></li>
                        <li class="flex items-start gap-2"><span class="text-sky-400 shrink-0 mt-0.5">âœ”</span><span>KayÄ±t dÄ±ÅŸÄ±nda mikrofon hiÃ§bir zaman aktif olmaz</span></li>
                        <li class="flex items-start gap-2"><span class="text-sky-400 shrink-0 mt-0.5">âœ”</span><span>Ses verisi yalnÄ±zca mesaj olarak iletilir, baÅŸka amaÃ§la kullanÄ±lmaz</span></li>
                        <li class="flex items-start gap-2"><span class="text-zinc-500 shrink-0 mt-0.5">â“˜</span><span class="text-zinc-500">Ä°zni tarayÄ±cÄ± ayarlarÄ±ndan istediÄŸin zaman iptal edebilirsin</span></li>
                    </ul>
                </div>
                <div class="grid grid-cols-2 gap-3 w-full">
                    <button id="pd-mic-deny" class="bg-zinc-900 border border-zinc-700 hover:bg-zinc-800 text-zinc-400 py-3 rounded-xl font-bold text-sm transition">VazgeÃ§</button>
                    <button id="pd-mic-allow" class="bg-gradient-to-r from-sky-700 to-sky-500 hover:opacity-90 text-white py-3 rounded-xl font-black text-sm tracking-widest shadow-[0_0_15px_rgba(14,165,233,0.35)]">Ä°zin Ver</button>
                </div>
                <p class="text-[10px] text-zinc-600 leading-relaxed">"Ä°zin Ver"e basÄ±nca tarayÄ±cÄ±nÄ±n standart izin penceresi aÃ§Ä±lÄ±r. Orada da onaylaman gerekir.</p>
            </div>
        </div>
    </div>

    <!-- ================================================================ -->
    <!-- GOOGLE PLAY PROMINENT DISCLOSURE â€” FOTOÄRAF / GALERÄ° MODALI      -->
    <!-- Politika: file input tetiklenmeden Ã–NCE gÃ¶sterilmesi zorunlu      -->
    <!-- ================================================================ -->
    <div id="pd-photo-modal" class="hidden fixed inset-0 z-[999999] flex items-center justify-center px-4" style="background:rgba(0,0,0,0.75);backdrop-filter:blur(6px)">
        <div class="glass-panel w-full max-w-sm rounded-3xl p-7 border border-pink-700/60 shadow-[0_0_50px_rgba(236,72,153,0.15)] scale-in-anim">
            <div class="flex flex-col items-center text-center gap-4">
                <div class="w-16 h-16 rounded-2xl bg-pink-900/50 border border-pink-600/50 flex items-center justify-center text-4xl shadow-lg" id="pd-photo-icon">ğŸ“¸</div>
                <div>
                    <h2 class="text-2xl text-white font-black tracking-wide mb-1" id="pd-photo-title">FotoÄŸraf EriÅŸimi</h2>
                    <p class="text-xs text-pink-400 font-bold uppercase tracking-widest" id="pd-photo-subtitle">Galeri EriÅŸimi</p>
                </div>
                <div class="bg-black/50 rounded-2xl p-4 border border-zinc-700 text-left w-full space-y-2">
                    <p class="text-sm text-zinc-200 leading-relaxed" id="pd-photo-desc">FreeriderTR, seÃ§tiÄŸin fotoÄŸrafa eriÅŸmek iÃ§in galerini kullanacak.</p>
                    <ul class="text-xs text-zinc-400 space-y-1.5 pt-1" id="pd-photo-list"></ul>
                </div>
                <div class="grid grid-cols-2 gap-3 w-full">
                    <button id="pd-photo-deny" class="bg-zinc-900 border border-zinc-700 hover:bg-zinc-800 text-zinc-400 py-3 rounded-xl font-bold text-sm transition">VazgeÃ§</button>
                    <button id="pd-photo-allow" class="bg-gradient-to-r from-pink-700 to-rose-500 hover:opacity-90 text-white py-3 rounded-xl font-black text-sm tracking-widest shadow-[0_0_15px_rgba(236,72,153,0.3)]">Galeriye Git</button>
                </div>
                <p class="text-[10px] text-zinc-600 leading-relaxed">SeÃ§ilen medya yalnÄ±zca belirtilen amaÃ§la kullanÄ±lÄ±r ve Ã¼Ã§Ã¼ncÃ¼ taraflarla paylaÅŸÄ±lmaz.</p>
            </div>
        </div>
    </div>

    <!-- ================================================================ -->
    <!-- GOOGLE PLAY IAP â€” Android SatÄ±n Alma Callback'leri               -->
    <!-- ================================================================ -->
    <script>
    // Android Google Play SatÄ±n Alma Callback'leri
    function onGooglePurchaseSuccess(purchaseToken, subscriptionId) {
        fetch('/api/verify_google_purchase', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            credentials: 'include',
            body: JSON.stringify({
                purchaseToken: purchaseToken,
                productId: subscriptionId    // Python'Ä±n beklediÄŸi field adÄ±
            })
        })
        .then(r => r.json())
        .then(data => {
            if (data.status === 'ok') {
                location.reload();
            } else {
                alert("DoÄŸrulama hatasÄ±: " + (data.message || "Hata"));
            }
        })
        .catch(err => {
            alert("Sunucuya ulaÅŸÄ±lamadÄ±, tekrar dene.");
        });
    }

    // YENÄ°: Google Play Billing Event (clever-responder webhook doÄŸrulamasÄ±)
    window.onBillingEvent = async function(event, data) {
        if (event === "billing_success") {
            const purchaseInfo = JSON.parse(data);
            
            console.log("Ã–deme alÄ±ndÄ±, Google sunucularÄ±nda doÄŸrulanÄ±yor...");

            try {
                // DÄ°KKAT: URL sonu clever-responder olarak gÃ¼ncellendi!
                const response = await fetch("https://xrzepgscyuqsimicljmm.supabase.co/functions/v1/clever-responder", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({
                        purchaseToken: purchaseInfo.purchaseToken,
                        productId: purchaseInfo.productId,
                        userId: (typeof currentUser !== 'undefined' && currentUser) ? currentUser.username : "guest" 
                    })
                });

                const result = await response.json();

                if (result.success) {
                    alert("Tebrikler! Premium hesabÄ±nÄ±z aktif edildi.");
                    window.location.reload();
                } else {
                    alert("Ã–deme doÄŸrulanamadÄ±: " + result.message);
                }
            } catch (error) {
                console.error("DoÄŸrulama servisinde hata:", error);
            }
        } 
    };

    function onGooglePurchaseCancelled(msg) {
        console.log("SatÄ±n alma iptal edildi");
    }

    function onGooglePurchaseError(errorMessage) {
        alert("Ã–deme baÅŸarÄ±sÄ±z: " + errorMessage);
    }

    function handleBuyButton(productId) {
        if (typeof window.Android !== 'undefined' && window.Android !== null && typeof window.Android.launchBilling === 'function') {
            try {
                window.Android.launchBilling(productId);
            } catch(e) {
                console.error('[IAP] launchBilling hatasÄ±:', e);
                showToast('Ã–deme ekranÄ± aÃ§Ä±lamadÄ±. LÃ¼tfen uygulamayÄ± gÃ¼ncelleyin.');
            }
        } else {
            // Web / tarayÄ±cÄ± â†’ admin'e talep gÃ¶nder
            _sendWebPurchaseRequest(productId);
        }
    }

    // â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
    // ğŸ”¥ PREMIUM PROMOSYON POPUP (24 saatte 1 kez, login sonrasÄ± 30sn)
    // switchTab'dan da Ã§aÄŸrÄ±lÄ±r (session baÅŸÄ±na max 1 kez)
    // â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
    function showPremiumPopup() {
        // Premium kullanÄ±cÄ±lara gÃ¶sterme
        if (currentUser && currentUser.stats && parseInt(currentUser.stats.premium_tier) > 0) return;
        
        // 24 saatte 1 kez kontrolÃ¼
        const lastShown = localStorage.getItem('_fr_prem_popup_ts');
        if (lastShown && (Date.now() - parseInt(lastShown)) < 86400000) return;
        
        localStorage.setItem('_fr_prem_popup_ts', Date.now().toString());
        
        const popup = document.createElement('div');
        popup.id = 'premium-promo-popup';
        popup.className = 'premium-popup-overlay';
        popup.innerHTML = `
            <div class="premium-popup-card">
                <div style="font-size:48px;margin-bottom:12px;animation:premiumGlow 2s ease-in-out infinite">ğŸ”¥</div>
                <h2 style="font-size:22px;font-weight:900;margin-bottom:4px;background:linear-gradient(135deg,#eab308,#f97316,#ef4444);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;letter-spacing:1px">%50 Ä°NDÄ°RÄ°M KAZANDIN!</h2>
                <p style="color:#a1a1aa;font-size:12px;margin-bottom:20px;font-weight:500">SÄ±nÄ±rlÄ± sÃ¼reliÄŸine Premium avantajlarÄ±nÄ± keÅŸfet</p>
                
                <div style="text-align:left;margin-bottom:24px;padding:0 8px">
                    <div style="display:flex;align-items:center;gap:10px;margin-bottom:10px;color:#d4d4d8;font-size:13px;font-weight:600">
                        <span style="color:#22c55e;font-size:16px">âœ“</span> ReklamsÄ±z deneyim
                    </div>
                    <div style="display:flex;align-items:center;gap:10px;margin-bottom:10px;color:#d4d4d8;font-size:13px;font-weight:600">
                        <span style="color:#22c55e;font-size:16px">âœ“</span> Ã–zel profil renkleri & rozet
                    </div>
                    <div style="display:flex;align-items:center;gap:10px;margin-bottom:10px;color:#d4d4d8;font-size:13px;font-weight:600">
                        <span style="color:#22c55e;font-size:16px">âœ“</span> SÄ±nÄ±rsÄ±z AI sohbet
                    </div>
                    <div style="display:flex;align-items:center;gap:10px;margin-bottom:10px;color:#d4d4d8;font-size:13px;font-weight:600">
                        <span style="color:#22c55e;font-size:16px">âœ“</span> Video Reels paylaÅŸÄ±mÄ±
                    </div>
                    <div style="display:flex;align-items:center;gap:10px;color:#d4d4d8;font-size:13px;font-weight:600">
                        <span style="color:#22c55e;font-size:16px">âœ“</span> OnaylÄ± hesap rozeti
                    </div>
                </div>
                
                <button onclick="document.getElementById('premium-promo-popup').remove(); switchTab(6);" 
                    style="width:100%;padding:14px;border-radius:14px;border:none;font-weight:900;font-size:14px;text-transform:uppercase;letter-spacing:2px;cursor:pointer;
                    background:linear-gradient(135deg,#eab308,#f97316);color:#000;
                    box-shadow:0 4px 20px rgba(234,179,8,0.4);
                    transition:all 0.25s;margin-bottom:10px"
                    onmouseover="this.style.transform='translateY(-2px) scale(1.02)';this.style.boxShadow='0 8px 30px rgba(234,179,8,0.6)'"
                    onmouseout="this.style.transform='';this.style.boxShadow='0 4px 20px rgba(234,179,8,0.4)'">
                    ğŸš€ HEMEN AL
                </button>
                <button onclick="document.getElementById('premium-promo-popup').remove()" 
                    style="width:100%;padding:12px;border-radius:14px;border:1px solid #3f3f46;background:transparent;color:#71717a;font-weight:700;font-size:12px;cursor:pointer;transition:all 0.25s;text-transform:uppercase;letter-spacing:1px"
                    onmouseover="this.style.borderColor='#52525b';this.style.color='#a1a1aa'"
                    onmouseout="this.style.borderColor='#3f3f46';this.style.color='#71717a'">
                    Daha Sonra
                </button>
            </div>
        `;
        document.body.appendChild(popup);
        
        // Overlay'e tÄ±klayÄ±nca kapat
        popup.addEventListener('click', (e) => {
            if (e.target === popup) popup.remove();
        });
    }

    // Popup triggers removed per user request

    // --- ADMIN EXTRA FUNCTIONS ---
        async function execAdminCmd(cmdOverride) {
            const cmd = cmdOverride || document.getElementById('admin-cmd-input').value;
            if(!cmd) return;
            try {
                const res = await sendAction('admin_command', {command: cmd});
                if(res.status==='ok') { 
                    showToast(`âœ… BaÅŸarÄ±lÄ±: ${res.message}`, 'success', 4000); 
                    if(!cmdOverride && document.getElementById('admin-cmd-input')) document.getElementById('admin-cmd-input').value = ''; 
                }
                else showToast(`âŒ Hata: ${res.message}`, 'error', 4000);
            } catch(e) {
                showToast(`âŒ Hata: ${e.message}`, 'error');
            }
        }

        let _adminRepPage = 1;
        async function loadAdminReports(page = 1) {
            _adminRepPage = page;
            const status = document.getElementById('admin-report-status') ? document.getElementById('admin-report-status').value : 'pending';
            const severity = document.getElementById('admin-report-severity') ? document.getElementById('admin-report-severity').value : 'all';
            const list = document.getElementById('admin-reports-list');
            const pg = document.getElementById('admin-reports-pagination');
            if(!list) return;
            list.innerHTML = '<div class="text-zinc-600 text-xs italic text-center py-4 animate-pulse">YÃ¼kleniyor...</div>';
            try {
                const res = await fetch(`/admin/reports?status=${status}&severity=${severity}&page=${page}&per_page=15`);
                const data = await res.json();
                if (data.status !== 'ok') { list.innerHTML = `<div class="text-sky-300 text-xs italic text-center py-4">Hata: ${data.message}</div>`; return; }
                if (!data.reports || !data.reports.length) { list.innerHTML = '<div class="text-zinc-600 text-xs italic text-center py-4">Rapor bulunamadÄ±.</div>'; pg.innerHTML=''; return; }
                list.innerHTML = data.reports.map((r, i) => {
                    let borderClass = 'border-zinc-700';
                    if(r.severity === 'high') borderClass = 'border-red-500/50';
                    else if(r.severity === 'medium') borderClass = 'border-orange-500/50';
                    else if(r.severity === 'low') borderClass = 'border-yellow-500/50';
                    return `
                    <div class="rounded-xl p-4 border ${borderClass} admin-card-enter transition-all" style="background:rgba(0,0,0,0.45);animation-delay:${i*0.03}s">
                        <div class="flex justify-between items-center mb-2">
                            <div class="flex gap-2 items-center text-[10px] font-bold uppercase tracking-widest">
                                <span class="${r.severity==='high'?'text-red-400':(r.severity==='medium'?'text-orange-400':'text-yellow-400')}">${r.severity}</span>
                                <span class="text-zinc-500">|</span>
                                <span class="text-blue-300">${r.status}</span>
                            </div>
                            <span class="text-[9px] text-zinc-500">${new Date(r.created_at).toLocaleString('tr-TR')}</span>
                        </div>
                        <div class="text-white text-xs font-bold mb-2">ğŸ‘¤ ${r.sender}</div>
                        <div class="bg-black/60 p-3 rounded-lg border border-zinc-800 text-zinc-300 text-xs mb-3 break-words font-medium">${escHtml(r.content)}</div>
                        ${r.status === 'pending' ? `
                        <div class="flex gap-2">
                            <button onclick="repBan('${r.sender}','${r.id}')" class="flex-1 py-2 bg-red-950/40 border border-sky-900/50 text-sky-400 text-[10px] font-bold rounded-lg hover:bg-sky-900/40 transition">ğŸš« Onayla & Banla</button>
                            <button onclick="repDismiss('${r.id}')" class="flex-1 py-2 bg-zinc-800 border border-zinc-700 text-zinc-300 text-[10px] font-bold rounded-lg hover:bg-zinc-700 transition">âœ… Yoksay</button>
                        </div>` : ''}
                        ${r.admin_note ? `<div class="mt-2 text-[10px] text-amber-400 font-bold">ğŸ’¬ Not: ${escHtml(r.admin_note)}</div>` : ''}
                    </div>`;
                }).join('');
                pg.innerHTML = '';
                if (page > 1) pg.innerHTML += `<button onclick="loadAdminReports(${page-1})" class="px-3 py-1 bg-zinc-800 text-zinc-300 text-xs rounded-lg hover:bg-zinc-700">â—€ Ã–nceki</button>`;
                if (data.count === 15) pg.innerHTML += `<button onclick="loadAdminReports(${page+1})" class="px-3 py-1 bg-zinc-800 text-zinc-300 text-xs rounded-lg hover:bg-zinc-700">Sonraki â–¶</button>`;
            } catch(e) {
                list.innerHTML = `<div class="text-sky-300 text-xs italic text-center py-4">BaÄŸlantÄ± hatasÄ±: ${e.message}</div>`;
            }
        }

        async function repBan(username, reportId) {
            if (!confirm(`âš ï¸ "${username}" kullanÄ±cÄ±sÄ±nÄ± banlamak istediÄŸinizden emin misiniz?`)) return;
            const reason = prompt('Ban gerekÃ§esi (opsiyonel):', 'Topluluk kurallarÄ± ihlali') || 'Moderasyon ihlali';
            try {
                const data = await sendAction('admin_ban_user', { username, reason });
                if(data.status === 'ok') { showToast(`âœ… ${username} banlandÄ±.`, 'success'); loadAdminReports(_adminRepPage); }
                else showToast(`âŒ Hata: ${data.message}`, 'error');
            } catch(e) {}
        }
        async function repDismiss(reportId) {
            try {
                const res = await fetch('/admin/dismiss_report', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({ report_id: reportId }) });
                const data = await res.json();
                if(data.status === 'ok') { showToast(`âœ… Rapor yoksayÄ±ldÄ±.`, 'success'); loadAdminReports(_adminRepPage); }
            } catch(e) {}
        }

        async function adminResetPassword(uname) {
            if(!confirm(`âš ï¸ ${uname} ÅŸifresi sÄ±fÄ±rlanacak. OnaylÄ±yor musunuz?`)) return;
            try {
                const r = await sendAction('admin_reset_password', {username: uname});
                if(r.status==='ok') alert(`âœ… Åifre sÄ±fÄ±rlandÄ±.
Yeni Åifre: ${r.new_password}
Email Gitti: ${r.email_sent}`);
                else showToast(`âŒ Hata: ${r.message}`, 'error');
            } catch(e) {}
        }
        async function adminChangeUsername(uname) {
            const newName = prompt(`${uname} iÃ§in YENÄ° kullanÄ±cÄ± adÄ± girin:`);
            if(!newName) return;
            try {
                const r = await sendAction('admin_change_username', {old_username: uname, new_username: newName});
                if(r.status==='ok') { showToast(`âœ… DeÄŸiÅŸtirildi.`, 'success'); document.getElementById('ua-username-label').textContent = '@' + newName; _uaCurrentUser = newName; }
                else showToast(`âŒ Hata: ${r.message}`, 'error');
            } catch(e) {}
        }
        async function adminDeleteUser(uname) {
            if(!confirm(`ğŸš¨ DÄ°KKAT! ${uname} hesabÄ±nÄ± tamamen silmek Ã¼zeresiniz. Bu iÅŸlem GERÄ° ALINAMAZ! Emin misiniz?`)) return;
            try {
                const r = await sendAction('admin_delete_user', {username: uname});
                if(r.status==='ok') { showToast(`âœ… ${uname} silindi.`, 'success'); document.getElementById('user-activity-modal').classList.add('hidden'); }
                else showToast(`âŒ Hata: ${r.message}`, 'error');
            } catch(e) {}
        }

        // --- END ADMIN EXTRA FUNCTIONS ---


        // --- NEW ADMIN PANEL ACTIONS ---
        async function adminCheckUserDetails() {
            const username = document.getElementById('admin-action-username').value.trim();
            if(!username) { showToast('KullanÄ±cÄ± adÄ± girin!', 'warning'); return; }
            
            const btn = event && event.target && event.target.tagName === 'BUTTON' ? event.target : document.querySelector('button[onclick="adminCheckUserDetails()"]');
            const originalText = btn.innerHTML;
            btn.innerHTML = 'â³ AranÄ±yor...';
            
            try {
                const res = await sendAction('admin_check_user_details', {username});
                btn.innerHTML = originalText;
                
                if(res.status === 'ok') {
                    document.getElementById('admin-action-result').classList.remove('hidden');
                    const u = res.user;
                    const p = res.premium;
                    
                    document.getElementById('aa-username').textContent = u.username;
                    document.getElementById('aa-email').textContent = u.email;
                    document.getElementById('aa-date').textContent = u.created_at.substring(0, 10);
                    document.getElementById('aa-cityxp').textContent = `${u.city} / ${u.xp} XP`;
                    document.getElementById('aa-role').textContent = u.role;
                    
                    const banEl = document.getElementById('aa-banned');
                    const banBtn = document.getElementById('aa-btn-ban');
                    if(u.is_banned) {
                        banEl.textContent = 'âŒ BanlÄ±';
                        banEl.className = 'font-bold text-red-500';
                        banBtn.textContent = 'âœ… Unban';
                    } else {
                        banEl.textContent = 'âœ… Aktif';
                        banEl.className = 'font-bold text-green-500';
                        banBtn.textContent = 'ğŸš« Banla';
                    }
                    
                    const tEl = document.getElementById('aa-tier');
                    tEl.textContent = p.tier === 3 ? 'Ultra+' : (p.tier === 2 ? 'Deluxe' : (p.tier === 1 ? 'Standart' : 'Yok'));
                    tEl.className = p.tier > 0 ? 'font-bold text-yellow-400' : 'font-bold text-zinc-500';
                    
                    document.getElementById('aa-expire').textContent = p.expire_date;
                    document.getElementById('aa-source').textContent = p.source;
                } else {
                    showToast(`Hata: ${res.message}`, 'error');
                    document.getElementById('admin-action-result').classList.add('hidden');
                }
            } catch(e) {
                btn.innerHTML = originalText;
                showToast(`Hata: ${e.message}`, 'error');
            }
        }

        async function adminActionExec(actionSuffix) {
            const username = document.getElementById('aa-username').textContent;
            if(!username) return;
            try {
                const res = await sendAction('admin_command', {command: `${username} ${actionSuffix}`});
                if(res.status === 'ok') {
                    showToast(`âœ… ${res.message}`, 'success');
                    adminCheckUserDetails();
                } else {
                    showToast(`âŒ Hata: ${res.message}`, 'error');
                }
            } catch(e) {}
        }
        
        async function adminActionBanToggle() {
            const username = document.getElementById('aa-username').textContent;
            if(!username) return;
            const btn = document.getElementById('aa-btn-ban');
            const isBan = btn.textContent.includes('Banla');
            
            if(isBan) {
                if(!confirm(`âš ï¸ ${username} kullanÄ±cÄ±sÄ±nÄ± banlamak Ã¼zeresiniz!`)) return;
                const reason = prompt('Ban gerekÃ§esi:');
                try {
                    const data = await sendAction('admin_ban_user', { username, reason });
                    if(data.status === 'ok') { showToast('BanlandÄ±!', 'success'); adminCheckUserDetails(); }
                    else showToast(data.message, 'error');
                } catch(e) {}
            } else {
                try {
                    const data = await sendAction('admin_unban_user', { username });
                    if(data.status === 'ok') { showToast('Ban aÃ§Ä±ldÄ±!', 'success'); adminCheckUserDetails(); }
                    else showToast(data.message, 'error');
                } catch(e) {}
            }
        }
        // --- END NEW ADMIN PANEL ACTIONS ---

</script>


<!-- ========================================== -->
<!-- AI HUB (YENI NESÄ°L AI MERKEZI)             -->
<!-- ========================================== -->
<style>
  .ai-fab {
      position: fixed;
      bottom: 90px;
      right: 20px;
      width: 56px;
      height: 56px;
      border-radius: 50%;
      background: linear-gradient(135deg, #0ea5e9, #8b5cf6);
      box-shadow: 0 0 20px rgba(139, 92, 246, 0.6), inset 0 0 10px rgba(255,255,255,0.4);
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      z-index: 50;
      transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
      border: 2px solid rgba(255,255,255,0.2);
  }
  .ai-fab:hover {
      transform: scale(1.1) rotate(5deg);
      box-shadow: 0 0 30px rgba(139, 92, 246, 0.9);
  }
  .ai-fab svg { width: 28px; height: 28px; fill: white; filter: drop-shadow(0 2px 4px rgba(0,0,0,0.4)); }
  .ai-overlay {
      position: fixed; inset: 0; background: rgba(5,5,10,0.95); backdrop-filter: blur(20px); z-index: 999999 !important;
      display: none; flex-direction: column; opacity: 0; transition: opacity 0.3s ease;
  }
  .ai-overlay.show { display: flex !important; opacity: 1 !important; }
  .ai-header { padding: 20px; border-bottom: 1px solid rgba(139, 92, 246, 0.3); background: linear-gradient(180deg, rgba(139,92,246,0.1), transparent); display: flex; justify-content: space-between; align-items: center; }
  .ai-title { font-size: 24px; font-weight: 900; background: linear-gradient(90deg, #38bdf8, #a78bfa); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-transform: uppercase; letter-spacing: 2px; }
  .ai-close { background: rgba(255,255,255,0.1); border-radius: 50%; width: 36px; height: 36px; display: flex; align-items: center; justify-content: center; cursor: pointer; color: white; font-size: 20px; font-weight: bold; }
  .ai-content { flex: 1; overflow-y: auto; padding: 20px; }
  .ai-card {
      background: linear-gradient(145deg, rgba(30,30,40,0.8), rgba(15,15,20,0.9));
      border: 1px solid rgba(139, 92, 246, 0.2);
      border-radius: 20px; padding: 24px; margin-bottom: 16px;
      box-shadow: 0 10px 30px rgba(0,0,0,0.5);
      transition: all 0.3s ease; cursor: pointer; position: relative; overflow: hidden;
  }
  .ai-card::before {
      content:''; position: absolute; top:0; left:0; width:100%; height:100%;
      background: radial-gradient(circle at top right, rgba(139, 92, 246, 0.2), transparent 60%); pointer-events: none;
  }
  .ai-card:hover { transform: translateY(-5px); border-color: rgba(139, 92, 246, 0.6); box-shadow: 0 15px 40px rgba(139, 92, 246, 0.2); }
  .ai-card-title { font-size: 18px; font-weight: 800; color: #fff; margin-bottom: 8px; display: flex; align-items: center; gap: 8px; }
  .ai-card-desc { font-size: 13px; color: #a1a1aa; line-height: 1.5; }
  .ai-screen { display: none; flex-direction: column; height: 100%; }
  
  /* Input & Button Styles */
  .ai-input { width: 100%; background: rgba(0,0,0,0.5); border: 1px solid rgba(255,255,255,0.1); border-radius: 12px; padding: 14px 16px; color: white; font-size: 14px; margin-bottom: 12px; outline: none; transition: border 0.3s; }
  .ai-input:focus { border-color: #8b5cf6; box-shadow: 0 0 15px rgba(139, 92, 246, 0.3); }
  .ai-btn { width: 100%; background: linear-gradient(90deg, #0ea5e9, #8b5cf6); border: none; border-radius: 12px; padding: 16px; color: white; font-weight: 900; font-size: 14px; text-transform: uppercase; letter-spacing: 1px; cursor: pointer; box-shadow: 0 5px 20px rgba(139, 92, 246, 0.4); margin-bottom: 20px; transition: transform 0.2s; }
  .ai-btn:active { transform: scale(0.98); }
  
  /* Result Components */
  .ai-result-box { background: rgba(20,20,30,0.8); border-radius: 16px; border: 1px solid rgba(255,255,255,0.05); padding: 20px; margin-top: 10px; animation: slideUpFade 0.4s ease forwards; }
  .ai-score-ring { width: 80px; height: 80px; border-radius: 50%; border: 6px solid #8b5cf6; display: flex; align-items: center; justify-content: center; font-size: 24px; font-weight: 900; color: white; box-shadow: 0 0 20px rgba(139,92,246,0.5); margin: 0 auto 20px; background: rgba(0,0,0,0.5); }
  .ai-stat-row { display: flex; justify-content: space-between; margin-bottom: 12px; font-size: 13px; }
  .ai-stat-label { color: #a1a1aa; font-weight: 600; }
  .ai-stat-val { color: #fff; font-weight: 800; text-align: right; }
  .ai-tag { display: inline-block; padding: 4px 10px; background: rgba(139,92,246,0.2); border: 1px solid rgba(139,92,246,0.5); border-radius: 8px; font-size: 11px; font-weight: 800; color: #c4b5fd; margin: 0 6px 6px 0; text-transform: uppercase; }
  .ai-tag.green { background: rgba(34,197,94,0.2); border-color: rgba(34,197,94,0.5); color: #86efac; }
  .ai-tag.red { background: rgba(239,68,68,0.2); border-color: rgba(239,68,68,0.5); color: #fca5a5; }
  
  /* Loader */
  .ai-loader { display: none; margin: 30px auto; width: 50px; height: 50px; border: 4px solid rgba(255,255,255,0.1); border-top-color: #8b5cf6; border-radius: 50%; animation: spin 1s linear infinite; }
  @keyframes spin { to { transform: rotate(360deg); } }
  
  /* Memory Build Progress */
  .build-progress { display: flex; gap: 4px; margin-bottom: 20px; }
  .build-step { flex: 1; height: 6px; background: rgba(255,255,255,0.1); border-radius: 3px; }
  .build-step.active { background: #8b5cf6; box-shadow: 0 0 10px #8b5cf6; }
</style>

<!-- Floating Button -->


<!-- Main Overlay -->
<div id="ai-hub-overlay" class="ai-overlay">
    <div class="ai-header">
        <div class="ai-title" id="ai-hub-title">AI Merkezi</div>
        <div class="ai-close" onclick="closeAIHub()">Ã—</div>
    </div>
    
    <div class="ai-content custom-scrollbar" id="ai-main-menu">
        <p class="text-xs text-zinc-400 mb-6 font-medium">Sana Ã¶zel geliÅŸtirilmiÅŸ yapay zeka analiz araÃ§larÄ±nÄ± keÅŸfet. SorularÄ±nÄ± yanÄ±tlamaktan Ã¶te, bisikletini analiz eder ve sana Ã¶zel tavsiyeler sunar.</p>
        
        <div class="ai-card" onclick="openAIScreen('analysis')">
            <div class="ai-card-title">ğŸ” Bisiklet Analizi</div>
            <div class="ai-card-desc">Bisikletinin veya parÃ§alarÄ±nÄ±n uyumluluÄŸunu, kategorisini ve performansÄ±nÄ± detaylÄ± raporla.</div>
        </div>
        
        <div class="ai-card" onclick="openAIScreen('recommend')">
            <div class="ai-card-title">ğŸ¯ AkÄ±llÄ± Ã–neri</div>
            <div class="ai-card-desc">BÃ¼tÃ§ene, tarzÄ±na ve seviyene en uygun bisiklet modelini ve geometri Ã¶zelliklerini bul.</div>
        </div>
        
        <div class="ai-card" onclick="openAIScreen('build')">
            <div class="ai-card-title">ğŸ› ï¸ Custom Build Yap</div>
            <div class="ai-card-desc">ParÃ§a parÃ§a hayalindeki bisikleti topla. AI uyumluluÄŸu kontrol edip ilerlemeni kaydetsin.</div>
        </div>
        
        <div class="ai-card" onclick="openAIScreen('part')">
            <div class="ai-card-title">âš™ï¸ ParÃ§a Ä°ncelemesi</div>
            <div class="ai-card-desc">Herhangi bir parÃ§anÄ±n sertlik, dayanÄ±klÄ±lÄ±k ve fiyat/performans skorunu Ã¶ÄŸren.</div>
        </div>
    </div>
    
    <!-- 1. Analysis Screen -->
    <div class="ai-content custom-scrollbar ai-screen" id="ai-screen-analysis">
        <button class="text-zinc-400 mb-4 text-xs font-bold uppercase" onclick="backToAIMenu()">â† Geri DÃ¶n</button>
        <input type="text" id="ai-inp-analysis" class="ai-input" placeholder="Ã–rn: Rockrider ST540 + RockShox Judy">
        <button class="ai-btn" onclick="runAI('analysis')">Analiz Et</button>
        <div id="ai-loader-analysis" class="ai-loader"></div>
        <div id="ai-res-analysis"></div>
    </div>

    <!-- 2. Recommend Screen -->
    <div class="ai-content custom-scrollbar ai-screen" id="ai-screen-recommend">
        <button class="text-zinc-400 mb-4 text-xs font-bold uppercase" onclick="backToAIMenu()">â† Geri DÃ¶n</button>
        <input type="text" id="ai-inp-rec-budget" class="ai-input" placeholder="BÃ¼tÃ§e (Ã–rn: 60.000 TL)">
        <input type="text" id="ai-inp-rec-style" class="ai-input" placeholder="SÃ¼rÃ¼ÅŸ TarzÄ± (Ã–rn: Downhill, Jump)">
        <input type="text" id="ai-inp-rec-terrain" class="ai-input" placeholder="Zemin (Ã–rn: KayalÄ±k, Ã‡amur)">
        <input type="text" id="ai-inp-rec-level" class="ai-input" placeholder="Seviye (Ã–rn: Orta)">
        <button class="ai-btn" onclick="runAI('recommend')">Bisiklet Ã–ner</button>
        <div id="ai-loader-recommend" class="ai-loader"></div>
        <div id="ai-res-recommend"></div>
    </div>

    <!-- 3. Build Screen -->
    <div class="ai-content custom-scrollbar ai-screen" id="ai-screen-build">
        <button class="text-zinc-400 mb-4 text-xs font-bold uppercase" onclick="backToAIMenu()">â† Geri DÃ¶n</button>
        <div class="build-progress" id="ai-build-progress">
            <div class="build-step active"></div><div class="build-step"></div><div class="build-step"></div><div class="build-step"></div><div class="build-step"></div>
        </div>
        <p class="text-xs text-purple-300 font-bold mb-4" id="ai-build-summary-text">Toplama sÃ¼recine baÅŸlayalÄ±m. Ä°lk parÃ§an ne olacak?</p>
        <input type="text" id="ai-inp-build" class="ai-input" placeholder="Ã–rn: Kadro olarak Trek Session 8 seÃ§iyorum">
        <button class="ai-btn" onclick="runAI('build')">Ekle & Ä°ncele</button>
        <button class="w-full bg-zinc-800 text-zinc-400 py-3 rounded-xl font-bold text-xs uppercase mb-4" onclick="aiBuildMemory=[]; document.getElementById('ai-res-build').innerHTML=''; document.getElementById('ai-build-summary-text').innerText='HafÄ±za temizlendi. BaÅŸtan baÅŸla.'; updateBuildProgress(0);">SÄ±fÄ±rla</button>
        <div id="ai-loader-build" class="ai-loader"></div>
        <div id="ai-res-build"></div>
    </div>

    <!-- 4. Part Screen -->
    <div class="ai-content custom-scrollbar ai-screen" id="ai-screen-part">
        <button class="text-zinc-400 mb-4 text-xs font-bold uppercase" onclick="backToAIMenu()">â† Geri DÃ¶n</button>
        <input type="text" id="ai-inp-part" class="ai-input" placeholder="ParÃ§a AdÄ± (Ã–rn: Fox 40 Factory)">
        <button class="ai-btn" onclick="runAI('part')">Skorla & Ä°ncele</button>
        <div id="ai-loader-part" class="ai-loader"></div>
        <div id="ai-res-part"></div>
    </div>

</div>

<script>
// AI HUB LOGIC
let aiBuildMemory = [];

window.openAIHub = function() {
    alert('AI Hub baslatiliyor...');
    try {
        const overlay = document.getElementById('ai-hub-overlay');
        if(!overlay) { alert('HATA: Overlay yok'); return; }
        
        document.body.appendChild(overlay);
        
        overlay.style.cssText = 'position: fixed !important; top: 0 !important; left: 0 !important; right: 0 !important; bottom: 0 !important; width: 100vw !important; height: 100vh !important; display: flex !important; opacity: 1 !important; visibility: visible !important; z-index: 2147483647 !important; pointer-events: auto !important; background: rgba(5,5,10,0.98) !important; flex-direction: column !important;';
        
        overlay.classList.add('show');
        
        if(typeof backToAIMenu === 'function') backToAIMenu();
    } catch(e) {
        alert('HATA: ' + e.message);
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
    const titles = { 'analysis': 'Bisiklet Analizi', 'recommend': 'AkÄ±llÄ± Ã–neri', 'build': 'Custom Build', 'part': 'ParÃ§a Ä°nceleme' };
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
                <div class="ai-stat-row"><span class="ai-stat-label">SÃ¼rÃ¼ÅŸ TarzÄ±</span> <span class="ai-stat-val">${d.riding_style || '-'}</span></div>
                <div class="ai-stat-row"><span class="ai-stat-label">Geometri</span> <span class="ai-stat-val">${d.geometry || '-'}</span></div>
                <div class="ai-stat-row"><span class="ai-stat-label">SÃ¼spansiyon</span> <span class="ai-stat-val">${d.suspension || '-'}</span></div>
                <div class="ai-stat-row"><span class="ai-stat-label">Lastikler</span> <span class="ai-stat-val">${d.tires || '-'}</span></div>
                
                <div class="mt-4 mb-2 font-bold text-sm text-green-400 uppercase tracking-widest border-b border-zinc-800 pb-1">GÃ¼Ã§lÃ¼ YÃ¶nler</div>
                <div>${(d.strengths||[]).map(s => `<span class="ai-tag green">${s}</span>`).join('')}</div>
                
                <div class="mt-4 mb-2 font-bold text-sm text-red-400 uppercase tracking-widest border-b border-zinc-800 pb-1">ZayÄ±f YÃ¶nler</div>
                <div>${(d.weaknesses||[]).map(s => `<span class="ai-tag red">${s}</span>`).join('')}</div>
                
                <div class="mt-4 mb-2 font-bold text-sm text-yellow-400 uppercase tracking-widest border-b border-zinc-800 pb-1">YÃ¼kseltme Ã–nerileri</div>
                <ul class="text-zinc-300 text-sm list-disc pl-4 space-y-1">${(d.upgrades||[]).map(s => `<li>${s}</li>`).join('')}</ul>
            </div>`;
        }
        else if (type === 'recommend') {
            html += `<div class="ai-result-box">
                <div class="text-center mb-6">
                    <div class="text-3xl mb-2">ğŸš²</div>
                    <div class="font-black text-xl text-purple-400 uppercase tracking-wider">${d.bike_type || '-'}</div>
                    <div class="text-xs text-zinc-400 mt-1">${d.level_advice || ''}</div>
                </div>
                
                <div class="ai-stat-row"><span class="ai-stat-label">Geometri</span> <span class="ai-stat-val text-blue-300">${d.geometry || '-'}</span></div>
                <div class="ai-stat-row"><span class="ai-stat-label">Travel Ã–nerisi</span> <span class="ai-stat-val text-yellow-400">${d.suspension_travel || '-'}</span></div>
                <div class="ai-stat-row"><span class="ai-stat-label">Teker Ã–nerisi</span> <span class="ai-stat-val">${d.wheel_size || '-'}</span></div>
                
                <div class="mt-6 mb-2 font-bold text-sm text-white uppercase tracking-widest border-b border-zinc-800 pb-1">Ã–rnek Modeller</div>
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
                warnHtml = `<div class="bg-red-900/30 border border-red-500/50 text-red-200 p-4 rounded-xl mb-4 text-sm shadow-[0_0_15px_rgba(239,68,68,0.3)]">âš ï¸ <b>Uyumsuzluk UyarÄ±:</b> ${d.compatibility_warning}</div>`;
            }
            
            document.getElementById('ai-build-summary-text').innerText = d.build_summary || 'Toplama devam ediyor...';
            updateBuildProgress(aiBuildMemory.length);
            
            html += `${warnHtml}<div class="ai-result-box">
                <div class="mt-2 mb-4 font-bold text-sm text-purple-400 uppercase tracking-widest border-b border-purple-900/50 pb-2">AI SÄ±radaki Ã–nerileri</div>
                <ul class="text-zinc-200 text-sm list-disc pl-4 space-y-2 mb-4">
                    ${(d.suggestions||[]).map(s => `<li>${s}</li>`).join('')}
                </ul>
                <div class="bg-black/40 p-3 rounded-lg border border-zinc-800">
                    <div class="text-[10px] text-zinc-500 font-bold uppercase mb-2">Åu anki Build GeÃ§miÅŸin:</div>
                    <div class="text-xs text-zinc-300 leading-relaxed">${aiBuildMemory.join(' <b class="text-purple-500">â†’</b> ')}</div>
                </div>
            </div>`;
        }
        else if (type === 'part') {
            html += `<div class="ai-result-box">
                <div class="ai-score-ring" style="border-color:#38bdf8; box-shadow:0 0 20px rgba(56,189,248,0.5)">${d.performance_score || 0}</div>
                <div class="text-center text-xs text-zinc-400 mb-6 font-bold tracking-widest uppercase">ParÃ§a Skoru</div>
                
                <div class="ai-stat-row"><span class="ai-stat-label">Kategori</span> <span class="ai-stat-val text-blue-400">${d.category || '-'}</span></div>
                <div class="ai-stat-row"><span class="ai-stat-label">Seviye</span> <span class="ai-stat-val">${d.level || '-'}</span></div>
                <div class="ai-stat-row"><span class="ai-stat-label">Sertlik</span> <span class="ai-stat-val">${d.stiffness || '-'}</span></div>
                <div class="ai-stat-row"><span class="ai-stat-label">DayanÄ±klÄ±lÄ±k</span> <span class="ai-stat-val">${d.durability || '-'}</span></div>
                <div class="ai-stat-row"><span class="ai-stat-label">Fiyat/Performans</span> <span class="ai-stat-val text-green-400">${d.price_performance || '-'}</span></div>
                
                <div class="mt-4 mb-2 font-bold text-sm text-green-400 uppercase tracking-widest border-b border-zinc-800 pb-1">GÃ¼Ã§lÃ¼ YÃ¶nler</div>
                <div>${(d.strengths||[]).map(s => `<span class="ai-tag green">${s}</span>`).join('')}</div>
                
                <div class="mt-4 mb-2 font-bold text-sm text-red-400 uppercase tracking-widest border-b border-zinc-800 pb-1">ZayÄ±f YÃ¶nler</div>
                <div>${(d.weaknesses||[]).map(s => `<span class="ai-tag red">${s}</span>`).join('')}</div>
                
                <div class="mt-4 p-3 bg-blue-900/20 border border-blue-500/30 rounded-lg text-sm text-blue-200 leading-relaxed">
                    <b>ğŸ’¡ Tavsiye:</b> ${d.usage_advice || '-'}
                </div>
            </div>`;
        }
        
        resBox.innerHTML = html;
        
    } catch(e) {
        loader.style.display = 'none';
        resBox.innerHTML = `<div class="ai-result-box" style="border-color: #ef4444;"><div class="text-red-400 font-bold">BaÄŸlantÄ± hatasÄ± oluÅŸtu.</div></div>`;
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
            if(typeof showToast==='function') showToast('Tur kÃ¼tÃ¼phanesi yÃ¼klenemedi!');
            return;
        }
        
        if(typeof showToast==='function') showToast('Uygulama Turu BaÅŸlÄ±yor...', 'success');
        
        try {
            const intro = introJs();
            intro.setOptions({
                nextLabel: 'Ä°leri â”',
                prevLabel: 'â¬… Geri',
                doneLabel: 'Bitir âœ”',
                showProgress: true,
                exitOnOverlayClick: false,
                steps: [
                    {
                        title: 'HoÅŸ Geldin! ğŸš´',
                        intro: 'FreeriderTR'ye katÄ±ldÄ±ÄŸÄ±n iÃ§in harika hissediyoruz. UygulamayÄ± en iyi ÅŸekilde kullanman iÃ§in detaylÄ± bir tura Ã§Ä±kalÄ±m.'
                    },
                    {
                        element: document.querySelector('#bnav-0'),
                        title: 'ğŸ—ºï¸ Harita',
                        intro: 'Buradan TÃ¼rkiye'deki tÃ¼m trail ve rampa noktalarÄ±nÄ± gÃ¶rebilirsin.'
                    },
                    {
                        element: document.querySelector('#bnav-1'),
                        title: 'ğŸ’¬ Chat',
                        intro: 'DiÄŸer sÃ¼rÃ¼cÃ¼lerle anlÄ±k sohbet et ve etkinlik planla.'
                    },
                    {
                        element: document.querySelector('#bnav-9'),
                        title: 'ğŸ¬ Reels',
                        intro: 'SÃ¼rÃ¼ÅŸ videolarÄ±nÄ± izle veya kendi anlarÄ±nÄ± paylaÅŸ.'
                    },
                    {
                        element: document.querySelector('#bnav-ai'),
                        title: 'ğŸ¤– AI Asistan',
                        intro: 'Yapay zeka asistanÄ± ile bisikletini topla ve teknik analiz yap.'
                    },
                    {
                        element: document.querySelector('#bnav-7'),
                        title: 'ğŸ‘¤ Profil & Garaj',
                        intro: 'Kendi dijital garajÄ±nÄ± oluÅŸtur ve rozetlerini takip et.'
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
            if(typeof showToast==='function') showToast('Tur hatasÄ±: ' + e.message);
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
</script>

<!-- iOS PWA Install Prompt -->
<div id="ios-pwa-prompt" class="hidden fixed bottom-5 left-1/2 -translate-x-1/2 w-[95%] max-w-sm z-[99999] slide-up-anim">
    <div class="glass-panel border border-zinc-700/80 rounded-2xl p-4 shadow-[0_10px_40px_rgba(0,0,0,0.9)] relative bg-black/80 backdrop-blur-xl">
        <button onclick="closeIosPrompt()" class="absolute top-2 right-2 text-zinc-400 hover:text-white bg-black/50 w-8 h-8 rounded-full flex items-center justify-center border border-zinc-700 transition hover:scale-110">âœ•</button>
        <div class="flex items-start gap-4">
            <img src="https://cdn.freeridertr.com.tr/profil%20resmi/unnamed.jpg" class="w-14 h-14 rounded-xl shadow-[0_0_15px_rgba(220,38,38,0.4)] border border-red-900/50">
            <div class="pr-6">
                <h4 class="text-white font-bold text-base leading-tight">UygulamayÄ± YÃ¼kle</h4>
                <p class="text-zinc-300 text-[11px] mt-1.5 leading-relaxed">
                    Tam ekran deneyim iÃ§in alttaki PaylaÅŸ <span class="inline-flex bg-zinc-800 text-blue-400 p-0.5 rounded mx-0.5 align-middle border border-zinc-700"><i data-lucide="share" class="w-3 h-3"></i></span> ikonuna dokunun ve <br><b class="text-white font-bold">"Ana Ekrana Ekle"</b> seÃ§eneÄŸini seÃ§in.
                </p>
            </div>
        </div>
    </div>
</div>

</body>

</html>
'''