import math
import re
from typing import Iterator

pattern = re.compile(r"\w+")


def parse() -> (Iterator[int], dict[str, tuple[str, str]]):
    rules: list[int] = []
    hm: dict[str, tuple[str, str]] = dict()
    with open(r"./data/day08.txt", "r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue

            if "=" in line:
                a, b, c = pattern.findall(line)
                hm[a] = (b, c)
            else:
                for c in line:
                    rules.append(1 if c == "R" else 0)

    return cycle_rules(rules), hm


def cycle_rules(rules):
    while True:
        for rule in rules:
            yield rule


def part01():
    rules, hm = parse()

    counter = 0
    result = "AAA"
    while result != "ZZZ":
        result = hm[result][next(rules)]
        counter += 1
    assert counter == 11309


def part02():
    """Brute force checking of every item could take a very-very long time.
    By treating the numbers as a set of individual tumblers that repeat a solution
    means we only have to find each of the first repeats and then find the
    lowest common multiplier."""
    rules, hm = parse()
    common = []
    for result in [s for s in hm.keys() if s.endswith("A")]:
        counter = 0
        results = [result]
        while not all([s.endswith("Z") for s in results]):
            index = next(rules)
            results = [hm[result][index] for result in results]
            counter += 1

        common.append(counter)

    assert math.lcm(*common) == 13740108158591


def run():
    part01()
    part02()


if __name__ == "__main__":
    run()
