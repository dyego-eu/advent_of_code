# https://adventofcode.com/2024/day/18

from collections import defaultdict
from pathlib import Path
from dataclasses import dataclass


MAZE_SIZE = 70
STREAM_SIZE = 1024


@dataclass(frozen=True)
class Position:
    x: int
    y: int


def read_data_stream() -> list[Position]:
    with open(Path(__file__).parent / "key.txt") as file:
        raw_data = file.read().strip().split("\n")

    points = []
    for raw_point in raw_data:
        raw_x, raw_y = raw_point.split(",")
        points.append(Position(int(raw_x), int(raw_y)))

    return points


def construct_map(positions: list[Position]) -> list[list[str]]:
    map = [["." for _ in range(MAZE_SIZE + 1)] for _ in range(MAZE_SIZE + 1)]

    for point in positions:
        map[point.y][point.x] = "#"

    return map


def get_next_current(distances, visited):
    min_val = float("inf")
    current = None
    for element, value in distances.items():
        if element in visited:
            continue
        if value <= min_val:
            min_val = value
            current = element

    return current


def get_neighbors(current, map):

    neighbors = []

    if current.x > 0 and map[current.y][current.x - 1] == ".":
        neighbors.append(Position(current.x - 1, current.y))
    if current.x < MAZE_SIZE and map[current.y][current.x + 1] == ".":
        neighbors.append(Position(current.x + 1, current.y))
    if current.y > 0 and map[current.y - 1][current.x] == ".":
        neighbors.append(Position(current.x, current.y - 1))
    if current.y < MAZE_SIZE and map[current.y + 1][current.x] == ".":
        neighbors.append(Position(current.x, current.y + 1))

    return neighbors


def find_min_distance(positions):
    map = construct_map(positions)

    visited = set()
    distances = defaultdict(lambda: float("inf"))
    current = Position(0, 0)
    distances[current] = 0

    while True:
        current = get_next_current(distances, visited)
        if current is None:
            break
        visited.add(current)
        neighbors = get_neighbors(current, map)
        for neighbor in neighbors:
            distances[neighbor] = min(distances[current] + 1, distances[neighbor])

        if current == Position(MAZE_SIZE, MAZE_SIZE):
            break

    if current is None:
        return None

    return distances[Position(MAZE_SIZE, MAZE_SIZE)]


def main():
    positions = read_data_stream()
    min_distance = find_min_distance(positions[:STREAM_SIZE])
    print(min_distance)

    blocking_byte = find_blocking_byte(positions)
    print(blocking_byte)


def find_blocking_byte(positions):
    N = len(positions)

    left = STREAM_SIZE
    right = N

    while left + 1 < right:
        center = (left + right) // 2
        min_distance = find_min_distance(positions[:center])
        if min_distance is None:
            right = center
        else:
            left = center

    return positions[left]


if __name__ == "__main__":
    main()
