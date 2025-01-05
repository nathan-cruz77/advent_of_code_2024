from dataclasses import dataclass
from dataclasses import field
from collections import defaultdict
from pprint import pp
import heapq


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

    # Makes nodes equal if they have the same `coords`.
    def __eq__(self, other):
        return self.coords == other.coords

    def __lt__(self, other):
        return self.distance < other.distance

    def unvisit(self):
        self.visited = False
        self.distance = float('inf')


def unvisit(matrix):
    for _, node in enumerate_n(matrix, n=2):
        node.unvisit()


# Finds distance from given `node` to every other node in the graph.optionally
# stopping at `target_symbol`.
def dijkstra(node, target_symbol=None):
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

        # Optionally stop search when we reach the given `target_symbol`
        if target_symbol and node.symbol == target_symbol:
            break

        for neighbor in node.neighbors():
            if neighbor.symbol == '#':
                continue

            neighbor.distance = min(neighbor.distance, node.distance + 1)

            if not neighbor.visited:
                heapq.heappush(nodes, neighbor)


with open('input.txt') as f:
    matrix = [list(l.strip()) for l in f.readlines()]

for coords, symbol in enumerate_n(matrix, n=2):
    matrix[coords[0]][coords[1]] = Node(symbol=symbol, coords=coords, matrix=matrix)

start = next(node for _, node in enumerate_n(matrix, n=2) if node.symbol == 'S')
end = next(node for _, node in enumerate_n(matrix, n=2) if node.symbol == 'E')

dijkstra(start, target_symbol=end.symbol)

distance_frequencies = defaultdict(int)

reference_distance = end.distance
walls = [node for _, node in enumerate_n(matrix, n=2) if node.symbol == '#']

for index, wall in enumerate(walls):
    print(f'{index + 1} / {len(walls)}', end='\r')
    unvisit(matrix)
    
    wall.symbol = '.'
    dijkstra(start, target_symbol=end.symbol)
    wall.symbol = '#'

    distance_frequencies[reference_distance - end.distance] += 1

print()
print(sum(value for key, value in distance_frequencies.items() if key >= 100))
