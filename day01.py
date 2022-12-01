with open("day01.txt", "r") as file:
    current_sum = 0
    current_list = []
    for x in file.readlines():
        try:
            num = int(x)
            current_sum += num
        except ValueError:
            current_list.append(current_sum)
            current_sum = 0
    current_list.sort(reverse=True)
    print(current_list[0])
    print(sum(current_list[0:3]))
