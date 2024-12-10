# https://adventofcode.com/2023/day/6

import re
from math import sqrt, floor
from typing import NamedTuple
from pathlib import Path


class Race(NamedTuple):
    time: int
    distance: int


def read_races() -> list[Race]:
    with open(Path(__file__).parent / "key.txt") as file:
        raw_races = file.read().strip().split("\n")

    times = [int(val) for val in re.split(r"\s+", raw_races[0].split(":")[1].strip())]
    distances = [
        int(val) for val in re.split(r"\s+", raw_races[1].split(":")[1].strip())
    ]

    return [Race(time, distance) for time, distance in zip(times, distances)]


def read_corrected_race() -> Race:
    with open(Path(__file__).parent / "key.txt") as file:
        raw_races = file.read().strip().split("\n")

    time = int(raw_races[0].split(":")[1].strip().replace(" ", ""))
    distance = int(raw_races[1].split(":")[1].strip().replace(" ", ""))
    return Race(time, distance)


def part_one(races: list[Race]) -> int:
    prod = 1
    for race in races:
        n_wins = floor(
            (race.time + sqrt(race.time**2 - 4 * race.distance) - 1e-4) / 2
        ) - floor((race.time - sqrt(race.time**2 - 4 * race.distance) + 1e-4) / 2)

        prod *= n_wins

    return prod


def part_two(race: Race) -> int:
    n_wins = floor(
        (race.time + sqrt(race.time**2 - 4 * race.distance) - 1e-4) / 2
    ) - floor((race.time - sqrt(race.time**2 - 4 * race.distance) + 1e-4) / 2)

    return n_wins


def main():
    races = read_races()
    print(part_one(races))

    race = read_corrected_race()
    print(part_two(race))


if __name__ == "__main__":
    main()
