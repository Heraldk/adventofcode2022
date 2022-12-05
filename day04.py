from typing import Tuple, List
from dataclasses import dataclass
import re


@dataclass
class CleaningRange:
    start: int
    end: int


def parse_input_range(input: str) -> Tuple[CleaningRange, CleaningRange]:
    vals = re.split(",|-", input)
    assert len(vals) == 4

    range1 = CleaningRange(start=int(vals[0]), end=int(vals[1]))
    range2 = CleaningRange(start=int(vals[2]), end=int(vals[3]))
    assert range1.start <= range1.end
    assert range2.start <= range2.end
    return range1, range2


def fully_contains(range1: CleaningRange, range2: CleaningRange) -> bool:
    if range1.start >= range2.start and range1.end <= range2.end:
        return True
    if range2.start >= range1.start and range2.end <= range1.end:
        return True
    return False


def has_overlap(range1: CleaningRange, range2: CleaningRange) -> bool:
    if range1.end < range2.start:
        return False
    if range2.end < range1.start:
        return False
    return True


with open("day04.txt", "r") as file:
    fully_contained_count = 0
    overlap_count = 0
    for line in file.readlines():
        range1, range2 = parse_input_range(line.strip())
        if fully_contains(range1, range2):
            fully_contained_count += 1
        if has_overlap(range1, range2):
            overlap_count += 1

    print(fully_contained_count)
    print(overlap_count)
