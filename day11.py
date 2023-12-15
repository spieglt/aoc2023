import itertools

def distance_between(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def sum_distances(coord_pairs):
    combinations = itertools.combinations(coord_pairs, 2)
    distances = [distance_between(p1, p2) for (p1, p2) in combinations]
    return sum(distances)

def get_expanded_coords(space_map, empty_rows, empty_columns, scale_factor):
    coords = []
    for y in range(len(space_map)):
        for x in range(len(space_map[0])):
            if space_map[y][x] == '#':
                expanded_x = x + (scale_factor - 1) * sum(col < x for col in empty_columns)
                expanded_y = y + (scale_factor - 1) * sum(row < y for row in empty_rows)
                coords.append((expanded_x, expanded_y))
    return coords

def get_empties(space_map):
    empty_rows = []
    empty_columns = list(range(len(space_map[0])))
    for y in range(len(space_map)):
        if all(map(lambda x: x == '.', space_map[y])):
            empty_rows.append(y)
        for x in range(len(space_map[0])):
            if x in empty_columns and space_map[y][x] == '#':
                empty_columns.remove(x)
    return empty_rows, empty_columns

def solve(input_file):
    f = open(input_file, 'r')
    lines = [list(l.strip()) for l in f.readlines()]

    empty_rows, empty_columns = get_empties(lines)

    def part1():
        coords = get_expanded_coords(lines, empty_rows, empty_columns, 2)
        return sum_distances(coords)

    def part2():
        coords = get_expanded_coords(lines, empty_rows, empty_columns, 1_000_000)
        return sum_distances(coords)

    print('day 11')
    print('part 1:', part1())
    print('part 2:', part2())

if __name__ == '__main__':
    solve('inputs/11.txt')

# naive way

# import copy

# def insert_row(space_map, row_num):
#     empty_row = ['.'] * len(space_map[0])
#     space_map.insert(row_num, empty_row)

# def insert_column(space_map, col_num):
#     for line in space_map:
#         line.insert(col_num, '.')

    # def part1():
    #     expanded = copy.deepcopy(lines)
    #     for row in empty_rows[::-1]: # walk these backwards so we don't put later ones in wrong places after map has been altered by previous ones
    #         insert_row(expanded, row)
    #     for col in empty_columns[::-1]:
    #         insert_column(expanded, col)

    #     coords = []
    #     for y in range(len(expanded)):
    #         for x in range(len(expanded[0])):
    #             if expanded[y][x] == '#':
    #                 coords.append((x, y))

    #     return sum_distances(coords)