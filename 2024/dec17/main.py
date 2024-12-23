# https://adventofcode.com/2024/day/17

from pathlib import Path


def read_program_and_registers() -> tuple[list[int], dict[str, int]]:
    with open(Path(__file__).parent / "key.txt") as f:
        raw_registers, raw_program = f.read().strip().split("\n\n")

    registers = {}
    for raw_register in raw_registers.split("\n"):
        register_name, register_value = raw_register.split(": ")
        register_name = register_name.replace("Register ", "")
        registers[register_name] = int(register_value)

    program = [int(code) for code in raw_program.split(": ")[1].split(",")]

    return program, registers


def read_combo(registers: dict[str, int], operand: int) -> int:
    match operand:
        case x if x <= 3:
            return operand
        case 4:
            return registers["A"]
        case 5:
            return registers["B"]
        case 6:
            return registers["C"]
        case _:
            raise NotImplementedError()


def step_program(
    program: list[int],
    registers: dict[str, int],
    program_counter: int,
) -> tuple[int, int] | None:
    while program_counter < len(program):
        instruction = program[program_counter]
        operand = program[program_counter + 1]

        match instruction:
            case 0:
                denominator = 2 ** read_combo(registers, operand)
                registers["A"] = registers["A"] // denominator
            case 1:
                registers["B"] = registers["B"] ^ operand
            case 2:
                registers["B"] = read_combo(registers, operand) % 8
            case 3:
                if registers["A"] != 0:
                    program_counter = operand - 2
            case 4:
                registers["B"] = registers["B"] ^ registers["C"]
            case 5:
                program_counter += 2
                return read_combo(registers, operand) % 8, program_counter
            case 6:
                denominator = 2 ** read_combo(registers, operand)
                registers["B"] = registers["A"] // denominator
            case 7:
                denominator = 2 ** read_combo(registers, operand)
                registers["C"] = registers["A"] // denominator
            case _:
                raise NotImplementedError()

        program_counter += 2


def execute_program(program: list[int], registers: dict[str, int]) -> list[int]:
    program_counter = 0
    output = []
    while True:
        step_output = step_program(program, registers, program_counter)
        if step_output is None:
            break

        next_val, program_counter = step_output
        output.append(next_val)

    return output


def recursive_find(
    sequence: list[int], program: list[int], previous: int = 0
) -> int | None:
    if len(sequence) == 0:
        return previous
    for i in range(0, 1024):
        registers = {"A": i, "B": 0, "C": 0}
        step_output = step_program(program, registers, program_counter=0)
        if step_output is None:
            continue

        next_val = step_output[0]
        if next_val == sequence[-1] and (i >> 3) == (previous & 127):
            output = recursive_find(sequence[:-1], program, previous << 3 | (i % 8))
            if output is not None:
                return output


def main():
    program, registers = read_program_and_registers()
    print(execute_program(program, registers))
    print(recursive_find(program, program))


if __name__ == "__main__":
    main()
