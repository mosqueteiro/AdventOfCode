"""
--- Day 11: Plutonian Pebbles ---

--------------------- Part I ---------------------
The arrangement is (233050) stones long after 25 blinks
First approach took 0.095919 s
The arrangement is (233050) stones long after 25 blinks
recursive approach took 0.004665 s

-------------------- Part II ---------------------
The arrangement is (276661131175807) stones long after 75 blinks
75 recursive blinks took 0.156687 s
"""


from functools import cache
from time import perf_counter
from tqdm import tqdm

def stripper_zero(stone: str) -> str:
    reduced = stone.lstrip("0")
    if reduced:
        return reduced
    else:
        return "0"

@cache
def stone_operator(stone: str) -> list[str]:
    match stone:
        case "0":
            return ["1"]
        case rock if len(rock) % 2 == 0:
            return [rock[: (half := len(rock)//2)], stripper_zero(rock[half:])]
        case _:
            return [str(int(stone) * 2024)]

def blink(stones: tuple[str, ...]) -> tuple[str, ...]:
    packed_stones = [stone_operator(stone) for stone in stones]
    return tuple(stone for pack in packed_stones for stone in pack)

@cache
def recur_blink(stone: str, blinks: int) -> int:
    if blinks == 1:
        return len(stone_operator(stone))

    total_len = 0
    for istone in stone_operator(stone):
        total_len += recur_blink(istone, blinks-1)
    return total_len


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
    stones = tuple(file.read().strip().split())
    pluto_pebbles = stones
    start = perf_counter()
    for i in tqdm(range(1, 25+1)):
        pluto_pebbles = blink(pluto_pebbles)
    end = perf_counter()
    print(f"The arrangement is ({len(pluto_pebbles)}) stones long after 25 blinks")
    print(f"First approach took {end-start:.6f} s")
    stone_operator.cache_clear()
    start = perf_counter()
    total_pebbles = sum(recur_blink(stone, 25) for stone in sorted(stones))
    end = perf_counter()
    print(f"The arrangement is ({total_pebbles}) stones long after 25 blinks")
    print(f"recursive approach took {end-start:.6f} s")

    if args.test:
        ans = 55312
        # assert len(pluto_pebbles) == ans, f"The number of stones didn't match expected ({ans})"
        assert total_pebbles == ans, f"The number of stones didn't match expected ({ans})"

    print()
    print(" Part II ".center(50, "-"))
    # for i in tqdm(range(25, 75+1)):
    #     pluto_pebbles = blink(pluto_pebbles)
    # print(f"The arangement is ({len(pluto_pebbles)}) stones long after 75 blinks")
    # stone_operator.cache_clear()
    start = perf_counter()
    total_pebbles = sum(recur_blink(stone, 75) for stone in sorted(stones))
    end = perf_counter()
    print(f"The arrangement is ({total_pebbles}) stones long after 75 blinks")
    print(f"75 recursive blinks took {end-start:.6f} s")

