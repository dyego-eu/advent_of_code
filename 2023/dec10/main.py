# https://adventofcode.com/2023/day/10

from enum import Enum, auto
import re
from pathlib import Path
from dataclasses import dataclass


@dataclass
class Position:
    x: int
    y: int


class Direction(int, Enum):
    top = auto()
    bottom = auto()
    left = auto()
    right = auto()

    @property
    def opposite(self):
        if self.name == "top":
            return Direction.bottom
        if self.name == "bottom":
            return Direction.top
        if self.name == "left":
            return Direction.right
        if self.name == "right":
            return Direction.left


def read_pipes() -> list[str]:
    with open(Path(__file__).parent / "key.txt") as f:
        raw_pipes = f.read()

    pipes = (
        raw_pipes.replace("|", "║")
        .replace("-", "═")
        .replace("J", "╝")
        .replace("F", "╔")
        .replace("7", "╗")
        .replace("L", "╚")
    )
    return pipes.split("\n")


def valid_directions(
    position: Position, pipes: list[str]
) -> tuple[Direction, Direction]:
    valid_directions = []
    if pipes[position.y][position.x - 1] in ["═", "╔", "╚"]:
        valid_directions.append(Direction.left)
    if pipes[position.y][position.x + 1] in ["═", "╗", "╝"]:
        valid_directions.append(Direction.right)
    if pipes[position.y - 1][position.x] in ["║", "╔", "╗"]:
        valid_directions.append(Direction.top)
    if pipes[position.y + 1][position.x] in ["║", "╚", "╝"]:
        valid_directions.append(Direction.bottom)
    return tuple(sorted(valid_directions))


def next_step(position: Position, direction: Direction):
    match direction:
        case Direction.top:
            return Position(position.x, position.y - 1)
        case Direction.bottom:
            return Position(position.x, position.y + 1)
        case Direction.left:
            return Position(position.x - 1, position.y)
        case Direction.right:
            return Position(position.x + 1, position.y)


PIPE_DIRECTIONS = {
    "║": (Direction.top, Direction.bottom),
    "═": (Direction.left, Direction.right),
    "╚": (Direction.top, Direction.right),
    "╝": (Direction.top, Direction.left),
    "╗": (Direction.bottom, Direction.left),
    "╔": (Direction.bottom, Direction.right),
}


def part_one(pipes: list[str]) -> tuple[int, list[list[str]]]:
    animal_re = re.compile(r"S")
    start_pos = Position(0, 0)

    for i, line in enumerate(pipes):
        match = animal_re.search(line)
        if match is not None:
            start_pos = Position(match.span(0)[0], i)

    animal_directions = valid_directions(start_pos, pipes)
    animal_pipe = {value: key for key, value in PIPE_DIRECTIONS.items()}[
        animal_directions
    ]
    next_direction = animal_directions[0]
    cur_pos = next_step(start_pos, next_direction)
    steps = 1

    N = len(pipes)
    LL = len(pipes[0])

    pipe_path = [["." for _ in range(LL)] for _ in range(N)]
    pipe_path[start_pos.y][start_pos.x] = animal_pipe
    while cur_pos != start_pos:
        pipe_path[cur_pos.y][cur_pos.x] = pipes[cur_pos.y][cur_pos.x]
        next_direction = [
            direction
            for direction in PIPE_DIRECTIONS[pipes[cur_pos.y][cur_pos.x]]
            if direction != next_direction.opposite
        ].pop()
        cur_pos = next_step(cur_pos, next_direction)
        steps += 1

    return steps // 2, pipe_path


