import os
import sys

import numpy as np

sys.setrecursionlimit(10000)
script_dir = os.path.dirname(__file__)
np.set_printoptions(linewidth=np.nan, threshold=np.nan)


def parse_input(input_file):
    abs_file_path = os.path.join(script_dir, input_file)
    with open(abs_file_path) as f:
        min_x = np.inf
        max_x = -np.inf
        min_y = np.inf
        max_y = -np.inf
        clay_spots = set([])
        for line in f:
            first, second = line.strip().split(', ')
            coord = first.split('=')
            start, end = [int(i) for i in second.split('=')[1].split('..')]
            if coord[0] == 'x':
                x = int(coord[1])
                if x > max_x:
                    max_x = x
                if x < min_x:
                    min_x = x
                for y in range(start, end + 1):
                    clay_spots.add((y, x))
                    if y > max_y:
                        max_y = y
                    if y < min_y:
                        min_y = y
            else:
                y = int(coord[1])
                if y > max_y:
                    max_y = y
                if y < min_y:
                    min_y = y
                for x in range(start, end + 1):
                    clay_spots.add((y, x))
                    if x > max_x:
                        max_x = x
                    if x < min_x:
                        min_x = x

    grid = np.full((max_y + 1, max_x + 10), '.', dtype=object)
    grid[0, 500] = '+'
    for spot in clay_spots:
        grid[spot] = '#'

    return grid, min_x, max_x, min_y, max_y

def fill_row(grid, start_y, start_x):
    enclosed = True
    left_border = start_x - 1
    right_border = start_x + 1

    while grid[start_y, left_border] != '#' or grid[start_y, right_border] != '#':
        if grid[start_y + 1, left_border] == '.' or \
        grid[start_y + 1, right_border] == '.':
            enclosed = False
            break
        if grid[start_y, left_border] != '#' and grid[start_y + 1, left_border] != '.':
            left_border -= 1
        if grid[start_y, right_border] != '#' and grid[start_y + 1, right_border] != '.':
            right_border += 1

    if enclosed:
        grid[start_y, left_border + 1:right_border] = '~'
    return enclosed

def fill_grid(grid, vertex, path=[]):
    path += [vertex]
    neighbors = []

    if vertex[0] + 1 == grid.shape[0]:
        return path

    if grid[vertex[0] + 1, vertex[1]] == '.':
        neighbors.append((vertex[0] + 1, vertex[1]))
    elif grid[vertex[0] + 1, vertex[1]] == '|':
        pass
    else:
        enclosed = fill_row(grid, vertex[0], vertex[1])
        if enclosed:
            neighbors.append((vertex[0] - 1, vertex[1]))
        else:
            if grid[vertex[0], vertex[1] - 1] == '.' or \
            grid[vertex[0], vertex[1] - 2] == '.':
                neighbors.append((vertex[0], vertex[1] - 1))
            if grid[vertex[0], vertex[1] + 1] == '.' or \
            grid[vertex[0], vertex[1] + 2] == '.':
                neighbors.append((vertex[0], vertex[1] + 1))

    for neighbor in neighbors:
        if grid[neighbor] == '.' or grid[neighbor] == '|':
            grid[neighbor] = '|'
            path = fill_grid(grid, neighbor, path)

    return path

def count_water(grid, min_y):
    count = 0
    for y in range(min_y, grid.shape[0]):
        for x in range(grid.shape[1]):
            if grid[y, x] == '~':
                count += 1
    return count


if __name__ == '__main__':
    well = (0, 500)

    grid, min_x, max_x, min_y, max_y = parse_input('input.txt')
    fill_grid(grid, well)
    # for i in range(200):
    #     print(''.join(grid[i, 500:600]))
    count = count_water(grid, min_y)
    print(count)

    # grid, min_x, max_x, min_y, max_y = parse_input('test-input.txt')
    # fill_grid(grid, well)
    # count = count_water(grid, min_y)
    # print(grid[:, 494:])
    # print(count)
