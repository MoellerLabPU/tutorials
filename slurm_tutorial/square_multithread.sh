#!/bin/bash
#SBATCH --ntasks=1
#SBATCH --nodes=1
#SBATCH --output=square_multithread.%J.out
#SBATCH --error=square_multithread.%J.err
#SBATCH --time=00:10:00
#SBATCH --mem=1G
#SBATCH --cpus-per-task=4


outDir="/workdir1/sidd"
python square_multithread.py --cpus "$SLURM_CPUS_PER_TASK" --output-file $outDir/square_multithread_results.csv
