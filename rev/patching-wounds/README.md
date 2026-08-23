## Solution

Looking at this binary in ghidra, it is a simple if statement, which checks if a function returns `1` or `0`, and prints the flag if it returns `0`:

```c
char * generate_flag(void)
{
  char *pcVar1;
  byte local_19;
  ulong local_18;
  
  pcVar1 = malloc(0x2e);
  if (pcVar1 == (char *)0x0) {
    pcVar1 = (char *)0x0;
  }
  else {
    local_19 = 0x3a;
    for (local_18 = 0; local_18 < 0x2d; local_18 = local_18 + 1) {
      pcVar1[local_18] = enc.0[local_18] ^ local_19;
      local_19 = local_19 * '\r' + 0x11;
    }
    pcVar1[0x2d] = '\0';
  }
  return pcVar1;
}

int is_wounded(void)
{
  return 1;
}

int main(void)
{
  int iVar1;
  char *__format;
  
  puts("Hold on soldier, let me check if you are wounded!");
  puts("Checking if wounded...");
  putchar(0x2e);
  putchar(0x2e);
  puts(".");
  iVar1 = is_wounded();
  if (iVar1 == 0) {
    puts("Congrats soldier, it seems you made it out of that battle without any wounds!");
    puts("As a reward here is a medal for you");
    __format = generate_flag();
    printf(__format);
  }
  else {
    puts("I\'m afraid your wounded soldier, it looks like you wont make it");
  }
  return 0;
}
```

With how the challenge is called `patching wounds`, and there is a function which just returns `1`, but we need to return `0`, it is obvious that you are supposed to `patch` the binary.

By right clicking the assembly code saying `MOV EAX, 0x1` in the `is_wounded` function in ghidra, then clicking `patch instruction`, the instruction can be changed to `MOV EAX, 0x0`, then `export`ing the new file as an `original file`.

This patches the binary which can now be run to output:
```bash
$ ./patched 
Hold on soldier, let me check if you are wounded!
Checking if wounded...
...
Congrats soldier, it seems you made it out of that battle without any wounds!
As a reward here is a medal for you
pecan{y0u_p4tch3d_up_th4t_w0und_w377_507d13r}
```

instead of the old one:
```bash
$ ./patch_wounded
Hold on soldier, let me check if you are wounded!
Checking if wounded...
...
I'm afraid your wounded soldier, it looks like you wont make it
```

Getting the flag:
```flag
pecan{y0u_p4tch3d_up_th4t_w0und_w377_507d13r}
```