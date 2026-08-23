# One Guess
The game is simple: guess the number, get the flag.

## Solution

1. Open `main.c` in your favourite editor and decompile `chall` with your
   favourite decompiler.

2. Read the source code
    - The program generates a random `unsigned int` by reading from
      `/dev/urandom`. This should imply that actually guessing the number isn't
      feasible.
    - The program gives the user one attempt to guess the number. If the guess
      is incorrect, the program prints if the guess was too high or too low. If
      the guess is correct the program prints the flag.
    - The fact that the program uses a `while` loop and prints if the guess was
      too high or too low is interesting. If the `while` loop had a higher
      upper bound it would be possible to use the feedback to perform a binary
      search for the correct number.

3. Discover the vulnerability.
    - The key vulnerability of the program is in the call to `scanf` which uses
      a `%lu` format specifier to read into an `unsigned int`.
    - The `%lu` format specifier should be used to read into a `long unsigned
      int`, not an `unsigned int`. On the target platform a `long unsigned int`
      is 8 bytes while an `unsigned int` is 4 bytes.
    - This mismatch causes `scanf` to write 8 bytes into a 4 byte variable,
      overflowing into the next field in the `struct game`.

4. Determine the struct layout.
    - The program stores its state in a `struct game`:
      ```c
      struct game {
        unsigned int target;
        unsigned int guess;
        int count;
      };
      ```
    - Struct fields are laid out in memory in the order they are declared.
      Therefore the layout is:
      ```
      target
      guess
      count
      ```
    - Since `guess` comes immediately before `count`, the extra 4 bytes written
      by `scanf` overwrite `count`.

5. Exploit the vulnerability.
    - By overflowing a negative number into `count`, you can cause the `while`
      loop to execute another iteration.
    - It is important to realise that you have to keep overflowing. You cannot
      just write a really negative number once and call it a day. Each call to
      `scanf` writes 8 bytes, meaning you are always overwriting `count`. You
      need to ensure that it remains negative on every iteration.
    - Now the challenge becomes a simple binary search problem. Use the feedback
      from the program to maintain an upper and lower bound, then continue
      guessing the middle value while adjusting the bounds until the correct
      number is found.
