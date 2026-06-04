import os
import time
import uuid
import random
import string
import subprocess
import threading
import telebot
from extensions import supabase, logger

TOKEN = "8964367576:AAEioOeJkrBAO5N7p768yBlfBe00WmgP6qs"
CHAT_ID = 6450414237

bot = telebot.TeleBot(TOKEN)

def is_admin(message):
    return message.chat.id == CHAT_ID

@bot.message_handler(commands=['start'])
def send_welcome(message):
    if not is_admin(message):
        return
    bot.reply_to(message, "🚴 Freerider VPS Bot Aktif\n\n"
                          "🔧 Sistem Komutları:\n"
                          "/durum - Sunucu Durumu\n"
                          "/sonkod - Son Commit\n"
                          "/restart - Sistemi Yeniden Başlat\n"
                          "/guncelle - Kodları Çek ve Başlat\n"
                          "/log - Son Logları Gör\n\n"
                          "👥 Yönetim Komutları:\n"
                          "/ban <kullanici_adi> <sebep> - Kullanıcıyı yasakla\n"
                          "/unban <kullanici_adi> - Kullanıcı yasağını kaldır\n"
                          "/reply <kullanici_adi> <mesaj> - Kullanıcıya DM at\n"
                          "/uyar <kullanici_adi> - Kullanıcıya kırmızı uyarı DM'si at\n"
                          "/broadcast <mesaj> - Tüm sohbete Sistem mesajı at\n"
                          "/istatistik - Günlük/Genel metrikleri gör\n\n"
                          "🌟 Premium Kod Komutları:\n"
                          "/kod <tier> <gun> - Aktivasyon kodu oluştur\n"
                          "  örnek: /kod 1 30 → 30 günlük Standart\n"
                          "  tier: 1=Standart | 2=Deluxe | 3=Ultra+\n"
                          "/kodlar - Kullanılmamış tüm kodları listele")

@bot.message_handler(commands=['durum'])
def get_durum(message):
    if not is_admin(message): return
    try:
        uptime = subprocess.getoutput("uptime")
        ram = subprocess.getoutput("free -h")
        disk = subprocess.getoutput("df -h /")
        msg = f"🖥 VPS Durumu\n\n{uptime}\n\n{ram}\n\n{disk}"
        bot.reply_to(message, msg)
    except Exception as e:
        bot.reply_to(message, f"Hata: {e}")

@bot.message_handler(commands=['sonkod'])
def get_sonkod(message):
    if not is_admin(message): return
    try:
        commit = subprocess.getoutput("cd /root/testson1122 && git log -1 --pretty=format:'%h - %s'")
        bot.reply_to(message, f"📦 Son Commit\n\n{commit}")
    except Exception as e:
        bot.reply_to(message, f"Hata: {e}")

@bot.message_handler(commands=['restart'])
def do_restart(message):
    if not is_admin(message): return
    bot.reply_to(message, "🔄 Freerider yeniden başlatılıyor...")
    subprocess.Popen("systemctl restart freerider", shell=True)

@bot.message_handler(commands=['guncelle'])
def do_guncelle(message):
    if not is_admin(message): return
    bot.reply_to(message, "🔄 GitHub kontrol ediliyor...")
    sonuc = subprocess.getoutput("cd /root/testson1122 && git fetch origin && git reset --hard origin/main")
    subprocess.Popen("systemctl restart freerider", shell=True)
    bot.reply_to(message, f"✅ Güncellendi\n\n{sonuc[-3500:]}")

@bot.message_handler(commands=['log'])
def get_log(message):
    if not is_admin(message): return
    logs = subprocess.getoutput("journalctl -u freerider -n 30 --no-pager")
    bot.reply_to(message, logs[-4000:])

@bot.message_handler(commands=['ban'])
def ban_user(message):
    if not is_admin(message): return
    parts = message.text.split(' ', 2)
    if len(parts) < 3:
        bot.reply_to(message, "Kullanım: /ban <kullanici_adi> <sebep>")
        return
    username = parts[1]
    reason = parts[2]
    try:
        if supabase:
            res = supabase.table('users').select('username').eq('username', username).execute()
            if not res.data:
                bot.reply_to(message, "Kullanıcı bulunamadı!")
                return
            
            supabase.table('users').update({
                'is_banned': True,
                'ban_reason': reason
            }).eq('username', username).execute()
            
            bot.reply_to(message, f"✅ {username} başarıyla banlandı.\nSebep: {reason}")
            
            # DM ile de bildir
            supabase.table('dms').insert({
                'id': str(int(time.time()*1000))+'_ban',
                'sender': 'Admin',
                'receiver': username,
                'participants': ['Admin', username],
                'text': f"Hesabınız askıya alınmıştır. Sebep: {reason}",
                'type': 'text'
            }).execute()
        else:
            bot.reply_to(message, "Supabase bağlantısı yok.")
    except Exception as e:
        bot.reply_to(message, f"Hata: {e}")

