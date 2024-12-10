# https://adventofcode.com/2023/day/1

import re
from pathlib import Path


def read_key() -> list[str]:
    with open(Path(__file__).parent / "key.txt") as file:
        return file.read().strip().split("\n")


def part_one(lines: list[str]) -> int:
    first_digit = re.compile(r"^\D*(\d)")
    last_digit = re.compile(r".*(\d)\D*$")
    sum = 0
    for line in lines:
        dig1 = int(first_digit.match(line)[1]) * 10
        dig2 = int(last_digit.match(line)[1])

        number = dig1 + dig2

        sum += number

    return sum


def part_two(lines: list[str]) -> int:
    numbers = {
        1: r"one",
        2: r"two",
        3: r"three",
        4: r"four",
        5: r"five",
        6: r"six",
        7: r"seven",
        8: r"eight",
        9: r"nine",
        0: r"zero",
    }

    re_first_digit = re.compile(r"^\D*?(\d)")
    re_last_digit = re.compile(r".*(\d)\D*?$")

    sum = 0
    for line in lines:
        current_match = re_first_digit.match(line)
        first_digit = int(current_match[1])
        for dig, code in numbers.items():
            match = re.match(rf"^.*?({code})", line)

            if match and (
                not current_match or match.span(1)[0] < current_match.span(1)[0]
            ):
                current_match = match
                first_digit = dig

        current_match = re_last_digit.match(line)
        last_digit = int(current_match[1])
        for dig, code in numbers.items():
            match = re.match(rf".*({code}).*?$", line)
            if match and (
                not current_match or match.span(1)[1] > current_match.span(1)[1]
            ):
                current_match = match
                last_digit = dig

        number = 10 * first_digit + last_digit
        sum += number

    return sum


def main():
    lines = read_key()
    print(part_one(lines))

    lines = read_key()
    print(part_two(lines))


if __name__ == "__main__":
    main()
