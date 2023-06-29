#! /bin/bash -l
 
#SBATCH --partition=panda   # cluster-specific
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --job-name=test_metaassembly
#SBATCH --time=05:00:00   # HH/MM/SS
#SBATCH --mem=16G   # memory requested, units available: K,M,G,T
#SBATCH --output test_metaassembly-%j.out
#SBATCH --error test_metaassembly-%j.err

#source ~/anaconda3/etc/profile.d/conda.sh
#conda activate flye_env
#cd /athena/ihlab/scratch/miw4007/simulation_test/tools/snakemake_assembly/

BINS_PATH=$1
#"../snakemake_read_simulation/10S1C_autobin_output_3/minimap2/mm2_bins/"
ASSEMBLY_OUTPUT=$2
#"../snakemake_read_simulation/10S1C_autobin_output_3/minimap2/flye_assembly"
BINS=$(ls $BINS_PATH | grep -E "bin.[0-9]*.fa" | grep -oe "[0-9]*")

mkdir $ASSEMBLY_OUTPUT || true

for bin_num in ${BINS[@]}; do
	if [ ! -d $ASSEMBLY_OUTPUT/bin$bin_num/ ]
	then
		mkdir $ASSEMBLY_OUTPUT/bin$bin_num/
		flye --nano-raw $BINS_PATH/bin."$bin_num".fa --meta -o $ASSEMBLY_OUTPUT/bin$bin_num/ || true
	elif [ ! -f $ASSEMBLY_OUTPUT/bin$bin_num/assembly_graph.gfa ]
	then
		flye --nano-raw $BINS_PATH/bin."$bin_num".fa --meta -o $ASSEMBLY_OUTPUT/bin$bin_num/ || true
	fi
done

