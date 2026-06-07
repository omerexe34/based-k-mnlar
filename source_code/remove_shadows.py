import re
import shutil

file_path = r'c:\Users\sevdi\OneDrive\Desktop\freeridertrv7.2.2\html_template.py'
shutil.copy(file_path, file_path + '.shadow_backup')

with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

before_len = len(content)

# 1. Remove box-shadow inline styles ending with ; or " or '
content = re.sub(r'box-shadow\s*:\s*[^;"\']+(?=[;"\'`])', '', content)

# 2. Remove text-shadow inline styles  
content = re.sub(r'text-shadow\s*:\s*[^;"\']+(?=[;"\'`])', '', content)

# 3. Remove Tailwind shadow utility classes
content = re.sub(r'\bshadow-\[[^\]]+\]\s*', '', content)
content = re.sub(r'\b(?:shadow-sm|shadow-md|shadow-lg|shadow-xl|shadow-2xl|shadow-inner|shadow-none)\s*', '', content)

# 4. Remove drop-shadow Tailwind
content = re.sub(r'\bdrop-shadow-\[[^\]]+\]\s*', '', content)
content = re.sub(r'\b(?:drop-shadow-sm|drop-shadow-md|drop-shadow-lg|drop-shadow-xl|drop-shadow-2xl)\s*', '', content)

after_len = len(content)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

remaining_box = content.count('box-shadow')
remaining_text = content.count('text-shadow')
print(f'Kaldirildi: {before_len - after_len} karakter')
print(f'Kalan box-shadow: {remaining_box}')
print(f'Kalan text-shadow: {remaining_text}')
