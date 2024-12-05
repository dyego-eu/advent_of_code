# https://adventofcode.com/2023/day/2

import re
from pathlib import Path
from typing import Literal 


BallColor = Literal["red"] | Literal["green"] | Literal["blue"]
Match = dict[BallColor, int]


def load_games() -> dict[int, list[Match]]:
    with open(Path(__file__).parent / "key.txt") as file:
        games_raw = file.read().strip().split("\n")

    games = {}
    red_regex = re.compile(r"(\d+) red")
    green_regex = re.compile(r"(\d+) green")
    blue_regex = re.compile(r"(\d+) blue")

    for game in games_raw:
        raw_id, raw_matches = game.split(": ", 1)

        id = int(raw_id.replace("Game ", ""))
        split_matches = raw_matches.split("; ")

        matches = [] 
        for raw_match in split_matches:
            match = {}
            red_capture = red_regex.search(raw_match)
            match["red"] = int(red_capture.group(1)) if red_capture else 0

            green_capture = green_regex.search(raw_match)
            match["green"] = int(green_capture.group(1)) if green_capture else 0

            blue_capture = blue_regex.search(raw_match)
            match["blue"] = int(blue_capture.group(1)) if blue_capture else 0
            matches.append(match)

        games[id] = matches

    return games


def part_one(games: dict[int, list[Match]]) -> int:
    RED_LIMIT = 12
    GREEN_LIMIT = 13
    BLUE_LIMIT = 14

    sum = 0
    for id, matches in games.items():
        is_possible = True

        for match in matches:
            if (
                match["red"] > RED_LIMIT
                or match["green"] > GREEN_LIMIT
                or match["blue"] > BLUE_LIMIT
            ):
                is_possible = False

        if is_possible:
            sum += id

    return sum


def part_two(games: dict[int, list[Match]]) -> int:
    total_power = 0
    
    for matches in games.values():
        min_red = 0
        min_green = 0
        min_blue = 0

        for match in matches:
            min_red = max(min_red, match["red"])
            min_green = max(min_green, match["green"])
            min_blue = max(min_blue, match["blue"])

        game_power = min_red * min_green * min_blue
        
        total_power += game_power

    return total_power


def main():
    games = load_games()
    print(part_one(games))
    print(part_two(games))



if __name__ == "__main__":
    main()
