import re, sys, copy, os
from collections import namedtuple

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

# Process the input. It's a series of 2D grids that are schematics for the structures of locks and
# keys. Locks have the top row filled with '#' and keys have the bottom row filled. These are
# effectively a list of five pin heights given in a complicated way.
num_pins = 5
max_height = 7
locks = []
keys = []
schematics = input_text.split('\n\n')

for schematic in schematics:
	grid = schematic.split('\n')
	heights = [len([grid[h][p] for h in range(max_height) if grid[h][p] == '#']) - 1 for p in range(num_pins)]
	if grid[0][0] == '#':
		locks.append(heights)
	else:
		keys.append(heights)
		
# Part 1: Try every key with every lock. How many unique lock/key pairs fit together without
# overlapping any column?
total = 0
for lock in locks:
	for key in keys:
		sums = [lock[p] + key[p] for p in range(num_pins)]
		if not any(sums[p] > 5 for p in range(num_pins)):
			total += 1
print(f"Part 1: The number of matching lock/key combinations is: {total}")





