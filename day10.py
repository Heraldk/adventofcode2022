from typing import List
from dataclasses import dataclass


@dataclass
class Instruction:
    operator: str
    param: int


def parse_program(lines: List[str]) -> List[Instruction]:
    instructions = []
    for line in lines:
        vals = line.strip().split(" ")
        assert vals[0] == "noop" or vals[0] == "addx"
        instructions.append(
            Instruction(operator=vals[0], param=int(vals[1]) if len(vals) > 1 else -1)
        )

    return instructions


def exec_program(program: List[Instruction]):
    registerX = 1
    pc = 0
    cycle = 1
    exec_count = 0

    interesting = []
    display = []

    row = ""
    while pc < len(program):
        if cycle in [20, 60, 100, 140, 180, 220]:
            interesting.append(cycle * registerX)

        pixel = (cycle - 1) % 40
        if registerX - 1 <= pixel and pixel <= registerX + 1:
            row = row + "#"
        else:
            row = row + "."

        if pixel == 39:
            display.append(row)
            row = ""

        if exec_count > 0:  # still waiting for a prior statement to finish executing
            exec_count -= 1
            assert program[pc].operator == "addx"
            registerX += program[pc].param
            pc += 1
        else:
            # exec new instruction
            if program[pc].operator == "noop":
                pc += 1
            elif program[pc].operator == "addx":
                exec_count = 1

        cycle += 1

    print(sum(interesting))
    for row in display:
        print(row)


with open("day10.txt", "r") as file:
    program = parse_program(file.readlines())
    exec_program(program)
