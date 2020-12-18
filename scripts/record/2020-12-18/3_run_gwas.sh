#!/bin/bash

###########################################################################
# Specify arguments for qsub command.
# Note that bash does not interpret qsub parameters, which are bash comments.
# Bash will not expand variables in qsub parameters.
# Shell.
#$ -S /bin/bash
# Name of job.
#$ -N waller_gwas
# Contact.
#$ -M tcameronwaller@gmail.com
### #$ -m abes
#$ -m abe
# Standard output and error.
# Specify as arguments when calling qsub.
### -o "./out"
### -e "./error"
# Queue.
# "1-hour", "1-day", "4-day", "7-day", "30-day", "lg-mem"
#$ -q 1-day
# Priority 0-15.
### -p -10
# Memory per iteration.
# Segmentation errors commonly indicate a memory error.
#$ -l h_vmem=20G
# Concurrent threads; assigns value to variable NSLOTS.
# Important to specify 32 threads to avoid inconsistency with interactive
# calculations.
#$ -pe threaded 32
# Range of indices.
# Specify as argument when calling qsub.
# Array batch indices cannot start at zero.
### -t 1-100:1
# Limit on concurrent processes.
# Process this count of chromosomes at a time for each job.
#$ -tc 4


###########################################################################
###########################################################################
###########################################################################
# This script executes GWAS regression across single nucleotide
# polymorphisms (SNPs).
# PLINK2's intermediate files occupy much more data storage space than do
# the final result files.
# If working within a processing directory with only 3 Terabytes of data
# storage, then only attempt to execute about 10 GWAS concurrently across
# a cohort of 30,000-40,000 persons.
###########################################################################
###########################################################################
###########################################################################

# Read private, local file paths.
echo "read private file path variables and organize paths..."
cd ~/paths
path_plink2=$(<"./tools_user_plink2.txt")
path_ukb_genotype=$(<"./ukbiobank_genotype.txt")

# Organize variables.
chromosome=$SGE_TASK_ID
path_table_phenotypes_covariates=$1
path_report=$2
analysis=$3
phenotypes=$4
covariates=$5
threads=$6
maf=$7

# Set directory.
path_chromosome="$path_report/chromosome_$chromosome"
# Determine whether the temporary directory structure already exists.
if [ ! -d $path_chromosome ]; then
    # Directory does not already exist.
    # Create directory.
    mkdir -p $path_chromosome
fi
cd $path_chromosome

# Call PLINK2.
# 90,000 Mebibytes (MiB) is 94.372 Gigabytes (GB)
# --pfilter drops SNPs with null p-values and any beyond threshold (such as 1)
$path_plink2 \
--memory 90000 \
--threads $threads \
--bgen $path_ukb_genotype/Chromosome/ukb_imp_chr${chromosome}_v3.bgen \
--sample $path_ukb_genotype/Chromosome/ukb46237_imp_chr${chromosome}_v3_s487320.sample \
--keep $path_table_phenotypes_covariates \
--maf $maf \
--freq --glm hide-covar \
--pfilter 1 \
--pheno $path_table_phenotypes_covariates \
--pheno-name $phenotypes \
--covar $path_table_phenotypes_covariates \
--covar-name $covariates \
--out report \
