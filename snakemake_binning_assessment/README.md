<!-- ABOUT THE PROJECT -->
## About
This snakemake pipeline is responsible for binning the simulated Nanopore reads using the current three methods: Metabat2, minimap2, CAT/BAT.

<!-- GETTING STARTED -->
### Conda Environment(s)

For now, the project's pipeline uses multiple separate conda environments to use all tools. It is left to the user to manage their environments and specify them to this tool. In this snakefile, four environments need to have metabat2, AMBER, minimap2, and CATBAT, the default environments specified in the config.yaml file can be created using the following commands:

```
conda create --name metabat2_env -c bioconda metabat2
conda create --name AMBER_env -c bioconda ambertools
conda create --name minimap2 -c bioconda minimap2
conda create --name CAT_env -c bioconda cat
```

### Usage
Once all environments are made or installed, the following values may need to be filled out in ```config.yaml``` if anything besides the default parameters want to be used:

```
reads_prefix:                       to specify the naming of nanosim files, {reads_prefix}_sample0_aligned_reads.fasta
autobin_dir:                        specify the location and name of the directory that will contain all pipeline outputs, it is very important to keep this consistent across all config files
```

Once the config file is ready, run the Snakefile like any other snakemake pipeline:
```
snakemake --cores 8
```
or by using the slurm job submission rapper ```run_snakemake.sh```
