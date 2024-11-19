"""
fertilizer.py
2024-11-11
--- Day 5: If You Give A Seed A Fertilizer ---

You take the boat and find the gardener right where you were told he would be: managing a giant "garden" that looks more to you like a farm.

"A water source? Island Island is the water source!" You point out that Snow Island isn't receiving any water.

"Oh, we had to stop the water because we ran out of sand to filter it with! Can't make snow with dirty water. Don't worry, I'm sure we'll get more sand soon; we only turned off the water a few days... weeks... oh no." His face sinks into a look of horrified realization.

"I've been so busy making sure everyone here has food that I completely forgot to check why we stopped getting more sand! There's a ferry leaving soon that is headed over in that direction - it's much faster than your boat. Could you please go check it out?"

You barely have time to agree to this request when he brings up another. "While you wait for the ferry, maybe you can help us with our food production problem. The latest Island Island Almanac just arrived and we're having trouble making sense of it."

The almanac (your puzzle input) lists all of the seeds that need to be planted. It also lists what type of soil to use with each kind of seed, what type of fertilizer to use with each kind of soil, what type of water to use with each kind of fertilizer, and so on. Every type of seed, soil, fertilizer and so on is identified with a number, but numbers are reused by each category - that is, soil 123 and fertilizer 123 aren't necessarily related to each other.

For example:
```
seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4
```

The almanac starts by listing which seeds need to be planted: seeds 79, 14, 55, and 13.

The rest of the almanac contains a list of maps which describe how to convert numbers from a source category into numbers in a destination category. That is, the section that starts with seed-to-soil map: describes how to convert a seed number (the source) to a soil number (the destination). This lets the gardener and his team know which soil to use with which seeds, which water to use with which fertilizer, and so on.

Rather than list every source number and its corresponding destination number one by one, the maps describe entire ranges of numbers that can be converted. Each line within a map contains three numbers: the destination range start, the source range start, and the range length.

Consider again the example seed-to-soil map:
```
50 98 2
52 50 48
```

The first line has a destination range start of 50, a source range start of 98, and a range length of 2. This line means that the source range starts at 98 and contains two values: 98 and 99. The destination range is the same length, but it starts at 50, so its two values are 50 and 51. With this information, you know that seed number 98 corresponds to soil number 50 and that seed number 99 corresponds to soil number 51.

The second line means that the source range starts at 50 and contains 48 values: 50, 51, ..., 96, 97. This corresponds to a destination range starting at 52 and also containing 48 values: 52, 53, ..., 98, 99. So, seed number 53 corresponds to soil number 55.

Any source numbers that aren't mapped correspond to the same destination number. So, seed number 10 corresponds to soil number 10.

So, the entire list of seed numbers and their corresponding soil numbers looks like this:

```
seed  soil
0     0
1     1
...   ...
48    48
49    49
50    52
51    53
...   ...
96    98
97    99
98    50
99    51
```

With this map, you can look up the soil number required for each initial seed number:

    Seed number 79 corresponds to soil number 81.
    Seed number 14 corresponds to soil number 14.
    Seed number 55 corresponds to soil number 57.
    Seed number 13 corresponds to soil number 13.

The gardener and his team want to get started as soon as possible, so they'd like to know the closest location that needs a seed. Using these maps, find the lowest location number that corresponds to any of the initial seeds. To do this, you'll need to convert each seed number through other categories until you can find its corresponding location number. In this example, the corresponding types are:

    Seed 79, soil 81, fertilizer 81, water 81, light 74, temperature 78, humidity 78, location 82.
    Seed 14, soil 14, fertilizer 53, water 49, light 42, temperature 42, humidity 43, location 43.
    Seed 55, soil 57, fertilizer 57, water 53, light 46, temperature 82, humidity 82, location 86.
    Seed 13, soil 13, fertilizer 52, water 41, light 34, temperature 34, humidity 35, location 35.

So, the lowest location number in this example is 35.

What is the lowest location number that corresponds to any of the initial seed numbers?
"""

from functools import partial
from typing import Generator

import numpy as np
import pandas as pd


def parse_almanac(raw_almanac: str) -> list[tuple[str, list[tuple[int, int, int]]]]:
    def parse_num_array(num_string):
        cleaned = num_string.strip()
        split = [tuple(map(int, i.split())) for i in cleaned.split("\n")]
        return split

    raw_split = raw_almanac.split("\n\n")
    name_strs = [step.split(":") for step in raw_split]
    return [(s[0].strip("map").strip(), parse_num_array(s[1])) for s in name_strs]

def map_num(num: int, spec_maps: list[tuple[int,int,int]]) -> int:
    for spec in spec_maps:
        dst_start, src_start, rng = spec
        if num >= src_start and num < src_start + rng:
            idx = num - src_start
            return dst_start + idx

    return num

def map_step(src: tuple[int,...], step_maps: list[tuple[int,int,int]]) -> tuple[int,...]:
    map_num_step = partial(map_num, spec_maps=step_maps)
    return tuple(dst for dst in map(map_num_step, src))

