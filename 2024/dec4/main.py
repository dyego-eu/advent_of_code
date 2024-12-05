# https://adventofcode.com/2024/day/4

import re
from pathlib import Path


def read_wordsearch() -> list[str]:
    with open(Path(__file__).parent / "key.txt") as f:
        wordsearch = f.read().strip().split("\n")
    return wordsearch


def part_one(wordsearch):

    N = len(wordsearch)
    LL = len(wordsearch[0])

    sum = 0
    x_re = re.compile("X")

    for y, line in enumerate(wordsearch):
        x = -1
        while True:
            match = x_re.search(line, x + 1)
            if match is None:
                break
            x = match.span()[0]

            directions = [
                line[x : x + 4],
                line[max(x - 3, 0) : x + 1][::-1],
            ]

            if y >= 3:
                directions.append(
                    line[x]
                    + wordsearch[y - 1][x]
                    + wordsearch[y - 2][x]
                    + wordsearch[y - 3][x]
                )
                if x >= 3:
                    directions.append(
                        line[x]
                        + wordsearch[y - 1][x - 1]
                        + wordsearch[y - 2][x - 2]
                        + wordsearch[y - 3][x - 3]
                    )
                if x < LL - 3:
                    directions.append(
                        line[x]
                        + wordsearch[y - 1][x + 1]
                        + wordsearch[y - 2][x + 2]
                        + wordsearch[y - 3][x + 3]
                    )
            if y < N - 3:
                directions.append(
                    line[x]
                    + wordsearch[y + 1][x]
                    + wordsearch[y + 2][x]
                    + wordsearch[y + 3][x]
                )
                if x >= 3:
                    directions.append(
                        line[x]
                        + wordsearch[y + 1][x - 1]
                        + wordsearch[y + 2][x - 2]
                        + wordsearch[y + 3][x - 3]
                    )
                if x < LL - 3:
                    directions.append(
                        line[x]
                        + wordsearch[y + 1][x + 1]
                        + wordsearch[y + 2][x + 2]
                        + wordsearch[y + 3][x + 3]
                    )

            sum += len([word for word in directions if word == "XMAS"])

    return sum


def part_two(wordsearch: list[str]) -> int:
    a_re = re.compile("A")

    N = len(wordsearch)
    LL = len(wordsearch[0])

    sum = 0

    for y, line in enumerate(wordsearch[1 : N - 1], 1):
        x = -1
        while True:
            match = a_re.search(line, x + 1)

            if match is None:
                break

            x = match.span()[0]

            if x == LL - 1:
                break

            forward_slash = (
                (wordsearch[y - 1][x - 1] == "M") and (wordsearch[y + 1][x + 1] == "S")
            ) or (
                (wordsearch[y - 1][x - 1] == "S") and (wordsearch[y + 1][x + 1] == "M")
            )
            backward_slash = (
                (wordsearch[y - 1][x + 1] == "M") and (wordsearch[y + 1][x - 1] == "S")
            ) or (
                (wordsearch[y - 1][x + 1] == "S") and (wordsearch[y + 1][x - 1] == "M")
            )

            sum += forward_slash and backward_slash

    return sum


def main():
    wordsearch = read_wordsearch()
    print(part_one(wordsearch))
    print(part_two(wordsearch))


if __name__ == "__main__":
    main()
