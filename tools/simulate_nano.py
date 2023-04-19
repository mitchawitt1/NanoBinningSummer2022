import preproc_nano
from Bio import SeqIO
import csv
import sys
import os
import argparse
import subprocess

def handle_args():
    parser = argparse.ArgumentParser()
    # optional arguments: directory where fasta files are located, number of reads to generate, where to put config files
    parser.add_argument('--inputdir', nargs='?', const='', type=str)
    parser.add_argument('--nreads', nargs='?', const=1000, type=int)
    parser.add_argument('--configdir', nargs='?', const='nano_config', type=str)
    parser.add_argument('--coverage', nargs='?', const=1.0, type=float)
    parser.add_argument('--profile', nargs=1, type=str)
    parser.add_argument('--outdir', nargs='?', type=str)
    
    args = parser.parse_args()
    inputdir = args.inputdir
    nreads = args.nreads
    configdir = args.configdir
    coverage = args.coverage
    
    # Since the profile becomes direct input of nanosim, simulator.py should be able to handle errors for this
    profile = args.profile[0]
    outdir = args.outdir

    # look for fasta files in current directory if not specified
    if inputdir == None:
        inputdir = ''

    if outdir == None:
        outdir = ''
        
    # look for or create a nano_config folder in current directory if not specified
    if configdir == None:
        configdir = 'nano_config'
        
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
    configdir = os.path.abspath(configdir)   
    if not(os.path.isdir(configdir)):
        os.mkdir(configdir)

    return (fasta_list, nreads, coverage, profile, configdir, outdir)

def main(argv):
    # average length of a nanopore read taken from https://www.nature.com/articles/s41587-021-01108-x
    AVG_LEN = 18350
        
    # parses arguments
    inp_seqs, nreads, coverage, profile, config_dir, out_dir = handle_args()
    
    # create config files
    n, total_length = preproc_nano.create_genome_list(inp_seqs, config_dir)
    preproc_nano.create_abundance_list(inp_seqs, nreads, n, config_dir, coverage, total_length)
    preproc_nano.create_dna_list(inp_seqs, config_dir)
    
    # get config file paths
    gl_path = os.path.join(config_dir, "gl.tsv")
    a_path = os.path.join(config_dir, "a.tsv")
    dl_path = os.path.join(config_dir, "dl.tsv")
    
    # set of strings for calling nanosim subprocess
    subproc_list = []
    subproc = ""
    
    # run simulator.py
    if out_dir == '':
        # if there is no specified output directory, then use default directory provided by nanosim
        subproc_list = ["simulator.py", "metagenome", "-c", profile, "-gl", gl_path, "-a", a_path, "-dl", dl_path, "-med", str(AVG_LEN), "-sd 1.0", "--fastq", "-b", "guppy"]
    else:
        # if there is a specified output directory, then let nanosim use it/handle any possible errors relating to it
        subproc_list = ["simulator.py", "metagenome", "-c", profile, "-gl", gl_path, "-a", a_path, "-dl", dl_path, "-med", str(AVG_LEN), "-sd 1.0", "--fastq", "-b", "guppy", "-o", out_dir]
        
    print(subproc_list)
    subproc_str = " ".join(subproc_list)        
    subprocess.run(subproc_str, shell=True)

if __name__ == '__main__':
    main(sys.argv[1:])
