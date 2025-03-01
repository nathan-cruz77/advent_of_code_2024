from dataclasses import dataclass
from dataclasses import field


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

    directions = {
        'north': (-1, 0),
        'south': (1, 0),
        'west': (0, -1),
        'east': (0, 1)
    }

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

    def neighbors(self):
        return [{'node': self._neighbor(direction), 'direction': direction} for direction in self.directions if self._neighbor(direction) is not None]

    def move(self, direction):
        neighbor = self._neighbor(direction)

        if neighbor.symbol == 'O':
            neighbor.move(direction)

        neighbor = self._neighbor(direction)

        matrix[self.coords[0]][self.coords[1]] = neighbor
        matrix[neighbor.coords[0]][neighbor.coords[1]] = self

        self.coords, neighbor.coords = neighbor.coords, self.coords


    def can_move(self, direction):
        neighbor = self._neighbor(direction)

        if neighbor.symbol == '.':
            return True

        if neighbor.symbol == '#':
            return False

        return neighbor.can_move(direction)


with open('input.txt') as f:
    data = f.read()

    matrix_data, movements = data.split('\n\n')

    matrix = [list(l) for l in matrix_data.splitlines()]
    movements = [c for c in movements if c in {'<', '>', '^', 'v'}]

for coords, symbol in enumerate_n(matrix, n=2):
    matrix[coords[0]][coords[1]] = Node(symbol=symbol, coords=coords, matrix=matrix)

movement_mapping = {
    '<': 'west',
    '>': 'east',
    '^': 'north',
    'v': 'south'
}

robot = next(node for _, node in enumerate_n(matrix, n=2) if node.symbol == '@')

for movement in movements:
    direction = movement_mapping[movement]
    
    if robot.can_move(direction):
        robot.move(direction)

total = 0
for coords, node in enumerate_n(matrix, n=2):
    if node.symbol == 'O':
        total += 100 * coords[0] + coords[1]

print(total)
