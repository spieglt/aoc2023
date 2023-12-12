


for i in range(12,26):
    with open(f'days/day{i}.py', 'w') as f:
        template = f'''
def solve(input_file):
    f = open(input_file, 'r')
    lines = [list(l.strip()) for l in f.readlines()]

    def part1():
        pass

    def part2():
        pass

    print('\\nday {i}')
    print('part 1:', part1())
    print('part 2:', part2())
'''
        f.write(template)
