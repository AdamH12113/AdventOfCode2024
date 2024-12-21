import re, sys, copy, os
from collections import namedtuple
from Vector import Vector, up, down, left, right

# Read the input
try:
	day_num = int(re.findall(r'\d+', __file__)[-1])
	filename_base = 'Example' if '--example' in sys.argv else 'Input'
	filename = filename_base + str(day_num) + '.txt'
	with open(filename, 'rt') as f:
		input_text = f.read()[:-1]
except Exception as e:
	print(f"Error reading input: [{e.__class__.__name__}] {e}")
	exit()

# Process the input. It's a square 2D grid that describes a maze for reindeer. The maze contains a
# start location ('S') and an end location ('E').
grid = list(reversed(input_text.split('\n')))
size = len(grid)
start = Vector(1, 1)
end = Vector(size - 2, size - 2)
walls = set(Vector(x, y) for x in range(size) for y in range(size) if grid[y][x] == '#')

# Part 1: What is the lowest-scoring path through the maze? The score is the number of forward
# steps plus 1000 times the number of 90-degree turns. A standard BFS should work here. Since we
# need to keep track of direction, let's only try turning if there aren't walls to the side to
# avoid blowing up the queue.
ReindeerState = namedtuple('ReindeerState', ['coords', 'dir', 'cost'])
CostNode = namedtuple('CostNode', ['coords', 'dir'])
costs = {}
queue = [ReindeerState(start, right, 0)]

while len(queue) > 0:
	loc, dir, cost = queue.pop()
	
	if loc + dir not in walls:
		cost_node = CostNode(loc + dir, dir)
		if cost_node not in costs or costs[cost_node] > cost + 1:
			costs[cost_node] = cost + 1
			queue.insert(0, ReindeerState(loc + dir, dir, cost + 1))
	
	ldir = dir.rotate_ccw()
	if loc + ldir not in walls:
		cost_node = CostNode(loc, ldir)
		if cost_node not in costs or costs[cost_node] > cost + 1000:
			costs[cost_node] = cost + 1000
			queue.insert(0, ReindeerState(loc, ldir, cost + 1000))
	
	rdir = dir.rotate_cw()
	if loc + rdir not in walls:
		cost_node = CostNode(loc, rdir)
		if cost_node not in costs or costs[cost_node] > cost + 1000:
			costs[cost_node] = cost + 1000
			queue.insert(0, ReindeerState(loc, rdir, cost + 1000))

min_cost = min(costs[cost] for cost in costs if cost.coords == end)
print(f"Part 1: The minimum cost to reach the exit is: {min_cost}")

# Part 2: How many tiles are part of at least one of the best paths through the maze? I think we can
# do this by following the costs from highest to lowest. If the cost of getting to an adjacent node
# is the lowest cost of the current node minus the mimimum movement needed to get to that node, then
# the adjacent node should be on the path.



