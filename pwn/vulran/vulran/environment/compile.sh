#!/bin/sh

gcc environment/vulran_secret_service.c -o environment/vulran_secret_service \
    -g \
    -Wl,-z,relro -Wl,-z,now \
    -O0 \
    -fno-pie -no-pie \
    -fstack-protector-strong \
    -Wl,-z,noexecstack
