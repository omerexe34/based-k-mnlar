import re

with open('html_template.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Find the IIFE block at the bottom
start_marker = "// AI HUB LOGIC - BULLETPROOF REWRITE"
end_marker = "console.log(\"AI HUB IIFE loaded successfully.\");\n})();"

start_idx = content.find(start_marker)
end_idx = content.find(end_marker)

if start_idx == -1 or end_idx == -1:
    print("Could not find the bulletproof block!")
    exit(1)

# Extract the block and remove it from the bottom
# The script block at the bottom is preceded by `<script>\n`
full_block_start = content.rfind("<script>", 0, start_idx)
if full_block_start == -1:
    full_block_start = start_idx

# Let's just remove the IIFE content from wherever it is.
iife_content = content[start_idx:end_idx + len(end_marker)]

# Remove it from content
content = content[:start_idx] + content[end_idx + len(end_marker):]

# Now, we need to inject it into the <head>
# Find the first `<script>` in the head.
head_script_marker = "<script src=\"https://cdn.onesignal.com/sdks/web/v16/OneSignalSDK.page.js\" defer></script>"
head_idx = content.find(head_script_marker)

if head_idx == -1:
    print("Could not find head marker!")
    exit(1)

insert_idx = head_idx + len(head_script_marker) + 1

# Inject a new <script> tag with the IIFE
injection = f"""<script>
{iife_content}
</script>
"""

new_content = content[:insert_idx] + injection + content[insert_idx:]

with open('html_template.py', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("AI HUB IIFE moved to head successfully.")
