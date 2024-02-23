from __future__ import annotations
from dataclasses import dataclass, field
import heapq
from typing import Optional

Vec2 = tuple[int, int]
Grid = dict[Vec2, int]


@dataclass
class Node:
    pos: Vec2
    dir: Vec2
    his: int
    val: int
    parent: Optional[Node]  # used for debugging
    key: tuple[Vec2, Vec2, int] = field(init=False)

    def __post_init__(self):
        self.key = (self.pos, self.dir, self.his)

    def __lt__(self, other):
        return self.val < other.val


def parse(s: str) -> Grid:
    grid: dict[Vec2, int] = dict()
    with open(s, "r", encoding="utf8") as file:
        for y, row in enumerate(file):
            for x, col in enumerate(row.strip()):
                grid[y, x] = int(col)
    return grid


def get_neighbours(grid: Grid, node: Node, min_: int, max_: int) -> list[Node]:
    """Can try left, right, and forward, but not backward."""
    neighbours = []

    for d in ((0, 1), (0, -1), (1, 0), (-1, 0)):
        # new direction should not be equal to the heading if reached maximum moves.
        if d == node.dir and node.his == max_:
            continue

        if (d[0] + node.dir[0], d[1] + node.dir[1]) == (0, 0):
            continue

        if d == node.dir:
            y, x = node.pos[0] + d[0], node.pos[1] + d[1]
            if (y, x) in grid:
                neighbours.append(
                    Node((y, x), d, node.his + 1, node.val + grid[(y, x)], node)
                )
        else:
            # Turning 90 degrees; move min_ spaces and check if result in grid.
            y, x = node.pos
            v = node.val
            for _ in range(min_):
                y += d[0]
                x += d[1]
                v += grid.get((y, x), 0)
            if (y, x) in grid:
                neighbours.append(Node((y, x), d, min_, v, node))

    return neighbours


def part01(grid: Grid):
    goal = max(grid)
    start = Node((0, 0), (0, 1), 0, 0, None)

    Q = [start]

    result = None
    visited = set()

    while Q:
        current = heapq.heappop(Q)
        if current.key in visited:
            continue

        visited.add(current.key)

        if current.pos == goal:
            return current

        for item in get_neighbours(grid, current, 1, 3):
            if item.key not in visited:
                heapq.heappush(Q, item)

    return result


def part02(grid: Grid):
    goal = max(grid)

    # some setup here to ensure that the Crucible starts with a four move!
    start = Node((0, 0), (0, 1), 0, 0, None)
    y, x = start.pos
    v = start.val
    for _ in range(4):
        y += 0
        x += 1
        v += grid.get((y, x), 0)
    Q = [Node((y, x), (0, 1), 4, v, start)]

    result = None
    visited = set()

    while Q:
        current = heapq.heappop(Q)

        if current.key in visited:
            continue

        visited.add(current.key)

        if current.pos == goal:
            return current

        for item in get_neighbours(grid, current, 4, 10):
            if item.key not in visited:
                heapq.heappush(Q, item)

    return result


def run() -> None:
    grid = parse(r"./data/day17.txt")
    r = part01(grid)
    assert r.val == 724

    grid = parse(r"./data/day17.txt")
    r = part02(grid)
    assert r.val == 877


def pprint(grid, r):
    dirs = {
        (0, 1): ">",
        (0, -1): "<",
        (1, 0): "v",
        (-1, 0): "^",
    }

    results = dict()
    while r.parent is not None:
        results[r.pos] = r.dir
        r = r.parent

    max_grid = max(grid)
    for y in range(max_grid[0] + 1):
        line = ""
        for x in range(max_grid[1] + 1):
            if (y, x) in results:
                line += dirs[results[(y, x)]]
            else:
                line += " "
        print(line)


if __name__ == "__main__":
    run()
