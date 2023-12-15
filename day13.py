
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

def detect_mirror_vertical(lines):
    cols = []
    for x in range(len(lines[0])):
        col = ([row[x] for row in lines])
        cols.append(col)
    # for col in cols:
        # print(f'col: {col}')
    for i, col in enumerate(cols): # test every column for vertical reflection
        mirror_broken = False
        cols_left = cols[:i]
        cols_right = cols[i:]
        num_cols_to_check = min(len(cols_left), len(cols_right))
        if not num_cols_to_check:
            mirror_broken = True
        for j in range(num_cols_to_check):
            col_left = cols[i-j-1]
            col_right = cols[i+j]
            # print(f'left: {col_left}, right: {col_right}')
            for k in range(len(col_left)):
                if col_left[k] != col_right[k]:
                    # print('broken')
                    mirror_broken = True
            if mirror_broken:
                break
        if not mirror_broken:
            # print(f'vertical reflection at {i}')
            return (i, len(cols_left))
        # else: print(f'no vertical reflection at {i}')

def detect_mirror_horizontal(lines):
    for i, row in enumerate(lines): # test every line for horizontal reflection
        # print('lines:', lines)
        mirror_broken = False
        rows_above = lines[:i]
        rows_below = lines[i:]
        # print(f'\ni = {i}\nrows above: {rows_above}\nrows below: {rows_below}')
        num_rows_to_check = min(len(rows_above), len(rows_below))
        if not num_rows_to_check:
            mirror_broken = True
        # print(f'num to check: {num_rows_to_check}')
        for j in range(num_rows_to_check): # mirroring test, looking above and below
            row_above = lines[i-j-1]
            row_below = lines[i+j]
            # print(f'above: {row_above}, below: {row_below}')
            for k in range(len(row_above)): # scanning the row
                if row_above[k] != row_below[k]:
                    # print('broken')
                    mirror_broken = True
            if mirror_broken:
                break
        if not mirror_broken: # we found a valid reflection
            # print(f'horizontal reflection at {i}')
            return (i, len(rows_above))
        # else:
            # print(f'no horizontal reflection at {i}')

def solve(input_file):
    f = open(input_file, 'r')
    all_puzzles = f.read()
    str_puzzles = all_puzzles.split('\n\n')
    # str_puzzles = test.split('\n\n') # overwrite with tests
    puzzles = []
    for str_puzzle in str_puzzles:
        # print('\nstr_puzzle\n' + str_puzzle)
        lines = str_puzzle.split('\n')
        lines = [list(l) for l in lines if l]
        puzzles.append(lines)

    def part1():
        sum = 0
        for i, puzzle in enumerate(puzzles):
            print('\ncurrent puzzle:')
            print(str_puzzles[i])
            res = detect_mirror_horizontal(puzzle)
            if res:
                horizontal_index = res[0]
                rows_to_left = res[1]
                print(f'horizontal reflection at {horizontal_index}')
                sum += rows_to_left * 100
            res = detect_mirror_vertical(puzzle)
            if res:
                vertical_index = res[0]
                rows_above = res[1]
                print(f'vertical reflection at {vertical_index}')
                sum += rows_above
        return sum

    def part2():
        pass

    print('day 13')
    print('part 1:', part1())
    print('part 2:', part2())

if __name__ == '__main__':
    solve('inputs/13.txt')
