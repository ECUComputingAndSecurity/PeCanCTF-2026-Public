# Mean Bean Emailing Machine

**Author:** Dio Lea, diol@our.ecu.edu.au

## Challenge Description:
Dearest SOC Analyst,

Our employer and Earth's greatest mega corp Bean Co. has been hit with a cyber attack in retaliation for their purchase of all legal rights to the rain. In spite of all Bean Co. systems crashing we've determined the cause to be a phishing attack. We know you've been wanting that promotion so it's your job to search Bean Co.'s email logs to find out just what kind of malware we're dealing with.

As for your reward, the CEO will personally give himself all the credit and a $10M bonus for your hard work.

For the shareholders!!

-Middle Manager Mike

## Flag
pecan{n3ver_b34n_b3tter}

## Files to Distribute
- bean_co_email_logs.json

# Writeup

After opening the json file we see a big wall of unorganised mess. After writing a quick program to organise it into a viewable format I can see keys that imitate real email logs such as DKIM, DMARC, and SPF. These may be unfamiliar to me so I research them and find that they are email authentication methods used to stop spam and phishing emails. If we suspect a phishing attack then it's safe to assume the email might have failed these checks. 

The phishing email must have had an attachment or a link. There are no links found when searching the email "body" keys.Though filtering by attachments narrows it down there are still far too many. Filtering by attachment and any failed authentications produces a much more manageable result though still too many to search manually. Trying all 3 authentications as a "fail" will not work either as the malicious email failed spf and dkim but passed dmarc allowing it to get through. Searching for an email by failed spf and dkim but passed dmarc will yield the malicious email.

Email attachments are encoded in base 64 so after running the attachment data through a base 64 decoder I will find a .gz file, our "malware".

Strings or grep will not yield the flag as it has been obfuscated. Using Ghidra I can see the decompiled C code in the main function. From here I can see that the flag has been obfuscated using an xor for loop with a key of 0x2a. Using the key I can xor the values stored in the main function's local variables to produce the flag.


# Secondary Writeup (Raahguu)

I just made a program that loops through the entire json file for all attachments, then uses the linux `file` command to see if it shows up as anything more then junk data.

If it does then it saves the file for later analysis:

``` python
import subprocess
import json

with open("../bean_co_email_logs.json", "r") as f:
    data = json.load(f)

for message in data:
    if message["attachment"] is None:
        continue

    # there is an attachment of some kind

    subprocess.run(f"echo {message["data"]} | base64 -d > temp.txt", shell=True)
    filetype = subprocess.check_output("file temp.txt", shell=True)

    # check for junk data
    if filetype == b"temp.txt: data\n":
        subprocess.run("rm temp.txt", shell=True)
        continue

    subprocess.run("mv temp.txt $(md5sum temp.txt | cut -d' ' -f1)", shell=True)
```


The files you get from that are:

``` bash
$ file *
0cf7d4b63400b8f0205ee7cf4177ed2a: OpenPGP Secret Key
3a348c5f874e85791b69a2a2426a3820: OpenPGP Public Key
4a1ebb27027f73b45ddcea3c516fb768: DOS executable (COM), maybe with interrupt 22h, start instruction 0xb8d4959c 5f1a0376
52726ec3e54dd6cb850f606fd20f683b: DOS executable (COM), start instruction 0x8c618e74 44ac974e
87e0580db2df0065c6a775ce7eba3a5b: OpenPGP Secret Key
8990dc821d3b2cf94ca911090e76049a: OpenPGP Public Key
93163c10441b46db563c5231799a995e: OpenPGP Secret Key
97d33582e5bef40aea76790451f1e8cf: OpenPGP Secret Key
a656d538166ed13eaa90e3a4e032d606: Zip archive data, at least v2.0 to extract, compression method=deflate
d0e9e842a6054608ea3f9f541e74f314: OpenPGP Public Key
```

OpenPGP is an extremely permissive format, and the two DOS executables appear to be corrupted, so the only actual file in those logs was the zip archive.

``` bash
$ unzip a656d538166ed13eaa90e3a4e032d606
Archive:  a656d538166ed13eaa90e3a4e032d606
  inflating: flag
$ file flag
flag: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=c25afe66add44f4b27c8e9e80261487a97fdab92, for GNU/Linux 3.2.0, not stripped
```

Analysing the binary the code is:

``` c
int main(void)
{
  byte local_28 [28];
  uint local_c;
  
  local_28[0] = 0x5a;
  local_28[1] = 0x4f;
  local_28[2] = 0x49;
  local_28[3] = 0x4b;
  local_28[4] = 0x44;
  local_28[5] = 0x51;
  local_28[6] = 0x44;
  local_28[7] = 0x19;
  local_28[8] = 0x5c;
  local_28[9] = 0x4f;
  local_28[10] = 0x58;
  local_28[0xb] = 0x75;
  local_28[0xc] = 0x48;
  local_28[0xd] = 0x19;
  local_28[0xe] = 0x1e;
  local_28[0xf] = 0x44;
  local_28[0x10] = 0x75;
  local_28[0x11] = 0x48;
  local_28[0x12] = 0x19;
  local_28[0x13] = 0x5e;
  local_28[0x14] = 0x5e;
  local_28[0x15] = 0x4f;
  local_28[0x16] = 0x58;
  local_28[0x17] = 0x57;

  for (local_c = 0; local_c < 0x18; local_c = local_c + 1) {
    local_28[(int)local_c] = local_28[(int)local_c] ^ 0x2a;
  }

  return 0;
}
```

This decrypts the flag, then returns.

The line of assembly that returns is line `118a` or `*main + 0x64`

Therefore using gdb:

``` gdb
$ gdb flag    
GNU gdb (Debian 17.1-3) 17.1
Copyright (C) 2025 Free Software Foundation, Inc.
License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.
Type "show copying" and "show warranty" for details.
This GDB was configured as "x86_64-linux-gnu".
Type "show configuration" for configuration details.
For bug reporting instructions, please see:
<https://www.gnu.org/software/gdb/bugs/>.
Find the GDB manual and other documentation resources online at:
    <http://www.gnu.org/software/gdb/documentation/>.

For help, type "help".
Type "apropos word" to search for commands related to "word"...
Reading symbols from flag...
(No debugging symbols found in flag)
(gdb) b *&main + 0x60
Breakpoint 1 at 0x1189
(gdb) run
Starting program: /home/kali/Desktop/pecan/others/bean/Mean Bean Emailing Machine/flag 
[Thread debugging using libthread_db enabled]
Using host libthread_db library "/usr/lib/x86_64-linux-gnu/libthread_db.so.1".

Breakpoint 1, 0x0000555555555189 in main ()
(gdb) x/s $rbp-0x20
0x7fffffffdc60: "pecan{n3ver_b34n_b3tter}\320\f\376\367\030"
```

there is the flag:

``` flag
pecan{n3ver_b34n_b3tter}
```

