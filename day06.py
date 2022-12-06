def find_start_marker(string: str, num_distinct: int) -> int:
    for x in range(num_distinct - 1, len(string)):
        if len(set(string[x - num_distinct + 1 : x + 1])) == num_distinct:
            return x + 1
    return -1


with open("day06.txt", "r") as file:
    line = file.readline()
    print(find_start_marker(line, 4))
    print(find_start_marker(line, 14))
