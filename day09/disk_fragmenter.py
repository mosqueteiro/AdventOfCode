"""
--- Day 9: Disk Fragmenter.py ---
https://adventofcode.com/2024/day/9

--------------------- Part I ---------------------
The filesystem checksum is (6299243228569)
"""


from typing import Generator


def decompress(disk_map_c: list[int]) -> list[str]:
    decompressed = []
    i = 0
    file = True
    for block in disk_map_c:
        decompressed += [str(i)] * block if file else ["."] * block
        i += 1 if not file else 0
        file = not file

    return decompressed

def mem_walk(disk_map: list[str], find_free: bool = True) -> Generator[tuple[int, str], None, None]:
    I = len(disk_map) - 1
    for i, val in enumerate(disk_map):
        match val:
            case "." if find_free:
                yield i, val
            case d if not find_free and d.isdigit():
                yield I - i, val

def is_compacted(disk_map: list[str]) -> bool:
    idx_dot = disk_map.index(".")
    return all(char == "." for char in disk_map[idx_dot:])

def organize_freespace(disk_map: list[str]) -> list[str]:
    disk_map_local = disk_map.copy()

    freespace = mem_walk(disk_map_local, find_free=True)
    file_blocks = mem_walk(disk_map[-1::-1], find_free=False)
    for i, dot in freespace:
        if is_compacted(disk_map_local):
            break
        j, block = next(file_blocks)
        disk_map_local[i] = block
        disk_map_local[j] = dot

    return disk_map_local


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
    disk_map_c = list(map(int, file.read().strip()))
    disk_map = decompress(disk_map_c)
    organized_disk = organize_freespace(disk_map)
    checksum = sum(i * int(block) for i, block in enumerate(organized_disk) if block.isdigit())
    print(f"The filesystem checksum is ({checksum})")

    if args.test:
        ans = 1928
        assert checksum == ans, f"The checksum didn't match the expected ({ans})"

