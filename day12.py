from typing import List, Optional, Dict, Set, Tuple
from dataclasses import dataclass
import heapq


@dataclass(frozen=True)
class Coords:
    x: int
    y: int


@dataclass
class Map:
    locations: List[List[int]]
    start: Coords
    end: Coords

    def neighbours(self, loc: Coords) -> List[Coords]:
        deltas = [(-1, 0), (0, -1), (1, 0), (0, 1)]
        neigh = []
        for delta in deltas:
            newX = delta[0] + loc.x
            newY = delta[1] + loc.y
            if (
                newX >= 0
                and newX < len(self.locations[0])
                and newY >= 0
                and newY < len(self.locations)
            ):
                neigh.append(Coords(x=newX, y=newY))
        return neigh

    def get_height(self, loc: Coords) -> int:
        return self.locations[loc.y][loc.x]


def parse_map(lines: List[str]) -> Map:
    locations = []
    for idy, line in enumerate(lines):
        row = []
        for idx, char in enumerate(line.strip()):
            if char == "S":
                start = Coords(x=idx, y=idy)
                row.append(0)
            elif char == "E":
                end = Coords(x=idx, y=idy)
                row.append(ord("z") - ord("a"))
            else:
                row.append(ord(char) - ord("a"))
        locations.append(row)
    return Map(locations=locations, start=start, end=end)


def find_path(start: Coords, map: Map) -> int | None:
    queue = [(start, 0)]
    loc = start
    explored = {}
    while len(queue) > 0:
        loc, distance = queue.pop(0)
        if loc in explored:
            continue
        explored[loc] = True
        if loc == map.end:
            return distance
        height = map.get_height(loc)
        for neighbour in map.neighbours(loc):
            if neighbour not in explored:
                neighbour_height = map.get_height(neighbour)
                if neighbour_height <= (height + 1):
                    queue.append((neighbour, distance + 1))
    return None


with open("day12.txt", "r") as file:
    map = parse_map(file.readlines())
    print(find_path(map.start, map))

    min_dist = None
    for y in range(len(map.locations)):
        for x in range(len(map.locations[0])):
            if map.get_height(Coords(x, y)) == 0:
                dist = find_path(Coords(x, y), map)
                if min_dist is None:
                    min_dist = dist
                elif dist is not None:
                    min_dist = min(dist, min_dist)
    print(min_dist)
