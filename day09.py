import re

digit = re.compile(r"-?\d+")

LinesType = list[list[int]]


def parse(path: str) -> LinesType:
    lines = []
    with open(path, "r", encoding="utf-8") as handle:
        for line in handle.readlines():
            lines.append([int(i) for i in digit.findall(line)])
    return lines


def reduction(nums: list[int]) -> list[list[int]]:
    history = [nums]
    while set(nums) != {0}:
        nums = [b - a for a, b in zip(nums, nums[1:])]
        history.append(nums)
    return history


def part01(lines: LinesType) -> None:
    total = 0
    for line in lines:
        reduced = reduction(line)
        total += sum(item[-1] for item in reduced)
    assert total == 1842168671


def part02(lines: LinesType) -> None:
    total = 0
    for line in lines:
        reduced = reduction(line)
        old = [item[0] for item in reduced]
        new = []
        current = 0
        while old:
            temp = old.pop()
            new.append(temp - current)
            current = temp - current

        total += new[-1]

    assert total == 903


def run() -> None:
    lines = parse(r"./data/day09.txt")
    part01(lines)
    part02(lines)


if __name__ == "__main__":
    run()
