import numpy as np


def create_grid(serial_number):
    grid = np.zeros((300, 300))
    for x in range(grid.shape[0]):
        for y in range(grid.shape[1]):
            grid[(x, y)] = calculate_power_level(x, y, serial_number)

    return grid

def calculate_power_level(x, y, serial_number):
    # x's and y's will all be + 1 because of 0 indexing messing up math
    rack_id = (x + 1) + 10
    power_level = rack_id * (y + 1)
    power_level += serial_number
    power_level *= rack_id
    power_level = (power_level // 100) % 10
    power_level -= 5
    return power_level

def largest_total_power(grid):
    largest_power = float("-inf")
    coordinate_and_square_size = None
    for square_size in range(301):
        for x in range(grid.shape[0] - square_size):
            for y in range(grid.shape[1] - square_size):
                cells = grid[x:(x + square_size), y:(y + square_size)]

                temp_power = cells.sum()
                if temp_power > largest_power:
                    largest_power = temp_power
                    coordinate_and_square_size = (x + 1),(y + 1),square_size

    return coordinate_and_square_size, largest_power


if __name__ == '__main__':
    actual_serial_number = 7803
    grid = create_grid(actual_serial_number)
    coordinate_and_square_size, power_level = largest_total_power(grid)
    print(coordinate_and_square_size)

    # test_serial_number_4 = 18
    # grid = create_grid(test_serial_number_4)
    # coordinate_and_square_size, power_level = largest_total_power(grid)
    # print('expected coordinate_and_square_size: 90,269,16')
    # print('actual: ', coordinate_and_square_size)
    # print('expected largest_total_power: 113')
    # print('actual: ', power_level)

    # test_serial_number_5 = 42
    # grid = create_grid(test_serial_number_5)
    # coordinate_and_square_size, power_level = largest_total_power(grid)
    # print('expected coordinate_and_square_size: 232,251,12')
    # print('actual: ', coordinate_and_square_size)
    # print('expected largest_total_power: 119')
    # print('actual: ', power_level)
