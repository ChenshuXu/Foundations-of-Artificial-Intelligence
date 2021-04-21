#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, logging, collections, heapq, math, time
from collections import deque

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def main():
    """ Main program """
    arguments = len(sys.argv) - 1
    position = 1
    while arguments >= position:
        logging.debug("Parameter %i: %s" % (position, sys.argv[position]))
        position = position + 1

    # get file name from argv
    file_name = "input25.txt"
    # read file and get params
    algorithm_name, dimensions, entrance_loc, exit_loc, N, grid_locations = read_params(file_name)
    # build graph
    graph = build_graph(grid_locations)

    path = []
    if algorithm_name == "BFS":
        path = bfs(graph, entrance_loc, exit_loc)
    elif algorithm_name == "UCS":
        path = ucs(graph, entrance_loc, exit_loc)
    elif algorithm_name == "A*":
        path = a_star(graph, entrance_loc, exit_loc)
    logging.debug(path)
    # output_file("output.txt", path)
    output_file("out_" + file_name, path)

    return 0


def read_params(file_name):
    # open file
    f = open(file_name, "r")

    # get algorithm name
    algorithm_name = f.readline().strip()
    logging.info(algorithm_name)

    # get dimensions
    x, y, z = f.readline().strip().split(" ")
    x = int(x)
    y = int(y)
    z = int(z)
    dimensions = (x, y, z)
    logging.info("dimensions: " + str(dimensions))

    # get entrance location
    x, y, z = f.readline().strip().split(" ")
    x = int(x)
    y = int(y)
    z = int(z)
    entrance_loc = (x, y, z)
    logging.info("entrance: " + str(entrance_loc))

    # get exit location
    x, y, z = f.readline().strip().split(" ")
    x = int(x)
    y = int(y)
    z = int(z)
    exit_loc = (x, y, z)
    logging.info("exit location: " + str(exit_loc))

    # the number of grids in the maze where there are actions available
    N = int(f.readline().strip())
    logging.info(N)

    grid_locations = []
    for line in f:
        line_list = line.strip().split(" ")
        x, y, z = line_list[:3]
        x = int(x)
        y = int(y)
        z = int(z)
        for d in line_list[3:]:
            direction = int(d)
            grid_locations.append((x, y, z, direction))
    logging.debug(grid_locations)
    logging.debug(len(grid_locations))

    f.close()
    return algorithm_name, dimensions, entrance_loc, exit_loc, N, grid_locations


def build_graph(grid_locations):
    # key = point, value = list of its neighbors
    graph = collections.defaultdict(list)
    for loc in grid_locations:
        x, y, z = loc[:3]
        d = loc[3]
        graph[(x, y, z)].append(next_grid((x, y, z), d))

    logging.debug(graph)
    return graph


def next_grid(location, direction):
    switcher = {
        1: (1, 0, 0),
        2: (-1, 0, 0),
        3: (0, 1, 0),
        4: (0, -1, 0),
        5: (0, 0, 1),
        6: (0, 0, -1),
        7: (1, 1, 0),
        8: (1, -1, 0),
        9: (-1, 1, 0),
        10: (-1, -1, 0),
        11: (1, 0, 1),
        12: (1, 0, -1),
        13: (-1, 0, 1),
        14: (-1, 0, -1),
        15: (0, 1, 1),
        16: (0, 1, -1),
        17: (0, -1, 1),
        18: (0, -1, -1)
    }
    x, y, z = location
    s = switcher[direction]
    return x + s[0], y + s[1], z + s[2]


def output_file(file_name, path):
    f = open(file_name, "w")
    if path:
        total_cost = 0
        number_of_steps = len(path)
        str_list = []
        for node in path:
            x, y, z, cost = node
            total_cost += cost
            str_list.append("{} {} {} {}\n".format(x, y, z, cost))
        str_list[-1] = str_list[-1].strip()
        f.write(str(total_cost) + "\n")
        f.write(str(number_of_steps) + "\n")
        f.writelines(str_list)
    else:
        f.write("FAIL")
    f.close()


