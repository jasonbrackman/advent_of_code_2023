from __future__ import annotations
from dataclasses import dataclass, field
import sys
import heapq


sys.setrecursionlimit(5000)


Vec2 = tuple[int, int]
Grid = dict[Vec2, int]

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
    his: int
    goal: Vec2
    val: int
    key: tuple[Vec2, Vec2, int] = field(init=False)

    def __post_init__(self):
        self.key = (
            self.pos,
            self.dir,
            self.his,
        )

    def __lt__(self, other):
        return self.val < other.val


def parse(s: str) -> Grid:
    grid: dict[Vec2, int] = dict()
    with open(s, "r", encoding="utf8") as file:
        for y, row in enumerate(file):
            for x, col in enumerate(row.strip()):
                grid[y, x] = int(col)
    return grid


def get_neighbours(
    grid: Grid, node: Node, goal: Vec2, min_: int, max_: int
) -> list[Node]:
    """Can try left, right, and forward, but not backward."""
    neighbours = []

    if node.his < min_:
        y, x = node.pos[0] + node.dir[0], node.pos[1] + node.dir[1]
        if (y, x) in grid:
            return [
                Node(
                    (y, x),
                    node.dir,
                    node.his + 1,
                    goal,
                    node.val + grid[(y, x)],
                )
            ]

    for d in ((0, 1), (0, -1), (1, 0), (-1, 0)):
        # new direction should not be equal to the heading if reached maximum moves.
        if d == node.dir and node.his == max_:
            continue

        if (d[0] + node.dir[0], d[1] + node.dir[1]) == (0, 0):
            continue

        # if the y, x position is within the Grid and not a backstep
        y, x = node.pos[0] + d[0], node.pos[1] + d[1]
        if (y, x) in grid:
            new_his = 1 if d != node.dir else node.his + 1
            neighbours.append(
                Node(
                    (y, x),
                    d,
                    new_his,
                    goal,
                    node.val + grid[(y, x)],
                )
            )

    return neighbours


def part01(grid: Grid):
    goal = max(grid)
    start = Node((0, 0), (0, 1), 0, goal, 0)

    Q = [start]

    result = None
    min_val = sys.maxsize
    visited = set()

    while Q:
        current = heapq.heappop(Q)
        if current.key in visited:
            continue

        visited.add(current.key)

        if current.pos == goal:
            # print("Result:", current)
            return current

        for item in get_neighbours(grid, current, goal, 0, 3):
            if item.key not in visited:
                if item.val < min_val:
                    heapq.heappush(Q, item)

    return result


def run() -> None:
    grid = parse(r"./data/day17.txt")
    r = part01(grid)
    assert r.val == 724


if __name__ == "__main__":
    run()