def parse(s: str) -> list[str]:
    """Parse the input file for a list of strings."""
    results = []
    with open(s, encoding="utf8") as lines:
        for line in lines:
            results.append(line.strip())
    return results


def shunt_right(pattern: list[str]) -> list[str]:
    """Rotate to the right and move all the mirrors to the right."""
    rotated = ["".join(r)[::-1] for r in list(zip(*pattern))]
    results = []
    for line in rotated:
        new = ""
        last = 0
        for index, c in enumerate(line[::]):
            if c == "#":
                new += "".join(sorted(line[last:index]))
                last = index
        new += "".join(sorted(line[last:]))
        results.append(new)
    return results


def _calc_value(results: list[str]) -> int:
    # convenience: rotate to the side for easier calculations
    results = ["".join(r)[::-1] for r in list(zip(*results))]
    t = 0
    for result in results:
        for val, c in enumerate(result, 1):
            if c == "O":
                t += val
    return t


def part01():
    pattern = parse(r"./data/day14.txt")

    results = shunt_right(pattern)
    t = 0
    for result in results:
        for val, c in enumerate(result, 1):
            if c == "O":
                t += val
    assert t == 112046


def part02():
    results = parse(r"./data/day14.txt")
    seen = []

    index = 0
    rotations = 1_000_000_000

    # not sure why I had to add the -1 here.  But it was necessary
    # for the test data.  When running against actual input the
    # answer was accepted.
    while index < rotations - 1:
        # cycle is a full spin
        for _ in range(4):
            results = shunt_right(results)

        hashable_results = frozenset(results)
        if hashable_results in seen:
            # let's fast-forward the index
            first = seen.index(hashable_results)
            new_index = (rotations - first) % (index - first)
            index = rotations - new_index
            seen.clear()
        else:
            seen.append(hashable_results)
            index += 1

    assert _calc_value(results) == 104619


def run() -> None:
    part01()
    part02()


if __name__ == "__main__":
    run()
