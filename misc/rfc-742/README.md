# Solution

The challenge runs the finger protocol, which is pointed at with how the name is 'RFC 742', which is the RFC number of 'finger' protocol.

This challenge is very easy to solve:
just nc in:

```bash
$ nc localhost 8000

users on this server:
raahguu
xanarto
morris
^C
```

Then go through each user to see if they have the flag:
```bash
$ nc localhost 8000
raahguu
user: raahguu
name: Joshua
dir: /home/raahguu
shell: /bin/sh
plan:
...Make Challenges...
...Write Flags...^C

$ nc localhost 8000
xanarto
user: xanarto
name: Xanarto Xanarto
dir: /home/xanarto
shell: /bin/sh
plan:
1.Refine my coding skills
2.Figure out how to run GIMP in the browser^C

$ nc localhost 8000
morris
user: morris
name: Morris Worm
dir: /home/morris
shell: /bin/sh
plan:
Infect Everything
Including: pecan{p0k3_p0k3_d07_do7_do7_p0k3_p0k3}^C
```

And there is the flag
```flag
pecan{p0k3_p0k3_d07_do7_do7_p0k3_p0k3}
```
