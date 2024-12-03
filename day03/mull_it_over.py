"""
--- Day 3: Mull It Over ---
https://adventofcode.com/2024/day/3

--------------------- Part I ---------------------
The sum of the multiplications is (163931492)
Time taken: 0.000852 s

-------------------- Part II ---------------------
The sum of the enabled multiplcations is (76911921)
Time take:  0.000568 s
"""


from math import prod
import re
from time import perf_counter
from typing import Generator


def do_blocks(whole_txt: str) -> Generator[tuple[int | None, int | None]]:
    do = "do()"
    donot = "don't()"
    donot_idx = whole_txt.find(donot)
    do_idx = None
    yield do_idx, donot_idx

    while donot_idx > 0:
        do_idx = do_idx + donot_idx if (do_idx := whole_txt[donot_idx:].find(do)) > 0 else do_idx
        donot_idx = donot_idx + do_idx if (donot_idx := whole_txt[do_idx:].find(donot)) > 0 else donot_idx
        yield do_idx, donot_idx if donot_idx > 0 else None


if __name__ == "__main__":
    from argparse import ArgumentParser, FileType

    parser = ArgumentParser()
    parser.add_argument("-f", type=FileType("r"), help="file input to run the code with")
    parser.add_argument("-v", action="store_true", help="verbose")
    parser.add_argument(
        "--test",
        action="store_true",
        help="ignores file input and runs test file `example`",
    )
    args = parser.parse_args()

    if args.test:
        filename = "example.txt"
        file = open(filename, "r")
    elif args.f:
        file = args.f
    else:
        raise Exception("File or test must be specified")

    print()
    print(" Part I ".center(50, "-"))
    start = perf_counter()
    corrupt_mem = file.read()
    raw_multiplies = re.findall(r'mul\((\d+),(\d+)\)', corrupt_mem)
    multiplies = [tuple(map(int, tup)) for tup in raw_multiplies]
    sum_mul = sum(map(prod, multiplies))
    end = perf_counter()
    print(f"The sum of the multiplications is ({sum_mul})")
    print(f"Time taken: {end - start:.6f} s")

    if args.test:
        ans = 161
        assert sum_mul == ans, f"The sum of multiplications did not match the expected ({ans})"

    print()
    print(" Part II ".center(50, "-"))
    if args.test:
        example2 = "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"
        corrupt_mem = example2

    start = perf_counter()
    enabled_slices = "".join(corrupt_mem[slice(l, r)] for l, r in do_blocks(corrupt_mem))
    extracted_multiplies = re.findall(r'mul\((\d+),(\d+)\)', enabled_slices)
    enabled_pairs = [tuple(map(int, tup)) for tup in extracted_multiplies]
    sum_mul_enabled = sum(map(prod, enabled_pairs))
    end = perf_counter()
    print(f"The sum of the enabled multiplcations is ({sum_mul_enabled})")
    print(f"Time take: {end - start: .6f} s")

    if args.test:
        ans = 48
        assert sum_mul_enabled == ans, f"The sum of enabled multiplications did not match expected ({ans})"

