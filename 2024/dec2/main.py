from pathlib import Path


def get_reports() -> list[list[int]]:
    with open(Path(__file__).parent / "key.txt") as file:
        file_str = file.read()

    return [
        [int(el) for el in line.split(" ")] for line in file_str.strip().split("\n")
    ]


def is_safe(report: list[int]) -> bool:
    diff = [b - a for a, b in zip(report[:-1], report[1:])]
    if not (all(x > 0 for x in diff) or all(x < 0 for x in diff)):
        return False

    abs_diff = [abs(x) for x in diff]

    if all(x <= 3 for x in abs_diff):
        return True

    return False


def part_one(reports: list[list[int]]) -> int:
    return sum(is_safe(report) for report in reports)


def part_two(reports: list[list[int]]) -> int:
    n_saveable_reports = 0
    for report in reports:
        saved = False
        if is_safe(report):
            saved = True
        for i in range(len(report)):
            if is_safe(report[:i] + report[i + 1 :]):
                saved = True

        if saved:
            n_saveable_reports += 1

    return n_saveable_reports


def main():
    reports = get_reports()

    print(part_one(reports))
    print(part_two(reports))


if __name__ == "__main__":
    main()
