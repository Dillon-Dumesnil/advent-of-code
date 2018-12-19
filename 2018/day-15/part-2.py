import os
import time

from collections import deque
import numpy as np

np.set_printoptions(linewidth=np.nan, threshold=np.nan)
script_dir = os.path.dirname(__file__)


def parse_input(input_file):
    abs_file_path = os.path.join(script_dir, input_file)
    with open(abs_file_path) as f:
        cavern = []
        units = {'E': [], 'G': []}
        x = 0
        for line in f:
            y = 0
            point_types = []
            for point_type in line.strip():
                if point_type == 'E' or point_type == 'G':
                    unit = Unit(point_type, x, y)
                    units[point_type].append(unit)
                    point_type = unit
                point_types.append(point_type)
                y += 1
            x += 1
            cavern.append(point_types)
        cavern = np.array(cavern)
    return cavern, units

class Unit(object):
    """docstring for Unit"""
    def __init__(self, unit_type, x, y):
        super(Unit, self).__init__()
        self.type = unit_type
        self.x = x
        self.y = y
        self.health = 200
        self.attack = 3

    def bfs(self, graph, start, goal):
        if start == goal:
            return [start]
        visited = {start}
        queue = deque([(start, [])])

        while queue:
            current, path = queue.popleft()
            visited.add(current)
            possible_nodes = [
                (current[0] - 1, current[1]),
                (current[0], current[1] - 1),
                (current[0], current[1] + 1),
                (current[0] + 1, current[1]),
            ]
            for neighbor in possible_nodes:
                if neighbor == goal:
                    return path + [current, neighbor]
                if neighbor in visited or graph[neighbor] != '.':
                    continue
                queue.append((neighbor, path + [current]))
                visited.add(neighbor)
        return None

    def choose_unit_and_movement(self, cavern, units):
        enemy_units = self.get_enemy_units(units)

        all_possible_paths_to_enemies = []
        overall_shortest_path_length = np.inf
        for enemy_unit in enemy_units:
            path = self.bfs(cavern, (self.x, self.y), (enemy_unit.x, enemy_unit.y))
            if path:
                if len(path) < overall_shortest_path_length:
                    overall_shortest_path_length = len(path)
                all_possible_paths_to_enemies.append(path)

        possible_enemy_paths = [
            enemy_path for enemy_path in all_possible_paths_to_enemies
            if len(enemy_path) == overall_shortest_path_length
        ]

        if possible_enemy_paths:
            chosen_enemy_path = possible_enemy_paths[0]
            # This means we are already standing next to enemy
            if len(chosen_enemy_path) == 2:
                return self.x, self.y
            move = chosen_enemy_path[1]  # Current location is index 0
            return move
        else:
            return self.x, self.y

    def move(self, cavern, units):
        cavern[self.x, self.y] = '.'
        self.x, self.y = self.choose_unit_and_movement(cavern, units)
        cavern[self.x, self.y] = self

    def attack_enemy(self, cavern, units, enemy_unit):
        enemy_unit.health -= self.attack
        if enemy_unit.health <= 0:
            cavern[enemy_unit.x, enemy_unit.y] = '.'
            units[enemy_unit.type].remove(enemy_unit)

    def get_enemy_units(self, units):
        if self.type == 'E':
            return sorted(units['G'], key=lambda unit: (unit.x, unit.y))
        else:
            return sorted(units['E'], key=lambda unit: (unit.x, unit.y))

    def distance(self, enemy_unit):
        return abs(self.x - enemy_unit.x) + abs(self.y - enemy_unit.y)

    def get_weakest_adjacent_enemy_unit(self, units):
        if self.type == 'E':
            adjacent_units = sorted([unit
                for unit in units['G']
                if self.distance(unit) == 1
            ], key=lambda unit: (unit.health, unit.x, unit.y))
        else:
            adjacent_units = sorted([unit
                for unit in units['E']
                if self.distance(unit) == 1
            ], key=lambda unit: (unit.health, unit.x, unit.y))

        if adjacent_units:
            return adjacent_units[0]
        else:
            return None

    def __repr__(self):
        # return "'" + self.type + "'"
        return self.type + ' (' + str(self.health) + ') @ (' +\
                str(self.x) + ', ' + str(self.y) + ')'

