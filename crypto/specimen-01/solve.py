def decrypt(code):
    binary_value = ""
    for c in code:
        if "A" == c:
            binary_value += "00"
        if "T" == c:
            binary_value += "01"
        if "C" == c:
            binary_value += "10"
        if "G" == c:
            binary_value += "11"

    for val in range(0, len(binary_value), 8):
        print(chr(int(binary_value[val:val+8], 2)), end="")

dna = "TGAATCTTTCAGTCATTCGCTGCGTCAGAGTGTCTCTTGGTGACTGTTTCGCAGTTTTGGAGATTCGCTTGGTCGTTGCTTTGGTCACAGATAGAAAGAATCTATGGT"

decrypt(dna)