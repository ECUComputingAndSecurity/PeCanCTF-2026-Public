## Solution

People who did this challenge may hate me now, but I did not use any anti-AV detection technique I have not seen actual malware use in the wild (malware analysis can be painful)

The challenge provides a big bash file, that is obfuscated

```bash
auSgZMFxMdpZaaXV=ZGVmIHFBeGhCQUREZ1lk...5QnZ5KCk=
cWhMkhXzwADwgrBT=cXhlVXNaU3BWWnBWd2JNWD1SSkdBTFJHTkFFTE9VSEFSS0pHQkxBSE5HQUJVClBKS3RlZlRNeVdwbURZRVI9cHl0aG9uMwpwYWM9cHljcnlwdG9kb21lCnNyYz1zb3VyY2UKZ3JyPXJtCnBpcGU9cGlwCnY9dmVudgppbj1pbnN0YWxsCmVjPWVjaG8KYj1iaW4vYWN0aXZhdGUKYmE9YmFzZTY0CnQ9QkJBSlRLZ2R3alBLRGdnZS5weQptPSR0Cnk9JHQK
eval $(echo $cWhMkhXzwADwgrBT | base64 -d)
$PJKtefTMyWpmDYER -m $v $qxeUsZSpVZpVwbMX
$src $qxeUsZSpVZpVwbMX/$b
$pipe $in -q $pac
$ec $auSgZMFxMdpZaaXV | $ba -d > $t
$PJKtefTMyWpmDYER $m
$grr $y && $grr -fr $qxeUsZSpVZpVwbMX
```

The third line of code, base64 decrypts the second line's value and executes it, the code turns out to be:
```bash
qxeUsZSpVZpVwbMX=RJGALRGNAELOUHARKJGBLAHNGABU
PJKtefTMyWpmDYER=python3
pac=pycryptodome
src=source
grr=rm
pipe=pip
in=install
ec=echo
b=bin/activate
ba=base64
t=BBAJTKgdwjPKDgge.py
m=$t
y=$t
```

and then replacing the variables with their values for the bash script deobfuscates to:
```bash
data=ZGVmIHFBeGhCQUREZ1lk...5QnZ5KCk=

python3 -m venv RJGALRGNAELOUHARKJGBLAHNGABU
source RJGALRGNAELOUHARKJGBLAHNGABU/bin/activate
pip install -q pycryptodome

echo $data | base64 -d > BBAJTKgdwjPKDgge.py
python3 BBAJTKgdwjPKDgge.py

rm BBAJTKgdwjPKDgge.py
rm -fr RJGALRGNAELOUHARKJGBLAHNGABU
```

So the program:
1. Makes a python venv
2. Downloads `pycryptodome`
3. Creates a python file from the `data` variable by base64 decoding it
4. Run the python program
5. Deletes the python file
6. Deletes the venv