def mapped_steps(steps: list[tuple[str, list[tuple[int, ...]]]]) -> Generator[tuple[str, tuple[int, ...]], None, None]:
    steps_it = iter(steps)
    step_name, src = next(steps_it)
    # src = src[0]  # seeds for part I
    src = seed_ranges(src[0])  # seeds for part II
    yield step_name, src

    for step_name, maps in steps_it:
        src = map_step(src, maps)
        yield step_name, src


def elf_range(rng_pair: tuple[int,int]) -> tuple[int, int]:
    start, additional = rng_pair
    return (start, start + additional)

def elf_pipe(elf_map: tuple[int,int,int]) -> tuple[tuple[int, int], ...]:
    dst, src, addit = elf_map
    return (src, src + addit), (dst, dst + addit)

def process_pipe(elf_range: tuple[int, int], elf_pipe: tuple[tuple[int, int], ...]):
    pipe_in, pipe_out = elf_pipe
    if elf_range[0] >= pipe_in[1]:
        return None, None, elf_range
    elif elf_range[1] < pipe_in[0]:
        return elf_range, None, None

    if elf_range[0] < pipe_in[0]:
        low = (elf_range[0], pipe_in[0])
        fit_0 = pipe_in[0]
    else:
        low = None
        fit_0 = elf_range[0]
    if elf_range[1] >= pipe_in[1]:
        high = (pipe_in[1], elf_range[1])
        fit_1 = pipe_in[1]
    else:
        high = None
        fit_1 = elf_range[1]

    fit = (fit_0, fit_1)
    transform = pipe_out[0] - pipe_in[0]
    transformed = tuple(i + transform for i in fit)
    return low, transformed, high

def pipe_organ(elf_ranges: list[tuple[int,int], ...], raw_pipes: list[tuple[int, int, int]]) -> Generator[tuple[int,int] | None, None, None]:
    pipes = (pipe for pipe in sorted(elf_pipe(raw_pipe) for raw_pipe in raw_pipes))
    # sorted(elf_ranges)
    it_elfrng = iter(sorted(elf_ranges))

    pipe = next(pipes)
    # elf_pop = next(it_elfrng)
    for elf_pop in it_elfrng:
        if pipe is None:
            yield elf_pop
        while elf_pop and pipe:
            low, xformed, elf_pop = process_pipe(elf_pop, pipe)
            if low:
                yield low
            if xformed:
                yield xformed
            if elf_pop is None:
                continue
            try:
                pipe = next(pipes)
            except StopIteration:
                yield elf_pop
                elf_pop = None
                pipe = None
                continue

# def elf_range(rng_pair: tuple[int,int]) -> np.ndarray:
#     start, additional = rng_pair
#     return np.arange(start=start, stop=start + additional, dtype=int)

# def step_remap(elf_ranges: list[tuple[int,int,int]]) -> pd.Series:
#     ranges = list()
#     for rng in elf_ranges:
#         dst, src, addit = rng
#         ser = pd.Series(elf_range((dst, addit)), index=elf_range((src, addit)))
#         ranges.append(ser)
#     remap = pd.concat(ranges, copy=False).sort_index()
#     return remap


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

    almanac = parse_almanac(file.read())
    file.close()

    # Lowest location number for all seeds
    # steps_mapped = tuple(step for step in mapped_steps(almanac))
    # lowest_loc = min(steps_mapped[-1][1])

    # steps_it = iter(almanac)
    # col, seed_vals = next(steps_it)
    # seed_vals_it = iter(seed_vals[0])
    # seed_pairs = list(zip(seed_vals_it, seed_vals_it))
    # seed_pairs_it = iter(seed_pairs)
    # seed_df = pd.DataFrame({col: elf_range(next(seed_pairs_it))})
    # prev_step = col

    # step, spec_maps = next(steps_it)
    # step_maps = step_remap(spec_maps)
    # seed_df[step] = seed_df.replace(step_maps)
    # for step, spec_maps in steps_it:
    #     step_maps
        # step_map = partial(map_num, spec_maps=spec_map)
        # steps_mapped[step] = steps_mapped[prev_step].map(step_map)
        # prev_step = step
    # lowest_loc = steps_mapped[step].min()

    it_almanac = iter(almanac)
    init = next(it_almanac)
    it_seeds = iter(init[1][0])
    seeds = [elf_range(germ) for germ in zip(it_seeds, it_seeds)]
    pipeline = [(name, partial(pipe_organ, raw_pipes=step)) for name, step in it_almanac]
    output = seeds
    for name, step in pipeline:
        # breakpoint()
        output = [pam for pam in step(output)]
        print(f"{name}: {output}")

    lowest_loc = min(min(output))

    print(f"The lowest location number: {lowest_loc}")
    if args.test:
        # ans = 35  # Part 1 example answer
        ans = 46  # Part 2 example answer
        assert lowest_loc == ans, f"Lowest location: {lowest_loc} does not match expected: {ans}"

