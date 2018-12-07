import os

import numpy as np

script_dir = os.path.dirname(__file__)


def parse_input(input_file):
    '''
    Creates a list of coordinates and shifts all coordinates such that the
    smallest x is 0 and the smallest y is 0
    '''
    abs_file_path = os.path.join(script_dir, input_file)
    coordinates = []
    with open(abs_file_path) as f:
        for line in f:
            x, y = line.split(', ')
            coordinates.append((int(x), int(y)))

    max_x = sorted(coordinates, key=lambda x: x[0])[-1][0]
    max_y = sorted(coordinates, key=lambda x: x[1])[-1][1]
    return coordinates, max_x, max_y

def calculate_grid(coordinates, max_x, max_y):
    grid = np.empty((max_x, max_y), dtype=object)

    for i in range(max_x):
        for j in range(max_y):
            point = (i, j)
            sum_distance = 0
            for index in range(len(coordinates)):
                coord = coordinates[index]
                sum_distance += manhattan_distance((point[0]+1, point[1]+1), coord)
            grid[point] = sum_distance < 10000

    return grid

def largest_area(grid):
    max_x, max_y = grid.shape
    count = 0
    for i in range(max_x):
        for j in range(max_y):
            point = (i, j)
            if grid[point]:
                count += 1

    return count

def manhattan_distance(point, coord):
    return abs(point[0] - coord[0]) + abs(point[1] - coord[1])


if __name__ == '__main__':
    coordinates, max_x, max_y = parse_input('input.txt')
    grid = calculate_grid(coordinates, max_x, max_y)
    count = largest_area(grid)
    print(count)
