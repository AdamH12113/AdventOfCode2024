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
	'L': null,
	'D': right,
	'U': right + up,
	'R': 2*right,
	'A': 2*right + up
}

# Part 1: A robot at the numeric keypad is controlled by a robot at a directional keypad, which is
# controlled by another robot with a directional keypad, which is controlled by me using a third
# directional keypad. Find the smallest number of keypresses needed for me to enter each code on
# the numeric keypad and multiply that by the numeric part of the code. Each robot starts out
# pointing at the A button on its keypad. There are gaps in the keypad layout (lower left on the
# numeric pad and upper left on the directional pad) that the robot is not allowed to point at.










