import sys

with open('html_template.py', 'r', encoding='utf-8') as f:
    content = f.read()

target = '<button onclick="openAIHub()" id="bnav-ai" class="flex flex-col items-center gap-0.5 px-3 py-2 rounded-2xl transition-all duration-300 text-purple-400" style="min-width:48px">'
replacement = '<button onclick="if(window.openAIHub) { window.openAIHub(); } else { alert(\'Hata: AI Hub kodu yuklenmedi!\'); }" ontouchend="if(window.openAIHub) window.openAIHub();" id="bnav-ai" class="flex flex-col items-center gap-0.5 px-3 py-2 rounded-2xl transition-all duration-300 text-purple-400" style="min-width:48px; pointer-events: auto !important; position: relative; z-index: 9999999 !important;">'

if target in content:
    content = content.replace(target, replacement)
    with open('html_template.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Success")
else:
    print("Target not found")
