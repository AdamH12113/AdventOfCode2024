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

# Process the input. It's a rectangular grid of letters.
grid = input_text.split('\n')
mx = len(grid[0])
my = len(grid)

# Part 1: Count the number of instances of XMAS in the grid. Instances can be vertical, horizontal,
# diagonal, and backwards, and can overlap other instances.
def is_xmas(grid, x, y, dx, dy):
	return (grid[y][x] == 'X' and
	       grid[y+dy][x+dx] == 'M' and
		   grid[y+2*dy][x+2*dx] == 'A' and
		   grid[y+3*dy][x+3*dx] == 'S')

total = 0
for x in range(mx):
	for y in range(my):
		if x >= 3:
			total += is_xmas(grid, x, y, -1, 0)
		if x <= mx - 4:
			total += is_xmas(grid, x, y, 1, 0)
		if y >= 3:
			total += is_xmas(grid, x, y, 0, -1)
		if y <= my - 4:
			total += is_xmas(grid, x, y, 0, 1)
		if x >= 3 and y >= 3:
			total += is_xmas(grid, x, y, -1, -1)
		if x <= mx - 4 and y <= my - 4:
			total += is_xmas(grid, x, y, 1, 1)
		if x >= 3 and y <= my - 4:
			total += is_xmas(grid, x, y, -1, 1)
		if x <= mx - 4 and y >= 3:
			total += is_xmas(grid, x, y, 1, -1)
print(f"Part 1: The total number of XMASes is: {total}")

# Part 2: Count the number of pairs of MASes overlapping in an X shape ("X-MAS"). Each MAS can go
# in either direction.
def is_x_mas(grid, x, y):
	return (grid[y][x] == 'A' and
	        ((grid[y+1][x+1] == 'M' and grid[y-1][x-1] == 'S') or (grid[y-1][x-1] == 'M' and grid[y+1][x+1] == 'S')) and
	        ((grid[y+1][x-1] == 'M' and grid[y-1][x+1] == 'S') or (grid[y-1][x+1] == 'M' and grid[y+1][x-1] == 'S')))

total = 0
for x in range(mx):
	for y in range(my):
		if x > 0 and x < mx - 1 and y > 0 and y < my - 1:
			total += is_x_mas(grid, x, y)
print(f"Part 2: The total number of X-MASes is: {total}")
