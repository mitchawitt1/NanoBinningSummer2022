import re
import sys
import os
import subprocess
import csv
from Bio import SeqIO
import numpy as np

### READ in simulated reads file and assign them bins based off their
### headers (created by nanosim, so it has info on reference)
def write_gsa(simulated_reads_path):
    bin_file = simulated_reads_path
    gsa_file = "gsa_mapping.binning"
    bin_ids = []
    with open(bin_file) as bins:
        with open(gsa_file, "w") as gsa:
            gsa.write("@Version:0.9.1\n")
            gsa.write("@SampleID:_SAMPLEID_\n")
            gsa.write("\n")
            # Each read is assigned a correct label and sequence length
            gsa.write("@@SEQUENCEID\tBINID\t_LENGTH\n")
            records = SeqIO.parse(bin_file, 'fasta')
            for record in records:
                # Nanosim assigns read headers according to this pattern I found
                # by looking at example headers
                # The bin ID is the beginning part of this pattern
                bin_search = re.search('(.*)_[0-9]*_aligned_[0-9]*_[R,F]_[0-9]*_[0-9]*_[0-9]*$', record.id)
                bin_id = bin_search.group(1)
                gsa.write(record.id + "\t" + bin_id + "\t" + str(len(record.seq)) + "\n")

def write_mappings_metabat2(bins_path, out_dir):
    script = ['python', '/athena/ihlab/store/miw4007/simulation_test/tools/AMBER/src/utils/convert_fasta_bins_to_biobox_format.py']
    files = os.listdir(bins_path)
    #print(files)
    metabat2_bin_regex = "bin\.[0-9]*\.fa"
    for f in files:
        if re.match(metabat2_bin_regex, f):
            script.append(os.path.join(bins_path, f))
    script.append('-o')
    script.append(out_dir)
    subprocess.call(script)

def write_mappings_catbat(tax_path, out_dir):
    bin_map_file = out_dir
    CAT_tax_path = tax_path
    taxonomy_scores = {}

    with open(CAT_tax_path) as tax_file:
        tax_file_reader = csv.reader(tax_file, delimiter="\t")
        tax_file_reader.__next__()
        for line in tax_file_reader:
            if len(line) == 4:
                lineage = line[2].split(";")
                if (len(lineage) > 7): ### CHANGE BACK TO 9, THE SPECIES LEVEL
                    speciesID = lineage[7]
                    index = line[0].rfind('_')
                    bit_score = float(line[3])
                    read_header = line[0][:index]
                    if (not(read_header in taxonomy_scores)):
                        entry = [[speciesID], [bit_score]]
                        taxonomy_scores[read_header] = entry
                    else:
                        taxonomy_scores[read_header][0].append(speciesID)
                        taxonomy_scores[read_header][1].append(bit_score)

    with open(bin_map_file, "w") as bin_map:
        bin_map.write("@Version:0.9.1\n")
        bin_map.write("@SampleID:_SAMPLEID_\n")
        bin_map.write("@@SEQUENCEID\tBINID\n")
        for read, spec_scores in taxonomy_scores.items():
            species_ids = spec_scores[0]
            scores = spec_scores[1]
            max_score_index = np.argmax(np.array(scores))
            max_species_id = species_ids[max_score_index]
            bin_map.write(read + "\t" + max_species_id + "\n")

def main(args):
    write_gsa(args[0])
    if (args[3] == "metabat2"):
        write_mappings_metabat2(args[1], args[2])
    elif (args[3] == "CATBAT"):
        write_mappings_catbat(args[1], args[2])

if __name__ == "__main__":
    main(sys.argv[1:])
