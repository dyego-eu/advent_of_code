# https://adventofcode.com/2024/day/6

import re
from pathlib import Path
from typing import NamedTuple
from enum import Enum, auto
from tqdm import tqdm


class Position(NamedTuple):
    x: int
    y: int


class Direction(Enum):
    up = auto()
    down = auto()
    left = auto()
    right = auto()


def read_map() -> tuple[Position, list[Position], Position]:
    with open(Path(__file__).parent / "key.txt") as f:
        raw_map_lines = f.read().strip().split("\n")

    obstacles: list[Position] = []
    guard = Position(0, 0)
    guard_re = re.compile(r"\^")
    obstacle_re = re.compile(r"#")

    max_y = len(raw_map_lines)
    max_x = len(raw_map_lines[0])
    map_dimensions = Position(max_x, max_y)

    for y, raw_map_line in enumerate(raw_map_lines):
        x = -1
        guard_match = guard_re.search(raw_map_line)

        if guard_match is not None:
            guard = Position(guard_match.span()[0], y)

        while True:
            obstacle_match = obstacle_re.search(raw_map_line, x + 1)

            if obstacle_match is None:
                break

            x = obstacle_match.span()[0]

            obstacles.append(Position(x, y))

    return guard, obstacles, map_dimensions


def next_position(
    guard: Position, obstacles: list[Position], direction: Direction
) -> tuple[Position, Direction]:
    match direction:
        case Direction.up:
            if Position(guard.x, guard.y - 1) in obstacles:
                direction = Direction.right
            else:
                guard = Position(guard.x, guard.y - 1)
        case Direction.down:
            if Position(guard.x, guard.y + 1) in obstacles:
                direction = Direction.left
            else:
                guard = Position(guard.x, guard.y + 1)
        case Direction.right:
            if Position(guard.x + 1, guard.y) in obstacles:
                direction = Direction.down
            else:
                guard = Position(guard.x + 1, guard.y)
        case Direction.left:
            if Position(guard.x - 1, guard.y) in obstacles:
                direction = Direction.up
            else:
                guard = Position(guard.x - 1, guard.y)

    return guard, direction


def is_out_of_bounds(guard: Position, map_dimensions: Position) -> bool:
    return (
        (guard.x < 0)
        or (guard.y < 0)
        or (guard.x >= map_dimensions.x)
        or (guard.y >= map_dimensions.y)
    )


def part_one(
    guard: Position, obstacles: list[Position], map_dimensions: Position
) -> set[Position]:
    visited = set()
    direction = Direction.up

    while True:
        visited.add(guard)
        guard, direction = next_position(guard, obstacles, direction)
        if is_out_of_bounds(guard, map_dimensions):
            break

    return visited


def gets_stuck_in_loop(
    guard: Position,
    obstacles: list[Position],
    map_dimensions: Position,
    added_obstacle: Position,
) -> bool:
    visited = set()
    direction = Direction.up
    new_obstacles = [*obstacles, added_obstacle]
    while True:
        visited.add((guard, direction))
        guard, direction = next_position(guard, new_obstacles, direction)
        if (guard, direction) in visited:
            return True
        if is_out_of_bounds(guard, map_dimensions):
            return False


def part_two(
    guard: Position,
    obstacles: list[Position],
    map_dimensions: Position,
    visited: set[Position],
):
    n_works = 0
    for added_obstacle in tqdm(visited):
        if (added_obstacle.x == guard.x) and (added_obstacle.y == guard.y):
            continue

        if gets_stuck_in_loop(guard, obstacles, map_dimensions, added_obstacle):
            n_works += 1

    return n_works


def main():
    guard, obstacles, map_dimensions = read_map()
    visited = part_one(guard, obstacles, map_dimensions)
    print(len(visited))

    print(part_two(guard, obstacles, map_dimensions, visited))


if __name__ == "__main__":
    main()
