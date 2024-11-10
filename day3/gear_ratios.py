"""
gear_ratios.py
2024-10-29

--- Day 3: Gear Ratios ---

You and the Elf eventually reach a gondola lift station; he says the gondola lift will take you up to the water source, but this is as far as he can bring you. You go inside.

It doesn't take long to find the gondolas, but there seems to be a problem: they're not moving.

"Aaah!"

You turn around to see a slightly-greasy Elf with a wrench and a look of surprise. "Sorry, I wasn't expecting anyone! The gondola lift isn't working right now; it'll still be a while before I can fix it." You offer to help.

The engineer explains that an engine part seems to be missing from the engine, but nobody can figure out which one. If you can add up all the part numbers in the engine schematic, it should be easy to work out which part is missing.

The engine schematic (your puzzle input) consists of a visual representation of the engine. There are lots of numbers and symbols you don't really understand, but apparently any number adjacent to a symbol, even diagonally, is a "part number" and should be included in your sum. (Periods (.) do not count as a symbol.)

Here is an example engine schematic:

467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..

Part I:
In this schematic, two numbers are not part numbers because they are not adjacent to a symbol: 114 (top right) and 58 (middle right). Every other number is adjacent to a symbol and so is a part number; their sum is 4361.

Of course, the actual engine schematic is much larger. What is the sum of all of the part numbers in the engine schematic?

Part II:
In this schematic there are two gears (`*`). The first is in the top left; it has part numbers 467 and 35, so its gear ratio (product) is 16345. The second gear is in the lower right; its gear ratio is 451490. (The * adjacent to 617 is not a gear because it is only adjacent to one part number.) Adding up all of the gear ratios produces 467835.

What is the sum of all of the gear ratios in your engine schematic?
"""

from dataclasses import dataclass
import math
from string import digits
from typing import Generator
from numpy import arange, where
import pandas as pd


SYMBOLS = list("!@#$%^&*()_+-=[]{}\\|;:'\"<>,?/")


@dataclass
class Coord:
    x: int
    y: int

    def adjacency(self, size: tuple[int, int]) -> pd.DataFrame:
        size_x, size_y = size
        i, j = self.x, self.y

        def get_slice(i, X):
            return slice(max(0, i - 1), min(i + 2, X))

        row_slice = get_slice(i, size_x)
        col_slice = get_slice(j, size_y)

        df = pd.DataFrame(
            False,
            index=arange(0, size_x),
            columns=arange(0, size_x),
        )
        df.iloc[row_slice, col_slice] = True

        return df

    def get_symbol(self, schematic: pd.DataFrame) -> str:
        return schematic.iloc[self.x, self.y]


@dataclass
class Number:
    row: pd.Series
    y: int
    number: int | None = None

    def __post_init__(self) -> None:
        def peek_around(self, left: bool) -> Generator[str, None, None]:
            inc = -1 if left else 1
            Y = self.row.index.min() if left else self.row.index.max()
            i = self.y + inc if (left and self.y > Y) or (self.y < Y) else None
            if i is None:
                return
            num = self.row[i]

            while num.isdigit():
                yield num

                if i != Y:
                    i += inc
                    num = self.row[i]
                else:
                    self.y_ = i
                    return
            if left:
                self.y_ = i - inc

        def collect_digits(self) -> None:
            num_start = [self.row[self.y]]
            num_list_left = [i for i in peek_around(self, left=True)]
            num_list_left.reverse()
            num_list = (
                num_list_left + num_start + [i for i in peek_around(self, left=False)]
            )
            num = int("".join(num_list))
            self.number = num
            self.y = self.y_
            del self.y_

        collect_digits(self)

    def __eq__(self, other: object, /) -> bool:
        if not isinstance(other, Number):
            return False
        row_match = self.row.name == other.row.name
        y_match = self.y == other.y
        num_match = self.number == other.number
        return row_match and y_match and num_match

    def __hash__(self) -> int:
        return hash((self.row.name, self.y, self.number))


def locate_symbols(schematic: pd.DataFrame) -> list[Coord]:
    symbols = SYMBOLS
    is_sym = schematic.isin(symbols)
    return [Coord(i, j) for i, j in zip(*where(is_sym))]


def locate_digits(schematic: pd.DataFrame) -> pd.DataFrame:
    return schematic.isin(list(digits))


def load_schematic(schematic: str) -> pd.DataFrame:
    lines = schematic.strip().split("\n")
    return pd.DataFrame(map(list, lines))


if __name__ == "__main__":
    from argparse import ArgumentParser, FileType

    parser = ArgumentParser()
    parser.add_argument("-f", type=FileType("r"))
    parser.add_argument("-v", action="store_true")
    parser.add_argument(
        "--test",
        action="store_true",
        help="ignores file input and runs test file `example`",
    )
    args = parser.parse_args()

    if args.test:
        filename = "example1.txt"
        file = open(filename, "r")
    elif args.f:
        file = args.f
    else:
        raise Exception("File or test must be specified")

    raw_schematic = file.read()

    schematic = load_schematic(raw_schematic)
    size = schematic.shape
    is_digit = schematic.isin(list(digits))

    symbols = locate_symbols(schematic)
    sym_where = sum(coord.adjacency(size) for coord in symbols).astype(bool)

    nums = {
        Number(schematic.iloc[row_n], y)
        for row_n, y in zip(*where(sym_where & is_digit))
    }
    total_parts = sum(num.number for num in nums)

    gears = [coord for coord in symbols if coord.get_symbol(schematic) == "*"]
    gear_ratios = []
    for gear in gears:
        nums = {
            Number(schematic.iloc[row_n], y)
            for row_n, y in zip(*where(gear.adjacency(size) & is_digit))
        }
        if len(nums) < 2:
            continue
        gear_ratio = math.prod(num.number for num in nums)
        gear_ratios.append(gear_ratio)
    total_gear_ratios = sum(gear_ratios)

    print(f"The total of the part numbers: {total_parts}")
    if args.test:
        ans = 4361
        matches = "does" if total_parts == ans else "does NOT"
        print(f"This {matches} match the test.")

    print(f"The total of the gear ratios: {total_gear_ratios}")
    if args.test:
        ans_ii = 467835
        matches = "does" if total_gear_ratios == ans_ii else "does NOT"
        print(f"This {matches} match the test.")
