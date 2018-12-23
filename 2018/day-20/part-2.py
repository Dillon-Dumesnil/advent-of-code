import os
import sys

from collections import deque

sys.setrecursionlimit(5000)
script_dir = os.path.dirname(__file__)


def parse_input(input_file):
    abs_file_path = os.path.join(script_dir, input_file)
    with open(abs_file_path) as f:
        path = f.readline().strip()
        path = path[1:len(path) - 1]
    return path

def create_graph(path, start, graph={}, branch_nodes=[]):
    current_node = start
    while path:
        if current_node not in graph:
            graph[current_node] = set()

        if path[0] == '(':
            branch_nodes.append(current_node)
            graph, path = create_graph(path[1:], current_node, graph, branch_nodes)
        elif path[0] == '|':
            branch_node = branch_nodes[-1]
            graph, path = create_graph(path[1:], branch_node, graph, branch_nodes)
        elif path[0] == ')':
            branch_nodes.pop()
        else:
            if path[0] == 'N':
                new_node = (current_node[0], current_node[1] + 1)
                graph[current_node].add(new_node)
                current_node = new_node
            if path[0] == 'E':
                new_node = (current_node[0] + 1, current_node[1])
                graph[current_node].add(new_node)
                current_node = new_node
            if path[0] == 'S':
                new_node = (current_node[0], current_node[1] - 1)
                graph[current_node].add(new_node)
                current_node = new_node
            if path[0] == 'W':
                new_node = (current_node[0] - 1, current_node[1])
                graph[current_node].add(new_node)
                current_node = new_node
            if current_node not in graph:
                graph[current_node] = set()
        path = path[1:]

    return graph, path

def bfs_path(graph, start, goal):
    if start == goal:
        return [start]
    visited = {start}
    queue = deque([(start, [])])

    while queue:
        current, path = queue.popleft()
        visited.add(current)
        for neighbor in graph[current]:
            if neighbor == goal:
                return path + [current, neighbor]
            if neighbor in visited:
                continue
            queue.append((neighbor, path + [current]))
            visited.add(neighbor)

def longest_shortest_path(graph):
    rooms_over_thousand = 0
    for node in graph:
        path = bfs_path(graph, (0, 0), node)
        if (len(path) - 1) >= 1000:
            rooms_over_thousand += 1
    return rooms_over_thousand


if __name__ == '__main__':
    path = parse_input('input.txt')
    graph, _ = create_graph(path, (0, 0), {})
    rooms_over_thousand = longest_shortest_path(graph)
    print(rooms_over_thousand)

    # path = parse_input('test-input-1.txt')
    # graph, _ = create_graph(path, (0, 0), {})
    # actual = longest_shortest_path(graph)
    # # for items in graph.items():
    # #     print(items)
    # expected = 3
    # print('expected:', expected)
    # print('actual:', actual)

    # path = parse_input('test-input-2.txt')
    # graph, _ = create_graph(path, (0, 0), {})
    # actual = longest_shortest_path(graph)
    # # for items in graph.items():
    # #     print(items)
    # expected = 10
    # print('expected:', expected)
    # print('actual:', actual)

    # path = parse_input('test-input-3.txt')
    # graph, _ = create_graph(path, (0, 0), {})
    # actual = longest_shortest_path(graph)
    # # for items in graph.items():
    # #     print(items)
    # expected = 18
    # print('expected:', expected)
    # print('actual:', actual)

    # path = parse_input('test-input-4.txt')
    # graph, _ = create_graph(path, (0, 0), {})
    # actual = longest_shortest_path(graph)
    # # for items in graph.items():
    # #     print(items)
    # expected = 23
    # print('expected:', expected)
    # print('actual:', actual)

    # path = parse_input('test-input-5.txt')
    # graph, _ = create_graph(path, (0, 0), {})
    # actual = longest_shortest_path(graph)
    # # for items in graph.items():
    # #     print(items)
    # expected = 31
    # print('expected:', expected)
    # print('actual:', actual)
