PosType = tuple[int, int]


def parse() -> list[list[str]]:
    with open(r"./data/day11.txt", "r", encoding="utf-8") as handle:
        old = [list(line.strip()) for line in handle]

    # update horizontal
    new = []
    for line in old:
        if set(line) == {
            ".",
        }:
            new.append(line[::])
        new.append(line)

    final = [[] for _ in new]

    # update vertical
    for index in range(len(new[0])):
        line = {row[index] for row in new}
        if line == {
            ".",
        }:
            for r, row in enumerate(new):
                final[r].append(row[index])

        for r, row in enumerate(new):
            final[r].append(row[index])

    return final


def parse2() -> tuple[list[list[str]], list[int], list[int]]:
    with open(r"./data/day11.txt", "r", encoding="utf-8") as handle:
        old = [list(line.strip()) for line in handle]

    # update horizontal
    rows = []
    for index, line in enumerate(old):
        if set(line) == {
            ".",
        }:
            rows.append(index)

    # update vertical
    cols = []
    for index in range(len(old[0])):
        line = {row[index] for row in old}
        if line == {
            ".",
        }:
            cols.append(index)

    return old, rows, cols


def find_galaxies(image: list[list[str]]) -> list[PosType]:
    galaxies = []
    for row, rr in enumerate(image):
        for col, _ in enumerate(rr):
            if image[row][col] == "#":
                galaxies.append((row, col))
    return galaxies


def generate_pairs(galaxies: list[PosType]) -> list[tuple[PosType, PosType]]:
    pairs = []
    while galaxies:
        galaxy = galaxies.pop()
        for g2 in galaxies:
            pairs.append((galaxy, g2))
    return pairs


def taxicab_distance(pos1: PosType, pos2: PosType) -> int:
    """he sum of the absolute value of the difference of x values and the
    absolute value of the difference of y values."""
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])


def taxicab_distance_modified(
    cost: int, pos1: PosType, pos2: PosType, rows: list[int], cols: list[int]
) -> int:
    """the sum of the absolute value of the difference of x values and the
    absolute value of the difference of y values."""
    distance = abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

    for row in rows:
        if row in range(min(pos1[0], pos2[0]), max(pos1[0], pos2[0])):
            # need to -1 here to `replace` the row
            distance += cost - 1

    for col in cols:
        if col in range(min(pos1[1], pos2[1]), max(pos1[1], pos2[1])):
            # need to -1 here to `replace` the col
            distance += cost - 1

    return distance


def part01() -> None:
    image = parse()
    galaxies = find_galaxies(image)
    # send in a copy - not sure if part2 will need the original yet.
    pairs = generate_pairs(galaxies[::])
    t = 0
    for pair in pairs:
        t += taxicab_distance(*pair)
    assert t == 9550717


def part02() -> None:
    image, rows, cols = parse2()
    galaxies = find_galaxies(image)
    # send in a copy - not sure if part2 will need the original yet.
    pairs = generate_pairs(galaxies[::])
    t = 0
    for pair in pairs:
        t += taxicab_distance_modified(1_000_000, pair[0], pair[1], rows, cols)
    assert t == 648458253817


def run() -> None:
    part01()
    part02()


if __name__ == "__main__":
    run()