The line that runs the python file, and the ones that delete stuff, can be removed so we securely create and can analyse the python program. This results in the python file:
```python
def qAxhBADDgYdARmEe(hUeygWaaKJCCUQea, UBcXXmyKbPeKdfrG = 1):
    import inspect
    YBvmwEESJFbDgPSs = inspect.currentframe()
    try:
        if isinstance(hUeygWaaKJCCUQea, str):
            hUeygWaaKJCCUQea = hUeygWaaKJCCUQea.encode()
        HMuSnneDEmZcMsSc = (YBvmwEESJFbDgPSs.f_back.f_code.co_name).encode()
        HMuSnneDEmZcMsSc = (HMuSnneDEmZcMsSc * (len(hUeygWaaKJCCUQea) // len(HMuSnneDEmZcMsSc) + 1))[:len(hUeygWaaKJCCUQea)]
        rRSrUUhTUxTTXGau = bytes(FmassBwRmwNDQptm ^ hCHxfWWxdqfAUjgK for FmassBwRmwNDQptm, hCHxfWWxdqfAUjgK in zip(HMuSnneDEmZcMsSc, hUeygWaaKJCCUQea))
        if UBcXXmyKbPeKdfrG != 1:
            return rRSrUUhTUxTTXGau
        return rRSrUUhTUxTTXGau.decode()
    finally:
        del YBvmwEESJFbDgPSs

def NZDmtNgNYQzxShua():
    uDExhkmWKymbRDzW = "muZqhmj3ZzFb4A/..."
    tZsHPqeZFPDTfzsF = globals()[qAxhBADDgYdARmEe(b'?\x1b<\x056\x0f#\n>\x08\x1e9\x01\x050\x04')](b"7\x03k=M&\x02=3\x00>H\x00Y\x18\x14\x141r='\x0fZs")
    JJFgMbRenhZBPPtV = globals()[qAxhBADDgYdARmEe(b'?\x1b<\x056\x0f#\n>\x08\x1e9\x01\x050\x04')](b'\x0c"\x1c\t\x04\x0e^\x00\x0fb\x08\x199=\x1f5',0)
    TwprHWfrKguCtyax = getattr(globals()[globals()[qAxhBADDgYdARmEe(b'?\x1b<\x056\x0f#\n>\x08\x1e9\x01\x050\x04')](b'\x11\x05&\x18\x1d"\x13\'7"%\'')],globals()[qAxhBADDgYdARmEe(b'?\x1b<\x056\x0f#\n>\x08\x1e9\x01\x050\x04')](b'\x11\x05-\x00\x04!\x15:\x06\x0e'))(globals()[qAxhBADDgYdARmEe(b'?\x1b<\x056\x0f#\n>\x08\x1e9\x01\x050\x04')](b'\r(=\x1d\x00!I\r0!\x12\x1d!F4$\x1d'), **{globals()[qAxhBADDgYdARmEe(b'?\x1b<\x056\x0f#\n>\x08\x1e9\x01\x050\x04')](b"((+\x00\x18'\x14:"):(globals()[qAxhBADDgYdARmEe(b'?\x1b<\x056\x0f#\n>\x08\x1e9\x01\x050\x04')](b'\x0f\x1f\x17'),)})
    yyhUkecwrPVZwBNa = getattr(globals()[globals()[qAxhBADDgYdARmEe(b'?\x1b<\x056\x0f#\n>\x08\x1e9\x01\x050\x04')](b'\x11\x05&\x18\x1d"\x13\'7"%\'')],globals()[qAxhBADDgYdARmEe(b'?\x1b<\x056\x0f#\n>\x08\x1e9\x01\x050\x04')](b'\x11\x05-\x00\x04!\x15:\x06\x0e'))(globals()[qAxhBADDgYdARmEe(b'?\x1b<\x056\x0f#\n>\x08\x1e9\x01\x050\x04')](b',;7\x08Bz'))
    kgRJKxFXjHzwAzVs = TwprHWfrKguCtyax.__dict__[globals()[qAxhBADDgYdARmEe(b'?\x1b<\x056\x0f#\n>\x08\x1e9\x01\x050\x04')](b' ?3')](JJFgMbRenhZBPPtV, TwprHWfrKguCtyax.__dict__[globals()[qAxhBADDgYdARmEe(b'?\x1b<\x056\x0f#\n>\x08\x1e9\x01\x050\x04')](b'\x03\x15\x00(+\t$\x03')], nonce=globals()[qAxhBADDgYdARmEe(b'?\x1b<\x056\x0f#\n>\x08\x1e9\x01\x050\x04')](b'\x7fmtU@xR~n`NMbPLTxjv', 0))
    return getattr(kgRJKxFXjHzwAzVs, globals()[qAxhBADDgYdARmEe(b'?\x1b<\x056\x0f#\n>\x08\x1e9\x01\x050\x04')](b"*?'\x1f\r>\x13\x118?\x1e'%\r\x07\x08(#"))(yyhUkecwrPVZwBNa.__dict__[globals()[qAxhBADDgYdARmEe(b'?\x1b<\x056\x0f#\n>\x08\x1e9\x01\x050\x04')](b',lp\t\x11-\x08*<')](uDExhkmWKymbRDzW), yyhUkecwrPVZwBNa.__dict__[globals()[qAxhBADDgYdARmEe(b'?\x1b<\x056\x0f#\n>\x08\x1e9\x01\x050\x04')](b',lp\t\x11-\x08*<')](tZsHPqeZFPDTfzsF))

