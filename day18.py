def parse(file: str) -> list[tuple[tuple[int, int], int, str]]:
    """Parse the file and return a list of strings."""
    dirs = {
        "U": (-1, 0),
        "L": (0, 1),
        "D": (1, 0),
        "R": (0, -1),
    }

    with open(file, "r", encoding="utf8") as f:
        data = []
        for line in f.read().splitlines():
            parts = line.split()
            data.append((dirs[parts[0]], int(parts[1]), parts[2]))

    return data


def create_grid(
    instructions: list[tuple[tuple[int, int], int, str]]
) -> dict[tuple[int, int], str]:
    grid = {}

    current = (0, 0)
    for inst in instructions:
        direction, steps, label = inst
        for _ in range(steps):
            current = (current[0] + direction[0], current[1] + direction[1])
            grid[current] = label

    return grid


def part01(s: str) -> int:
    data = parse(s)
    grid = create_grid(data)
    # pprint(grid)

    t = 0
    min_y = min(grid)[0]
    max_y = max(grid)[0]
    min_x = min(g[1] for g in grid)
    max_x = max(g[1] for g in grid)

    for y in range(min_y, max_y + 1):
        scoop = 0
        for x in range(min_x, max_x + 1):
            if (y, x) not in grid:
                # how many edges to the right? within = odd; outside = 0 or even
                edge_count = 0
                y_pos = None
                for i in range(x, max_x + 1):
                    # Count each edge only once (if connected; it may be another edge)
                    # Example:
                    #                .                     .   .
                    #   One Edge ->  . . .   Two Edges ->  . . .
                    #                    .

                    if (y, i) in grid:
                        a = (y, i - 1) not in grid
                        b = (i + 1) <= max_x and (y, i + 1) not in grid
                        if a and b:
                            edge_count += 1
                        elif a:
                            assert y_pos is None
                            # left is clear so this is the first occupied space
                            edge_count += 1
                            # check up and down
                            if (y - 1, i) in grid:
                                y_pos = y - 1
                            if (y + 1, i) in grid:
                                y_pos = y + 1
                        elif b:
                            assert y_pos is not None
                            # edge_count += 1
                            if (y - 1, i) in grid and y_pos == y - 1:
                                edge_count += 1
                            elif (y + 1, i) in grid and y_pos == y + 1:
                                edge_count += 1

                            # else nothing to do but to clear the flag
                            y_pos = None

                if edge_count % 2 != 0:
                    scoop += 1
                    t += 1

                # if edge_count % 2 != 0:
                #    print(edge_count, end=", ")

            else:
                t += 1
        # print(" ", scoop)
    return t


def pprint(grid):
    min_y = min(grid)[0]
    max_y = max(grid)[0]
    min_x = min(g[1] for g in grid)
    max_x = max(g[1] for g in grid)
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            if (y, x) in grid:
                print("#", end="")
            else:
                print(".", end="")
            # print(grid.get((y, x), '.'), end='')
        print()


def run():
    t = part01(r"./data/day18t.txt")
    assert t == 62
    p1 = part01(r"./data/day18.txt")
    assert p1 == 50603


if __name__ == "__main__":
    run()
