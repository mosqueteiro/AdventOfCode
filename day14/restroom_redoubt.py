"""
--- Day 14: Restroom Redoubt

--------------------- Part I ---------------------
The safety factor of this room is (225521010)
Time: 0.032529 s

-------------------- Part II ---------------------
It took 7774 s to get to the easter egg
This took IRL  33.648112 s
"""


from collections import Counter
from dataclasses import dataclass
from math import prod
import re
from time import perf_counter


@dataclass
class Robot:
    position: tuple[int, int]
    velocity: tuple[int, int]

@dataclass
class Room:
    size: tuple[int, int]
    robots: list[Robot]

    def __post_init__(self):
        self.time = 0

    def __str__(self):
        header = f"{self.__class__.__name__}(size={self.size}, robots={len(self.robots)}, time={self.time})"
        grid = self._state_()
        return f"{header}\n\nRoom:\n{grid}"

    def __repr__(self) -> str:
        return self.__str__()

    def _state_(self):
        grid = ["." * self.size[0] for _ in range(self.size[1])]

        positions = Counter()
        positions.update(tuple(robot.position for robot in self.robots))
        for position, count in positions.items():
            col, row = position
            grid[row] = ''.join(c if i != col else str(count) for i, c in enumerate(grid[row]))
        return '\n'.join(grid)

    def simulate_second(self, robot: Robot):
        pos = robot.position
        vel = robot.velocity
        new_pos = []
        for p, v, s in zip(pos, vel, self.size):
            new_p = p+v
            if new_p >= s:
                new_p -= s
            elif new_p < 0:
                new_p += s
            new_pos.append(new_p)
        robot.position = tuple(new_pos)

    def simulate(self, seconds: int):
        for s in range(1, seconds + 1):
            _ = [self.simulate_second(robot) for robot in self.robots]
            self.time += 1

    def score_quadrants(self) -> tuple[int, int, int, int]:
        mid = tuple(i/2 + 0.01 for i in self.size)
        quadrants = Counter()
        for robot in self.robots:
            x, y = robot.position
            if (0 <= x < int(mid[0])) and (0 <= y < int(mid[1])):
                quadrants[1] += 1
            elif (round(mid[0]) <= x < self.size[0]) and (0 <= y < int(mid[1])):
                quadrants[2] += 1
            elif (0 <= x < int(mid[0])) and (round(mid[1]) <= y < self.size[1]):
                quadrants[3] += 1
            elif (round(mid[0]) <= x < self.size[0]) and (round(mid[1]) <= y < self.size[1]):
                quadrants[4] += 1
        return tuple(quadrants[i] for i in (1,2,3,4))

    def easter_egg_search(self):
        return True if re.search(r'\d{10}', self._state_()) else False

def parse_input(input: str) -> list[Robot]:
    regex_iter = re.finditer(r"[-\d]+,[-\d]+", input, flags=re.M)
    robots = []
    for pair in regex_iter:
        robot = Robot(
            position=tuple(int(i) for i in pair.group().split(",")),
            velocity=tuple(int(i) for i in next(regex_iter).group().split(","))
        )
        robots.append(robot)
    return robots


if __name__ == "__main__":
    from argparse import ArgumentParser, FileType

    from adventofcode import print_part_divider

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
        space = (11, 7)
    elif args.f:
        file = args.f
        space = (101, 103)
    else:
        raise Exception("File or test must be specified")

    print_part_divider("Part I")
    start = perf_counter()
    robots = parse_input(file.read())
    room = Room(space, robots)
    room.simulate(100)
    safety_factor = prod(room.score_quadrants())
    end = perf_counter()
    print(f"The safety factor of this room is ({safety_factor})")
    print(f"Time: {end - start:.6f} s")

    if args.test:
        ans = 12
        assert safety_factor == ans, f"The safety factor doesn't match the expected ({ans})"

    print_part_divider("Part II")
    file.seek(0)
    start = perf_counter()
    robots = parse_input(file.read())
    room = Room(space, robots)
    while not room.easter_egg_search():
        room.simulate(1)
    easter_egg_time = room.time
    end = perf_counter()
    print(f"It took {easter_egg_time} s to get to the easter egg")
    print(f"This took IRL {end - start: .6f} s")

