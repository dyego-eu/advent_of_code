# https://adventofcode.com/2023/day/12

from functools import cache
from pathlib import Path


def read_arrangements() -> list[tuple[str, list[int]]]:
    with open(Path(__file__).parent / "key.txt") as f:
        raw_arrangements = f.read().strip().split("\n")

    arrangement_keys = []

    for raw_arrangement in raw_arrangements:
        arrangement, raw_key = raw_arrangement.split(" ")
        key = [int(val) for val in raw_key.split(",")]
        arrangement_keys.append((arrangement, key))

    return arrangement_keys


def compute_all_arrangements(key: list[int], length: int) -> list[str]:
    if sum(key) + len(key) - 1 > length or length < 0:
        return []

    if length == 0:
        return [""]

    if len(key) == 0:
        return ["." * length]

    return [
        *[
            "#" * key[0] + "." * (1 if len(key) > 1 else 0) + arrangement
            for arrangement in compute_all_arrangements(
                key[1:], length - (key[0] + (1 if len(key) > 1 else 0))
            )
        ],
        *[
            "." + arrangement
            for arrangement in compute_all_arrangements(key, length - 1)
            if arrangement != ""
        ],
    ]


def test_possibility(possibility: str, arrangement: str):
    for char, key_char in zip(possibility, arrangement):
        if (char == "#" and key_char == ".") or (char == "." and key_char == "#"):
            return False
    return True


def count_arrangements(arrangement: str, key: list[int]) -> int:
    possible_arrangements = compute_all_arrangements(key, len(arrangement))

    arrangement_count = 0
    for possibility in possible_arrangements:
        arrangement_count += test_possibility(possibility, arrangement)
    return arrangement_count


def part_one(arrangement_keys: list[tuple[str, list[int]]]) -> int:
    sum = 0
    for arrangement, key in arrangement_keys:
        sum += count_arrangements(arrangement, key)

    return sum


def unfold(arrangement: str, key: list[int]) -> tuple[str, list[int]]:
    return ("?".join([arrangement for _ in range(5)]), sum([key for _ in range(5)], []))


@cache
def recursive_count_arrangements(
    arrangement: str, key: tuple[int, ...], current_count: int = 0
) -> int:
    if len(arrangement) == 0:
        # When you get to the end of the string, you need to have exhausted the key
        # and not be counting. This is why all strings must be terminated by a "."
        return not key and not current_count

    results = 0
    # This point is where you create a split-reality: When ? is found, you
    # recursively advance both with "#" and ".", effectively creating 2 parallel realities
    next_possible_chars = arrangement[0] if arrangement[0] != "?" else "#."

    for next_char in next_possible_chars:
        # Recursion advances characters in the list

        if next_char == "#":
            # When currently inspected character is #, advance arrangement
            # keep the key being inspected, and add +1 to the current count
            results += recursive_count_arrangements(
                arrangement[1:], key, current_count + 1
            )
        elif next_char == ".":
            # When currently inspected char is ".", there are 2 cases to inspect
            if current_count > 0:
                # If we had started a count, this is a count-stop. THis is where we
                # check that the count satisfied the key.
                #
                # If not, we won't don't keep looking in this possibility
                if len(key) > 0 and current_count == key[0]:
                    # If the count satisfied the key, we move to the next char
                    results += recursive_count_arrangements(arrangement[1:], key[1:], 0)

            elif current_count == 0:
                # If no count has yet started, simply move to next character
                results += recursive_count_arrangements(arrangement[1:], key, 0)

    return results


def part_two(arrangement_keys: list[tuple[str, list[int]]]):
    sum = 0
    for arrangement, key in arrangement_keys:
        unfold_arrangement, unfold_key = unfold(arrangement, key)
        count = recursive_count_arrangements(
            unfold_arrangement + ".", tuple(unfold_key)
        )
        sum += count

    return sum


def main():
    arrangement_keys = read_arrangements()
    print(part_one(arrangement_keys))
    print(part_two(arrangement_keys))


if __name__ == "__main__":
    main()
