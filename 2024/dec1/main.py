# https://adventofcode.com/2024/day/1

from collections import defaultdict
from pathlib import Path


def read_lists() -> tuple[list[int], list[int]]:

    with open(Path(__file__).parent / "key.txt") as file:
        lists = [line.split("   ") for line in file.read().split("\n") if line.strip()]

    list_1 = [int(line[0]) for line in lists]
    list_2 = [int(line[1]) for line in lists]

    return list_1, list_2


def part_1(list_1: list[int], list_2: list[int]) -> int:
    sorted_list_1 = sorted(list_1)
    sorted_list_2 = sorted(list_2)

    return sum(abs(el1 - el2) for el1, el2 in zip(sorted_list_1, sorted_list_2))


def part_2(list_1: list[int], list_2: list[int]) -> int:
    processed_list_2 = defaultdict(int)
    for el in list_2:
        processed_list_2[el] += 1

    return sum([el * processed_list_2[el] for el in list_1])


def main():
    list_1, list_2 = read_lists()
    print(part_1(list_1, list_2))
    print(part_2(list_1, list_2))


if __name__ == "__main__":
    main()
