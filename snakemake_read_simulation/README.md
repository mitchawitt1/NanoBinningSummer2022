<!-- ABOUT THE PROJECT -->
## About
This snakemake pipeline is responsible for creating simulated Nanopore reads and Illumina reads using Nanosim and ART Illumina respectively.

<!-- GETTING STARTED -->
### Conda Environment(s)

For now, the project's pipeline uses multiple separate conda environments to use all tools. It is left to the user to manage their environments and specify them to this tool. In this snakefile, two environments need to have ART Illumina and Nanosim on them, the default environments specified in the config.yaml file can be created using the following commands:

```
conda create --name nanosim_env -c bioconda nanosim
conda create --name ART_env -c bioconda art
```

If you create your own environments, you have to specify them in ```config.yaml``` by changing the values of the variables ```ART_env``` and ```nanosim_env```

### Usage
Once all environments are made or installed, the following values may need to be filled out in ```config.yaml``` if anything besides the default parameters want to be used:

```
reference_genomes:                  directory that contains reference genomes in fasta files format, should represent all of the species to included in the simulated reads.
error_profile:                      directory that contains the error profile files used for nanosim.
reads_prefix:                       to specify the naming of nanosim files, {reads_prefix}_sample0_aligned_reads.fasta
coverage:                           default 1.0X
autobin_dir:                        specify the location and name of the directory that will contain all pipeline outputs, it is very important to keep this consistent across all config files
```

Once the config file is ready, run the Snakefile like any other snakemake pipeline:
```
snakemake --cores 1
```
or by using the slurm job submission rapper ```run_snakemake.sh```
