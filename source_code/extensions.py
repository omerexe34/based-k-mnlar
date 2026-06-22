"""
extensions.py
=============
Tüm üçüncü parti importlar, Flask app nesnesi, Supabase ve R2 istemcileri,
global sabitler ve temel yapılandırma buradadır.
Diğer tüm modüller buradan import yapar — dairesel bağımlılık yoktur.
"""
import os
from dotenv import load_dotenv
load_dotenv(override=True)

import re
import json
import html
import logging
import datetime
import time
import hashlib
import requests
import base64
import uuid
import random
import threading
from collections import deque

from flask import Flask, render_template_string, request, jsonify, session, Response
from werkzeug.security import generate_password_hash, check_password_hash
from flask_compress import Compress
from supabase import create_client, Client
import boto3
from botocore.config import Config

# ==============================================================================
# GOOGLE PLAY IAP — Kütüphane importları
# Gerekli kurulum: pip install google-auth google-api-python-client
# ==============================================================================
try:
    import google.oauth2.service_account as gsa
    from googleapiclient.discovery import build as gapi_build
    GOOGLE_API_AVAILABLE = True
except ImportError:
    GOOGLE_API_AVAILABLE = False
    logging.getLogger("freeridertr").warning(
        "Google API kütüphaneleri eksik. "
        "Kurulum: pip install google-auth google-api-python-client"
    )

# ==============================================================================
# PROFESYONEL LOGLAMA SİSTEMİ
# ==============================================================================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("freeridertr")

# ==============================================================================
# ENVIRONMENT VARIABLE'LAR
# ==============================================================================
ONESIGNAL_APP_ID  = os.environ.get("ONESIGNAL_APP_ID")
ONESIGNAL_API_KEY = os.environ.get("ONESIGNAL_REST_API_KEY") or os.environ.get("ONESIGNAL_API_KEY")
ONESIGNAL_API_URL = "https://onesignal.com/api/v1/notifications"

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")  # geriye dönük uyumluluk
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")
RESEND_API_KEY = os.environ.get("RESEND_API_KEY")

SUPABASE_URL = os.environ.get("SUPABASE_URL")
if SUPABASE_URL:
    SUPABASE_URL = SUPABASE_URL.strip().strip('"').strip("'")

SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
if SUPABASE_KEY:
    SUPABASE_KEY = SUPABASE_KEY.strip().strip('"').strip("'")

SUPABASE_ANON_KEY = os.environ.get("SUPABASE_ANON_KEY")
if SUPABASE_ANON_KEY:
    SUPABASE_ANON_KEY = SUPABASE_ANON_KEY.strip().strip('"').strip("'")

R2_ACCESS_KEY_ID     = os.environ.get("R2_ACCESS_KEY_ID")
R2_SECRET_ACCESS_KEY = os.environ.get("R2_SECRET_ACCESS_KEY")
R2_ENDPOINT_URL      = os.environ.get("R2_ENDPOINT_URL")
R2_BUCKET_NAME       = os.environ.get("R2_BUCKET_NAME", "freeridertr")
R2_PUBLIC_URL        = os.environ.get("R2_PUBLIC_URL")

GOOGLE_PLAY_PACKAGE_NAME = os.environ.get("GOOGLE_PLAY_PACKAGE_NAME", "")

ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD")

GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", "")

# ==============================================================================
# ZORUNLU VE OPSİYONEL ENVIRONMENT VARIABLE KONTROLÜ
# ==============================================================================
_REQUIRED_ENVS = [
    "SUPABASE_URL",
    "SUPABASE_KEY",
    "FLASK_SECRET_KEY",
    "ADMIN_PASSWORD",
]

_OPTIONAL_ENVS = [
    "R2_ACCESS_KEY_ID",
    "R2_SECRET_ACCESS_KEY",
    "ONESIGNAL_APP_ID",
    "ONESIGNAL_REST_API_KEY",
    "GROQ_API_KEY",
    "OPENROUTER_API_KEY",
    "RESEND_API_KEY",
    "R2_ENDPOINT_URL",
    "R2_BUCKET_NAME",
    "R2_PUBLIC_URL",
    "GOOGLE_APPLICATION_CREDENTIALS",
    "GOOGLE_PLAY_PACKAGE_NAME",
    "SUPABASE_ANON_KEY",
]

_missing_required = [k for k in _REQUIRED_ENVS if not os.environ.get(k)]
if _missing_required:
    print(f"KRITIK HATA: Asagidaki zorunlu environment variable'lar eksik: {', '.join(_missing_required)}. Gunicorn cokmemesi icin calismaya devam edilecek ama uygulama hatali calisabilir.")
    # raise EnvironmentError() yerine print ile uyardik.

_missing_optional = [k for k in _OPTIONAL_ENVS if not os.environ.get(k)]
if _missing_optional:
    print(f"UYARI: Su opsiyonel environment variable'lar eksik (ilgili ozellikler devre disi): "
          f"{', '.join(_missing_optional)}")

print("OneSignal yapilandirildi")

# ==============================================================================
# FLASK UYGULAMA AYARLARI VE GÜVENLİK
# ==============================================================================
app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY")

# Güvenlik: Canlı ortamda secure cookie her zaman aktif olmalı
app.config['SESSION_COOKIE_SECURE']   = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days=30)
app.config['MAX_CONTENT_LENGTH'] = 150 * 1024 * 1024  # 150 MB

MAX_PAYLOAD_SIZE = 75 * 1024 * 1024

# Response Compression — JSON payload'ları %60-80 küçültür
app.config['COMPRESS_ALGORITHM'] = ['gzip', 'br', 'deflate']
app.config['COMPRESS_LEVEL'] = 6       # 6: hız/boyut dengesi (1=hızlı, 9=küçük)
app.config['COMPRESS_MIN_SIZE'] = 500  # 500 byte altı sıkıştırmaya değmez
app.config['COMPRESS_MIMETYPES'] = [
    'application/json',
    'text/html',
    'text/css',
    'application/javascript',
]
Compress(app)

@app.errorhandler(413)
def too_large(e):
    return jsonify({'status': 'error', 'message': 'Dosya çok büyük! Video için maks. 50MB, fotoğraf için maks. 5MB.'}), 413

# ==============================================================================
# SUPABASE VERİTABANI BAĞLANTISI
# ==============================================================================
try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    print("===================================================")
    print("SUPABASE BAĞLANTISI BAŞARILI!")
    print("SİSTEM: FREERIDER PLUS V7.0 (HAFTALIK YARIŞ & SOSYAL MEDYA EDITION)")
    print("===================================================")
except Exception as e:
    print("[X] SUPABASE BAĞLANTI HATASI YAŞANDI:", e)
    supabase = None

# ==============================================================================
# CLOUDFLARE R2 BAĞLANTISI
# ==============================================================================
if R2_ACCESS_KEY_ID and R2_SECRET_ACCESS_KEY and R2_ENDPOINT_URL:
    r2_client = boto3.client(
        service_name='s3',
        endpoint_url=R2_ENDPOINT_URL,
        aws_access_key_id=R2_ACCESS_KEY_ID,
        aws_secret_access_key=R2_SECRET_ACCESS_KEY,
        region_name="auto",
        config=Config(signature_version='s3v4')
    )
else:
    r2_client = None
    logger.warning("R2 depolama devre dışı: R2_ACCESS_KEY_ID, R2_SECRET_ACCESS_KEY veya R2_ENDPOINT_URL eksik.")


