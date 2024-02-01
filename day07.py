from collections import Counter
from typing import Dict, List

Hand = list[tuple[str, int]]


def parse(path: str) -> Hand:
    """
    Parse a file containing a list of hands, one per line.
    """
    results = []
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            items = line.split(' ')
            results.append((items[0], int(items[1].strip())))

    return results


def convert_to_nums(cards: str, part2=False) -> tuple[int, ...]:
    """
    For the purposes of sorting, convert a hand to a tuple of numbers.
    """
    hm = {
        'A': 14,
        'K': 13,
        'Q': 12,
        'J': 11,
        'T': 10,
        '9': 9,
        '8': 8,
        '7': 7,
        '6': 6,
        '5': 5,
        '4': 4,
        '3': 3,
        '2': 2,

    }
    if part2 is True:
        hm['J'] = 1

    return tuple(hm.get(item, ord(item)) for item in cards)


def rank_hand(hand: str) -> int:
    """Return the rank of a hand.  Higher is stronger"""
    counts = Counter(hand)

    if len(counts) == 1:
        # Five of a kind
        return 6

    if 4 in counts.values():
        # Four of a kind
        return 5

    if 3 in counts.values():
        if len(counts) == 2:
            # Full house
            return 4

        # Three of a kind
        return 3

    if 2 in counts.values():
        if len(counts) == 3:
            # Two pair
            return 2
        # One pair
        return 1

    # High card
    return 0


def upgrade_hand(cards: str) -> str:
    """
    Upgrade a hand to a better hand, if possible.
    """
    # Return early if no Jokers or all Jokers present in the hand
    if "J" not in cards or set(cards) == {"J"}:
        return cards

    counts = Counter(cards.replace("J", ""))
    target = counts.most_common(1)[0][0]
    return cards.replace("J", target)


def get_ranked_results(jokers_wild=False) -> Dict[int, List[Hand]]:
    """Get the ranked results of the cards collected."""
    ranked_results: Dict[int, List[Hand]] = {}
    for hand in parse(r"./data/day07.txt"):
        new = upgrade_hand(hand[0]) if jokers_wild else hand[0]

        rank = rank_hand(new)

        if rank not in ranked_results:
            ranked_results[rank] = [hand]
        else:
            ranked_results[rank].append(hand)
    return ranked_results


def part01() -> None:
    """Solution for part01"""
    ranked_results = get_ranked_results(jokers_wild=False)

    final = []
    for _, v in sorted(ranked_results.items()):
        final += sorted(v, key=lambda x: convert_to_nums(x[0]))

    total = 0
    for index, hand in enumerate(final, 1):
        total += index * hand[1]

    assert total == 246409899


def part02() -> None:
    """Solution for part02"""
    ranked_results = get_ranked_results(jokers_wild=True)

    final = []
    for _, v in sorted(ranked_results.items()):
        # note the part2 flag
        s = sorted(v, key=lambda x: convert_to_nums(x[0], part2=True))
        final += s

    total = 0
    for index, hand in enumerate(final, 1):
        total += index * hand[1]
    assert total == 244848487


def run() -> None:
    part01()
    part02()


if __name__ == "__main__":
    run()
