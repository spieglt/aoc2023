# this code is bad and could be heavily deduplicated

# | is a vertical pipe connecting north and south.
# - is a horizontal pipe connecting east and west.
# L is a 90-degree bend connecting north and east.
# J is a 90-degree bend connecting north and west.
# 7 is a 90-degree bend connecting south and west.
# F is a 90-degree bend connecting south and east.
# . is ground; there is no pipe in this tile.
# S is the starting position of the animal; there is a pipe on this tile, but your sketch doesn't show what shape the pipe has.

up = 0
down = 1
left = 2
right = 3

def coords_to(src, direction):
    if direction == up:
        return (src[0], src[1]-1)
    if direction == down:
        return (src[0], src[1]+1)
    if direction == left:
        return (src[0]-1, src[1])
    if direction == right:
        return (src[0]+1, src[1])

def solve(input_file):
    f = open(input_file, 'r')
    pipes = [l.strip() for l in f.readlines()]
    loop_coords = set()

    def to_char(coord, pipe_map):
        return pipe_map[coord[1]][coord[0]]

    def follow_pipe(current, previous, pipe_map):
        x, y = current[0], current[1]
        current_char = pipe_map[y][x]
        next, from_dir = None, None
        if previous == up:
            if current_char == 'L':
                next = (x+1, y)
                from_dir = left
            if current_char == 'J':
                next = (x-1, y)
                from_dir = right
            if current_char == '|':
                next = (x, y+1)
                from_dir = up
        if previous == down:
            if current_char == '7':
                next = (x-1, y)
                from_dir = right
            if current_char == 'F':
                next = (x+1, y)
                from_dir = left
            if current_char == '|':
                next = (x, y-1)
                from_dir = down
        if previous == left:
            if current_char == '7':
                next = (x, y+1)
                from_dir = up
            if current_char == 'J':
                next = (x, y-1)
                from_dir = down
            if current_char == '-':
                next = (x+1, y)
                from_dir = left
        if previous == right:
            if current_char == 'L':
                next = (x, y-1)
                from_dir = down
            if current_char == 'F':
                next = (x, y+1)
                from_dir = up
            if current_char == '-':
                next = (x-1, y)
                from_dir = right
        return (next, from_dir)
    
    def part1():
        # find animal
        animal = (0, 0)
        for y in range(len(pipes)):
            for x in range(len(pipes[0])):
                if pipes[y][x] == 'S':
                    animal = (x, y)
        # determine directions from animal
        x, y = animal[0], animal[1]
        loop_coords.add((x, y))
        left_neighbor = pipes[y][x-1]
        right_neighbor = pipes[y][x+1]
        up_neighbor = pipes[y-1][x]
        down_neighbor = pipes[y][x]
        starts = []
        directions = []
        if left_neighbor in 'LF-':
            starts.append((x-1, y))
            directions.append(right)
        if right_neighbor in 'J7-':
            starts.append((x+1, y))
            directions.append(left)
        if up_neighbor in '7F|':
            starts.append((x, y-1))
            directions.append(down)
        if down_neighbor in 'LJ|':
            starts.append((x, y+1))
            directions.append(up)

        path1, prev1 = starts[0], directions[0]
        path2, prev2 = starts[1], directions[1]
        steps = 1 # took first step by finding these starts
        while True:
            loop_coords.add(path1)
            loop_coords.add(path2)
            steps += 1
            path1, prev1 = follow_pipe(path1, prev1, pipes)
            if path1 == path2:
                loop_coords.add(path1)
                loop_coords.add(path2)
                break
            path2, prev2 = follow_pipe(path2, prev2, pipes)
            if path1 == path2:
                loop_coords.add(path1)
                loop_coords.add(path2)
                break

        return steps


    def part2():
        # loop_coords populated by part 1
        tiles_enclosed = 0
        new_pipes = [list(x) for x in pipes]
        # make map with non-pipe locations blanked
        # get coordinates of first piece of pipe. because we're searching from the top-right, first will be an F.
        first_piece_of_pipe = None
        for y in range(len(pipes)):
            for x in range(len(pipes[0])):
                if (x, y) not in loop_coords:
                    new_pipes[y][x] = ' '
                elif not first_piece_of_pipe and pipes[y][x] == 'F':
                    first_piece_of_pipe = (x, y)
                if new_pipes[y][x] == 'S': # replace S from part 1
                    new_pipes[y][x] = 'J' # just reading the input file for this

        # print('first_piece_of_pipe:', first_piece_of_pipe)
        # new_pipes_flat = [''.join(x) for x in new_pipes]
        # for r in new_pipes_flat:
        #     print(r)


        # travel clockwise. that means to the left of pipe is outside, to the right is inside.
        # everything north and west of this F will be outside, but only because this F is going northeast. left of northeast is northwest.
        # if we were going west then south via this F, left would be southeast.
        # so have to be mindful of direction. if we come into an F from the right, north and west are inside.

        # now travel the loop, watch for interior blank spaces? if F, care about blanks above and to the left. if approaching from the south, those are outside. if from east, those are inside
        corner_criteria = {
            'F': {'active_previous_direction': right, 'candidate_directions': [up, left]}, # if we approached this f from the right, then up and left are to the right of the pipe, so these count as inside
            'L': {'active_previous_direction': up, 'candidate_directions': [left, down]},
            'J': {'active_previous_direction': left, 'candidate_directions': [right, down]},
            '7': {'active_previous_direction': down, 'candidate_directions': [up, right]},
        }
        current_location = first_piece_of_pipe
        prev_direction = down
        while current_location != (first_piece_of_pipe[0], first_piece_of_pipe[1] + 1): # while we're not at the tile below the start
            current_char = to_char(current_location, new_pipes)
            if current_char in corner_criteria and prev_direction == corner_criteria[current_char]['active_previous_direction']:
                # check relevant directions for blank spaces
                for direction in corner_criteria[current_char]['candidate_directions']:
                    location_to_check = coords_to(current_location, direction)
                    if to_char(location_to_check, new_pipes) == ' ':
                        # we know we came in from the right direction, so this spot should be interior
                        new_pipes[location_to_check[1]][location_to_check[0]] = 'I'
            elif current_char == '-':
                if prev_direction == right:
                    location_to_check = coords_to(current_location, up)
                    if to_char(location_to_check, new_pipes) == ' ':
                        new_pipes[location_to_check[1]][location_to_check[0]] = 'I'
                if prev_direction == left:
                    location_to_check = coords_to(current_location, down)
                    if to_char(location_to_check, new_pipes) == ' ':
                        new_pipes[location_to_check[1]][location_to_check[0]] = 'I'
            elif current_char == '|':
                if prev_direction == up:
                    location_to_check = coords_to(current_location, left)
                    if to_char(location_to_check, new_pipes) == ' ':
                        new_pipes[location_to_check[1]][location_to_check[0]] = 'I'
                if prev_direction == down:
                    location_to_check = coords_to(current_location, right)
                    if to_char(location_to_check, new_pipes) == ' ':
                        new_pipes[location_to_check[1]][location_to_check[0]] = 'I'
            current_location, prev_direction = follow_pipe(current_location, prev_direction, new_pipes)
        
        # now need to fill in interior spots
        for y in range(len(new_pipes)):
            interior = False
            for x in range(len(new_pipes[0])):
                if interior and new_pipes[y][x] == ' ':
                    new_pipes[y][x] = 'I'
                if new_pipes[y][x] == 'I':
                    interior = True
                if new_pipes[y][x] not in 'I ':
                    interior = False
        
        # print('updated again:')
        # new_pipes_flat = [''.join(x) for x in new_pipes]
        # for r in new_pipes_flat:
        #     print(r)

        # one more time, count em up
        for y in range(len(new_pipes)):
            for x in range(len(new_pipes[0])):
                if new_pipes[y][x] == 'I':
                    tiles_enclosed += 1

        return tiles_enclosed

    print('\nday 10')
    print('part 1:', part1())
    print('part 2:', part2())