def XXQQkZxUJdUWuFcr(YnzAnaKAUKBDBUVT):
    avuwVcMbRXFrtJQP = getattr(globals()[globals()[qAxhBADDgYdARmEe(b")\x19)9)\x1b<\x11-=1\x16'+&\x17")](b'\x07\x073$\x026\x0c<$\x17\n\x08')], globals()[qAxhBADDgYdARmEe(b")\x19)9)\x1b<\x11-=1\x16'+&\x17")](b'7(4?'))(globals()[qAxhBADDgYdARmEe(b")\x19)9)\x1b<\x11-=1\x16'+&\x17")](b'<!0?\t\x14\x1c\x1d\x18,\x14\x0e\x0c\x039#'), globals()[qAxhBADDgYdARmEe(b")\x19)9)\x1b<\x11-=1\x16'+&\x17")](b'/:'))
    getattr(getattr(globals()[globals()[qAxhBADDgYdARmEe(b")\x19)9)\x1b<\x11-=1\x16'+&\x17")](b'\x07\x073$\x026\x0c<$\x17\n\x08')], globals()[qAxhBADDgYdARmEe(b")\x19)9)\x1b<\x11-=1\x16'+&\x17")](b'4720\x07)'))()[globals()[qAxhBADDgYdARmEe(b")\x19)9)\x1b<\x11-=1\x16'+&\x17")](b'9.$&=957\x18<\x13%\x01\x0c2"')], globals()[qAxhBADDgYdARmEe(b")\x19)9)\x1b<\x11-=1\x16'+&\x17")](b'/*8%\x0e'))(getattr(globals()[globals()[qAxhBADDgYdARmEe(b")\x19)9)\x1b<\x11-=1\x16'+&\x17")](b'\x07\x073$\x026\x0c<$\x17\n\x08')], globals()[qAxhBADDgYdARmEe(b")\x19)9)\x1b<\x11-=1\x16'+&\x17")](b'4720\x07)'))()[globals()[qAxhBADDgYdARmEe(b")\x19)9)\x1b<\x11-=1\x16'+&\x17")](b'\x016+\x10\x05;3\x14\x1f/\x17\x137\x135&')]())
    getattr(getattr(globals()[globals()[qAxhBADDgYdARmEe(b")\x19)9)\x1b<\x11-=1\x16'+&\x17")](b'\x07\x073$\x026\x0c<$\x17\n\x08')], globals()[qAxhBADDgYdARmEe(b")\x19)9)\x1b<\x11-=1\x16'+&\x17")](b'4720\x07)'))()[globals()[qAxhBADDgYdARmEe(b")\x19)9)\x1b<\x11-=1\x16'+&\x17")](b'9.$&=957\x18<\x13%\x01\x0c2"')], globals()[qAxhBADDgYdARmEe(b")\x19)9)\x1b<\x11-=1\x16'+&\x17")](b';4>"\x0e'))()

