FROM debian:bookworm-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends socat coreutils && \
    rm -rf /var/lib/apt/lists/* && \
    useradd -ms /bin/bash ctf

WORKDIR /home/ctf

COPY tielur_overflow /home/ctf/tielur_overflow
COPY flag.txt /home/ctf/flag.txt

RUN chmod 555 /home/ctf/tielur_overflow && \
    chmod 444 /home/ctf/flag.txt && \
    chown root:root /home/ctf/tielur_overflow /home/ctf/flag.txt

USER ctf

EXPOSE 1111

CMD ["socat", "-T60", "TCP4-LISTEN:1111,reuseaddr,fork", "EXEC:/usr/bin/timeout 60 /home/ctf/tielur_overflow"]