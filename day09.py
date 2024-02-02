import re

digit = re.compile(r"-?\d+")


def parse(path: str) -> list[list[int]]:
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


def part01() -> None:
    lines = parse(r"./data/day09.txt")
    t = 0
    for line in lines:
        h = reduction(line)
        t += sum(item[-1] for item in h)
    assert t == 1842168671


def run() -> None:
    part01()


# def new_sub(a: int, b: int) -> int:
#     return a - b
#
#
# def part02():
#     lines = parse(r"./data/day09t.txt")
#     t = 0
#     for line in lines:
#         h = reduction(line)
#         n = [item[0] for item in h][::-1]
#         print(n)
#         for a, b in zip(n, n[1:]):
#             print(a, b, new_sub(a, b))
#             t += new_sub(a, b)
#     print(t)
#
#
# part02()


if __name__ == "__main__":
    run()
