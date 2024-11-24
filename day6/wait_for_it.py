"""
--- Day 6: Wait For It ---

The ferry quickly brings you across Island Island. After asking around, you discover that there is indeed normally a large pile of sand somewhere near here, but you don't see anything besides lots of water and the small island where the ferry has docked.

As you try to figure out what to do next, you notice a poster on a wall near the ferry dock. "Boat races! Open to the public! Grand prize is an all-expenses-paid trip to Desert Island!" That must be where the sand comes from! Best of all, the boat races are starting in just a few minutes.

You manage to sign up as a competitor in the boat races just in time. The organizer explains that it's not really a traditional race - instead, you will get a fixed amount of time during which your boat has to travel as far as it can, and you win if your boat goes the farthest.

As part of signing up, you get a sheet of paper (your puzzle input) that lists the time allowed for each race and also the best distance ever recorded in that race. To guarantee you win the grand prize, you need to make sure you go farther in each race than the current record holder.

The organizer brings you over to the area where the boat races are held. The boats are much smaller than you expected - they're actually toy boats, each with a big button on top. Holding down the button charges the boat, and releasing the button allows the boat to move. Boats move faster if their button was held longer, but time spent holding the button counts against the total race time. You can only hold the button at the start of the race, and boats don't move until the button is released.

For example:

```
Time:      7  15   30
Distance:  9  40  200
```

This document describes three races:

    The first race lasts 7 milliseconds. The record distance in this race is 9 millimeters.
    The second race lasts 15 milliseconds. The record distance in this race is 40 millimeters.
    The third race lasts 30 milliseconds. The record distance in this race is 200 millimeters.

Your toy boat has a starting speed of zero millimeters per millisecond. For each whole millisecond you spend at the beginning of the race holding down the button, the boat's speed increases by one millimeter per millisecond.

So, because the first race lasts 7 milliseconds, you only have a few options:

    Don't hold the button at all (that is, hold it for 0 milliseconds) at the start of the race. The boat won't move; it will have traveled 0 millimeters by the end of the race.
    Hold the button for 1 millisecond at the start of the race. Then, the boat will travel at a speed of 1 millimeter per millisecond for 6 milliseconds, reaching a total distance traveled of 6 millimeters.
    Hold the button for 2 milliseconds, giving the boat a speed of 2 millimeters per millisecond. It will then get 5 milliseconds to move, reaching a total distance of 10 millimeters.
    Hold the button for 3 milliseconds. After its remaining 4 milliseconds of travel time, the boat will have gone 12 millimeters.
    Hold the button for 4 milliseconds. After its remaining 3 milliseconds of travel time, the boat will have gone 12 millimeters.
    Hold the button for 5 milliseconds, causing the boat to travel a total of 10 millimeters.
    Hold the button for 6 milliseconds, causing the boat to travel a total of 6 millimeters.
    Hold the button for 7 milliseconds. That's the entire duration of the race. You never let go of the button. The boat can't move until you let go of the button. Please make sure you let go of the button so the boat gets to move. 0 millimeters.

Since the current record for this race is 9 millimeters, there are actually 4 different ways you could win: you could hold the button for 2, 3, 4, or 5 milliseconds at the start of the race.

In the second race, you could hold the button for at least 4 milliseconds and at most 11 milliseconds and beat the record, a total of 8 different ways to win.

In the third race, you could hold the button for at least 11 milliseconds and no more than 19 milliseconds and still beat the record, a total of 9 ways you could win.

To see how much margin of error you have, determine the number of ways you can beat the record in each race; in this example, if you multiply these values together, you get 288 (4 * 8 * 9).

Determine the number of ways you could beat the record in each race. What do you get if you multiply these numbers together?


Notes:
x: button hold time [ms]
T: total race time [ms]
D: record distance for race [mm]
v(x): velocity f(x) [mm/ms] := x
d(x,T): distance traveled f(x,T) where x <= T := v(x) * (T - x) = -x^2 + Tx

Then if we want to find where d(x,T) = D we can use the quadratic formula
x = -b +/- sqrt(b^2 - 4ac)/2a

by first setting the equation to zero
d(x,T) - D = 0
-x^2 + Tx - D = 0
with
a := -1
b := T
c := -D

--- Part Two ---

As the race is about to start, you realize the piece of paper with race times and record distances you got earlier actually just has very bad kerning. There's really only one race - ignore the spaces between the numbers on each line.

So, the example from before:

Time:      7  15   30
Distance:  9  40  200

...now instead means this:

Time:      71530
Distance:  940200

Now, you have to figure out how many ways there are to win this single race. In this example, the race lasts for 71530 milliseconds and the record distance you need to beat is 940200 millimeters. You could hold the button anywhere from 14 to 71516 milliseconds and beat the record, a total of 71503 ways!

How many ways can you beat the record in this one much longer race?
"""


from typing import TypeAlias

import pandas as pd
import numpy as np


Roots: TypeAlias = tuple[float, float]
WinRangeEnds: TypeAlias = tuple[int, int]

def parse_line(line: str) -> tuple[str, list[int]]:
    key, values_str = tuple(splt.strip() for splt in line.strip().split(":"))
    value_list_int = list(map(int, values_str.split()))
    return (key, value_list_int)

def parse_line_better_kerning(line: str) -> tuple[str, int]:
    key, values_str = tuple(splt.strip() for splt in line.strip().split(":"))
    value_int = int(values_str.replace(" ", ""))
    return (key, value_int)

def quadratic_formula(t_f: int, d_f: int) -> Roots:
    a = -1; b = t_f; c = - d_f
    left = - b / (2*a)
    right = np.sqrt(b**2 - 4 * a * c) / (2*a)
    return left - right, left + right

def win_range(t_f: int, d_f: int) -> WinRangeEnds:
    a = -1; b = t_f; c = - d_f
    hi_root, lo_root =  np.roots([a,b,c])
    win_rng_float = (np.ceil(hi_root), np.floor(lo_root) + 1)
    win_rng_int = tuple(map(int, win_rng_float))
    assert len(win_rng_int) == 2, "Error, too many roots"
    return win_rng_int

def sub_map(win_rng_int: WinRangeEnds) -> int:
    hi_, lo_ = win_rng_int
    return hi_ - lo_


if __name__ == "__main__":
    from argparse import ArgumentParser, FileType

    parser = ArgumentParser()
    parser.add_argument("-f", type=FileType("r"))
    parser.add_argument("-v", action="store_true")
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

    print(f"\n--- Part I ---")
    races = pd.DataFrame(dict(map(parse_line, file.readlines())))
    races["win_range"] = races.apply(lambda row: win_range(row["Time"], row["Distance"]), axis="columns")
    races["n_wins"] = races["win_range"].map(sub_map)

    record_prod = races["n_wins"].prod()
    print(f"Product of number of possible wins: {record_prod}")

    if args.test:
        ans = 288
        assert record_prod == ans, f"The product of wins reported ({record_prod}) does not match the expected product ({ans})"

    print(f"\n--- Part II: bad kerning ---")
    file.seek(0)
    races_ii = dict(map(parse_line_better_kerning, file.readlines()))
    races_ii_win_range = win_range(races_ii["Time"], races_ii["Distance"])
    races_ii_n_wins = sub_map(races_ii_win_range)

    print(f"Product of number of possible wins: {races_ii_n_wins}")

    if args.test:
        ans_ii = 71503
        assert races_ii_n_wins == ans_ii, f"The product of wins reported ({races_ii_n_wins}) does not match the expected product ({ans_ii})"

