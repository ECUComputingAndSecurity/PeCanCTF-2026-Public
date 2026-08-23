import sys
import math

with open("flags.txt", "r") as file:
    flags = []
    lines = file.readlines()

    outputs = [int(x) for x in lines[0].split(', ')]
    
    n = None
    for i in range(len(outputs) - 1):
        diff = outputs[i] ** 2 - outputs[i + 1]
        n = math.gcd(n, diff) if n is not None else diff
    if n is None:
        print("Modulus extraction failed.")
        sys.exit(1)
    n = abs(n)

    for flag in lines[1].split(', '):
        flags.append(bytearray(bytes.fromhex(flag.replace("pecan{", "").replace("}", ""))))

    seed = len(flags)
    flag_len = int(round(seed ** (1/3)))
    curr = seed

    result = bytearray(b'*' * flag_len)
    for i in range(seed):
        # Setting value random is generated first. Order needs to be reversed from generation.
        curr = (curr**2) % n
        result_rand_a = curr % seed
        curr = (curr**2) % n
        result_rand_b = curr % seed
        curr = (curr**2) % n
        flags_rand_a = curr % seed
        curr = (curr**2) % n
        flags_rand_b = curr % seed
        result[(result_rand_a + result_rand_b) % flag_len] = flags[i][(flags_rand_a - flags_rand_b) % len(flags[i])]

    print(result.decode())
