# Hamming Codez Writeup

## Overview

This challenge gives you four 8x8 binary matrices and a separate EC table.

The main trick is that the ECs are not meant to be solved matrix by matrix. They have to be read in the visual order shown in the table, top to bottom and left to right within each row.

Once you do that, each EC tells you which single bit to flip, and the affected row becomes an ASCII character.

## What the program is doing

Each matrix contains 64 data bits arranged in row-major order.

Those 64 bits are treated as the data portion of a Hamming-style codeword, where parity positions sit at powers of two and the remaining positions hold the real matrix bits.

That means the EC value can be treated as a syndrome position. Once you know that position, you can map it back to one data bit in the 8x8 matrix.

After that, you flip that bit, take the row containing the flipped bit, and read that 8-bit row as ASCII.

## math

For 64 data bits, we need enough parity bits \(p\) to satisfy:

```text
2^p >= 64 + p + 1
```

Using \(p = 7\) works because:

```text
2^7 = 128 >= 72
```

So the codeword has 71 positions total, with parity bits at positions:

```text
1, 2, 4, 8, 16, 32, 64
```

Every other position is one of the 64 real matrix bits.

If an EC is, for example, `0100110`, that is decimal 38.

So the intended error location is codeword position 38. We look up which data bit occupies that position, convert that back into a matrix row and column, flip it, and decode the row.

## EC table order

The matrices are fixed, and the EC table gives the real solve order.

The important part is that the table order is the message order. You do not solve every EC from Matrix 1 first, then Matrix 2, and so on.

You solve them exactly as they appear in the visual table.

The corrected EC table used by the solver is:

```python
ec_table = [
    (None, None, "0100110", None),
    (None, "0000111", None, None),
    (None, "1000100", None, "0011010"),
    (None, None, "0010110", "0110110"),
    (None, "0100100", "0000110", None),
    ("0000111", None, None, None),
    ("0101001", None, None, None),
    ("0100110", None, "0101000", None),
    (None, None, "1000100", "1000110"),
    (None, "0100111", "0111100", None),
    ("0111000", None, None, None),
    ("0011010", None, "0101000", None),
    (None, None, "0010100", None),
    ("1000101", "0100111", None, "1000110"),
    ("0101111", None, "0010100", None),
    (None, "0111110", None, None),
]
```

## First few steps

The first visible EC in the intended order is `0100110` under Matrix 3.

That points to codeword position 38. In Matrix 3, that maps to the bit at row 3, column 7 using zero-based indexing.

That row starts as:

```text
01110001
```

Flipping the last bit gives:

```text
01110000
```

That is ASCII `p`.

The next code is `0000111` under Matrix 2, which gives `e`.

Then `1000100` under Matrix 2 gives `c`, and `0011010` under Matrix 4 gives `a`.

So the flag starts as:

```text
peca
```

At that point the solve path is clear. Keep applying the same process in the table order until every EC has been consumed.

## Solver
refer to solver.py

## Full solve steps

1. Read the EC table in the visual order shown in the challenge.
2. For each EC, convert the binary string to its decimal syndrome position.
3. Map that syndrome position back to the corresponding data bit in the chosen matrix.
4. Flip that one bit.
5. Take the affected row and decode it as ASCII.
6. Append the recovered character.
7. Repeat until the full string is recovered.

## Flag

```text
pecan{1tsh4mm1n_t1m3_n1c3}
```