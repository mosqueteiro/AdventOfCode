"""
--- Day 13: Clay Contraption ---

The mathemagics
Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

 I     K     M        J     L     N
94A + 22B = 8400 and 34A + 67B = 5400
                     B = 5400/67 - 34A/67
94A + 22(5400/67 - 34A/67) = 8400
(94 - 22*34/67)A = 8400 - 22(5400/67)
A = (8400 - (22*5400/67)) / (94 - (22*34/67))  | A = (M - (K*N/L)) / (I - (K*J/L))
B = (5400 - 34*A)/67                           | B = (N - J*A)/L

--------------------- Part I ---------------------
The total cost is 20872 tokens
Solved in 0.010396 s

--------------------- PartII ---------------------
The total cost is 92827349540204 tokens
Solved in 0.000899 s
"""


from string import digits
from time import perf_counter
from typing import TypeAlias


Game: TypeAlias = tuple[int, int, int, int, int, int]

def parse_games(input: str) -> list[Game]:
    def game_str_xform(game: str):
        str_xform = ''.join(c for c in game if c in (*digits, "=", "+"))[1:].replace("=", "+")
        return tuple(int(s) for s in str_xform.split("+"))
    raw_games = input.strip().split("\n\n")
    return [game_str_xform(game) for game in raw_games]

def solve_button_presses(game: Game, part2: bool = False) -> tuple[int, int] | None:
    I, J, K, L, M, N = game
    if part2:
        correction = 10000000000000
        M = M + correction
        N = N + correction
    A = (M - (K*N/L)) / (I - (K*J/L))
    B = (N - J*A)/L
    A = round(A,2)
    B = round(B,2)
    if any(x % 1 > 0 for x in (A,B)):
        # if any(round(x,2) % 1 <= 0 for x in (A,B)):
            # breakpoint()
        return
    return int(A), int(B)


if __name__ == "__main__":
    from argparse import ArgumentParser, FileType

    from adventofcode import print_part_divider

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

    print_part_divider("Part I")
    start = perf_counter()
    games = parse_games(file.read())
    valid_games = [valid_game for game in games if (valid_game := solve_button_presses(game))]
    total_cost = sum(3*A + 1*B for A,B in valid_games)
    end = perf_counter()
    print(f"The total cost is {total_cost:d} tokens")
    print(f"Solved in {end-start:.6f} s")

    if args.test:
        ans = 480
        assert total_cost == ans, f"Total cost didn't match expected ({ans})"

    print_part_divider("PartII")
    start = perf_counter()
    valid_games = [valid_game for game in games if (valid_game := solve_button_presses(game, part2=True))]
    total_cost = sum(3*A + 1*B for A,B in valid_games)
    end = perf_counter()
    print(f"The total cost is {total_cost:d} tokens")
    print(f"Solved in {end-start:.6f} s")

    if args.test:
        assert len(valid_games) == 2, "Only 2 games should be valid"

