import re
from pathlib import Path


def read_instructions():
    with open(Path(__file__).parent / "key.txt") as f:
        instructions = f.read().strip().replace("\n", "")
    return instructions


def part_1(instructions: str) -> int:
    mul_instruction = re.compile(r"mul\((\d{1,3}),(\d{1,3})\)")
    sum = 0
    start_idx = 0
    while True:
        next_mul = mul_instruction.search(instructions, start_idx)
        if next_mul is None:
            break
        start_idx = next_mul.span()[1]
        sum += int(next_mul.group(1)) * int(next_mul.group(2))
    return sum


def part_2(instructions: str) -> int:
    do_instruction = re.compile(r"do\(\)")
    dont_instruction = re.compile(r"don't\(\)")
    mul_instruction = re.compile(r"mul\((\d{1,3}),(\d{1,3})\)")

    sum = 0
    start_idx = 0

    is_do = True

    while True:
        if is_do:
            next_dont = dont_instruction.search(instructions, start_idx)
            next_mul = mul_instruction.search(instructions, start_idx)

            if next_mul is None:
                break

            if next_dont is None or (next_mul.span()[0] < next_dont.span()[0]):
                start_idx = next_mul.span()[1]
                sum += int(next_mul.group(1)) * int(next_mul.group(2))
            else:
                is_do = False
                start_idx = next_dont.span()[1]

        else:
            next_do = do_instruction.search(instructions, start_idx)
            if next_do is None:
                break
            is_do = True
            start_idx = next_do.span()[1]

    return sum


def main():
    instructions = read_instructions()
    print(part_1(instructions))
    print(part_2(instructions))


if __name__ == "__main__":
    main()
