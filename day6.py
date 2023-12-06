
def day6(input_file):
    # f = open(input_file, 'r')
    races = [ # (time, distance)
        (62, 553),
        (64, 1010),
        (91, 1473),
        (90, 1074),
    ]
    
    real_race = (62649190, 553101014731074)

    def part1():
        multiple = 1
        for race in races:
            number_of_ways = 0
            time = race[0]
            for ms_held in range(time):
                ms_traveling = time - ms_held
                mm_traveled = ms_traveling * ms_held
                if mm_traveled > race[1]:
                    number_of_ways += 1
            multiple *= number_of_ways
        return multiple

    def part2():
        number_of_ways = 0
        time = real_race[0]
        for ms_held in range(time):
            ms_traveling = time - ms_held
            mm_traveled = ms_traveling * ms_held
            if mm_traveled > real_race[1]:
                number_of_ways += 1
        return number_of_ways

    print('\nday 6')
    print('part 1:', part1())
    print('part 2:', part2())
