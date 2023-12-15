def hash(s):
    current_value = 0
    for c in s:
        current_value += ord(c)
        current_value *= 17
        current_value %= 256
    return current_value

def solve(input_file):
    f = open(input_file, 'r')
    line = f.read().strip()
    instructions = line.split(',')
    # instructions = 'rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7'.split(',')

    def part1():
        sum = 0
        for instruction in instructions:
            val = hash(instruction)
            sum += val
        return sum

    def part2():
        boxes = [[] for _ in range(256)]
        for instruction in instructions:
            if instruction[-1] == '-':
                label = instruction[:-1]
                relevant_box = hash(label)
                for i, lens in enumerate(boxes[relevant_box]):
                    if label in lens:
                        boxes[relevant_box].pop(i)
            elif instruction[-2] == '=':
                focal_length = int(instruction[-1])
                label = instruction[:-2]
                relevant_box = hash(label)
                lens_found = False
                for i, lens in enumerate(boxes[relevant_box]):
                    if label in lens:
                        boxes[relevant_box][i] = {label: focal_length}
                        lens_found = True
                if not lens_found:
                    boxes[relevant_box].append({label: focal_length})
        sum = 0
        for i, box in enumerate(boxes):
            for j, lens in enumerate(box):
                focusing_power = (1 + i) * (1 + j) * list(lens.values())[0]
                sum += focusing_power
        return sum

    print('day 15')
    print('part 1:', part1())
    print('part 2:', part2())

if __name__ == '__main__':
    solve('inputs/15.txt')
