#! /bin/bash -l
 
#SBATCH --partition=panda   # cluster-specific
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --job-name=snakemake_binning_assessment
#SBATCH --time=16:00:00   # HH/MM/SS
#SBATCH --mem=28G   # memory requested, units available: K,M,G,T
#SBATCH --output sm_autobin.out
#SBATCH --error sm_autobin.err
source ~/.bashrc

snakemake --cores 8
