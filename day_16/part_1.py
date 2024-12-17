from dataclasses import dataclass
from dataclasses import field
from functools import cache


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


ABSOLUTE_MIN=float('inf')


@dataclass 
class Node:
    symbol: str
    coords: tuple
    matrix: list=field(repr=False)
    visited: dict=field(
        default_factory=lambda: {
            'north': False,
            'south': False,
            'east': False,
            'west': False
        }
    )

    directions = {
        'north': (-1, 0),
        'south': (1, 0),
        'west': (0, -1),
        'east': (0, 1)
    }

    turns = {
        'north': ['east', 'west'],
        'south': ['east', 'west'],
        'east': ['north', 'south'],
        'west': ['north', 'south']
    }

    def __hash__(self):
        return id(self)

    def __repr__(self):
        if self.visited['north']:
            return '^'

        if self.visited['south']:
            return 'v'

        if self.visited['east']:
            return '>'

        if self.visited['west']:
            return '<'

        return self.symbol

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

    def neighbors(self, current_direction):
        neighbors_with_cost = []

        neighbor = self._neighbor(current_direction)
            
        if neighbor.symbol != '#':
            neighbors_with_cost.append((1, current_direction, neighbor))
        
        for direction in self.turns[current_direction]:
            neighbor = self._neighbor(direction)
            
            if neighbor.symbol != '#':
                neighbors_with_cost.append((1001, direction, neighbor))

        return neighbors_with_cost

    def find_cheapest_path(self, current_direction, current_cost):
        if self.symbol == 'E':
            global ABSOLUTE_MIN
            ABSOLUTE_MIN = min(current_cost, ABSOLUTE_MIN)
            
            return current_cost

        neighbors = self.neighbors(current_direction)
        cheapest_cost = float('inf')
        
        for (cost, direction, neighbor) in neighbors:
            if neighbor.visited[direction]:
                continue

            if current_cost + cost >= ABSOLUTE_MIN:
                continue

            neighbor.visited[direction] = True

            neighbor_cost = neighbor.find_cheapest_path(direction, current_cost + cost)
            cheapest_cost = min(cheapest_cost, neighbor_cost)

            neighbor.visited[direction] = False

        return cheapest_cost


with open('input.txt') as f:
    matrix = [list(l.strip()) for l in f.readlines()]

for coords, symbol in enumerate_n(matrix, n=2):
    matrix[coords[0]][coords[1]] = Node(symbol=symbol, coords=coords, matrix=matrix)

reindeer = next(node for _, node in enumerate_n(matrix, n=2) if node.symbol == 'S')

print(reindeer.find_cheapest_path('east', 0))
