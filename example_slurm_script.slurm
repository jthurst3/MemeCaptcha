#!/bin/bash
#SBATCH -p standard
#SBATCH -N 1
#SBATCH -t 1:00:00
#SBATCH --mem-per-cpu=1GB
#SBATCH -o plot.log
#SBATCH -e plot.error
#SBATCH -J plot.log
#SBATCH --mail-type=all

module load r
args="/scratch/alarracu_lab/tkhunkhe/jellyfish-out/ RNApolII.enrichment.25.tsv RNApolII.enrichment.25.2.tsv"
Rscript plot_enrichment_wrapper.R ${args}

#to submit type: sbatch example_slurm_script.slurm