@bot.message_handler(commands=['unban'])
def unban_user(message):
    if not is_admin(message): return
    parts = message.text.split(' ', 1)
    if len(parts) < 2:
        bot.reply_to(message, "Kullanım: /unban <kullanici_adi>")
        return
    username = parts[1]
    try:
        if supabase:
            supabase.table('users').update({
                'is_banned': False,
                'ban_reason': None
            }).eq('username', username).execute()
            bot.reply_to(message, f"✅ {username} yasağı kaldırıldı.")
        else:
            bot.reply_to(message, "Supabase bağlantısı yok.")
    except Exception as e:
        bot.reply_to(message, f"Hata: {e}")

@bot.message_handler(commands=['reply'])
def reply_user(message):
    if not is_admin(message): return
    parts = message.text.split(' ', 2)
    if len(parts) < 3:
        bot.reply_to(message, "Kullanım: /reply <kullanici_adi> <mesaj>")
        return
    username = parts[1]
    msg_text = parts[2]
    try:
        if supabase:
            supabase.table('dms').insert({
                'id': str(int(time.time()*1000))+'_adm_reply',
                'sender': 'Admin',
                'receiver': username,
                'participants': ['Admin', username],
                'text': msg_text,
                'type': 'text'
            }).execute()
            bot.reply_to(message, f"✅ {username} kullanıcısına mesaj gönderildi:\n{msg_text}")
        else:
            bot.reply_to(message, "Supabase bağlantısı yok.")
    except Exception as e:
        bot.reply_to(message, f"Hata: {e}")

@bot.message_handler(commands=['uyar'])
def warn_user(message):
    if not is_admin(message): return
    parts = message.text.split(' ', 1)
    if len(parts) < 2:
        bot.reply_to(message, "Kullanım: /uyar <kullanici_adi>")
        return
    username = parts[1]
    try:
        if supabase:
            supabase.table('dms').insert({
                'id': str(int(time.time()*1000))+'_warn',
                'sender': 'Admin',
                'receiver': username,
                'participants': ['Admin', username],
                'text': "🚨 DİKKAT: Davranışlarınız veya mesajlarınız topluluk kurallarımızı ihlal ediyor olabilir. Lütfen kurallara uyun, aksi takdirde hesabınız askıya alınacaktır.",
                'type': 'text'
            }).execute()
            bot.reply_to(message, f"✅ {username} kullanıcısına resmi uyarı mesajı gönderildi.")
        else:
            bot.reply_to(message, "Supabase bağlantısı yok.")
    except Exception as e:
        bot.reply_to(message, f"Hata: {e}")

@bot.message_handler(commands=['broadcast'])
def broadcast_chat(message):
    if not is_admin(message): return
    parts = message.text.split(' ', 1)
    if len(parts) < 2:
        bot.reply_to(message, "Kullanım: /broadcast <mesaj>")
        return
    msg_text = parts[1]
    try:
        if supabase:
            import uuid
            supabase.table('messages').insert({
                'id': str(uuid.uuid4().hex),
                'user': 'SİSTEM DUYURUSU',
                'text': f"📢 {msg_text}",
                'type': 'text'
            }).execute()
            bot.reply_to(message, f"✅ Global sohbete duyuru gönderildi:\n{msg_text}")
        else:
            bot.reply_to(message, "Supabase bağlantısı yok.")
    except Exception as e:
        bot.reply_to(message, f"Hata: {e}")

@bot.message_handler(commands=['istatistik'])
def show_stats(message):
    if not is_admin(message): return
    try:
        if supabase:
            users_res = supabase.table('users').select('username', count='exact').execute()
            msg_res = supabase.table('messages').select('id', count='exact').execute()
            markers_res = supabase.table('markers').select('id', count='exact').execute()
            
            u_count = users_res.count if hasattr(users_res, 'count') else '?'
            m_count = msg_res.count if hasattr(msg_res, 'count') else '?'
            mk_count = markers_res.count if hasattr(markers_res, 'count') else '?'
            
            bot.reply_to(message, f"📊 <b>SİSTEM İSTATİSTİKLERİ</b>\n\n"
                                  f"👥 Toplam Kullanıcı: {u_count}\n"
                                  f"💬 Toplam Mesaj: {m_count}\n"
                                  f"📍 Toplam Harita Pin: {mk_count}", parse_mode="HTML")
        else:
            bot.reply_to(message, "Supabase bağlantısı yok.")
    except Exception as e:
        bot.reply_to(message, f"Hata: {e}")


