import os
from random import randint
from hashlib import sha256
from custom_rand import SemiPRand

FLAG = os.environ.get("FLAG", "pecan{f4k3_fl4g}")

def gen_flags(flag):
    flag_bytes = flag.encode()
    seed = len(flag_bytes) ** 3
    rand = SemiPRand(seed)
    
    flags = []
    for i in range(seed):
        result = sha256(flag_bytes + bytes(i)).digest()
        result = bytearray(result)
        result[(rand.next(seed) - rand.next(seed)) % len(result)] = flag_bytes[(rand.next(seed) + rand.next(seed)) % len(flag_bytes)]
        flags.append(result.hex())
    return flags

with open("flags.txt", "w") as file:
    rand = SemiPRand(randint(2**28, 2**32 - 1))
    file.write(', '.join([repr(rand.next()) for _ in range(10)]))
    file.write("\n")
    file.write(', '.join([("pecan{" + f + "}") for f in gen_flags(FLAG)]))
