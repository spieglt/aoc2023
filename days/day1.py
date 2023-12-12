
numbers = [
    'one',
    'two',
    'three',
    'four',
    'five',
    'six',
    'seven',
    'eight',
    'nine',
]

def solve(input_file):
    def part1(input_file):
        f = open(input_file, 'r')
        sum = 0
        for line in f:
            line_sum = 0
            for i in range(len(line)):
                if line[i] in '0123456789':
                    line_sum += int(line[i]) * 10
                    break
            for i in range(len(line)):
                if line[-(i+1)] in '0123456789':
                    line_sum += int(line[-(i+1)])
                    break
            sum += line_sum
        return sum

    def part2(input_file):
        f = open(input_file, 'r')
        sum = 0
        for line in f:
            first_number = 0
            last_number = 0
            first_digit_index = 0
            last_digit_index = 0
            
            # check for digits
            for i in range(len(line)):
                if line[i] in '0123456789':
                    first_digit_index = i
                    first_number = int(line[i]) * 10
                    break
            for i in range(len(line)):
                if line[-(i+1)] in '0123456789':
                    last_digit_index = len(line) - (i+1)
                    last_number = int(line[-(i+1)])
                    break
            
            # check for words, get index of earliest number
            indices_of_words = [line.find(num) for num in numbers]
            location_of_smallest_index = -1
            for i, v in enumerate(indices_of_words):
                if v != -1:
                    if location_of_smallest_index == -1:
                        location_of_smallest_index = i
                    if v < indices_of_words[location_of_smallest_index]:
                        location_of_smallest_index = i
            # if earliest word is before earliest digit, replace first_number
            if location_of_smallest_index != -1 and indices_of_words[location_of_smallest_index] < first_digit_index:
                first_number = (location_of_smallest_index + 1) * 10

            # check for words, get index of latest number
            indices_of_words = [line.rfind(num) for num in numbers]
            location_of_largest_index = -1
            for i, v in enumerate(indices_of_words):
                if location_of_largest_index == -1:
                    location_of_largest_index = i
                if v > indices_of_words[location_of_largest_index]:
                    location_of_largest_index = i
            # if latest word is after latest digit, replace last_number
            if location_of_largest_index != -1 and indices_of_words[location_of_largest_index] > last_digit_index:
                last_number = (location_of_largest_index + 1)

            sum += first_number + last_number

        return sum

    print('\nday 1')
    print('part 1:', part1(input_file))
    print('part 2:', part2(input_file))

