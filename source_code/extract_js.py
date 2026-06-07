import re
import os

with open("html_template.py", "r", encoding="utf-8") as f:
    html = f.read()

# Extract the script tag that contains window.openAIHub
match = re.search(r'<script>(.*?)</script>', html, re.DOTALL)
if match:
    js_code = match.group(1)
    with open("test_syntax_extract.js", "w", encoding="utf-8") as f:
        f.write(js_code)
    print("Extracted JS to test_syntax_extract.js")
else:
    print("Could not find script tag")
