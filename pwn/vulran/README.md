This challenge consists of an old, poorly written, legacy military service by a futuristic imaginary country being attacked by aliens. The goal is to find nuclear launch codes to launch an attack against these aliens. This challenge aims to teach players basic reverse engineering skills, and conducting exploits against stack vulnerabilities.

The players will be given the IP and port of the insecure service, which they can connect to. They can do a few operations: `list`: list existing documents, `read`: read documents, `readl`: read documents with long names, `auth`: authenticate and `launch`. A few things can be noticed by interacting with the server:

Reading the binary `vulran_secret_service` will leak it to the player. The player can write a simple script to capture the binary and save it on their VM. Players can then use rev tools like ghidra to hunt for bugs. Note that the binary has stack canary enabled! Which means we can't just simply write to the return address with the address of a gadget that opens and displays the flag file.

Firstly, let's try to authenticate, the intended solution will not work unless we have access to `read`. We don't have the password, trying to read `password.txt` will fail as it is blacklisted from reading. In the `auth` function, a simple buffer overrun allows us to write up to 16 bytes past the input buffer. Note that the first byte is a read pointer, while the second byte is a pointer to an output message to be displayed at the end. The first pointer is unimportant, we can set it as it is before (address of `isAuthenticated`), as long as it doesn't segfault, or resolve to 0. The second pointer however, can be set to point to the global `password` buffer, which holds the actual password, which allows the real password to be printed and leaked. We can then capture this password and attempt to `auth` again with it, this time it will succeed.

(Note that here we practically have an arbitrary read vulnerability. While reading the stack canary is possible, it is made difficult with ALSR, which means we have to leak stack base somehow. While this is possible I believe doing so is harder than the intended solution.)

Now we have access to `read`. Note that inputting `read` and `readl` goes to the same function `readFile`, except `read` sets the input `longMode` option to 0 and `readl` sets it to 1. The input is then negated and placed inside a `shortMode` variable. This function reads from the input into `bufLocation`, which points to a local buffer if `shortMode=0`, otherwise it points to an malloc'd chunk. Note that there's no intended vulnerabilities when using `readl`, as the `fgets` call correctly respects the chunk size. However, in short mode, the size passed into `fgets` is 33, while the buffer itself is 32. This allows the null byte to overflow into the next contiguous variable, which is `shortMode`. We can then use this vulnerability to set `shortMode` to 0, which keeps the `bufLocation` to point to the stack buffer while the size passed into `fgets` becomes 128.

After doing this, we can now overrun the `whitelist` and `blacklist` arrays, which keeps track of document names whitelisted for reading and those that are blacklisted. A document can only be read if it is in the whitelist **and not** in the blacklist. Using ghidra, we can find the address of the string `launch_codes.txt`, and add it to the whitelist entries, while entries in the blacklist can be replaced by placeholder file names that we don't need to read to get our flag.

There's just one small problem: fgets and sending the line appends a line break followed by a null byte `0x0010` to the name, naively overwriting each entry in the blacklist will touch the canary. So instead, we write enough to remove `launch_codes.txt` from the blacklist, and `0x0010` will set the least-significant two bytes of the next entry, corrupting it, but will not cause a segfault since it is still pointing in the data section.

The program will then display the launch codes, which can be captured. Using the `launch` command followed by the captured launch code, we successfully initiate the attack and obtain the flag.

**Solution Files:**

[sol.py](https://github.com/user-attachments/files/29451468/sol.py)

[leak_binary.py](https://github.com/user-attachments/files/29451469/leak_binary.py)