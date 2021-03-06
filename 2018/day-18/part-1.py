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
    for _ in range(10):
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
    print(resource_value)

    # forest = parse_input('test-input.txt')
    # forest = change_landscape(forest)
    # resource_value = count_resource_value(forest)
    # print(resource_value)
