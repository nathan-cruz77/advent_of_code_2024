from dataclasses import dataclass
from dataclasses import field

import heapq

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
        'east': (0, 1),
        'northeast': (-1, 1),
        'northwest': (-1, -1),
        'southeast': (1, 1),
        'southwest': (1, -1)
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

    # Makes nodes equal if they have the same `coords`.
    def __eq__(self, other):
        return self.coords == other.coords

    def __lt__(self, other):
        return self.distance < other.distance

    def reset(self):
        self.visited = False
        self.disatnce = float('inf')


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
            neighbor.distance = min(neighbor.distance, node.distance + 1)

            if not neighbor.visited:
                heapq.heappush(nodes, neighbor)
