MAGIC = 17


def parse() -> list[str]:
    with open(r'./data/day15.txt', encoding='utf8') as f:
        for line in f:
            return line.strip().split(',')
    raise ValueError('no data')


def word_hash(data: list[str]) -> int:
    results = []
    for d in data:
        val = 0
        for r in d:
            val = (val + ord(r)) * MAGIC % 256
        results.append(val)
    return sum(results)


def part01() -> None:
    data = parse()
    assert word_hash(data) == 502139


def run() -> None:
    part01()
    # part02()


if __name__ == '__main__':
    run()
