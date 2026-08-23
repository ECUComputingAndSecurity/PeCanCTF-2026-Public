Ye Olde Programme Walkthrough

This part isn’t required but to download and use spl:
sudo apt install pipx
pipx install shakespearelang
After creating a program.spl file use "shakespeare run program.spl"

Shakespeare lang(spl) is an esoteric programming language that uses Shakespearean characters and dialogue to perform calculations. Each character is assigned an integer value based upon the noun and adjectives ascribed to them. A positive noun is a value of 1 while a negative is -1. Negative nouns can only be preceded by negative adjectives and vice versa. Each adjective multiplies the value of the noun by 2. Operations include addition(thou art the sum of x and y), subtraction (thou art the difference between x and y), and multiplication(thou art the product of x and y). By declaring “speak thy mind!” the character will convert their value into ASCII and print it to the terminal.

Competitors will need to reverse the calculations to obtain the input value assigned to Puck at the beginning of the program.

The output they are given to work back from is “spl”. the command “Speak thy mind!” converts the characters current value to an ASCII character and prints it so first they must convert the first character from an ASCII value to an integer 115.
Calculations:
a + -1 = 115 | a = 115 + 1 is 116
z + - 4 = 116 | z = 116 + 4 is 120
y – 8 = 120 | y = 120 + 8 is 128
x \* 2 = 128 | 128 / 2 is 64

The input was 64. Wrapped in flag format pecan{64}