def _make_code(tier: int, days: int) -> str:
    """FRK-XXXX1234 formatında benzersiz aktivasyon kodu oluşturur ve DB'ye kaydeder."""
    chars = string.ascii_uppercase + string.digits
    suffix = ''.join(random.choices(chars, k=8))
    code_id = f"FRK-{suffix}"
    supabase.table('activation_codes').insert({
        'id': code_id,
        'tier': tier,
        'days': days,
        'created_at': int(time.time()),
        'is_used': False,
        'used_by': None,
        'used_at': None
    }).execute()
    return code_id


@bot.message_handler(commands=['kod'])
def create_code(message):
    if not is_admin(message): return
    parts = message.text.split()
    if len(parts) != 3:
        bot.reply_to(message,
            "❌ Kullanım: /kod <tier> <gun>\n"
            "Tier: 1=Standart | 2=Deluxe | 3=Ultra+\n"
            "\u00d6rnek: /kod 2 30")
        return
    try:
        tier = int(parts[1])
        days = int(parts[2])
    except ValueError:
        bot.reply_to(message, "❌ Tier ve gün sayı olmalıdır. Örnek: /kod 1 7")
        return
    if tier not in (1, 2, 3):
        bot.reply_to(message, "❌ Tier 1, 2 veya 3 olmalıdır.\n1=Standart | 2=Deluxe | 3=Ultra+")
        return
    if days < 1 or days > 3650:
        bot.reply_to(message, "❌ Gün sayısı 1 ile 3650 arasında olmalıdır.")
        return
    try:
        code = _make_code(tier, days)
        tier_names = {1: '⭐ Standart', 2: '🌟 Deluxe', 3: '👑 Ultra+'}
        bot.reply_to(message,
            f"🎁 <b>Aktivasyon Kodu Oluşturuldu!</b>\n\n"
            f"🔑 Kod: <code>{code}</code>\n"
            f"🏆 Seviye: {tier_names[tier]}\n"
            f"📅 Süre: {days} gün\n\n"
            f"Kullanıcı bu kodu uygulamada <b>Premium &gt; Aktivasyon Kodu</b> bölümünden girebilir.",
            parse_mode='HTML')
    except Exception as e:
        bot.reply_to(message, f"❌ Hata: {e}")


@bot.message_handler(commands=['kodlar'])
def list_codes(message):
    if not is_admin(message): return
    try:
        res = supabase.table('activation_codes').select('*').eq('is_used', False).order('created_at', desc=True).limit(30).execute()
        if not res.data:
            bot.reply_to(message, "📦 Kullanılmamış aktif kod bulunamadı.")
            return
        tier_names = {1: '⭐ Std', 2: '🌟 Dlx', 3: '👑 Ult'}
        lines = ["🔑 <b>Aktif Kodlar</b> (Kullanılmamış)\n"]
        for c in res.data:
            t = tier_names.get(c.get('tier', 1), '?')
            d = c.get('days', '?')
            lines.append(f"<code>{c['id']}</code> — {t} — {d}gün")
        bot.reply_to(message, '\n'.join(lines), parse_mode='HTML')
    except Exception as e:
        bot.reply_to(message, f"❌ Hata: {e}")


@bot.message_handler(commands=['kodiptal'])
def cancel_code(message):
    if not is_admin(message): return
    parts = message.text.split()
    if len(parts) != 2:
        bot.reply_to(message, "Kullanım: /kodiptal <FRK-XXXXXXXX>")
        return
    code_id = parts[1].strip().upper()
    try:
        supabase.table('activation_codes').delete().eq('id', code_id).eq('is_used', False).execute()
        bot.reply_to(message, f"✅ Kod iptal edildi: {code_id}")
    except Exception as e:
        bot.reply_to(message, f"❌ Hata: {e}")

def start_bot_thread():
    def run():
        while True:
            try:
                bot.polling(none_stop=True, interval=1, timeout=20)
            except Exception as e:
                logger.error(f"Telegram bot polling error: {e}")
                time.sleep(5)
    
    thread = threading.Thread(target=run, daemon=True)
    thread.start()
    logger.info("✅ Telegram bot arka planda başlatıldı.")

if __name__ == "__main__":
    start_bot_thread()
    # Script bağımsız çalıştırılırsa kapanmaması için sonsuz döngü
    while True:
        time.sleep(1)
