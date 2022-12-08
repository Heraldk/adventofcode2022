from typing import List, Tuple
import math


def parse_input(lines: List[str]) -> List[List[int]]:
    grid = []
    for line in lines:
        line = line.strip()
        grid.append([int(x) for x in line])
    assert len(grid) == len(grid[0])  # assume it is square for simplicity's sake
    return grid


def update_visibility(
    x: int,
    y: int,
    grid: List[List[int]],
    cur_max_height: int,
    visible_checker: List[List[bool]],
) -> Tuple[int, int]:
    new_max_height = cur_max_height
    if grid[y][x] > cur_max_height:
        new_max_height = grid[y][x]
        if not visible_checker[y][x]:
            visible_checker[y][x] = True
            return 1, new_max_height
    return 0, new_max_height


def count_visible(grid: List[List[int]]) -> int:
    visible_checker = [[False for _ in grid[0]] for _ in grid]
    visible_count = 0

    for y in range(0, len(grid)):
        max_height_left = -1
        max_height_right = -1
        for x in range(0, len(grid)):
            incr_right, max_height_right = update_visibility(
                x, y, grid, max_height_right, visible_checker
            )
            incr_left, max_height_left = update_visibility(
                len(grid) - x - 1, y, grid, max_height_left, visible_checker
            )
            visible_count += incr_right + incr_left

    for x in range(0, len(grid)):
        max_height_up = -1
        max_height_down = -1
        for y in range(0, len(grid)):
            incr_down, max_height_down = update_visibility(
                x, y, grid, max_height_down, visible_checker
            )
            incr_up, max_height_up = update_visibility(
                x, len(grid) - y - 1, grid, max_height_up, visible_checker
            )
            visible_count += incr_up + incr_down

    return visible_count


def calc_scenic_score(x: int, y: int, grid: List[List[int]]) -> int:
    directions = [(-1, 0), (0, -1), (1, 0), (0, 1)]
    tree_counts = []
    for modX, modY in directions:
        locX, locY = x, y
        start_height = grid[locY][locX]
        locX += modX
        locY += modY
        tree_count = 0
        while locX >= 0 and locY >= 0 and locX < len(grid) and locY < len(grid):
            tree_count += 1
            if grid[locY][locX] >= start_height:
                break
            locX += modX
            locY += modY

        tree_counts.append(tree_count)
    return math.prod(tree_counts)


with open("day08.txt", "r") as file:

    grid = parse_input(file.readlines())
    print(count_visible(grid))

    max_score = 0
    for y in range(len(grid)):
        for x in range(len(grid)):
            max_score = max(max_score, calc_scenic_score(x, y, grid))
    print(max_score)
