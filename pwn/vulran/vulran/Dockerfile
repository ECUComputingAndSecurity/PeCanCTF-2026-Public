FROM ubuntu:22.04

RUN apt-get update && apt-get install -y \
    gcc \
    socat \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m -s /bin/bash ctf

WORKDIR /home/ctf

COPY ./environment /home/ctf/environment

RUN /home/ctf/environment/compile.sh && rm /home/ctf/environment/compile.sh

RUN chown -R root:root /home/ctf && \
    chmod 755 /home/ctf && \
    chmod 755 /home/ctf/environment && \
    chmod 755 /home/ctf/environment/vulran_secret_service && \
    chmod 444 /home/ctf/environment/*.txt && \
    chmod 444 /home/ctf/environment/vulran_secret_service.c

USER ctf
EXPOSE 6767

CMD ["socat", "-d", "-d", "TCP-LISTEN:6767,reuseaddr,fork", "SYSTEM:'cd /home/ctf/environment && ./vulran_secret_service',stderr"]
