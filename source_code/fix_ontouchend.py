import re

with open('html_template.py', 'r', encoding='utf-8') as f:
    text = f.read()

text = re.sub(r'\s*ontouchend="[^"]*"', '', text)

with open('html_template.py', 'w', encoding='utf-8') as f:
    f.write(text)

print("Removed ontouchend attributes.")
