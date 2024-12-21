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

# Process the input. It's a list of towel patterns (basically letter sequences) and a list of
# desired designs, which are letter sequences that can be constructed from the towel patterns.
parts = input_text.split('\n\n')
towels = set(parts[0].split(', '))
designs = parts[1].split('\n')

# Part 1: How many designs are possible with the available towel patterns? I think a depth-first
# search should work here. Let's add caching to keep it from taking forever.
cache = {}

def design_possible(design):
	if len(design) == 0:
		return True
	
	if design in cache:
		return cache[design]

	for towel in towels:
		if design[:len(towel)] == towel:
			if design_possible(design[len(towel):]):
				cache[design] = True
				return True
	
	cache[design] = False
	return False

num_possible = sum(design_possible(design) for design in designs)
print(f"Part 1: The number of possible designs is: {num_possible}")

# Part 2: How many different ways can each design be made? We can use the same basic approach, but
# keeping track of counts instead of booleans.
cache = {}

def num_possible_assemblies(design):
	if len(design) == 0:
		return 1
	
	if design in cache:
		return cache[design]
	
	total = 0
	for towel in towels:
		if design[:len(towel)] == towel:
			total += num_possible_assemblies(design[len(towel):])
	
	cache[design] = total
	return total

num_possible = sum(num_possible_assemblies(design) for design in designs)
print(f"Part 2: The number of possible ways to create the designs is: {num_possible}")
