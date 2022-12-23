from dataclasses import dataclass
from copy import deepcopy
import math


@dataclass(frozen=True)
class Blueprint:
    num: int
    robot_costs: list[tuple[int, int, int, int]]
    max_counts: list[int]


def parse_blueprints(lines: list[str]) -> list[Blueprint]:
    blueprints = []
    for line in lines:
        vals = line.split(" ")

        ore_bot_cost = (int(vals[6]), 0, 0, 0)
        clay_bot_cost = (int(vals[12]), 0, 0, 0)
        obsidian_bot_cost = (int(vals[18]), int(vals[21]), 0, 0)
        geode_bot_cost = (int(vals[27]), 0, int(vals[30]), 0)

        blueprints.append(
            Blueprint(
                num=int(vals[1][:-1]),
                robot_costs=[
                    ore_bot_cost,
                    clay_bot_cost,
                    obsidian_bot_cost,
                    geode_bot_cost,
                ],
                max_counts=[
                    max(
                        ore_bot_cost[0],
                        clay_bot_cost[0],
                        obsidian_bot_cost[0],
                        geode_bot_cost[0],
                    ),
                    max(
                        ore_bot_cost[1],
                        clay_bot_cost[1],
                        obsidian_bot_cost[1],
                        geode_bot_cost[1],
                    ),
                    max(
                        ore_bot_cost[2],
                        clay_bot_cost[2],
                        obsidian_bot_cost[2],
                        geode_bot_cost[2],
                    ),
                ],
            )
        )
    return blueprints


def max_geodes(
    rem_time: int,
    resources: list[int],
    robots: list[int],
    blueprint: Blueprint,
    max_so_far: int,
):
    if rem_time == 0:
        return resources[3]  # number of geodes total

    if max_so_far > resources[3] + robots[3] * rem_time + (
        (rem_time - 1) * (rem_time - 1) // 2
    ):
        return -1

    # if we construct no more robots and just wait for them to collect geodes, this is the amount to beat
    current_max = robots[3] * rem_time + resources[3]

    # print(rem_time, resources, robots)

    # consider each robot we could try and target making
    # find out how many minutes until we can afford to make that robot at current resources
    for robotId, costs in enumerate(blueprint.robot_costs):
        time_to_accumulate = 0

        # no need to assemble robot if we already have enough to make the maximum of one resource we would need in one minute
        if robotId != 3 and robots[robotId] >= blueprint.max_counts[robotId]:
            continue
        for resourceId, cost in enumerate(costs):
            if resources[resourceId] < cost:
                if robots[resourceId] > 0:
                    time_to_accumulate = max(
                        time_to_accumulate,
                        math.ceil((cost - resources[resourceId]) / robots[resourceId]),
                    )
                else:
                    time_to_accumulate = None
                    break

        if time_to_accumulate is None or rem_time <= time_to_accumulate:
            continue

        rem_resources = []
        time_passing = time_to_accumulate + 1
        for resourceId, cost in enumerate(costs):
            rem_resources.append(
                resources[resourceId] - cost + robots[resourceId] * time_passing
            )

        next_robots = deepcopy(robots)
        next_robots[robotId] += 1
        next_iter = max_geodes(
            rem_time - time_passing, rem_resources, next_robots, blueprint, current_max
        )
        current_max = max(current_max, next_iter)

    return current_max


with open("day19.txt", "r") as file:
    blueprints = parse_blueprints(file.readlines())
    print(blueprints)

    total_quality = 0
    for blueprint in blueprints:
        geodes = max_geodes(24, [0, 0, 0, 0], [1, 0, 0, 0], blueprint, 0)
        print(blueprint.num, geodes)
        total_quality += blueprint.num * geodes
    print(total_quality)

    total_quality = 0
    for blueprint in blueprints[0:2]:
        geodes = max_geodes(32, [0, 0, 0, 0], [1, 0, 0, 0], blueprint, 0)
        print(blueprint.num, geodes)
        total_quality += blueprint.num * geodes
    print(total_quality)
