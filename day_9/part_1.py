def sum_block(start, size):
    nth_term = start + size - 1
    total_sum = (size / 2) * (start + nth_term)
    
    return total_sum


def last_with_space(files):
    return next(
        ((index, size) for index, size in reversed(files.items()) if size > 0),
        None
    )


def process_chunk(files, file_id, index, chunksize):
    total = file_id * sum_block(index, chunksize)
    files[file_id] -= chunksize

    return total


with open('input.txt') as f:
    disk_data = [int(i) for i in f.read().strip()]

files = {}
spaces = []

for index, value in enumerate(disk_data):
    if index % 2 == 0:
        files[index // 2] = value
    else:
        spaces.append(value)

total = 0
aux_counter = 0

for index, value in enumerate(disk_data):
    current_index = index // 2

    if index % 2 == 0:
        current_file_id = current_index
        current_filesize = files[current_file_id]
        
        total += process_chunk(files, current_file_id, aux_counter, current_filesize)
        aux_counter += current_filesize
    else:
        current_space_index = current_index
        current_space_size = spaces[current_space_index]

        file = last_with_space(files)
        
        if file is None:
            continue

        current_file_id, current_filesize = file

        while current_space_size >= current_filesize:
            total += process_chunk(files, current_file_id, aux_counter, current_filesize)

            aux_counter += current_filesize
            current_space_size -= current_filesize
            
            file = last_with_space(files)

            if file is None:
                break

            current_file_id, current_filesize = last_with_space(files)
            
        if current_space_size == 0 or file is None:
            continue

        total += process_chunk(files, current_file_id, aux_counter, current_space_size)
        aux_counter += current_space_size

print(int(total))
