import os
from Bio import SeqIO
from collections import Counter
import numpy as np



###############################################
# calculate base frequencies
###############################################

current_dir = os.path.dirname(os.path.abspath(__file__))
print(current_dir)
seq = os.path.join(current_dir, "sequences", "chr1.fna")
genomes = SeqIO.parse(seq, "fasta")

for genome in genomes:
    counter = Counter(genome.seq)
    total = sum(counter.values()) - counter.get('N', 0)  # Ignore 'N'
    frequencies = {base: count/total for base, count in counter.items() if base not in 'NMR'}
    print(frequencies)


###############################################
# generate random dna sequences 
###############################################

# Bases and their probabilities
bases = list(frequencies.keys())
probs = list(frequencies.values())

# Length of the sequences
N = 50

# Number of sequences
num_seqs = 1000

# Generate sequences
sequences = []
for _ in range(num_seqs):
    seq = np.random.choice(bases, size=N, p=probs)
    sequences.append(''.join(seq))
    

###############################################
# get alignment score
###############################################

from NeedlemanWunsch import NeedlemanWunsch
from SmithWaterman import SmithWaterman



### Test with small sequences
sequences = sequences[:100] ###

matrix_nw = [[0 for _ in range(len(sequences)+1)] for _ in range(len(sequences)+1)]
matrix_sw = [[0 for _ in range(len(sequences)+1)] for _ in range(len(sequences)+1)]
# this may take a while
for i, seq0 in enumerate(sequences):
    for j, seq1 in enumerate(sequences):
        if i > j:
            continue
        nw = NeedlemanWunsch(seq0, seq1, m=1, M=-1, g=-1)
        sw = SmithWaterman(seq0, seq1, m=1, M=-1, g=-1)
        score_nw = nw.nw()
        score_sw = sw.sw()
        matrix_nw[i][j] = matrix_nw[j][i] = score_nw
        matrix_sw[i][j] = matrix_sw[j][i] = score_sw


###############################################
# draw a histogram
###############################################

import matplotlib.pyplot as plt

# Flatten the matrix
# flat_matrix = [item for sublist in matrix_nw for item in sublist]
# Flatten the matrix and ignoring diagonal elements
flat_matrix = [matrix_nw[i][j] for i in range(len(matrix_nw)) for j in range(len(matrix_nw[i])) if i != j]
# print(matrix_nw)

# Plot histogram
plt.hist(flat_matrix, bins=20, edgecolor='black')
plt.title('Histogram of matrix elements')
plt.xlabel('Value')
plt.ylabel('Frequency')
plt.show()
