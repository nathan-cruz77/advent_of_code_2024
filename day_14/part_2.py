from dataclasses import dataclass
from itertools import product
import re
import os
import time

ROOM_SIZE=(101, 103)


@dataclass
class Robot:
    coords: tuple
    speed: tuple

    regex = re.compile(r'p=(\d+),(\d+) v=(-?\d+),(-?\d+)')

    def move(self, seconds):
        self.coords = (
            (self.coords[0] + self.speed[0] * seconds) % ROOM_SIZE[0],
            (self.coords[1] + self.speed[1] * seconds) % ROOM_SIZE[1]
        )

    def quadrant(self):
        middle_line = ROOM_SIZE[0] // 2
        middle_column = ROOM_SIZE[1] // 2

        if self.coords[0] == middle_line or self.coords[1] == middle_column:
            return None

        if self.coords[0] < middle_line and self.coords[1] < middle_column:
            return '1'

        if self.coords[0] < middle_line and self.coords[1] > middle_column:
            return '2'

        if self.coords[0] > middle_line and self.coords[1] < middle_column:
            return '3'

        return '4'


    @staticmethod
    def build(line):
        [pos_x, pos_y, spd_x, spd_y] = [int(i) for i in Robot.regex.findall(line)[0]]
        
        coords = (pos_x, pos_y)
        speed = (spd_x, spd_y)

        return Robot(coords=coords, speed=speed)


def print_room(room):
    for x in range(ROOM_SIZE[0]):
        for y in range(ROOM_SIZE[1]):
            print(room[(x, y)], end='')

        print()

    
def clear(room):
    for k in room:
        room[k] = ' '


with open('input.txt') as f:
    robots = [Robot.build(line) for line in f.readlines()]

room = {(x, y): ' ' for x, y in product(range(ROOM_SIZE[0]), range(ROOM_SIZE[1]))}

for robot in robots:
    robot.move(6_731)
    room[robot.coords] = '#'

seconds = 6_731

while True:
    print(f'Second: {seconds}')
    
    print_room(room)
    clear(room)

    for robot in robots:
        robot.move(1)
        room[robot.coords] = '#'

    seconds += 1

    time.sleep(2)
    os.system('clear')
