"""
--- Day 7: Bridge Repair ---
https://adventofcode.com/2024/day/7

--------------------- Part I ---------------------
Total calibration result: 1289579105366

-------------------- Part II ---------------------
Total extended calibration result: 92148721834692
"""


from itertools import product
from typing import TypeAlias


Equation: TypeAlias = tuple[int, tuple[str, ...]]
CalibrationMap: TypeAlias = list[Equation]

OPERATORS = ('+', '*')

def load_calibration(input: str) -> CalibrationMap:
    return [
        (int(left), tuple(right.strip().split()))
            for left, right in (
                line.split(":") for line in input.strip().split("\n")
        )
    ]

def process_calculations(numbers: tuple[str, ...], operators: tuple[str, ...]) -> int:
    n_it = iter(numbers)
    calc = next(n_it)
    for op in operators:
        calc = str(eval(f"{calc}{op}{next(n_it)}"))
    return int(calc)

def can_solve(equation: Equation, operators=OPERATORS) -> bool:
    sol, nums = equation
    op_combos = product(operators, repeat=len(nums)-1)
    for op_set in op_combos:
        if process_calculations(nums, op_set) == sol:
            return True
    return False


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
    calibration = load_calibration(file.read())
    total_calibartion = sum(equation[0] for equation in calibration if can_solve(equation))
    print(f"Total calibration result: {total_calibartion}")

    if args.test:
        ans = 3749
        assert total_calibartion == ans, f"Total calibration result didn't match expected ({ans})"

    print()
    print(" Part II ".center(50, "-"))
    extended_ops = (*OPERATORS, '')
    total_extended_calibartion = sum(equation[0] for equation in calibration if can_solve(equation, operators=extended_ops))
    print(f"Total extended calibration result: {total_extended_calibartion}")

    if args.test:
        ans = 11387
        assert total_extended_calibartion == ans, f"Extended calibration did not match expected ({ans})"

