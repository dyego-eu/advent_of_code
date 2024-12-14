# https://adventofcode.com/2023/day/13

from pathlib import Path


def read_patterns():
    with open(Path(__file__).parent / "key.txt") as f:
        patterns = f.read().strip().split("\n\n")

    return patterns


def as_rows(pattern: str) -> list[str]:
    return pattern.split("\n")


def as_columns(pattern: str) -> list[str]:
    rows = as_rows(pattern)
    LL = len(rows[0])

    columns = [[] for _ in range(LL)]
    for row in rows:
        for column, char in zip(columns, row):
            column.append(char)

    return ["".join(column) for column in columns]


def test_mirror(list_pattern: list[str], idx: int, size: int) -> bool:
    delta = 0

    while delta + idx + 1 <= size - 1 and idx - delta >= 0:
        if list_pattern[delta + idx + 1] != list_pattern[idx - delta]:
            return False
        delta += 1

    return True


def part_one(patterns: list[str]) -> int:
    patterns = read_patterns()

    summary = 0
    for pattern in patterns:

        pattern_sum = 0
        columns = as_columns(pattern)
        for i in range(len(columns) - 1):
            if test_mirror(columns, i, len(columns)):
                pattern_sum += i + 1

        rows = as_rows(pattern)
        for i in range(len(rows) - 1):
            if test_mirror(rows, i, len(rows)):
                pattern_sum += 100 * (i + 1)

        if pattern_sum == 0:
            breakpoint()

        summary += pattern_sum
    return summary


def test_smudged_mirror(list_pattern: list[str], idx: int, size: int) -> bool:
    delta = 0
    smudges = 0

    while delta + idx + 1 <= size - 1 and idx - delta >= 0:
        for char, mirror_char in zip(
            list_pattern[delta + idx + 1], list_pattern[idx - delta]
        ):
            if char != mirror_char:
                smudges += 1
            if smudges >= 2:
                return False
        delta += 1

    if smudges != 1:
        return False

    return True


def part_two(patterns: list[str]) -> int:
    patterns = read_patterns()

    summary = 0
    for pattern in patterns:

        pattern_sum = 0
        columns = as_columns(pattern)
        for i in range(len(columns) - 1):
            if test_smudged_mirror(columns, i, len(columns)):
                pattern_sum += i + 1

        rows = as_rows(pattern)
        for i in range(len(rows) - 1):
            if test_smudged_mirror(rows, i, len(rows)):
                pattern_sum += 100 * (i + 1)

        if pattern_sum == 0:
            breakpoint()

        summary += pattern_sum
    return summary


def main():
    patterns = read_patterns()
    print(part_one(patterns))
    print(part_two(patterns))


if __name__ == "__main__":
    main()
