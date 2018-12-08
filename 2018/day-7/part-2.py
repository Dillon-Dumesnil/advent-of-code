import os
import string

script_dir = os.path.dirname(__file__)

time_map = {}
for i in range(1, 27):
    time_map[string.ascii_uppercase[i - 1]] = (60 + i)

def parse_input(input_file):
    abs_file_path = os.path.join(script_dir, input_file)
    steps = {}
    with open(abs_file_path) as f:
        for line in f:
            words = line.split()
            parent = words[1]
            child = words[7]
            # print("child: " + child)
            # print("parent: " + parent)

            if parent in steps:
                steps[parent].add_child(child)
            else:
                steps[parent] = Step(parent, [child], [])
            if child in steps:
                steps[child].add_parent(parent)
            else:
                steps[child] = Step(child, [], [parent])

    no_parents = []
    for letter in steps:
        steps[letter].sort()
        if not steps[letter].parents:
            no_parents.append(letter)

    return steps, no_parents

class Step():
    def __init__(self, letter, children, parents):
        self.letter = letter
        self.children = children
        self.parents = parents
        self.time_to_finish = time_map[self.letter]
        self.start_time = None

    def add_child(self, letter):
        self.children.append(letter)

    def add_parent(self, letter):
        self.parents.append(letter)

    def remove_child(self, letter):
        self.children.remove(letter)

    def remove_parent(self, letter):
        self.parents.remove(letter)

    def sort(self):
        self.children = sorted(set(self.children))
        self.parents = sorted(set(self.parents))

def traverse_graph(steps, eligible_nodes, num_workers):
    num_idle_workers = num_workers
    time = 0
    steps_being_worked_on = []
    order = ''
    while eligible_nodes or steps_being_worked_on:
        # See if any steps are done
        for letter in steps_being_worked_on:
            if time == (steps[letter].start_time + steps[letter].time_to_finish):
                steps_being_worked_on.remove(letter)
                num_idle_workers += 1
                order += letter

                for child in steps[letter].children:
                    steps[child].remove_parent(letter)
                    if not steps[child].parents:
                        eligible_nodes.append(child)
                steps[letter].children = []

        eligible_nodes = sorted(eligible_nodes)
        while eligible_nodes and num_idle_workers > 0:
            num_idle_workers -= 1
            letter = eligible_nodes.pop(0)
            steps_being_worked_on.append(letter)
            steps[letter].start_time = time

        time += 1

    return time - 1, order


if __name__ == '__main__':
    steps, no_parents = parse_input('input.txt')
    time, order = traverse_graph(steps, no_parents, 5)
    print(time)
