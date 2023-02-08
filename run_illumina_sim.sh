#! /bin/bash -l
 
#SBATCH --partition=panda   # cluster-specific
#SBATCH --nodes=1
#SBATCH --ntasks=8
#SBATCH --job-name=illumina_sim
#SBATCH --time=24:00:00   # HH/MM/SS
#SBATCH --mem=8G   # memory requested, units available: K,M,G,Ti

source ~/.bashrc
conda deactivate
conda activate ART_env

cd /athena/ihlab/store/miw4007/simulation_test/simulation_output/100Spec/10Cov/
mkdir ART_illumina

sed -n '1~4s/^@/>/p;2~4p' mgERR_sample0_aligned_reads.fastq > mgERR_sample0_aligned_reads.fasta

cd ART_illumina

echo "SIMULATING_ILLUMINA"

art_illumina -p -sam -i /athena/ihlab/store/miw4007/simulation_test/simulation_output/100Spec/10Cov/mgERR_sample0_aligned_reads.fasta -o illumina_sim -l 50 -f 20 -m 200 -s 10

exit
