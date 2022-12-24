from dataclasses import dataclass
import re
from copy import deepcopy


@dataclass(frozen=True)
class Coords:
    x: int
    y: int


@dataclass
class Elf:
    proposed_location: Coords | None = None


@dataclass
class Map:
    elves: dict[Coords, Elf]

    def bounds(self):
        minX = min([val.x for val in self.elves.keys()])
        maxX = max([val.x for val in self.elves.keys()])
        minY = min([val.y for val in self.elves.keys()])
        maxY = max([val.y for val in self.elves.keys()])
        return minX, maxX, minY, maxY

    def count_empty_spaces(self) -> int:
        minX, maxX, minY, maxY = self.bounds()
        count = 0
        for row in range(minY, maxY + 1):
            for col in range(minX, maxX + 1):
                if Coords(col, row) not in self.elves:
                    count += 1
        return count

    def __repr__(self):
        minX, maxX, minY, maxY = self.bounds()
        rows = []
        for row in range(minY, maxY + 1):
            rowvals = []
            for col in range(minX, maxX + 1):
                if Coords(col, row) in self.elves:
                    rowvals.append("#")
                else:
                    rowvals.append(".")
            rows.append("".join(rowvals))
        return "\n".join(rows)


def parse_elves(lines: list[str]) -> Map:
    elves = {}
    for rowIdx, line in enumerate(lines):
        for idx, char in enumerate(line):
            if char == "#":
                elves[Coords(idx, rowIdx)] = Elf()

    return Map(elves)


NORTHEAST = Coords(1, -1)
NORTH = Coords(0, -1)
NORTHWEST = Coords(-1, -1)
EAST = Coords(1, 0)
WEST = Coords(-1, 0)
SOUTHEAST = Coords(1, 1)
SOUTH = Coords(0, 1)
SOUTHWEST = Coords(-1, 1)

neighbours = [NORTHEAST, NORTH, NORTHWEST, EAST, WEST, SOUTHEAST, SOUTH, SOUTHWEST]
directions = [
    ([NORTHEAST, NORTH, NORTHWEST], NORTH),
    ([SOUTH, SOUTHEAST, SOUTHWEST], SOUTH),
    ([WEST, NORTHWEST, SOUTHWEST], WEST),
    ([EAST, NORTHEAST, SOUTHEAST], EAST),
]


def has_neighbour(test_locations: list[Coords], loc: Coords, map: Map) -> bool:
    for neighbour in test_locations:
        test_coords = Coords(loc.x + neighbour.x, loc.y + neighbour.y)
        if test_coords in map.elves:
            return True
    return False


def propose_step(map: Map) -> dict[Coords, int]:
    locations = {}
    for loc, elf in map.elves.items():
        elf.proposed_location = None
        if has_neighbour(neighbours, loc, map):
            for test_directions, propose_direction in directions:
                if not has_neighbour(test_directions, loc, map):
                    elf.proposed_location = Coords(
                        loc.x + propose_direction.x, loc.y + propose_direction.y
                    )
                    locations[elf.proposed_location] = (
                        locations.get(elf.proposed_location, 0) + 1
                    )
                    break
    return locations


def move_elves(map: Map) -> int:
    propose_locs = propose_step(map)
    new_elf_locs = {}
    moved_elves = 0
    for loc, elf in map.elves.items():
        if elf.proposed_location is None:
            new_elf_locs[loc] = elf
        elif propose_locs[elf.proposed_location] == 1:
            new_elf_locs[elf.proposed_location] = elf
            moved_elves += 1
        else:
            new_elf_locs[loc] = elf
    map.elves = new_elf_locs
    return moved_elves


with open("day23.txt", "r") as file:
    map = parse_elves(file.readlines())
    moved = 1
    iteration_count = 0
    while moved > 0:
        # move the elves
        moved = move_elves(map)
        # change the move direction list
        first = directions.pop(0)
        directions.append(first)
        iteration_count += 1
        if iteration_count == 10:
            print(map.count_empty_spaces())
    print(iteration_count, map.count_empty_spaces())
