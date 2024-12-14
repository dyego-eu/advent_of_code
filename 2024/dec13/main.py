# https://adventofcode.com/2024/day/13

from pathlib import Path
from dataclasses import dataclass


@dataclass
class Machine:
    ax: int
    ay: int
    bx: int
    by: int
    rx: int
    ry: int

    @property
    def determinant(self) -> int:
        return self.ax * self.by - self.bx * self.ay

    def compute_A_presses(self) -> float | None:
        if self.determinant == 0:
            return None

        return (self.rx * self.by - self.ry * self.bx) / self.determinant

    def compute_B_presses(self) -> float | None:
        if self.determinant == 0:
            return None

        return -(self.rx * self.ay - self.ry * self.ax) / self.determinant


def process_machine(raw_machine: str) -> Machine:
    line_a, line_b, line_r = raw_machine.strip().split("\n")

    raw_ax, raw_ay = line_a.split(": ")[1].split(", ")
    raw_bx, raw_by = line_b.split(": ")[1].split(", ")
    raw_rx, raw_ry = line_r.split(": ")[1].split(", ")

    return Machine(
        ax=int(raw_ax.replace("X+", "")),
        ay=int(raw_ay.replace("Y+", "")),
        bx=int(raw_bx.replace("X+", "")),
        by=int(raw_by.replace("Y+", "")),
        rx=int(raw_rx.replace("X=", "")),
        ry=int(raw_ry.replace("Y=", "")),
    )


def read_machines() -> list[Machine]:
    with open(Path(__file__).parent / "key.txt") as f:
        raw_machines = f.read().strip().split("\n\n")

    machines = []
    for raw_machine in raw_machines:
        machines.append(process_machine(raw_machine))

    return machines


def part_one(machines: list[Machine]) -> int:
    total = 0
    for machine in machines:
        if (
            machine.compute_A_presses() is not None
            and machine.compute_B_presses() is not None
            and int(machine.compute_A_presses()) == machine.compute_A_presses()
            and int(machine.compute_B_presses()) == machine.compute_B_presses()
        ):
            total += 3 * machine.compute_A_presses() + machine.compute_B_presses()

    return int(total)


def part_two(machines: list[Machine]) -> int:
    total = 0

    for machine in machines:
        machine.rx += 10000000000000
        machine.ry += 10000000000000

        if (
            machine.compute_A_presses() is not None
            and machine.compute_B_presses() is not None
            and int(machine.compute_A_presses()) == machine.compute_A_presses()
            and int(machine.compute_B_presses()) == machine.compute_B_presses()
        ):
            total += 3 * machine.compute_A_presses() + machine.compute_B_presses()

    return int(total)


def main():
    machines = read_machines()
    print(part_one(machines))
    print(part_two(machines))


if __name__ == "__main__":
    main()
