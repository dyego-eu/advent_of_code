# https://adventofcode.com/2024/day/12

from pathlib import Path
from enum import Enum
from typing import NamedTuple


class FenceSide(str, Enum):
    top = "T"
    bottom = "B"
    left = "L"
    right = "R"


class Field(NamedTuple):
    crop: str
    x: int
    y: int
    fence_up: bool
    fence_down: bool
    fence_left: bool
    fence_right: bool

    @property
    def n_fences(self) -> int:
        return sum(
            [
                self.fence_up,
                self.fence_down,
                self.fence_left,
                self.fence_right
            ]
        )

    def get_fence(self) -> FenceSide | None:
        if self.fence_up:
            return FenceSide.top
        if self.fence_left:
            return FenceSide.left
        if self.fence_right:
            return FenceSide.right
        if self.fence_down:
            return FenceSide.bottom
        return None
        

def read_farm() -> list[list[Field]]:
    with open(Path(__file__).parent / "key.txt") as file:
        raw_farm = file.read().strip().split()

    N = len(raw_farm)
    LL = len(raw_farm[0])

    farm = []
    for y in range(N):
        farm_line = []
        for x in range(LL):
            crop = raw_farm[y][x]
            farm_line.append(
                Field(
                    crop=crop,
                    x=x,
                    y=y,
                    fence_left=(x == 0) or (raw_farm[y][x - 1] != crop),
                    fence_right=(x == LL - 1) or (raw_farm[y][x + 1] != crop),
                    fence_up=(y == 0) or (raw_farm[y - 1][x] != crop),
                    fence_down=(y == N - 1) or (raw_farm[y + 1][x] != crop),
                )
            )
        farm.append(farm_line)

    return farm


def find_all_neighbors(x: int, y: int, farm: list[list[Field]]) -> set[Field]:
    visited = set()
    queue = [farm[y][x]]
    while queue:
        current = queue.pop()
        visited.add(current)
        if (
            (not current.fence_up)
            and farm[current.y - 1][current.x] not in queue
            and farm[current.y - 1][current.x] not in visited
        ):
            queue.append(farm[current.y - 1][current.x])
        if (
            (not current.fence_down)
            and farm[current.y + 1][current.x] not in queue
            and farm[current.y + 1][current.x] not in visited
        ):
            queue.append(farm[current.y + 1][current.x])
        if (
            (not current.fence_left)
            and farm[current.y][current.x - 1] not in queue
            and farm[current.y][current.x - 1] not in visited
        ):
            queue.append(farm[current.y][current.x - 1])
        if (
            (not current.fence_right)
            and farm[current.y][current.x + 1] not in queue
            and farm[current.y][current.x + 1] not in visited
        ):
            queue.append(farm[current.y][current.x + 1])
    return visited


def get_size_fences(group: set[Field]) -> tuple[int, int]:
    size = len(group)
    fences = 0
    for field in group:
        fences += field.n_fences
    return size, fences


def part_one(farm: list[list[Field]]) -> int:

    N = len(farm)
    LL = len(farm[0])

    visited = set()
    group_info = []

    for y in range(N):
        for x in range(LL):
            if farm[y][x] not in visited:
                group = find_all_neighbors(x, y, farm)
                group_info.append(get_size_fences(group))
                visited.update(group)

    return sum(group[0] * group[1] for group in group_info)


def walk_fence(
    position: Field, fence_side: FenceSide, group: set[Field], farm: list[list[Field]]
):
    N = len(farm)
    LL = len(farm[0])

    match fence_side:
        case FenceSide.top:
            if (position.x == LL - 1) or (
                farm[position.y][position.x + 1] not in group
            ):
                return position, FenceSide.right
            if (position.y == 0) or (farm[position.y - 1][position.x + 1] not in group):
                return farm[position.y][position.x + 1], FenceSide.top

            return farm[position.y - 1][position.x + 1], FenceSide.left
        case FenceSide.bottom:
            if (position.x == 0) or (farm[position.y][position.x - 1] not in group):
                return position, FenceSide.left
            if (position.y == N - 1) or (
                farm[position.y + 1][position.x - 1] not in group
            ):
                return farm[position.y][position.x - 1], FenceSide.bottom

            return farm[position.y + 1][position.x - 1], FenceSide.right
        case FenceSide.left:
            if (position.y == 0) or (farm[position.y - 1][position.x] not in group):
                return position, FenceSide.top
            if (position.x == 0) or (farm[position.y - 1][position.x - 1] not in group):
                return farm[position.y - 1][position.x], FenceSide.left

            return farm[position.y - 1][position.x - 1], FenceSide.bottom
        case FenceSide.right:
            if (position.y == N - 1) or (farm[position.y + 1][position.x] not in group):
                return position, FenceSide.bottom
            if (position.x == LL - 1) or (
                farm[position.y + 1][position.x + 1] not in group
            ):
                return farm[position.y + 1][position.x], FenceSide.right

            return farm[position.y + 1][position.x + 1], FenceSide.top


def count_nsides(group: set[Field], farm: list[list[Field]]) -> int:
    has_fences = {field for field in group if field.n_fences > 0}

    side_count = 0
    while has_fences:
        start_pos = has_fences.pop()
        start_fence = start_pos.get_fence()

        current_pos, current_fence = walk_fence(start_pos, start_fence, group, farm)
        side_count += (start_fence != current_fence)
        has_fences.discard(current_pos)


        while (current_pos, current_fence) != (start_pos, start_fence):
            current_pos, walked_fence = walk_fence(current_pos, current_fence, group, farm)
            has_fences.discard(current_pos)
            side_count += current_fence != walked_fence
            current_fence = walked_fence
    

    return side_count


def part_two(farm: list[list[Field]]) -> int:

    N = len(farm)
    LL = len(farm[0])

    visited = set()
    group_info = []

    for y in range(N):
        for x in range(LL):
            if farm[y][x] not in visited:
                group = find_all_neighbors(x, y, farm)
                group_info.append((len(group), count_nsides(group, farm)))
                visited.update(group)

    return sum(group[0] * group[1] for group in group_info)


def main():
    farm = read_farm()
    print(part_one(farm))
    print(part_two(farm))


if __name__ == "__main__":
    main()
