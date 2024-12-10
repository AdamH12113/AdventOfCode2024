import re, sys, copy
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

# Process the input. Each line contains a numeric test value, a colon, and a list of numbers.
Record = namedtuple('Record', ['test', 'nums'])
records = []
lines = input_text.split('\n')
for line in lines:
	parts = line.split(':')
	test = int(parts[0])
	nums = [int(n) for n in re.findall(r'\d+', parts[1])]
	records.append(Record(test, nums))

# Part 1: Between each pair of numbers in a record, there can be an addition or multiplication
# operator. If any combination of operators makes the numbers equal to the test value, the record
# is considered value. Find the sum of the test values from the valid records. This looks like a
# boolean satisfiability problem, which would be NP-complete. But since the operators are evaluated
# left to right, multiplication will always produce a larger result than addition. So the search
# can be short-circuited whenever we get a result that's larger than the test value.
def is_valid(test_value, result, remaining_nums):
	if len(remaining_nums) == 0:
		return result == test_value
	add_result = result + remaining_nums[0]
	mul_result = result * remaining_nums[0]
	add_valid = add_result <= test_value
	mul_valid = mul_result <= test_value
	return (add_valid and is_valid(test_value, add_result, remaining_nums[1:])) or (mul_valid and is_valid(test_value, mul_result, remaining_nums[1:]))	

sum_valid_test_values = 0
for record in records:
	if is_valid(record.test, record.nums[0], record.nums[1:]):
		sum_valid_test_values += record.test
print(f"Part 1: The number of possibly-valid records is: {sum_valid_test_values}")

# Part 2: Now there can also be a concatenation operator. For once, the existing solution can handle
# this easily!
def is_valid2(test_value, result, remaining_nums):
	if len(remaining_nums) == 0:
		return result == test_value
	add_result = result + remaining_nums[0]
	mul_result = result * remaining_nums[0]
	concat_result = int(str(result) + str(remaining_nums[0]))
	add_valid = add_result <= test_value
	mul_valid = mul_result <= test_value
	concat_valid = concat_result <= test_value
	return ((add_valid and is_valid2(test_value, add_result, remaining_nums[1:])) or
	        (mul_valid and is_valid2(test_value, mul_result, remaining_nums[1:])) or
	        (concat_valid and is_valid2(test_value, concat_result, remaining_nums[1:])))

sum_valid_test_values = 0
for record in records:
	if is_valid2(record.test, record.nums[0], record.nums[1:]):
		sum_valid_test_values += record.test
print(f"Part 2: The number of possibly-valid records is: {sum_valid_test_values}")
