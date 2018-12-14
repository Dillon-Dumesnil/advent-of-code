import os
import time

script_dir = os.path.dirname(__file__)


def parse_input(input_file):
    abs_file_path = os.path.join(script_dir, input_file)

    with open(abs_file_path) as f:
        # has form 'initial state: #..#.#..##......###...###\n'
        initial_state = f.readline().strip().split(': ')[1]
        # pots = [pot for pot in initial_state]
        f.readline()  # Empty line
        rules = {}
        for line in f:
            config, result = line.strip().split(' => ')
            rules[config] = result

    return initial_state, rules

def simulate_generation(pots, rules):
    new_pots = pots
    for i in range(2, len(pots) - 2):
        # We want to look at Left Left Current Right Right
        pot_configuration = pots[(i - 2):(i + 3)]
        if new_pots[i] != rules[pot_configuration]:
            new_pots = new_pots[:i] + rules[pot_configuration] + new_pots[i + 1:]

    return new_pots

def simulate_multiple_generations(pots, rules, num_generations):
    # since pots can go in the negative direction, we are keeping a count of
    # the number of pots that are negative so we can subtract this when finding
    # the sum based on indexes.
    num_negative_pots = 0
    previous_sum = 0
    current_sum = 0
    for i in range(num_generations):
        if '#' in pots[:3]:
            # we add three empty pots because we are always checking two to the
            # left and the newly added pot is now eligible too
            pots = '...' + pots
            num_negative_pots += 3
        if '#' in pots[-3:]:
            # Similar to above, we are always checking two to the right of the
            # current pot so we want to make sure we pad there as well
            pots = pots + '...'

        pots = simulate_generation(pots, rules)

        # find steady state delta increase (91 for my input)
        previous_sum = current_sum
        current_sum = calculate_sum(pots, num_negative_pots)
        print("generation: ", i)
        print(current_sum - previous_sum)

    return current_sum, current_sum - previous_sum

def calculate_sum(pots, num_negative_pots):
    sum_plant_indexes = 0
    for index in range(len(pots)):
        if pots[index] == '#':
            sum_plant_indexes += (index - num_negative_pots)

    return sum_plant_indexes


if __name__ == '__main__':
    pots, rules = parse_input('test-input.txt')
    num_generations = 500
    # start = time.time()
    current_sum, steady_state = simulate_multiple_generations(pots, rules, num_generations)
    # end = time.time()
    # print(num_generations, "took", end - start)
    sum_plant_indexes = current_sum + ((50000000000 - 100) * steady_state)
    print(sum_plant_indexes)
