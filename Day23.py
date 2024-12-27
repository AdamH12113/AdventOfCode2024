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

# Process the input. It's a list of pairs of computers connected to each other in a network. I
# have a feeling this is going to be one of those graph theory puzzles where you have to know the
# right algorithm, and I'm inclined to pull in a graph library because of that, but I'll give it
# the benefit of the doubt to start with.
connections = dict()
for line in input_text.split('\n'):
	c1, c2 = line.split('-')
	if c1 in connections:
		connections[c1].add(c2)
	else:
		connections[c1] = set([c2])
	if c2 in connections:
		connections[c2].add(c1)
	else:
		connections[c2] = set([c1])

# Part 1: Find all groups of three inter-connected computers. How many contain at least one
# computer with a name that starts with 't'? All computers are ultimately connected in a larger
# network, so we just need to solve the narrow problem of finding triplets of direct connections.
# Order doesn't matter, so this isn't entirely trivial, but Python's set operations can do most
# of the work.
t_names = [comp for comp in connections if comp[0] == 't']
t_triplets = []
for tn in t_names:
	connected = list(connections[tn])
	for c1 in range(len(connected) - 1):
		for c2 in range(c1, len(connected)):
			if connected[c1] in connections[connected[c2]]:
				triplet = set([tn, connected[c1], connected[c2]])
				if triplet not in t_triplets:
					t_triplets.append(triplet)

print(f"Part 1: The number of t-triplets is: {len(t_triplets)}")

# Part 2: Find the largest group of inter-connected computers, then sort the computer names
# alphabetically and join them with commas. What is the result? In graph theory, this is called
# the clique problem, and we are looking for a single maximal clique. Googling and implementing
# a weird algorithm is kind of boring to me as a puzzle, so a library it is.
import networkx as nx

G = nx.Graph()
for c1 in connections:
	for c2 in connections[c1]:
		G.add_edge(c1, c2)

cliques = list(nx.find_cliques(G))
max_clique_size = max(len(clique) for clique in cliques)
max_clique = [clique for clique in cliques if len(clique) == max_clique_size][0]
password = ','.join(sorted(max_clique))
print(f"Part 2: The password is: {password}")


