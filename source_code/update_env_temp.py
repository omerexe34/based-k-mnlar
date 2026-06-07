import json
import os
import base64

new_json = {
  'type': 'service_account',
  'project_id': 'freeridertr',
  'private_key_id': '05c585ca308d30a15585f0b01ecdbf3149ed1289',
  'private_key': '-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDClIAUWxWFtjQ2\n+62iVsJmkWvIudK5qF8knWrQL1Mn7nobbElq7qwH7Ur5YHhEEPjAlbEo+WgqlXcs\n49zIgdR94uDLoA9eGO2YxJybJyEQ1ILAK5SJf2PGP+WY6gPpVlI46CdN8GHrekxX\nn79FBYXSoQ79pfUnoX2XEDIkaokNE9mcWdryBe4BoLcITpHDr7DQyvBMYBb0A+EO\ngBcOnIbJzjWvefMnKVOnlVcOfieCB8KkwSbBLlDtCOWyFELhmhShB1W25maEUgVl\n8i2XlVLnErjTNQa2agnL6vphDTZsSILKHtTochibGh6GFenHB6yRJZGHWqJaVI1B\nlX0AIAM/AgMBAAECggEACSByCYJkNgtf05xmfpDXOXxks9uTeMXfAJappe4yVlMn\nQxYHM47SXuTQeXX+7iJlqJLc5nEcY7LzDhX6CyWb0/PKW4K8dctxiZLfTZ++O03c\nfCsPIovpIClrGYsQd+dmn+izv0IhNaxc3FdP32rs5f5L97XLE/rNK0LFN1QP7Z8F\noy799T7WHI8Q+DrC0zUuW3pp8gElkdfDat2V19pq3WuxiZHjs+k1HFXb4vflsRqp\ne+lI82Qlv97zQYzTLQkGGc1uyrz7r7hdkbcssYr4rpzmoRBvE78wXxrIh3VuIG4y\nKMgV7Jc5BWKXoVerx6YH/vhWeBhoqL5Nr2WeG7+DkQKBgQD8flNCP5Xhdb7pPczV\nhV2HvVh/Y9sdZ0xYsTjb8NoV3m8ROrYvM1wRX/4HgjMxXpmlbJYQNhnWfXQKDwKM\ngGTiIeVANrkFisxYQI1ECz2YRoUCNsReaHsn/yIILoQj2IFobouFJOFfAced89Al\nshgMHjoDU6PIUpCeq4O5KpFKBQKBgQDFSEd1iJC/evYpyjIzAIb+4b+bAz6OXs1p\n1PM5/0H3AySZxkJpBzaa7TxZ+OgjMTmZbJHzApPM4XLz6a7iB5U07Rm04fc2Rvep\nTvjILUQOcMk83CSx8yMBQUePkySBhELOfghX3nPGtNYqTLWZf+HU/3etephPBlpM\nYilKd1EncwKBgQDJEF+EtdXIwFbSrZ/buGQOn71FVGM8OvIU/qtkmZtRJtwTQEmr\ntJ5wR5ympgvWGJsJnDqzliFlKGmrSOCiueucF5nTVMBppWmsLVtRABKAnEd2x93/\nv/uykfyrvz8CvHnwi3cXA5NkcKphIbJzEisMG1XfKE+YSgdYEwTGAxvHcQKBgQC2\nn1kfEQNFbdMQDk937QYKTfmryk4PRu0KCgn55zQuL+eivefeB8Jhmjii5QonAbtb\nLijQ9tLQ9uYNqoWsUO6rJs0EJ6VLxlgej682xshYQcnXn8YMQJFn6QEQhFpn1oJt\nWjfo91DfYalbUNVOuhXYsYAcw/7YMH5IdRnaCCfExwKBgHqgf9KwkvfdZFCyxQKx\nt5RfSMHTO7H7TDqVPUOYS1sYN6qHJdEP9LBq2aPE4YRdGGmwxRU8zWUs6OQB5p1E\nr/boNu8LeSEeMwEIOTuGkTf++2OtGBlmvF2g/+EH/40pMmvQHcL2cqkDWhyZIo62\nBf99o41/ti4ybg7q3jVPzNeS\n-----END PRIVATE KEY-----\n',
  'client_email': 'freeridertr@freeridertr.iam.gserviceaccount.com',
  'client_id': '108012689794887625282',
  'auth_uri': 'https://accounts.google.com/o/oauth2/auth',
  'token_uri': 'https://oauth2.googleapis.com/token',
  'auth_provider_x509_cert_url': 'https://www.googleapis.com/oauth2/v1/certs',
  'client_x509_cert_url': 'https://www.googleapis.com/robot/v1/metadata/x509/freeridertr%40freeridertr.iam.gserviceaccount.com',
  'universe_domain': 'googleapis.com'
}

json_str = json.dumps(new_json)
b64_str = base64.b64encode(json_str.encode('utf-8')).decode('utf-8')
env_path = '.env'

if os.path.exists(env_path):
    with open(env_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    with open(env_path, 'w', encoding='utf-8') as f:
        found = False
        for line in lines:
            if line.startswith('GOOGLE_CREDENTIALS_JSON='):
                f.write(f'GOOGLE_CREDENTIALS_JSON={b64_str}\n')
                found = True
            else:
                f.write(line)
        if not found:
            f.write(f'\nGOOGLE_CREDENTIALS_JSON={b64_str}\n')
    print('Updated .env with base64 credentials')
else:
    print('.env not found')
