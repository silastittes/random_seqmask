import numpy as np

n_seq = 10
seq_size = 1000
nucs = ["A", "T", "G", "C"]

seq_file = open("fake.fa", "w")

for i in range(n_seq):
	#seq_size = int(np.random.uniform(40, 1000, size = 1)[0])
	seq = np.random.choice(nucs, size = seq_size, replace = True)
	print(f">{i}", file = seq_file)
	print(f"{''.join(seq)}", file = seq_file)
