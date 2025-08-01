"""
--- Day 16: Reindeer Maze ---

--------------------- Part I ---------------------
The lowest score for the Reindeer Maze is (95444)
Took 9.056[s] to run.

-------------------- Part II ---------------------
There are (514) best tiles to choose from
Took 1020.043[s] to run.

It was actually 513, off by one somewhere.
"""


from collections import deque
from heapq import heapify, heappop, heappush
from time import perf_counter

from numpy import array, dtype, ndarray, where
from pandas import DataFrame


type Point = tuple[int, int]

type Path = list[str]

DIRECTIONS = {
    "^": (-1, 0),
    "v": (1, 0),
    "<": (0, -1),
    ">": (0, 1),
}

class Maze:
    def __init__(self, maze: ndarray):
        self.maze = maze
        start = tuple(zip(*where(maze == "S")))
        assert len(start) == 1
        start = start[0]
        assert len(start) == 2
        self.start: Point = start
        end = tuple(zip(*where(maze == "E")))
        assert len(end) == 1
        end = end[0]
        assert len(end) == 2
        self.end: Point = end
        all_points = list(zip(*where(maze == ".")))
        all_points += [start, end]
        self.all_points: list[Point] = all_points

    @property
    def start_directions(self) -> deque:
        return deque((">", "^", "<", "v"))

    def __str__(self) -> str:
        return DataFrame(self.maze).__str__()

    def neighbors(self, position: Point, directions: deque) -> list[tuple[Point, int, int]]:
        ROTATE_LEFT = -1
        ROTATE_RIGHT = 1
        face_forward, face_left, _, face_right = directions
        pnt_forward = add_points(position, DIRECTIONS[face_forward])
        pnt_left = add_points(position, DIRECTIONS[face_left])
        pnt_right = add_points(position, DIRECTIONS[face_right])
        points = [
            (pnt, val, rotate)
            for pnt, val, rotate in zip((pnt_forward, pnt_left, pnt_right), (1, 1000+1, 1000+1), (0, ROTATE_LEFT, ROTATE_RIGHT))
            if pnt in self.all_points
        ]

        return points

    def dijkstra(self) -> tuple[dict[Point, int | float], dict[Point, tuple[Point | None, str]]]:
        priorq = [(0, self.start, self.start_directions)]
        heapify(priorq)

        dist = {point: float("inf") for point in self.all_points}
        dist[self.start] = 0
        prev: dict[Point, tuple[Point | None, str]] = {}
        prev[self.start] = (None, self.start_directions[0])

        while priorq:
            current_cost, current_point, current_directions = heappop(priorq)

            for point, cost, rotation in self.neighbors(current_point, current_directions):
                alt_cost = current_cost + cost
                if alt_cost < dist[point]:
                    dist[point] = alt_cost
                    prev[point] = (current_point, current_directions[0])
                    next_directions = current_directions.copy()
                    next_directions.rotate(rotation)
                    heappush(priorq, (alt_cost, point, next_directions))

        return dist, prev


def add_points(p1: Point, p2: Point) -> Point:
    x1, y1 = p1
    x2, y2 = p2
    return x1 + x2, y1 + y2

def parse_maze(raw_input: str) -> Maze:
    maze = array([tuple(s.strip()) for s in raw_input.split()])
    assert maze.dtype == dtype('U1'), f"Array must be tupe 'U1' not {maze.dtype}"
    return Maze(maze)

def find_similar_paths(maze: Maze, dist: dict, prev: dict) -> set[Point | None]:
    end = maze.end
    directions = maze.start_directions
    score_match = dist[end]
    init_path = reconstruct_path(end, prev)
    orig_path = [tile for tile, _ in init_path]
    best_tiles = set(orig_path)
    for tile, new_dir in init_path[:-1]:
        if tile is None:
            continue
        rotation = directions.index(new_dir)
        directions.rotate(rotation)
        neighbors = maze.neighbors(tile, directions)
        if len(neighbors) <= 1:
            continue

        disable_tile, *_ = [point for point, *_ in neighbors if point in orig_path]
        assert not _, "Too many points on path, something went wrong."
        assert maze.maze[disable_tile] == ".", "Invalid tile, something went wrong"
        maze.maze[disable_tile] = "#"
        _maze = Maze(maze.maze)
        # get new lowest_score, if new_lowest_score == score_match: add to path set
        _low_score, _prev_path = _maze.dijkstra()
        if _low_score[_maze.end] == score_match:
            _path, _ = zip(*reconstruct_path(_maze.end, _prev_path))
            best_tiles.update(_path)
        maze.maze[disable_tile] = "."

    return best_tiles

def reconstruct_path(end: Point, prev_paths: dict[Point, tuple[Point | None, str]]) -> list[tuple[Point | None, str]]:
    point = end
    path: list[tuple[Point | None, str]] = [(end, 'E')]
    while step:=prev_paths.get(point):
        point, _ = step
        path.append(step)

    path.reverse()
    return path


if __name__ == "__main__":
    from adventofcode import arg_parser_init, print_part_divider

    parser = arg_parser_init()
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
    raw_input = file.read()
    start = perf_counter()
    maze = parse_maze(raw_input)
    if args.v:
        print("Maze:")
        print(maze)
        print("\n"*2)
    lowest_scores, previous_paths = maze.dijkstra()
    lowest_score = lowest_scores[maze.end]
    total_time = perf_counter() - start
    print(f"The lowest score for the Reindeer Maze is ({lowest_score})")
    print(f"Took {total_time:.3f}[s] to run.")

    if args.test:
        ans = 7036
        assert lowest_score == ans, f"The lowest score didn't match expected ({ans})"

    print_part_divider("Part II")
    start = perf_counter()
    all_best_tiles = find_similar_paths(maze, lowest_scores, previous_paths)
    total_time = perf_counter() - start
    print(f"There are ({len(all_best_tiles)}) best tiles to choose from")
    print(f"Took {total_time:.3f}[s] to run.")

    if args.test:
        ans = 45
        assert len(all_best_tiles) == ans, f"The number of paths didn't match expected ({ans})"

