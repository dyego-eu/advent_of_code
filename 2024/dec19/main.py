# https://adventofcode.com/2024/day/19

from tqdm import tqdm
from functools import cache
from pathlib import Path


def read_towels_and_patterns() -> tuple[list[str], list[str]]:
    with open(Path(__file__).parent / "key.txt") as f:
        raw_towels, raw_patterns = f.read().strip().split("\n\n")

    towels = raw_towels.split(", ")
    patterns = raw_patterns.split("\n")

    return towels, patterns


def can_fit(pattern: str, towels: list[str]) -> bool:
    if len(pattern) == 0:
        return True

    for towel in towels:
        if pattern.startswith(towel):
            if can_fit(pattern[len(towel) :], towels):
                return True
    return False


def renew_trie(trie, towels):
    for towel in towels:
        current = trie
        for char in towel:
            if char not in current:
                current[char] = {}
            current = current[char]

        current["*"] = True


def part_one(towels, patterns) -> int:

    found_patterns = 0
    for pattern in tqdm(patterns):
        trie = {}
        renew_trie(trie, towels)
        current = trie

        found_pattern = True
        for char in pattern:
            if "*" in current:
                renew_trie(current, towels)
            if char in current:
                current = current[char]
            else:
                found_pattern = False
                break

        if "*" in current and found_pattern:
            found_patterns += 1

    return found_patterns


@cache
def count_patterns(pattern, towels) -> int:
    if pattern == "":
        return 1
    count = 0
    for towel in towels:
        if pattern.startswith(towel):
            count += count_patterns(pattern[len(towel) :], towels)

    return count


def part_two(towels, patterns) -> int:
    count = 0
    for pattern in tqdm(patterns):
        count += count_patterns(pattern, towels)

    return count


def main():
    towels, patterns = read_towels_and_patterns()
    towels = tuple(towels)
    print(part_one(towels, patterns))
    print(part_two(towels, patterns))


if __name__ == "__main__":
    main()
