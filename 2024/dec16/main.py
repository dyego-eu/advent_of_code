# https://adventofcode.com/2024/day/16

from copy import deepcopy
from pathlib import Path
from enum import Enum, auto
from dataclasses import dataclass
from typing import NamedTuple


class Type(Enum):
    wall = 0
    dead_end = 1
    corridor = 2
    crossroads = 3


class Direction(Enum):
    up = auto()
    down = auto()
    left = auto()
    right = auto()

    def __neg__(self):
        if self == Direction.up:
            return Direction.down
        if self == Direction.down:
            return Direction.up
        if self == Direction.left:
            return Direction.right
        if self == Direction.right:
            return Direction.left

    def __lt__(self, other):
        return self.value < other.value


@dataclass
class Tile:
    directions: list[Direction]

    @property
    def type(self) -> Type:
        if len(self.directions) >= 3:
            return Type.crossroads
        return Type(len(self.directions))


class Position(NamedTuple):
    x: int
    y: int


def read_map() -> tuple[Position, Position, list[list[Tile]]]:
    with open(Path(__file__).parent / "key.txt") as f:
        raw_map = f.read().strip().split("\n")

    map = []
    start = Position(0, 0)
    end = Position(0, 0)
    for y, raw_line in enumerate(raw_map):
        line = []
        for x, char in enumerate(raw_line):
            match char:
                case "#":
                    line.append(Tile([]))

                case _:
                    directions = []
                    if raw_map[y - 1][x] != "#":
                        directions.append(Direction.up)
                    if raw_map[y + 1][x] != "#":
                        directions.append(Direction.down)
                    if raw_map[y][x + 1] != "#":
                        directions.append(Direction.right)
                    if raw_map[y][x - 1] != "#":
                        directions.append(Direction.left)

                    line.append(Tile(directions))

                    if char == "S":
                        start = Position(x, y)
                    if char == "E":
                        end = Position(x, y)
        map.append(line)

    return start, end, map


def move(
    points: int, position: Position, direction: Direction, map: list[list[Tile]]
) -> list[tuple[int, Position, Direction]]:
    new_positions = []
    for map_dir in map[position.y][position.x].directions:
        match map_dir:
            case Direction.up:
                if direction == Direction.down:
                    continue
                new_positions.append(
                    (
                        points + (1001 if map_dir != direction else 1),
                        Position(position.x, position.y - 1),
                        Direction.up,
                    )
                )
            case Direction.down:
                if direction == Direction.up:
                    continue
                new_positions.append(
                    (
                        points + (1001 if map_dir != direction else 1),
                        Position(position.x, position.y + 1),
                        Direction.down,
                    )
                )
            case Direction.right:
                if direction == Direction.left:
                    continue
                new_positions.append(
                    (
                        points + (1001 if map_dir != direction else 1),
                        Position(position.x + 1, position.y),
                        Direction.right,
                    )
                )
            case Direction.left:
                if direction == Direction.right:
                    continue
                new_positions.append(
                    (
                        points + (1001 if map_dir != direction else 1),
                        Position(position.x - 1, position.y),
                        Direction.left,
                    )
                )
    return new_positions


def print_map(map):
    print("\n".join("".join(line) for line in map))


def print_path(map, path):
    new_map = deepcopy(map)
    for entry in path:
        new_map[entry.y][entry.x] = "*"
    print_map(new_map)


def main():
    start, end, map = read_map()

    position = start
    direction = Direction.right
    next_positions = [(0, start, direction, [start])]
    visited = {(start, direction): 0}
    best_paths = []
    best_points = float("inf")
    while next_positions:
        points, position, direction, path = next_positions.pop(0)
        new_position_tuples = move(points, position, direction, map)

        for new_points, new_position, new_direction in new_position_tuples:
            if new_points > best_points:
                continue
            if (new_position, new_direction) in visited and visited[
                (new_position, new_direction)
            ] < new_points:
                continue

            visited[(new_position, new_direction)] = new_points
            if new_position == end:
                if best_points == new_points:
                    best_paths.append(path + [new_position])
                elif new_points < best_points:
                    best_points = new_points
                    best_paths = [path + [new_position]]
            else:
                next_positions.append(
                    (
                        new_points,
                        new_position,
                        new_direction,
                        path + [new_position],
                    )
                )

    print(f"Part one: {best_points}")
    print(f"Part two: {len(set(sum(best_paths, [])))}")


if __name__ == "__main__":
    main()
