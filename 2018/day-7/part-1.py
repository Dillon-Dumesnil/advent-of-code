import os

script_dir = os.path.dirname(__file__)


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

def traverse_graph(steps, eligible_nodes):
    order = ''
    while eligible_nodes:
        eligible_nodes = sorted(eligible_nodes)
        letter = eligible_nodes.pop(0)
        order += letter
        for child in steps[letter].children:
            steps[child].remove_parent(letter)
            if not steps[child].parents:
                eligible_nodes.append(child)
        steps[letter].children = []

    return order


if __name__ == '__main__':
    steps, no_parents = parse_input('input.txt')
    order = traverse_graph(steps, no_parents)
    print(order)
