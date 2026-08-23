FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DATABASE_PATH=/data/devhub.db \
    BOT_URL=http://127.0.0.1:5001 \
    CHALLENGE_BASE_URL=http://127.0.0.1 \
    FLAG=PECAN{W38_C4CH3_D3C3P710N_W2T7P3C4SA5X6ZHQFM4SK7}

RUN apt-get update \
    && apt-get install -y --no-install-recommends nginx supervisor \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /srv

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app
COPY admin-bot ./admin-bot
COPY nginx/nginx.conf /etc/nginx/nginx.conf
COPY deploy/supervisord.conf /etc/supervisor/conf.d/devhub.conf
COPY deploy/entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh \
    && mkdir -p /data /run/nginx /var/cache/nginx/devhub

EXPOSE 80

HEALTHCHECK --interval=5s --timeout=3s --retries=12 \
    CMD python -c "import requests; requests.get('http://127.0.0.1/healthz', timeout=2).raise_for_status()"

ENTRYPOINT ["/entrypoint.sh"]
