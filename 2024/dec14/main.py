# https://adventofcode.com/2024/day/14

import re
import statistics
from tqdm import tqdm
from collections import Counter
from pathlib import Path
from dataclasses import dataclass
from enum import Enum, auto

MAP_WIDTH = 101
MAP_HEIGHT = 103


class Quadrant(Enum):
    top_right = auto()
    top_left = auto()
    bottom_right = auto()
    bottom_left = auto()
    middle_cross = auto()


@dataclass
class Robot:
    px: int
    py: int
    vx: int
    vy: int

    @property
    def quadrant(self) -> Quadrant:
        match self.px, self.py:
            case (x, y) if x < (MAP_WIDTH - 1) // 2 and y < (MAP_HEIGHT - 1) // 2:
                return Quadrant.top_left
            case (x, y) if x >= (MAP_WIDTH + 1) // 2 and y < (MAP_HEIGHT - 1) // 2:
                return Quadrant.top_right
            case (x, y) if x < (MAP_WIDTH - 1) // 2 and y >= (MAP_HEIGHT + 1) // 2:
                return Quadrant.bottom_left
            case (x, y) if x >= (MAP_WIDTH + 1) // 2 and y >= (MAP_HEIGHT + 1) // 2:
                return Quadrant.bottom_right

        return Quadrant.middle_cross

    def move(self, n_steps: int = 1):
        self.px = (self.px + n_steps * self.vx) % MAP_WIDTH
        self.py = (self.py + n_steps * self.vy) % MAP_HEIGHT
        return self


def read_robots() -> list[Robot]:
    with open(Path(__file__).parent / "key.txt") as f:
        raw_robots = f.read().strip().split("\n")

    robot_re = re.compile(r"^p=(\d+),(\d+) v=(-?\d+),(-?\d+)$")
    robots = []

    for raw_robot in raw_robots:
        robot_match = robot_re.match(raw_robot)

        if robot_match is None:
            breakpoint()
            raise ValueError("Unrecognized robot format!")

        robots.append(
            Robot(
                px=int(robot_match.group(1)),
                py=int(robot_match.group(2)),
                vx=int(robot_match.group(3)),
                vy=int(robot_match.group(4)),
            )
        )

    return robots


def main():
    robots = read_robots()

    moved_robots = [robot.move(100) for robot in robots]
    quadrants = [robot.quadrant for robot in moved_robots]

    count = Counter(quadrants)
    print(
        count[Quadrant.top_right]
        * count[Quadrant.top_left]
        * count[Quadrant.bottom_right]
        * count[Quadrant.bottom_left]
    )

    robots = read_robots()

    for i in range(1, 100000):
        for robot in robots:
            robot.move(1)

        if compute_entropy(robots) < 40:
            break

    map = [[" " for _ in range(MAP_WIDTH)] for _ in range(MAP_HEIGHT)]

    for robot in robots:
        map[robot.py][robot.px] = "#"

    print("\n".join(["".join(map_line) for map_line in map]))
    print(i)


def compute_entropy(robots: list[Robot]) -> float:
    return statistics.stdev([robot.px for robot in robots]) + statistics.stdev(
        [robot.py for robot in robots]
    )


if __name__ == "__main__":
    main()
