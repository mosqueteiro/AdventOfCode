"""
--- Day 8: Haunted Wasteland ---

You're still riding a camel across Desert Island when you spot a sandstorm quickly approaching. When you turn to warn the Elf, she disappears before your eyes! To be fair, she had just finished warning you about ghosts a few minutes ago.

One of the camel's pouches is labeled "maps" - sure enough, it's full of documents (your puzzle input) about how to navigate the desert. At least, you're pretty sure that's what they are; one of the documents contains a list of left/right instructions, and the rest of the documents seem to describe some kind of network of labeled nodes.

It seems like you're meant to use the left/right instructions to navigate the network. Perhaps if you have the camel follow the same instructions, you can escape the haunted wasteland!

After examining the maps for a bit, two nodes stick out: AAA and ZZZ. You feel like AAA is where you are now, and you have to follow the left/right instructions until you reach ZZZ.

This format defines each node of the network individually. For example:

```
RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)
```

Starting with AAA, you need to look up the next element based on the next left/right instruction in your input. In this example, start with AAA and go right (R) by choosing the right element of AAA, CCC. Then, L means to choose the left element of CCC, ZZZ. By following the left/right instructions, you reach ZZZ in 2 steps.

Of course, you might not find ZZZ right away. If you run out of left/right instructions, repeat the whole sequence of instructions as necessary: RL really means RLRLRLRLRLRLRLRL... and so on. For example, here is a situation that takes 6 steps to reach ZZZ:

```
LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)
```

Starting at AAA, follow the left/right instructions. How many steps are required to reach ZZZ?

--- Part Two ---

The sandstorm is upon you and you aren't any closer to escaping the wasteland. You had the camel follow the instructions, but you've barely left your starting position. It's going to take significantly more steps to escape!

What if the map isn't for people - what if the map is for ghosts? Are ghosts even bound by the laws of spacetime? Only one way to find out.

After examining the maps a bit longer, your attention is drawn to a curious fact: the number of nodes with names ending in A is equal to the number ending in Z! If you were a ghost, you'd probably just start at every node that ends with A and follow all of the paths at the same time until they all simultaneously end up at nodes that end with Z.

For example:

```
LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)
```

Here, there are two starting nodes, 11A and 22A (because they both end with A). As you follow each left/right instruction, use that instruction to simultaneously navigate away from both nodes you're currently on. Repeat this process until all of the nodes you're currently on end with Z. (If only some of the nodes you're on end with Z, they act like any other node and you continue as normal.) In this example, you would proceed as follows:

    Step 0: You are at 11A and 22A.
    Step 1: You choose all of the left paths, leading you to 11B and 22B.
    Step 2: You choose all of the right paths, leading you to 11Z and 22C.
    Step 3: You choose all of the left paths, leading you to 11B and 22Z.
    Step 4: You choose all of the right paths, leading you to 11Z and 22B.
    Step 5: You choose all of the left paths, leading you to 11B and 22C.
    Step 6: You choose all of the right paths, leading you to 11Z and 22Z.

So, in this example, you end up entirely on nodes that end in Z after 6 steps.

Simultaneously start on every node that ends with A. How many steps does it take before you're only on nodes that end with Z?

"""


from enum import IntEnum
from textwrap import dedent
from typing import Generator, TypeAlias


Node_map: TypeAlias = dict[str, tuple[str, str]]

class Directions(IntEnum):
    L = 0
    R = 1

def follow_directions(directions: list[Directions], node_map: Node_map) -> Generator[tuple[int, str], None, None]:
    i = 0
    node = 'AAA'
    while node != 'ZZZ':
        for dir in directions:
            i += 1
            node = node_map[node][dir]
            yield i, node
            if node == 'ZZZ':
                return

def follow_ghost_directions(directions: list[Directions], node_map: Node_map) -> Generator[tuple[int, tuple[str, ...]], None, None]:
    i = 0
    nodes = tuple(node for node in node_map if node[-1] == 'A')
    while True:
        for dir in directions:
            i += 1
            # node = node_map[node][dir]
            nodes = tuple(node_map[node][dir] for node in nodes)
            yield i, nodes
            if all(node[-1] == 'Z' for node in nodes):
                return

def node_cycle(node: str, directions: list[Directions], node_map: Node_map)  -> Generator[tuple[int, str], None, None]:
    i = 0
    while True:
        for dir in directions:
            i += 1
            node = node_map[node][dir]
            if node[-1] == 'Z':
                yield i, node

def is_cycle(first_cycle: tuple[int, str], gen: Generator[tuple[int, str], None, None]) -> bool:
    steps, end_node = first_cycle
    for n in range(2, 4+2):  # check for 4 cycles
        step_n, node_n = next(gen)
        if (step_n / steps != n) or (node_n != end_node):
            return False
    return True

def gcd(a: int, b:int) ->  int:
    while b != 0:
        a, b = b, a%b
    return a

def lcm(*args: int) -> int:
    it_args = iter(args)
    a = next(it_args)
    for b in it_args:
        a = a // gcd(a, b) * b
    return a

def parse_nodes(text: str) -> Node_map:
    raw_nodes = [node.split("=") for node in text.strip().split("\n")]
    node_map = {k.strip(): tuple(v.strip()[1:-1].split(", ")) for k, v in raw_nodes}
    return node_map

def parse_map(text: str) -> tuple[list[Directions], Node_map]:
    raw_directions, raw_nodes = text.split("\n\n")
    directions = list(Directions[d] for d in raw_directions.strip())
    node_map = parse_nodes(raw_nodes)
    return directions, node_map


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

    directions, node_map = parse_map(file.read())
    for n in follow_directions(directions, node_map):
        steps, node = n
    print(f"Total steps are: {steps}\nEnding on node: {node}")

    if args.test:
        ans = 2
        assert steps == ans, f"\nTotal steps did not equal expected ({ans})"

        ans2 = 6
        EXAMPLE_2 = dedent("""
        LLR

        AAA = (BBB, BBB)
        BBB = (AAA, ZZZ)
        ZZZ = (ZZZ, ZZZ)
        """)
        for n in follow_directions(*parse_map(EXAMPLE_2)):
            steps, node = n
        assert steps == ans2, f"Second test failure: total steps ({steps}) did not match expected ({ans2})"

    print(" Step II: Ghost steps ".center(50, "-"))
    if args.test:
        ans = 6
        EXAMPLE_II = dedent("""
        LR

        11A = (11B, XXX)
        11B = (XXX, 11Z)
        11Z = (11B, XXX)
        22A = (22B, XXX)
        22B = (22C, 22C)
        22C = (22Z, 22Z)
        22Z = (22B, 22B)
        XXX = (XXX, XXX)
        """)
        for n in follow_ghost_directions(*parse_map(EXAMPLE_II)):
            steps, node = n
        assert steps == ans, f"Total number of ghost steps ({steps}) did not equal expected ({ans})"

    start_nodes = [node for node in node_map.keys() if node[-1] == 'A']
    cycle_generators = tuple(node_cycle(node, directions, node_map) for node in start_nodes)
    node_cycles = tuple(next(gen) for gen in cycle_generators)
    are_cycles = tuple(is_cycle(first_cycle, gen) for first_cycle, gen in zip(node_cycles, cycle_generators))
    assert all(are_cycles), "Not all nodes are cyclical"
    cycles, end_nodes = [*zip(*node_cycles)]
    steps = lcm(*(node for node in cycles))
    print(f"Total ghost steps are: {steps}\nEnding on nodes: {end_nodes}")

    # This took too long, cancelled running after 10 min
    # for n in follow_ghost_directions(directions, node_map):
    #     steps, nodes = n

