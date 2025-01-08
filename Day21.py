import re, sys, copy, os
from collections import namedtuple
from Vector import Vector, up, down, left, right, null

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

# Process the input. It's a list of numeric keypad codes with an 'A' on the end, one per line. The
# puzzle description also includes layouts for a numeric keypad and a directional keypad, which
# we might as well define here. The button locations are given as distances from the bottom-left
# of the keypad.
codes = input_text.split('\n')

numeric = {
	'0': right,
	'1': up,
	'2': up + right,
	'3': up + 2*right,
	'4': 2*up,
	'5': 2*up + right,
	'6': 2*up + 2*right,
	'7': 3*up,
	'8': 3*up + right,
	'9': 3*up + 2*right,
	'A': 2*right
}
directional = {
	'<': null,
	'v': right,
	'^': right + up,
	'>': 2*right,
	'A': 2*right + up
}

# Part 1: A robot at the numeric keypad is controlled by a robot at a directional keypad, which is
# controlled by another robot with a directional keypad, which is controlled by me using a third
# directional keypad. Find the smallest number of keypresses needed for me to enter each code on
# the numeric keypad and multiply that by the numeric part of the code. Each robot starts out
# pointing at the A button on its keypad. There are gaps in the keypad layout (lower left on the
# numeric pad and upper left on the directional pad) that the robot is not allowed to point at.
#
# I think a key feature of this puzzle is that to push a button on the numeric keypad, all of the
# directional keypads need to be pressing A at the same time. Likewise, to press a button on the
# first directional keypad, the higher keypads all need to press A at the same time. So it's
# recursive, like the Towers of Hanoi. (Maybe part 2 will make me do ten levels of indirection!)
def dx_to_directions(dx):
	char = '<' if dx < 0 else '>'
	return abs(dx) * char
def dy_to_directions(dy):
	char = 'v' if dy < 0 else '^'
	return abs(dy) * char

def numeric_press_to_directions(start, end):
	cs = numeric[start]
	ce = numeric[end]
	dxd = dx_to_directions(ce.x - cs.x)
	dyd = dy_to_directions(ce.y - cs.y)
	
	if cs.x == 0 and ce.y == 0:
		return dxd + dyd + 'A'
	elif cs.y == 0 and ce.x == 0:
		return dyd + dxd + 'A'
	elif ce.x > cs.x:
		return dyd + dxd + 'A'
	else:
		return dxd + dyd + 'A'

def directional_press_to_directions(start, end):
	cs = directional[start]
	ce = directional[end]
	dxd = dx_to_directions(ce.x - cs.x)
	dyd = dy_to_directions(ce.y - cs.y)

	if cs.x == 0 and ce.y == 1:
		return dxd + dyd + 'A'
	elif cs.y == 1 and ce.x == 0:
		return dyd + dxd + 'A'
	elif ce.x > cs.x:
		return dyd + dxd + 'A'
	else:
		return dxd + dyd + 'A'

def code_to_directions(code):
	seq = 'A' + code
	dirs = []
	for c1 in range(len(seq) - 1):
		dirs.append(numeric_press_to_directions(seq[c1], seq[c1 + 1]))
	return ''.join(dirs)

def dirs_to_directions(dirs):
	seq = 'A' + dirs
	new_dirs = []
	for c1 in range(len(seq) - 1):
		new_dirs.append(directional_press_to_directions(seq[c1], seq[c1 + 1]))
	return ''.join(new_dirs)

score = 0
for code in codes:
	m1 = code_to_directions(code)
	m2 = dirs_to_directions(m1)
	m3 = dirs_to_directions(m2)
	score += int(code[:3]) * len(m3)
print(f"Part 1: The total complexity is: {score}")

# Part 2: Now there are 25 robot-controlled directional keypads between me and the numeric keypad.
# (Called it!) What is the sum of the complexities now? Clearly we need a more efficient algorithm.

score = 0
for code in codes:
	m = code_to_directions(code)
	for _ in range(25):
		print(_)
		m = dirs_to_directions(m)
	score += int(code[:3]) * len(m)
	print(score)
print(f"Part 2: The total complexity is: {score}")


# 118392478819140



