from dataclasses import dataclass

@dataclass
class Block:
    starting_position: int
    size: int


@dataclass
class File(Block):
    index: int


class Space(Block):
    def fits(self, block):
        return self.size >= block.size and self.starting_position < block.starting_position


def find_first_fitting_space(spaces, file):
    for space in spaces:
        if space.starting_position > file.starting_position:
            return None

        if space.fits(file):
            return space

    return None


def sum_block(start, size):
    nth_term = start + size - 1
    total_sum = (size / 2) * (start + nth_term)
    
    return total_sum


def process_chunk(file_id, index, chunksize):
    return file_id * sum_block(index, chunksize)


with open('input.txt') as f:
    data = f.read().strip()
    
files = []
spaces = []
last_block = Block(starting_position=0, size=0)

for index, disk_entry in enumerate(data):
    disk_entry = int(disk_entry)

    if index % 2 == 0:
        file = File(
            index=index // 2,
            starting_position=last_block.starting_position + last_block.size,
            size=disk_entry
        )

        files.append(file)
        last_block = file
    else:
        space = Space(
            starting_position=last_block.starting_position + last_block.size,
            size=disk_entry
        )

        spaces.append(space)
        last_block = space

total = 0

for file in reversed(files):
    space = find_first_fitting_space(spaces, file)

    if space is not None:
        file.starting_position = space.starting_position

        space.starting_position += file.size
        space.size -= file.size

    total += process_chunk(file.index, file.starting_position, file.size)

print(int(total))
