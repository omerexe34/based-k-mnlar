import re

with open('inject_iife.py', 'r', encoding='utf-8') as f:
    c_inject = f.read()

s_str = c_inject.find('new_iife = """// AI HUB LOGIC - BULLETPROOF REWRITE\n(function() {')
e_str = c_inject.find('console.log("AI HUB IIFE loaded successfully.");\n})();"""', s_str) + 55

full_js = c_inject[s_str + 14:e_str]

with open('html_template.py', 'r', encoding='utf-8') as f:
    c_html = f.read()

s_html = c_html.find('// AI HUB LOGIC - BULLETPROOF REWRITE')
e_html = c_html.find('</script>', s_html)

c_html = c_html[:s_html] + full_js + '\n' + c_html[e_html:]

with open('html_template.py', 'w', encoding='utf-8') as f:
    f.write(c_html)

print('Successfully restored full AI Hub JS logic.')
