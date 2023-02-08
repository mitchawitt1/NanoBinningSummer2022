#!/bin/bash
FSTQ="$1" # Nanopore read FastQ
ILL1="$2" # First paired-end Illumina FastQ
ILL2="$3" # Second paired-end Illumina FastQ
OUTD="$4" # output directory
# Initialize all output directories and constants
mkdir -p $OUTD
mkdir -p $OUTD/workdir
mkdir -p $OUTD/mags
PREFIX=$(basename $FSTQ .fastq)
#echo $PREFIX
# Convert Nanopore read FastQ to FastA
# One-liner here, make the output $OUTD/workdir/$PREFIX.fasta
ONTF=$OUTD/workdir/$PREFIX.fasta

echo "ONTF=$ONTF"
echo "PREFIX=$PREFIX"

sed -n '1~4s/^@/>/p;2~4p' $FSTQ > $ONTF
# Map Illumina reads to the 'reference' Nanopore reads
bowtie2-build $ONTF $OUTD/workdir/$PREFIX
bowtie2 -x $OUTD/workdir/$PREFIX -p 40 -1 $ILL1 -2 $ILL2 | \
    samtools view -@ 40 -uS - | \
    samtools sort -@ 40 - \
    -o $OUTD/workdir/$PREFIX.sort.bam
samtools index -@ 40 $OUTD/workdir/$PREFIX.sort.bam
# Calculate the average coverage depth of each reference genome
jgi_summarize_bam_contig_depths $OUTD/workdir/$PREFIX.sort.bam --outputDepth $OUTD/workdir/coverage.txt
# Use the reference metagenome and average coverage to bin the Nanopore reads
metabat2 -m 2500 -t 40 --unbinned -i $ONTF -a $OUTD/workdir/coverage.txt -o $OUTD/mags/bin
mv $OUTD/mags/bin.unbinned.fa $OUTD/mags/unbinned.fa
# Some kind of Python script here to convert the binned reads in FastA format back to FastQ (i.e.: re-match to quality scores)
