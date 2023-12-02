from typing import List


def part01(lines: List[str]) -> int:
    collection = []
    for line in lines:
        nums = [i for i in line if i.isdigit()]
        collection.append(int(nums[0] + nums[-1]))
    return sum(collection)


def part02(lines: List[str]) -> int:
    collection = []
    for line in lines:
        start = _find_num(line, False)
        end = _find_num(line, True)
        collection.append(int(start + end))

    return sum(collection)


def _find_num(line: str, reversed: bool) -> str:
    words = "one two three four five six seven eight nine".split()

    if reversed:
        line = line[::-1]

    new = ""
    for c in line:
        if c.isdigit():
            return c

        if reversed:
            new = c + new
        else:
            new += c

        for index, word in enumerate(words, 1):
            if word in new:
                return str(index)

    return ""


def run():
    with open(r"./data/day01.txt", encoding="utf-8") as f:
        lines = [line.strip() for line in f.readlines()]
    assert part01(lines) == 54708  # 1004th place
    assert part02(lines) == 54087


if __name__ == "__main__":
    run()
