import pandas as pd
import Bio
import sys
from Bio import SeqIO
import os

"""
The purpose of this script is to take the mapping files generated from the MM2-based
binning method into actual fasta files that represent the subsequently generated bins.
The current structure of MM2 (and CATBAT) files is:
sequence_header -> taxid
for example:
MGYG000000001_1-MGYG000000001-1_1359349_aligned_1_F_2_160812_14 -> 1496

We use the unique taxids to correspond to a specific bin number and then write all
sequences to their subsequent bin fasta file
"""
# specify where we want to put bin fastas
map_file_loc = sys.argv[1]
nanopore_reads = sys.argv[2]
outdir = sys.argv[3]

# read in the mm2 mappings file
mm2_mapping = pd.read_csv(map_file_loc, skiprows=4, header=None, sep="\t")

# specify the first entry, just so dictionary isn't empty
taxid_to_binnum = {mm2_mapping.iloc[0, 1]: 0}
num_bins = 1

# start populating a mapping for taxid to its bin number
for index, row in mm2_mapping.iterrows():
    tax_id = row.iloc[1]
    # if taxid is not already present, add a new mapping
    if not(tax_id in taxid_to_binnum):
        taxid_to_binnum[tax_id] = num_bins
        num_bins += 1
        
# start writing bin fastas
for tax_id, binnum in taxid_to_binnum.items():
    # extract all sequence headers that are mapped to this specific taxid
    headers = list(mm2_mapping.loc[mm2_mapping.iloc[:, 1] == tax_id].loc[:, 0])
    # get the sequences that correspond to these headers
    records = (r for r in SeqIO.parse(open(nanopore_reads), "fasta") if r.id in headers)
    # write all header-sequence pairs to bin fasta
    bin_file = open(os.path.join(outdir, "bin." + str(binnum) + ".fa"), 'w+')
    count = SeqIO.write(records, bin_file, "fasta")