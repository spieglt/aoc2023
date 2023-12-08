import math

def day6(input_file):
    # f = open(input_file, 'r')
    races = [ # (time, distance)
        (62, 553),
        (64, 1010),
        (91, 1473),
        (90, 1074),
    ]
    
    real_race = (62649190, 553101014731074)

    # brute force solutions, slow

    # def part1():
    #     multiple = 1
    #     for race in races:
    #         number_of_ways = 0
    #         time = race[0]
    #         for ms_held in range(time):
    #             ms_traveling = time - ms_held
    #             mm_traveled = ms_traveling * ms_held
    #             if mm_traveled > race[1]:
    #                 number_of_ways += 1
    #         multiple *= number_of_ways
    #     return multiple

    # def part2():
    #     number_of_ways = 0
    #     time = real_race[0]
    #     for ms_held in range(time):
    #         ms_traveling = time - ms_held
    #         mm_traveled = ms_traveling * ms_held
    #         if mm_traveled > real_race[1]:
    #             number_of_ways += 1
    #     return number_of_ways

    def part1():
        multiple = 1
        for race in races:
            first_zero, second_zero = get_ms_held_to_equal_distance(race[0], race[1])
            if first_zero % 1.0 == 0:
                first_zero += 1
            number_of_ways = math.ceil(second_zero) - math.ceil(first_zero)
            multiple *= number_of_ways
        return multiple
    
    def part2():
        first_zero, second_zero = get_ms_held_to_equal_distance(real_race[0], real_race[1])
        if first_zero % 1.0 == 0:
            first_zero += 1
        return math.ceil(second_zero) - math.ceil(first_zero)

    def get_ms_held_to_equal_distance(time, distance):
        # if time = 62 and distance = 553, 62 - ms_held = ms_traveling
        # ms_held * ms_traveling = distance
        # ms_held * (62 - ms_held) = 553
        # -(ms_held^2) + 62ms_held - 553 = 0, quadratic formula
        a = -1
        b = time
        c = -distance
        first_zero = (-b + math.sqrt(b**2 - (4 * a * c))) / (2 * a)
        second_zero = (-b - math.sqrt(b**2 - (4 * a * c))) / (2 * a)
        return first_zero, second_zero

    print('\nday 6')
    print('part 1:', part1())
    print('part 2:', part2())
