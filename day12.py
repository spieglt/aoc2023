# TODO: still too slow

def place_group(row, groups, memo):
    if groups == []:
        return 1
    group = groups[0]
    cached = memo.get(f'{row} {groups}')
    if cached:
        return cached
    count = 0

    for i in range(len(row)):
        anchored = row[i] == '#'
        if len(groups) == 1 and '#' in row[i+group:]:
            if anchored:
                break
            else:
                continue
        # need the value of each group, plus a filler . or ? to separate, or we can't fit the remaining groups
        # subtract one because if we start on a group, and the row ends on a group, we need one less filler char than number of groups
        space_needed = sum(groups) + len(groups) - 1
        if i > len(row) - space_needed:
            break
        substring = row[i : i + group]
        up_against_end = i + group == len(row)
        match = True
        for j in range(group):
            if substring[j] not in '#?':
                match = False
        if match and (up_against_end or row[i + group] in "?."):
            extra = 0 if up_against_end else 1
            cutoff = (i + group + extra)
            count += place_group(row[cutoff:], groups[1:], memo)
            memo[f'{row} {groups}'] = count
        if anchored:
            break
    return count

def solve(input_file):
    f = open(input_file, 'r')
    lines = [l.strip() for l in f.readlines()]

    def part1():
        memo = {}
        sum = 0
        for line in lines:
            line = line.split(' ')
            row = line[0]
            groups = line[1]
            groups = [int(x) for x in groups.split(',')]
            count = place_group(row, groups, memo)
            sum += count
        return sum

    def part2():
        memo = {}
        sum = 0
        for i, line in enumerate(lines):
            line = line.split(' ')
            unfolded_row = ((line[0] + '?') * 5)[:-1]
            unfolded_groups = ((line[1] + ',') * 5)[:-1]
            unfolded_groups = [int(x) for x in unfolded_groups.split(',')]
            count = place_group(unfolded_row, unfolded_groups, memo)
            print(f'{i+1}: {count} found for {line[0]}, {line[1]}')
            sum += count
        return sum

    print('day 12')
    print('part 1:', part1())
    print('part 2:', part2())

if __name__ == '__main__':
    solve('inputs/12.txt')
