import copy

u = 'U'
d = 'D'
l = 'L'
r = 'R'

def get_dimensions(directions, lengths):
    x_min, x_max, y_min, y_max = 0, 0, 0, 0
    x, y = 0, 0
    for i, direction in enumerate(directions):
        if direction == u:
            y -= lengths[i]
        if direction == d:
            y += lengths[i]
        if direction == l:
            x -= lengths[i]
        if direction == r:
            x += lengths[i]
        if x < x_min:
            x_min = x
        if x > x_max:
            x_max = x
        if y < y_min:
            y_min = y
        if y > y_max:
            y_max = y
    return (x_min, x_max, y_min, y_max)

def go(cursor, direction, length, land):
    length += 1
    x, y = cursor[0], cursor[1]
    if direction == 'U':
        for i in range(length):
            land[y-i][x] = '#'
        return (x, y-i)
    if direction == 'D':
        for i in range(length):
            land[y+i][x] = '#'
        return (x, y+i)
    if direction == 'L':
        for i in range(length):
            land[y][x-i] = '#'
        return (x-i, y)
    if direction == 'R':
        for i in range(length):
            land[y][x+i] = '#'
        return (x+i, y)

def paint(cursor, direction, length, land):
    length += 1
    x, y = cursor[0], cursor[1]
    if direction == 'U':
        for i in range(length):
            if land[y-i][x+1] == ' ':
                land[y-i][x+1] = 'O'
        return (x, y-i)
    if direction == 'D':
        for i in range(length):
            if land[y+i][x-1] == ' ':
                land[y+i][x-1] = 'O'
        return (x, y+i)
    if direction == 'L':
        for i in range(length):
            if land[y-1][x-i] == ' ':
                land[y-1][x-i] = 'O'
        return (x-i, y)
    if direction == 'R':
        for i in range(length):
            if land[y+1][x+i] == ' ':
                land[y+1][x+i] = 'O'
        return (x+i, y)

def get_lake_size(directions, lengths):
    
        # get dimensions needed for lake
        dimensions = get_dimensions(directions, lengths)
        width = abs(dimensions[0]) + abs(dimensions[1]) + 1
        height = abs(dimensions[2]) + abs(dimensions[3]) + 1

        #  make space for the lake
        cursor = (abs(dimensions[0]), abs(dimensions[2]))
        row = [' ' for _ in range(width)]
        land = [copy.deepcopy(row) for _ in range(height)]

        # draw the border path
        for i, direction in enumerate(directions):
            cursor = go(cursor, direction, lengths[i], land)
        assert cursor == (abs(dimensions[0]), abs(dimensions[2]))

        # mark the inside of the path with O
        for i, direction in enumerate(directions):
            cursor = paint(cursor, direction, lengths[i], land)
        assert cursor == (abs(dimensions[0]), abs(dimensions[2]))
        
        land[cursor[1]][cursor[0]] = 'X'

        # fill in the rest of the interior
        for y in range(len(land)):
            interior = False
            for x in range(len(land[0])):
                if interior and land[y][x] == ' ':
                    land[y][x] = 'O'
                if land[y][x] == 'O':
                    interior = True
                if land[y][x] not in 'O ':
                    interior = False

        # count all interior and border tiles
        total_lava = 0
        for r in land:
            total_lava += r.count('#')
            total_lava += r.count('O')
            print(''.join(r))
        return total_lava

def get_points(directions, lengths):
    points = {}
    x, y = 0, 0
    for i, direction in enumerate(directions):
        new_points = []
        if direction == 'U':
            for j in range(lengths[i] + 1):
                new_points.append((x, y-j))
            y -= j
        if direction == 'D':
            for j in range(lengths[i] + 1):
                new_points.append((x, y+j))
            y += j
        if direction == 'L':
            for j in range(lengths[i] + 1):
                new_points.append((x-j, y))
            x -= j
        if direction == 'R':
            for j in range(lengths[i] + 1):
                new_points.append((x+j, y))
            x += j
        for point in new_points:
            xs_for_y = points.get(point[1])
            if not xs_for_y:
                points[point[1]] = {point[0]}
            else:
                xs_for_y.add(point[0])
    print(len(points))
    return points

def new_get_lake_size(directions, lengths):
    total = 0
    points = get_points(directions, lengths)
    print(f'points: {points}')
    dimensions = get_dimensions(directions, lengths)
    for y in range(dimensions[2], dimensions[3] + 5):
        row = points.get(y)
        if row:
            row_total = 0
            sorted_row = sorted(row)
            interior = False
            for i, x in enumerate(sorted_row):

                



                row_total += 1 # add current x, even if on horizontal line
                print(f'added one for ({x}, {y})')
                if i + 1 < len(sorted_row): # if there is no next x, there can't be a closing wall
                    if sorted_row[i+1] - x > 1: # if there's a gap between this x and the next one, we're crossing a wall, detect inside/outside
                        interior = not interior
                        if interior:
                            row_total += sorted_row[i+1] - x
                            print(f'adding {row_total} for ({x}, {y}) to ({sorted_row[i+1]}, {y})')
                    # else: determine wall type: s or u or A. get wall beginning and end. 
            print(f'total for row {y}: {row_total}')
            total += row_total
    return total

def solve(input_file):
    f = open(input_file, 'r')
    lines = [l.strip() for l in f.readlines()]
    lines = [l.split(' ') for l in lines]
    directions = [l[0] for l in lines]
    lengths = [int(l[1]) for l in lines]
    colors = [l[2] for l in lines]

    def part1():
        print('new:', new_get_lake_size(directions, lengths))
        return get_lake_size(directions, lengths)


    def part2():
        length_map = {'0': 'R', '1': 'D', '2': 'L', '3': 'U'}
        new_directions = [length_map[c[7]] for c in colors]
        new_lengths = [int(c[2:7], 16) for c in colors]
        return new_get_lake_size(new_directions, new_lengths)

    print('day 18')
    print('part 1:', part1())
    # print('part 2:', part2())

if __name__ == '__main__':
    solve('inputs/18.txt')
