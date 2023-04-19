#! /bin/bash -l
 
#SBATCH --partition=panda   # cluster-specific
#SBATCH --nodes=1
#SBATCH --ntasks=8
#SBATCH --job-name=snakemake_binning_assessment
#SBATCH --time=72:00:00   # HH/MM/SS
#SBATCH --mem=20G   # memory requested, units available: K,M,G,T
#SBATCH --output 100S0.1C1_autobin.out
#SBATCH --error 100S0.1C1_autobin.err
source ~/.bashrc

snakemake --cores 8
