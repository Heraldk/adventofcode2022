from typing import List, Optional, Dict, Set
from dataclasses import dataclass
from itertools import groupby
import re
from copy import deepcopy
import math


@dataclass
class Monkey:
    items: List[int]
    op: str  # the operator
    op1: Optional[int]  # operand 1: None if we use the old value
    op2: Optional[int]  # operand 2: None if we use the old value
    test_mod: int
    true_target: int
    false_target: int


def parse_monkey(lines: List[str]) -> Monkey:
    items_str = lines[1][len("  Starting items: ") :].strip()
    items = [int(x) for x in re.split(", ", items_str)]
    op_row = lines[2][len("  Operation: new = ") :].strip()
    ops = op_row.split(" ")
    op1 = None if ops[0] == "old" else int(ops[0])
    op2 = None if ops[2] == "old" else int(ops[2])
    test_mod = int(lines[3][len("  Test: divisible by ") :].strip())
    true_target = int(lines[4][len("    If true: throw to monkey ") :].strip())
    false_target = int(lines[5][len("    If false: throw to monkey ") :].strip())
    return Monkey(
        items=items,
        op=ops[1],
        op1=op1,
        op2=op2,
        test_mod=test_mod,
        true_target=true_target,
        false_target=false_target,
    )


def parse_input(lines: List[str]) -> List[Monkey]:
    monkeys = []
    id = 0
    monkey_input = [
        list(y) for x, y in groupby(lines, key=lambda z: z == "\n") if not x
    ]
    for monkey in monkey_input:
        parsed = parse_monkey(monkey)
        monkeys.append(parsed)

    return monkeys


def get_worry(item: int, monkey: Monkey) -> int:
    op1 = monkey.op1 if monkey.op1 is not None else item
    op2 = monkey.op2 if monkey.op2 is not None else item
    if monkey.op == "*":
        worry = op1 * op2
    elif monkey.op == "+":
        worry = op1 + op2
    else:
        raise ValueError()
    return worry


def throw_items_round(
    monkeys: List[Monkey],
    inspect_count: List[int],
    divide_worry: bool = True,
    mod_worry: int = -1,
):
    for idx, monkey in enumerate(monkeys):
        items = monkey.items
        monkey.items = []
        for item in items:
            worry = get_worry(item, monkey)
            if divide_worry:
                worry //= 3
            elif mod_worry > 0:
                worry %= mod_worry
            if worry % monkey.test_mod == 0:
                monkeys[monkey.true_target].items.append(worry)
            else:
                monkeys[monkey.false_target].items.append(worry)
            inspect_count[idx] += 1


def throw_items_part1(monkeys: List[Monkey]):
    inspect_count = [0 for x in monkeys]
    for _ in range(20):
        throw_items_round(monkeys, inspect_count)
    inspect_count.sort(reverse=True)
    print(inspect_count[0] * inspect_count[1])


def throw_items_part2(monkeys: List[Monkey]):
    inspect_count = [0 for x in monkeys]
    # trick here is to keep the item's worry level to numbers that we can still do math on in a reasonable amount of time
    # all the mod tests each monkey performs is on a prime number. If we multiply these numbers together then whenever
    # an item's worry gets above this multiple we can mod it by this multiple to retain the same mod properties across
    # all these numbers.
    mod_worry = math.prod([x.test_mod for x in monkeys])

    for idx in range(10000):
        throw_items_round(
            monkeys, inspect_count, divide_worry=False, mod_worry=mod_worry
        )
    inspect_count.sort(reverse=True)
    print(inspect_count[0] * inspect_count[1])


with open("day11.txt", "r") as file:
    monkey_input = parse_input(file.readlines())
    monkeys = deepcopy(monkey_input)
    throw_items_part1(monkeys)

    monkeys = deepcopy(monkey_input)
    throw_items_part2(monkeys)
