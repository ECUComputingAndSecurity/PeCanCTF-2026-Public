# SaveTielurCTF Writeup

## Overview

This challenge is a 32-bit unsigned integer overflow/underflow ctf.

TIELUR starts with a big chunk of HP and keeps losing health every tick. You get one chance to lock in a healing plan, and if you choose the right combination of items, the HP calculation underflows and TIELUR survives with 1 HP left.

If you choose the wrong healing items, TIELUR dies.

## What the program is doing

- `START_HP = 4026579840`
- `TICK_DAMAGE = 268435456`
- `CRITICAL_HP = 268483456`
- `UINT32_MAX_VALUE = 4294967295`

When the program starts, you’re in a preparation phase. Nothing is ticking down yet, so you can inspect the inventory first.

The two commands that matter are:

- `inventory`
- `heal <indices...>`

`inventory` shows all heal items and their values.

`heal` locks in your chosen set of item indices.

After the user runs heal, TIELUR loses `268435456` HP every 0.4 seconds until it reaches the critical HP value/threshold. At that exact point, the prepared healing burst is applied automatically.

Then one more damage tick happens.

If the HP integer underflows and becomes exactly `4294967295`, the program treats that as success (> max 32 unsigned int - 1) and runs a final step that drops TIELUR to exactly `1` HP. That prints the flag.

If the HP integer underflows to anything else, the boss dies from the ultimate attack and you lose. The last attack is dynamic (up to max 32 unsigned int - 1) and does not trigger further underflow.

## math

Let the total of your chosen healing items be H.

At the critical point, the boss is at:

```text
268483456 HP
```

Then the game applies the chosen heal, followed by one more damage tick:

```text
268483456 + H - 268435456
```

That simplifies to:

```text
H + 48000
```

For the challenge to succeed, that result needs to be exactly:

```text
4294967295
```

So:

```text
H + 48000 = 4294967295
```

Which means:

```text
H = 4294919295
```

The next step is finding a subset of inventory values that adds up to `4294919295`.

## Inventory values

These are the heal values shown in the program:

1. 536864881
2. 536865136
3. 536864882
4. 536865392
5. 536864884
6. 536865904
7. 536866928
8. 536864888
9. 536868976
10. 536864896
11. 536873072
12. 536881264
13. 536864912
14. 536897648
15. 536930416
16. 536864944
17. 536995952
18. 537127024
19. 536865008
20. 537389168

## Finding the subset in code

Since there are only 20 values, the easiest way to find the right combination is just brute force all subsets until one of them sums to `4294919295`.

```python
from itertools import combinations

vals = [
    536864881, 536865136, 536864882, 536865392, 536864884,
    536865904, 536866928, 536864888, 536868976, 536864896,
    536873072, 536881264, 536864912, 536897648, 536930416,
    536864944, 536995952, 537127024, 536865008, 537389168
]

target = 4294919295

for r in range(1, len(vals) + 1):
    for combo in combinations(range(len(vals)), r):
        total = sum(vals[i] for i in combo)
        if total == target:
            print("indices:", [i + 1 for i in combo])
            print("total:", total)
            raise SystemExit
```

This prints:

```text
indices: [1, 3, 5, 8, 10, 13, 16, 19]
total: 4294919295
```

## Correct heal plan

The intended solve is:

```text
heal 1 3 5 8 10 13 16 19
```

Those values add up to:

```text
536864881
+ 536864882
+ 536864884
+ 536864888
+ 536864896
+ 536864912
+ 536864944
+ 536865008
= 4294919295
```

## Why that works

Once TIELUR hits the critical HP value, the game applies that heal plan.

So the HP calculation becomes:

\[
268483456 + 4294919295 - 268435456
\]

That simplifies to:

\[
4294967295
\]

That is `UINT32_MAX_VALUE`, so the program takes the success branch.

After that, the final strike subtracts `4294967294`, which leaves:

\[
1 HP
\]

So TIELUR survives with exactly 1 HP, and the flag is thus printed.

## Full solve steps

1. Connect to the challenge.
2. Run `inventory` if you want to inspect the values manually.
3. Use the Python script above to find the subset.
4. Enter:

```text
heal 1 3 5 8 10 13 16 19
```

5. Wait for the automatic combat sequence to finish.
6. The heal triggers at critical HP threshold.
7. The HP wraps to the exact success value.
8. TIELUR survives on 1 HP.
9. The flag is revealed.

## Flag

```text
pecan{Y0U_S4VeD_T1ELuR_G0ODJ0B26}
```