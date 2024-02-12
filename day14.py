def parse(s: str) -> list[str]:
    results = []
    with open(s, encoding="utf8") as lines:
        for line in lines:
            results.append(line.strip())
    return results


def shunt_right(pattern):
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
    results = parse(r"./data/day14t.txt")
    seen = [
        # frozenset(results),
    ]
    index = 0
    rotations = 1_000_000_000
    while index < rotations:
        print(index)
        results = shunt_right(results)
        if frozenset(results) in seen:
            # let's fast-forward the index
            first = seen.index(frozenset(results))  # zero indexed
            new_index = (rotations - index) % (index - first)
            # print(index, "->", rotations - new_index)
            index = rotations - new_index
            seen.clear()
            # for i in range((rotations - index) % (index - first)):
            #     results = shunt_right(results)
            # break
        else:
            seen.append(frozenset(results))
            index += 1
    for _ in range(4):
        # print("-" * 10)
        calc_value(results)
        # for r in results:
        #     print(r)
        # print("-" * 10)
        results = ["".join(r)[::-1] for r in list(zip(*results))]


def calc_value(results):
    t = 0
    for result in results:
        for val, c in enumerate(result, 1):
            if c == "O":
                t += val
    print(t)


def run():
    part01()
    part02()  #  86453 too low
              # 112472 too high


if __name__ == "__main__":
    run()
