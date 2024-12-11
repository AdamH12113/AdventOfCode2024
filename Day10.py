import re, sys, copy
from Vector import Vector

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

# Process the input. It's a 2D grid of digits where each digit indicates the height of the position.
grid_text = list(reversed(input_text.split('\n')))
size = len(grid_text)
grid = [[int(grid_text[y][x]) for y in range(size)] for x in range(size)]
trailheads = [Vector(x, y) for x in range(size) for y in range(size) if grid[x][y] == 0]

def height(v):
	return grid[v.x][v.y]

# Part 1: Find the sum of the scores of each trailhead. The score is the number of 9-height positions
# reachable from the trailhead along a path that increases by 1 with each step. Time for a breadth-
# first search!
up = Vector(0, 1)
down = Vector(0, -1)
left = Vector(-1, 0)
right = Vector(1, 0)

def compute_score(trailhead):
	score = 0
	queue = [trailhead]
	visited = set()
	while len(queue) > 0:
		vnext = queue.pop()
		visited.add(vnext)
		if height(vnext) == 9:
			score += 1
			continue
		for neighbor in (vnext + up, vnext + down, vnext + left, vnext + right):
			if neighbor.in_range_sq(size) and not neighbor in visited and not neighbor in queue and height(neighbor) == height(vnext) + 1:
				queue.insert(0, neighbor)
	return score

total = sum(compute_score(trailhead) for trailhead in trailheads)
print(f"Part 1: The sum of the trailhead scores is: {total}")

# Part 2: Find the sum of the ratings of each trialhead. The rating is the number of *distinct* trails
# from 0 to 9 leading out of a trailhead. Given the short length and one-way nature of the trails, I
# don't think a depth-first search would be computationally infeasible.
def compute_rating(position):
	if height(position) == 9:
		return 1
	
	neighbors = (position + up, position + down, position + left, position + right)
	neighbor_scores = 0
	for neighbor in neighbors:
		if neighbor.in_range_sq(size) and height(neighbor) == height(position) + 1:
			neighbor_scores += compute_rating(neighbor)
	return neighbor_scores

total = sum(compute_rating(trailhead) for trailhead in trailheads)
print(f"Part 2: The sum of the trailhead ratings is: {total}")


