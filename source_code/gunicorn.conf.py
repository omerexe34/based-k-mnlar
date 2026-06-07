# gunicorn.conf.py
# ============================================================
# 4 GB RAM, 2 vCPU VDS için optimize Gunicorn yapılandırması
# Formül: (2 × vCPU) + 1 = 5 worker
# ============================================================

import multiprocessing

# ── Temel ───────────────────────────────────────────────────
bind = "127.0.0.1:5000"
workers = 5               # (2 × 2 CPU) + 1
worker_class = "gthread"  # thread tabanlı: gevent+preload_app requests'i kiriyor
threads = 4               # her worker 4 thread → 5×4 = 20 eş zamanlı istek
worker_connections = 1000

# ── Zaman aşımı ─────────────────────────────────────────────
timeout = 120             # uzun AI/dosya yükleme işlemleri için
graceful_timeout = 30
keepalive = 5             # HTTP keep-alive bağlantısı (saniye)

# ── Bellek ──────────────────────────────────────────────────
max_requests = 1000       # 1000 istekten sonra worker yenilenir (bellek sızıntısı önleme)
max_requests_jitter = 200 # yenileme zamanlamasını dağıt (hepsi aynı anda yenilenmesin)

# ── Loglama ─────────────────────────────────────────────────
accesslog = "-"           # stdout
errorlog  = "-"           # stderr
loglevel  = "warning"     # info yerine warning → daha az disk I/O
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s %(D)sµs'

# ── Performans ipuçları ─────────────────────────────────────
preload_app = True        # tüm worker'lar HTML cache'i paylaşır (copy-on-write)
reuse_port  = True        # SO_REUSEPORT: birden fazla worker aynı porta bağlanabilir
