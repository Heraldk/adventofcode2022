from typing import List, Optional, Dict, Set, Tuple
from dataclasses import dataclass
import functools


@dataclass
class Packet:
    items: List["Packet"] | None
    value: Optional[int]


def parse_packet(remaining_str: str) -> Tuple[Packet, int]:
    ix = 1
    items = []
    assert remaining_str[0] == "["

    while ix < len(remaining_str):
        if remaining_str[ix] == "]":
            return Packet(items=items, value=None), ix + 1
        elif remaining_str[ix] == "[":
            next_packet, length = parse_packet(remaining_str[ix:])
            items.append(next_packet)
            ix += length
        elif remaining_str[ix].isdigit():
            # input has only small numbers, so this is a small hack :)
            length = 2 if remaining_str[ix + 1].isdigit() else 1
            items.append(Packet(items=None, value=int(remaining_str[ix : ix + length])))
            ix += length
        else:
            assert remaining_str[ix] == ","
            ix += 1
    return Packet(items=items, value=None), 0


def compare_packets(packet1: Packet, packet2: Packet) -> int:
    ### returns 0 if the packets are equal, returns -1 if packet1 is less than packet2, returns 1 if packet1 is greater than packet2
    if packet1.items is None and packet2.items is None:
        assert packet1.value is not None and packet2.value is not None
        val = packet1.value - packet2.value
        if val < 0:
            val = -1
        if val > 0:
            val = 1
        return val
    if packet1.items is None:
        packet1.items = [Packet(items=None, value=packet1.value)]
    if packet2.items is None:
        packet2.items = [Packet(items=None, value=packet2.value)]

    max_len = max(len(packet1.items), len(packet2.items))
    for ix in range(max_len):
        if ix >= len(packet1.items):
            return -1
        elif ix >= len(packet2.items):
            return 1
        compare = compare_packets(packet1.items[ix], packet2.items[ix])
        if compare != 0:
            return compare

    return 0


def parse_packets(lines: List[str]) -> List[Packet]:
    packets = []
    for line in lines:
        if line.strip() == "":
            continue
        packet, _ = parse_packet(line)
        packets.append(packet)
    return packets


with open("day13.txt", "r") as file:
    packets = parse_packets(file.readlines())
    ix = 0
    comparisonIx = 1
    total = 0
    while ix < len(packets):
        comparison = compare_packets(packets[ix], packets[ix + 1])
        if comparison <= 0:
            total += comparisonIx
        ix += 2
        comparisonIx += 1
    print(total)

    # add decoder packets
    next_packet, _ = parse_packet("[[2]]")
    packets.append(next_packet)
    next_packet, _ = parse_packet("[[6]]")
    packets.append(next_packet)

    packets.sort(key=functools.cmp_to_key(compare_packets))

    index1 = -1
    index2 = -1
    for ix, packet in enumerate(packets):
        if packet.items is not None and len(packet.items) == 1:
            first_packet = packet.items[0]
            if first_packet.items is not None and len(first_packet.items) == 1:
                if first_packet.items[0].value == 2:
                    index1 = ix + 1
                elif first_packet.items[0].value == 6:
                    index2 = ix + 1
    print(index1, index2, index1 * index2)
