import re
from typing import List, Dict, Tuple

pattern = re.compile(r"(\d+)")

DataType = List[Tuple[List[int], List[int]]]


def parse() -> DataType:
    data = []
    with open(r"./data/day04.txt", encoding="utf-8") as f:
        for line in f.readlines():
            vals = line.strip().split(":")[1]
            winners, haves = vals.split("|")
            winners = [int(w) for w in winners.split()]
            haves = [int(h) for h in haves.split()]
            data.append((winners, haves))
    return data


def calc(num: int) -> int:
    t = 0
    c = 1
    for _ in range(num):
        t = c
        c += c
    return t


def part01(data: DataType) -> int:
    results = []
    for winners, haves in data:
        result = [have for have in haves if have in winners]
        results.append(calc(len(result)))
    return sum(results)


def part02(data: DataType) -> int:
    results: Dict[int, int] = dict()

    for index in range(1, len(data) + 1):
        results[index] = 1

    for idx, (winners, haves) in enumerate(data, 1):
        wins = sum(1 for winner in winners if winner in haves)
        for i in range(idx + 1, idx + wins + 1):
            if i <= len(data):
                results[i] += results[idx]

    return sum(results.values())


def run() -> None:
    data = parse()
    assert part01(data) == 20407
    assert part02(data) == 23806951


if __name__ == "__main__":
    run()
