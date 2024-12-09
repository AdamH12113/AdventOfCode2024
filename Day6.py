import re, sys, copy

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
# along with empty space (.).
grid = [line for line in input_text.split('\n')]
size = len(grid)
obstacle_coords = []
guard_coords = (-1, -1)
for x in range(size):
	for y in range(size):
		if grid[y][x] == '#':
			obstacle_coords.append((x, y))
		elif grid[y][x] == '^':
			guard_coords = (x, y)

# Part 1: How many distinct positions will the guard visit before leaving the area?
