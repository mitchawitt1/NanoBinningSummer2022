#! /bin/bash -l
 
#SBATCH --partition=panda   # cluster-specific
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --job-name=get_bamfa
#SBATCH --time=04:00:00   # HH/MM/SS
#SBATCH --mem=4G   # memory requested, units available: K,M,G,T

cd /athena/ihlab/store/miw4007/simulation_test/

wget https://portal.nersc.gov/dna/RD/Metagenome_RD/MetaBAT/Software/Mockup/library1.sorted.bam

wget https://portal.nersc.gov/dna/RD/Metagenome_RD/MetaBAT/Software/Mockup/library2.sorted.bam

wget https://portal.nersc.gov/dna/RD/Metagenome_RD/MetaBAT/Software/Mockup/assembly.fa

wget https://portal.nersc.gov/dna/RD/Metagenome_RD/MetaBAT/Software/Mockup/membership.txt

exit
