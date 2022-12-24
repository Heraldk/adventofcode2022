from dataclasses import dataclass
import re
from copy import deepcopy


@dataclass(frozen=True)
class Coords:
    x: int
    y: int


@dataclass
class Map:
    tiles: dict[Coords, str]
    # map of y coords to min and max x in that row
    minX: dict[int, int]
    maxX: dict[int, int]
    minY: dict[int, int]
    maxY: dict[int, int]


def parse_map(lines: list[str]) -> Map:
    minXMap = {}
    maxXMap = {}
    minYMap = {}
    maxYMap = {}
    tiles = {}
    for rowIdx, line in enumerate(lines):
        minX = None
        maxX = None
        for idx, char in enumerate(line):
            if char == "." or char == "#":
                if minX is None:
                    minX = idx
                maxX = idx
                tiles[Coords(idx + 1, rowIdx + 1)] = char
                minYMap[idx + 1] = min(minYMap.get(idx + 1, 10000000000000), rowIdx + 1)
                maxYMap[idx + 1] = max(maxYMap.get(idx + 1, 0), rowIdx + 1)
        minXMap[rowIdx + 1] = minX + 1
        maxXMap[rowIdx + 1] = maxX + 1

    return Map(tiles, minXMap, maxXMap, minYMap, maxYMap)


# based on "facing" direction, what you should add to the coordinates to take a step forward
# indexes going up are for rotating right, and going down are for rotating left
step_forward = [Coords(1, 0), Coords(0, 1), Coords(-1, 0), Coords(0, -1)]


def walk_map(map: Map, instrs: list[str]) -> tuple[Coords, int]:
    loc = Coords(map.minX[1], 1)
    facing = 0  # start facing "right"
    for instr in instrs:
        if instr == "L":
            facing = (facing - 1) % len(step_forward)
        elif instr == "R":
            facing = (facing + 1) % len(step_forward)
        else:
            for _ in range(int(instr)):
                new_loc = Coords(
                    loc.x + step_forward[facing].x, loc.y + step_forward[facing].y
                )
                if new_loc not in map.tiles:
                    if facing == 0:
                        new_loc = Coords(map.minX[new_loc.y], new_loc.y)
                    elif facing == 1:
                        new_loc = Coords(new_loc.x, map.minY[new_loc.x])
                    elif facing == 2:
                        new_loc = Coords(map.maxX[new_loc.y], new_loc.y)
                    else:
                        new_loc = Coords(new_loc.x, map.maxY[new_loc.x])
                assert new_loc in map.tiles
                if map.tiles[new_loc] == ".":
                    loc = new_loc
                else:
                    # walked into a wall: no point in continuing
                    break
    return loc, facing


def transition_cube_edge(loc: Coords, map: Map) -> tuple[Coords, int]:
    # hard coded for my input. Didn't feel like writing arbitrary cube mapping code ... :)
    # my cube looked like this with each letter being a face
    #   A B
    #   C
    # D E
    # F

    # off the top edge
    if loc.y == 0:
        # off the top edge of A, arrives left edge of F, heading right
        if loc.x >= 51 and loc.x <= 100:
            return Coords(1, loc.x + 100), 0
        # off the top edge of B, arrives bottom edge of F, heading up
        elif loc.x >= 101 and loc.x <= 150:
            return Coords(loc.x - 100, 200), 3
    # off the right-most edge is off the right edge of B, arrives right edge of E, heading left
    if loc.x == 151:
        assert loc.y >= 1 and loc.y <= 50
        return Coords(100, 151 - loc.y), 2
    # off the bottom of B, arrives right edge of C heading left
    if loc.y == 51:
        assert loc.x >= 101 and loc.x <= 150
        return Coords(100, loc.x - 50), 2
    if loc.x == 101:
        # off the right side of C, arrives bottom edge of B heading up
        if loc.y >= 51 and loc.y <= 100:
            return Coords(loc.y + 50, 50), 3
        # off the right side of E, arrives right edge of B heading left
        elif loc.y >= 101 and loc.y <= 150:
            return Coords(150, 151 - loc.y), 2
    # off the bottom of E, arrives on the right edge of F heading left
    if loc.y == 151:
        assert loc.x >= 51 and loc.x <= 100
        return Coords(50, loc.x + 100), 2
    # off the right edge of F, arrives bottom edge of E heading up
    if loc.x == 51:
        assert loc.y >= 151 and loc.y <= 200
        return Coords(loc.y - 100, 150), 3
    # off the bottom edge of F, arrives top of B, heading down
    if loc.y == 201:
        assert loc.x >= 1 and loc.x <= 50
        return Coords(loc.x + 100, 1), 1
    if loc.x == 0:
        # off the left edge of F, arrives top of A, heading down
        if loc.y >= 151 and loc.y <= 200:
            return Coords(loc.y - 100, 1), 1
        # off the left edge of D. arrives left edge of A, heading right
        elif loc.y >= 101 and loc.y <= 150:
            return Coords(51, 151 - loc.y), 0
    # off the top edge of D, arrives left edge of C, heading right
    if loc.y == 100:
        assert loc.x >= 1 and loc.x <= 50
        return Coords(51, loc.x + 50), 0
    if loc.x == 50:
        # off the left edge of C, arrives top of D, heading down
        if loc.y >= 51 and loc.y <= 100:
            return Coords(loc.y - 50, 101), 1
        # off the left edge of A, arrives left side of D heading right
        if loc.y >= 1 and loc.y <= 50:
            return Coords(1, 151 - loc.y), 0
    assert False


def walk_map_cube(map: Map, instrs: list[str]) -> Coords:
    loc = Coords(map.minX[1], 1)
    facing = 0  # start facing "right"
    for instr in instrs:
        if instr == "L":
            facing = (facing - 1) % len(step_forward)
        elif instr == "R":
            facing = (facing + 1) % len(step_forward)
        else:
            for _ in range(int(instr)):
                new_loc = Coords(
                    loc.x + step_forward[facing].x, loc.y + step_forward[facing].y
                )
                new_facing = facing
                if new_loc not in map.tiles:
                    new_loc, new_facing = transition_cube_edge(new_loc, map)
                assert new_loc in map.tiles
                if map.tiles[new_loc] == ".":
                    loc = new_loc
                    facing = new_facing
                else:
                    # walked into a wall: no point in continuing
                    break
    return loc, facing


def parse_instructions(line: str) -> list[str]:
    instrs = []
    cur_str = ""
    for char in line.strip():
        if char == "R" or char == "L":
            if cur_str != "":
                instrs.append(cur_str)
            instrs.append(char)
            cur_str = ""
        else:
            cur_str += char
    if cur_str != "":
        instrs.append(cur_str)
    return instrs


with open("day22.txt", "r") as file:
    lines = file.readlines()
    map = parse_map(lines[:-2])
    instrs = parse_instructions(lines[-1])
    stopping_point, facing = walk_map(map, instrs)
    print(
        stopping_point, facing, stopping_point.x * 4 + stopping_point.y * 1000 + facing
    )

    stopping_point, facing = walk_map_cube(map, instrs)
    print(
        stopping_point, facing, stopping_point.x * 4 + stopping_point.y * 1000 + facing
    )
