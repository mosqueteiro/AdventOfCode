"""
--- Day 22: Monkey Market ---
https://adventofcode.com/2024/day/22

--------------------- Part I ---------------------
The sum of the final secrets is (13022553808)

-------------------- Part II ---------------------
The most bananas possible is (1555)
"""

from collections import Counter
from typing import Generator
from numpy import apply_along_axis, array, bitwise_xor, diff, mod, unique
from numpy._typing import ArrayLike, NDArray
from numpy.lib.stride_tricks import sliding_window_view


def mix(secret: ArrayLike, mixer: ArrayLike) -> NDArray:
    return bitwise_xor(secret, mixer)

def prune(secret: ArrayLike) -> NDArray:
    pruner = 16777216
    return mod(secret, pruner)

def secret_squence(secret: ArrayLike) -> Generator[NDArray, None, None]:
    secret = array(secret)
    yield secret

    while True:
        step_1 = prune(mix(secret, secret * 64))
        step_2 = prune(mix(step_1, step_1 // 32))
        step_3 = prune(mix(step_2, step_2 * 2048))
        yield (secret:= step_3)

def price_sequence(sliding_window: NDArray) -> tuple[list[bytes], NDArray]:
    win_end = 3
    to_price = 1
    sequences, idx = unique(sliding_window, axis=0, return_index=True)
    # Note: apply_along_axis didn't work, some rows were getting truncated
    # seq_bytes = apply_along_axis(lambda x: x.tobytes(), 1, sequences)
    seq_bytes = [row.tobytes() for row in sequences]
    # breakpoint()
    return seq_bytes, idx + win_end + to_price


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
        expected = array([[
            15887950,
            16495136,
            527345,
            704524,
            1553684,
            12683156,
            11100544,
            12249484,
            7753432,
            5908254,
        ]]).T
        seq = secret_squence([123])
        assert next(seq) == 123, "Secret Sequence didn't start with first number"
        matching = array([next(seq) for _ in range(10)]) == expected
        assert matching.all(), "Test sequence didn't match expected"
        filename = "example.txt"
        file = open(filename, "r")
    elif args.f:
        file = args.f
    else:
        raise Exception("File or test must be specified")

    print()
    print(" Part I ".center(50, "-"))
    daily_nums = 2000
    initial_secret_nums = array(file.read().strip().split(), dtype=int)
    daily_secrets = array([secret for secret, _ in zip(secret_squence(initial_secret_nums), range(daily_nums + 1))])
    final_secrets = daily_secrets[daily_nums, :]
    secret_sum = final_secrets.sum()
    print(f"The sum of the final secrets is ({secret_sum})")

    if args.test:
        ans = 37327623
        assert secret_sum == ans, f"The sum of final secrets didn't match expected ({ans})"

    print()
    print(" Part II ".center(50, "-"))
    if args.test:
        example_2 = [1, 2, 3, 2024]
        daily_secrets = array([secret for secret, _ in zip(secret_squence(example_2), range(daily_nums + 1))])

    daily_prices = mod(daily_secrets, 10)
    daily_diff = diff(daily_prices, axis=0)
    sequences = Counter()
    win4 = sliding_window_view(daily_diff, 4, axis=0)
    for window in range(win4.shape[1]):
        sequences.update({
            pattern: daily_prices[idx, window]
            for pattern, idx in zip(*price_sequence(win4[:, window, :]))
        })
    pattern_bytes, most_bananas = sequences.most_common(1)[0]
    print(f"The most bananas possible is ({most_bananas})")

    if args.test:
        ans = 23
        assert most_bananas == ans, f"The possible bananas didn't match expected ({ans})"