def bfs(graph, start, end):
    parent = {}
    visited = set()
    queue = collections.deque()
    queue.append(start)
    found = False
    while queue:
        node = queue.popleft()
        # logging.debug(node)
        if node == end:
            found = True
            break
        for nei in graph[node]:
            if nei not in visited:
                visited.add(nei)
                parent[nei] = node
                queue.append(nei)

    if not found:
        return []

    path = backtrace(parent, start, end)
    path[0] = path[0] + (0,)
    for i in range(1, len(path)):
        path[i] = path[i] + (1,)
    return path


def backtrace(parent, start, end):
    path = [end]
    while path[-1] != start:
        path.append(parent[path[-1]])
    path.reverse()
    return path


def ucs(graph, start, end):
    parent = {}
    cost_dic = collections.defaultdict(int)
    visited = set()
    queue = []
    # in order to make heapq work,
    # the first element in each tuple in the queue is the cost, then x, y, z
    heapq.heappush(queue, (0,) + start)
    cost_dic[start] = 0
    found = False
    while queue:
        cost, x, y, z = heapq.heappop(queue)
        node = (x, y, z)
        # logging.debug(node)
        if node == end:
            found = True
            break
        for nei in graph[node]:
            if nei not in visited:
                visited.add(nei)
                parent[nei] = node
                new_cost = cost + calculate_distance(node, nei)
                cost_dic[nei] = calculate_distance(node, nei)
                new_tup = (new_cost,) + nei
                heapq.heappush(queue, new_tup)

    if not found:
        return []

    path = backtrace(parent, start, end)
    path[0] = path[0] + (0,)
    for i in range(1, len(path)):
        path[i] = path[i] + (cost_dic[path[i]],)
    return path


def a_star(graph, start, end):
    parent = {}
    cost_dic = collections.defaultdict(int)
    visited = set()
    queue = []
    # in order to make heapq work,
    # the first element in each tuple in the queue is the evaluation, cost, then x, y, z
    heapq.heappush(queue, (0, 0,) + start)
    cost_dic[start] = 0
    found = False
    while queue:
        evaluation, cost, x, y, z = heapq.heappop(queue)
        node = (x, y, z)
        # logging.debug(node)
        if node == end:
            found = True
            break
        for nei in graph[node]:
            if nei not in visited:
                visited.add(nei)
                parent[nei] = node
                new_evaluation = cost + calculate_distance(node, nei) + calculate_distance(nei, end)
                new_cost = cost + calculate_distance(node, nei)
                cost_dic[nei] = calculate_distance(node, nei)
                new_tup = (new_evaluation, new_cost,) + nei
                heapq.heappush(queue, new_tup)

    if not found:
        return []

    path = backtrace(parent, start, end)
    path[0] = path[0] + (0,)
    for i in range(1, len(path)):
        path[i] = path[i] + (cost_dic[path[i]],)
    return path


def calculate_distance(start, end):
    x1, y1, z1 = start
    x2, y2, z2 = end
    dx, dy, dz = abs(x2 - x1), abs(y2 - y1), abs(z2 - z1)
    cost = 0
    while dx > 0 or dy > 0 or dz > 0:
        if dx > 0 and dy > 0:
            cost += 14
            dx -= 1
            dy -= 1
        elif dx > 0 and dz > 0:
            cost += 14
            dx -= 1
            dz -= 1
        elif dy > 0 and dz > 0:
            cost += 14
            dy -= 1
            dz -= 1
        elif dx > 0:
            cost += 10
            dx -= 1
        elif dy > 0:
            cost += 10
            dy -= 1
        elif dz > 0:
            cost += 10
            dz -= 1
    logging.debug(cost)
    return cost


if __name__ == "__main__":
    start = time.time()
    main()
    end = time.time()
    cost = end - start
    logging.info(cost)
