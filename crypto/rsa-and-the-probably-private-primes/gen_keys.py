from secrets import SystemRandom
from Crypto.Util.number import bytes_to_long, inverse, long_to_bytes
from math import sqrt

PRIME_LARGE_MIN = 2**2047
PRIME_LARGE_MAX = 2**2048
MR_TESTS = 5

def isPrimeMR(n):
    if n % 2 == 0 or n % 5 == 0:
        return False
    
    for prime in LOW_PRIMES:
         if (n == prime):
             return True
         if (n % prime == 0):
             return False
    
    d = (n - 1) // 2
    s = 1
    while d % 2 == 0:
        d //= 2
        s += 1

    for _ in range(MR_TESTS):
        a = SystemRandom().randint(2, n - 1)
        if pow(a, d, n) != 1:
            for i in range(s):
                if pow(a, (2**i) * d, n) == n - 1:
                    break
                if i == s - 1:
                    return False
    return True

def primeSieve(sieveSize):
    # Returns a list of prime numbers calculated using
    # the Sieve of Eratosthenes algorithm.

    sieve = [True] * sieveSize
    sieve[0] = False # Zero and one are not prime numbers.
    sieve[1] = False

    # Create the sieve:
    for i in range(2, int(sqrt(sieveSize)) + 1):
        pointer = i * 2
        while pointer < sieveSize:
            sieve[pointer] = False
            pointer += i

    # Compile the list of primes:
    primes = []
    for i in range(sieveSize):
        if sieve[i] == True:
            primes.append(i)

    return primes
LOW_PRIMES = primeSieve(100)

def genPrime():
    rand = SystemRandom().randint(PRIME_LARGE_MIN, PRIME_LARGE_MAX)
    if rand % 2 == 0:
        rand += 1

    while not isPrimeMR(rand):
        rand += 2
        if rand > PRIME_LARGE_MAX:
            rand = SystemRandom().randint(PRIME_LARGE_MIN, PRIME_LARGE_MAX)
    return rand

def encrypt(keyp, m):
    N,e = keyp
    return pow(bytes_to_long(m.encode('utf-8')), e, N)

def decrypt(keyp, m):
    N,e = keyp
    return long_to_bytes(pow(m, e, N)).decode('utf-8')


p = genPrime()
q = genPrime()
r = genPrime()

n1 = p * q
n2 = p * r 
e = 65537

c1 = encrypt((n1, e), 'pecan{r3us1ng_pr1')
c2 = encrypt((n2, e), 'm3s_i5_b4d}')

print((n1, c1))
print((n2, c2))