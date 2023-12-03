import re
from typing import List, Dict, Tuple

pattern = re.compile(r"(\d+)+")


def parse() -> List[str]:
    with open(r"./data/day03.txt", encoding="utf-8") as f:
        lines = [line.strip() for line in f.readlines()]
    return lines


def part01(lines: List[str]) -> int:
    valid = "0123456789."
    max_line_length = len(lines[0])

    results = []

    for count, line in enumerate(lines):
        for num in pattern.finditer(line):
            good_num = False

            # now walk the index to the length of the num
            walk_min = max(0, num.span()[0] - 1)
            walk_max = num.span()[1]

            for c in range(walk_min, walk_max + 1):
                # exit early if possible
                if good_num:
                    break

                # Ensure we don't walk over the edge
                if c < max_line_length:
                    # check same line
                    if lines[count][c] not in valid:
                        good_num = True

                    # can't go before start
                    if count - 1 >= 0:
                        if lines[count - 1][c] not in valid:
                            good_num = True

                    # can't go after end
                    if count + 1 <= len(lines) - 1:
                        if lines[count + 1][c] not in valid:
                            good_num = True

            if good_num:
                results.append(int(num.group()))

    return sum(results)


def part02(lines: List[str]) -> int:
    shared: Dict[Tuple[int, int], List[int]] = dict()

    for count, line in enumerate(lines):
        for num in pattern.finditer(line):
            val = int(num.group())

            walk_min = max(0, num.span()[0] - 1)
            walk_max = num.span()[1]

            for c in range(walk_min, walk_max + 1):
                if c < len(lines[count]):
                    # same line
                    if lines[count][c] == "*":
                        if (count, c) not in shared:
                            shared[(count, c)] = []
                        shared[(count, c)].append(val)

                    # can't go before start
                    if count - 1 >= 0:
                        if lines[count - 1][c] == "*":
                            if (count - 1, c) not in shared:
                                shared[(count - 1, c)] = []
                            shared[(count - 1, c)].append(val)

                    # can't go after end
                    if count + 1 <= len(lines) - 1:
                        if lines[count + 1][c] == "*":
                            if (count + 1, c) not in shared:
                                shared[(count + 1, c)] = []
                            shared[(count + 1, c)].append(val)

    # calc total
    t = 0
    for k, v in shared.items():
        if len(v) == 2:
            t += v[0] * v[1]
    return t


def run():
    lines = parse()
    assert part01(lines) == 550934
    assert part02(lines) == 81997870


if __name__ == "__main__":
    run()
