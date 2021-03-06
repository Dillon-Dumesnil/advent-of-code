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
            grid[point] = [None, np.inf]
            for index in range(len(coordinates)):
                coord = coordinates[index]
                distance = manhattan_distance((point[0]+1, point[1]+1), coord)
                if distance < grid[point][1]:
                    grid[point] = [index, distance]
                elif distance == grid[point][1]:
                    grid[point][0] = None

    return grid

def largest_area(grid, num_coordinates):
    dont_count = set([])
    max_x, max_y = grid.shape
    coord_counts = {i: 0 for i in range(num_coordinates)}
    for i in range(max_x):
        for j in range(max_y):
            point = (i, j)
            index = grid[point][0]
            if i == 0 or j == 0 or i == (max_x - 1) or j == (max_y - 1):
                dont_count.add(index)
            if grid[point][0] != None:
                coord_counts[index] += 1

    best_count = -1
    best_index = -1
    for key in coord_counts:
        if key in dont_count:
            continue
        elif coord_counts[key] > best_count:
            best_count = coord_counts[key]
            best_index = key

    return best_index, best_count


def manhattan_distance(point, coord):
    return abs(point[0] - coord[0]) + abs(point[1] - coord[1])


if __name__ == '__main__':
    coordinates, max_x, max_y = parse_input('input.txt')
    grid = calculate_grid(coordinates, max_x, max_y)
    best_index, best_count = largest_area(grid, len(coordinates))
    print(best_index, best_count)
