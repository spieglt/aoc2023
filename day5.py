import re

class Mapper:
    def __init__(self):
        self.ends = []
        self.starts = []
        self.ranges = []

reference = {
    'seed-to-soil': Mapper(),
    'soil-to-fertilizer': Mapper(),
    'fertilizer-to-water': Mapper(),
    'water-to-light': Mapper(),
    'light-to-temperature': Mapper(),
    'temperature-to-humidity': Mapper(),
    'humidity-to-location': Mapper(),
}

def trace(value, mapper):
    found = False
    dst = None
    for i in range(len(mapper.starts)):
        start = mapper.starts[i]
        r = mapper.ranges[i]
        if value in range(start, start + r):
            dst = mapper.ends[i] + (value - start)
            found = True
            break
    if not found:
        dst = value
    return dst

def seed_to_location(seed):
    soil = trace(seed, reference['seed-to-soil'])
    fertilizer = trace(soil, reference['soil-to-fertilizer'])
    water = trace(fertilizer, reference['fertilizer-to-water'])
    light = trace(water, reference['water-to-light'])
    temperature = trace(light, reference['light-to-temperature'])
    humidity = trace(temperature, reference['temperature-to-humidity'])
    location = trace(humidity, reference['humidity-to-location'])
    return location

def reverse_trace(value, mapper):
    found = False
    src = None
    for i in range(len(mapper.ends)):
        end = mapper.ends[i]
        r = mapper.ranges[i]
        if value in range(end, end + r):
            src = mapper.starts[i] + (value - end)
            found = True
            break
    if not found:
        src = value
    return src

def location_to_seed(location):
    humidity = reverse_trace(location, reference['humidity-to-location'])
    temperature = reverse_trace(humidity, reference['temperature-to-humidity'])
    light = reverse_trace(temperature, reference['light-to-temperature'])
    water = reverse_trace(light, reference['water-to-light'])
    fertilizer = reverse_trace(water, reference['fertilizer-to-water'])
    soil = reverse_trace(fertilizer, reference['soil-to-fertilizer'])
    seed = reverse_trace(soil, reference['seed-to-soil'])
    return seed

def day5(input_file):
    f = open(input_file, 'r')
    lines = [l.strip() for l in f.readlines()]
    seeds = lines[0][len('seeds: '):].split(' ')
    seeds = [int(s) for s in seeds]

    current_key = ''
    for line in lines[1:]: # skip seeds line
        if re.match('\d+ \d+ \d', line):
            vals = line.split(' ')
            vals = [int(v) for v in vals]
            reference[current_key].ends.append(vals[0])
            reference[current_key].starts.append(vals[1])
            reference[current_key].ranges.append(vals[2])
        else:
            for k in reference.keys():
                if k in line:
                    current_key = k

    def part1():
        smallest_location = None
        for seed in seeds:
            location = seed_to_location(seed)
            if smallest_location == None or location < smallest_location:
                smallest_location = location
        return smallest_location

    def part2():
        # get seeds and ranges
        seed_starts = []
        seed_ranges = []
        for i in range(len(seeds)):
            if i % 2 == 0:
                seed_starts.append(seeds[i])
            else:
                seed_ranges.append(seeds[i])
        seed_ranges = [range(seed_starts[i], seed_starts[i] + seed_ranges[i]) for i in range(len(seed_starts))]
        # sort locations by smallest
        location_ends_starts_ranges = []
        for i in range(len(reference['humidity-to-location'].ends)):
            location_ends_starts_ranges.append((
                reference['humidity-to-location'].ends[i],
                reference['humidity-to-location'].starts[i],
                reference['humidity-to-location'].ranges[i],
            ))
        sorted_locations = sorted(location_ends_starts_ranges, key = lambda x: x[0])
        # testing the lowest value in each location end range to find out which one starts to map to a seed
        smallest_location = None
        for end_start_range in sorted_locations:
            end = end_start_range[0]
            seed = location_to_seed(end)
            for r in seed_ranges:
                if seed in r:
                    # print('ties back to a seed:', end)
                    smallest_location = end
            if smallest_location != None:
                break
        # now we know the range... now walk backwards?
        # can do this by thousands because it takes too long otherwise,
        # and because the ranges are all considerably larger than 1000.
        # this is not the right way to do this problem, but i didn't know what interval trees were
        # till after i wrote this
        for i in range(smallest_location, 0, -1000):
            seed = location_to_seed(i)
            for r in seed_ranges:
                if seed in r:
                    # print(f'seed: {seed}, location: {i}')
                    smallest_location = i
        return smallest_location
    
    print('\nday 5')
    print('part 1:', part1())
    print('part 2:', part2())
