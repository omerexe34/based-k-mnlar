import re

with open('html_template.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Make sure we don't duplicate ontouchend if it's already there
def replace_onclick(match):
    full_match = match.group(0)
    onclick_content = match.group(1)
    if "ontouchend" in full_match:
        return full_match
    return f'onclick="{onclick_content}" ontouchend="{onclick_content}" style="pointer-events: auto;"'

# Targeting the specific AI HUB buttons
content = re.sub(r'onclick="(closeAIHub\(\))"', replace_onclick, content)
content = re.sub(r'onclick="(openAIScreen\([^\)]+\))"', replace_onclick, content)
content = re.sub(r'onclick="(backToAIMenu\(\))"', replace_onclick, content)
content = re.sub(r'onclick="(runAI\([^\)]+\))"', replace_onclick, content)

# Reset button has a long onclick
long_onclick = "aiBuildMemory=[]; document.getElementById('ai-res-build').innerHTML=''; document.getElementById('ai-build-summary-text').innerText='Hafıza temizlendi. Baştan başla.'; updateBuildProgress(0);"
if long_onclick in content:
    content = content.replace(f'onclick="{long_onclick}"', f'onclick="{long_onclick}" ontouchend="{long_onclick}" style="pointer-events: auto;"')

with open('html_template.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Buttons fixed successfully.")
