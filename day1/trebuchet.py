"""
trebuchet.py
Author: Nathan James
Date: 2024/10/20

Day 1, Puzzle 1 + 2

From a given input find the calibration value in each line where the two-digit
number corresponds to the first digit and last digit of the line, respectively
in that order. Finally, sum all the calibration numbers.
"""

from string import digits

from numpy import inf
import pandas as pd


digits_df = pd.DataFrame(
    {
        "char": list(digits),
        "word": [
            "zero",
            "one",
            "two",
            "three",
            "four",
            "five",
            "six",
            "seven",
            "eight",
            "nine",
        ],
    }
)


def get_digits(line: str) -> int:
    first_d = (
        digits_df.map(line.find)
        .replace(-1, inf)
        .min(axis=1)
        .sort_values(ascending=True)
        .first_valid_index()
    )
    last_d = (
        digits_df.map(line.rfind)
        .replace(-1, -inf)
        .max(axis=1)
        .sort_values(ascending=False)
        .first_valid_index()
    )
    return int(f"{first_d}{last_d}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-f",
        type=argparse.FileType("r"),
        dest="input",
        help="input file to parse for coordinates",
    )
    parser.add_argument(
        "-v",
        action="store_true",
    )
    args = parser.parse_args()

    file_lines = pd.read_csv(args.input, header=None)
    file_lines["coords"] = file_lines.map(get_digits)
    ans = file_lines["coords"].sum()
    if args.v:
        print(file_lines)

    print(f"The sum of all calibration values is {ans}.")
