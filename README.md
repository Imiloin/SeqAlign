# SeqAlign

SJTU BIO2502 Mini-project 2: Dynamic programming

## Task

1. **Needleman-Wunsch algorithm (global alignment)**

   - Generate 1000 random DNA sequences with the same A/C/G/T proportions as the chromosome 1, human reference genome (Note: You need to download the chr1 of the human genome, and count them).
   - Use your pre-built library to parse the DNA sequences stored in a FASTA file, and output the optimal pairwise global alignment score, and store them in a square matrix.
   - Draw a histogram of the alignment scores using the functions in Matplotlib package. Does it look like the bell-shape? That is, is it similar to Gaussian (normal) distribution?
   - You need to repeat the process with different length setting: $N=50, 100, 200, 500$

   

2. **Smith-Waterman algorithm (local alignment)**

   - Write Smith-Waterman algorithm in Python using the fashion of object-oriented programming.
   - Run local alignment on the random sequences generated in the exercise above. 

## Prepare Data

首先需要下载数据，在项目目录下，
```bash
conda activate <your-env>
conda install -c conda-forge ncbi-datasets-cli
datasets download genome taxon human --reference --chromosomes 1 --include genome --filename human_chr1_seq.zip
unzip -j human_chr1_seq.zip ncbi_dataset/data/GCF_000001405.40/chr1.fna -d sequences
```
生成的随机序列将使用该基因组中 A/C/G/T 的比例。如果没有下载，将启用 `frequencies.json` 中指定的频率值。


## Install Dependencies

```bash
# conda activate <your-env>
pip install -r requirements.txt
```


## Usage

`main.py` 是一个用于生物序列对齐的脚本。它接受以下命令行参数：

- `m`：匹配得分，应为正浮点数。必选参数。

- `M`：不匹配得分，应为负浮点数。必选参数。

- `g`：空位罚分，应为负浮点数。必选参数。

- `--algo`：对齐算法，可以是 `nw`（Needleman-Wunsch）全局对齐算法或 `sw`（Smith-Waterman）局部对齐算法。默认值为 `nw`。例如，`--algo sw` 将使用 Smith-Waterman 算法。

- `--seqnum`：要生成的随机序列的数量。默认值为 100。例如，`--seqnum 200` 将生成 200 个随机序列，较大的数值会导致较长的运行时间。


- `--seqlen`：要生成的每个序列的长度。默认值为 50。例如，`--seqlen 100` 将生成长度为 100 的序列，较大的数值会导致较长的运行时间。


以下是运行 `main.py` 的一个示例：

```bash
python main.py 1 -1 -1 --algo nw --seqnum 100 --seqlen 50
```

这将使用 Needleman-Wunsch 算法对 100 个长度为 50 的随机序列进行对齐，匹配得分为 1，不匹配得分为 -1，空位罚分为 -1。
