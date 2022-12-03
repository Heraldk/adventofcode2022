from collections import Counter
from typing import Tuple, List


def process_compartments(line: str) -> Tuple[str, str]:
    half = len(line) // 2
    return line[0:half], line[half:]


def find_common(groups: List[str]) -> str:
    first = True
    common = set()
    for group in groups:
        group_uniques = set(Counter(group).keys())
        if first:
            first = False
            common = group_uniques
        else:
            common = common.intersection(group_uniques)

    assert len(common) == 1
    return list(common)[0]


def get_priority(a: str) -> int:
    ascii_value = ord(a)
    if ascii_value >= ord("a"):
        return ascii_value - ord("a") + 1
    else:
        return ascii_value - ord("A") + 27


with open("day03.txt", "r") as file:
    lines = [x.strip() for x in file.readlines()]

    # part 1
    part1_priority = 0
    for x in lines:
        a, b = process_compartments(x)
        common = find_common([a, b])
        part1_priority += get_priority(common)
    print(part1_priority)

    # part 2
    part2_priority = 0
    for x in range(0, len(lines), 3):
        common = find_common(lines[x : x + 3])
        part2_priority += get_priority(common)
    print(part2_priority)
