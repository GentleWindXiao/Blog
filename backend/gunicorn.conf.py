import multiprocessing
import os

# 宝塔Linux环境配置
bind = os.getenv("GUNICORN_BIND", "127.0.0.1:8000")
workers = int(os.getenv("GUNICORN_WORKERS", max(2, multiprocessing.cpu_count())))
threads = int(os.getenv("GUNICORN_THREADS", 2))
worker_class = os.getenv("GUNICORN_WORKER_CLASS", "gthread")
accesslog = os.getenv("GUNICORN_ACCESSLOG", "-")
errorlog = os.getenv("GUNICORN_ERRORLOG", "-")
loglevel = os.getenv("GUNICORN_LOGLEVEL", "info")
keepalive = int(os.getenv("GUNICORN_KEEPALIVE", 5))
max_requests = int(os.getenv("GUNICORN_MAX_REQUESTS", 0))
max_requests_jitter = int(os.getenv("GUNICORN_MAX_REQUESTS_JITTER", 0))
timeout = int(os.getenv("GUNICORN_TIMEOUT", 120))

# 宝塔Linux特定配置
preload_app = True
worker_connections = 1000
max_requests_jitter = 50
graceful_timeout = 30
forwarded_allow_ips = "*"
secure_scheme_headers = {
    'X-FORWARDED-PROTOCOL': 'ssl',
    'X-FORWARDED-PROTO': 'https',
    'X-FORWARDED-SSL': 'on'
}
