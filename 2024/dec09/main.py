# https://adventofcode.com/2024/day/9

from pathlib import Path
from dataclasses import dataclass


@dataclass
class File:
    id: int
    size: int
    start_pos: int

    @property
    def checksum(self):
        return sum(
            [self.id * val for val in range(self.start_pos, self.start_pos + self.size)]
        )


@dataclass
class Empty:
    size: int
    start_pos: int


def read_memory_map() -> str:
    with open(Path(__file__).parent / "key.txt") as file:
        return file.read().strip()


def part_one(memory_map: str) -> int:
    expanded = []

    for idx, char in enumerate(memory_map):
        if idx % 2 == 0:
            expanded += [idx // 2] * int(char)
        else:
            expanded += [None] * int(char)

    i = 0
    j = len(expanded) - 1

    while i < j:
        if expanded[i] is None:
            expanded[i], expanded[j] = expanded[j], expanded[i]
            while expanded[j] is None:
                j -= 1
        i += 1

    return sum(
        [idx * val for idx, val in enumerate(expanded[: j + 1]) if val is not None]
    )


def part_two(memory_map: str) -> int:
    files = []
    empties = []

    current_pos = 0
    for idx, char in enumerate(memory_map):
        if idx % 2 == 0:
            files.append(File(id=idx // 2, size=int(char), start_pos=current_pos))
        else:
            empties.append(Empty(size=int(char), start_pos=current_pos))
        current_pos += int(char)

    for file in reversed(files):
        for empty in empties:
            if file.size <= empty.size and file.start_pos > empty.start_pos:
                file.start_pos = empty.start_pos
                empty.size -= file.size
                empty.start_pos += file.size
                if empty.size == 0:
                    del empty
                break

    return sum([file.checksum for file in files])


def main():
    memory_map = read_memory_map()
    print(part_one(memory_map))
    print(part_two(memory_map))


if __name__ == "__main__":
    main()
