import re

criteria = {
    'red': 12,
    'green': 13,
    'blue': 14,
}

def solve(input_file):
    def part1(input_file):
        f = open(input_file, 'r')
        sum = 0
        for i, line in enumerate(f): # each iteration of this loop is a game
            game_is_possible = True
            index_of_colon = line.find(':')
            rounds = line[index_of_colon + 1:].split(';')
            for round in rounds:
                for color in ['red', 'green', 'blue']:
                    colors = re.search(f'(\d+) {color}', round)
                    if colors != None:
                        number = colors.group(1)
                        if int(number) > criteria[color]:
                            game_is_possible = False
            if game_is_possible:
                sum += i + 1
        return sum

    def part2(input_file):
        f = open(input_file, 'r')
        sum = 0
        for line in f: # each iteration of this loop is a game
            maximums = {
                'red': 0,
                'green': 0,
                'blue': 0,
            }
            index_of_colon = line.find(':')
            rounds = line[index_of_colon + 1:].split(';')
            for round in rounds:
                for color in ['red', 'green', 'blue']:
                    colors = re.search(f'(\d+) {color}', round)
                    if colors != None:
                        number = int(colors.group(1))
                        if number > maximums[color]:
                            maximums[color] = number
            power = maximums['red'] * maximums['green'] * maximums['blue']
            sum += power
        return sum

    print('\nday 2')
    print('part 1:', part1(input_file))
    print('part 2:', part2(input_file))