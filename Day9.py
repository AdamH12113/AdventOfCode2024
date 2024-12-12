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

# Process the input. It's a single line with a digit string describing a disk layout. Each digit
# gives the number of disk blocks used by files (even digits) or empty space (odd digits). The
# position of the file blocks gives their file ID number. The last digit is a file.
file_sizes = [int(n) for n in input_text[0::2]]
empty_sizes = [int(n) for n in input_text[1::2]]
data_size = sum(file_sizes)
disk_size = data_size + sum(empty_sizes)
num_files = len(file_sizes)

# Part 1: Compact the disk by moving file blocks from the end of the disk to the earliest possible
# empty blocks. Compute the checksum for the disk, which is the sum of the products of the block
# positions and their file ID numbers.
left_file = 0
left_on_data = True
left_blocks_written = 0
right_file = num_files - 1
right_blocks_read = 0

checksum = 0
b = 0
while b < data_size:
	if left_on_data:
		file_size = file_sizes[left_file]
		remaining_data = data_size - b
		read_size = file_size if file_size < remaining_data else remaining_data
		for _ in range(read_size):
			checksum += b * left_file
			b += 1
		left_on_data = False
	else:
		empty_size = empty_sizes[left_file]
		file_size = file_sizes[right_file]
		moved = 0
		while left_blocks_written < empty_size and right_blocks_read < file_size:
			checksum += b * right_file
			left_blocks_written += 1
			right_blocks_read += 1
			b += 1
		if left_blocks_written == empty_size:
			left_file += 1
			left_blocks_written = 0
			left_on_data = True
		if right_blocks_read == file_size:
			right_file -= 1
			right_blocks_read = 0
print(f"Part 1: The filesystem checksum is: {checksum}")

# Part 2: Now attempt to move whole files in descending order by file ID and recompute the checksum.
# I think I'm going to just simulate the whole disk. There's probably a more efficient way but I used
# to like watching disks defragment so this way is more fun.
Region = namedtuple('Region', ['addr', 'size'])

files = {}
empties = []
disk = []
b = 0

for f in range(num_files - 1):
	files[f] = Region(b, file_sizes[f])
	for _ in range(file_sizes[f]):
		disk.append(f)
		b += 1
	
	if empty_sizes[f] > 0:
		empties.append(Region(b, empty_sizes[f]))
		for _ in range(empty_sizes[f]):
			disk.append(-1)
			b += 1

files[num_files - 1] = Region(b, file_sizes[num_files - 1])
for _ in range(file_sizes[num_files - 1]):
	disk.append(num_files - 1)

# Now we can defragment!
for f in range(num_files - 1, 0, -1):
	faddr = files[f].addr
	fsize = files[f].size
	
	e = 0
	while e < len(empties):
		eaddr = empties[e].addr
		esize = empties[e].size
		
		if esize >= fsize and eaddr < faddr:
			for b in range(fsize):
				disk[eaddr + b] = disk[faddr + b]
				disk[faddr + b] = -1
			files[f] = Region(eaddr, fsize)
			if esize - fsize == 0:
				del empties[e]
			else:
				empties[e] = Region(eaddr + fsize, esize - fsize)
			break
		else:
			e += 1

# And... SCORE!
checksum = 0
for b in range(disk_size):
	if disk[b] >= 0:
		checksum += b * disk[b]
print(f"Part 2: The filesystem checksum is: {checksum}")
