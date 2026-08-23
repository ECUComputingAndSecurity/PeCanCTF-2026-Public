#!/usr/bin/env python3

from pwn import *

context.binary = "./chall"

def main():
    t = process(context.binary.path)

    low = 0
    high = 4294967295
    x = None

    while True:
        guess = (low + high) // 2
        t.sendlineafter(b"What's your guess? ", str(u64(p32(guess) + p32(0xffffffff))).encode())
        x = t.recvline()

        match x:
            case b"Too low!\n":
                low = guess
            case b"Too high!\n":
                high = guess
            case _:
                break

    print(x.split(b": ")[-1][:-1].decode())

    t.close()

if __name__ == "__main__":
    main()
