#! /bin/bash -l

#SBATCH --partition=panda   # cluster-specific 
#SBATCH --nodes=1
#SBATCH --ntasks=1 
#SBATCH --job-name=CATBAT
#SBATCH --time=96:00:00   # HH/MM/SS
#SBATCH --mem=8G   # memory requested, units available: K,M,G,T

DATASET="10Spec/0.1Cov"
conda deactivate
conda activate CAT_env

cd /athena/ihlab/scratch/miw4007/simulation_test/binning_outputs/$DATASET/mgErr_Even/
mkdir CATBAT

cd /athena/ihlab/scratch/miw4007/simulation_test/tools

CAT contigs -c /athena/ihlab/store/miw4007/simulation_test/10S0_1Cautobin_output/mgERR_sample0_aligned_reads.fasta -d /athena/masonlab/scratch/databases/metagenomics/CAT_prepare_20210107/2021-01-07_CAT_database/ -t /athena/masonlab/scratch/databases/metagenomics/CAT_prepare_20210107/2021-01-07_taxonomy/ --force -o ../binning_outputs/$DATASET/mgErr_Even/CATBAT/CATBAT --block_size 0.25 --tmpdir ../binning_outputs/$DATASET/mgErr_Even/CATBAT
exit
