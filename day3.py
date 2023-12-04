
number_characters = '0123456789'
nonsymbols = '.' + number_characters

class Number:
    def __init__(self):
        self.string_rep = ''
        self.x_coords = []
        self.y_coord = None
    def value(self):
        return int(self.string_rep)
    
class Gear:
    def __init__(self, x, y):
        self.x_coord = x
        self.y_coord = y

def search_up(number, schematic):
    if number.y_coord == 0:
        return False
    for x in number.x_coords:
        # above
        if schematic[number.y_coord - 1][x] not in nonsymbols:
            return True
        # above-left
        if x > 0 and schematic[number.y_coord - 1][x - 1] not in nonsymbols:
            return True
        # above-right
        if x + 1 < len(schematic[number.y_coord]) and schematic[number.y_coord - 1][x + 1] not in nonsymbols:
            return True
    return False

def search_down(number, schematic):
    if number.y_coord == len(schematic) - 1: # last row
        return False
    for x in number.x_coords:
        # below
        if schematic[number.y_coord + 1][x] not in nonsymbols:
            return True
        # below-left
        if x > 0 and schematic[number.y_coord + 1][x - 1] not in nonsymbols:
            return True
        # below-right
        if x + 1 < len(schematic[number.y_coord]) and schematic[number.y_coord + 1][x + 1] not in nonsymbols:
            return True
    return False

def search_left(number, schematic):
    for x in number.x_coords:
        if x > 0 and schematic[number.y_coord][x - 1] not in nonsymbols:
            return True
    return False

def search_right(number, schematic):
    for x in number.x_coords:
        if x + 1 < len(schematic[number.y_coord]) and schematic[number.y_coord][x + 1] not in nonsymbols:
            return True
    return False

def search_number(number, schematic):
    return search_up(number, schematic) \
        or search_down(number, schematic) \
        or search_left(number, schematic) \
        or search_right(number, schematic)

def find_numbers(schematic):
    numbers = []
    for y, row in enumerate(schematic):
        constructing_number = False
        for x, char in enumerate(row):
            if char in number_characters:
                if constructing_number:
                    # add current number to one we're building
                    numbers[-1].string_rep += char
                    numbers[-1].x_coords.append(x)
                    numbers[-1].y_coord = y
                else:
                    # start new number, signal that we're in one
                    new_number = Number()
                    new_number.string_rep += char
                    # new_number.x_coords = [] # TODO: why was this necessary before making __init__() for Number? without, python keeps the x_coords list from the previous number
                    new_number.x_coords.append(x)
                    new_number.y_coord = y
                    numbers.append(new_number)
                    constructing_number = True
            else: # signal that we're not in a number
                constructing_number = False
    return numbers

def find_gears(schematic):
    gears = []
    for y, row in enumerate(schematic):
        for x, char in enumerate(row):
            if char == '*':
                gears.append(Gear(x, y))
    return gears                

def day3(input_file):
    f = open(input_file, 'r')
    schematic = [l.strip() for l in f.readlines()]
    def part1():
        # get all numbers and their x and y coordinates
        numbers = find_numbers(schematic)
        # for each number, check if it's adjacent to a symbol
        # if so, add it to sum
        sum = 0
        for n in numbers:
            if search_number(n, schematic):
                sum += n.value()
        return sum

    def part2():
        # find gear locations. find number locations. for each gear, search each number. if number is adjacent, keep. if total numbers != 2, abandon.
        # what does it mean for number to be adjacent to gear? if, for y coord and some x coord of number, abs(gear_x - num_x) <= 1 and abs(gear_y - num_y) <= 1.
        # don't need to worry about case where both could be zero, number and gear can't be in same place.
        gears = find_gears(schematic)
        numbers = find_numbers(schematic)
        sum = 0
        for gear in gears:
            adjacent_numbers = []
            for number in numbers:
                is_adjacent = False
                for x in number.x_coords:
                    if abs(gear.x_coord - x) <= 1 and abs(gear.y_coord - number.y_coord) <= 1:
                        is_adjacent = True
                if is_adjacent:
                    adjacent_numbers.append(number)
            if len(adjacent_numbers) == 2:
                ratio = adjacent_numbers[0].value() * adjacent_numbers[1].value()
                sum += ratio
        return sum

    print('\nday 3')
    print('part 1:', part1())
    print('part 2:', part2())
