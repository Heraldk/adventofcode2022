from typing import Tuple, Dict
from dataclasses import dataclass


@dataclass(frozen=True)
class Position:
    x: int
    y: int


move_lookup = {"U": (0, 1), "D": (0, -1), "L": (-1, 0), "R": (1, 0)}


def move(
    head: Position, tail: Position, movement: str, visited: Dict[Position, bool]
) -> Tuple[Position, Position]:
    move_vals = movement.strip().split(" ")
    direction = move_vals[0]
    assert direction in move_lookup
    incrX, incrY = move_lookup[direction]
    distance = int(move_vals[1])
    for _ in range(distance):
        head = Position(x=head.x + incrX, y=head.y + incrY)
        if abs(head.x - tail.x) == 2:
            tail = Position(x=head.x - 1 if head.x > tail.x else head.x + 1, y=head.y)
        elif abs(head.y - tail.y) == 2:
            tail = Position(x=head.x, y=head.y - 1 if head.y > tail.y else head.y + 1)
        visited[tail] = True
    return head, tail


def move_part_2(
    ropes: Dict[int, Position], movement: str, visited: Dict[Position, bool]
) -> Dict[int, Position]:
    move_vals = movement.strip().split(" ")
    direction = move_vals[0]
    assert direction in move_lookup
    incrX, incrY = move_lookup[direction]
    distance = int(move_vals[1])
    new_ropes = ropes
    for _ in range(distance):
        head = new_ropes[0]
        head = Position(x=head.x + incrX, y=head.y + incrY)
        new_ropes[0] = head
        for x in range(len(ropes) - 1):
            tail = new_ropes[x + 1]
            if abs(head.x - tail.x) == 2 and abs(head.y - tail.y) == 2:
                tail = Position(
                    x=head.x - 1 if head.x > tail.x else head.x + 1,
                    y=head.y - 1 if head.y > tail.y else head.y + 1,
                )
            elif abs(head.x - tail.x) == 2:
                tail = Position(
                    x=head.x - 1 if head.x > tail.x else head.x + 1, y=head.y
                )
            elif abs(head.y - tail.y) == 2:
                tail = Position(
                    x=head.x, y=head.y - 1 if head.y > tail.y else head.y + 1
                )
            new_ropes[x + 1] = tail
            head = tail
        visited[tail] = True

    return new_ropes


with open("day09.txt", "r") as file:
    visited = {}
    head = Position(x=0, y=0)
    tail = Position(x=0, y=0)
    lines = file.readlines()
    for movement in lines:
        head, tail = move(head, tail, movement, visited)
    print(len(visited))

    # re-calculate part 1 with part 2's solution to double check!
    ropes = {x: Position(x=0, y=0) for x in range(2)}
    visited = {}
    for movement in lines:
        ropes = move_part_2(ropes, movement, visited)
    print(len(visited))

    ropes = {x: Position(x=0, y=0) for x in range(10)}
    visited = {}
    for movement in lines:
        ropes = move_part_2(ropes, movement, visited)
    print(len(visited))
