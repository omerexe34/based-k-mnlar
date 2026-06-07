import re, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('html_template.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

line = lines[8514]
print("HAS ONERROR:", 'onerror' in line)

if 'onerror' in line:
    # Remove " onerror="..." " part - everything from onerror= to the closing >
    fixed = re.sub(r' onerror="[^"]*"', '', line)
    print("FIXED:", repr(fixed[:300]))
    lines[8514] = fixed
    with open('html_template.py', 'w', encoding='utf-8') as f:
        f.writelines(lines)
    print("SAVED OK")
else:
    print("LINE CONTENT:", repr(line[:300]))
