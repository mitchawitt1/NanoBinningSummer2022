import sys,gzip
dic = {}
dic_dead = {}

with gzip.open('nucl_gb.accession2taxid.gz') as fh:
    for line in fh:
        line = line.split()
        dic[line[0]] = line[1]
