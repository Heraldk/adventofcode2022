from typing import List, Dict, Tuple
from dataclasses import dataclass


@dataclass
class File:
    name: str
    size: int


@dataclass
class DirList:
    subdirs: List[str]
    files: List[File]


def parse_input(lines: List[str]):
    path = [""]
    idx = 0
    tree = {}
    while idx < len(lines):
        line = lines[idx].strip()
        assert line[0] == "$"

        if line.startswith("$ cd /"):
            path = [""]
        elif line.startswith("$ cd .."):
            path.pop()
        elif line.startswith("$ cd"):
            vals = line.split(" ")
            path.append(vals[2])
        else:
            assert line.startswith("$ ls")
            # loop through listing

            subdirs = []
            files = []
            while idx + 1 < len(lines) and lines[idx + 1][0] != "$":
                idx += 1
                line_vals = lines[idx].strip().split(" ")
                if line_vals[0] == "dir":
                    subdirs.append(line_vals[1])
                else:
                    files.append(File(line_vals[1], int(line_vals[0])))

            abs_path = "/".join(path) + "/"
            tree[abs_path] = DirList(subdirs=subdirs, files=files)
        idx += 1
    return tree


def calc_sizes(
    path: str, tree: Dict[str, DirList], size_dict: Dict[str, int]
) -> Tuple[int, Dict[str, int]]:
    size = 0
    listing = tree[path]
    for file in listing.files:
        size += file.size
    for subdir in listing.subdirs:
        dir_size, _ = calc_sizes(path + subdir + "/", tree, size_dict)
        size += dir_size

    size_dict[path] = size
    return size, size_dict


with open("day07.txt", "r") as file:
    lines = file.readlines()
    input = parse_input(lines)
    total_size, size_dict = calc_sizes("/", input, {})

    # part 1
    filtered_sizes = [y for y in size_dict.values() if y < 100000]
    print(sum(filtered_sizes))

    # part 2
    space_to_free = 30000000 - (70000000 - total_size)
    assert space_to_free > 0
    filtered_sizes = [y for y in size_dict.values() if y > space_to_free]
    print(min(filtered_sizes))
