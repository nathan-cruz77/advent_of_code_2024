from functools import cache

@cache
def backtrack(pattern, towels):
    if not pattern:
        return 1

    count = 0

    for towel in towels:
        if pattern.startswith(towel):
            count += backtrack(pattern[len(towel):], towels)

    return count


with open('input.txt') as f:
    data = f.read()

    towels_data, patterns_data = data.split('\n\n')

    towels = tuple(towels_data.strip().split(', '))
    patterns = [l for l in patterns_data.splitlines()]

count = 0
for pattern in patterns:
    count += backtrack(pattern, towels)

print(count)
