from typing import List

Boat = tuple[int, int]


def simulate(boats: List[Boat]) -> int:
    """
    Based on existing boat race winners; calculate a 'margin of error'; a
    multiplier of all possible wins for each boat race.
    """
    results = 1
    for (time_ms, distance_mm) in boats:
        wins = 0
        for i in range(time_ms + 1):
            distance = i * (time_ms - i)
            if distance > distance_mm:
                wins += 1
        results *= wins

    return results


def run() -> None:
    """Run both parts of the day in one go."""
    p1: List[Boat] = [
        (58, 434),
        (81, 1041),
        (96, 2219),
        (76, 1218),
    ]

    p2: List[Boat] = [(58819676, 434104122191218)]
    assert simulate(p1) == 1159152
    assert simulate(p2) == 41513103


if __name__ == "__main__":
    run()
