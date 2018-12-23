import os

from copy import deepcopy

script_dir = os.path.dirname(__file__)


def parse_input(input_file):
    abs_file_path = os.path.join(script_dir, input_file)
    with open(abs_file_path) as f:
        forest = []
        for line in f:
            row = []
            for acre in line.strip():
                row.append(acre)
            forest.append(row)
    return forest

def change_landscape(forest):
    old_count = None
    resource_value = None
    for _ in range(500):
        new_forest = deepcopy(forest)
        for x in range(len(forest)):
            for y in range(len(forest[0])):
                tree_count = 0
                lumberyard_count = 0
                for i in [-1, 0, 1]:
                    for j in [-1, 0, 1]:
                        if (i == 0 and j == 0) or \
                        (x + i) < 0 or \
                        (x + i) >= len(forest) or \
                        (y + j) < 0 or \
                        (y + j) >= len(forest[0]):
                            continue
                        if forest[x + i][y + j] == '|':
                            tree_count += 1
                        elif forest[x + i][y + j] == '#':
                            lumberyard_count += 1

                open_ground = forest[x][y] == '.'
                trees = forest[x][y] == '|'
                lumberyard = forest[x][y] == '#'
                if open_ground:
                    if tree_count >= 3:
                        new_forest[x][y] = '|'
                elif trees:
                    if lumberyard_count >= 3:
                        new_forest[x][y] = '#'
                elif lumberyard:
                    if lumberyard_count < 1 or tree_count < 1:
                        new_forest[x][y] = '.'

        forest = new_forest
        if _ > 400:
            print(count_resource_value(forest), _)

    return forest

def count_resource_value(forest):
    tree_count = 0
    lumberyard_count = 0
    for x in range(len(forest)):
        for y in range(len(forest[0])):
            if forest[x][y] == '|':
                tree_count += 1
            elif forest[x][y] == '#':
                lumberyard_count += 1
    return tree_count * lumberyard_count

if __name__ == '__main__':
    forest = parse_input('input.txt')
    forest = change_landscape(forest)
    resource_value = count_resource_value(forest)

    # forest = parse_input('test-input.txt')
    # forest = change_landscape(forest)
    # resource_value = count_resource_value(forest)
    # print(resource_value)

# Pattern:
# resource_value, iteration value, value in pattern
# 197556, 430, 1
# 204350, 431, 2
# 210184, 432, 3
# 211560, 433, 4
# 213408, 434, 5
# 215460, 435, 6
# 221328, 436, 7
# 223416, 437, 8
# 227409, 438, 9
# 224005, 439, 10
# 227907, 440, 11
# 222768, 441, 12
# 215400, 442, 13
# 208260, 443, 14
# 199850, 444, 15
# 191178, 445, 16
# 182381, 446, 17
# 175168, 447, 18
# 165680, 448, 19
# 164892, 449, 20
# 163602, 450, 21
# 163430, 451, 22
# 167739, 452, 23
# 172104, 453, 24
# 176900, 454, 25
# 184004, 455, 26
# 189440, 456, 27
# 192279, 457, 28

# Solution was found by finding the pattern and then taking 1000000000 % 28
# to find what the resource_value should be.
