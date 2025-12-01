"""
Entry point for aoc_utils CLI.
"""

import argparse
import sys
from .puzzle import get_puzzle_input
from .setup import main as setup_main


def puzzle_input_cmd(args):
    """Handle puzzle_input subcommand."""
    try:
        input_path = get_puzzle_input(args.year, args.day, args.overwrite)
        print(f"Input file: {input_path}")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def setup_cmd(args):
    """Handle setup subcommand."""
    setup_main()


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        prog="aoc_utils",
        description="Advent of Code utilities"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # puzzle_input subcommand
    puzzle_parser = subparsers.add_parser(
        "puzzle_input",
        help="Download puzzle input for a specific year and day"
    )
    puzzle_parser.add_argument("--year", type=int, help="AoC year (e.g., 2024, 2025)")
    puzzle_parser.add_argument("--day", type=int, help="Day of the month (1-25)")
    puzzle_parser.add_argument(
        "--overwrite", 
        action="store_true", 
        help="Re-download even if file already exists"
    )
    puzzle_parser.set_defaults(func=puzzle_input_cmd)

    # setup subcommand
    setup_parser = subparsers.add_parser(
        "setup",
        help="Set up AoC session token"
    )
    setup_parser.set_defaults(func=setup_cmd)

    # Parse arguments
    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        sys.exit(1)
    elif args.command == 'puzzle_input' and (
        args.year is None or args.day is None
        ):
        puzzle_parser.print_help()
        sys.exit(1)

    # Execute the appropriate command
    args.func(args)


if __name__ == "__main__":
    main()
