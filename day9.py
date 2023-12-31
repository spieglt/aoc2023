
def construct_pyramid(seq):
    pyramid = [seq]
    current_layer = 0
    while True:
        if all(map(lambda x: x == 0, pyramid[current_layer])):
            break
        new_layer = []
        for i, v in enumerate(pyramid[current_layer]):
            if i == 0:
                continue
            new_layer.append(v - pyramid[current_layer][i - 1])
        pyramid.append(new_layer)
        current_layer += 1
    return pyramid

def solve(input_file):
    f = open(input_file, 'r')
    lines = [l.strip() for l in f.readlines()]
    sequences = [l.split(' ') for l in lines]
    for i in range(len(sequences)):
        sequences[i] = [int(n) for n in sequences[i]]

    def part1():
        sum = 0
        for seq in sequences:
            pyramid = construct_pyramid(seq)
            next_value = 0
            for i in range(len(pyramid)):
                previous_layer = pyramid[-(i+2)]
                next_value = next_value + previous_layer[-1]
                if i == len(pyramid) - 2:
                    break
            sum += next_value
        return sum

    def part2():
        sum = 0
        for seq in sequences:
            pyramid = construct_pyramid(seq)
            next_value = 0
            for i in range(len(pyramid)):
                previous_layer = pyramid[-(i+2)]
                next_value = previous_layer[0] - next_value
                if i == len(pyramid) - 2:
                    break
            sum += next_value
        return sum

    print('day 9')
    print('part 1:', part1())
    print('part 2:', part2())

if __name__ == '__main__':
    solve('inputs/9.txt')
