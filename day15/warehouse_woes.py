"""
--- Day 15: Warehouse Woes ---

--------------------- Part I ---------------------
The sum of all the boxes GPS coords is (1442192)

-------------------- Part II ---------------------
The sum of all the wide boxes GPS coords is (1448458)
"""


from collections import deque
from dataclasses import dataclass
from typing import Generator

from numpy import array, dtype, ndarray, where
from pandas import DataFrame


type Point = tuple[int, int]

@dataclass
class Warehouse:
    layout: ndarray
    robot_moves: deque

    def __post_init__(self):
        self.robot = self.find_robot()
        self.move_map = {
            "^": (-1,0),
            "v": (1,0),
            "<": (0, -1),
            ">": (0, 1),
        }

    def __str__(self):
        df = DataFrame(self.layout)
        return f"{df}\n\nMoves left: {len(self.robot_moves)}\n{self.robot_moves}"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(\n{self.__str__()}\n)"

    def find_robot(self) -> Point:
        locs = list(zip(*where(self.layout == '@')))
        assert len(locs) == 1, "Robot found at too many locations, only 1 allowed"
        return locs[0]

    def move_robot(self, moves: int = 1):
        if not self.robot_moves:
            raise IndexError("No moves left for robot")
        elif moves > len(self.robot_moves):
            raise IndexError(f"Too many moves specified, only ({len(self.robot_moves)}) left")

        if moves in {None, -1}:
            moves = len(self.robot_moves)
        for _ in range(moves):
            self._move(self.robot, self.robot_moves.popleft())

    def _move(self, position: Point, direction: str) -> bool:
        if not all(0 <= x < X for x, X in zip(position, self.layout.shape)):
            raise IndexError("Position is out of bounds")

        next_pos = tuple(i + d for i,d in zip(position, self.move_map[direction]))
        match (self.layout[position], self.layout[next_pos]):
            case [("#" | "."), _] | [_, "#"]:
                return False
            case [curr, "."]:
                self.layout[next_pos] = curr
                if curr == "@":
                    self.robot = next_pos
                self.layout[position] = "."
                return True
            case [curr, "O"]:
                if self._move(next_pos, direction):
                    self.layout[next_pos] = curr
                    if curr == "@":
                        self.robot = next_pos
                    self.layout[position] = "."
                    return True
                return False
            case [curr, ("[" | "]") as big_box]:
                if direction in ("^", "v"):
                    match big_box:
                        case "[":
                            next_pos_opp = tuple(i + d for i,d in zip(next_pos, self.move_map[">"]))
                            wide_pos = (next_pos, next_pos_opp)
                        case "]":
                            next_pos_opp = tuple(i + d for i,d in zip(next_pos, self.move_map["<"]))
                            wide_pos = (next_pos_opp, next_pos)
                    if self._move_wide(wide_pos, direction):
                        self.layout[next_pos] = curr
                        self.layout[position] = "."
                        self.robot = next_pos
                        return True
                elif self._move(next_pos, direction):
                    self.layout[next_pos] = curr
                    if curr == "@":
                        self.robot = next_pos
                    self.layout[position] = "."
                    return True
                return False
            case _:
                raise ValueError(f"Unexpected values at {position} or {next_pos}")

    def _move_wide(self, wide_position: tuple[Point, Point], direction: str) -> bool:
        moves_list = list(self._move_wide_wrapper(wide_position, direction))
        moves_list = [wide_position] + moves_list
        if not moves_list.pop():
            return False

        start = array(moves_list)
        # move = start + self.move_map[direction]
        dups = set()
        for left, right in reversed(start):
            if ((*left,), (*right,)) in dups:
                continue
            dups.add(((*left,), (*right,)))
            l_move = left + self.move_map[direction]
            r_move = right + self.move_map[direction]
            self.layout[*l_move] = self.layout[*left]
            self.layout[*r_move] = self.layout[*right]
            self.layout[*left] = "."
            self.layout[*right] = "."
        # Don't forget to move the initial wide_position
        return True

    def _move_wide_wrapper(self, wide_position: tuple[Point, Point], direction: str) -> Generator[tuple[Point, Point] | bool, None, None]:
        can_move = yield from self._move_wide_gen(wide_position, direction)
        yield can_move

    def _move_wide_gen(self, wide_position: tuple[Point, Point], direction: str) -> Generator[tuple[Point, Point], None, bool]:
        left_pos, right_pos = wide_position
        left, right = self.layout[left_pos], self.layout[right_pos]
        while True:
            next_left: Point = tuple(i + d for i,d in zip(left_pos, self.move_map[direction]))
            next_right: Point = tuple(i + d for i,d in zip(right_pos, self.move_map[direction]))
            match (left, right, self.layout[next_left], self.layout[next_right]):
                case [_, _, "#", _] | [_, _, _, "#"]:
                    return False
                case [_, _, ".", "."]:
                    return True
                case [left, right, "]", "["]:
                    _side_left = tuple(i + d for i,d in zip(next_left, self.move_map["<"]))
                    _side_right = tuple(i + d for i,d in zip(next_right, self.move_map[">"]))
                    yield _side_left, next_left
                    yield next_right, _side_right
                    left_return = yield from self._move_wide_gen((_side_left, next_left), direction)
                    if left_return == False:
                        return left_return
                    right_return = yield from self._move_wide_gen((next_right, _side_right), direction)
                    return right_return
                case [left, right, "[", "]"]:
                    yield next_left, next_right
                case [left, right, "]", "."]:
                    next_right = next_left
                    next_left = tuple(i + d for i,d in zip(next_left, self.move_map["<"]))
                    yield next_left, next_right
                case [left, right, ".", "["]:
                    next_left = next_right
                    next_right = tuple(i + d for i,d in zip(next_right, self.move_map[">"]))
                    yield next_left, next_right
                case [left, right, _left, _right]:
                    raise ValueError(f"Unknown position encountered ({left}, {right}) -> ({_left, _right})")
            left_pos, right_pos = next_left, next_right
            left, right = self.layout[left_pos], self.layout[right_pos]

    def sum_gps(self, wide: bool = False) -> int:
        box = "[" if wide else "O"
        top, left = where(self.layout == box)
        return (top * 100 + left).sum()

