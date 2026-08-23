#!/usr/bin/env python3
import json
from pathlib import Path

JSON_PATH = Path(__file__).with_name("HammingCodes.json")


def is_power_of_two(x):
    return x > 0 and (x & (x - 1)) == 0


def build_code_to_data_map():
    mapping = {}
    di = 0
    for pos in range(1, 72):
        if not is_power_of_two(pos):
            mapping[pos] = di
            di += 1
    return mapping


def recover_char(matrix, ec_bin, code_to_data):
    pos = int(ec_bin, 2)
    if pos not in code_to_data:
        raise ValueError(f"EC {ec_bin} ({pos}) does not map to a data bit position")

    data_index = code_to_data[pos]
    row = data_index // 8
    col = data_index % 8

    row_bits = matrix[row][:]
    row_bits[col] ^= 1

    return chr(int("".join(map(str, row_bits)), 2))


def load_data(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if "matrices" not in data:
        raise ValueError("HammingCodes.json must contain a top-level 'matrices' object")
    if "ec_table_rows" not in data:
        raise ValueError("HammingCodes.json must contain a top-level 'ec_table_rows' array")

    matrices = data["matrices"]
    ec_table_rows = data["ec_table_rows"]

    required = [f"matrix_{i}" for i in range(1, 5)]
    for key in required:
        if key not in matrices:
            raise ValueError(f"Missing {key} in 'matrices'")
        matrix = matrices[key]
        if len(matrix) != 8 or any(len(row) != 8 for row in matrix):
            raise ValueError(f"{key} must be an 8x8 matrix")

    return matrices, ec_table_rows


def solve_flag(matrices, ec_table_rows):
    code_to_data = build_code_to_data_map()
    out = []

    for row in ec_table_rows:
        for i in range(1, 5):
            ec = row.get(f"matrix_{i}")
            if ec is None:
                continue
            ch = recover_char(matrices[f"matrix_{i}"], ec, code_to_data)
            out.append(ch)

    return "".join(out)


def main():
    matrices, ec_table_rows = load_data(JSON_PATH)
    flag = solve_flag(matrices, ec_table_rows)
    print(flag)


if __name__ == "__main__":
    main()