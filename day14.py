from dataclasses import dataclass
import re
from itertools import pairwise
from copy import deepcopy


@dataclass(frozen=True)
class Coords:
    x: int
    y: int


@dataclass
class Map:
    grid: dict[Coords, str]

    def print_map(self):
        max_y = max([coord.y for coord in map.grid.keys()])
        min_x = min([coord.x for coord in map.grid.keys()])
        max_x = max([coord.x for coord in map.grid.keys()])
        for y in range(max_y + 3):
            for x in range(min_x - 1, max_x + 2):
                loc = Coords(x, y)
                print("." if loc not in self.grid else self.grid[loc], end="")
            print()


def parse_coords(coord: str) -> Coords:
    vals = coord.strip().split(",")
    return Coords(x=int(vals[0]), y=int(vals[1]))


def parse_input(lines: list[str]) -> Map:
    map = Map(grid={})
    for line in lines:
        vals = re.split(" -> ", line)
        coords = [parse_coords(x) for x in vals]

        for a, b in pairwise(coords):
            isHorizontal = a.y == b.y
            if isHorizontal:
                start, end = (a, b) if a.x < b.x else (b, a)
                rg = range(start.x, end.x + 1)
            else:
                start, end = (a, b) if a.y < b.y else (b, a)
                rg = range(start.y, end.y + 1)
            dist = 0
            for _ in rg:
                if isHorizontal:
                    map.grid[Coords(x=start.x + dist, y=start.y)] = "#"
                else:
                    map.grid[Coords(x=start.x, y=start.y + dist)] = "#"
                dist += 1
    return map


def drop_sand(
    loc: Coords, max_depth: int, map: Map, use_bottom_floor: bool = False
) -> Coords | None:

    while loc.y < max_depth + 3:
        below = Coords(loc.x, loc.y + 1)
        downleft = Coords(loc.x - 1, loc.y + 1)
        downright = Coords(loc.x + 1, loc.y + 1)

        if use_bottom_floor and loc.y + 1 == max_depth + 2:
            map.grid[below] = "#"
            map.grid[downleft] = "#"
            map.grid[downright] = "#"

        if below not in map.grid:
            loc = below
        elif downleft not in map.grid:
            loc = downleft
        elif downright not in map.grid:
            loc = downright
        else:
            return loc

    return None


with open("day14.txt", "r") as file:
    map = parse_input(file.readlines())
    map_part_2 = deepcopy(map)
    max_depth = max([coord.y for coord in map.grid.keys()])
    start = Coords(500, 0)
    dropped = 0
    while True:
        rest_loc = drop_sand(start, max_depth, map)
        if rest_loc:
            map.grid[rest_loc] = "o"
            dropped += 1
        else:
            break
    print(dropped)

    dropped = 0
    while start not in map_part_2.grid:
        rest_loc = drop_sand(start, max_depth, map_part_2, use_bottom_floor=True)
        if rest_loc:
            map_part_2.grid[rest_loc] = "o"
            dropped += 1
    map_part_2.print_map()
    print(dropped)
