import multiprocessing
import os

bind = os.getenv("GUNICORN_BIND", "0.0.0.0:8000")
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
