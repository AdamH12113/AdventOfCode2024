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

# Process the input. It's a list of secret numbers, one per line.
init_secrets = [int(n) for n in input_text.split('\n')]

# Part 1: What is the sum of the 2000th secret number generated from each starting number? The
# generation process involves a sequence of "mixing" and "pruning" steps. These all use powers of
# two, so clearly there's some binary shenanigans going on here. Let's save that for part 2...
def mix(n, m):
	return n ^ m

def prune(n):
	return n % 16777216

def evolve_secret(s):
	n = s * 64
	s = mix(s, n)
	s = prune(s)
	
	n = s // 32
	s = mix(s, n)
	s = prune(s)
	
	n = s * 2048
	s = mix(s, n)
	s = prune(s)
	return s

secret_lists = []
for secret in init_secrets:
	secret_lists.append([secret])
	for _ in range(2000):
		secret = evolve_secret(secret)
		secret_lists[-1].append(secret)

total = sum(secrets[-1] for secrets in secret_lists)
print(f"Part 1: The sum of the 2000th secrets is: {total}")

# Part 2: The ones digits of the secret numbers are prices. We need to find a sequence of four
# price *changes* that will trigger a buy on each list of prices such that we get the maximum
# total price. Yeesh. Not even sure where to start with this one.
price_lists = [[s % 10 for s in secrets] for secrets in secret_lists]
derivatives = [[prices[n] - prices[n-1] for n in range(1, len(prices))] for prices in price_lists]
print(derivatives[0])



