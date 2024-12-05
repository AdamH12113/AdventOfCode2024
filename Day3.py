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

# Despite the presence of newline characters, the input is one big string.

# Part 1: Find all the valid multiplication instructions in the input, do the multiplications,
# and sum the products. A valid multiplication instruction has the form: mul(NNN,MMM) where NNN
# and MMM are 1-3 digit numbers. No whitespace is allowed. This can be easily solved with a
# regular expression.
valid_mul_re = r'mul\(\d\d?\d?,\d\d?\d?\)'
valid_muls = re.findall(valid_mul_re, input_text)
total = 0
for mul in valid_muls:
	nums = mul[4:-1].split(',')
	total += int(nums[0]) * int(nums[1])
print(f"Part 1: The sum of the products of the valid multiplication instructions is: {total}.")

# Part 2: Now include the effects of do() and don't() instructions, which enable and disable mul()
# instructions, respectively. Instructions are enabled at the start.
valid_instructions_re = r"mul\(\d\d?\d?,\d\d?\d?\)|do\(\)|don't\(\)"
valid_instructions = re.findall(valid_instructions_re, input_text)
total = 0
enabled = True
for instruction in valid_instructions:
	if instruction == "do()":
		enabled = True
	elif instruction == "don't()":
		enabled = False
	elif enabled:
		nums = instruction[4:-1].split(',')
		total += int(nums[0]) * int(nums[1])

print(f"Part 2: The sum of the products of the enabled multiplication instructions is: {total}.")
