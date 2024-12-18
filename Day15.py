import re, sys, copy, os
from collections import namedtuple
from Vector import Vector, null

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
init_boxes = set()
start = Vector(0, 0)
for x in range(size):
	for y in range(size):
		char = grid_text[y][x]
		if char == '#':
			walls.add(Vector(x, y))
		elif char == 'O':
			init_boxes.add(Vector(x, y))
		elif char == '@':
			start = Vector(x, y)

moves = []
for char in moves_text:
	if char == '<':
		moves.append(Vector(-1, 0))
	elif char == '>':
		moves.append(Vector(1, 0))
	elif char == '^':
		moves.append(Vector(0, -1))
	elif char == 'v':
		moves.append(Vector(0, 1))

# Part 1: After the robot finishes moving, find the sum of the Y coordinates times 100 plus the sum
# of the X coordinates. Any number of boxes can be pushed at once but boxes cannot go through other
# boxes or through walls. Just for fun, let's do this recursively.
def move_box(loc, boxes, dir):
	if loc + dir in walls:
		rdir = null
	elif loc + dir in boxes:
		rdir = move_box(loc + dir, boxes, dir)
	else:
		rdir = dir

	boxes.remove(loc)
	boxes.add(loc + rdir)
	return rdir

robot = start
boxes = copy.deepcopy(init_boxes)
for move in moves:
	if robot + move in walls:
		continue
	elif robot + move not in boxes:
		robot += move
	else:
		rdir = move_box(robot + move, boxes, move)
		robot += rdir

score = sum(100*b.y + b.x for b in boxes)
print(f"Part 1: The sum of the coordinates is: {score}")

# Part 2: All boxes and walls now have double the width. It is now possible for a box pushed by the
# robot to push two other boxes at once. What's the score now?









