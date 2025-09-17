# syntax=docker/dockerfile:1
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 
    PYTHONUNBUFFERED=1 
    PIP_DISABLE_PIP_VERSION_CHECK=on 
    PIP_NO_CACHE_DIR=on

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends 
    bash 
    curl 
    netcat-openbsd 
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . /app

# Ensure entrypoint is executable
RUN chmod +x /app/entrypoint.sh

RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

ENTRYPOINT ["/app/entrypoint.sh"]
