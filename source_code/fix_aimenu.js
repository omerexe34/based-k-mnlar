const fs = require('fs');
let html = fs.readFileSync('html_template.py', 'utf8');

html = html.replace(
    "document.getElementById('ai-chat-screen').style.display = 'none';",
    "if(document.getElementById('ai-chat-screen')) document.getElementById('ai-chat-screen').style.display = 'none';"
);

html = html.replace(
    "document.getElementById('ai-analysis-screen').style.display = 'none';",
    "if(document.getElementById('ai-analysis-screen')) document.getElementById('ai-analysis-screen').style.display = 'none';"
);

fs.writeFileSync('html_template.py', html);
console.log('Fixed backToAIMenu');
