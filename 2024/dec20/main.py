# https://adventofcode.com/2024/day/20

from pathlib import Path
from itertools import combinations
from collections import Counter
from dataclasses import dataclass


@dataclass(frozen=True)
class Position:
    x: int
    y: int


def read_maze():
    with open(Path(__file__).parent / "key.txt") as f:
        maze = [[*line] for line in f.read().strip().split("\n")]

    return maze


def find_neighbors(position: Position, maze):
    N = len(maze)
    LL = len(maze[0])

    neighbors = []
    if position.x > 0 and maze[position.y][position.x - 1] in [".", "S", "E"]:
        neighbors.append(Position(position.x - 1, position.y))
    if position.x < LL - 1 and maze[position.y][position.x + 1] in [".", "S", "E"]:
        neighbors.append(Position(position.x + 1, position.y))
    if position.y > 0 and maze[position.y - 1][position.x] in [".", "S", "E"]:
        neighbors.append(Position(position.x, position.y - 1))
    if position.y < N - 1 and maze[position.y + 1][position.x] in [".", "S", "E"]:
        neighbors.append(Position(position.x, position.y + 1))

    return neighbors


def part_one(maze) -> int:
    N = len(maze)
    LL = len(maze[0])

    start = Position(0, 0)
    end = Position(0, 0)
    neighbors = {}
    for y in range(N):
        for x in range(LL):
            match maze[y][x]:
                case "#":
                    neighbors[Position(x, y)] = find_neighbors(Position(x, y), maze)

                case "S":
                    start = Position(x, y)

                case "E":
                    end = Position(x, y)

    positions = {}
    idx = 0
    current = start
    while current != end:
        positions[current] = idx
        idx += 1
        maze[current.y][current.x] = "~"
        current = find_neighbors(current, maze)[0]

    positions[end] = idx

    shortcut_sizes = {}
    for wall, neighbor in neighbors.items():
        if len(neighbor) < 2:
            continue

        for pos1, pos2 in combinations(neighbor, 2):
            shortcut_size = abs(positions[pos1] - positions[pos2]) - 2
            if shortcut_size not in shortcut_sizes:
                shortcut_sizes[shortcut_size] = [wall]
            else:
                shortcut_sizes[shortcut_size].append(wall)

    total = 0
    for shortcut_size, walls in shortcut_sizes.items():
        if shortcut_size >= 100:
            total += len(walls)

    return total


def part_two(maze) -> int:
    N = len(maze)
    LL = len(maze[0])
    MIN_CHEAT = 100

    start = Position(0, 0)
    end = Position(0, 0)
    for y in range(N):
        for x in range(LL):
            match maze[y][x]:
                case "S":
                    start = Position(x, y)

                case "E":
                    end = Position(x, y)

    positions = []
    current = start
    while current != end:
        positions.append(current)
        maze[current.y][current.x] = "~"
        current = find_neighbors(current, maze)[0]

    positions.append(end)

    shortcuts = []

    for i, pos in enumerate(positions):
        for j, pos2 in enumerate(positions[i + MIN_CHEAT :], i + MIN_CHEAT):
            delta = abs(pos.x - pos2.x) + abs(pos.y - pos2.y)
            shortcut_size = j - i - delta
            if delta <= 20 and shortcut_size >= MIN_CHEAT:
                shortcuts.append(shortcut_size)

    return len(shortcuts)


def main():
    maze = read_maze()
    print(part_one(maze))

    maze = read_maze()
    print(part_two(maze))


if __name__ == "__main__":
    main()
