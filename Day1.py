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

# Process the input. The input is two lists of numbers organized into two columns, so each line
# contains one number from each list.
number_pairs = [[int(n) for n in s.split()] for s in input_text.split('\n')]
left_list = [pair[0] for pair in number_pairs]
right_list = [pair[1] for pair in number_pairs]

# Part 1: Sort the lists from smallest to largest, then compute the pairwise differences between
# the elements of the two lists.
left_list.sort()
right_list.sort()
diffs = [abs(p[0] - p[1]) for p in zip(left_list, right_list)]
print(f"Part 1: The sum of the differences is: {sum(diffs)}")

# Part 2: Multiply each number in the left list by the total number of times that number appears
# in the right list.
total = 0
for nl in left_list:
	appearances = sum((1 if nr == nl else 0) for nr in right_list)
	total += nl * appearances
print(f"Part 2: The similarity score is: {total}")
