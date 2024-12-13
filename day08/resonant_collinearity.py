"""
--- Day 8: Resonant Collinearity ---

--------------------- Part I ---------------------
Unique antinodes: 390

-------------------- Part II ---------------------
Unique antinodes with harmonics: 1246
"""


from itertools import combinations
from typing import TypeAlias
from numpy import array, where
import pandas as pd


Coord: TypeAlias = tuple[int, int]

def parse_map(input: str) -> tuple[pd.DataFrame, set[str]]:
    antenna_freq = {*input}
    antenna_freq.remove("\n")
    antenna_freq.remove(".")

    mapa = pd.DataFrame(map(tuple, input.strip().split("\n")))
    return mapa, antenna_freq

def locate_antenna(mapa: pd.DataFrame, a_freq: str) -> list[Coord]:
    m, n = where(mapa.isin([a_freq]))
    return list(zip(m.tolist(), n.tolist()))

def calc_antinodes(antenna_pair: tuple[Coord, Coord], extended: bool = False) -> tuple[Coord, Coord] | list[Coord]:
    a1, a2 = map(array, antenna_pair)
    slope = a2 - a1
    if not extended:
        return tuple(a1 - slope), tuple(a2 + slope)
    else:
        forward = [tuple(a2 + k * slope) for k in range(1, 45)]
        backward = [tuple(a1 - k * slope) for k in range(1, 45)]
        return forward + backward + [*antenna_pair]

def inbounds(pos: Coord, map_size: tuple[int, int]) -> bool:
    return all(0 <= x < X for x, X in zip(pos, map_size))


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
    mapa, antenna_freq = parse_map(file.read())
    map_size = mapa.shape
    antenna_map = {freq: locate_antenna(mapa, freq) for freq in antenna_freq}
    antinodes = set()
    for freq, antennas in antenna_map.items():
        collinear_antennas = combinations(antennas, 2)
        _antinodes = [calc_antinodes(antenna_pair) for antenna_pair in collinear_antennas]
        antinodes.update(antinode for pair in _antinodes for antinode in pair if inbounds(antinode, map_size))

    total_antinodes = len(antinodes)
    print(f"Unique antinodes: {total_antinodes}")

    if args.test:
        ans = 14
        assert total_antinodes == ans, f"Unique antinodes didn't match expected ({ans})"

    print()
    print(" Part II ".center(50, "-"))
    antinodes = set()
    for freq, antennas in antenna_map.items():
        collinear_antennas = combinations(antennas, 2)
        _antinodes = [calc_antinodes(antenna_pair, extended=True) for antenna_pair in collinear_antennas]
        antinodes.update(antinode for pair in _antinodes for antinode in pair if inbounds(antinode, map_size))

    total_antinodes = len(antinodes)
    print(f"Unique antinodes with harmonics: {total_antinodes}")

    if args.test:
        ans = 34
        assert total_antinodes == ans, f"Unique antinodes with harmonics didn't match expected ({ans})"

