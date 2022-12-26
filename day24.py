from dataclasses import dataclass
import heapq


@dataclass(order=True, frozen=True)
class Coords:
    x: int
    y: int


@dataclass(frozen=True, eq=True)
class Map:
    blizzards: dict[Coords, str]
    maxX: int
    maxY: int

    def hashable_map(self) -> str:
        result = ""
        for y in range(map.maxY + 1):
            for x in range(map.maxX + 1):
                coords = Coords(x, y)
                if coords in self.blizzards:
                    result += self.blizzards[coords]
                    result += " " * (4 - len(self.blizzards[coords]))
                else:
                    result += ".   "
        return result

    def __hash__(self):
        return hash(self.hashable_map())

    def __lt__(self, other):
        # make a string of the map and hash that
        if self.maxX != other.maxX:
            return self.maxX < other.maxX
        elif self.maxY != other.maxY:
            return self.maxY < other.maxY

        return self.hashable_map() < other.hashable_map()


def parse_map(lines: list[str]) -> Map:
    blizzards = {}
    for rowIdx, line in enumerate(lines):
        for idx, char in enumerate(line.strip()):
            if char in "<v>^":
                loc = Coords(idx, rowIdx)
                blizzards[loc] = "".join(sorted(blizzards.get(loc, "") + char))
        maxX = idx
    maxY = rowIdx

    return Map(blizzards, maxX, maxY)


UP = Coords(0, -1)
LEFT = Coords(-1, 0)
RIGHT = Coords(1, 0)
DOWN = Coords(0, 1)
STANDSTILL = Coords(0, 0)

blizzard_directions = {
    "^": UP,
    ">": RIGHT,
    "<": LEFT,
    "v": DOWN,
}
move_options = [UP, LEFT, RIGHT, DOWN, STANDSTILL]


def manhattan_distance(a: Coords, b: Coords) -> int:
    return abs(a.x - b.x) + abs(a.y - b.y)


def move_blizzards(map: Map) -> Map:
    new_blizzards = {}
    for blizzard_loc, directions in map.blizzards.items():
        for direction in directions:
            movement = blizzard_directions[direction]
            new_loc = Coords(blizzard_loc.x + movement.x, blizzard_loc.y + movement.y)
            if new_loc.x == 0:
                new_loc = Coords(map.maxX - 1, new_loc.y)
            elif new_loc.y == 0:
                new_loc = Coords(new_loc.x, map.maxY - 1)
            elif new_loc.x == map.maxX:
                new_loc = Coords(1, new_loc.y)
            elif new_loc.y == map.maxY:
                new_loc = Coords(new_loc.x, 1)
            new_blizzards[new_loc] = "".join(
                sorted(new_blizzards.get(new_loc, "") + direction)
            )
    return Map(new_blizzards, map.maxX, map.maxY)


def possible_moves(location: Coords, map: Map) -> list[Coords]:
    moves = []
    for move in move_options:
        new_loc = Coords(location.x + move.x, location.y + move.y)
        if (
            new_loc.x > 0
            and new_loc.y > 0
            and new_loc.x < map.maxX
            and new_loc.y < map.maxY
        ):
            if new_loc not in map.blizzards:
                moves.append(new_loc)
        elif (new_loc.x == 1 and new_loc.y == 0) or (
            (new_loc.x == map.maxX - 1 and new_loc.y == map.maxY)
        ):
            moves.append(new_loc)
    return moves


@dataclass(frozen=True, order=True)
class SearchState:
    location: Coords
    blizzard_index: int


def a_star_search(
    start: Coords, initial_blizzard_index: int, blizzards: list[Map], dest: Coords
) -> int:
    open_set: list[tuple[int, SearchState]] = []
    initial_state = SearchState(start, initial_blizzard_index)
    heapq.heappush(open_set, (initial_blizzard_index, initial_state))

    gScore: dict[SearchState, int] = {}
    gScore[initial_state] = 0
    fScore: dict[SearchState, int] = {}
    fScore[initial_state] = manhattan_distance(start, dest)
    explored: set[SearchState] = set()

    while len(open_set) > 0:
        _, current = heapq.heappop(open_set)

        if current in explored:
            continue
        if current.location == dest:
            return gScore[current]

        explored.add(current)

        next_blizzard_index = (current.blizzard_index + 1) % len(blizzards)
        moves = possible_moves(current.location, blizzards[next_blizzard_index])
        for move in moves:
            new_gscore = gScore[current] + 1
            new_state = SearchState(move, next_blizzard_index)
            if new_state not in gScore or new_gscore < gScore[new_state]:
                gScore[new_state] = new_gscore
                fScore[new_state] = new_gscore + manhattan_distance(move, dest)
                heapq.heappush(open_set, (fScore[new_state], new_state))

    return None


with open("day24.txt", "r") as file:
    map = parse_map(file.readlines())

    blizzards = [map]
    while True:
        map = move_blizzards(map)
        if map == blizzards[0]:
            break
        blizzards.append(map)

    result = a_star_search(Coords(1, 0), 0, blizzards, Coords(map.maxX - 1, map.maxY))
    result2 = a_star_search(
        Coords(map.maxX - 1, map.maxY), result % len(blizzards), blizzards, Coords(1, 0)
    )
    result3 = a_star_search(
        Coords(1, 0),
        (result + result2) % len(blizzards),
        blizzards,
        Coords(map.maxX - 1, map.maxY),
    )
    print(result, result2, result3)
    print(result + result2 + result3)
