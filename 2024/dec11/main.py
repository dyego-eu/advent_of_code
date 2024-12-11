# https://adventofcode.com/2024/day/11

from pathlib import Path
from functools import cache
from collections import Counter
from tqdm import tqdm


def read_stones():
    with open(Path(__file__).parent / "key.txt") as file:
        stones = file.read().strip().split(" ")

    return stones


def apply_rules(stone: str) -> list[str]:
    if stone == "0":
        return ["1"]

    N = len(stone)
    if N % 2 == 0:
        return [f"{int(stone[:N//2])}", f"{int(stone[N//2:])}"]

    return [f"{int(stone) * 2024}"]


@cache
def apply_5_steps(stone: str, count: int) -> dict[str, int]:
    stones = [stone]
    for _ in range(5):
        stones = sum([apply_rules(stone) for stone in stones], [])
    counter = Counter(stones)

    for stone in counter:
        counter[stone] *= count

    return counter


def part_one(stones: list[str]) -> int:
    counter = Counter(stones)

    for _ in tqdm(range(5)):
        new_counter = Counter()

        for stone, count in counter.items():
            new_counter += apply_5_steps(stone, count)

        counter = new_counter

    return sum(counter.values())


def part_two(stones: list[str]) -> int:
    counter = Counter(stones)
    for _ in tqdm(range(15)):
        new_counter = Counter()

        for stone, count in counter.items():
            new_counter += apply_5_steps(stone, count)

        counter = new_counter

    return sum(counter.values())


def main():
    stones = read_stones()
    print(part_one(stones))
    print(part_two(stones))


if __name__ == "__main__":
    main()
