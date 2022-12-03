player_score = {"X": 1, "Y": 2, "Z": 3}
table_lookup = {
    "A": {"X": 3, "Y": 6, "Z": 0},
    "B": {"X": 0, "Y": 3, "Z": 6},
    "C": {"X": 6, "Y": 0, "Z": 3},
}

result_lookup = {
    "A": {"X": "Z", "Y": "X", "Z": "Y"},
    "B": {"X": "X", "Y": "Y", "Z": "Z"},
    "C": {"X": "Y", "Y": "Z", "Z": "X"},
}


def score_round(opponent: str, me: str) -> int:
    assert me in player_score.keys()
    assert opponent in table_lookup.keys()
    score = player_score[me] + table_lookup[opponent][me]
    return score


with open("day02.txt", "r") as file:
    total_score = 0
    score_part2 = 0
    for x in file.readlines():
        if len(x) > 0:
            round = x.split(" ")
            total_score += score_round(round[0].strip(), round[1].strip())

            # for part two, lookup what we should play to get the result we want
            our_play = result_lookup[round[0].strip()][round[1].strip()]
            score_part2 += score_round(round[0].strip(), our_play)

    print(total_score)
    print(score_part2)
