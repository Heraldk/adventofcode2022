from dataclasses import dataclass
import re
import functools


@dataclass(frozen=True)
class Coords:
    x: int
    y: int


@dataclass(frozen=True)
class Piece:
    # relative locations to left-most square that makes up this piece
    locs: list[Coords]
    height: int
    bottom: int = 0


pieces = [
    Piece(locs=[Coords(0, 0), Coords(1, 0), Coords(2, 0), Coords(3, 0)], height=1),
    Piece(
        locs=[Coords(0, 0), Coords(1, 1), Coords(1, 0), Coords(1, -1), Coords(2, 0)],
        bottom=-1,
        height=2,
    ),
    Piece(
        locs=[Coords(0, 0), Coords(1, 0), Coords(2, 0), Coords(2, 1), Coords(2, 2)],
        height=3,
    ),
    Piece(locs=[Coords(0, 0), Coords(0, 1), Coords(0, 2), Coords(0, 3)], height=4),
    Piece(locs=[Coords(0, 0), Coords(0, 1), Coords(1, 0), Coords(1, 1)], height=2),
]


def collides(loc: Coords, piece: Piece, grid: dict[Coords, bool]) -> bool:
    for rel in piece.locs:
        test_loc = Coords(x=loc.x + rel.x, y=loc.y + rel.y)
        if test_loc in grid:
            return True
        if test_loc.x < 0 or test_loc.x >= 7:
            return True
        if test_loc.y < 0:
            return True
    return False


def drop_piece(
    num: int,
    grid: dict[Coords, bool],
    height: int,
    instr_offset: int,
    instructions: str,
) -> tuple[int, int]:
    piece = pieces[num % len(pieces)]
    piece_loc = Coords(x=2, y=height + 3 - piece.bottom)
    idx = instr_offset
    iterations = 0
    while True:
        # blow the piece left or right
        if instructions[idx] == "<":
            new_loc = Coords(x=piece_loc.x - 1, y=piece_loc.y)
        elif instructions[idx] == ">":
            new_loc = Coords(x=piece_loc.x + 1, y=piece_loc.y)
        if not collides(new_loc, piece, grid):
            piece_loc = new_loc
        idx += 1
        if idx >= len(instructions):
            idx = 0
        iterations += 1

        # drop the piece one position
        new_loc = Coords(x=piece_loc.x, y=piece_loc.y - 1)
        if collides(new_loc, piece, grid):
            break
        piece_loc = new_loc

    # fill in the grid with this piece
    new_height = height
    for rel in piece.locs:
        fill_loc = Coords(x=piece_loc.x + rel.x, y=piece_loc.y + rel.y)
        assert fill_loc not in grid
        grid[fill_loc] = True
        new_height = max(fill_loc.y + 1, new_height)

    return iterations, new_height


def print_tower_top(height: int, grid: dict[Coords, bool]):
    for ydiff in range(1, 20):
        if height - ydiff < 0:
            break
        for x in range(7):
            coord = Coords(x, height - ydiff)
            if coord in grid:
                print("#", end="")
            else:
                print(".", end="")
        print()


def top_of_grid_as_string(grid: dict[Coords, bool], height: int, rows: int) -> str:
    top = max(height, rows)
    grid_str = ""
    for row in range(rows):
        yval = top - rows - 1
        for x in range(7):
            coords = Coords(x, yval)
            grid_str = grid_str + f"{'#' if coords in grid else '.'}"
    return grid_str


@dataclass(frozen=True)
class GridHash:
    top_of_grid: str
    piece_id: int
    instruction_id: int


with open("day17.txt", "r") as file:
    grid = {}
    instructions = file.readline().strip()

    idx = 0
    iteration = 0
    height = 0
    while iteration < 2022:
        instructions_used, height = drop_piece(
            iteration, grid, height, idx, instructions
        )
        idx += instructions_used
        if idx >= len(instructions):
            idx %= len(instructions)
        iteration += 1
    print(height)

    grid = {}
    cache: dict[GridHash, tuple[int, int]] = {}
    loop_height = 0
    iteration = 0
    height = 0
    idx = 0
    TARGET_ITERATIONS = 1000000000000
    shortcut = False
    while iteration < TARGET_ITERATIONS:
        grid_str = top_of_grid_as_string(grid, height, 20)
        grid_hash = GridHash(grid_str, iteration % len(pieces), idx)
        if grid_hash in cache and not shortcut:
            orig_iteration, orig_height = cache[grid_hash]
            loop_length = iteration - orig_iteration
            num_loops = (TARGET_ITERATIONS - iteration) // loop_length
            loop_height = num_loops * (height - orig_height)
            iteration += num_loops * loop_length
            shortcut = True
        else:
            cache[grid_hash] = (iteration, height)

        instructions_used, height = drop_piece(
            iteration, grid, height, idx, instructions
        )
        idx += instructions_used
        if idx >= len(instructions):
            idx %= len(instructions)
        iteration += 1
    print(height + loop_height)
