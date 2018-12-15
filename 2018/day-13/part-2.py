import os

import numpy as np

script_dir = os.path.dirname(__file__)


def parse_input(input_file):
    abs_file_path = os.path.join(script_dir, input_file)
    with open(abs_file_path) as f:
        temp_tracks = []
        max_x = 0
        for line in f:
            temp_line = []
            line = line.strip('\n')
            if len(line) > max_x:
                max_x = len(line)
            for piece in line:
                temp_line.append(piece)
            temp_tracks.append(temp_line)
    max_y = len(temp_tracks)

    tracks = np.full((max_y, max_x), ' ', dtype=object)
    carts = []
    cart_to_track = {'>': '-', '<': '-', '^': '|', 'v': '|'}
    for y in range(len(temp_tracks)):
        for x in range(len(temp_tracks[y])):
            if temp_tracks[y][x] in ['>', '<', '^', 'v']:
                cart_direction = temp_tracks[y][x]
                carts.append(Cart(cart_direction, y, x))
                temp_tracks[y][x] = cart_to_track[cart_direction]
            tracks[(y, x)] = temp_tracks[y][x]

    return tracks, carts

class Cart(object):
    def __init__(self, direction, x, y):
        super(Cart, self).__init__()
        self.direction = direction
        self.y = y
        self.x = x
        self.turn_direction = 'l'
        self.direction_update = {
            ('<', '\\'): '^',
            ('>', '\\'): 'v',
            ('^', '\\'): '<',
            ('v', '\\'): '>',

            ('<', '/'): 'v',
            ('>', '/'): '^',
            ('^', '/'): '>',
            ('v', '/'): '<',

            ('<', 'l'): ('v', 's'),
            ('>', 'l'): ('^', 's'),
            ('^', 'l'): ('<', 's'),
            ('v', 'l'): ('>', 's'),

            ('<', 's'): ('<', 'r'),
            ('>', 's'): ('>', 'r'),
            ('^', 's'): ('^', 'r'),
            ('v', 's'): ('v', 'r'),

            ('<', 'r'): ('^', 'l'),
            ('>', 'r'): ('v', 'l'),
            ('^', 'r'): ('>', 'l'),
            ('v', 'r'): ('<', 'l'),
        }

    def tick(self, tracks):
        if self.direction == '>':
            self.y += 1
        elif self.direction == '<':
            self.y -= 1
        elif self.direction == '^':
            self.x -= 1
        elif self.direction == 'v':
            self.x += 1

        # Special cases. Direction changes here!
        current_track_piece = tracks[(self.x, self.y)]
        if current_track_piece in ['+', '\\', '/']:
            if current_track_piece == '+':
                self.direction, self.turn_direction = self.direction_update[(self.direction, self.turn_direction)]
            else:
                self.direction = self.direction_update[(self.direction, current_track_piece)]


    def __str__(self):
        return self.direction + ' @ ' + str(self.y) + ', ' + str(self.x)


def detect_collision(tracks, carts):
    while len(carts) > 1:
        # Need to sort because carts are supposed to move from top to bottom,
        # left to right in each tick.
        for cart in sorted(carts, key=lambda cart: (cart.y, cart.x)):
            cart.tick(tracks)
            for cart_2 in carts:
                if cart != cart_2 and (cart.x, cart.y) == (cart_2.x, cart_2.y):
                    carts.remove(cart)
                    carts.remove(cart_2)
                    break

    last_cart = carts[0]
    return last_cart.y, last_cart.x


if __name__ == '__main__':
    tracks, carts = parse_input('input.txt')
    remaining_cart_coordinate = detect_collision(tracks, carts)
    print(remaining_cart_coordinate)
