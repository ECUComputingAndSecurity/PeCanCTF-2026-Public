#!/usr/bin/env python3
from pwn import *

p = remote("127.0.0.1", 6767)
print(p.recvuntil(b"> ").decode())
p.sendline(b"readl")
print(p.recvuntil(b"> ").decode())
p.sendline("vulran_secret_service")
b = p.recvuntil(b"read > ")
with open("scraped_binary", "wb") as f:
    f.write(b)
p.sendline(b"done")
p.recvuntil(b"> ")
p.sendline("exit")
p.recvall()
