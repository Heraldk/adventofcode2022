from dataclasses import dataclass
import re
import functools


@dataclass(frozen=True)
class Valve:
    name: str
    rate: int
    neighbours: list[str]


def parse_input(lines: list[str]) -> dict[str, Valve]:
    valves = {}
    for line in lines:
        vals = re.split(
            "Valve | has flow rate=|; tunnels lead to valves |; tunnel leads to valve ",
            line.strip(),
        )
        name = vals[1]
        rate = int(vals[2])
        neighbours = [val.strip() for val in vals[3].split(",")]
        valves[name] = Valve(name=name, rate=rate, neighbours=neighbours)
    return valves


valves: dict[str, Valve] = {}


def all_pairs_shortest_path(valves: dict[str, Valve]) -> dict[str, dict[str, int]]:
    distances = {}
    for src in valves.keys():
        distances[src] = {}

    for src in valves.values():
        for dst in src.neighbours:
            distances[src.name][dst] = 1
        distances[src.name][src.name] = 0

    for k in valves:
        for i in valves:
            for j in valves:
                if k in distances[i] and j in distances[k]:
                    if (
                        j not in distances[i]
                        or distances[i][j] > distances[i][k] + distances[k][j]
                    ):
                        distances[i][j] = distances[i][k] + distances[k][j]
    return distances


def calc_flow(
    loc: str,
    rem_time: int,
    current_flow_rate: int,
    closed_valves: list[str],
    valves: dict[str, Valve],
    distances=dict[str, dict[str, int]],
) -> int:
    max_flow = 0
    # consider each closed valve: walking over to it and opening it
    for closed_valve in closed_valves:
        time_to_open = distances[loc][closed_valve] + 1
        if rem_time >= time_to_open:
            new_closed_valves = list(closed_valves)
            new_closed_valves.remove(closed_valve)
            flow = calc_flow(
                closed_valve,
                rem_time - time_to_open,
                current_flow_rate + valves[closed_valve].rate,
                new_closed_valves,
                valves,
                distances,
            )
            # how much flows out while we're walking there and opening the valve
            flow += time_to_open * current_flow_rate
            max_flow = max(flow, max_flow)

    # also just consider sitting put and not going anywhere
    flow = rem_time * current_flow_rate
    max_flow = max(flow, max_flow)

    return max_flow


def calc_flow_part_2(
    loc: str,
    loc_other: str,
    time_to_dest_other: int,
    rem_time: int,
    current_flow_rate: int,
    closed_valves: list[str],
    valves: dict[str, Valve],
    distances=dict[str, dict[str, int]],
) -> int:
    max_flow = 0
    # consider each closed valve: walking over to it and opening it
    for closed_valve in closed_valves:
        time_to_open = distances[loc][closed_valve] + 1
        if rem_time >= time_to_open:
            new_closed_valves = list(closed_valves)
            new_closed_valves.remove(closed_valve)

            # wrinkle here is need to know which of us gets to the valve first
            if time_to_dest_other >= 0 and time_to_open > time_to_dest_other:
                flow = calc_flow_part_2(
                    loc_other,
                    closed_valve,
                    time_to_open - time_to_dest_other,
                    rem_time - time_to_dest_other,
                    current_flow_rate + valves[loc_other].rate,
                    new_closed_valves,
                    valves,
                    distances,
                )
                flow += time_to_dest_other * current_flow_rate
            else:
                flow = calc_flow_part_2(
                    closed_valve,
                    loc_other,
                    time_to_dest_other - time_to_open,
                    rem_time - time_to_open,
                    current_flow_rate + valves[closed_valve].rate,
                    new_closed_valves,
                    valves,
                    distances,
                )
                flow += time_to_open * current_flow_rate
            max_flow = max(flow, max_flow)

    # also just consider sitting put and not going anywhere
    flow = 0
    if time_to_dest_other >= 0:
        flow = calc_flow_part_2(
            loc_other,
            loc,
            -1,
            rem_time - time_to_dest_other,
            current_flow_rate + valves[loc_other].rate,
            closed_valves,
            valves,
            distances,
        )
        flow += time_to_dest_other * current_flow_rate
        max_flow = max(flow, max_flow)
    else:
        flow += rem_time * current_flow_rate
        max_flow = max(flow, max_flow)

    return max_flow


with open("day16.txt", "r") as file:
    valves = parse_input(file.readlines())
    # print(calc_flow(30, 0, dict(), "AA", valves))
    distances = all_pairs_shortest_path(valves)
    flow = calc_flow(
        "AA", 30, 0, [x.name for x in valves.values() if x.rate > 0], valves, distances
    )
    print(flow)

    flow = calc_flow_part_2(
        "AA",
        "AA",
        0,
        26,
        0,
        [x.name for x in valves.values() if x.rate > 0],
        valves,
        distances,
    )
    print(flow)
