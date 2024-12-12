import re, sys, copy
from functools import cmp_to_key

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

# Process the input. It comes in two blocks -- one with pairs of numbers (page ordering rules)
# and one with lists of updated page numbers.
input_blocks = input_text.split('\n\n')
rules_lines = input_blocks[0].split('\n')
updates_lines = input_blocks[1].split('\n')
rules = []
for line in rules_lines:
	pages = line.split('|')
	first_page = int(pages[0])
	second_page = int(pages[1])
	rules.append((first_page, second_page))
updates = [[int(p) for p in line.split(',')] for line in updates_lines]

# Part 1: Find the updates that follow all of the page ordering rules. Sum the middle numbers of
# those updates.
def update_is_valid(update, rules):
	for first_page, second_page in rules:
		if first_page in update and second_page in update:
			if update.index(second_page) < update.index(first_page):
				return False
	return True
	
total = 0
for update in updates:
	if update_is_valid(update, rules):
		total += update[len(update) // 2]
print(f"Part 1: The sum of the middle page numbers of the valid updates is: {total}")

# Part 2: For the invalid updates, sort them using the page number rules until they're valid, then
# sum the middle numbers of the formerly-invalid updates. The puzzle description is a bit fuzzy on
# what I'm supposed to do with numbers that aren't affected by the rules, so I'm going to try a
# stable sort (the default kind in Python) and hope that's what the author wants.
def compare(page1, page2):
	for first_page, second_page in rules:
		if page1 == first_page and page2 == second_page:
			return -1
		if page2 == first_page and page1 == second_page:
			return 1
	return 0

invalid_updates = [update for update in updates if not update_is_valid(update, rules)]
total = 0
for update in invalid_updates:
	sorted_update = sorted(update, key = cmp_to_key(compare))
	total += sorted_update[len(sorted_update) // 2]
print(f"Part 2: The sum of the middle page numbers of the sorted invalid updates is: {total}")










