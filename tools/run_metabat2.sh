#! /bin/bash -l
 
#SBATCH --partition=panda   # cluster-specific
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --job-name=metabat2
#SBATCH --time=120:00:00   # HH/MM/SS
#SBATCH --mem=36G   # memory requested, units available: K,M,G,T

source ~/.bashrc
conda deactivate
conda activate metabat2_env

cd /athena/ihlab/store/miw4007/simulation_test/binning_outputs/100Spec/1Cov/mgErr_Even/

bash /athena/ihlab/store/miw4007/simulation_test/tools/metabat2.sh /athena/ihlab/store/miw4007/simulation_test/simulation_output/100Spec/1Cov/mgERR_sample0_aligned_reads.fastq /athena/ihlab/store/miw4007/simulation_test/simulation_output/100Spec/1Cov/ART_illumina/illumina_sim1.fq /athena/ihlab/store/miw4007/simulation_test/simulation_output/100Spec/1Cov/ART_illumina/illumina_sim2.fq metabat2

exit
