from Bio import SeqIO
import csv
import sys
import os
import argparse


### from a list of fasta files, create the genome list (.tsv) required for nanosim and put into config folder

def create_genome_list(fasta_list, out_dir):
    # should return the number of species for abundance calculation and verification
    num_species = 0
    cwd = os.getcwd()
    out_path = os.path.join(out_dir, 'gl.tsv')
    total_length = 0
    with open(out_path, 'wt') as gl:
        tsv_writer = csv.writer(gl, delimiter='\t')

        # open every fasta file in the given list (assumed to local paths only)

        for f in fasta_list:
#             if not os.path.isabs(f):
#                 path_to_f = cwd + '/' + f
            for record in SeqIO.parse(f, 'fasta'):
                num_species += 1
                total_length += len(record.seq)
                # first column is species/strain name, second is path to file that has genome
                tsv_writer.writerow([record.name, f])

    return num_species, total_length


### from a list of fasta files, create the abundance list (.tsv) required for nanosim and put it into config folder

def create_abundance_list(
    fasta_list,
    num_reads,
    num_species,
    out_dir,
    coverage,
    total_length
    ):
    
    # latest average length of nanopore reads taken from https://www.nature.com/articles/s41587-021-01108-x
    AVG_LENGTH = 18350
    out_path = os.path.join(out_dir, 'a.tsv')
    with open(out_path, 'wt') as dl:
        tsv_writer = csv.writer(dl, delimiter='\t')
        size = num_reads
        if num_reads == None:
            size = total_length * coverage / AVG_LENGTH
            size = int(size)
            
        tsv_writer.writerow(['Size', size])
        
        # open every fasta file in the given list (assumed to local paths only)
        for f in fasta_list:
            for record in SeqIO.parse(f, 'fasta'):
                # first column is species name, second chromosome name, third is abundance
                # relative abundances are supposed to add up  to 100
                # also assuming even abundances, which really isn't that realistic
                # SOOOOO, it would be cool to make a realistic abundance distribution (geometric distribution??)
                rel_abundance = 100 / num_species
                tsv_writer.writerow([record.name, rel_abundance])


### from a list of fasta files, create the dna list (.tsv) required for nanosim, and put it into specified config folder

def create_dna_list(fasta_list, out_dir):
    out_path = os.path.join(out_dir, 'dl.tsv')
    with open(out_path, 'wt') as dl:
        tsv_writer = csv.writer(dl, delimiter='\t')

        # open every fasta file in the given list (assumed to local paths only)
        for f in fasta_list:
            for record in SeqIO.parse(f, 'fasta'):

                # first column is species name, second chromosome name, third is dna type (linear/circular)
                tsv_writer.writerow([record.name, 'NA', 'linear'])


def ap_handle_args():
    parser = argparse.ArgumentParser()
    # optional arguments: directory where fasta files are located, number of reads to generate, where to put config files
    parser.add_argument('--inputdir', nargs='?', const='', type=str)
    parser.add_argument('--nreads', nargs='?', const=1000, type=int)
    parser.add_argument('--outputdir', nargs='?', const='nano_config', type=str)
    parser.add_argument('--coverage', nargs='?', const=1.0, type=float)
    
    args = parser.parse_args()
    inputdir = args.inputdir
    nreads = args.nreads
    outputdir = args.outputdir
    coverage = args.coverage

    # look for fasta files in current directory if not specified
    if inputdir == None:
        inputdir = ''

    # look for or create a nano_config folder in current directory if not specified
    if outputdir == None:
        outputdir = 'nano_config'
        
    # create 1000 reads if not specified
#     if nreads == None:
#         nreads = 1000
    
    # coverage should override the number of reads
    if coverage == None:
        if nreads == None:
            nreads = 1000
    else:
        nreads = None

    inputdir = os.path.abspath(inputdir)
#     print(inputdir)
    fasta_list = []
    # find all fasta/fna files in input directory
    if not(os.path.isdir(inputdir)):
        raise Exception("input directory does not exist")
    else:
        file_list = os.listdir(inputdir)
#         print(file_list)
        for f in file_list:
            if not(os.path.isdir(f)):
                ext = os.path.splitext(f)[-1]
#                 print(ext)
                if (ext == '.fna') or (ext == '.fasta'):
                    fasta_list.append(os.path.abspath(os.path.join(inputdir, f)))
                
    # program can't run if there are no fasta/fna files found
    if fasta_list == []:
        raise Exception("No .fasta or .fna files listed in the input directory")
     
    # make output directory if not found
    outputdir = os.path.abspath(outputdir)   
    if not(os.path.isdir(outputdir)):
        os.mkdir(outputdir)

    return (fasta_list, nreads, outputdir, coverage)


# def handle_args(args):
    # # Note to self: this code is really ugly, please change this structure with parse arguments or something
#     if len(args) == 3:
#         if os.path.isdir(args[2]):
#             if args[1].isnumeric():
#                 if os.path.isdir(args[0]):
#                     return args[0], int(args[1]), args[2]
#                 else:
#                     raise Exception
#             else:

#     if os.path.isdir(args[-1]):
#         if args[-2].isnumeric():
#             return args[:-2], int(args[-2]), args[-1]
#         else:
#             return args[:-2], 1000, args[-1]

#     else:
#         if args[-1].isnumeric():
#             try:
#                 os.mkdir("nano_config")
#             except FileExistsError:
#                 pass

#             return args[:-1], int(args[-1]), 'nano_config'

#         elif args[-2].isnumeric():
#             try:
#                 os.mkdir(args[-1])
#             except FileExistsError:
#                 pass
#             return args[:-2], int(args[-2]), args[-1]

def main(argv):
#     inp_seqs, nreads, out_dir = handle_args(argv)
#     inp_seqs, nreads, out_dir = ap_handle_args(argv)

    # parses arguments
    inp_seqs, nreads, out_dir, coverage = ap_handle_args()
    
#     print(inp_seqs)
#     print(inp_seqs)
#     print(nreads)
#     print(out_dir)

    n, total_length = create_genome_list(inp_seqs, out_dir)
    create_abundance_list(inp_seqs, nreads, n, out_dir, coverage, total_length)
    create_dna_list(inp_seqs, out_dir)

if __name__ == '__main__':
    main(sys.argv[1:])
