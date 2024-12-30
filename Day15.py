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

up = Vector(0, -1)
down = Vector(0, 1)
left = Vector(-1, 0)
right = Vector(1, 0)
moves = []
for char in moves_text:
	if char == '<':
		moves.append(left)
	elif char == '>':
		moves.append(right)
	elif char == '^':
		moves.append(up)
	elif char == 'v':
		moves.append(down)

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
# robot to push two other boxes at once. What's the score now? We're only going to store the left
# half of each box and check for the right half in code. The holidays are waning so I half-assed
# this part. :-(
def print_field(boxes):
	for y in range(size):
		for x in range(2*size):
			loc = Vector(x, y)
			if loc in dwalls:
				print('#', end='')
			elif loc in boxes:
				print('[', end='')
			elif loc + left in boxes:
				print(']', end='')
			elif loc == robot:
				print('@', end='')
			else:
				print('.', end='')
		print()

dwalls = set()
for wall in walls:
	dwalls.add(Vector(2*wall.x, wall.y))
	dwalls.add(Vector(2*wall.x + 1, wall.y))

dinit_boxes = set(Vector(2*box.x, box.y) for box in init_boxes)
dstart = Vector(2*start.x, start.y)

def dmove_possible(loc, boxes, dir):
	if dir.y == 0:
		if (dir == left and loc + dir in dwalls) or (dir == right and loc + 2*dir in dwalls):
			return False
		elif loc + 2*dir in boxes:
			return dmove_possible(loc + 2*dir, boxes, dir)
		else:
			return True
	else:
		if loc + dir in dwalls or loc + right + dir in dwalls:
			return False

		left_vert_left = loc + dir in boxes
		right_vert_left = loc + dir + left in boxes
		left_vert_right = loc + dir + right in boxes
		possible = True
		if left_vert_left:
			possible = possible and dmove_possible(loc + dir, boxes, dir)
		if right_vert_left:
			possible = possible and dmove_possible(loc + dir + left, boxes, dir)
		if left_vert_right:
			possible = possible and dmove_possible(loc + dir + right, boxes, dir)
		return possible

def dmove_box(loc, boxes, dir):
	if not dmove_possible(loc, boxes, dir):
		return null
	
	if dir.y == 0:
		next_box_loc = loc + 2*dir
		if next_box_loc in boxes:
			dmove_box(next_box_loc, boxes, dir)
	else:
		left_vert_left = loc + dir in boxes
		right_vert_left = loc + dir + left in boxes
		left_vert_right = loc + dir + right in boxes

		if left_vert_left:
			dmove_box(loc + dir, boxes, dir)
		if right_vert_left:
			dmove_box(loc + dir + left, boxes, dir)
		if left_vert_right:
			dmove_box(loc + dir + right, boxes, dir)
	
	boxes.remove(loc)
	boxes.add(loc + dir)
	return dir

robot = dstart
boxes = copy.deepcopy(dinit_boxes)
for move in moves:
	if robot + move in dwalls:
		continue
	
	rdir = null
	if move == left:
		if robot + 2*move in boxes:
			rdir = dmove_box(robot + 2*move, boxes, move)
		else:
			rdir = move
	elif move == right:
		if robot + move in boxes:
			rdir = dmove_box(robot + move, boxes, move)
		else:
			rdir = move
	else:
		left_above = robot + move in boxes
		right_above = robot + move + left in boxes
		
		if left_above:
			rdir = dmove_box(robot + move, boxes, move)
		elif right_above:
			rdir = dmove_box(robot + move + left, boxes, move)
		else:
			rdir = move
	
	robot += rdir

score = sum(100*box.y + box.x for box in boxes)
print(f"Part 2: The sum of the coordinates is: {score}")









