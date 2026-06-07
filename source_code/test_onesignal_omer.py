import os, requests
from dotenv import load_dotenv
load_dotenv()
app_id = os.environ.get("ONESIGNAL_APP_ID", "").strip()
api_key = (os.environ.get("ONESIGNAL_REST_API_KEY") or os.environ.get("ONESIGNAL_API_KEY", "")).strip()
auth_header = f"Basic {api_key}" if not api_key.startswith("os_v2_") else f"Key {api_key}"

payload = {
    "app_id": app_id,
    "include_player_ids": ["fce74318-7c57-49c2-b0ae-ff76fbfedfeb"], 
    "target_channel": "push",
    "contents": {"en": "Test message to Omer1"}
}
try:
    r = requests.post("https://onesignal.com/api/v1/notifications", json=payload, headers={"Authorization": auth_header, "Content-Type": "application/json"})
    print("Status:", r.status_code)
    print("Response:", r.text[:300])
except Exception as e:
    print(e)
