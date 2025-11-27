"""
--- Day 19: Linen Layout ---
https://adventofcode.com/2024/day/19


"""


from tqdm import tqdm


def parse_design_space(input: str) -> tuple[tuple[str, ...], list[str]]:
    raw_towels, raw_designs = input.strip().split("\n\n")
    towels = tuple(raw_towels.strip().split(", "))
    designs = raw_designs.strip().split()
    return towels, designs

def design_plans(design: str, towels: tuple[str, ...]) -> dict | bool:
    plans = {'design': design, 'towels': {}}
    if design == "":
        return True
    towel_fit = [towel for towel in towels if design.startswith(towel)]
    if not towel_fit:
        return False

    for towel in towel_fit:
        match (step:= design_plans(design[len(towel):], towels)):
            case True:
                return True
            case dict():
                plans['towels'][towel] = step
        # if (step:= design_plans(design[len(towel):], towels)):
        #     plans['towels'][towel] = step

    if plans['towels']:
        return plans
    else:
        return False


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
    _towels, designs = parse_design_space(file.read())
    towels = tuple(sorted(_towels, key=lambda x: len(x) * -1))
    possible_designs = tuple(patterns for design in tqdm(designs) if (patterns:= design_plans(design, towels)))
    total_possible = len(possible_designs)
    print(f"Total possible design patterns are ({total_possible})")

    if args.test:
        ans = 6
        assert total_possible == ans, f"Possible design patterns did not match expected ({ans})"