def battle(cavern, units):
    number_of_rounds_completed = 0
    end = False
    while len(units['E']) > 0 and len(units['G']) > 0:
        start = time.time()
        all_units = sorted(units['E'] + units['G'], key=lambda unit: (unit.x, unit.y))
        for unit in all_units:
            # Check if the unit has already died
            if unit.health > 0:
                unit.move(cavern, units)
                enemy_unit = unit.get_weakest_adjacent_enemy_unit(units)
                if enemy_unit:
                    unit.attack_enemy(cavern, units, enemy_unit)
                elif len(units['E']) == 0 or len(units['G']) == 0:
                    end = True
                    break

        if not end:
            number_of_rounds_completed += 1

    return number_of_rounds_completed, units

def outcome_of_battle(units, number_of_rounds_completed):
    if len(units['E']) > 0:
        return number_of_rounds_completed * sum([elf.health for elf in units['E']])
    else:
        print(sum([goblin.health for goblin in units['G']]))
        return number_of_rounds_completed * sum([goblin.health for goblin in units['G']])


if __name__ == '__main__':
    cavern, units = parse_input('input.txt')
    num_elves = len(units['E'])
    elf_attack = 32
    # print(units)
    number_of_rounds_completed, units = battle(cavern, units)
    while num_elves != len(units['E']):
        elf_attack += 1
        print("elf attack", elf_attack)
        cavern, units = parse_input('input.txt')
        for elf in units['E']:
            elf.attack = elf_attack

        number_of_rounds_completed, units = battle(cavern, units)
        # print(units)
    print(number_of_rounds_completed)
    outcome = outcome_of_battle(units, number_of_rounds_completed)
    print(outcome)

    # cavern, units = parse_input('test-input-8.txt')
    # # print(units)
    # num_elves = len(units['E'])
    # elf_attack = 4
    # number_of_rounds_completed, units = battle(cavern, units)
    # while num_elves != len(units['E']):
    #     print("elf attack", elf_attack)
    #     cavern, units = parse_input('test-input-8.txt')
    #     for elf in units['E']:
    #         elf.attack = elf_attack

    #     number_of_rounds_completed, units = battle(cavern, units)
    #     elf_attack += 1
    # print(number_of_rounds_completed)
    # outcome = outcome_of_battle(units, number_of_rounds_completed)
    # print(outcome)

    # cavern, units = parse_input('test-input-2.txt')
    # # print(units)
    # num_elves = len(units['E'])
    # elf_attack = 3
    # number_of_rounds_completed, units = battle(cavern, units)
    # while num_elves != len(units['E']):
    #     elf_attack += 1
    #     cavern, units = parse_input('test-input-2.txt')
    #     for elf in units['E']:
    #         elf.attack = elf_attack

    #     number_of_rounds_completed, units = battle(cavern, units)
    # print(elf_attack)
    # print(number_of_rounds_completed)
    # outcome = outcome_of_battle(units, number_of_rounds_completed)
    # print(outcome)
    # print()

    # cavern, units = parse_input('test-input-3.txt')
    # # print(units)
    # num_elves = len(units['E'])
    # elf_attack = 3
    # number_of_rounds_completed, units = battle(cavern, units)
    # while num_elves != len(units['E']):
    #     elf_attack += 1
    #     cavern, units = parse_input('test-input-3.txt')
    #     for elf in units['E']:
    #         elf.attack = elf_attack

    #     number_of_rounds_completed, units = battle(cavern, units)
    # print(elf_attack)
    # print(number_of_rounds_completed)
    # outcome = outcome_of_battle(units, number_of_rounds_completed)
    # print(outcome)
    # print()

    # cavern, units = parse_input('test-input-4.txt')
    # # print(units)
    # num_elves = len(units['E'])
    # elf_attack = 3
    # number_of_rounds_completed, units = battle(cavern, units)
    # while num_elves != len(units['E']):
    #     elf_attack += 1
    #     cavern, units = parse_input('test-input-4.txt')
    #     for elf in units['E']:
    #         elf.attack = elf_attack

    #     number_of_rounds_completed, units = battle(cavern, units)
    # print(elf_attack)
    # print(number_of_rounds_completed)
    # outcome = outcome_of_battle(units, number_of_rounds_completed)
    # print(outcome)
    # print()

    # cavern, units = parse_input('test-input-5.txt')
    # # print(units)
    # num_elves = len(units['E'])
    # elf_attack = 3
    # number_of_rounds_completed, units = battle(cavern, units)
    # while num_elves != len(units['E']):
    #     elf_attack += 1
    #     cavern, units = parse_input('test-input-5.txt')
    #     for elf in units['E']:
    #         elf.attack = elf_attack

    #     number_of_rounds_completed, units = battle(cavern, units)
    # print(elf_attack)
    # print(number_of_rounds_completed)
    # outcome = outcome_of_battle(units, number_of_rounds_completed)
    # print(outcome)
