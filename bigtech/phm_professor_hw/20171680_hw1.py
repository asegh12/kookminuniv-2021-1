from collections import Counter

c = Counter()

# Read the file 
with open("wikisent2.txt", "r") as f:
	line = f.readline()
	while line:
		words = line.split()
		for word in words:
			c[word] += 1
		line = f.readline()

# Write to output.txt
with open("output.txt", 'w') as f:
	idx = 1
	for word, freq in c.most_common(1000):
		f.write("%d - [%s : %d]\n"%(idx, word, freq))
		idx += 1

