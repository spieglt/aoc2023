import copy

# need loop detection. loops can only start on a branch. only - and | can branch. anytime we hit one of these, even when passing through them, do loop detection?
# loop detection is a matter of detecting "I've been here before, from this direction, from this previous location?" can that happen without a loop? don't think so.
# 2 paths into one loop? yes. loop within loop? yes. if here before, from this previous and this previous direction, don't append it to the queue to search.
# /....\
# ......
# .....|.....<
# ......
# .....|........<
# ......
# \..../

up = 0
down = 1
left = 2
right = 3

direction_map = {
    '.': [(up,), (down,), (left,), (right,)],
    '-': [(left, right), (left, right), (left,), (right,)],
    '|': [(up,), (down,), (up, down), (up, down)],
    '/': [(right,), (left,), (down,), (up,)],
    '\\': [(left,), (right,), (up,), (down,)],
}

def coords_to(x, y, direction, layout):
    if direction == up and y > 0:
        return x, y-1
    if direction == down and y < len(layout) - 1:
        return x, y+1
    if direction == left and x > 0:
        return x-1, y
    if direction == right and x < len(layout[0]) - 1:
        return x+1, y
    return None, None

def solve(input_file):
    f = open(input_file, 'r')
    lines = [list(l.strip()) for l in f.readlines()]

    def get_next_locations(x, y, direction):
        next_locations = []
        current_char = lines[y][x]
        next_directions = direction_map[current_char][direction]
        for next_direction in next_directions:
            next_x, next_y = coords_to(x, y, next_direction, lines)
            if next_x != None:
                next_locations.append((next_x, next_y, next_direction))
        return next_locations

    def walk_map(initial_beam):
        turns_seen = set()
        empty_row = ['.' for _ in range(len(lines[0]))]
        visited_map = [copy.deepcopy(empty_row) for _ in range(len(lines))]
        queue = [initial_beam]
        while queue != []:
            current_beam = queue.pop()
            visited_map[current_beam[1]][current_beam[0]] = '#'
            new_beams = get_next_locations(*current_beam)
            if lines[current_beam[1]][current_beam[0]] in '-|':
                for new_beam in new_beams:
                    current_turn = (new_beam[0], new_beam[1], current_beam[0], current_beam[1], current_beam[2])
                    if current_turn not in turns_seen:
                        turns_seen.add(current_turn)
                        queue.append(new_beam)
            elif new_beams:
                    queue.append(new_beams[0])
        total_visited = 0
        for row in visited_map:
            total_visited += row.count('#')
        return total_visited

    def part1():
        initial_beam = (0, 0, right) # (x, y, direction)
        return walk_map(initial_beam)

    def part2():
        max_energized = 0
        for y in range(len(lines)):
            for (x, d) in [(0, right), (len(lines[0]) - 1, left)]:
                energized = walk_map((x, y, d))
                if energized > max_energized:
                    max_energized = energized
        for x in range(len(lines[0])):
            for (y, d) in [(0, down), (len(lines) - 1, up)]:
                energized = walk_map((x, y, d))
                if energized > max_energized:
                    max_energized = energized
        return max_energized

    print('day 16')
    print('part 1:', part1())
    print('part 2:', part2())

if __name__ == '__main__':
    solve('inputs/16.txt')
