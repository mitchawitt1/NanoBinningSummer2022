#contig_counter=0
#INPUT_FILE="/athena/ihlab/scratch/miw4007/simulation_test/tools/snakemake_read_simulation/50S1C_autobin_output_3/CATBAT/CATBAT_assemblies.fasta"
awk '$1 ~ ">contig_[0-9]*" { printf(">contig_%d\n", ++i); next } { print }' $1
#awk 'BEGIN{contig_counter=0} {for(i=1;i<=NF;i++){if($i~/^>contig_/){$contig_counter=($contig_counter+1); $i=">contig_"$contig_counter}}} 1' 
