# https://adventofcode.com/2024/day/7

from pathlib import Path
from itertools import product
from dataclasses import dataclass
from typing import Callable


@dataclass
class Operation:
    result: int
    operands: list[int]


def read_operations():
    with open(Path(__file__).parent / "key.txt") as f:
        raw_operations = f.read().strip().split("\n")

    operations = []
    for raw_operation in raw_operations:
        raw_result, raw_operands = raw_operation.split(": ")
        operations.append(
            Operation(
                int(raw_result),
                [int(val) for val in raw_operands.split(" ")],
            )
        )

    return operations


def could_be_true(
    operation: Operation, available_ops: list[Callable[[int, int], int]]
) -> bool:
    placements = len(operation.operands) - 1

    for potential_operations in product(available_ops, repeat=placements):
        result = operation.operands[0]

        for pair_operation, next_val in zip(
            potential_operations, operation.operands[1:]
        ):
            result = pair_operation(result, next_val)

        if result == operation.result:
            return True

    return False


def pair_sum(x, y):
    return x + y


def pair_mul(x, y):
    return x * y


def part_one(operations: list[Operation]) -> int:

    available_ops = [pair_sum, pair_mul]

    return sum(
        operation.result
        for operation in operations
        if could_be_true(operation, available_ops)
    )


def pair_concat(x, y):
    return int(str(x) + str(y))


def part_two(operations: list[Operation]) -> int:

    available_ops = [pair_sum, pair_mul, pair_concat]

    return sum(
        operation.result
        for operation in operations
        if could_be_true(operation, available_ops)
    )


def main():
    operations = read_operations()

    print(part_one(operations))
    print(part_two(operations))


if __name__ == "__main__":
    main()