def parse_input(input: str, wide: bool = False) -> Warehouse:
    if wide:
        input = input.replace("O", "[]").replace("#", "##").replace(".","..").replace("@", "@.")
    raw_layout, raw_moves = input.split("\n\n")
    layout = array([tuple(s.strip()) for s in raw_layout.split()])
    assert layout.dtype == dtype('U1'), f"Array must be tupe 'U1' not {layout.dtype}"
    robot_moves = deque(raw_moves.replace('\n','').strip())
    return Warehouse(layout, robot_moves)


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
    input = file.read()
    warehouse = parse_input(input)
    frames = [warehouse.layout.copy()]
    for _ in range(len(warehouse.robot_moves)):
        warehouse.move_robot(1)
        frames.append(warehouse.layout.copy())
    sum_gps = warehouse.sum_gps()
    print(f"The sum of all the boxes GPS coords is ({sum_gps})")

    if args.test:
        ans = 10092
        assert sum_gps == ans, f"The sum of GPS coords didn't match expected ({ans})"

    print_part_divider("Part II")
    wide_warehouse = parse_input(input, wide=True)
    frames_wide = [wide_warehouse.layout.copy()]
    for _ in range(len(wide_warehouse.robot_moves)):
        wide_warehouse.move_robot(1)
        frames_wide.append(wide_warehouse.layout.copy())

    sum_gps_wide = wide_warehouse.sum_gps(wide=True)
    print(f"The sum of all the wide boxes GPS coords is ({sum_gps_wide})")

    if args.test:
        ans = 9021
        assert sum_gps_wide == ans, f"The sum of GPS coords didn't match expected ({ans})"

