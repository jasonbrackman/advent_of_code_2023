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

PosType = tuple[int, int]

dirs = {
    "N": (-1, 0),
    "E": (0, 1),
    "S": (1, 0),
    "W": (0, -1),
}

rules = {
    "|": {dirs["N"], dirs["S"]},
    "-": {dirs["E"], dirs["W"]},
    "L": {dirs["N"], dirs["E"]},
    "J": {dirs["N"], dirs["W"]},
    "7": {dirs["S"], dirs["W"]},
    "F": {dirs["S"], dirs["E"]},
    ".": set(),
}


def parse() -> list[list[str]]:
    hm: list[list[str]] = []
    with open(r"./data/day10.txt", "r", encoding="utf-8") as handle:
        for line in handle.readlines():
            hm.append(list(line.strip()))
    return hm


def get_start_pos(hm: list[list[str]]) -> PosType:
    for r, row in enumerate(hm):
        for c, cell in enumerate(row):
            if cell == "S":
                return r, c
    raise ValueError("No start position found")


def add_pos(pos: PosType, other: PosType) -> PosType:
    return pos[0] + other[0], pos[1] + other[1]


def get_inverse(pos: PosType) -> PosType:
    return -pos[0], -pos[1]


def get_neighbours(pos: PosType, hm: list[list[str]]) -> list[PosType]:
    neighbours = []
    possibles = rules[hm[pos[0]][pos[1]]]
    for possible in possibles:
        nr, nc = add_pos(pos, possible)
        if 0 <= nr < len(hm) and 0 <= nc < len(hm[0]):
            neighbours.append((nr, nc))

    return neighbours


def part01(pipes: set[PosType]) -> int:
    return int(len(pipes) / 2)


def part02(hm: list[list[str]], pipes: set[PosType]) -> int:
    debug = []
    t = 0
    for row, rr in enumerate(hm):
        for col, _ in enumerate(rr):
            if (row, col) not in pipes:
                # If hit count is odd, the space is within the polygon.
                raycast = [hm[row][i] for i in range(-1, col) if (row, i) in pipes]

                # Account for lines L--7 is 1 hit L--J is two (its a miss but even)
                hits = [i for i in raycast if i in ("|JL")]
                if len(hits) % 2 == 1:
                    t += 1
                    debug.append((row, col))

    # pprint(debug, hm, pipes)
    return t


def pipe_path(hm, start):
    seen = {
        start,
    }
    neighbours = get_neighbours(start, hm)
    while neighbours:
        pos = neighbours.pop()

        if pos in seen:
            continue

        for n in get_neighbours(pos, hm):
            seen.add(pos)
            if n not in seen:
                neighbours.append(n)
    return seen


def pprint(debug, hm, seen):
    for index, row in enumerate(hm):
        for c in range(len(row)):
            if (index, c) in debug:
                print("*", end="")
            elif (index, c) not in seen:
                print(" ", end="")
            else:
                print(hm[index][c], end="")
        print()


def run() -> None:
    hm = parse()
    start = get_start_pos(hm)

    # This probably should not be hardcoded; visual check for input/tests is the same.
    hm[start[0]][start[1]] = "F"

    pipes = pipe_path(hm, start)

    assert part01(pipes) == 6690
    assert part02(hm, pipes) == 525


if __name__ == "__main__":
    run()
