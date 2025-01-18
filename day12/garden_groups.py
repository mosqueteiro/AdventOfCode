"""
--- Day 12: Garden Groups

--------------------- Part I ---------------------
The total price of fencing all regions is (1485656)
Processing time: 1.222576 s

-------------------- Part II ---------------------
The total price of fencing all regions is (899196)
Processing time: 1.405213 s
"""


from time import perf_counter
from typing import TypeAlias

from numpy import array, ndarray, where


GardenGrid: TypeAlias = ndarray
Point: TypeAlias = tuple[int, int]

DPAD = (
    (-1, 0),
    (0, 1),
    (1, 0),
    (0, -1)
)

def survey_plot(plot: Point, garden: GardenGrid) -> tuple[set[Point], list[Point]]:
    max_bound = garden.shape
    fences = set()
    neighbors = []
    for dir in DPAD:
        adjacent = tuple(a+b for a,b in zip(plot, dir))
        if not all(0 <= i < lim for i, lim in zip(adjacent, max_bound)):
            fences.add(dir)
        elif garden[plot] != garden[adjacent]:
            fences.add(dir)
        else:
            neighbors.append(adjacent)
    return fences, neighbors

def detect_sides(perimeter: dict[Point, set]) -> int:
    def detect_axis_sides(perimeter):
        axis_sorted = sorted(perimeter)
        prev_point = (None, None)
        prev_fences = set()
        side_reduction = 0
        for point in axis_sorted:
            fences = perimeter[point]
            if (point[0] == prev_point[0]) and (point[1]-1 == prev_point[1]):
                side_reduction += len(fences.intersection(prev_fences))
            prev_point = point
            prev_fences = fences
        return side_reduction
    # return fence reduction for contiguous sides
    # side len - 1, for all sides
    # x_sort = sorted(perimeter)
    perimeter_T = {(k[1], k[0]): v for k,v in perimeter.items()}
    # y_sort = sorted(perimeter_T)
    # perimeter_T.update(perimeter)
    # return fence_reduction
    return sum(detect_axis_sides(axis) for axis in (perimeter, perimeter_T))

def survey_region(plot: Point, garden: GardenGrid, discount: bool = False) -> int:
    fences = 0
    plots = set()
    perimeter = dict()
    pending = {plot}
    while pending:
        _plot = pending.pop()
        add_fences, add_plots = survey_plot(_plot, garden)
        if add_fences:
            fences += len(add_fences)
            perimeter[_plot] = add_fences
        plots.add(_plot)
        pending.update(add_plots)
        pending -= plots

    garden[tuple(zip(*plots))] = ''
    if discount:
        fences -= detect_sides(perimeter)
    return fences * len(plots)

def calculate_price(garden: GardenGrid, discount: bool = False) -> int:
    total_price = 0
    while (unseen := tuple(zip(*where(garden != '')))):
        plot = unseen[0]
        total_price += survey_region(plot, garden, discount)
    return total_price


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
    garden = array(tuple(tuple(line.strip()) for line in file.readlines()))
    start = perf_counter()
    total_price = calculate_price(garden.copy())
    finish = perf_counter()
    print(f"The total price of fencing all regions is ({total_price})")
    print(f"Processing time: {finish-start:.6f} s")

    if args.test:
        ex1 = array([
        list("AAAA"),
        list("BBCD"),
        list("BBCC"), 
        list("EEEC"),
        ])
        tp1 = calculate_price(ex1.copy())
        ans1 = 140
        assert tp1 == ans1, f"Example 1 didn't match expected ({ans1})"
        ex2 = array([
            list("OOOOO"),
            list("OXOXO"),
            list("OOOOO"),
            list("OXOXO"),
            list("OOOOO"),
        ])
        tp2 = calculate_price(ex2.copy())
        ans2 = 772
        assert tp2 == ans2, f"Example 2 didn't match expected ({ans2})"
        ans = 1930
        assert total_price == ans, f"Total price of fencing didn't match expected ({ans})"

    print()
    print(" Part II ".center(50, "-"))
    start = perf_counter()
    total_price = calculate_price(garden, discount=True)
    finish = perf_counter()
    print(f"The total price of fencing all regions is ({total_price})")
    print(f"Processing time: {finish-start:.6f} s")

    if args.test:
        tp1 = calculate_price(ex1, discount=True)
        ans1 = 80
        assert tp1 == ans1, f"Example 1 didn't match expected ({ans1})"
        tp2 = calculate_price(ex2, discount=True)
        ans2 = 436
        assert tp2 == ans2, f"Example 2 didn't match expected ({ans2})"
        ans = 1206
        assert total_price == ans, f"Total price of fencing didn't match expected ({ans})"

