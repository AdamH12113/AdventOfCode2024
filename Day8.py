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

# Process the input. It's a 2D grid showing the locations of antennas. Each type of antenna
# ("frequency") is indicated by a different letter or number.
grid = list(reversed(input_text.split('\n')))
size = len(grid)
antennas = dict()
for x in range(size):
	for y in range(size):
		char = grid[y][x]
		if char != '.':
			if char in antennas:
				antennas[char].append(Vector(x, y))
			else:
				antennas[char] = [Vector(x, y)]

# Part 1: The antennas form antinodes at points on a line between two antennas of the same
# frequency that are twice as far from one antenna as the other. How many unique locations
# contain antinodes? Each pair of antennas creates (ideally) two antinodes, so we can enumerate
# them pretty easily as long as we make sure not to count antinodes outside the grid.
antinodes = set()
for frequency in antennas:
	txs = antennas[frequency]
	for a1 in range(len(txs)):
		for a2 in range(len(txs)):
			if a1 == a2:
				continue
			antinode_loc = txs[a1] + (txs[a1] - txs[a2])
			if antinode_loc.in_range_sq(size):
				antinodes.add(antinode_loc)
print(f"Part 1: The number of unique antinodes is: {len(antinodes)}")

# Part 2: Now there are antinodes at every coordinate in line with two antennas of the same
# frequency. It looks like the input made this easy on me and separated the antennas by irreducible
# rational coordinate distances, so I don't think I have to worry about antinodes between antennas.
# Each non-solitary antenna does have an antinode on it, though.
antinodes = set()
for frequency in antennas:
	txs = antennas[frequency]
	for a1 in range(len(txs)):
		for a2 in range(len(txs)):
			if a1 == a2:
				continue
			separation = txs[a1] - txs[a2]
			for step in range(size):
				loc = txs[a1] + step*separation
				if loc.in_range_sq(size):
					antinodes.add(loc)
print(f"Part 2: The number of unique antinodes is: {len(antinodes)}")
