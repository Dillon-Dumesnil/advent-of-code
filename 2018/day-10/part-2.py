import os

import numpy as np

script_dir = os.path.dirname(__file__)
np.set_printoptions(linewidth=np.nan, threshold=np.nan)


def parse_input(input_file):
    abs_file_path = os.path.join(script_dir, input_file)
    point_tuples = []
    with open(abs_file_path) as f:
        max_x = -1
        max_y = -1
        min_x = 1
        min_y = 1
        for line in f:
            first_less_than = line.find('<')
            first_greater_than = line.find('>')
            position = line[first_less_than + 1:first_greater_than]
            x, y = [int(i) for i in position.split(',')]

            if x > max_x:
                max_x = x
            if y > max_y:
                max_y = y
            if x < min_x:
                min_x = x
            if y < min_y:
                min_y = y

            line = line[first_greater_than + 1:]
            second_less_than = line.find('<')
            second_greater_than = line.find('>')
            velocity = line[second_less_than + 1:second_greater_than]
            v_x, v_y = [int(i) for i in velocity.split(',')]
            point_tuples.append((x, y, v_x, v_y))

    points = []
    for point in point_tuples:
        x, y, v_x, v_y = point
        points.append(Point(x, y, v_x, v_y))
    bounding_box = abs(min_x - max_x) + abs(min_y - max_y)

    return Sky(points, bounding_box)


class Sky(object):
    """docstring for sky"""
    def __init__(self, points, current_bounding_box):
        super(Sky, self).__init__()
        self.points = points
        self.current_bounding_box = current_bounding_box
        self.previous_bounding_box = float("inf")

    def step(self):
        for point in self.points:
            point.step()

    def set_bounding_box(self):
        max_x = float("-inf")
        max_y = float("-inf")
        min_x = float("inf")
        min_y = float("inf")
        for point in self.points:
            if point.x > max_x:
                max_x = point.x
            if point.y > max_y:
                max_y = point.y
            if point.x < min_x:
                min_x = point.x
            if point.y < min_y:
                min_y = point.y
        self.previous_bounding_box = self.current_bounding_box
        self.current_bounding_box = abs(min_x - max_x) + abs(min_y - max_y)

    def show_message(self):
        max_x = float("-inf")
        max_y = float("-inf")
        min_x = float("inf")
        min_y = float("inf")
        for point in self.points:
            point.reverse_step()
            if point.x > max_x:
                max_x = point.x
            if point.y > max_y:
                max_y = point.y
            if point.x < min_x:
                min_x = point.x
            if point.y < min_y:
                min_y = point.y

        message = np.full((max_x + 1, max_y + 1), '.', dtype=object)
        for point in self.points:
            message[(point.x, point.y)] = '#'

        print(message)

class Point(object):
    """docstring for Point"""
    def __init__(self, x, y, v_x, v_y):
        super(Point, self).__init__()
        self.x = x
        self.y = y
        self.v_x = v_x
        self.v_y = v_y

    def step(self):
        self.x += self.v_x
        self.y += self.v_y

    def reverse_step(self):
        self.x -= self.v_x
        self.y -= self.v_y


def step(sky):
    count = 0
    while sky.current_bounding_box < sky.previous_bounding_box:
        count += 1
        sky.step()
        sky.set_bounding_box()
    return count - 1


if __name__ == '__main__':
    sky = parse_input('input.txt')
    count = step(sky)
    print(count)
