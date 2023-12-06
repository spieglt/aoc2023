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

def stitch_maps(map1, map2):
    # stitch ends of map1 to starts of map2
    # return new maps that translate from starts of map1 to ends of map2
    new_map = Mapper()
    translator = []
    for i in range(len(map1.ends)):
        m1_start = map1.ends[i] # this is us grabbing from the ends of map 1
        m1_end = m1_start + map1.ranges[i]
        for j in range(len(map1.starts)):
            m2_start = map2.starts[j] # here we grab the starts of map 2
            m2_end = m2_start + map2.ranges[i]
            if (m1_end > m2_start  # one possible partial overlap
                or m2_end > m1_start # other partial overlap
                or (m1_start < m2_start and m1_end > m2_end) # 1 contains 2
                or (m1_start < m2_start and m1_end > m2_end)): # 2 contains 1
                start_of_overlap = max(m1_start, m2_start)
                end_of_overlap = min(m1_end, m2_end)
                # is new map a translation layer? it represents overlaps of map 1's ends and map2's starts. how does that link map 1 starts to map2 ends? map 1's starts must be revised to line up with this new map's ends.
                # and map 2's must be revised to line up with this new map's starts.

                # no, we're not constructing a map yet.
                # new_map.ends.append(end_of_overlap)
                # new_map.starts.append(start_of_overlap)
                # new_map.ranges.append(end_of_overlap - start_of_overlap)
                
                # translation_range = start_of_overlap to end_of_overlap
                # look these values up in m1 start and m2 end
                # that's the new start and end for new_map, and its range is end - start
                offset_from_end = map1.ends[i] + map1.ranges[i] - m1_end

                


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



    # map1_tuples = []
    # map2_tuples = []
    # don't really need the tuples because we don't need to sort here?
    # for i in range(len(map1.starts)):
    #     map1_tuples.append((
    #         map1.ends[i],
    #         map1.starts[i],
    #         map1.ranges[i],
    #     ))
    # for i in range(len(map2.starts)):
    #     map2_tuples.append((
    #         map2.ends[i],
    #         map2.starts[i],
    #         map2.ranges[i],
    #     ))