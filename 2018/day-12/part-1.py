import os
import time
import random

script_dir = os.path.dirname(__file__)


def parse_input(input_file):
    abs_file_path = os.path.join(script_dir, input_file)

    with open(abs_file_path) as f:
        # has form 'initial state: #..#.#..##......###...###\n'
        initial_state = f.readline().strip().split(': ')[1]
        # f.readline()
        # initial_state = ['.' if random.random() > .7 else '#' for i in range(40)]
        pots = [pot for pot in initial_state]
        f.readline()  # Empty line
        rules = {}
        for line in f:
            config, result = line.strip().split(' => ')
            rules[config] = result
            # rules[config] = '.' if random.random() > .6 else '#'

    return pots, rules

def simulate_generation(pots, rules):
    new_pots = pots
    pots = ''.join(pots)
    for i in range(2, len(pots) - 2):
        # We want to look at Left Left Current Right Right
        pot_configuration = pots[(i - 2):(i + 3)]
        new_pots[i] = rules[pot_configuration]

    return new_pots

def simulate_multiple_generations(pots, rules, num_generations):
    # since pots can go in the negative direction, we are keeping a count of
    # the number of pots that are negative so we can subtract this when finding
    # the sum based on indexes.
    num_negative_pots = 0
    previous_sum = 0
    current_sum = 0
    steady_state = 0
    count = 0
    for i in range(num_generations):
        if '#' in pots[:3]:
            # we add three empty pots because we are always checking two to the
            # left and the newly added pot is now eligible too
            pots = ['.', '.', '.'] + pots
            num_negative_pots += 3
        if '#' in pots[-3:]:
            # Similar to above, we are always checking two to the right of the
            # current pot so we want to make sure we pad there as well
            pots.append('.')
            pots.append('.')
            pots.append('.')

        pots = simulate_generation(pots, rules)

        # previous_sum = current_sum
        # current_sum = calculate_sum(pots, num_negative_pots)
        # if current_sum - previous_sum == steady_state:
        #     count += 1
        # else:
        #     count = 0

        # if count == 15:
        #     print("steady state of:", current_sum - previous_sum, '@ generation:', i - 15)
        #     break

        # steady_state = current_sum - previous_sum
        # print("generation: ", i)
        # print(current_sum - previous_sum)

    return pots, num_negative_pots

def calculate_sum(pots, num_negative_pots):
    sum_plant_indexes = 0
    for index in range(len(pots)):
        if pots[index] == '#':
            sum_plant_indexes += (index - num_negative_pots)

    return sum_plant_indexes


if __name__ == '__main__':
    pots, rules = parse_input('input.txt')
    num_generations = 20
    # start = time.time()
    pots, num_negative_pots = simulate_multiple_generations(pots, rules, num_generations)
    # end = time.time()
    # print(num_generations, "took", end - start)
    sum_plant_indexes = calculate_sum(pots, num_negative_pots)
    print(sum_plant_indexes)
