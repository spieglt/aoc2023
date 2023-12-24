import copy
import heapq
import math

u = 0
d = 1
l = 2
r = 3

class Vertex:
    def __init__(self, x, y, cost, direction, streak):
        self.x = x
        self.y = y
        self.cost = cost # heat loss for this tile
        self.direction = direction # direction that was travelled to get to here
        self.streak = streak # number of times in a row we've travelled this direction
    dist = math.inf # length of shortest path found to this tile
    prev = None # (x, y, direction, streak) of previous tile in shortest path
    def __lt__(self, other):
        return self.dist < other.dist

def build_graph(str_graph):

    streaks = list(range(11))
    directions = [copy.deepcopy(streaks) for _ in range(4)]
    x = [copy.deepcopy(directions) for _ in range(len(str_graph[0]))]
    graph = [copy.deepcopy(x) for _ in range(len(str_graph))]

    for y in range(len(str_graph)):
        for x in range(len(str_graph[0])):
            for d in range(4):
                for s in range(11):
                    vertex = Vertex(x, y, int(str_graph[y][x]), d, s)
                    graph[y][x][d][s] = vertex

    return graph

def get_neighbors(vertex, min_streak, max_streak, graph):
    neighbors = []
    neighbors_xy = [None, None, None, None] # up, down, left, right
    over_min = min_streak <= vertex.streak
    under_max = vertex.streak < max_streak

    turns = {
        u: [l, r],
        d: [r, l],
        l: [d, u],
        r: [u, d],
    }
    
    if vertex.y != 0:
        neighbors_xy[u] = (vertex.x, vertex.y - 1)
    if vertex.y != len(graph) - 1:
        neighbors_xy[d] = (vertex.x, vertex.y + 1)
    if vertex.x != 0:
        neighbors_xy[l] = (vertex.x - 1, vertex.y)
    if vertex.x != len(graph[0]) - 1:
        neighbors_xy[r] = (vertex.x + 1, vertex.y)

    if under_max:
        straight_neighbor_xy = neighbors_xy[vertex.direction]
        if straight_neighbor_xy:
            straight_neighbor = graph[straight_neighbor_xy[1]][straight_neighbor_xy[0]][vertex.direction][vertex.streak + 1]
            neighbors.append(straight_neighbor)

    if over_min:
        left_neighbor_direction = turns[vertex.direction][0]
        left_neighbor_xy = neighbors_xy[left_neighbor_direction]
        if left_neighbor_xy:
            left_neighbor = graph[left_neighbor_xy[1]][left_neighbor_xy[0]][left_neighbor_direction][1]
            neighbors.append(left_neighbor)
        right_neighbor_direction = turns[vertex.direction][1]
        right_neighbor_xy = neighbors_xy[right_neighbor_direction]
        if right_neighbor_xy:
            right_neighbor = graph[right_neighbor_xy[1]][right_neighbor_xy[0]][right_neighbor_direction][1]
            neighbors.append(right_neighbor)

    return neighbors

def dijkstra(graph, min_streak, max_streak, destination):
    source = graph[0][0][1][0] # set initial direction to down so it doesn't keep us from backtracking. streak == 0.
    source.dist = 0
    queue = [source]
    while queue != []:
        shortest = heapq.heappop(queue)
        if shortest.x == destination[0] and shortest.y == destination[1]:
            return shortest
        for neighbor in get_neighbors(shortest, min_streak, max_streak, graph):
            this_dist = shortest.dist + neighbor.cost
            if this_dist < neighbor.dist:
                neighbor.dist = this_dist
                neighbor.prev = (shortest.x, shortest.y, shortest.direction, shortest.streak)
                heapq.heappush(queue, neighbor)


def retrace(target, graph, graph_copy):
    previous = target
    total_cost = 0
    while previous.prev:
        graph_copy[previous.y][previous.x] = '\x1b[1;31;40m' + '#' + '\x1b[0m'
        total_cost += previous.cost
        (x, y, d, s) = previous.prev
        previous = graph[y][x][d][s]
    return total_cost


def solve(input_file):
    f = open(input_file, 'r')
    lines = [list(l.strip()) for l in f.readlines()]

    # lines = '''
    #     2413432311323
    #     3215453535623
    #     3255245654254
    #     3446585845452
    #     4546657867536
    #     1438598798454
    #     4457876987766
    #     3637877979653
    #     4654967986887
    #     4564679986453
    #     1224686865563
    #     2546548887735
    #     4322674655533'''.split('\n')
    # lines = [list(l.strip()) for l in lines if l]

    def find_shortest_path(min_streak, max_streak):
        graph = build_graph(lines)
        destination = (len(lines[0]) - 1, len(lines) - 1)
        target = dijkstra(graph, min_streak, max_streak, destination)
        graph_copy = copy.deepcopy(lines)
        total_cost = retrace(target, graph, graph_copy)
        for line in graph_copy:
            print(''.join(line))
        return target.dist

    def part1():
        return find_shortest_path(0, 3)

    def part2():
        return find_shortest_path(4, 10)

    print('day 17')
    print('part 1:', part1())
    print('part 2:', part2())

if __name__ == '__main__':
    solve('inputs/17.txt')
