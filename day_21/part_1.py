from dataclasses import dataclass
from dataclasses import field
from itertools import chain
from itertools import product


@dataclass
class Node:
    symbol: str
    coords: tuple
    matrix: list=field(repr=False)
    visited: bool=False
    distance: int=float('inf')

    directions = {
        'north': (-1, 0),
        'south': (1, 0),
        'west': (0, -1),
        'east': (0, 1)
    }

    # Gets neighbor in `self.matrix` given a `direction`.
    def _neighbor(self, direction):
        neighbor_coords = (
            self.coords[0] + self.directions[direction][0],
            self.coords[1] + self.directions[direction][1]
        )

        if neighbor_coords[0] not in range(len(self.matrix)):
            return None

        if neighbor_coords[1] not in range(len(self.matrix[0])):
            return None

        return self.matrix[neighbor_coords[0]][neighbor_coords[1]]

    # All neighbors in `self.directions`.
    def neighbors(self):
        return [self._neighbor(direction) for direction in self.directions if self._neighbor(direction) is not None]

    def manhattan_distance(self, other):
        return abs(self.coords[0] - other.coords[0]) + abs(self.coords[1] - other.coords[1])

    def a_star_score(self, target_node):
        return self.distance + self.manhattan_distance(target_node)

    # Makes nodes equal if they have the same `coords`.
    def __eq__(self, other):
        return self.coords == other.coords

    def __lt__(self, other):
        return self.distance < other.distance

    def reset(self):
        self.visited = False
        self.distance = float('inf')

    def unvisit(self):
        self.visited = False

    def __repr__(self):
        return f'{self.symbol}'


def reset(matrix):
    for _, node in enumerate_n(matrix, n=2):
        node.reset()


def unvisit(matrix):
    for _, node in enumerate_n(matrix, n=2):
        node.unvisit()

def enumerate_n(iterable, start=0, n=1):
    from collections.abc import Iterable

    count = start

    for item in iterable:
        if isinstance(item, Iterable) and n > 1:
            for index, value in enumerate_n(iter(item), start=start, n=n - 1):
                if not isinstance(index, Iterable):
                    index = [index]

                yield tuple([count, *index]), value
        else:
            yield count, item

        count += 1


def sliding_window(iterable, n=2):
    from itertools import islice

    args = [islice(iter(iterable), i, None) for i in range(n)]
    return zip(*args)


# Finds distance from given `node` to every other node in the graph.optionally
# stopping at `target_node`.
def dijkstra(node, target_node=None):
    import heapq

    node.distance = 0

    nodes = [node]
    heapq.heapify(nodes)

    while nodes:
        # Get node with smallest distance
        node = heapq.heappop(nodes)

        if node.visited:
            continue

        # Mark current node as visited in current direction
        node.visited = True

        # Optionally stop search when we reach the given `target_node`
        if target_node and node == target_node:
            break

        for neighbor in node.neighbors():
            if neighbor.symbol == '#':
                continue

            neighbor.distance = min(neighbor.distance, node.distance + 1)

            if not neighbor.visited:
                heapq.heappush(nodes, neighbor)


class Robot:
    def to_instruction(self, node_a, node_b):
        distance_x = node_a.coords[0] - node_b.coords[0]
        distance_y = node_a.coords[1] - node_b.coords[1]

        if distance_x == -1:
            return 'v'

        if distance_x == 1:
            return '^'

        if distance_y == -1:
            return '>'

        if distance_y == 1:
            return '<'



