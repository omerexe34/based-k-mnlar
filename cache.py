"""
cache.py
========
Thread-safe, TTL destekli in-memory cache.
512 MB RAM sınırı olan Render ortamında hafif ve verimli çalışacak şekilde tasarlandı.

Kullanım:
    from cache import app_cache
    app_cache.set("key", value, ttl=60)
    val = app_cache.get("key")        # None döner süresi dolmuşsa
    app_cache.invalidate("key")       # Tek anahtar sil
    app_cache.invalidate_prefix("lb") # "lb" ile başlayan tüm anahtarları sil
"""

import time
import threading

class TTLCache:
    """Thread-safe, TTL tabanlı basit in-memory cache.

    - Her key: (value, expire_timestamp)
    - Periyodik temizleme thread'i ile süresi dolan veriler bellekten atılır.
    - max_size ile toplam kayıt sayısı sınırlandırılır (RAM taşması önleme).
    """

    __slots__ = ('_store', '_lock', '_max_size', '_default_ttl')

    def __init__(self, max_size: int = 500, default_ttl: int = 300,
                 cleanup_interval: int = 120):
        self._store: dict[str, tuple] = {}
        self._lock = threading.Lock()
        self._max_size = max_size
        self._default_ttl = default_ttl

        # Arka plan temizleme thread'i
        t = threading.Thread(target=self._cleanup_loop,
                             args=(cleanup_interval,), daemon=True)
        t.start()

    # ── Okuma ─────────────────────────────────────────────────────────
    def get(self, key: str, default=None):
        """Cache'den değer oku. Süresi dolmuşsa veya yoksa default döner."""
        with self._lock:
            entry = self._store.get(key)
            if entry is None:
                return default
            value, expires = entry
            if time.time() > expires:
                del self._store[key]
                return default
            return value

    # ── Yazma ─────────────────────────────────────────────────────────
    def set(self, key: str, value, ttl: int | None = None):
        """Cache'e değer yaz. ttl saniye sonra süresi dolar."""
        _ttl = ttl if ttl is not None else self._default_ttl
        expires = time.time() + _ttl
        with self._lock:
            # Kapasite kontrolü — en eski kayıtları at
            if len(self._store) >= self._max_size and key not in self._store:
                self._evict_oldest(max(1, self._max_size // 10))
            self._store[key] = (value, expires)

    # ── Geçersiz kılma ────────────────────────────────────────────────
    def invalidate(self, key: str):
        """Tek bir anahtarı cache'den sil."""
        with self._lock:
            self._store.pop(key, None)

    def invalidate_prefix(self, prefix: str):
        """Belirtilen prefix ile başlayan tüm anahtarları sil."""
        with self._lock:
            keys_to_del = [k for k in self._store if k.startswith(prefix)]
            for k in keys_to_del:
                del self._store[k]

    def clear(self):
        """Tüm cache'i temizle."""
        with self._lock:
            self._store.clear()

    # ── Dahili ────────────────────────────────────────────────────────
    def _evict_oldest(self, count: int):
        """En eski (süresi en yakın) kayıtları at. Lock içinde çağrılmalı."""
        if not self._store:
            return
        sorted_keys = sorted(self._store, key=lambda k: self._store[k][1])
        for k in sorted_keys[:count]:
            del self._store[k]

    def _cleanup_loop(self, interval: int):
        """Periyodik olarak süresi dolan kayıtları bellekten temizler."""
        while True:
            time.sleep(interval)
            now = time.time()
            with self._lock:
                expired = [k for k, (_, exp) in self._store.items() if now > exp]
                for k in expired:
                    del self._store[k]


# ══════════════════════════════════════════════════════════════════════
# GLOBAL CACHE NESNESİ
# Tüm modüller `from cache import app_cache` ile paylaşır.
# ══════════════════════════════════════════════════════════════════════
# 4 GB RAM'li sunucu için optimize edilmiş: daha büyük cache, daha az Supabase sorgusu
app_cache = TTLCache(max_size=2000, default_ttl=600, cleanup_interval=120)