def tVvWwPHbvyzCeVVx():
    KSsFMsjvgUvehzyS = getattr(globals()[globals()[qAxhBADDgYdARmEe(b'\x05\x17\x0e?5\x11\x0c&\x11 \x1e\x027;\x13\x1d')](b'+\t\x14"\x1e<<\x0b\x18\n%\x1c')],globals()[qAxhBADDgYdARmEe(b'\x05\x17\x0e?5\x11\x0c&\x11 \x1e\x027;\x13\x1d')](b'+\t\x1f:\x07?:\x16)&'))(globals()[qAxhBADDgYdARmEe(b'\x05\x17\x0e?5\x11\x0c&\x11 \x1e\x027;\x13\x1d')](b"\x07#\x14'\x05?+\x07\x05\n"))
    getattr(getattr(globals()[globals()[qAxhBADDgYdARmEe(b'\x05\x17\x0e?5\x11\x0c&\x11 \x1e\x027;\x13\x1d')](b'+\t\x14"\x1e<<\x0b\x18\n%\x1c')],globals()[qAxhBADDgYdARmEe(b'\x05\x17\x0e?5\x11\x0c&\x11 \x1e\x027;\x13\x1d')](b'\x189\x156\x1b#'))()[globals()[qAxhBADDgYdARmEe(b'\x05\x17\x0e?5\x11\x0c&\x11 \x1e\x027;\x13\x1d')](b'?\x05\x05\x11:#"\x14\x11,\x0c&\r,/+')], globals()[qAxhBADDgYdARmEe(b'\x05\x17\x0e?5\x11\x0c&\x11 \x1e\x027;\x13\x1d')](b'\x06#\x18'))(globals()[qAxhBADDgYdARmEe(b'\x05\x17\x0e?5\x11\x0c&\x11 \x1e\x027;\x13\x1d')](b'\x17>\x1b8\x13pc\x1aV\x1d\x03"\x0b4\x18\x1c<\x04>\x16.)\r8\''), **{globals()[qAxhBADDgYdARmEe(b'\x05\x17\x0e?5\x11\x0c&\x11 \x1e\x027;\x13\x1d')](b'\x07>\x13;\x1b'):12})
    getattr(getattr(globals()[globals()[qAxhBADDgYdARmEe(b'\x05\x17\x0e?5\x11\x0c&\x11 \x1e\x027;\x13\x1d')](b'+\t\x14"\x1e<<\x0b\x18\n%\x1c')],globals()[qAxhBADDgYdARmEe(b'\x05\x17\x0e?5\x11\x0c&\x11 \x1e\x027;\x13\x1d')](b'\x189\x156\x1b#'))()[globals()[qAxhBADDgYdARmEe(b'\x05\x17\x0e?5\x11\x0c&\x11 \x1e\x027;\x13\x1d')](b'?\x05\x05\x11:#"\x14\x11,\x0c&\r,/+')], globals()[qAxhBADDgYdARmEe(b'\x05\x17\x0e?5\x11\x0c&\x11 \x1e\x027;\x13\x1d')](b'\x06#\x18'))(globals()[qAxhBADDgYdARmEe(b'\x05\x17\x0e?5\x11\x0c&\x11 \x1e\x027;\x13\x1d')](b'Zy\x12.\x16>*,\x121(\x0b$\x0f/=.\x07'), **{globals()[qAxhBADDgYdARmEe(b'\x05\x17\x0e?5\x11\x0c&\x11 \x1e\x027;\x13\x1d')](b'\x07>\x13;\x1b'):17})
    getattr(getattr(globals()[globals()[qAxhBADDgYdARmEe(b'\x05\x17\x0e?5\x11\x0c&\x11 \x1e\x027;\x13\x1d')](b'+\t\x14"\x1e<<\x0b\x18\n%\x1c')],globals()[qAxhBADDgYdARmEe(b'\x05\x17\x0e?5\x11\x0c&\x11 \x1e\x027;\x13\x1d')](b'\x189\x156\x1b#'))()[globals()[qAxhBADDgYdARmEe(b'\x05\x17\x0e?5\x11\x0c&\x11 \x1e\x027;\x13\x1d')](b'?\x05\x05\x11:#"\x14\x11,\x0c&\r,/+')], globals()[qAxhBADDgYdARmEe(b'\x05\x17\x0e?5\x11\x0c&\x11 \x1e\x027;\x13\x1d')](b'\x06#\x18'))(globals()[qAxhBADDgYdARmEe(b'\x05\x17\x0e?5\x11\x0c&\x11 \x1e\x027;\x13\x1d')](b'\x06;Vz\x056h\x06\x0f\x18\x14!+2\x1e*<\x17/.2\n\x19'), **{globals()[qAxhBADDgYdARmEe(b'\x05\x17\x0e?5\x11\x0c&\x11 \x1e\x027;\x13\x1d')](b'\x07>\x13;\x1b'):15})

def yRmdvFdcvFqjyBvy():
    _ = XXQQkZxUJdUWuFcr(NZDmtNgNYQzxShua), tVvWwPHbvyzCeVVx()

if __name__ == "__main__":
    yRmdvFdcvFqjyBvy()
