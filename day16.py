from __future__ import annotations
from collections import deque
from dataclasses import dataclass
from typing import List

Grid = list[str]


def parse(s: str) -> Grid:
    with open(s, "r", encoding="utf-8") as file:
        return [line.strip() for line in file]


@dataclass(frozen=True)
class Node:
    pos: tuple[int, int]
    dir: tuple[int, int]

    def next(self, grid: Grid) -> list[Node]:
        nodes = []
        new_pos = (self.pos[0] + self.dir[0], self.pos[1] + self.dir[1])

        if (
            new_pos[0] < 0
            or new_pos[0] >= len(grid)
            or new_pos[1] < 0
            or new_pos[1] >= len(grid[0])
        ):
            return nodes

        icon = grid[new_pos[0]][new_pos[1]]
        if icon == ".":
            return [Node(new_pos, self.dir)]

        elif icon == "|":
            if self.dir in ((0, 1), (0, -1)):
                # go up / down
                nodes.append(Node(new_pos, (-1, 0)))
                nodes.append(Node(new_pos, (1, 0)))
            else:
                nodes.append(Node(new_pos, self.dir))
            return nodes

        elif icon == "-":
            if self.dir in ((-1, 0), (1, 0)):
                # go left / right
                nodes.append(Node(new_pos, (0, -1)))
                nodes.append(Node(new_pos, (0, 1)))
            else:
                nodes.append(Node(new_pos, self.dir))
            return nodes
        elif icon == "/":
            if self.dir == (0, 1):
                # go up
                nodes.append(Node(new_pos, (-1, 0)))
            elif self.dir == (0, -1):
                # go down
                nodes.append(Node(new_pos, (1, 0)))
            elif self.dir == (1, 0):
                # go left
                nodes.append(Node(new_pos, (0, -1)))
            else:
                nodes.append(Node(new_pos, (0, 1)))
            return nodes

        elif icon == "\\":
            if self.dir == (0, 1):
                # go down
                nodes.append(Node(new_pos, (1, 0)))
            elif self.dir == (0, -1):
                # go up
                nodes.append(Node(new_pos, (-1, 0)))
            elif self.dir == (1, 0):
                # go right
                nodes.append(Node(new_pos, (0, 1)))
            else:
                nodes.append(Node(new_pos, (0, -1)))
            return nodes
        # empty?
        return nodes


def part01():
    grid = parse(r"./data/day16.txt")

    start = Node((0, 0), (1, 0))
    nodes = deque([start])

    visited = {start}
    while nodes:
        current = nodes.popleft()
        for node in current.next(grid):
            if node not in visited:
                visited.add(node)
                nodes.append(node)

    total = len({v.pos for v in visited})
    assert total == 7939


def run():
    part01()


if __name__ == "__main__":
    run()
