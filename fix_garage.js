const fs = require('fs');
let html = fs.readFileSync('html_template.py', 'utf8');

const targetStr = `                            // Başkası için sadece temel alanlar
                            db.users[idx] = {
                                ...db.users[idx],
                                xp: updated.xp,
                                stats: { ...(updated.stats || {}), garage: db.users[idx]?.stats?.garage },
                                avatar: updated.avatar,
                                role: updated.role
                            };`;

const replacementStr = `                            // Başkası için sadece temel alanlar
                            db.users[idx] = {
                                ...db.users[idx],
                                xp: updated.xp,
                                stats: { ...(updated.stats || {}) }, // Garaj dahil her seyi guncelle
                                avatar: updated.avatar,
                                role: updated.role
                            };`;

if (html.includes(targetStr)) {
    html = html.replace(targetStr, replacementStr);
    fs.writeFileSync('html_template.py', html);
    console.log('Fixed garage bug');
} else {
    console.log('Target string not found');
}
