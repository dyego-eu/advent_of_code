# https://adventofcode.com/2023/day/9

from pathlib import Path


def read_sequences() -> list[list[int]]:
    with open(Path(__file__).parent / "key.txt") as f:
        raw_sequences = f.read().strip().split("\n")

    return [
        [int(val) for val in raw_sequence.split(" ")] for raw_sequence in raw_sequences
    ]


def predict_next(sequence: list[int]):
    if len(sequence) == 0:
        return 0

    if all(val == sequence[0] for val in sequence):
        return sequence[0]

    diff = [b - a for a, b in zip(sequence[:-1], sequence[1:])]
    return sequence[-1] + predict_next(diff)


def part_one(sequences: list[list[int]]) -> int:
    next_vals = []
    for sequence in sequences:
        next_vals.append(predict_next(sequence))
    return sum(next_vals)


def predict_previous(sequence: list[int]):
    if len(sequence) == 0:
        return 0

    if all(val == sequence[0] for val in sequence):
        return sequence[0]

    diff = [b - a for a, b in zip(sequence[:-1], sequence[1:])]
    return sequence[0] - predict_previous(diff)


def part_two(sequences: list[list[int]]) -> int:
    next_vals = []
    for sequence in sequences:
        next_vals.append(predict_previous(sequence))
    return sum(next_vals)


def main():
    sequences = read_sequences()
    print(part_one(sequences))
    print(part_two(sequences))


if __name__ == "__main__":
    main()
