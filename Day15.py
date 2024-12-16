import re, sys, copy, os
from collections import namedtuple
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

# Process the input. It has two parts: a square grid describing the layout of a warehouse, and a
# list of moves that a robot will attempt to make. The moves have some newlines thrown in for
# formatting reasons, but those should be ignored. For scoring purposes, y = 0 is at the top-left
# of the grid and y = ymax is at the bottom, so I'm going to avoid using the predefined unit vectors
# here since the names would be wrong.
parts = input_text.split('\n\n')
grid_text = parts[0].split('\n')
moves_text = ''.join(parts[1].split('\n'))
size = len(grid_text)

walls = set()
boxes = set()
start = Vector(0, 0)
for x in range(size):
	for y in range(size):
		char = grid_text[y][x]
		if char == '#':
			walls.add(Vector(x, y))
		elif char == 'O':
			boxes.add(Vector(x, y))
		elif char == '@':
			start = Vector(x, y)

moves = []
for char in moves_text:
	if c == '<':
		moves.append(Vector(-1, 0))
	elif c == '>':
		moves.append(Vector(1, 0))
	elif c == '^':
		moves.append(Vector(0, -1))
	elif c == 'v':
		moves.append(Vector(0, 1))











