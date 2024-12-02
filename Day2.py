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

# Process the input. Each line ("report") is just a list of numbers.
reports = [[int(n) for n in s.split()] for s in input_text.split('\n')]

# Part 1: Find out how many reports are safe. "Safe" means that the numbers are either only
# increasing or only decreasing, and that the difference between two adjacent numbers is at least
# 1 and at most 3.
def derivative(r):
	return [r[n+1] - r[n] for n in range(len(r) - 1)]
def monotonic(dr):
	return all(n >= 0 for n in dr) or all(n <= 0 for n in dr)
def gentle(dr):
	return all(abs(n) >= 1 and abs(n) <= 3 for n in dr)
derivatives = [derivative(r) for r in reports]
safe_reports = [monotonic(dr) and gentle(dr) for dr in derivatives]
print(f"Part 1: The number of safe reports is {sum(safe_reports)}")

# Part 2: A report now counts as safe if removing any one number would make it safe.
def safe(r):
	dr = derivative(r)
	return monotonic(dr) and gentle(dr)

def conditionally_safe(r):
	if safe(r):
		return True
	return any(safe(r[:n] + r[n+1:]) for n in range(len(r)))

conditionally_safe_reports = [conditionally_safe(r) for r in reports]
print(f"Part 2: The number of safe reports is: {sum(conditionally_safe_reports)}")
