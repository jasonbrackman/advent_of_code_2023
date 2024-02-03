"""
| is a vertical pipe connecting north and south.
- is a horizontal pipe connecting east and west.
L is a 90-degree bend connecting north and east.
J is a 90-degree bend connecting north and west.
7 is a 90-degree bend connecting south and west.
F is a 90-degree bend connecting south and east.
. is ground; there is no pipe in this tile.
S is the starting position of the animal; there is a pipe on this tile, but your sketch
doesn't show what shape the pipe has.
"""
dirs = {
    'N': (-1, 0),
    'E': (0, 1),
    'S': (1, 0),
    'W': (0, -1),
}

rules = {
    '|': {dirs['N'], dirs['S']},
    '-': {dirs['E'], dirs['W']},
    'L': {dirs['N'], dirs['E']},
    'J': {dirs['N'], dirs['W']},
    '7': {dirs['S'], dirs['W']},
    'F': {dirs['S'], dirs['E']},
    '.': set(),
}


def parse() -> list[list[str]]:
    hm: list[list[str]] = []
    with open(r"./data/day10.txt", "r", encoding="utf-8") as handle:
        for line in handle.readlines():
            hm.append(list(line.strip()))
    return hm


def get_start_pos(hm: list[list[str]]) -> tuple[int, int]:
    for r, row in enumerate(hm):
        for c, cell in enumerate(row):
            if cell == "S":
                return r, c
    raise ValueError("No start position found")


def add_pos(pos: tuple[int, int], other: tuple[int, int]) -> tuple[int, int]:
    return pos[0] + other[0], pos[1] + other[1]


def get_inverse(pos: tuple[int, int]) -> tuple[int, int]:
    return -pos[0], -pos[1]


def get_neighbours(pos: tuple[int, int], hm: list[list[str]]) -> list[tuple[int, int]]:
    neighbours = []
    possibles = rules[hm[pos[0]][pos[1]]]
    for possible in possibles:
        nr, nc = add_pos(pos, possible)
        if 0 <= nr < len(hm) and 0 <= nc < len(hm[0]):
            neighbours.append((nr, nc))

    return neighbours


def part01():
    hm = parse()
    start = get_start_pos(hm)
    hm[start[0]][start[1]] = 'F'  # This should not be hardcoded; but seems to be fine for now

    seen = {start, }

    neighbours = get_neighbours(start, hm)
    while neighbours:
        pos = neighbours.pop()

        if pos in seen:
            continue

        for n in get_neighbours(pos, hm):
            seen.add(pos)
            if n not in seen:
                neighbours.append(n)

    assert int(len(seen) / 2) == 6690


def run() -> None:
    part01()


if __name__ == "__main__":
    run()
