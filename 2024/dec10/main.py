# https://adventofcode.com/2024/day/10

from pathlib import Path
from enum import Enum, auto
from typing import NamedTuple


class Direction(Enum):
    up = auto()
    down = auto()
    left = auto()
    right = auto()


Map = list[list[list[Direction]]]


class Position(NamedTuple):
    x: int
    y: int


def read_map() -> tuple[Map, list[Position], list[Position]]:
    with open(Path(__file__).parent / "key.txt") as f:
        raw_map = f.read().strip().split("\n")

    N = len(raw_map)
    LL = len(raw_map[0])

    trail_heads = []
    success = []
    map = []
    for y, line in enumerate(raw_map):
        map_line = []
        for x, char in enumerate(line):
            if char == "0":
                trail_heads.append(Position(x, y))
            if char == "9":
                success.append(Position(x, y))

            directions = []
            if y > 0 and int(char) + 1 == int(raw_map[y - 1][x]):
                directions.append(Direction.up)
            if y < N - 1:
                if int(char) + 1 == int(raw_map[y + 1][x]):
                    directions.append(Direction.down)
            if x > 0 and int(char) + 1 == int(line[x - 1]):
                directions.append(Direction.left)
            if x < LL - 1 and int(char) + 1 == int(line[x + 1]):
                directions.append(Direction.right)
            map_line.append(directions)
        map.append(map_line)

    return map, trail_heads, success


def step(position: Position, map: Map) -> list[Position]:
    current_directions = map[position.y][position.x]
    output = []
    for direction in current_directions:
        match direction:
            case Direction.up:
                output.append(Position(position.x, position.y - 1))
            case Direction.down:
                output.append(Position(position.x, position.y + 1))
            case Direction.left:
                output.append(Position(position.x - 1, position.y))
            case Direction.right:
                output.append(Position(position.x + 1, position.y))

    return output


def part_one(map, trail_heads, success) -> int:
    sum = 0
    for trail_head in trail_heads:
        position_queue = [trail_head]

        successes = set()
        while position_queue:
            cur_position = position_queue.pop(0)
            if cur_position in success:
                successes.add(cur_position)
            else:
                position_queue.extend(step(cur_position, map))

        sum += len(successes)

    return sum


def part_two(map, trail_heads, success) -> int:
    sum = 0
    for trail_head in trail_heads:
        position_queue = [trail_head]

        score = 0
        while position_queue:
            cur_position = position_queue.pop(0)
            if cur_position in success:
                score += 1
            else:
                position_queue.extend(step(cur_position, map))

        sum += score

    return sum


def main():
    map, trail_heads, success = read_map()
    print(part_one(map, trail_heads, success))
    print(part_two(map, trail_heads, success))


if __name__ == "__main__":
    main()
