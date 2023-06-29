#! /bin/bash -l
 
#SBATCH --partition=panda   # cluster-specific
#SBATCH --nodes=1
#SBATCH --ntasks=8
#SBATCH --job-name=snakemake_binning_assessment
#SBATCH --time=72:00:00   # HH/MM/SS
#SBATCH --mem=50G   # memory requested, units available: K,M,G,T
#SBATCH --output new_10S10C_autobin.out
#SBATCH --error new_10S10C_autobin.err
source ~/.bashrc

snakemake --cores 8
