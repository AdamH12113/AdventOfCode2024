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

# Process the input. It's just a list of numbers carved on stones.
starting_stones = [int(n) for n in input_text.split(' ')]

# Part 1: The numbers change and split every iteration ("blink"). After 25 blinks, how many
# stones are there? The rules are:
#   1. If the stone's number is 0, it becomes 1 instead.
#   2. If the stone's number has an even number of digits, it becomes two stones, each of
#      which has half of the digits (split left/right).
#   3. If neither of the other rules apply, the stone's number is multiplied by 2024.
def update_stone(num):
	if num == 0:
		return [1]
	
	strnum = str(num)
	num_digits = len(strnum)
	if num_digits % 2 == 0:
		return [int(strnum[:num_digits//2]), int(strnum[num_digits//2:])]
	
	return [num * 2024]

def update_stones(stones):
	new_groups = []
	for stone in stones:
		new_groups.append(update_stone(stone))
	return [new_stone for new_group in new_groups for new_stone in new_group]

stones = copy.deepcopy(starting_stones)
for _ in range(25):
	stones = update_stones(stones)
print(f"Part 1: After 25 blinks, the number of stones is: {len(stones)}")

# Part 2: How many stones are there after 75 blinks? Obviously there's no brute-forcing this one;
# the list gets too big. Maybe a depth-first approach will work.
#
# Nope, didn't work. Better idea: depth-first with a result cache!
cache = {}

def count_stones(num, remaining_blinks):
	if remaining_blinks == 0:
		return 1

	cache_key = (num, remaining_blinks)
	if cache_key in cache:
		return cache[(num, remaining_blinks)]

	strnum = str(num)
	num_digits = len(strnum)
	
	if num == 0:
		result = count_stones(1, remaining_blinks - 1)
	elif num_digits % 2 == 0:
		result = (count_stones(int(strnum[:num_digits//2]), remaining_blinks - 1) +
		          count_stones(int(strnum[num_digits//2:]), remaining_blinks - 1))
	else:
		result = count_stones(2024 * num, remaining_blinks - 1)
	
	cache[cache_key] = result
	return result

total_stones = 0
for stone in starting_stones:
	total_stones += count_stones(stone, 75)
print(f"Part 2: After 75 blinks, the number of stones is: {total_stones}")
