"""
--- Day 10: Hoof it
https://adventofcode.com/2024/day/10

--------------------- Part I ---------------------
Total trails for trailheads is (574)

-------------------- Part II ---------------------
Total unique trails are (1238)
"""


from collections import Counter, defaultdict
from typing import TypeAlias
import numpy as np
from numpy.typing import NDArray


Coord: TypeAlias = tuple[int, int]

DIRECTIONS: tuple[Coord, Coord, Coord, Coord] = (
    NORTH:= (-1, 0),
    SOUTH:= (1, 0),
    EAST:= (0, 1),
    WEST:= (0, -1),
)

def locate_border_trailheads(topo: NDArray) -> set[Coord]:
    M, N = topo.shape
    trailheads = set(point for point in zip(*np.where(topo == 0)) if (point[0] in (0, M-1)) or (point[1] in (0, N-1)))
    return trailheads

def valid_path(move: Coord, pos: Coord, topo: NDArray) -> bool:
    M, N = topo.shape
    n_pos = tuple(a + b for a, b in zip(pos, move))

    if not (0 <= n_pos[0] < M) or not (0 <= n_pos[1] < N):
        return False

    if topo[n_pos] == topo[pos] + 1:
        return True
    else:
        return False

def locate_trails(trailhead: Coord, topo: NDArray) -> dict[int, Counter[Coord]]:
    trails = defaultdict(Counter)
    trails[0].update([trailhead])
    for i in range(1,9+1):
        if not (last_paths:= trails[i-1]):
            return trails
        for path, n_tread in last_paths.items():
            trails[i].update({
                tuple(a+b for a,b in zip(path, heading)): n_tread for heading in DIRECTIONS if valid_path(heading, path, topo)
            })
    return trails


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
    topo = np.array(tuple(tuple(map(int,line.strip())) for line in file.readlines()))
    trailheads = set(zip(*np.where(topo == 0)))
    # trailheads = locate_border_trailheads(topo)
    all_trails = tuple(locate_trails(trailhead, topo) for trailhead in trailheads)
    total_trails = sum(len(trails[9]) for trails in all_trails) # sum the numbers of trails for each trailhead
    print(f"Total trails for trailheads is ({total_trails})")

    if args.test:
        ans = 36
        assert total_trails == ans, f"Total trails didn't match expected ({ans})"

    print()
    print(" Part II ".center(50, "-"))
    total_unique = sum(trailhead[9].total() for trailhead in all_trails)
    print(f"Total unique trails are ({total_unique})")

    if args.test:
        ans = 81
        assert total_unique == ans, f"Total unique trails didn't match expected ({ans})"

