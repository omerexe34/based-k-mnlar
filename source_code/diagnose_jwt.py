"""
diagnose_jwt.py
===============
VPS'te Google JWT sorununu teşhis eder.
Çalıştır: python diagnose_jwt.py
"""

import os
import json
import datetime
import time

from dotenv import load_dotenv
load_dotenv()

print("=" * 60)
print("GOOGLE JWT SORUN TEŞHİSİ")
print("=" * 60)

# ── 1. Sistem saati kontrolü ──────────────────────────────────
print("\n[1] SİSTEM SAATİ:")
now = datetime.datetime.utcnow()
print(f"    UTC  : {now.strftime('%Y-%m-%d %H:%M:%S')}")
print(f"    LOCAL: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# Google'ın saatiyle farkı kontrol et
try:
    import urllib.request
    import urllib.error
    import email.utils
    google_date = None
    try:
        req = urllib.request.urlopen("https://www.googleapis.com/", timeout=5)
        google_date = req.headers.get("Date", "")
    except urllib.error.HTTPError as he:
        google_date = he.headers.get("Date", "")
    except Exception:
        try:
            req = urllib.request.urlopen("https://www.google.com", timeout=5)
            google_date = req.headers.get("Date", "")
        except Exception:
            pass

    print(f"    GOOGLE SERVER: {google_date}")
    if google_date:
        google_ts = email.utils.parsedate_to_datetime(google_date).timestamp()
        local_ts  = time.time()
        diff_sec  = abs(local_ts - google_ts)
        print(f"    FARK: {diff_sec:.1f} saniye", end=" ")
        if diff_sec > 60:
            print("[!] SORUN! Saat farki >60 saniye -> JWT hatasi bu yuzden!")
        else:
            print("[+] Saat farki normal")
    else:
        print("    Google sunucu saati alınamadı.")
except Exception as e:
    print(f"    Saat kontrolü başarısız: {e}")

# ── 2. Env var kontrolü ────────────────────────────────────────
print("\n[2] GOOGLE_CREDENTIALS_JSON:")
creds_json = os.environ.get("GOOGLE_CREDENTIALS_JSON", "")
if not creds_json:
    print("    [X] BULUNAMADI! Env var set edilmemiş.")
else:
    creds_json = creds_json.strip().strip("'\"")
    print(f"    Uzunluk: {len(creds_json)} karakter")
    
    # base64 decode check
    if not creds_json.startswith("{"):
        try:
            import base64
            decoded = base64.b64decode(creds_json).decode("utf-8")
            if decoded.strip().startswith("{"):
                creds_json = decoded.strip()
                print("    [!] Base64 algilandi ve cozuldu.")
        except Exception as e:
            print("    Base64 decode denemesi basarisiz:", e)

    try:
        info = json.loads(creds_json)
        print(f"    [+] JSON gecerli")
        print(f"    private_key_id : {info.get('private_key_id')}")
        print(f"    client_email   : {info.get('client_email')}")
        
        # Clean private_key format
        if "private_key" in info:
            pk = info["private_key"]
            pk = pk.replace("\\n", "\n")
            header = "-----BEGIN PRIVATE KEY-----"
            footer = "-----END PRIVATE KEY-----"
            if header in pk and footer in pk:
                parts = pk.split(header)[1].split(footer)
                body = parts[0].strip()
                if "\n" not in body and " " in body:
                    body = body.replace(" ", "\n")
                    print("    [!] private_key icindeki bosluklar yeni satira cevrildi.")
                pk = f"{header}\n{body}\n{footer}\n"
            info["private_key"] = pk
            
        pk = info.get("private_key", "")
        if "BEGIN PRIVATE KEY" in pk:
            print(f"    private_key    : [+] Mevcut ({len(pk)} karakter)")
        else:
            print(f"    private_key    : [X] BOZUK veya eksik!")
    except json.JSONDecodeError as e:
        print(f"    [X] JSON PARSE HATASI: {e}")
        print(f"    İlk 100 karakter: {repr(creds_json[:100])}")

# ── 3. Google API token testi ──────────────────────────────────
print("\n[3] GOOGLE API TOKEN TESTİ:")
try:
    import google.oauth2.service_account as gsa
    import google.auth.transport.requests as grequests

    creds_json = os.environ.get("GOOGLE_CREDENTIALS_JSON", "").strip("'\"")
    if not creds_json.startswith("{"):
        try:
            import base64
            decoded = base64.b64decode(creds_json).decode("utf-8")
            if decoded.strip().startswith("{"):
                creds_json = decoded.strip()
        except Exception:
            pass

    info = json.loads(creds_json)
    if "private_key" in info:
        pk = info["private_key"]
        pk = pk.replace("\\n", "\n")
        header = "-----BEGIN PRIVATE KEY-----"
        footer = "-----END PRIVATE KEY-----"
        if header in pk and footer in pk:
            parts = pk.split(header)[1].split(footer)
            body = parts[0].strip()
            if "\n" not in body and " " in body:
                body = body.replace(" ", "\n")
            pk = f"{header}\n{body}\n{footer}\n"
        info["private_key"] = pk

    creds = gsa.Credentials.from_service_account_info(
        info,
        scopes=["https://www.googleapis.com/auth/androidpublisher"]
    )
    creds.refresh(grequests.Request())
    print("    [+] TOKEN BASARILI — Google Play API kullanilabilir!")
except Exception as e:
    print(f"    [X] TOKEN BASARISIZ: {e}")
    err_str = str(e).lower()
    if "invalid_grant" in err_str:
        print("    → Neden: Saat senkronizasyonu, bozuk key formati veya iptal edilmis anahtar")
    elif "json" in err_str:
        print("    → Neden: GOOGLE_CREDENTIALS_JSON formatı bozuk")
    elif "import" in err_str:
        print("    → Neden: google-auth kütüphanesi yüklü değil")

print("\n" + "=" * 60)
print("Düzeltme komutları:")
print("  Saat sorunu: sudo ntpdate -u pool.ntp.org")
print("  veya       : sudo timedatectl set-ntp true")
print("=" * 60)
