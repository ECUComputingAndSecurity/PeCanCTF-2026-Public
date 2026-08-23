FROM python:3.12-slim
RUN apt-get update \
  && apt-get install -y --no-install-recommends redis-server \
  && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV FLAG=pecan{o0ps!_a11_k3ys}
RUN chmod +x entrypoint.sh
EXPOSE 5000
CMD ["./entrypoint.sh"]
