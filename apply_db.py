import re

with open("parts_db_temp.txt", "r", encoding="utf-8") as f:
    new_db = f.read()

with open("html_template.py", "r", encoding="utf-8") as f:
    html = f.read()

# Replace everything from `const PARTS_DB = {` to the matching `};`
pattern = re.compile(r"    const PARTS_DB = \{.*?\n    \};\n", re.DOTALL)
html_replaced = pattern.sub(new_db + "\n", html)

with open("html_template.py", "w", encoding="utf-8") as f:
    f.write(html_replaced)

print("Replaced PARTS_DB successfully!")
