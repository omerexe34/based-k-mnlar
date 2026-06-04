import re

with open('html_template.py', 'r', encoding='utf-8') as f:
    content = f.read()

# The head script block starts around line 83:
#     <script>
#     // DEFINE AI HUB GLOBALLY EARLY
# ...
#     </script>
#     <script>
#       window.OneSignalDeferred = window.OneSignalDeferred || [];

# We want to remove this entire script block.
# Let's find the exact string that starts the script block.
start_marker = '<script>\n    // DEFINE AI HUB GLOBALLY EARLY'
end_marker = '</script>\n    <script>\n      window.OneSignalDeferred'

if start_marker in content and end_marker in content:
    start_idx = content.find(start_marker)
    end_idx = content.find(end_marker)
    if start_idx != -1 and end_idx != -1:
        # Remove the block, but keep the '<script>\n      window.OneSignalDeferred'
        content = content[:start_idx] + content[end_idx + 10:]

# Wait, the original had:
#     <script src="https://cdn.onesignal.com/sdks/web/v16/OneSignalSDK.page.js" defer></script>
#     <script>
#       window.OneSignalDeferred = window.OneSignalDeferred || [];

# So if we remove from start_marker to end_idx, we should just leave:
#     <script src="https://cdn.onesignal.com/sdks/web/v16/OneSignalSDK.page.js" defer></script>
#     <script>
#       window.OneSignalDeferred = window.OneSignalDeferred || [];

# Let's do a regex replacement to be safe.
# We want to remove everything between `<script>\n    // DEFINE AI HUB GLOBALLY EARLY` and `    </script>\n    <script>\n      window.OneSignalDeferred`, inclusive.
pattern = re.compile(r'<script>\s*// DEFINE AI HUB GLOBALLY EARLY.*?</script>\s*(?=<script>\s*window\.OneSignalDeferred)', re.DOTALL)
content = pattern.sub('', content)

# Check if there is another "// DEFINE AI HUB GLOBALLY EARLY TO PREVENT UNDEFINED ERRORS"
pattern2 = re.compile(r'<script>\s*// DEFINE AI HUB GLOBALLY EARLY TO PREVENT UNDEFINED ERRORS.*?</script>\s*(?=<script>\s*window\.OneSignalDeferred)', re.DOTALL)
content = pattern2.sub('', content)


# Now ensure the BOTTOM AI HUB LOGIC is intact.
if "let aiBuildMemory = [];" in content:
    print("aiBuildMemory found.")
else:
    print("aiBuildMemory MISSING! Something is wrong.")

# Check the bnav-ai button to make sure it's correct
if "Hata: AI Hub kodu yuklenmedi!" in content:
    print("Button alert exists.")

with open('html_template.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Cleanup successful.")
