# https://adventofcode.com/2023/day/3

import re
from typing import NamedTuple
from pathlib import Path


class Number(NamedTuple):
    val: int
    x_start: int
    x_end: int


class Symbol(NamedTuple):
    char: str
    x: int


def decode_numbers_and_symbols() -> tuple[list[list[Number]], list[list[Symbol]]]:
    with open(Path(__file__).parent / "key.txt") as f:
        engine_str = f.read().strip()

    number_re = re.compile(r"\d+")
    symbol_re = re.compile(r"[^\.0-9]")

    numbers: list[list[Number]] = []
    symbols: list[list[Symbol]] = []

    for line in engine_str.split("\n"):
        start_idx = 0
        number_line = []
        while True:
            match = number_re.search(line, start_idx)
            if match is None:
                break
            number_line.append(
                Number(
                    val=int(match.group(0)),
                    x_start=match.span()[0],
                    x_end=match.span()[1],
                )
            )
            start_idx = match.span()[1]
        numbers.append(number_line)

        start_idx = 0
        symbol_line = []
        while True:
            match = symbol_re.search(line, start_idx)
            if match is None:
                break
            symbol_line.append(
                Symbol(
                    char=match.group(0),
                    x=match.span(0)[0],
                )
            )
            start_idx = match.span(0)[1]
        symbols.append(symbol_line)

    return numbers, symbols


def part_one(numbers: list[list[Number]], symbols: list[list[Symbol]]) -> int:
    activated_numbers = []
    N = len(numbers)
    for idx, number_line in enumerate(numbers):
        for number in number_line:
            is_activated = False
            for symbol in [
                *(symbols[idx - 1] if (idx - 1 > 0) else []),
                *symbols[idx],
                *(symbols[idx + 1] if (idx + 1 < N) else []),
            ]:
                if number.x_start - 1 <= symbol.x < number.x_end + 1:
                    is_activated = True
                    break

            if is_activated:
                activated_numbers.append(number)

    return sum(number.val for number in activated_numbers)


def part_two(numbers: list[list[Number]], symbols: list[list[Symbol]]) -> int:
    gear_ratios = []

    N = len(symbols)
    for idx, symbol_line in enumerate(symbols):
        for symbol in symbol_line:
            if not symbol.char == "*":
                continue

            gear_parts = []
            for number in [
                *(numbers[idx - 1] if (idx - 1 >= 0) else []),
                *numbers[idx],
                *(numbers[idx + 1] if (idx + 1 < N) else []),
            ]:
                if number.x_start - 1 <= symbol.x < number.x_end + 1:
                    gear_parts.append(number)

            if len(gear_parts) == 2:
                gear_ratios.append(gear_parts[0].val * gear_parts[1].val)

    return sum(gear_ratios)


def main():
    numbers, symbols = decode_numbers_and_symbols()

    print(part_one(numbers, symbols))
    print(part_two(numbers, symbols))


if __name__ == "__main__":
    main()
