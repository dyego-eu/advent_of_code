# https://adventofcode.com/2024/day/15

from pathlib import Path
from enum import Enum, auto
from dataclasses import dataclass
from typing import Literal
from time import sleep


class Instruction(Enum):
    up = auto()
    down = auto()
    left = auto()
    right = auto()


@dataclass
class Position:
    x: int
    y: int


def read_map_and_instructions() -> tuple[Position, list[list[str]], list[Instruction]]:
    with open(Path(__file__).parent / "key.txt") as f:
        raw_map, raw_instructions = f.read().strip().split("\n\n")

    map = [[*line] for line in raw_map.split("\n")]

    robot = Position(0, 0)
    for y, line in enumerate(map):
        for x, char in enumerate(line):
            if char == "@":
                robot.x, robot.y = x, y

    instructions: list[Instruction] = []
    raw_instructions = "".join(raw_instructions.split("\n"))
    for raw_instruction in raw_instructions:
        match raw_instruction:
            case "^":
                instructions.append(Instruction.up)
            case "v":
                instructions.append(Instruction.down)
            case ">":
                instructions.append(Instruction.right)
            case "<":
                instructions.append(Instruction.left)

    return robot, map, instructions


def move(
    obj: Position,
    obj_char: str,
    map: list[list[str]],
    instruction: Instruction,
) -> bool:
    match instruction:
        case Instruction.up:
            match map[obj.y - 1][obj.x]:
                case ".":
                    map[obj.y][obj.x] = "."
                    obj.y -= 1
                    map[obj.y][obj.x] = obj_char
                    return True
                case "#":
                    return False
                case "O":
                    if move(Position(obj.x, obj.y - 1), "O", map, Instruction.up):
                        map[obj.y][obj.x] = "."
                        obj.y -= 1
                        map[obj.y][obj.x] = obj_char
                        return True
                    return False

        case Instruction.down:
            match map[obj.y + 1][obj.x]:
                case ".":
                    map[obj.y][obj.x] = "."
                    obj.y += 1
                    map[obj.y][obj.x] = obj_char
                    return True
                case "#":
                    return False
                case "O":
                    if move(Position(obj.x, obj.y + 1), "O", map, Instruction.down):
                        map[obj.y][obj.x] = "."
                        obj.y += 1
                        map[obj.y][obj.x] = obj_char
                        return True
                    return False

        case Instruction.right:
            match map[obj.y][obj.x + 1]:
                case ".":
                    map[obj.y][obj.x] = "."
                    obj.x += 1
                    map[obj.y][obj.x] = obj_char
                    return True
                case "#":
                    return False
                case "O":
                    if move(Position(obj.x + 1, obj.y), "O", map, Instruction.right):
                        map[obj.y][obj.x] = "."
                        obj.x += 1
                        map[obj.y][obj.x] = obj_char
                        return True
                    return False

        case Instruction.left:
            match map[obj.y][obj.x - 1]:
                case ".":
                    map[obj.y][obj.x] = "."
                    obj.x -= 1
                    map[obj.y][obj.x] = obj_char
                    return True
                case "#":
                    return False
                case "O":
                    if move(Position(obj.x - 1, obj.y), "O", map, Instruction.left):
                        map[obj.y][obj.x] = "."
                        obj.x -= 1
                        map[obj.y][obj.x] = obj_char
                        return True
                    return False
    return False


def print_map(map: list[list[str]]) -> None:
    print("\n".join("".join(mapline) for mapline in map))


def part_one():
    robot, map, instructions = read_map_and_instructions()

    for instruction in instructions:
        move(robot, "@", map, instruction)

    boxes = []
    for y, row in enumerate(map):
        for x, char in enumerate(row):
            if char == "O":
                boxes.append(Position(x, y))

    sum = 0
    for box in boxes:
        sum += box.x + 100 * box.y

    print(sum)


def read_double_map_and_instructions():
    with open("key.txt") as f:
        raw_map, raw_instructions = f.read().strip().split("\n\n")

    double_map = (
        raw_map.replace("#", "##")
        .replace("O", "[]")
        .replace(".", "..")
        .replace("@", "@.")
        .split("\n")
    )
    double_map = [[*line] for line in double_map]

    robot = Position(0, 0)
    for y, line in enumerate(double_map):
        for x, char in enumerate(line):
            if char == "@":
                robot.x, robot.y = x, y

    instructions: list[Instruction] = []
    raw_instructions = "".join(raw_instructions.split("\n"))
    for raw_instruction in raw_instructions:
        match raw_instruction:
            case "^":
                instructions.append(Instruction.up)
            case "v":
                instructions.append(Instruction.down)
            case ">":
                instructions.append(Instruction.right)
            case "<":
                instructions.append(Instruction.left)

    return robot, double_map, instructions


def can_move(
    pos: Position, obj_char: Literal["[", "]"], delta: int, map: list[list[str]]
) -> bool:
    if obj_char == "[":
        if map[pos.y + delta][pos.x] == "." and map[pos.y + delta][pos.x + 1] == ".":
            return True
        if map[pos.y + delta][pos.x] == "#" or map[pos.y + delta][pos.x + 1] == "#":
            return False

        success = True

        if map[pos.y + delta][pos.x] in ["[", "]"]:
            success = success and can_move(
                Position(pos.x, pos.y + delta),
                map[pos.y + delta][pos.x],
                delta,
                map,
            )
        if map[pos.y + delta][pos.x + 1] in ["[", "]"]:
            success = success and can_move(
                Position(pos.x + 1, pos.y + delta),
                map[pos.y + delta][pos.x + 1],
                delta,
                map,
            )

        return success

    if obj_char == "]":
        if map[pos.y + delta][pos.x] == "." and map[pos.y + delta][pos.x - 1] == ".":
            return True
        if map[pos.y + delta][pos.x] == "#" or map[pos.y + delta][pos.x - 1] == "#":
            return False

        success = True

        if map[pos.y + delta][pos.x] in ["[", "]"]:
            success = success and can_move(
                Position(pos.x, pos.y + delta), map[pos.y + delta][pos.x], delta, map
            )
        if map[pos.y + delta][pos.x - 1] in ["[", "]"]:
            success = success and can_move(
                Position(pos.x - 1, pos.y + delta),
                map[pos.y + delta][pos.x - 1],
                delta,
                map,
            )

        return success


