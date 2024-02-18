from __future__ import annotations
import sys
from dataclasses import dataclass, field
from typing import Optional

from queue import PriorityQueue


sys.setrecursionlimit(5000)

Grid = list[list[int]]
Vec2 = tuple[int, int]

dirs = {
    (0, 1): ">",
    (0, -1): "<",
    (1, 0): "v",
    (-1, 0): "^",
}


@dataclass
class Node:
    pos: Vec2
    dir: Vec2
    his: tuple[Vec2, ...]
    val: int = field(default=0)
    prev: Optional[Node] = field(default=None)

    def manhattan(self, p2: Vec2) -> int:
        return abs(self.pos[0] - p2[0]) + abs(self.pos[1] - p2[1])

    def __lt__(self, other):
        return self.val < other.val

    def __hash__(self):
        return hash(self.pos) + hash(self.dir) + hash(self.his) + hash(self.val)


def parse(s: str) -> Grid:
    with open(s, "r", encoding="utf8") as file:
        return [list(int(i) for i in f.strip()) for f in file]


def get_neighbours(grid: Grid, node: Node) -> list[Node]:
    """Can try left, right, and forward, but not backward."""
    neighbours = []
    his = node.his[0] if len(node.his) == 3 else None

    # ensure new_pos is not the inverse of the .dir
    for d in ((0, 1), (0, -1), (1, 0), (-1, 0)):
        if d == his:
            continue
        if (d[0] + node.dir[0], d[1] + node.dir[1]) == (0, 0):
            continue

        y, x = node.pos[0] + d[0], node.pos[1] + d[1]

        if 0 <= y < len(grid) and 0 <= x < len(grid[0]):
            new_his = (d,) if d not in node.his else node.his + (d,)
            neighbours.append(
                Node((y, x), d, new_his, node.val + grid[y][x], prev=node)
            )

    return neighbours


def part01(grid: Grid):
    result = None
    min_val = sys.maxsize

    start = Node((0, 0), (0, 1), ((0, 1),))
    dest = (len(grid) - 1, len(grid[0]) - 1)
    visited = {start}

    nodes = PriorityQueue()
    nodes.put((start.manhattan(dest), start))
    while not nodes.empty():
        _, current = nodes.get()
        if current.val >= min_val:
            continue

        if current.pos == dest:
            print("Result:", current)
            if current.val < min_val:
                min_val = current.val
                result = current
            continue

        for item in get_neighbours(grid, current):
            hash_item = hash(item)
            if hash_item not in visited and item.val < min_val:
                visited.add(hash_item)
                nodes.put((item.manhattan(dest), item))

    return result


def run() -> None:
    grid = parse(r"./data/day17.txt")
    r = part01(grid)

    t1 = 0
    while r.prev is not None:
        t1 += grid[r.pos[0]][r.pos[1]]
        r = r.prev
    assert t1 == 724


if __name__ == "__main__":
    run()
