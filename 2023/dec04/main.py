# https://adventofcode.com/2023/day/4

import re
from typing import NamedTuple
from pathlib import Path


class Card(NamedTuple):
    sampled_numbers: list[int]
    my_numbers: list[int]


def read_cards() -> list[Card]:
    with open(Path(__file__).parent / "key.txt") as f:
        raw_cards = f.read().strip().split("\n")

    cards = []
    for raw_card in raw_cards:
        deheaded = raw_card.split(":", 1)[1]
        raw_sampled, raw_mine = deheaded.split(" | ", 1)

        sampled_numbers = [
            int(number) for number in re.split(r"\s+", raw_sampled.strip())
        ]
        my_numbers = [int(number) for number in re.split(r"\s+", raw_mine.strip())]

        cards.append(Card(my_numbers=my_numbers, sampled_numbers=sampled_numbers))

    return cards


def part_one(cards: list[Card]):
    sum = 0
    for card in cards:
        common_numbers = set(card.sampled_numbers).intersection(card.my_numbers)
        if not common_numbers:
            continue
        sum += 2 ** (len(common_numbers) - 1)

    return sum


def part_two(cards: list[Card]):
    n_copies = [1] * len(cards)

    for idx, card in enumerate(cards, 1):
        common_numbers = set(card.sampled_numbers).intersection(card.my_numbers)

        for i in range(idx, idx + len(common_numbers)):
            try:
                n_copies[i] += n_copies[idx - 1]
            except Exception:
                print(i, idx)

    return sum(n_copies)


def main():
    cards = read_cards()
    print(part_one(cards))
    print(part_two(cards))


if __name__ == "__main__":
    main()
