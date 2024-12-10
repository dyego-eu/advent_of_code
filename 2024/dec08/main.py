# https://adventofcode.com/2024/day/8

from pathlib import Path
from itertools import combinations
from typing import NamedTuple


class Position(NamedTuple):
    x: int
    y: int


def read_antennae() -> tuple[dict[str, list[Position]], Position]:
    with open(Path(__file__).parent / "key.txt") as file:
        raw_map = file.read().strip().split("\n")

    antennae = {}
    for y, line in enumerate(raw_map):
        for x, char in enumerate(line):
            if char != ".":
                if char in antennae:
                    antennae[char].append(Position(x=x, y=y))
                else:
                    antennae[char] = [Position(x=x, y=y)]
    return antennae, Position(len(raw_map[0]), len(raw_map))


def find_antinodes(
    antenna1: Position, antenna2: Position, map_bounds: Position
) -> list[Position]:
    delta = Position(antenna1.x - antenna2.x, antenna1.y - antenna2.y)
    antinode1 = Position(antenna1.x + delta.x, antenna1.y + delta.y)
    antinode2 = Position(antenna2.x - delta.x, antenna2.y - delta.y)

    output = []
    if is_inside_map(antinode1, map_bounds):
        output.append(antinode1)

    if is_inside_map(antinode2, map_bounds):
        output.append(antinode2)

    return output


def is_inside_map(antenna: Position, map_bounds: Position):
    return (0 <= antenna.x < map_bounds.x) and (0 <= antenna.y < map_bounds.y)


def part_one(antennae: dict[str, list[Position]], map_bounds: Position) -> int:
    antinodes = set()

    for antennas in antennae.values():
        for antenna1, antenna2 in combinations(antennas, 2):
            antinodes.update(find_antinodes(antenna1, antenna2, map_bounds))

    return len(antinodes)


def find_interference_antinodes(
    antenna1: Position, antenna2: Position, map_bounds: Position
) -> list[Position]:
    delta = Position(antenna1.x - antenna2.x, antenna1.y - antenna2.y)

    antinodes = []

    antenna1_antinode = antenna1
    while is_inside_map(antenna1_antinode, map_bounds):
        antinodes.append(antenna1_antinode)
        antenna1_antinode = Position(
            antenna1_antinode.x + delta.x,
            antenna1_antinode.y + delta.y,
        )

    antenna2_antinode = antenna2
    while is_inside_map(antenna2_antinode, map_bounds):
        antinodes.append(antenna2_antinode)
        antenna2_antinode = Position(
            antenna2_antinode.x - delta.x,
            antenna2_antinode.y - delta.y,
        )

    return antinodes


def part_two(antennae: dict[str, list[Position]], map_bounds: Position) -> int:
    antinodes = set()

    for antennas in antennae.values():
        for antenna1, antenna2 in combinations(antennas, 2):
            antinodes.update(
                find_interference_antinodes(antenna1, antenna2, map_bounds)
            )

    return len(antinodes)


def main():
    antennae, map_bounds = read_antennae()
    print(part_one(antennae, map_bounds))
    print(part_two(antennae, map_bounds))


if __name__ == "__main__":
    main()
