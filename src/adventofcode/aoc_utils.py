"""
aoc_utils.py

File for storing python utilities generic and useful across the days.
"""

from argparse import ArgumentParser, FileType


def arg_parser_init() -> ArgumentParser:
    """Creates the default arguments for Advent of Code challenges

    Arguments created are:
    -f filename     file input to run code with, opens a file buffer with this file
    -v              verbose output, use this as needed for debugging
    --test          use this to indicate running a test file instead of input file

    Returns
    -------
    ArgumentParser:
        The parser with default arguments added to it. Run `parser.parse_args()`
        to return a parsed dict
    """
    parser = ArgumentParser()
    parser.add_argument("-f", type=FileType("r"), help="file input to run the code with")
    parser.add_argument("-v", action="store_true", help="verbose")
    parser.add_argument(
        "--test",
        action="store_true",
        help="ignores file input and runs test file `example`",
    )
    return parser


def print_part_divider(part: str) -> None:
    print()
    print(f" {part} ".center(50, "-"))

