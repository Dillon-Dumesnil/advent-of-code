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
    coordinate = None
    for x in range(grid.shape[0] - 2):
        for y in range(grid.shape[1] - 2):
            nine_cells = []
            for x_offset in range(3):
                for y_offset in range(3):
                    nine_cells.append(grid[(x + x_offset, y + y_offset)])

            temp_power = sum(nine_cells)
            if temp_power > largest_power:
                largest_power = temp_power
                coordinate = (x + 1),(y + 1)

    return coordinate, largest_power


if __name__ == '__main__':
    actual_serial_number = 7803
    grid = create_grid(actual_serial_number)
    coordinate, power_level = largest_total_power(grid)
    print(coordinate)

    # test_serial_number_1 = 57
    # grid = create_grid(test_serial_number_1)
    # print('expected power_level @ 122,79: -5')
    # print('actual: ', grid[(121, 78)])

    # test_serial_number_2 = 39
    # grid = create_grid(test_serial_number_2)
    # print('expected power_level @ 217,196: 0')
    # print('actual: ', grid[(216, 195)])

    # test_serial_number_3 = 71
    # grid = create_grid(test_serial_number_3)
    # print('expected power_level @ 101,153: 4')
    # print('actual: ', grid[(100, 152)])

    # test_serial_number_4 = 18
    # grid = create_grid(test_serial_number_4)
    # coordinate, power_level = largest_total_power(grid)
    # print('expected coordinate: 33,45')
    # print('actual: ', coordinate)
    # print('expected power_level at coordinate: 4')
    # actual_x, actual_y = coordinate
    # actual_x -= 1
    # actual_y -= 1
    # print('actual: ', grid[actual_x, actual_y])
    # print('expected largest_total_power: 29')
    # print('actual: ', power_level)

    # test_serial_number_5 = 42
    # grid = create_grid(test_serial_number_5)
    # coordinate, power_level = largest_total_power(grid)
    # print('expected coordinate: 21,61')
    # print('actual: ', coordinate)
    # print('expected power_level at coordinate: 4')
    # actual_x, actual_y = coordinate
    # actual_x -= 1
    # actual_y -= 1
    # print('actual: ', grid[actual_x, actual_y])
    # print('expected largest_total_power: 30')
    # print('actual: ', power_level)
