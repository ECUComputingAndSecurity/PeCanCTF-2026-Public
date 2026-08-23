FROM ghcr.io/foundry-rs/foundry:latest

# Install Python
USER root
RUN apt-get update && \
    apt-get install -y \
        python3 \
        python3-pip && \
    rm -rf /var/lib/apt/lists/*


# Setup App
WORKDIR /app

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .


# Run Server
EXPOSE 5000

RUN chmod +x entrypoint.sh

ENV FOUNDRY_DISABLE_NIGHTLY_WARNING=1

CMD ["./entrypoint.sh"]
