from pathlib import Path
from collections import Counter
from enum import IntEnum
from typing import NamedTuple


class Hand(NamedTuple):
    cards: str
    bid: int


class HandType(IntEnum):
    five_of_a_kind = 7
    four_of_a_kind = 6
    full_house = 5
    three_of_a_kind = 4
    two_pair = 3
    one_pair = 2
    high_card = 1


def read_hands() -> list[Hand]:
    with open(Path(__file__).parent / "key.txt") as file:
        raw_hands = file.read().strip().split("\n")

    hands = []
    for raw_hand in raw_hands:
        cards, raw_bid = raw_hand.split(" ")
        hands.append(Hand(cards, int(raw_bid)))

    return hands


def determine_type(cards: str) -> HandType:
    hand_counter = Counter(cards)
    if 5 in hand_counter.values():
        return HandType.five_of_a_kind
    if 4 in hand_counter.values():
        return HandType.four_of_a_kind
    if 3 in hand_counter.values() and 2 in hand_counter.values():
        return HandType.full_house
    if 3 in hand_counter.values():
        return HandType.three_of_a_kind
    if len([val for val in hand_counter.values() if val == 2]) == 2:
        return HandType.two_pair
    if 2 in hand_counter.values():
        return HandType.one_pair
    return HandType.high_card


def part_one(hands: list[Hand]) -> int:
    sorted_hands = []
    for hand in hands:
        sorted_hands.append(
            (
                determine_type(hand.cards),
                hand.cards.replace("A", "Z")
                .replace("K", "Y")
                .replace("Q", "X")
                .replace("J", "W")
                .replace("T", "V"),
                hand.bid,
            )
        )

    sorted_hands.sort()

    sum = 0
    for rank, (_, _, bid) in enumerate(sorted_hands, 1):
        sum += rank * bid

    return sum


def determine_type_joker_rule(cards: str) -> HandType:
    hand_counter = Counter(cards)

    n_jokers = 0
    if "J" in cards:
        n_jokers = hand_counter.pop("J")
        if n_jokers == 5:
            return HandType.five_of_a_kind

    highest_card = hand_counter.most_common(1)[0][0]
    hand_counter[highest_card] += n_jokers

    if 5 in hand_counter.values():
        return HandType.five_of_a_kind
    if 4 in hand_counter.values():
        return HandType.four_of_a_kind
    if 3 in hand_counter.values() and 2 in hand_counter.values():
        return HandType.full_house
    if 3 in hand_counter.values():
        return HandType.three_of_a_kind
    if len([val for val in hand_counter.values() if val == 2]) == 2:
        return HandType.two_pair
    if 2 in hand_counter.values():
        return HandType.one_pair
    return HandType.high_card


def part_two(hands: list[Hand]) -> int:
    sorted_hands = []
    for hand in hands:
        sorted_hands.append(
            (
                determine_type_joker_rule(hand.cards),
                hand.cards.replace("A", "Z")
                .replace("K", "Y")
                .replace("Q", "X")
                .replace("J", "0")
                .replace("T", "V"),
                hand.bid,
            )
        )

    sorted_hands.sort()

    print(sorted_hands)
    sum = 0
    for rank, (_, _, bid) in enumerate(sorted_hands, 1):
        sum += rank * bid

    return sum


def main():
    hands = read_hands()
    print(part_one(hands))
    print(part_two(hands))


if __name__ == "__main__":
    main()
