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

# Process the input. It's yet another 2D grid describing the layout of a racetrack. This looks
# like a maze, but there's only one path from start to end.
grid = list(reversed(input_text.split('\n')))
size = len(grid)
walls = set()
for x in range(size):
	for y in range(size):
		if grid[y][x] == 'S':
			start = Vector(x, y)
		elif grid[y][x] == 'E':
			end = Vector(x, y)
		elif grid[y][x] == '#':
			walls.add(Vector(x, y))

# Part 1: While traversing the track, we're allowed to cheat once by "clipping" through a single
# wall segment. How many such cheats would save at least 100 steps? To compute this, we can find
# the distance from the end node to each other node, then look for walls separating distances that
# would improve the best distance. Time for a pseudo-BFS!
costs = {end: 0}
cur_node = end
cost = 0
while cur_node != start:
	cost += 1
	for dir in up, left, down, right:
		candidate = cur_node + dir
		if candidate.in_range_sq(size) and candidate not in walls and candidate not in costs:
			costs[candidate] = cost
			cur_node = candidate
			break

cheats = {}
for src in costs:
	for cheat in 2*up, 2*down, 2*left, 2*right:
		dest = src + cheat
		if dest in costs:
			gain = costs[dest] - costs[src] - 2
			if gain > 2:
				if gain not in cheats:
					cheats[gain] = 1
				else:
					cheats[gain] += 1

num_cheats = sum(cheats[cheat] for cheat in cheats if cheat >= 100)
print(f"Part 1: The number of cheats that save at least 100 steps is: {num_cheats}")

# Part 2: Cheats can now last up to 20 steps. Cheats with the same start and end location are
# identical even if they pass through different wall segments. Now how many cheats are there that
# save at least 100 steps? This is basically the same at part 1 but we need to consider the distance
# between each pair of nodes within 20 steps of each other.
possible_jumps = set()
for x in range(-20, 20 + 1):
	for y in range(-20, 20 + 1):
		if abs(x) + abs(y) <= 20:
			possible_jumps.add(Vector(x, y))

cheats = {}
for src in costs:
	for jump in possible_jumps:
		dest = src + jump
		if dest in costs:
			gain = costs[dest] - costs[src] - abs(jump)
			if gain > abs(jump):
				if gain not in cheats:
					cheats[gain] = 1
				else:
					cheats[gain] += 1

num_cheats = sum(cheats[cheat] for cheat in cheats if cheat >= 100)
print(f"Part 2: The number of cheats that save at least 100 steps is: {num_cheats}")
