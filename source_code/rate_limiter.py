"""
rate_limiter.py
===============
In-memory rate limiter — batch persist optimizasyonu.
Her rate_check çağrısında diske yazmak yerine periyodik olarak yazar.
Sunucu kapatılırken atexit ile son durumu kaydeder.
"""

import os
import json
import time
import atexit
import threading

from extensions import logger

# ==============================================================================
# IN-MEMORY RATE LIMITER (BATCH PERSIST)
# ==============================================================================
_RATE_STORE_PATH = os.path.join(os.environ.get("RATE_STORE_DIR", "/tmp"), "freerider_rate_store.json")
_rate_store: dict = {}
_rate_lock  = threading.Lock()
_dirty      = False   # Değişiklik oldu mu? — persist gerekiyor mu?

def _load_rate_store_from_disk():
    """Uygulama başlangıcında JSON dosyasını okur, süresi geçmiş kayıtları atar."""
    global _rate_store
    try:
        with open(_RATE_STORE_PATH, "r") as f:
            raw = json.load(f)
        now = time.time()
        _rate_store = {k: tuple(v) for k, v in raw.items() if now - v[1] <= 600}
        logger.info(f"Rate store yüklendi: {len(_rate_store)} aktif kayıt.")
    except FileNotFoundError:
        _rate_store = {}
    except Exception as exc:
        logger.warning(f"Rate store okunamadı, sıfırlanıyor: {exc}")
        _rate_store = {}

def _persist_rate_store():
    """Rate store'u diske yazar (kilit içinde çağrılmalı)."""
    global _dirty
    try:
        with open(_RATE_STORE_PATH, "w") as f:
            json.dump(_rate_store, f)
        _dirty = False
    except Exception as exc:
        logger.warning(f"Rate store yazılamadı: {exc}")

_load_rate_store_from_disk()

def _rate_key(ip: str, action: str) -> str:
    return f"{ip}:{action}"

def rate_check(ip: str, action: str, max_calls: int, window_sec: int) -> bool:
    """True → izin ver, False → limit aşıldı."""
    global _dirty
    key = _rate_key(ip, action)
    now = time.time()
    with _rate_lock:
        calls, window_start = _rate_store.get(key, (0, now))
        if now - window_start > window_sec:
            calls, window_start = 0, now
        if calls >= max_calls:
            return False
        _rate_store[key] = (calls + 1, window_start)
        _dirty = True
        # ÖNCEKİ: Her çağrıda _persist_rate_store() → KALDIRILDI
        # Artık 30 sn'de bir batch persist yapılıyor
    return True

# Periyodik temizlik + batch persist (bellek sızıntısı ve şişen dosya önleme)
def _cleanup_and_persist():
    global _dirty
    while True:
        time.sleep(30)  # 30 saniyede bir çalış (önceki: temizlik 300 sn, persist her çağrıda)
        now = time.time()
        with _rate_lock:
            expired = [k for k, (_, t) in _rate_store.items() if now - t > 600]
            for k in expired:
                del _rate_store[k]
            if expired:
                _dirty = True
            if _dirty:
                _persist_rate_store()

threading.Thread(target=_cleanup_and_persist, daemon=True).start()

# Uygulama kapatılırken son durumu kaydet
def _atexit_persist():
    with _rate_lock:
        _persist_rate_store()

atexit.register(_atexit_persist)
