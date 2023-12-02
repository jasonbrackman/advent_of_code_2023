import re
from typing import List, Dict

GamesType = Dict[int, List[Dict[str, int]]]

pattern = re.compile(r"\d+")


def parse() -> GamesType:
    games: GamesType = dict()

    with open(r"./data/day02.txt", encoding="utf-8") as f:
        lines = [line.strip() for line in f.readlines()]
        for line in lines:
            num, values = line.split(":")
            bag = int(pattern.findall(num)[0])
            games[bag] = []
            for vals in values.split(";"):
                items = [v.strip().split() for v in vals.split(",")]
                game = {item[1]: int(item[0]) for item in items}
                games[bag].append(game)
    return games


def part01(games: GamesType) -> int:
    # rules: only 12 red cubes, 13 green cubes, and 14 blue cubes?
    rsults = []
    for game, rolls in games.items():
        good = True
        for roll in rolls:
            red = roll.get("red", 12)
            green = roll.get("green", 13)
            blue = roll.get("blue", 14)

            if not (red <= 12 and green <= 13 and blue <= 14):
                good = False
        if good:
            rsults.append(game)
    return sum(rsults)


def part02(games: GamesType) -> int:
    # rules are to find the power of maximum number of cubes needed
    results = []
    for game, rolls in games.items():
        red_max = max(roll.get("red", 1) for roll in rolls)
        green_max = max(roll.get("green", 1) for roll in rolls)
        blue_max = max(roll.get("blue", 1) for roll in rolls)

        results.append(red_max * green_max * blue_max)
    return sum(results)


def run() -> None:
    games = parse()
    assert part01(games) == 2685
    assert part02(games) == 83707


if __name__ == "__main__":
    run()
