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


def _jump_move(
    grid: Grid, node: Node, node_dir: Vec2, min_: int
) -> tuple[int, int, int]:
    """Move forward the minimum number of steps required by the rules."""
    y, x = node.pos
    v = node.val
    for _ in range(min_):
        y += node_dir[0]
        x += node_dir[1]
        v += grid.get((y, x), 0)
    return y, x, v


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
                    Node((y, x), d, node.his + 1, node.val + grid[(y, x)])
                )
        else:
            # Turning 90 degrees; move min_ spaces and check if result in grid.
            y, x, v = _jump_move(grid, node, d, min_)
            if (y, x) in grid:
                neighbours.append(Node((y, x), d, min_, v))

    return neighbours


def pathfind(grid: Grid, min_: int, max_: int) -> Optional[Node]:
    goal = max(grid)

    # some setup here to ensure that the Crucible starts with a four move!
    start = Node((0, 0), (0, 1), 0, 0)

    y, x, v = _jump_move(grid, start, start.dir, min_)

    Q = [Node((y, x), start.dir, min_, v)]

    result = None
    visited = set()

    while Q:
        current = heapq.heappop(Q)

        if current.key in visited:
            continue

        visited.add(current.key)

        if current.pos == goal:
            return current

        for item in get_neighbours(grid, current, min_, max_):
            if item.key not in visited:
                heapq.heappush(Q, item)

    return result


def run() -> None:
    grid = parse(r"./data/day17.txt")
    part01 = pathfind(grid, 1, 3)
    assert part01.val == 724

    grid = parse(r"./data/day17.txt")
    part02 = pathfind(grid, 4, 10)
    assert part02.val == 877


if __name__ == "__main__":
    run()