class DoorRobot(Robot):
    def __init__(self):
        self.matrix = [
            ['7', '8', '9'],
            ['4', '5', '6'],
            ['1', '2', '3'],
            ['#', '0', 'A']
        ]

        for coords, symbol in enumerate_n(self.matrix, n=2):
            node = Node(
                symbol=symbol,
                coords=coords,
                matrix=self.matrix
            )

            self.matrix[coords[0]][coords[1]] = node

            if node.symbol == 'A':
                self.node_a = node

    def generate(self, targets):
        last_node = self.node_a

        instructions = []

        for target in targets:
            target_node = next(node for _, node in enumerate_n(self.matrix, n=2) if node.symbol == target)
            dijkstra(last_node)
            unvisit(self.matrix)

            paths = generate_paths(target_node, last_node, ())

            local_instructions = []

            for path in paths:
                instruction_set = tuple(self.to_instruction(a, b) for a, b in sliding_window(path[::-1])) + ('A',)
                local_instructions.append(instruction_set)

            if not instructions:
                instructions = local_instructions
            else:
                instructions = [a + b for a, b in product(instructions, local_instructions)]

            reset(self.matrix)
            last_node = target_node

        # instructions.sort(key=lambda i: (len(i), instruction_sequence_score(i)))
        instructions.sort(key=lambda i: len(i))

        min_length = len(instructions[0])
        # min_score = instruction_sequence_score(instructions[0])

        result = []

        for i in instructions:
            if len(i) == min_length:
                result.append(i)
            else:
                break

        return result


def generate_paths(current_node, target_node, current_path):
    current_node.visited = True
    current_path = current_path + (current_node,)

    if current_node == target_node:
        current_node.visited = False
        return [current_path]

    min_neighbor_distance = min((n.distance for n in current_node.neighbors() if not n.visited), default=-1)
    nodes = [n for n in current_node.neighbors() if not n.visited and n.distance == min_neighbor_distance]

    paths = []
    for node in nodes:
        paths.append(generate_paths(node, target_node, current_path))

    current_node.visited = False

    if type(paths[0]) != tuple:
        return list(chain.from_iterable(paths))

    return paths


def instruction_sequence_score(instruction_sequence):
    score = 0
    directional_robot = DirectionalRobot()

    for a, b in sliding_window(instruction_sequence):
        node_a_coords = directional_robot.coords[a]
        node_a = directional_robot.matrix[node_a_coords[0]][node_a_coords[1]]

        node_b_coords = directional_robot.coords[b]
        node_b = directional_robot.matrix[node_b_coords[0]][node_b_coords[1]]

        score += node_a.manhattan_distance(node_b)

    return score


class DirectionalRobot(Robot):
    def __init__(self):
        self.matrix = [
            ['#', '^', 'A'],
            ['<', 'v', '>']
        ]

        self.coords = {}

        for coords, symbol in enumerate_n(self.matrix, n=2):
            node = Node(
                symbol=symbol,
                coords=coords,
                matrix=self.matrix
            )

            self.matrix[coords[0]][coords[1]] = node
            self.coords[symbol] = coords

            if node.symbol == 'A':
                self.node_a = node

    def generate(self, received_paths):
        last_node = self.node_a

        final_instructions = []

        for received_path in received_paths:
            instructions = []

            for target in received_path:
                target_node = next(node for _, node in enumerate_n(self.matrix, n=2) if node.symbol == target)
                dijkstra(last_node)
                unvisit(self.matrix)

                paths = generate_paths(target_node, last_node, ())

                local_instructions = []

                for path in paths:
                    instruction_set = tuple(self.to_instruction(a, b) for a, b in sliding_window(path[::-1])) + ('A',)
                    local_instructions.append(instruction_set)

                if not instructions:
                    instructions = local_instructions
                else:
                    instructions = [a + b for a, b in product(instructions, local_instructions)]

                reset(self.matrix)
                last_node = target_node

            final_instructions.extend(instructions)

        # final_instructions.sort(key=lambda i: (len(i), instruction_sequence_score(i)))
        final_instructions.sort(key=lambda i: len(i))

        min_length = len(final_instructions[0])
        # min_score = instruction_sequence_score(final_instructions[0])

        result = []

        for i in final_instructions:
            if len(i) == min_length:
                result.append(i)
            else:
                break

        return result

with open('input.txt') as f:
    data = f.readlines()

total = 0

for code in data:
    code = code.strip()
    numeric_code = int(''.join(c for c in code if c.isdigit()))

    paths = DoorRobot().generate(code)
    paths = DirectionalRobot().generate(paths)
    min_size = len(DirectionalRobot().generate(paths)[0])

    total += numeric_code * min_size

print(total)
