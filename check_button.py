import re

with open(r"C:\Users\sevdi\.gemini\antigravity\brain\e31aa6dd-9697-4caf-9d58-6ef1364bee3b\.system_generated\steps\313\content.md", "r", encoding="utf-8") as f:
    content = f.read()

# Find the bnav-ai button by looking for openAIHub
match = re.search(r'<button[^>]*openAIHub[^>]*>', content)
if match:
    print(match.group(0))
else:
    print("Button with openAIHub not found")
