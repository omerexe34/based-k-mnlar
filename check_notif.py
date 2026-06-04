import os, requests
from extensions import supabase

# 1. Env var kontrol
app_id = os.environ.get("ONESIGNAL_APP_ID", "")
api_key = os.environ.get("ONESIGNAL_REST_API_KEY") or os.environ.get("ONESIGNAL_API_KEY", "")
print(f"APP_ID: {app_id}")
print(f"API_KEY ilk 20: {api_key[:20] if api_key else 'YOK'}")

# 2. Veritabaninda player_id var mi?
print("\n--- Player ID Kontrol ---")
res = supabase.table("users").select("username, stats").limit(10).execute()
found = 0
for u in res.data:
    stats = u.get("stats") or {}
    pid = stats.get("onesignal_player_id", "")
    if pid:
        print(f"  BULUNDU: {u['username']} -> {pid[:30]}...")
        found += 1
    else:
        print(f"  YOK: {u['username']}")
print(f"Toplam player_id olan kullanici: {found}")

# 3. API key testi - Basic
print("\n--- API Key Test (Basic) ---")
try:
    r = requests.post(
        "https://onesignal.com/api/v1/notifications",
        json={
            "app_id": app_id,
            "included_segments": ["Total Subscriptions"],
            "contents": {"en": "test"},
            "headings": {"en": "test"}
        },
        headers={
            "Authorization": f"Basic {api_key}",
            "Content-Type": "application/json"
        },
        timeout=10
    )
    print(f"Status: {r.status_code}")
    print(f"Response: {r.text[:300]}")
except Exception as e:
    print(f"Hata: {e}")
