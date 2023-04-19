#! /bin/bash -l
 
#SBATCH --partition=panda   # cluster-specific
#SBATCH --nodes=1
#SBATCH --ntasks=4
#SBATCH --job-name=nano_assembly
#SBATCH --time=72:00:00   # HH/MM/SS
#SBATCH --mem=20G   # memory requested, units available: K,M,G,T
#SBATCH --output 10S1C3_assembly_autobin.out
#SBATCH --error 10S1C3_assembly_autobin.err
source ~/.bashrc

snakemake --cores 4
