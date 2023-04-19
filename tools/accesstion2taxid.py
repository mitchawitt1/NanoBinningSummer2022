import sys,gzip
dic = {}
dic_dead = {}

with gzip.open('nucl_gb.accession2taxid.gz') as fh:
    for line in fh:
        line = line.split()
        dic[line[0]] = line[1]

print(dic['A00001'])
# * 
#blast = 'A00001.1'
#for line in blast:
#    line = line.split()
#    if line[1] in dic:
#        print('%s\t%s\t%s'%(line[0],line[1],dic[line[1]]))
#    else:
#        print('%s\t%s\tNA'%(line[0],line[1]))


