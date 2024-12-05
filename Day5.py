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



