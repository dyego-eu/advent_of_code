# https://adventofcode.com/2023/day/5

from pathlib import Path
from typing import NamedTuple


class MapRange(NamedTuple):
    start_dest: int
    start_source: int
    length: int


class Map(NamedTuple):
    name: str
    ranges: list[MapRange]


class SeedRange(NamedTuple):
    start: int
    length: int


def read_maps() -> tuple[list[int], list[Map]]:
    with open(Path(__file__).parent / "key.txt") as f:
        raw_maps = f.read().strip().split("\n\n")

    seeds = [int(val) for val in raw_maps[0].split(": ")[1].strip().split(" ")]

    maps = []
    for raw_map in raw_maps[1:]:
        map_name, map_contents = raw_map.split(":\n")

        ranges = []
        for raw_range in map_contents.strip().split("\n"):
            ranges.append(MapRange(*[int(val) for val in raw_range.split(" ")]))
        maps.append(Map(map_name, ranges))

    return seeds, maps


def part_one(seeds: list[int], maps: list[Map]) -> int:

    locations = []
    for seed in seeds:
        for map in maps:
            for map_range in map.ranges:
                if (
                    map_range.start_source
                    <= seed
                    < (map_range.start_source + map_range.length)
                ):
                    seed = seed - map_range.start_source + map_range.start_dest
                    break

        locations.append(seed)

    return min(locations)


def part_two(seeds: list[int], maps: list[Map]) -> int:
    seed_ranges = [SeedRange(*val) for val in zip(seeds[::2], seeds[1::2])]

    for map in maps:
        next_seed_ranges = []
        while seed_ranges:
            seed_range = seed_ranges.pop()
            allocated = False
            for map_range in map.ranges:
                if allocated:
                    break
                if (
                    map_range.start_source
                    <= seed_range.start
                    < (map_range.start_source + map_range.length)
                ):
                    if (seed_range.start + seed_range.length) <= (
                        map_range.start_source + map_range.length
                    ):
                        next_seed_ranges.append(
                            SeedRange(
                                seed_range.start
                                - map_range.start_source
                                + map_range.start_dest,
                                seed_range.length,
                            )
                        )
                        allocated = True
                    else:
                        next_seed_ranges.append(
                            SeedRange(
                                seed_range.start
                                - map_range.start_source
                                + map_range.start_dest,
                                map_range.start_source
                                + map_range.length
                                - seed_range.start,
                            )
                        )
                        seed_ranges.append(
                            SeedRange(
                                map_range.start_source + map_range.length,
                                seed_range.length
                                - (
                                    map_range.start_source
                                    + map_range.length
                                    - seed_range.start
                                ),
                            )
                        )
                        allocated = True
                elif (
                    map_range.start_source
                    < seed_range.start + seed_range.length
                    <= (map_range.start_source + map_range.length)
                ):
                    next_seed_ranges.append(
                        SeedRange(
                            map_range.start_dest,
                            seed_range.length
                            - (map_range.start_source - seed_range.start),
                        )
                    )
                    seed_ranges.append(
                        SeedRange(
                            seed_range.start,
                            map_range.start_source - seed_range.start,
                        )
                    )
                    allocated = True
                elif (
                    map_range.start_source + map_range.length <= seed_range.start
                ) or (seed_range.start + seed_range.length <= map_range.start_source):
                    continue
                else:
                    next_seed_ranges.append(
                        SeedRange(
                            map_range.start_dest,
                            map_range.length,
                        )
                    )
                    seed_ranges.append(
                        SeedRange(
                            seed_range.start,
                            map_range.start_source - seed_range.start,
                        )
                    )
                    seed_ranges.append(
                        SeedRange(
                            map_range.start_source + map_range.length,
                            seed_range.length
                            - map_range.length
                            - (map_range.start_source - seed_range.start),
                        )
                    )
                    allocated = True
            if not allocated:
                next_seed_ranges.append(seed_range)

        seed_ranges = next_seed_ranges

    return min([seed_range.start for seed_range in seed_ranges])


def main():
    seeds, maps = read_maps()
    print(part_one(seeds, maps))
    print(part_two(seeds, maps))


if __name__ == "__main__":
    main()
