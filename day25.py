from itertools import zip_longest

decimal_vals = {"=": -2, "-": -1, "0": 0, "1": 1, "2": 2}
snafu_vals = {-2: "=", -1: "-", 0: "0", 1: "1", 2: "2"}


def add_snafu_nums(a: str, b: str) -> str:
    num_str = ""
    carry = "0"
    for x, y in zip_longest(b[::-1], a[::-1], fillvalue="0"):
        decimal_val = decimal_vals[x] + decimal_vals[y] + decimal_vals[carry]
        if decimal_val in snafu_vals:
            num_str += snafu_vals[decimal_val]
            carry = "0"
        elif decimal_val > 2:
            carry = "1"
            num_str += snafu_vals[decimal_val - 5]
        elif decimal_val < -2:
            carry = "-"
            num_str += snafu_vals[decimal_val + 5]
    if carry != "0":
        num_str += carry
    return num_str[::-1]


with open("day25.txt", "r") as file:
    num = "0"
    for line in file.readlines():
        num = add_snafu_nums(line.strip(), num)
    print(num)
