import math

def solve(input_file):
    f = open(input_file, 'r')
    lines = [l.strip() for l in f.readlines()]
    paths = {}
    for line in lines[2:]:
        paths[line[:3]] = (line[7:10], line[12:15])
    def part1():
        instructions = list(lines[0])
        location = 'AAA'
        steps = 0
        while True:
            for instruction in instructions:
                if instruction == 'L':
                    location = paths[location][0]
                elif instruction == 'R':
                    location = paths[location][1]
                steps += 1
                if location == 'ZZZ':
                    return steps
        
    def part2():
        instructions = list(lines[0])
        locations = []
        all_steps = []
        for path in paths:
            if path[-1] == 'A':
                locations.append(path)
        for location in locations:
            steps = 0
            while True:
                for instruction in instructions:
                    if instruction == 'L':
                        location = paths[location][0]
                    elif instruction == 'R':
                        location = paths[location][1]
                    steps += 1
                if location[-1] == 'Z':
                    break
            all_steps.append(steps)     
        return math.lcm(*all_steps)

    print('day 8')
    print('part 1:', part1())
    print('part 2:', part2())

if __name__ == '__main__':
    solve('inputs/8.txt')
