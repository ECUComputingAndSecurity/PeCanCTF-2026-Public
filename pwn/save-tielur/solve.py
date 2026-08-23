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