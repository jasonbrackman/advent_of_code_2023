def parse() -> list[tuple[str, list[int]]]:
    records = []
    with open(r"./data/day12t.txt", encoding="utf-8") as handle:
        for line in handle:
            record, nums = line.strip().split()
            nums = [int(i) for i in nums.split(",")]
            records.append((record, nums))
    return records


records = parse()
for record in records:
    print(record)
