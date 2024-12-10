# https://adventofcode.com/2023/day/8

import re
import math
from pathlib import Path
from enum import Enum
from typing import TypedDict


class Direction(str, Enum):
    left = "left"
    right = "right"


class MapNode(TypedDict):
    left: str
    right: str


def read_instructions_and_map() -> tuple[list[Direction], dict[str, MapNode]]:
    with open(Path(__file__).parent / "key.txt") as file:
        raw_instructions_and_map = file.read().strip()

    raw_instructions, raw_map = raw_instructions_and_map.split("\n\n")

    instructions = []
    for instruction in raw_instructions:
        match instruction:
            case "L":
                instructions.append(Direction.left)
            case "R":
                instructions.append(Direction.right)
            case _:
                raise ValueError("Undefined Instruction")

    map_node_re = re.compile(r"^([0-9A-Z]{3}) = \(([0-9A-Z]{3}), ([0-9A-Z]{3})\)$")
    map_nodes = {}
    for map_node in raw_map.split("\n"):
        match = map_node_re.match(map_node)
        if match is None:
            raise ValueError("Map hasnt been properly processed")
        map_nodes[match.group(1)] = MapNode(left=match.group(2), right=match.group(3))

    return instructions, map_nodes


def part_one(instructions: list[Direction], map_nodes: dict[str, MapNode]) -> int:
    n_steps = 0
    N = len(instructions)
    location = "AAA"
    while location != "ZZZ":
        next_instruction = instructions[n_steps % N]
        n_steps += 1
        location = map_nodes[location][next_instruction]

    return n_steps


def compute_n_cycles(
    location: str, instructions: list[Direction], map_nodes: dict[str, MapNode]
) -> int:
    n = 0
    N = len(instructions)
    while not location.endswith("Z"):
        location = map_nodes[location][instructions[n % N]]
        n += 1

    return n // N


def part_two(instructions: list[Direction], map_nodes: dict[str, MapNode]) -> int:

    start_locations = [node for node in map_nodes if node.endswith("A")]

    n_cycles = [
        compute_n_cycles(location, instructions, map_nodes)
        for location in start_locations
    ]
    return len(instructions) * math.lcm(*n_cycles)


def main():
    instructions, map_nodes = read_instructions_and_map()

    print(part_one(instructions, map_nodes))
    print(part_two(instructions, map_nodes))


if __name__ == "__main__":
    main()
