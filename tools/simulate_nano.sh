#! /bin/bash -l
 
#SBATCH --partition=panda   # cluster-specific
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --job-name=simulate_nano
#SBATCH --time=02:00:00   # HH/MM/SS
#SBATCH --mem=8G   # memory requested, units available: K,M,G,Ti

#conda deactivate
conda activate nanos2

module load python
python simulate_nano.py --inputdir ../input_seq/cleaned_seqs/2Spec --coverage 1 --configdir ../nano_config --profile ../err_profs/metagenome_ERR3152364_Even/metagenome_ERR3152364_Even --outdir ../auto_binning_output/mgERR

exit 
