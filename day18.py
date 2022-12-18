from dataclasses import dataclass
import re
import functools


@dataclass(frozen=True)
class Coords:
    x: int
    y: int
    z: int


def parse_cubes(input: list[str]) -> dict[bool]:
    cubes = {}
    for line in input:
        vals = line.strip().split(",")
        cubes[Coords(int(vals[0]), int(vals[1]), int(vals[2]))] = True
    return cubes


neighbours = [
    Coords(0, 0, 1),
    Coords(0, 1, 0),
    Coords(1, 0, 0),
    Coords(-1, 0, 0),
    Coords(0, -1, 0),
    Coords(0, 0, -1),
]


def count_openfaces(cubes: dict[bool]) -> int:
    openfaces = 0
    for cube in cubes.keys():
        for neighbour in neighbours:
            check = Coords(
                cube.x + neighbour.x, cube.y + neighbour.y, cube.z + neighbour.z
            )
            if check not in cubes:
                openfaces += 1
    return openfaces


def fill_outside(cubes: dict[bool], minVal: int, maxVal: int) -> int:
    queue = {Coords(minVal, 0, 0)}
    outside = {}
    while len(queue) > 0:
        current = queue.pop()
        outside[current] = True
        for neighbour in neighbours:
            coords = Coords(
                current.x + neighbour.x,
                current.y + neighbour.y,
                current.z + neighbour.z,
            )
            if (
                coords not in cubes
                and coords not in queue
                and coords not in outside
                and coords.x >= minVal
                and coords.y >= minVal
                and coords.z >= minVal
                and coords.x <= maxVal
                and coords.y <= maxVal
                and coords.z <= maxVal
            ):
                queue.add(coords)
    return outside


def count_externalfaces(cubes: dict[bool], outside: dict[bool]) -> int:
    externalfaces = 0
    for cube in cubes.keys():
        for neighbour in neighbours:
            check = Coords(
                cube.x + neighbour.x, cube.y + neighbour.y, cube.z + neighbour.z
            )
            if check in outside:
                externalfaces += 1
    return externalfaces


with open("day18.txt", "r") as file:
    cubes = parse_cubes(file.readlines())
    print(count_openfaces(cubes))

    maxVal = max([max(cube.x, cube.y, cube.z) for cube in cubes])
    minVal = min([min(cube.x, cube.y, cube.z) for cube in cubes])

    outside = fill_outside(cubes, minVal - 1, maxVal + 1)
    print(count_externalfaces(cubes, outside))
