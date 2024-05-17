# SeqAlign

下载数据
```bash
conda activate <your-env>
conda install -c conda-forge ncbi-datasets-cli
datasets download genome taxon human --reference --chromosomes 1 --include genome --filename human_chr1_seq.zip
unzip -j human_chr1_seq.zip ncbi_dataset/data/GCF_000001405.40/chr1.fna -d sequences
```