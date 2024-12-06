"""
--- Day 4: Ceres Search ---
https://adventofcode.com/2024/day/4

--------------------- Part I ---------------------
Total XMAS is (2514)

-------------------- Part II ---------------------
Total X-MAS is (1888)
"""


from typing import Generator


def vertical_traverse(text_lines: tuple[str, ...]) -> Generator[str, None, None]:
    M, N = len(text_lines), len(text_lines[0])
    for j in range(N):
        v_line = "".join(text_lines[i][j] for i in range(M))
        yield v_line

def diagonal_traverse(text_lines: tuple[str, ...], positive: bool = True) -> Generator[str, None, None]:
    M, N = len(text_lines), len(text_lines[0])
    if positive:
        end_r = -1
        step = -1
        start_desc = N - 1
    else:
        end_r = N
        step = 1
        start_desc = 0

    for n in range(N):
        diag_line = "".join(text_lines[i][j] for i, j in zip(range(M), range(n, end_r, step)))
        # diag_line = "".join(text_lines[i][j] for i, j in zip(range(M), range(n, N, 1)))
        yield diag_line
    for m in range(1, M):
        diag_line = "".join(text_lines[i][j] for i, j in zip(range(m, M), range(start_desc, end_r, step)))
        yield diag_line


def count_line(line: str, search: str) -> int:
    hcraes = search[::-1]
    return line.count(search) + line.count(hcraes)

def crossword_count(text_lines: tuple[str, ...], search: str) -> int:
    sum_M = sum(count_line(line, search) for line in text_lines)
    sum_N = sum(count_line(line, search) for line in vertical_traverse(text_lines))
    return sum_M + sum_N

def is_x_mas(text_line: tuple[str, ...], pos: tuple[int, int]) -> bool:
    pos_dir = (-1, 1)
    neg_dir = (-1, -1)

    pos_diag = tuple(x+y for x, y in zip(pos, pos_dir)), pos, tuple(x-y for x, y in zip(pos, pos_dir))
    pos_str = "".join(text_line[i][j] for i, j in pos_diag)
    if not any((pos_str.count("MAS"), pos_str.count("SAM"))):
        return False
    neg_diag = tuple(x+y for x, y in zip(pos, neg_dir)), pos, tuple(x-y for x, y in zip(pos, neg_dir))
    neg_str = "".join(text_line[i][j] for i, j in neg_diag)
    if not any((neg_str.count("MAS"), neg_str.count("SAM"))):
        return False
    else:
        return True


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
    search = "XMAS"
    crossword = tuple(file.readlines())
    horizontal = sum(count_line(line, search) for line in crossword)
    vertical = sum(count_line(line, search) for line in vertical_traverse(crossword))
    pos_diag = sum(count_line(line, search) for line in diagonal_traverse(crossword, positive=True))
    neg_diag = sum(count_line(line, search) for line in diagonal_traverse(crossword, positive=False))
    total = horizontal + vertical + pos_diag + neg_diag
    print(f"Total XMAS is ({total})")

    if args.test:
        ans = 18
        assert total == ans, f"The total found did not match expected ({ans})"

    print()
    print(" Part II ".center(50, "-"))
    total_x_mas = 0
    for i, line in enumerate(crossword[1:-1], 1):
        total_x_mas += sum(is_x_mas(crossword, (i,j)) for j, char in enumerate(line) if char == "A")
    print(f"Total X-MAS is ({total_x_mas})")

    if args.test:
        ans = 9 
        assert total_x_mas == ans, f"The total X-MAS found did not match expected ({ans})"

