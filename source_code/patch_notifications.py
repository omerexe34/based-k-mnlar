import sys

with open('html_template.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Remove annoying sound
content = content.replace('try { document.getElementById("notif-sound").play().catch(e => {}); } catch(e) {}', '// sound muted')

# Make showToast less annoying (duration 1500, top position, smaller padding)
content = content.replace("function showToast(message, typeOrDuration = 'info', duration = 3000)", "function showToast(message, typeOrDuration = 'info', duration = 1500)")
content = content.replace("'position:fixed', 'bottom:80px', 'left:50%',", "'position:fixed', 'top:20px', 'left:50%',")
content = content.replace("'padding:14px 24px', 'border-radius:16px',", "'padding:8px 16px', 'border-radius:24px',")

# Make showRankToast less annoying (smaller, shorter duration, pointer-events none)
old_rank_class = "toast.className = 'fixed top-20 left-1/2 -translate-x-1/2 z-[99999] px-5 py-3 rounded-2xl font-bold text-sm  flex items-center gap-3 scale-in-anim';"
new_rank_class = "toast.className = 'fixed top-10 left-1/2 -translate-x-1/2 z-[99999] px-4 py-2 rounded-full font-bold text-xs flex items-center gap-2 scale-in-anim pointer-events-none opacity-90';"
content = content.replace(old_rank_class, new_rank_class)
content = content.replace("setTimeout(() => { toast.style.opacity='0'; toast.style.transition='opacity 0.4s'; setTimeout(()=>toast.remove(),400); }, 3000);", "setTimeout(() => { toast.style.opacity='0'; toast.style.transition='opacity 0.4s'; setTimeout(()=>toast.remove(),400); }, 1500);")

# Make showMissionToast less annoying
old_mission_class = "toast.className = 'fixed top-20 left-1/2 -translate-x-1/2 z-[99999] bg-gradient-to-r from-yellow-600 to-orange-500 text-white px-6 py-3 rounded-2xl font-bold text-sm  flex items-center gap-3 scale-in-anim';"
new_mission_class = "toast.className = 'fixed top-10 left-1/2 -translate-x-1/2 z-[99999] bg-gradient-to-r from-yellow-600 to-orange-500 text-white px-4 py-2 rounded-full font-bold text-xs flex items-center gap-2 scale-in-anim pointer-events-none opacity-90';"
content = content.replace(old_mission_class, new_mission_class)
content = content.replace("setTimeout(() => { toast.style.opacity='0'; toast.style.transition='opacity 0.5s'; setTimeout(()=>toast.remove(),500); }, 3500);", "setTimeout(() => { toast.style.opacity='0'; toast.style.transition='opacity 0.5s'; setTimeout(()=>toast.remove(),500); }, 1500);")

with open('html_template.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('Patched successfully')
