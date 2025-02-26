#!/bin/bash
#SBATCH --ntasks=1
#SBATCH --nodes=1
#SBATCH --output=prodigal.%J.out
#SBATCH --error=prodigal.%J.err
#SBATCH --time=00:10:00
#SBATCH --mem=4000
#SBATCH --cpus-per-task=1

# Path to prodigal binary
export PATH=/programs/prodigal-2.6.3:$PATH

# My genome to analyze
fasta="/workdir1/Shared_Folder/for_slurm_tutorial/GCA_024761245.1.fna"

# Output directory
outDir="/workdir1/sidd"

# Final command
prodigal -i $fasta -o $outDir/GCA_024761245.gbk -f gbk -a $outDir/GCA_024761245.faa