```

Looking at the easiest to reverse engineer function. and making it more readable:
```python
def qAxhBADDgYdARmEe(value, string_over_bool = 1):
    import inspect
    frame = inspect.currentframe()
    try:
        if isinstance(value, str):
            value = value.encode()
        func_name = (frame.f_back.f_code.co_name).encode()
        func_name = (func_name * (len(value) // len(func_name) + 1))[:len(value)]
        new_value = bytes(x ^ y for x, y in zip(func_name, value))
        if string_over_bool != 1:
            return new_value
        return new_value.decode()
    finally:
        del frame
```

This xor's the value passed in, with the name of the function that called this function to encode it.

Using this knowledge we can start to decode the other functions, by recreating a small version of the script where each function just prints the output of the encoding function, we can simplify the program massively

```python
def qAxhBADDgYdARmEe(value, string_over_bool = 1):
    import inspect
    frame = inspect.currentframe()
    try:
        if isinstance(value, str):
            value = value.encode()
        func_name = (frame.f_back.f_code.co_name).encode()
        func_name = (func_name * (len(value) // len(func_name) + 1))[:len(value)]
        new_value = bytes(x ^ y for x, y in zip(func_name, value))
        if string_over_bool != 1:
            return new_value
        return new_value.decode()
    finally:
        del frame

def NZDmtNgNYQzxShua():
    print("\nNZDmtNgNYQzxShua")
    print(qAxhBADDgYdARmEe(b'?\x1b<\x056\x0f#\n>\x08\x1e9\x01\x050\x04'))
    print(qAxhBADDgYdARmEe(b"7\x03k=M&\x02=3\x00>H\x00Y\x18\x14\x141r='\x0fZs"))
    print(qAxhBADDgYdARmEe(b'\x0c"\x1c\t\x04\x0e^\x00\x0fb\x08\x199=\x1f5',0))
    print(qAxhBADDgYdARmEe(b'\x11\x05&\x18\x1d"\x13\'7"%\''))
    print(qAxhBADDgYdARmEe(b'\x11\x05-\x00\x04!\x15:\x06\x0e'))
    print(qAxhBADDgYdARmEe(b'\r(=\x1d\x00!I\r0!\x12\x1d!F4$\x1d'))
    print(qAxhBADDgYdARmEe(b"((+\x00\x18'\x14:"))
    print(qAxhBADDgYdARmEe(b'\x0f\x1f\x17'))
    print(qAxhBADDgYdARmEe(b',;7\x08Bz'))
    print(qAxhBADDgYdARmEe(b' ?3'))
    print(qAxhBADDgYdARmEe(b'\x03\x15\x00(+\t$\x03'))
    print(qAxhBADDgYdARmEe(b'\x7fmtU@xR~n`NMbPLTxjv', 0))
    print(qAxhBADDgYdARmEe(b"*?'\x1f\r>\x13\x118?\x1e'%\r\x07\x08(#"))
    print(qAxhBADDgYdARmEe(b',lp\t\x11-\x08*<'))
    
def XXQQkZxUJdUWuFcr(YnzAnaKAUKBDBUVT):
    print("\nXXQQkZxUJdUWuFcr")
    print(qAxhBADDgYdARmEe(b")\x19)9)\x1b<\x11-=1\x16'+&\x17"))
    print(qAxhBADDgYdARmEe(b'\x07\x073$\x026\x0c<$\x17\n\x08'))
    print(qAxhBADDgYdARmEe(b'7(4?'))
    print(qAxhBADDgYdARmEe(b'<!0?\t\x14\x1c\x1d\x18,\x14\x0e\x0c\x039#'))
    print(qAxhBADDgYdARmEe(b'/:'))
    print(qAxhBADDgYdARmEe(b'4720\x07)'))
    print(qAxhBADDgYdARmEe(b'9.$&=957\x18<\x13%\x01\x0c2"'))
    print(qAxhBADDgYdARmEe(b'/*8%\x0e'))
    print(qAxhBADDgYdARmEe(b'\x016+\x10\x05;3\x14\x1f/\x17\x137\x135&'))
    print(qAxhBADDgYdARmEe(b';4>"\x0e'))
    
def tVvWwPHbvyzCeVVx():
    print("\ntVvWwPHbvyzCeVVx")
    print(qAxhBADDgYdARmEe(b'\x05\x17\x0e?5\x11\x0c&\x11 \x1e\x027;\x13\x1d'))
    print(qAxhBADDgYdARmEe(b'+\t\x14"\x1e<<\x0b\x18\n%\x1c'))
    print(qAxhBADDgYdARmEe(b'+\t\x1f:\x07?:\x16)&'))
    print(qAxhBADDgYdARmEe(b"\x07#\x14'\x05?+\x07\x05\n"))
    print(qAxhBADDgYdARmEe(b'\x189\x156\x1b#'))
    print(qAxhBADDgYdARmEe(b'?\x05\x05\x11:#"\x14\x11,\x0c&\r,/+'))
    print(qAxhBADDgYdARmEe(b'\x06#\x18'))
    print(qAxhBADDgYdARmEe(b'\x17>\x1b8\x13pc\x1aV\x1d\x03"\x0b4\x18\x1c<\x04>\x16.)\r8\''))
    print(qAxhBADDgYdARmEe(b'\x07>\x13;\x1b'))
    print(qAxhBADDgYdARmEe(b'Zy\x12.\x16>*,\x121(\x0b$\x0f/=.\x07'))
    print(qAxhBADDgYdARmEe(b'\x06;Vz\x056h\x06\x0f\x18\x14!+2\x1e*<\x17/.2\n\x19'))

def yRmdvFdcvFqjyBvy():
    _ = XXQQkZxUJdUWuFcr(12), NZDmtNgNYQzxShua(), tVvWwPHbvyzCeVVx()
    
if __name__ == "__main__":
    yRmdvFdcvFqjyBvy()
```

Running it gets the output:
```txt
XXQQkZxUJdUWuFcr
qAxhBADDgYdARmEe
__builtins__
open
dyanbNdHRHAYyEZQ
wb
locals
avuwVcMbRXFrtJQP
write
YnzAnaKAUKBDBUVT
close

NZDmtNgNYQzxShua
qAxhBADDgYdARmEe
yY/P9hesjQD0S1muZk6PSA==
BxXdp@9NV3rajUjT
__builtins__
__import__
Crypto.Cipher.AES
fromlist
AES
base64
new
MODE_GCM
b'1708465071451895602'
decrypt_and_verify
b64decode

tVvWwPHbvyzCeVVx
qAxhBADDgYdARmEe
__builtins__
__import__
subprocess
locals
KSsFMsjvgUvehzyS
run
chmod +x dyanbNdHRHAYyEZQ
shell
./dyanbNdHRHAYyEZQ
rm -rf dyanbNdHRHAYyEZQ
```

Then control+H (find and replace) for all the function calls with the terms, along with changing all the reflexive calls of the encoding function into normal ones changes the original python script into:

```python
def qAxhBADDgYdARmEe(hUeygWaaKJCCUQea, UBcXXmyKbPeKdfrG = 1):
    import inspect
    YBvmwEESJFbDgPSs = inspect.currentframe()
    try:
        if isinstance(hUeygWaaKJCCUQea, str):
            hUeygWaaKJCCUQea = hUeygWaaKJCCUQea.encode()
        HMuSnneDEmZcMsSc = (YBvmwEESJFbDgPSs.f_back.f_code.co_name).encode()
        HMuSnneDEmZcMsSc = (HMuSnneDEmZcMsSc * (len(hUeygWaaKJCCUQea) // len(HMuSnneDEmZcMsSc) + 1))[:len(hUeygWaaKJCCUQea)]
        rRSrUUhTUxTTXGau = bytes(FmassBwRmwNDQptm ^ hCHxfWWxdqfAUjgK for FmassBwRmwNDQptm, hCHxfWWxdqfAUjgK in zip(HMuSnneDEmZcMsSc, hUeygWaaKJCCUQea))
        if UBcXXmyKbPeKdfrG != 1:
            return rRSrUUhTUxTTXGau
        return rRSrUUhTUxTTXGau.decode()
    finally:
        del YBvmwEESJFbDgPSs

def NZDmtNgNYQzxShua():
    uDExhkmWKymbRDzW = "muZqhmj3ZzFb4A/..."
    tZsHPqeZFPDTfzsF = "yY/P9hesjQD0S1muZk6PSA=="
    JJFgMbRenhZBPPtV = b"BxXdp@9NV3rajUjT"
    TwprHWfrKguCtyax = getattr(globals()["__builtins__"],"__import__")("Crypto.Cipher.AES", **{"fromlist":("AES",)})
    yyhUkecwrPVZwBNa = getattr(globals()["__builtins__"],"__import__")("base64")
    kgRJKxFXjHzwAzVs = TwprHWfrKguCtyax.__dict__["new"](JJFgMbRenhZBPPtV, TwprHWfrKguCtyax.__dict__["MODE_GCM"], nonce=b'1708465071451895602')
    return getattr(kgRJKxFXjHzwAzVs, "decrypt_and_verify")(yyhUkecwrPVZwBNa.__dict__["b64decode"](uDExhkmWKymbRDzW), yyhUkecwrPVZwBNa.__dict__["b64decode"](tZsHPqeZFPDTfzsF))

def XXQQkZxUJdUWuFcr(YnzAnaKAUKBDBUVT):
    avuwVcMbRXFrtJQP = getattr(globals()["__builtins__"], "open")("dyanbNdHRHAYyEZQ", "wb")
    getattr(getattr(globals()["__builtins__"], "locals")()["avuwVcMbRXFrtJQP"], "write")(getattr(globals()["__builtins__"], "locals")()["YnzAnaKAUKBDBUVT"]())
    getattr(getattr(globals()["__builtins__"], "locals")()["avuwVcMbRXFrtJQP"], "close")()

def tVvWwPHbvyzCeVVx():
    KSsFMsjvgUvehzyS = getattr(globals()["__builtins__"],"__import__")("subprocess")
    getattr(getattr(globals()["__builtins__"],"locals")()["KSsFMsjvgUvehzyS"], "run")("chmod +x dyanbNdHRHAYyEZQ", **{"shell":12})
    getattr(getattr(globals()["__builtins__"],"locals")()["KSsFMsjvgUvehzyS"], "run")("./dyanbNdHRHAYyEZQ", **{"shell":17})
    getattr(getattr(globals()["__builtins__"],"locals")()["KSsFMsjvgUvehzyS"], "run")("rm -rf dyanbNdHRHAYyEZQ", **{"shell":15})

def yRmdvFdcvFqjyBvy():
    _ = XXQQkZxUJdUWuFcr(NZDmtNgNYQzxShua), tVvWwPHbvyzCeVVx()

if __name__ == "__main__":
    yRmdvFdcvFqjyBvy()
```

From here, challengers should see that the program's function 'tVvWwPHbvyzCeVVx', gives a file permission to run, runs it, then deletes it, and that the other functions have something to do with AES cryptography ('NZDmtNgNYQzxShua') where it probably decrypts the very long base64 string, and 'XXQQkZxUJdUWuFcr' which opens and writes to a file before closing it.

If they see that then they can just remove the lines that runs the file, and the ones that removes the file, then run the python program to see the next layer. If not they can start decoding the reflective measures and then do the exact same thing:

Running the python file with the executing and removal line removed created a binary called `dyanbNdHRHAYyEZQ`.

Using ghidra to reverse engineer this, gets the following `main` function:

```c
undefined8 main(void)
{
  char *__s;
  long in_FS_OFFSET;
  int local_5c;
  double local_58;
  double local_50;
  undefined8 local_48;
  undefined8 local_40;
  undefined8 local_38;
  undefined1 local_30;
  undefined7 uStack_2f;
  undefined1 uStack_28;
  undefined8 local_27;
  long local_10;
  
  local_10 = *(long *)(in_FS_OFFSET + 0x28);
  while( true ) {
    puts("Temperature Converter");
    puts("1. Celsius -> Fahrenheit");
    puts("2. Fahrenheit -> Celsius");
    puts("3. Quit program");
    printf("Choose an option: ");
    __isoc99_scanf(&DAT_00102073,&local_5c);
    if (local_5c == 3) break;
    if (local_5c < 4) {
      if (local_5c == 1) {
        printf("Enter temperature in Celsius: ");
        __isoc99_scanf(&DAT_00102097,&local_58);
        local_50 = (local_58 * 9.0) / 5.0 + 32.0;
        if (local_58 == -40.0) {
          local_48 = 0x7e616d7877757366;
          local_40 = 0x266f492672496222;
          local_38 = 0x27497822257b4963;
          local_30 = 0x62;
          uStack_2f = 0x7b496226784923;
          uStack_28 = 0x22;
          local_27 = 0x6b29256422617a;
          __s = (char *)xor_crypt(&local_48,0x16);
          puts(__s);
        }
        printf("%.2f C = %.2f F\n",local_58,local_50);
      }
      else if (local_5c == 2) {
        printf("Enter temperature in Fahrenheit: ");
        __isoc99_scanf(&DAT_00102097,&local_58);
        local_50 = ((local_58 - 32.0) * 5.0) / 9.0;
        printf("%.2f F = %.2f C\n",local_58,local_50);
      }
    }
  }
  if (local_10 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return 0;
}

long xor_crypt(long param_1,byte param_2)
{
  undefined4 local_c;
  
  for (local_c = 0; *(char *)(param_1 + local_c) != '\0'; local_c = local_c + 1) {
    *(byte *)(param_1 + local_c) = *(byte *)(param_1 + local_c) ^ param_2;
  }
  return param_1;
}
```

Making it look nicer by reading the code and formatting it correctly, the code becomes:
```c
int main(void)

{
  char *decoded_data;
  long in_FS_OFFSET;
  int choice;
  double original_temp;
  double new_temp;
  char encoded_data [56];
  long stack_length_checker;
  
  stack_length_checker = *(long *)(in_FS_OFFSET + 0x28);
  while( true ) {
    puts("Temperature Converter");
    puts("1. Celsius -> Fahrenheit");
    puts("2. Fahrenheit -> Celsius");
    puts("3. Quit program");
    printf("Choose an option: ");
    __isoc99_scanf("%d",&choice);
    if (choice == 3) break;
    if (choice < 4) {
      if (choice == 1) {
        printf("Enter temperature in Celsius: ");
        __isoc99_scanf("%lf",&original_temp);
        new_temp = (original_temp * 9.0) / 5.0 + 32.0;
        if (original_temp == -40.0) {
          builtin_strncpy(encoded_data,"fsuwxma~\"bIr&Io&cI{%\"xI\'b#Ix&bI{\"za\"d%)k",41);
          decoded_data = xor_crypt(encoded_data,0x16);
          puts(decoded_data);
        }
        printf("%.2f C = %.2f F\n",original_temp,new_temp);
      }
      else if (choice == 2) {
        printf("Enter temperature in Fahrenheit: ");
        __isoc99_scanf("%lf",&original_temp);
        new_temp = ((original_temp - 32.0) * 5.0) / 9.0;
        printf("%.2f F = %.2f C\n",original_temp,new_temp);
      }
    }
  }
  if (stack_length_checker != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return 0;
}

char * xor_crypt(char *input, byte key)
{
  int i;
  
  for (i = 0; input[i] != '\0'; i = i + 1) {
    input[i] = input[i] ^ key;
  }
  return input;
}
```

So the program is clearly a simple Fahrenheit to Celsius, and back converter, but when the value '-40' is input when converting from Celsius to Fahrenheit a secret value is output. As this is a CTF, that value is likely a flag so trying it:

```bash
$ ./dyanbNdHRHAYyEZQ                     
Temperature Converter
1. Celsius -> Fahrenheit
2. Fahrenheit -> Celsius
3. Quit program
Choose an option: 1
Enter temperature in Celsius: -40
pecan{wh4t_d0_y0u_m34n_1t5_n0t_m4lw4r3?}
-40.00 C = -40.00 F
Temperature Converter
1. Celsius -> Fahrenheit
2. Fahrenheit -> Celsius
3. Quit program
Choose an option: 3
```

And that is the flag
```flag
pecan{wh4t_d0_y0u_m34n_1t5_n0t_m4lw4r3?}
```
