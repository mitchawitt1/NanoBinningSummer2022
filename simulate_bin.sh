#! /bin/bash -l
 
#SBATCH --partition=panda   # cluster-specific
#SBATCH --nodes=1
#SBATCH --ntasks=8
#SBATCH --job-name=simulate_nano
#SBATCH --time=72:00:00   # HH/MM/SS
#SBATCH --mem=20G   # memory requested, units available: K,M,G,Ti

source ~/.bashrc
cd /athena/ihlab/store/miw4007/simulation_test/tools/

conda deactivate
conda activate nanosim_env

INPUT_DIR="../input_seq/cleaned_seqs/100Spec/"
COV=0.1
CONFIG_DIR="../nano_config/"
PROFILE="../err_profs/metagenome_ERR3152364_Even/metagenome_ERR3152364_Even"
OUT_DIR="../auto_binning_output/"
PREFIX="mgERR"
NANO_PRE="$OUT_DIR$PREFIX"
BIN_METHOD="metabat2"

if [ $BIN_METHOD != "metabat2" ] && [ $BIN_METHOD != "metaprob" ]
then
	echo "Binning method not recognized!"
	exit
fi

#echo $NANO_PRE

#module load python
# Simulate nanopore reads using a custom made config file creator and nanosim
python simulate_nano.py --inputdir $INPUT_DIR --coverage $COV --configdir $CONFIG_DIR --profile $PROFILE --outdir $NANO_PRE

cd $OUT_DIR

# convert fastq aligned reads file to fasta format
sed -n '1~4s/^@/>/p;2~4p' "$PREFIX"_sample0_aligned_reads.fastq > "$PREFIX"_sample0_aligned_reads.fasta

# create art illumina simulated reads to get coverage
mkdir ART_reads
cd ART_reads

conda deactivate
conda activate ART_env

READS="$PREFIX"_sample0_aligned_reads

art_illumina -p -sam -i ../"$READS".fasta -o illumina_sim -l 50 -f 20 -m 200 -s 10

# running metabat2 binning method
if [ $BIN_METHOD = "metabat2" ]
then
	conda deactivate
	conda activate metabat2_env

	cd ../
	mkdir bins
	cd bins

	bash /athena/ihlab/store/miw4007/simulation_test/tools/metabat2.sh ../"$READS".fastq ../ART_reads/illumina_sim1.fq ../ART_reads/illumina_sim2.fq metabat2
	
	# run AMBER metrics on the bins created by metabat2
	conda deactivate
	conda activate AMBER_env
	
	cd ../
	mkdir AMBER_results
	cd AMBER_results

	# get gold standard mapping from simulated reads and bin mappings
	python /athena/ihlab/store/miw4007/simulation_test/tools/get_bin_mappings.py ../"$READS".fasta ../bins/metabat2/mags metabat2_bins.tsv metabat2

	# run AMBER analysis
	amber.py -g gsa_mapping.binning metabat2_bins.tsv -o .
fi

exit 
