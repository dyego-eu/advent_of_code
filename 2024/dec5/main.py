from typing import NamedTuple
from pathlib import Path


class Rule(NamedTuple):
    before: int
    after: int


def read_rules_and_manuals() -> tuple[list[Rule], list[list[int]]]:
    with open(Path(__file__).parent / "key.txt") as f:
        raw_rules_and_manuals = f.read().strip()

    raw_rules, raw_manuals = raw_rules_and_manuals.split("\n\n")

    rules = []
    for raw_rule in raw_rules.strip().split("\n"):
        rules.append(Rule(*[int(val) for val in raw_rule.split("|")]))

    manuals = []
    for raw_manual in raw_manuals.strip().split("\n"):
        manuals.append([int(val) for val in raw_manual.split(",")])

    return rules, manuals


def pages_are_sorted(manual: list[int], rules: list[Rule]) -> bool:
    is_sorted = True
    for rule in rules:
        if rule.before not in manual or rule.after not in manual:
            continue

        if manual.index(rule.before) > manual.index(rule.after):
            return False

    return is_sorted


def part_one(rules: list[Rule], manuals: list[list[int]]) -> int:
    ordered_manuals = [manual for manual in manuals if pages_are_sorted(manual, rules)]
    result = sum(manual[len(manual) // 2] for manual in ordered_manuals)
    return result


def order_pages(manual: list[int], rules: list[Rule]) -> list[int]:
    relevant_rules = [
        rule for rule in rules if (rule.before in manual and rule.after in manual)
    ]

    if len(manual) <= 1:
        return manual

    first_page = manual[0]

    for page in manual:
        if page in [rule.after for rule in relevant_rules]:
            continue
        first_page = page
        break

    manual.remove(first_page)

    return [first_page, *order_pages(manual, relevant_rules)]


def part_two(rules, manuals) -> int:
    corrected_manuals = [
        order_pages(manual, rules)
        for manual in manuals
        if not pages_are_sorted(manual, rules)
    ]
    result = sum(manual[len(manual) // 2] for manual in corrected_manuals)
    return result


def main():
    rules, manuals = read_rules_and_manuals()

    result_one = part_one(rules, manuals)
    print(result_one)

    result_two = part_two(rules, manuals)
    print(result_two)


if __name__ == "__main__":
    main()
