from dataclasses import dataclass
import re
from copy import deepcopy


@dataclass
class TreeNode:
    val: int | None = None
    left: str = ""
    right: str = ""
    op: str = ""


def parse_monkeys(lines: list[str]) -> dict[str, TreeNode]:
    result = {}
    for line in lines:
        vals = re.split(" |:", line)
        if len(vals) == 3:
            assert vals[0] not in result
            result[vals[0]] = TreeNode(val=int(vals[2].strip()))
        else:
            assert len(vals) == 5
            result[vals[0]] = TreeNode(
                left=vals[2].strip(), right=vals[4].strip(), op=vals[3].strip()
            )
    return result


def eval_tree(name: str, monkeys: dict[str, TreeNode]):
    if name in monkeys:
        node = monkeys[name]
        if node.val is not None:
            return node.val
        else:
            leftval = eval_tree(node.left, monkeys)
            rightval = eval_tree(node.right, monkeys)
            if leftval is None or rightval is None:
                return None
            else:
                match node.op:
                    case "+":
                        node.val = leftval + rightval
                    case "-":
                        node.val = leftval - rightval
                    case "*":
                        node.val = leftval * rightval
                    case "/":
                        node.val = leftval // rightval
                return node.val
    else:
        return None


def find_value_to_equal(
    node: TreeNode, value: int, monkeys: dict[str, TreeNode], key: str
) -> int:

    leftVal = eval_tree(node.left, monkeys)
    rightVal = eval_tree(node.right, monkeys)

    if leftVal is None:
        match node.op:
            case "+":
                next_value = value - rightVal
            case "-":
                next_value = value + rightVal
            case "*":
                next_value = value // rightVal
            case "/":
                next_value = value * rightVal
        if node.left == key:
            return next_value
        else:
            node = monkeys[node.left]
            return find_value_to_equal(node, next_value, monkeys, key)
    else:
        match node.op:
            case "+":
                next_value = value - leftVal
            case "-":
                next_value = leftVal - value
            case "*":
                next_value = value // leftVal
            case "/":
                next_value = leftVal // value
        if node.right == key:
            return next_value
        else:
            node = monkeys[node.right]
            return find_value_to_equal(node, next_value, monkeys, key)


with open("day21.txt", "r") as file:
    monkeys = parse_monkeys(file.readlines())
    monkeys_part_one = deepcopy(monkeys)
    val = eval_tree("root", monkeys_part_one)
    print(val)

    monkeys_part_two = deepcopy(monkeys)
    del monkeys_part_two["humn"]
    curNode = monkeys["root"]

    leftVal = eval_tree(curNode.left, monkeys_part_two)
    rightVal = eval_tree(curNode.right, monkeys_part_two)
    if leftVal is None:
        node = monkeys_part_two[curNode.left]
        val = find_value_to_equal(node, rightVal, monkeys_part_two, "humn")
    else:
        node = monkeys_part_two[curNode.right]
        val = find_value_to_equal(node, leftVal, monkeys_part_two, "humn")
    print(val)
