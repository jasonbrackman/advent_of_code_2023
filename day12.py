import re
from functools import cache

RecordType = str
RulesType = tuple[int]
RecordDataType = tuple[RecordType, RulesType]

pattern = re.compile(r'(#+)')


def parse() -> RecordDataType:
    records = []
    with open(r"./data/day12.txt", encoding="utf-8") as handle:
        for line in handle:
            record, nums_ = line.strip().split()
            nums = tuple(int(i) for i in nums_.split(","))
            records.append((record, nums))
    return records


@cache
def eat_record(record: RecordType, rules: RulesType) -> int:
    """Using DP, eat away at the record until the record and rules are used up."""
    if not record:
        return 1 if not rules else 0
    if not rules:
        return 0 if '#' in record else 1

    current, rest = record[0], record[1:]

    if current == ".":
        return eat_record(rest, rules)

    if current == "#":
        rule = rules[0]
        if ('.' not in record[:rule] and
                len(record[:rule]) == rule and
                record[rule:].startswith('#') is False):
            return eat_record(record[rule + 1:], rules[1:])
        return 0

    if current == '?':
        return eat_record(f'#{rest}', rules) + eat_record(f'.{rest}', rules)

    raise ValueError(f"Unknown character encountered: {current}")


def part01(data: RecordDataType):
    t = 0
    for (record, rules) in data:
        r = eat_record(record, rules)
        t += r
    assert t == 7599


def part02(data: RecordDataType):
    """Problem was actually folded into 5 parts -- so it's a much larger dataset."""
    t = 0
    for record, rules in data:
        record = '?'.join([record] * 5)
        t += eat_record(record, rules * 5)
    assert t == 15454556629917


def run() -> None:
    data = parse()
    part01(data)
    part02(data)


if __name__ == "__main__":
    run()