def mark_inside_out(
    cur_pos: Position, pipe_path: list[list[str]], next_direction: Direction
) -> None:
    match next_direction:
        case Direction.right:
            if pipe_path[cur_pos.y + 1][cur_pos.x] == ".":
                pipe_path[cur_pos.y + 1][cur_pos.x] = "☄"
            if pipe_path[cur_pos.y - 1][cur_pos.x] == ".":
                pipe_path[cur_pos.y - 1][cur_pos.x] = " "

        case Direction.left:
            if pipe_path[cur_pos.y - 1][cur_pos.x] == ".":
                pipe_path[cur_pos.y - 1][cur_pos.x] = "☄"
            if pipe_path[cur_pos.y + 1][cur_pos.x] == ".":
                pipe_path[cur_pos.y + 1][cur_pos.x] = " "

        case Direction.top:
            if pipe_path[cur_pos.y][cur_pos.x + 1] == ".":
                pipe_path[cur_pos.y][cur_pos.x + 1] = "☄"
            if pipe_path[cur_pos.y][cur_pos.x - 1] == ".":
                pipe_path[cur_pos.y][cur_pos.x - 1] = " "

        case Direction.bottom:
            if pipe_path[cur_pos.y][cur_pos.x - 1] == ".":
                pipe_path[cur_pos.y][cur_pos.x - 1] = "☄"
            if pipe_path[cur_pos.y][cur_pos.x + 1] == ".":
                pipe_path[cur_pos.y][cur_pos.x + 1] = " "


def part_two(pipe_path: list[list[str]]) -> int:
    N = len(pipe_path)
    LL = len(pipe_path[0])

    x, y = 0, 0
    for i, line in enumerate(pipe_path):
        if any(char != "." for char in line):
            y = i
            for j, char in enumerate(line):
                if char != ".":
                    x = j
                    break
            break

    start_pos = Position(x, y)
    print(start_pos)
    print(pipe_path[start_pos.y][start_pos.x])
    next_direction = Direction.right
    cur_pos = next_step(start_pos, next_direction)
    print(pipe_path[cur_pos.y][cur_pos.x])

    while cur_pos != start_pos:
        mark_inside_out(cur_pos, pipe_path, next_direction)

        next_direction = [
            direction
            for direction in PIPE_DIRECTIONS[pipe_path[cur_pos.y][cur_pos.x]]
            if direction != next_direction.opposite
        ].pop()

        mark_inside_out(cur_pos, pipe_path, next_direction)

        cur_pos = next_step(cur_pos, next_direction)

    for i in range(N):
        for j in range(LL):
            if j == 0 or j == LL - 1 or i == 0 or i == N - 1:
                pipe_path[i][j] = " "

            elif pipe_path[i][j] == "☄":
                if pipe_path[i][j + 1] == ".":
                    pipe_path[i][j + 1] = "☄"
                if pipe_path[i][j - 1] == ".":
                    pipe_path[i][j - 1] = "☄"
                if pipe_path[i + 1][j] == ".":
                    pipe_path[i + 1][j] = "☄"
                if pipe_path[i - 1][j] == ".":
                    pipe_path[i - 1][j] = "☄"

            elif pipe_path[i][j] == " ":
                if pipe_path[i][j + 1] == ".":
                    pipe_path[i][j + 1] = " "
                if pipe_path[i][j - 1] == ".":
                    pipe_path[i][j - 1] = " "
                if pipe_path[i + 1][j] == ".":
                    pipe_path[i + 1][j] = " "
                if pipe_path[i - 1][j] == ".":
                    pipe_path[i - 1][j] = " "

            elif pipe_path[i][j] == ".":
                if pipe_path[i][j + 1] == " ":
                    pipe_path[i][j] = " "
                if pipe_path[i][j - 1] == " ":
                    pipe_path[i][j] = " "
                if pipe_path[i + 1][j] == " ":
                    pipe_path[i][j] = " "
                if pipe_path[i - 1][j] == " ":
                    pipe_path[i][j] = " "

    print("\n".join("".join(line) for line in pipe_path))
    return sum(sum(char == "☄" for char in line) for line in pipe_path)


def main():
    pipes = read_pipes()

    result, pipe_path = part_one(pipes)
    print(result)

    print(part_two(pipe_path))


if __name__ == "__main__":
    main()
