"""
telegram_notify.py
==================
Admin'e Telegram üzerinden anlık bildirim gönderir.
Tüm önemli olaylar (şikayet, satın alma, ban, çekiliş vb.) bu modül üzerinden iletilir.

Kullanım:
    from telegram_notify import tg

    tg.send("💳 Satın alma talebi geldi!")
    tg.purchase(username, product_label)
    tg.report_message(reporter, suspect, content, severity)
    tg.report_user(reporter, target, reason)
    tg.ban(admin, target, reason)
    tg.unban(admin, target)
    tg.giveaway_created(admin, title)
    tg.giveaway_winner(title, winner, winner_ig)
    tg.new_register(username)
"""

import threading
import requests

_TOKEN   = "8716965792:AAFYeB3AQ1MnciFvrrKLRcpZJS0-QPEIX-U"
_CHAT_ID = 6450414237
_API_URL = f"https://api.telegram.org/bot{_TOKEN}/sendMessage"


def _send_async(text: str):
    """Telegram mesajını arka plan thread'inde gönderir — Flask request'ini bloklamaz."""
    def _do():
        try:
            requests.post(
                _API_URL,
                json={
                    "chat_id":    _CHAT_ID,
                    "text":       text,
                    "parse_mode": "HTML",
                },
                timeout=8,
            )
        except Exception as exc:
            print(f"[Telegram] Gönderim hatası: {exc}")
    threading.Thread(target=_do, daemon=True).start()


class _TelegramNotifier:
    """Olay bazlı Telegram bildirim göndericisi."""

    def send(self, text: str):
        """Ham metin gönder (diğer metodlar buraya delege eder)."""
        _send_async(text)

    # ──────────────────────────────────────────────
    # Destek hattı: kullanıcı destek talebi
    # ──────────────────────────────────────────────
    def support(self, username: str, message: str, priority: str = ""):
        snip = message[:300].replace("<", "&lt;").replace(">", "&gt;")
        priority_part = f"\n🎯 Öncelik  : {priority}" if priority else ""
        text = (
            f"🎧 <b>DESTEK TALEBİ</b>"
            f"{priority_part}\n"
            f"👤 Kullanıcı : <code>{username}</code>\n"
            f"💬 Mesaj     : {snip}"
        )
        self.send(text)

    # ──────────────────────────────────────────────
    # Destek hattı: mesaj şikayeti (küfür vb.)
    # ──────────────────────────────────────────────
    def report_message(self, reporter: str, suspect: str,
                        content: str, severity: str = "?", reason: str = ""):
        sev_emoji = {"high": "🔴", "medium": "🟠", "low": "🟡"}.get(severity, "⚪")
        snip = content[:200].replace("<", "&lt;").replace(">", "&gt;")
        text = (
            f"{sev_emoji} <b>MESAJ ŞİKAYETİ</b>\n"
            f"📢 Bildiren : <code>{reporter}</code>\n"
            f"🎯 Şüpheli  : <code>{suspect}</code>\n"
            f"📊 Seviye   : {severity.upper()}\n"
        )
        if reason:
            text += f"💬 Sebep    : {reason}\n"
        text += f"📝 İçerik   : {snip}"
        self.send(text)

    # ──────────────────────────────────────────────
    # Destek hattı: kullanıcı şikayeti
    # ──────────────────────────────────────────────
    def report_user(self, reporter: str, target: str, reason: str = ""):
        text = (
            f"🚨 <b>KULLANICI ŞİKAYETİ</b>\n"
            f"📢 Bildiren : <code>{reporter}</code>\n"
            f"🎯 Hedef    : <code>{target}</code>\n"
            f"💬 Sebep    : {reason or 'Belirtilmedi'}"
        )
        self.send(text)

    # ──────────────────────────────────────────────
    # Web / üyelik satın alma talebi
    # ──────────────────────────────────────────────
    def purchase(self, username: str, product_label: str):
        text = (
            f"💳 <b>SATIN ALMA TALEBİ</b>\n"
            f"👤 Kullanıcı : <code>{username}</code>\n"
            f"📦 Ürün      : {product_label}"
        )
        self.send(text)

    # ──────────────────────────────────────────────
    # Admin: ban işlemi
    # ──────────────────────────────────────────────
    def ban(self, admin: str, target: str, reason: str = ""):
        text = (
            f"🔨 <b>KULLANICI BANLANDI</b>\n"
            f"👮 Admin  : <code>{admin}</code>\n"
            f"🎯 Hedef  : <code>{target}</code>\n"
            f"💬 Sebep  : {reason or 'Belirtilmedi'}"
        )
        self.send(text)

    # ──────────────────────────────────────────────
    # Admin: ban kaldırma
    # ──────────────────────────────────────────────
    def unban(self, admin: str, target: str):
        text = (
            f"✅ <b>BAN KALDIRILDI</b>\n"
            f"👮 Admin  : <code>{admin}</code>\n"
            f"🎯 Hedef  : <code>{target}</code>"
        )
        self.send(text)

    # ──────────────────────────────────────────────
    # Çekiliş: yeni çekiliş oluşturuldu
    # ──────────────────────────────────────────────
    def giveaway_created(self, admin: str, title: str):
        text = (
            f"🎁 <b>YENİ ÇEKİLİŞ BAŞLADI</b>\n"
            f"👮 Admin  : <code>{admin}</code>\n"
            f"📌 Başlık : {title}"
        )
        self.send(text)

    # ──────────────────────────────────────────────
    # Çekiliş: kazanan belirlendi
    # ──────────────────────────────────────────────
    def giveaway_winner(self, title: str, winner: str, winner_ig: str = ""):
        ig_part = f"\n📸 Instagram: @{winner_ig}" if winner_ig else ""
        text = (
            f"🏆 <b>ÇEKİLİŞ SONUÇLANDI</b>\n"
            f"📌 Çekiliş : {title}\n"
            f"🥇 Kazanan : <code>{winner}</code>"
            f"{ig_part}"
        )
        self.send(text)

    # ──────────────────────────────────────────────
    # Yeni kayıt
    # ──────────────────────────────────────────────
    def new_register(self, username: str):
        text = (
            f"🆕 <b>YENİ ÜYE KAYDI</b>\n"
            f"👤 Kullanıcı : <code>{username}</code>"
        )
        self.send(text)

    # ──────────────────────────────────────────────
    # Admin premium onayı / reddi
    # ──────────────────────────────────────────────
    def premium_approved(self, admin: str, target: str, tier: int, days: int):
        tier_label = {1: "⭐ Standart", 2: "🌟 Deluxe", 3: "👑 Ultra+"}.get(tier, f"Tier {tier}")
        text = (
            f"✅ <b>PREMİUM ONAYLANDI</b>\n"
            f"👮 Admin     : <code>{admin}</code>\n"
            f"👤 Kullanıcı : <code>{target}</code>\n"
            f"📦 Paket     : {tier_label}\n"
            f"📅 Süre      : {days} gün"
        )
        self.send(text)

    def premium_rejected(self, admin: str, target: str):
        text = (
            f"❌ <b>PREMİUM REDDEDİLDİ</b>\n"
            f"👮 Admin     : <code>{admin}</code>\n"
            f"👤 Kullanıcı : <code>{target}</code>"
        )
        self.send(text)


# Tek örnek — her yerden `from telegram_notify import tg` ile kullanılır
tg = _TelegramNotifier()
