"""
--- Day 5: Print Queue ---
https://adventofcode.com/2024/day/5

--------------------- Part I ---------------------
The sum of the valid middles is (4462)

-------------------- Part II ---------------------
The sum of the reordered middles is (6767)
"""


from __future__ import annotations
from collections import defaultdict, deque
from dataclasses import dataclass


def parse_behind_queue(raw_ordering: str) -> dict[int, set[int]]:
    ordering = raw_ordering.split("\n")
    behind_queue = defaultdict(set)
    for p_ord in ordering:
        first, last = map(int, p_ord.split("|"))
        behind_queue[last].add(first)
    return behind_queue

def parse_updates(raw_updates: str) -> list[tuple[int, ...]]:
    splits = [tuple(line.split(",")) for line in raw_updates.strip().split("\n")]
    return [tuple(map(int, nums)) for nums in splits]

def update_ordered(update: tuple[int, ...], behind_queue: dict[int, set[int]]) -> bool:
    for i, num in enumerate(update, 1):
        if behind_queue[num].intersection(update[i:]):
            return False

    return True

def middle(update: tuple[int, ...]) -> int:
    idx = len(update) // 2
    return update[idx]

@dataclass
class Node:
    value: int
    left: Node | None = None
    right: Node | None = None

@dataclass
class BinaryTree:
    root: Node
    lookup: dict[int, set[int]]

    def add(self, node: Node):
        curr = self.root
        while curr is not None:
            prior = curr
            if node.value in self.lookup.get(curr.value, set()):
                curr = curr.left
                if curr is None:
                    prior.left = node
            else:
                curr = curr.right
                if curr is None:
                    prior.right = node

    def sorted_tuple(self) -> tuple[int, ...]:
        curr = self.root
        q = deque()
        sortup = deque()
        while curr or q:
            if curr:
                q.append(curr)
                curr = curr.left
            elif q:
                this = q.pop()
                sortup.append(this.value)
                curr = this.right

        return tuple(sortup)

def btree_sort(arr: tuple[int, ...], lookup: dict[int, set[int]]) -> tuple[int, ...]:
    it_arr = iter(arr)
    btree = BinaryTree(Node(next(it_arr)), lookup)
    for i in it_arr:
        btree.add(Node(i))
    return btree.sorted_tuple()


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
    order_rules, raw_updates = file.read().split("\n\n")
    behind_queue = parse_behind_queue(order_rules)
    updates = parse_updates(raw_updates)
    sum_middles = sum(middle(update) for update in updates if update_ordered(update, behind_queue))
    print(f"The sum of the valid middles is ({sum_middles})")

    if args.test:
        ans = 143
        assert sum_middles == ans, f"The sum of middles didn't match expected ({ans})"

    print()
    print(" Part II ".center(50, "-"))
    out_of_order = (update for update in updates if not update_ordered(update, behind_queue))
    ordered = [btree_sort(unordered, behind_queue) for unordered in out_of_order]
    sum_middles = sum(middle(update) for update in ordered)
    print(f"The sum of the reordered middles is ({sum_middles})")

    if args.test:
        ans = 123
        assert sum_middles == ans, f"Reordered sum of middles didn't match expected ({ans})"

