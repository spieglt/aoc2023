import copy

north = 0
south = 1
east = 2
west = 3

seen = {}

def coords_to(direction, x, y):
    if direction == north:
        return x, y-1
    if direction == south:
        return x, y+1
    if direction == east:
        return x+1, y
    if direction == west:
        return x-1, y

def slide_to(direction, x, y, lines):
    hit_solid = False
    i = 0
    dst = None
    while not hit_solid:
        i += 1
        if direction == north:
            if y-i == 0:
                break
            dst = lines[y-i][x] # x, y-i
        if direction == south:
            if y+i == len(lines):
                break
            dst = lines[y+i][x] # x, y+i
        if direction == east:
            if x+i == len(lines[0]):
                break
            dst = lines[y][x+i] # x+i, y
        if direction == west:
            if x-i == 0:
                break
            dst = lines[y][x-i] # x-i, y
        hit_solid = dst != '.'
    i -= 1 # only travel one shy of solid
    if direction == north:
        lines[y][x] = '.'
        lines[y-i][x] = 'O'
    if direction == south:
        lines[y][x] = '.'
        lines[y+i][x] = 'O'
    if direction == east:
        lines[y][x] = '.'
        lines[y][x+i] = 'O'
    if direction == west:
        lines[y][x] = '.'
        lines[y][x-i] = 'O'

# TODO: broken, and tilt() is too slow
def tilt_faster(lines, direction):
    # if we're tilting north, need to start with first row. if tilting south, start with last row and slide every O south
    if direction == north:
        for y, row in enumerate(lines):
            if y == 0:
                continue
            for x, char in enumerate(row):
                if char == 'O':
                    slide_to(north, x, y, lines)
    if direction == south:
        for i in range(len(lines)):
            if i == 0:
                continue
            y = len(lines) - i - 1
            row = lines[y]
            for x, char in enumerate(row):
                if char == 'O':
                    slide_to(south, x, y, lines)
    if direction == east: # start with ends of rows
        for y, row in enumerate(lines):
            for i in range(len(row)):
                if i == 0:
                    continue
                x = len(row) - i - 1
                if row[x] == 'O':
                    slide_to(east, x, y, lines)
    if direction == west:
        for y, row in enumerate(lines):
            for x, char in enumerate(row):
                if x == 0:
                    continue
                if char == 'O':
                    slide_to(west, x, y, lines)

def tilt(lines, direction):
    while True:
        shifted = False
        for y, row in enumerate(lines):
            if (direction == north and y == 0) or (direction == south and y == len(lines) - 1):
                continue
            for x, char in enumerate(row):
                if (direction == west and x == 0) or (direction == east and x == len(row) - 1):
                    continue
                adj_x, adj_y = coords_to(direction, x, y)
                adj_char = lines[adj_y][adj_x]
                if char == 'O' and adj_char == '.':
                    lines[adj_y][adj_x] = 'O'
                    lines[y][x] = '.'
                    shifted = True
        if not shifted:
            break

def serialize(lines):
    str_lines = [''.join(line) for line in lines]
    return '\n'.join(str_lines)

def spin_cycle(lines):
    for direction in [north, west, south, east]:
        tilt(lines, direction)

def calculate_load(lines):
    total_load = 0
    for y, row in enumerate(lines):
        factor = len(lines) - y
        num_rocks = row.count('O')
        total_load += num_rocks * factor
    return total_load

def solve(input_file):
    f = open(input_file, 'r')
    original_lines = [list(l.strip()) for l in f.readlines()]

    def part1():
        lines = copy.deepcopy(original_lines)
        tilt(lines, north)
        return calculate_load(lines)

    def part2():
        lines = copy.deepcopy(original_lines)
        target = 1_000_000_000
        for i in range(1, target):
            seen[serialize(lines)] = i
            spin_cycle(lines)
            if serialize(lines) in seen:
                loop_starts_at = seen[serialize(lines)]
                loop_length = i - loop_starts_at + 1 # why this plus one?
                print(f'loop detected. i = {i}. loop started at {loop_starts_at}. period is {loop_length}.')
                break
        cycles_needed = ((target - loop_starts_at) % loop_length) + loop_starts_at
        lines = copy.deepcopy(original_lines)
        for i in range(cycles_needed):
            spin_cycle(lines)
        return calculate_load(lines)

    print('day 14')
    print('part 1:', part1())
    print('part 2:', part2())

if __name__ == '__main__':
    solve('inputs/14.txt')
