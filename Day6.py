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

# Process the input. It's a 2D grid containing a map of a facility with a guard (^) and obstacles (#)
# along with empty space (.). To make working with vectors easier, the start of the input will be the
# maximum y coordinate.
grid = [line for line in input_text.split('\n')]
size = len(grid)
obstacles = set()
guard_coords = Vector(-1, -1)
for x in range(size):
	for y in range(size):
		if grid[y][x] == '#':
			obstacles.add(Vector(x, (size - 1) - y))
		elif grid[y][x] == '^':
			guard_coords = Vector(x, (size - 1) - y)

# Part 1: How many distinct positions will the guard visit before leaving the area? Let's do this
# the naive way so we can see how part 2 will pull the rug out from under us.
position = guard_coords
direction = Vector(0, 1)
visited = set()
while position.in_range(0, size - 1, 0, size - 1):
	visited.add(position)
	while position + direction in obstacles:
		direction = direction.rotate_cw()
	position += direction
print(f"Part 1: The guard will visit {len(visited)} distinct positions.")

# Part 2: In how many places (aside from the starting location) could a new obstacle be added that
# would cause the guard to move in a loop? Only obstacles added to a coordinate that was visited in
# part 1 can make a difference, so we can cut down on the number of locations a bit. It's still slow,
# but oh well.
def guard_goes_in_loop(obstacles):
	position = guard_coords
	direction = Vector(0, 1)
	visited_corners = set()
	while True:
		while position + direction not in obstacles:
			position += direction
			if not position.in_range(0, size - 1, 0, size - 1):
				return False
		if (position, direction) in visited_corners:
			return True
		else:
			visited_corners.add((position, direction))
			direction = direction.rotate_cw()

obstruction_locs = 0
for x in range(size):
	print(x)
	for y in range(size):
		new_obstacle = Vector(x, y)
		if new_obstacle not in obstacles and new_obstacle != guard_coords and new_obstacle in visited:
			modified_obstacles = obstacles | set([new_obstacle])
			if guard_goes_in_loop(modified_obstacles):
				obstruction_locs += 1
print(f"Part 2: The number of possible obstruction locations is {obstruction_locs}.")
