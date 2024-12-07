# https://adventofcode.com/2023/day/11

from pathlib import Path
from itertools import combinations
from dataclasses import dataclass


@dataclass
class Position:
    x: int
    y: int


def read_galaxies() -> tuple[list[Position], list[int], list[int]]:
    with open(Path(__file__).parent / "key.txt") as file:
        galaxy = [[char for char in line] for line in file.read().strip().split("\n")]

    N = len(galaxy)
    M = len(galaxy[0])

    expansion_rows = []
    for i in range(N):
        if all(char == "." for char in galaxy[i]):
            expansion_rows.append(i)

    expansion_cols = []
    for j in range(M):
        if all(char == "." for char in [line[j] for line in galaxy]):
            expansion_cols.append(j)

    positions = []
    for i in range(N):
        for j in range(M):
            if galaxy[i][j] == "#":
                positions.append(Position(j, i))

    return positions, expansion_rows, expansion_cols


def compute_distance(
    pos1: Position,
    pos2: Position,
    expansion_rows: list[int],
    expansion_cols: list[int],
    multiplier: int = 1,
) -> int:
    n_expansions_x = len(
        [
            val
            for val in expansion_cols
            if ((pos1.x < val < pos2.x) or (pos2.x < val < pos1.x))
        ]
    )
    n_expansions_y = len(
        [
            val
            for val in expansion_rows
            if ((pos1.y < val < pos2.y) or (pos2.y < val < pos1.y))
        ]
    )
    return (
        abs(pos1.x - pos2.x)
        + n_expansions_x * multiplier
        + abs(pos1.y - pos2.y)
        + n_expansions_y * multiplier
    )


def part_one(
    positions: list[Position], expansion_rows: list[int], expansion_cols: list[int]
) -> int:
    sum = 0

    for pos1, pos2 in combinations(positions, 2):
        distance = compute_distance(pos1, pos2, expansion_rows, expansion_cols)
        sum += distance

    return sum


def part_two(
    positions: list[Position], expansion_rows: list[int], expansion_cols: list[int]
) -> int:
    sum = 0
    for pos1, pos2 in combinations(positions, 2):
        distance = compute_distance(
            pos1, pos2, expansion_rows, expansion_cols, multiplier=1_000_000 - 1
        )
        sum += distance

    return sum


def main():
    positions, expansion_rows, expansion_cols = read_galaxies()
    print(part_one(positions, expansion_rows, expansion_cols))
    print(part_two(positions, expansion_rows, expansion_cols))


if __name__ == "__main__":
    main()
