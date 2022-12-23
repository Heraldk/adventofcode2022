from dataclasses import dataclass


class LinkedList:
    def __init__(self):
        self.head: Node = None
        self.tail: Node = None

    def __repr__(self):
        node = self.head
        nodes = []
        while node is not None:
            nodes.append(str(node.number))
            node = node.next
        nodes.append("None")

        node = self.tail
        rev_nodes = []
        while node is not None:
            rev_nodes.append(str(node.number))
            node = node.prev
        rev_nodes.append("None")

        return " -> ".join(nodes) + " reverse: " + " -> ".join(rev_nodes)


class Node:
    def __init__(self, id: int, number):
        self.id = id
        self.number = number
        self.next = None
        self.prev = None

    def __repr__(self):
        return str(self.number)


def parse_nums(lines: list[str], multiplier=1) -> tuple[LinkedList, dict[int, Node]]:
    lookup = {}
    myList = LinkedList()
    curNode = None
    for pos, line in enumerate(lines):
        if curNode:
            curNode.next = Node(pos, int(line.strip()) * multiplier)
            curNode.next.prev = curNode
            curNode = curNode.next
            lookup[pos] = curNode
        else:
            myList.head = Node(pos, int(line.strip()) * multiplier)
            curNode = myList.head
            lookup[pos] = curNode
    myList.tail = curNode

    return myList, lookup


def mix(myList: LinkedList, lookup: dict[int, Node]):
    for id in range(len(lookup.keys())):
        node = lookup[id]
        if node.number != 0:
            if node.prev is not None:
                node.prev.next = node.next
            if node.next is not None:
                node.next.prev = node.prev
            if myList.head.id == node.id:
                myList.head = node.next
            elif myList.tail.id == node.id:
                myList.tail = node.prev
            curNode = node

            if node.number > 0:
                num_iterations = node.number % (len(lookup.keys()) - 1)
            else:
                num_iterations = -node.number % (len(lookup.keys()) - 1) + 1

            if node.number > 0:
                for _ in range(num_iterations):
                    curNode = curNode.next
                    if curNode == None:
                        curNode = myList.head

            elif node.number < 0:
                for _ in range(num_iterations):
                    curNode = curNode.prev
                    if curNode == None:
                        curNode = myList.tail

            node.next = curNode.next
            node.prev = curNode
            if curNode.next is not None:
                curNode.next.prev = node
            curNode.next = node
            if curNode.id == myList.tail.id:
                myList.tail = node


def getValsAfterZero(myList: LinkedList, indexes: list[int]):
    node = myList.head
    while node.number != 0:
        node = node.next

    interestingVals = []
    for index in range(max(indexes)):
        if node.next is None:
            node = myList.head
        else:
            node = node.next
        if index + 1 in indexes:
            interestingVals.append(node.number)
    return interestingVals


with open("day20.txt", "r") as file:
    numList, lookup = parse_nums(file.readlines())
    mix(numList, lookup)
    vals = getValsAfterZero(numList, [1000, 2000, 3000])
    print(vals, sum(vals))

with open("day20.txt", "r") as file:
    numList, lookup = parse_nums(file.readlines(), multiplier=811589153)
    for _ in range(10):
        mix(numList, lookup)
    vals = getValsAfterZero(numList, [1000, 2000, 3000])
    print(vals, sum(vals))
