#! /bin/bash -l
 
#SBATCH --partition=panda   # cluster-specific
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --job-name=metaprob_binning
#SBATCH --time=12:00:00   # HH/MM/SS
#SBATCH --mem=8G   # memory requested, units available: K,M,G,T

source ~/.bashrc

conda deactivate
conda activate metaprob2

cd /athena/ihlab/store/miw4007/simulation_test/binning_outputs/2Spec/1Cov/mgErr_Even/metaprob

#MetaProb -si /athena/ihlab/store/miw4007/simulation_test/deprecated/metaprob2/MetaProb/TestInputFile/long_example_1.fna -numSp 2 -feature 2 -m 45

MetaProb -si /athena/ihlab/store/miw4007/simulation_test/simulation_output/2Spec/1Cov/MetaProbInput/submpr_mgERR_sample0_aligned_reads_1.fastq -numSp 2 -feature 2 -m 45

exit
