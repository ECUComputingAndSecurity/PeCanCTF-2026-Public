activate: PECAN+ CTF 2026 reverse engineering challenge.
Java program which poses as proprietary software that needs to be 'activated' to run.
Competitor expected to decompile the program to reverse-engineer the expected activation logic; the correct activation
key is the flag value.

Description for Players: Closed doors. Next-level obfuscation technology. But you don't have the keys.

Flag:

```
pecan{9668-2015-0080-3526}
```

Solution:

```
% java -jar target/activate-1.0.0.jar pecan{9668-2015-0080-3526}
---------------------------------------------------------------------------
Proprietary Software 9000

This software is protected by Placebo Obfuscation technology.
---------------------------------------------------------------------------

--- Software Activated ---
License Key: pecan{9668-2015-0080-3526}
This program has been activated successfully. Thank you for your purchase.
```

Assumed resolution process:

1. Competitor downloads challenge JAR binary
2. May attempt to run JAR if they have a host with Java runtime installed, or skip to #3.
   - May attempt to install runtime to run JAR.
   - Will run program with no arguments, which gives a hint to use '--debug' parameter.
   - Debug parameter hints that the competitor will need to reverse engineer the program to progress (in this case,
decompiling the JAR).
3. Competitor decompiles the JAR using a Java decompiler (these are available online with no installation required).
4. Competitor navigates general logic of the program and understand how activation works given the
reverse-engineered logic.
5. Competitor specifies license key (flag value) and program advises the key is correct.

Author: Lachlan Adamson <lachy@lachy.space>

[activate-1.0.0.jar.zip](https://github.com/user-attachments/files/28697204/activate-1.0.0.jar.zip)
