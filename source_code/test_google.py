import os
from dotenv import load_dotenv
load_dotenv()
import json
import google.oauth2.service_account as gsa
from googleapiclient.discovery import build as gapi_build
import google.auth.transport.requests as grequests

c = os.environ.get('GOOGLE_CREDENTIALS_JSON', '')
c = c.strip().strip("'\"")

def clean_credentials(c_str):
    c_str = c_str.strip().strip("'\"")
    if not c_str.startswith("{"):
        try:
            import base64
            decoded = base64.b64decode(c_str).decode("utf-8")
            if decoded.strip().startswith("{"):
                c_str = decoded.strip()
        except Exception as e:
            print("Base64 decode failed:", e)

    info = json.loads(c_str)
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
    return info

# Test 1: Original
print("Testing Original...")
info1 = clean_credentials(c)
creds1 = gsa.Credentials.from_service_account_info(info1, scopes=['https://www.googleapis.com/auth/androidpublisher'])
creds1.refresh(grequests.Request())
print("Test 1 Passed!")

# Test 2: Space-replaced private_key
print("Testing Space-replaced private_key...")
import copy
info2 = copy.deepcopy(info1)
info2["private_key"] = info2["private_key"].replace("\n", " ").strip()
# Reconstruct string
c_space = json.dumps(info2)
info2_clean = clean_credentials(c_space)
creds2 = gsa.Credentials.from_service_account_info(info2_clean, scopes=['https://www.googleapis.com/auth/androidpublisher'])
creds2.refresh(grequests.Request())
print("Test 2 Passed!")

# Test 3: Base64 encoded JSON
print("Testing Base64 encoded JSON...")
import base64
c_b64 = base64.b64encode(c.encode("utf-8")).decode("utf-8")
info3_clean = clean_credentials(c_b64)
creds3 = gsa.Credentials.from_service_account_info(info3_clean, scopes=['https://www.googleapis.com/auth/androidpublisher'])
creds3.refresh(grequests.Request())
print("Test 3 Passed!")

