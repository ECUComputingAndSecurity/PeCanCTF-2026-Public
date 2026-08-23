Common password. Brute force it.

Rockyou.txt contains the password early on, making it a very quick crack

Solution: `fcrackzip -b -D -p /usr/share/wordlists/rockyou.txt -u ./archive.zip`, and find the password is "!geez!". `unzip archive.zip` using the password to get the flag.

## Alt solution
Participants can actually just use John the ripper
`zip2john archive.zip > hash.txt`
`john --wordlist=/usr/share/wordlists/rockyou.txt hash.txt`
Find the password is !geez!
`unzip archive.zip`