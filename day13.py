import copy

test = '''
#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#
'''

def detect_mirror_vertical(lines, ignore_column):
    cols = []
    for x in range(len(lines[0])):
        col = ([row[x] for row in lines])
        cols.append(col)
    for i, col in enumerate(cols):
        mirror_broken = False
        cols_left = cols[:i]
        cols_right = cols[i:]
        num_cols_to_check = min(len(cols_left), len(cols_right))
        if not num_cols_to_check:
            mirror_broken = True
        for j in range(num_cols_to_check):
            col_left = cols[i-j-1]
            col_right = cols[i+j]
            for k in range(len(col_left)):
                if col_left[k] != col_right[k]:
                    mirror_broken = True
            if mirror_broken:
                break
        if not mirror_broken and i != ignore_column:
            return (i, len(cols_left))

def detect_mirror_horizontal(lines, ignore_row):
    for i, row in enumerate(lines): # test every line for horizontal reflection
        mirror_broken = False
        rows_above = lines[:i]
        rows_below = lines[i:]
        num_rows_to_check = min(len(rows_above), len(rows_below))
        if not num_rows_to_check:
            mirror_broken = True
        for j in range(num_rows_to_check): # mirroring test, looking above and below
            row_above = lines[i-j-1]
            row_below = lines[i+j]
            for k in range(len(row_above)): # scanning the row
                if row_above[k] != row_below[k]:
                    mirror_broken = True
            if mirror_broken:
                break
        if not mirror_broken and i != ignore_row: # we found a valid reflection
            return (i, len(rows_above))

def solve(input_file):
    f = open(input_file, 'r')
    all_puzzles = f.read()
    str_puzzles = all_puzzles.split('\n\n')
    # str_puzzles = test.split('\n\n') # overwrite with tests
    puzzles = []
    for str_puzzle in str_puzzles:
        lines = str_puzzle.split('\n')
        lines = [list(l) for l in lines if l]
        puzzles.append(lines)

    old_horizontal_reflection_indices = [None for _ in range(len(puzzles))]
    old_vertical_reflection_indices = [None for _ in range(len(puzzles))]

    def part1():
        sum = 0
        for i, puzzle in enumerate(puzzles):
            res = detect_mirror_horizontal(puzzle, None)
            if res:
                old_horizontal_reflection_indices[i] = res[0]
                rows_above = res[1]
                sum += rows_above * 100
            res = detect_mirror_vertical(puzzle, None)
            if res:
                old_vertical_reflection_indices[i] = res[0]
                rows_to_left = res[1]
                sum += rows_to_left
        return sum

    def part2():
        sum = 0
        for i, puzzle in enumerate(puzzles):
            for y in range(len(puzzle)):
                skip_puzzle = False
                for x in range(len(puzzle[0])):
                    smudge_puzzle = copy.deepcopy(puzzle)
                    if smudge_puzzle[y][x] == '.':
                        smudge_puzzle[y][x] = '#'
                    else:
                        smudge_puzzle[y][x] = '.'
                    res = detect_mirror_horizontal(smudge_puzzle, old_horizontal_reflection_indices[i])
                    if res and old_horizontal_reflection_indices[i] != res[0]:
                        rows_above = res[1]
                        sum += rows_above * 100
                        skip_puzzle = True
                        break
                    res = detect_mirror_vertical(smudge_puzzle, old_vertical_reflection_indices[i])
                    if res and old_vertical_reflection_indices[i] != res[0]:
                        rows_to_left = res[1]
                        sum += rows_to_left
                        skip_puzzle = True
                        break
                if skip_puzzle:
                    break
        return sum

    print('day 13')
    print('part 1:', part1())
    print('part 2:', part2())

if __name__ == '__main__':
    solve('inputs/13.txt')
