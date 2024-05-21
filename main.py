import os
import argparse
import logging
import json
from Bio import SeqIO
from collections import Counter
import numpy as np


###############################################
# process arguments
###############################################

parser = argparse.ArgumentParser(description="BioSequence Alignment.")
parser.add_argument("m", type=float, help="Match score, positive float")
parser.add_argument("M", type=float, help="Mismatch score, negative float")
parser.add_argument("g", type=float, help="Gap penalty, negative float")
parser.add_argument(
    "--algo",
    type=str,
    default="nw",
    help="Alignment algorithm, nw (Needleman-Wunsch) or sw (Smith-Waterman).",
)
parser.add_argument(
    "--seqnum", type=int, default=100, help="Number of random sequences to generate"
)
parser.add_argument(
    "--seqlen", type=int, default=50, help="Length of each sequence to generate"
)

args = parser.parse_args()

###############################################
# calculate base frequencies
###############################################

if not os.path.exists("frequencies.json"):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    seq = os.path.join(current_dir, "sequences", "chr1.fna")
    genomes = SeqIO.parse(seq, "fasta")

    for genome in genomes:
        counter = Counter(genome.seq)
        total = sum(counter.values()) - sum(
            counter.get(base, 0) for base in "NMR"
        )  # Ignore 'NMR'
        frequencies = {
            base: count / total for base, count in counter.items() if base not in "NMR"
        }
        print(frequencies)

    with open("frequencies.json", "w") as f:
        json.dump(frequencies, f)
else:
    with open("frequencies.json", "r") as f:
        frequencies = json.load(f)


###############################################
# generate random dna sequences
###############################################

# Bases and their probabilities
bases = list(frequencies.keys())
probs = list(frequencies.values())

# Length of the sequences
N = args.seqlen
if N > 100:
    logging.warning("Sequence length is too long, may take a long time.")

# Number of sequences
num_seqs = args.seqnum
if num_seqs > 200:
    logging.warning("Number of sequences is too large, may take a long time.")

# Generate sequences
sequences = []
for _ in range(num_seqs):
    seq = np.random.choice(bases, size=N, p=probs)
    sequences.append("".join(seq))


###############################################
# get alignment score
###############################################

from NeedlemanWunsch import NeedlemanWunsch
from SmithWaterman import SmithWaterman


matrix = [[0 for _ in range(len(sequences) + 1)] for _ in range(len(sequences) + 1)]
# this may take a while
for i, seq0 in enumerate(sequences):
    for j, seq1 in enumerate(sequences):
        if i > j:
            continue
        if args.algo == "nw":
            nw = NeedlemanWunsch(seq0, seq1, m=args.m, M=args.M, g=args.g)
            score = nw.nw()
            matrix[i][j] = matrix[j][i] = score
        elif args.algo == "sw":
            sw = SmithWaterman(seq0, seq1, m=args.m, M=args.M, g=args.g)
            score = sw.sw()
            matrix[i][j] = matrix[j][i] = score
        else:
            raise ValueError(f"Invalid alignment algorithm {args.algo}.")


###############################################
# draw a histogram
###############################################

import matplotlib.pyplot as plt

# Flatten the matrix
# flat_matrix = [item for sublist in matrix_nw for item in sublist]
# Flatten the matrix and ignoring diagonal elements
flat_matrix = [
    matrix[i][j] for i in range(len(matrix)) for j in range(len(matrix[i])) if i != j
]
# print(matrix_nw)

# Plot histogram
plt.hist(flat_matrix, bins=N // 5, edgecolor="black")
plt.title("Histogram of alignment score")
plt.xlabel("Value")
plt.ylabel("Frequency")
plt.show()
