"""
storage.py
==========
Cloudflare R2 üzerine base64 ve multipart dosya yükleme işlemleri.
"""

import base64
import uuid
from collections import deque

from extensions import r2_client, R2_BUCKET_NAME, R2_PUBLIC_URL

# Video MIME → uzantı eşlemesi
_VIDEO_EXT_MAP = {
    "mp4": "mp4", "mpeg": "mp4", "quicktime": "mov", "mov": "mov",
    "webm": "webm", "ogg": "ogv", "x-msvideo": "avi", "x-matroska": "mkv",
    "3gpp": "3gp", "3gpp2": "3g2", "x-ms-wmv": "wmv"
}

def upload_base64_to_storage(base64_string, folder="uploads"):
    if not isinstance(base64_string, str):
        return base64_string
    if not (base64_string.startswith("data:image/") or
            base64_string.startswith("data:audio/") or
            base64_string.startswith("data:video/")):
        return base64_string
    if not r2_client:
        print("⚠️ R2 depolama yapılandırılmamış, dosya yüklenemiyor.")
        return base64_string
    try:
        header, encoded = base64_string.split(",", 1)
        mime_type = header.split(";")[0].split(":")[1]          # e.g. video/mp4
        raw_sub   = mime_type.split("/")[1].split(";")[0]       # e.g. mp4

        if mime_type.startswith("video/"):
            ext = _VIDEO_EXT_MAP.get(raw_sub, "mp4")
        elif mime_type.startswith("audio/"):
            ext = raw_sub if raw_sub in ("mp3","ogg","wav","webm","aac","m4a") else "mp3"
        else:
            ext = raw_sub
        if ext == "jpeg": ext = "jpg"

        file_data = base64.b64decode(encoded)
        file_name = f"{folder}/{uuid.uuid4().hex}.{ext}"

        r2_client.put_object(
            Bucket=R2_BUCKET_NAME,
            Key=file_name,
            Body=file_data,
            ContentType=mime_type,
            CacheControl="public, max-age=31536000"
        )

        public_url = f"{R2_PUBLIC_URL}/{file_name}"
        print(f"✅ R2 yüklendi: {file_name} ({len(file_data)//1024} KB)")
        return public_url

    except Exception as e:
        print(f"❌ R2 Yükleme Hatası: {e}")
        return base64_string  # fallback: base64 string'i döndür, en azından gösterilsin

def upload_binary_to_storage(file_stream, mime_type, folder="uploads", ext="mp4"):
    """
    Base64 dönüşümü yapmadan doğrudan binary dosya akışını (stream) R2'ye yükler.
    Çok düşük RAM kullanır ve devasa dosyaların hızlı yüklenmesini sağlar.
    """
    if not r2_client:
        print("⚠️ R2 depolama yapılandırılmamış, dosya yüklenemiyor.")
        return None
    try:
        if mime_type.startswith("video/"):
            ext = _VIDEO_EXT_MAP.get(ext, "mp4")
        if ext == "jpeg": ext = "jpg"

        file_name = f"{folder}/{uuid.uuid4().hex}.{ext}"

        r2_client.put_object(
            Bucket=R2_BUCKET_NAME,
            Key=file_name,
            Body=file_stream,
            ContentType=mime_type,
            CacheControl="public, max-age=31536000"
        )

        public_url = f"{R2_PUBLIC_URL}/{file_name}"
        print(f"✅ R2 Binary yüklendi: {file_name}")
        return public_url

    except Exception as e:
        print(f"❌ R2 Binary Yükleme Hatası: {e}")
        return None

    return base64_string

def process_base64_in_dict(root):
    """Sözlük veya listede base64 veri URL'lerini R2'ye yükler.
    Özyinelemeli (recursive) değil, yığın (stack) tabanlı iteratif yaklaşım kullanır.
    Bu sayede derin iç içe yapılarda Python özyineleme limiti aşılmaz."""
    _B64_PREFIXES = ("data:image/", "data:audio/", "data:video/")
    stack: deque = deque()
    stack.append(root)
    while stack:
        node = stack.pop()
        if isinstance(node, dict):
            for k in list(node.keys()):
                v = node[k]
                if isinstance(v, str) and v.startswith(_B64_PREFIXES):
                    node[k] = upload_base64_to_storage(v)
                elif isinstance(v, (dict, list)):
                    stack.append(v)
        elif isinstance(node, list):
            for i, v in enumerate(node):
                if isinstance(v, str) and v.startswith(_B64_PREFIXES):
                    node[i] = upload_base64_to_storage(v)
                elif isinstance(v, (dict, list)):
                    stack.append(v)
