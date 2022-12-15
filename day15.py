from dataclasses import dataclass
import re


@dataclass(frozen=True)
class Coords:
    x: int
    y: int


@dataclass
class Sensor:
    location: Coords
    closest_beacon: Coords


def parse_coords(coord: str) -> Coords:
    vals = re.split("x=|, y=", coord)
    return Coords(x=int(vals[1]), y=int(vals[2]))


def parse_input(lines: list[str]) -> list[Sensor]:
    items = []
    for line in lines:
        vals = re.split("Sensor at |: closest beacon is at ", line)
        coords = [parse_coords(x.strip()) for x in vals if x != ""]
        items.append(Sensor(location=coords[0], closest_beacon=coords[1]))
    return items


def manhattan_distance(loc1: Coords, loc2: Coords) -> int:
    return abs(loc1.y - loc2.y) + abs(loc1.x - loc2.x)


def next_covered_in_row(
    loc: Coords, sensors: list[Sensor]
) -> tuple[Coords, Sensor] | None:
    closests_non_coverage = None
    relevant_sensor = None
    for sensor in sensors:
        coverage_dist = manhattan_distance(sensor.closest_beacon, sensor.location)
        ydiff = abs(loc.y - sensor.location.y)
        if ydiff <= coverage_dist:
            remaining = coverage_dist - ydiff
            minXVal = sensor.location.x - remaining
            if minXVal > loc.x:
                xloc = minXVal
            elif minXVal <= loc.x and sensor.location.x + remaining > loc.x:
                xloc = loc.x + 1
            else:
                continue
            if closests_non_coverage is None or closests_non_coverage.x > xloc:
                closests_non_coverage = Coords(x=xloc, y=loc.y)
                relevant_sensor = sensor
    return (
        None
        if closests_non_coverage is None
        else (closests_non_coverage, relevant_sensor)
    )


def last_covered_by_sensor(loc: Coords, sensor: Sensor) -> Coords:
    coverage_dist = manhattan_distance(sensor.closest_beacon, sensor.location)
    ydiff = abs(loc.y - sensor.location.y)
    assert ydiff <= coverage_dist
    xloc = sensor.location.x + (coverage_dist - ydiff)
    return Coords(x=xloc, y=loc.y)


def count_nonbeacons(
    row: int,
    sensors: list[Sensor],
) -> int:
    col = -100000000
    next_covered = next_covered_in_row(Coords(x=col, y=row), sensors)
    total_covered_locations = 0
    while next_covered is not None:
        loc, sensor = next_covered
        last = last_covered_by_sensor(loc, sensor)
        leftmost = loc.x
        rightmost = last.x
        total_covered_locations += (rightmost - leftmost) + 1
        # if the beacon is actually at either end of this subtract one since that is not a non-beacon
        if loc == sensor.closest_beacon or last == sensor.closest_beacon:
            total_covered_locations -= 1
        # print(loc, last, leftmost, rightmost, total_covered_locations)
        next_covered = next_covered_in_row(last, sensors)
    return total_covered_locations


def find_gap(
    row: int,
    sensors: list[Sensor],
    minX: int,
    maxX: int,
) -> Coords:
    col = minX - 1
    next_covered = next_covered_in_row(Coords(x=col, y=row), sensors)
    prev = None
    while next_covered is not None:
        loc, sensor = next_covered
        last = last_covered_by_sensor(loc, sensor)
        leftmost = max(minX, loc.x)
        rightmost = min(last.x, maxX)
        if prev is not None and prev.x + 1 < loc.x:
            return Coords(prev.x + 1, row)
        # print(loc, last, leftmost, rightmost, total_covered_locations)
        next_covered = next_covered_in_row(last, sensors)
        if next_covered is not None and next_covered[0].x > maxX:
            next_covered = None
        prev = last
    return None


with open("day15 sample.txt", "r") as file:
    sensors = parse_input(file.readlines())

    print(count_nonbeacons(10, sensors))

    for row in range(0, 20):
        loc = find_gap(row, sensors, 0, 20)
        if loc is not None:
            print(loc.x, loc.y, loc.x * 4000000 + loc.y)


with open("day15.txt", "r") as file:
    sensors = parse_input(file.readlines())

    print(count_nonbeacons(2000000, sensors))

    # so this is really slow, but it does get the right answer
    for row in range(0, 4000000):
        loc = find_gap(row, sensors, 0, 4000000)
        if loc is not None:
            print(loc.x, loc.y, loc.x * 4000000 + loc.y)
            break
