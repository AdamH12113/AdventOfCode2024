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
# total price. Yeesh. Not even sure where to start with this one. One of my friends said it can
# be brute-forced, so I guess I'll try that. I'll need to be at least a little efficient about it.
price_lists = [[s % 10 for s in secrets] for secrets in secret_lists]
derivative_lists = [[prices[n] - prices[n-1] for n in range(1, len(prices))] for prices in price_lists]
der_start_indices = []
for derivatives in derivative_lists:
	starts = {n: [] for n in range(-9, 9 + 1)}
	for d in range(len(derivatives)):
		starts[derivatives[d]].append(d)
	der_start_indices.append(starts)

def bananas_for_derivatives(d1, d2, d3, d4):
	total = 0
	for buyer in range(len(price_lists)):
		prices = price_lists[buyer]
		derivatives = derivative_lists[buyer]
		starts = der_start_indices[buyer][d1]
		for d in starts:
			if d < len(derivatives) - 3 and derivatives[d+1] == d2 and derivatives[d+2] == d3 and derivatives[d+3] == d4:
				total += prices[d+4]
				break
	return total

max_bananas = 0
for d1 in range(-9, 9 + 1):
	for d2 in range(-9, 9 + 1):
		#print(d1, d2)
		for d3 in range(-9, 9 + 1):
			for d4 in range(-9, 9 + 1):
				total = bananas_for_derivatives(d1, d2, d3, d4)
				if total > max_bananas:
					max_bananas = total
print(f"Part 2: The most maximum possible number of bananas is: {max_bananas}")
