from typing import Tuple, List
from dataclasses import dataclass
from copy import deepcopy


@dataclass
class Instruction:
    count: int
    src: int
    dest: int


def parse_input(lines: List[str]) -> Tuple[List[List[str]], List[Instruction]]:
    is_reading_starting_state = True
    stacks = [[] for _ in range(0, 9)]  # hardcoded to 9 columns
    instructions = []
    for line in lines:
        if is_reading_starting_state:
            if line.startswith(" 1"):
                continue
            elif len(line.strip()) == 0:
                is_reading_starting_state = False
            else:
                index = 0
                for x in range(0, len(line), 4):
                    if line[x] == "[":
                        stacks[index].append(line[x + 1])
                    index += 1
        else:
            vals = line.split(" ")
            instructions.append(
                Instruction(
                    count=int(vals[1].strip()),
                    src=int(vals[3].strip()) - 1,  # convert index to zero based
                    dest=int(vals[5].strip()) - 1,  # convert index to zero based
                )
            )
    for stack in stacks:
        stack.reverse()  # reversed for efficiency
    return stacks, instructions


def run_instructions(
    starting: List[List[str]], instructions: List[Instruction], move_one_at_a_time: bool
) -> List[List[str]]:
    state = deepcopy(starting)
    for instr in instructions:
        if move_one_at_a_time:
            for _ in range(instr.count):
                assert len(state[instr.src]) > 0
                item = state[instr.src].pop()
                state[instr.dest].append(item)
        else:
            items = state[instr.src][-instr.count :]
            state[instr.dest].extend(items)
            del state[instr.src][-instr.count :]
    return state


with open("day05.txt", "r") as file:
    stacks, instructions = parse_input(file.readlines())
    result = run_instructions(stacks, instructions, move_one_at_a_time=True)
    top_of_each = "".join([x[-1] for x in result])
    print(top_of_each)

    result = run_instructions(stacks, instructions, move_one_at_a_time=False)
    top_of_each = "".join([x[-1] for x in result])
    print(top_of_each)
