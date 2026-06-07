import os, requests
from dotenv import load_dotenv
load_dotenv()

app_id = os.environ.get("ONESIGNAL_APP_ID", "").strip()
api_key = (os.environ.get("ONESIGNAL_REST_API_KEY") or os.environ.get("ONESIGNAL_API_KEY", "")).strip()
auth_header = f"Basic {api_key}" if not api_key.startswith("os_v2_") else f"Key {api_key}"

def test_payload(name, payload, url="https://onesignal.com/api/v1/notifications"):
    payload["app_id"] = app_id
    payload["contents"] = {"en": "test"}
    print(f"\n--- Testing {name} to {url} ---")
    try:
        r = requests.post(url, json=payload, headers={"Authorization": auth_header, "Content-Type": "application/json"})
        print(f"Status: {r.status_code}")
        print(f"Response: {r.text[:300]}")
    except Exception as e:
        print(f"Error: {e}")

test_payload("include_aliases", {"include_aliases": {"external_id": ["admin"]}, "target_channel": "push"})
test_payload("include_external_user_ids", {"include_external_user_ids": ["admin"]})
test_payload("include_subscription_ids", {"include_subscription_ids": ["dummy-id"]})
test_payload("include_player_ids", {"include_player_ids": ["dummy-id"]})
test_payload("api.onesignal.com aliases", {"include_aliases": {"external_id": ["admin"]}, "target_channel": "push"}, url="https://api.onesignal.com/notifications")