def wide_move(
    obj: Position, obj_char: str, map: list[list[str]], instruction: Instruction
) -> bool:
    match instruction:
        case Instruction.up:
            if obj_char == "@":
                if map[obj.y - 1][obj.x] == ".":
                    map[obj.y][obj.x] = "."
                    obj.y -= 1
                    map[obj.y][obj.x] = "@"
                    return True

                if map[obj.y - 1][obj.x] == "#":
                    return False

                if can_move(Position(obj.x, obj.y - 1), map[obj.y - 1][obj.x], -1, map):
                    if map[obj.y - 1][obj.x] == "[":
                        wide_move(Position(obj.x, obj.y - 1), "[", map, instruction)
                        wide_move(Position(obj.x + 1, obj.y - 1), "]", map, instruction)
                    if map[obj.y - 1][obj.x] == "]":
                        wide_move(Position(obj.x - 1, obj.y - 1), "[", map, instruction)
                        wide_move(Position(obj.x, obj.y - 1), "]", map, instruction)
                    map[obj.y][obj.x] = "."
                    obj.y -= 1
                    map[obj.y][obj.x] = "@"
                    return True

                else:
                    return False

            else:
                if map[obj.y - 1][obj.x] == "[":
                    wide_move(Position(obj.x, obj.y - 1), "[", map, instruction)
                    wide_move(Position(obj.x + 1, obj.y - 1), "]", map, instruction)
                if map[obj.y - 1][obj.x] == "]":
                    wide_move(Position(obj.x - 1, obj.y - 1), "[", map, instruction)
                    wide_move(Position(obj.x, obj.y - 1), "]", map, instruction)

                map[obj.y][obj.x] = "."
                obj.y -= 1
                map[obj.y][obj.x] = obj_char
                return True

        case Instruction.down:
            if obj_char == "@":
                if map[obj.y + 1][obj.x] == ".":
                    map[obj.y][obj.x] = "."
                    obj.y += 1
                    map[obj.y][obj.x] = "@"
                    return True

                if map[obj.y + 1][obj.x] == "#":
                    return False

                if can_move(Position(obj.x, obj.y + 1), map[obj.y + 1][obj.x], 1, map):
                    if map[obj.y + 1][obj.x] == "[":
                        wide_move(Position(obj.x, obj.y + 1), "[", map, instruction)
                        wide_move(Position(obj.x + 1, obj.y + 1), "]", map, instruction)
                    if map[obj.y + 1][obj.x] == "]":
                        wide_move(Position(obj.x - 1, obj.y + 1), "[", map, instruction)
                        wide_move(Position(obj.x, obj.y + 1), "]", map, instruction)
                    map[obj.y][obj.x] = "."
                    obj.y += 1
                    map[obj.y][obj.x] = "@"
                    return True

                else:
                    return False

            else:
                if map[obj.y + 1][obj.x] == "[":
                    wide_move(Position(obj.x, obj.y + 1), "[", map, instruction)
                    wide_move(Position(obj.x + 1, obj.y + 1), "]", map, instruction)
                if map[obj.y + 1][obj.x] == "]":
                    wide_move(Position(obj.x - 1, obj.y + 1), "[", map, instruction)
                    wide_move(Position(obj.x, obj.y + 1), "]", map, instruction)

                map[obj.y][obj.x] = "."
                obj.y += 1
                map[obj.y][obj.x] = obj_char
                return True

        case Instruction.left:
            if map[obj.y][obj.x - 1] == ".":
                map[obj.y][obj.x] = "."
                obj.x -= 1
                map[obj.y][obj.x] = obj_char
                return True
            if map[obj.y][obj.x - 1] == "#":
                return False
            if wide_move(
                Position(obj.x - 1, obj.y), map[obj.y][obj.x - 1], map, instruction
            ):
                map[obj.y][obj.x] = "."
                obj.x -= 1
                map[obj.y][obj.x] = obj_char
                return True
            return False

        case Instruction.right:
            if map[obj.y][obj.x + 1] == ".":
                map[obj.y][obj.x] = "."
                obj.x += 1
                map[obj.y][obj.x] = obj_char
                return True

            if map[obj.y][obj.x + 1] == "#":
                return False

            if wide_move(
                Position(obj.x + 1, obj.y), map[obj.y][obj.x + 1], map, instruction
            ):
                map[obj.y][obj.x] = "."
                obj.x += 1
                map[obj.y][obj.x] = obj_char
                return True
            return False


def part_two():
    robot, double_map, instructions = read_double_map_and_instructions()

    for instruction in instructions:
        wide_move(robot, "@", double_map, instruction)

    boxes = []
    for y, line in enumerate(double_map):
        for x, char in enumerate(line):
            if char == "[":
                boxes.append(Position(x, y))

    sum = 0
    for box in boxes:
        sum += box.y * 100 + box.x

    print(sum)


def main():
    part_one()
    part_two()


if __name__ == "__main__":
    main()
