def parse():
    with open(r"./data/day13.txt", "r", encoding="utf8") as handle:
        patterns = []

        current = []
        for line in handle:
            line = line.strip()
            if line:
                current.append(line)
            else:
                if current:
                    patterns.append(current[::])
                    current.clear()
        patterns.append(current)
    return patterns


def mirrored(pattern: list[str]) -> int:
    for index in range(1, len(pattern[0])):
        trigger = True
        for line in pattern:
            lhs = reversed(line[:index])
            rhs = line[index:]
            if not all(a == b for a, b in zip(lhs, rhs)):
                trigger = False
                break
        if trigger:
            return index
    return 0


def rotate_and_mirror(pattern: list[str]) -> list[str]:
    """
    The following could also be done with:
        ["".join(r) for r in list(zip(*pattern))]
    """
    results = []

    current = []
    for index in range(len(pattern[0])):
        for line in pattern:
            current.append(line[index])
        results.append(current[::])
        current.clear()

    if current:
        results.append(current)

    return ["".join(result) for result in results]


def part01() -> None:
    t = 0
    patterns = parse()
    for pattern in patterns:
        r1 = mirrored(pattern)
        if r1 != 0:
            t += r1
        else:
            rotated = rotate_and_mirror(pattern)
            r3 = mirrored(rotated)
            t += r3 * 100

    assert t == 31877


def run():
    part01()


if __name__ == "__main__":
    run()
