## Creation Process
``` python
flag = "pecan{c7f_run5_1n_my_b100d}"
binary = "".join([f"{ord(char):08b}" for char in flag])

d = {"00": "A",
     "01": "T",
     "10": "C",
     "11": "G"}

dna = "".join([d[binary[i*2:(i+1)*2]] for i in range(len(binary)//2)])
print(dna)
```

## Writeup
Simple DNA cipher.

A: 00
T: 01
C: 10
G: 11

This is the default mapping that can be easily found on the internet, e.g. https://www.geeksforgeeks.org/dsa/dna-cryptography/

However, brute-forcing all 24 possible mappings is also easy. 

``` python
import itertools

dna = "TGAATCTTTCAGTCATTCGCTGCGTCAGAGTGTCTCTTGGTGACTGTTTCGCAGTTTTGGAGATTCGCTTGGTCGTTGCTTTGGTCACAGATAGAAAGAATCTATGGT"

mapping = ["00", "01", "10", "11"]

for item in list(itertools.permutations(mapping)):
    d = {"A": item[0],
         "T": item[1], 
         "C": item[2],
         "G": item[3]}
    
    binary = "".join([d[char] for char in dna])
    flag = "".join([chr(int(binary[i*8:(i+1)*8],2)) for i in range(0, len(binary)//8)])
    print(flag)
```
