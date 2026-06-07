const fs = require('fs');
let html = fs.readFileSync('html_template.py', 'utf8');

const targetStr = `                        if (wasAdmin) {
                            currentUser.role = 'Admin';
                        }`;

const replacementStr = `                        if (wasAdmin) {
                            currentUser.role = 'Admin';
                            if (!currentUser.stats) currentUser.stats = {};
                            currentUser.stats.premium_tier = 3;
                            currentUser.stats.premium_color = 'rainbow';
                            currentUser.stats.avatar_effect = 'fire';
                        }`;

html = html.replace(targetStr, replacementStr);

// Let's also patch the main initialization of currentUser to ensure it ALWAYS has stats if it's admin.
const initTarget = `        let userCache = localStorage.getItem('userCache');
        if (userCache) {
            currentUser = JSON.parse(userCache);
        }`;
        
const initReplacement = `        let userCache = localStorage.getItem('userCache');
        if (userCache) {
            currentUser = JSON.parse(userCache);
            if (currentUser && (currentUser.role === 'Admin' || currentUser.username === 'Admin' || (currentUser.username && currentUser.username.toLowerCase() === 'admin'))) {
                currentUser.role = 'Admin';
                if (!currentUser.stats) currentUser.stats = {};
                currentUser.stats.premium_tier = 3;
                currentUser.stats.premium_color = 'rainbow';
                currentUser.stats.avatar_effect = 'fire';
            }
        }`;
html = html.replace(initTarget, initReplacement);

// Let's also patch the login success handler
const loginTarget = `                    currentUser = res.user;
                    window.currentUser = currentUser;`;
const loginReplacement = `                    currentUser = res.user;
                    if (currentUser && (currentUser.role === 'Admin' || currentUser.username === 'Admin' || (currentUser.username && currentUser.username.toLowerCase() === 'admin'))) {
                        currentUser.role = 'Admin';
                        if (!currentUser.stats) currentUser.stats = {};
                        currentUser.stats.premium_tier = 3;
                        currentUser.stats.premium_color = 'rainbow';
                        currentUser.stats.avatar_effect = 'fire';
                    }
                    window.currentUser = currentUser;`;
html = html.replace(loginTarget, loginReplacement);

fs.writeFileSync('html_template.py', html);
console.log('Fixed admin premium');
