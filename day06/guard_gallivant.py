"""
--- Day 6: Guard Gallivant ---
https://adventofcode.com/2024/day/6

--------------------- Part I ---------------------
Total distinct positions visited by the guard is (4883)
"""


from collections import deque
from typing import Generator, TypeAlias


Coord: TypeAlias = tuple[int, int]
PatrolMap: TypeAlias = tuple[str, ...]

N: Coord = (-1, 0)
E: Coord = (0, 1)
S: Coord = (1, 0)
W: Coord = (0, -1)

def locate_start(grid: PatrolMap) -> Coord | None:
    start = '^'
    for i, line in enumerate(grid):
        if (j:= line.find(start)) > -1:
            return i, j

def move(pos: Coord, heading: Coord) -> Coord:
    x, y = pos
    i, j = heading
    return x + i, y + j

def peek(grid: PatrolMap, pos: Coord) -> str:
    x, y = pos
    return grid[x][y]

def in_bounds(bounds: tuple[int, int, int], pos: Coord) -> bool:
    og, m, n = bounds
    i, j = pos
    if (og <= i < m) and (og <= j < n):
        return True
    else:
        return False

def walk_patrol(grid: PatrolMap) -> Generator[Coord, None, None]:
    bounds = (0, len(grid), len(grid[0]))
    barrier = '#'
    direct = deque((N, E, S, W))
    if (pos:= locate_start(grid)):
        yield pos
    else:
        return
    while pos:
        heading = direct.popleft()
        direct.append(heading)
        while in_bounds(bounds, step:= move(pos, heading)) and (peek(grid, step) != barrier):
            pos = step
            yield pos
        if not in_bounds(bounds, step):
            return


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
    grid = tuple(line for line in file.read().strip().split("\n"))
    distinct_pos = {pos for pos in walk_patrol(grid)}
    total_distict = len(distinct_pos)
    print(f"Total distinct positions visited by the guard is ({total_distict})")

    if args.test:
        ans = 41
        assert total_distict == ans, f"Total distinct position visited did not match expected ({ans})"

