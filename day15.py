import re
from collections import defaultdict

MAGIC = 17
PATTERN = re.compile(r'([=-])')


def parse(s: str) -> list[str]:
    with open(s, encoding='utf8') as f:
        line = f.read()
    return line.strip().split(',')


def _hash(word: str) -> int:
    val = 0
    for r in word:
        val = (val + ord(r)) * MAGIC % 256
    return val


def hash_words(data: list[str]) -> int:
    """Hash a list of words and sum the results."""
    results = []
    for d in data:
        val = _hash(d)
        results.append(val)
    return sum(results)


def _in_boxes(box: list[tuple[str, int]], label: str) -> bool:
    for index, item in enumerate(box):
        if item[0] == label:
            return index
    return -1


def part01() -> None:
    data = parse(r'./data/day15.txt')
    assert hash_words(data) == 502139


def part02() -> None:
    boxes = defaultdict(list)
    data = parse(r'./data/day15.txt')
    for d in data:
        label, op, *val = PATTERN.split(d)
        hash_ = _hash(label)
        if op == '=':
            index = _in_boxes(boxes[hash_], label)
            if index == -1:
                boxes[hash_].append((label, int(val[0])))
            else:
                boxes[hash_][index] = (label, int(val[0]))

        else:
            # op must be a '-'
            index = _in_boxes(boxes[hash_], label)
            if index == -1:
                continue
            boxes[hash_] = boxes[hash_][:index] + boxes[hash_][index + 1:]

    # calc result
    t = 0
    for k, v in boxes.items():
        for slot, item in enumerate(v, 1):
            #    slot * focal_length * box_number
            #    \      \              /
            t += slot * item[1] * (k + 1)
    assert t == 284132


def run() -> None:
    part01()
    part02()


if __name__ == '__main__':
    run()
