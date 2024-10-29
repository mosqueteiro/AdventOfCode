"""
cube_conundrum.py

2024-10-29
Nathan James

Playing a game with an Elf on the way to **Snow Island**. There are red, blue,
and greed cubes in a bag. Elf will pull out handfuls and show you how many of
each they pulled out. Each game will be a number of sets, the example shows 3
sets per game.

Elf wants to know which games are possible or impossible given the bag only
contained 12 red cubes, 13 green cubes, and 14 blue cubes. In the `example1`
games 1, 2, and 5 are possible and games 3 and 4 are impossible. Determine the
games which are possible and report the sum of their IDs.
"""

from dataclasses import dataclass
from enum import IntEnum
from typing import Tuple


class MaxPos(IntEnum):
    RED = 12
    GREEN = 13
    BLUE = 14


@dataclass
class CubeSet:
    red: int = 0
    green: int = 0
    blue: int = 0

    def possible(self) -> bool:
        max_pos = MaxPos
        if (
            self.red > max_pos.RED
            or self.green > max_pos.GREEN
            or self.blue > max_pos.BLUE
        ):
            return False
        return True


def parse_line(line: str) -> dict[int, list[CubeSet]]:
    game_str, sets = line.split(": ")
    game_id = int(game_str.split(" ")[1])
    # if game_id == 5:
    #     breakpoint()
    return {game_id: parse_sets(sets)}


# def parse_sets(sets: str) -> list[CubeSet]:
#     cor_parse = lambda cor: cor.split(" ")
#     set_to_dict = lambda s: dict(map(cor_parse, s.split(", ")))
#     inv_dict = lambda d: {v: k for k, v in d.items()}

#     set_list = sets.split("; ")
#     set_list_post = map(lambda s: inv_dict(set_to_dict(s)), set_list)
#     return [CubeSet(**d) for d in set_list_post]


def parse_sets(sets: str) -> list[CubeSet]:
    def cor_parse(cor_str: str) -> Tuple[str, int]:
        n, cor = cor_str.split(" ")
        return cor, int(n)

    def set_to_dict(set_str: str) -> dict[str, int]:
        return dict(map(cor_parse, set_str.split(", ")))

    # def inv_dict(d: dict) -> dict:
    #     return {v: k for k, v in d.items()}

    set_list = sets.strip().split("; ")
    # set_list_post = map(lambda s: inv_dict(set_to_dict(s)), set_list)
    set_list_post = map(lambda s: set_to_dict(s), set_list)
    return [CubeSet(**d) for d in set_list_post]


def check_game(game: dict[int, list[CubeSet]]) -> Tuple[bool, int]:
    game_n, sets = game.popitem()
    possible = all(map(lambda cs: cs.possible(), sets))
    return possible, game_n


def min_cubes(game: dict[int, list[CubeSet]]) -> dict[int, CubeSet]:
    game_id, sets = game.popitem()
    min_set = CubeSet(
        **{
            "red": max(sets, key=lambda cs: cs.red).red,
            "blue": max(sets, key=lambda cs: cs.blue).blue,
            "green": max(sets, key=lambda cs: cs.green).green,
        }
    )
    return {game_id: min_set}


def cube_power(game_min: dict[int, CubeSet]) -> dict[int, int]:
    game_id, min_set = game_min.popitem()
    return {game_id: (min_set.red * min_set.blue * min_set.green)}


if __name__ == "__main__":
    from argparse import ArgumentParser, FileType

    parser = ArgumentParser()
    parser.add_argument("-f", type=FileType("r"), help="Game file to parse")
    parser.add_argument("-v", action="store_true")
    args = parser.parse_args()

    lines = args.f.readlines()
    processed_lines = map(parse_line, lines)
    games_checked = map(check_game, processed_lines)
    # print(*games_checked)
    final = sum(map(lambda tup: tup[1] if tup[0] else 0, games_checked))
    print(f"Sum of possible games: {final}")

    print(f"\n\nAnalyzing all {len(lines)} games\n")
    processed_lines = map(parse_line, lines)
    if args.v:
        processed_lines = [*processed_lines]
        print(f"Games:\n{processed_lines}")
    min_cube_game = map(min_cubes, processed_lines)
    if args.v:
        min_cube_game = [*min_cube_game]
        print(f"Min cub games:\n{min_cube_game}")
    game_power = map(cube_power, min_cube_game)
    if args.v:
        game_power = [*game_power]
        print(f"Power per game:\n{game_power}")
    total_power = sum(power.popitem()[1] for power in game_power)
    print(f"Total power is: {total_power}")
