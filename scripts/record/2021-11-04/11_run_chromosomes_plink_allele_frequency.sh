#!/bin/bash

# Note:
# Each linear GWAS (30,000 - 200,000 records; 22 chromosomes) requires about
# 5-7 hours to run on the grid.

################################################################################
# Organize argument variables.

path_table_cohort=${1} # full path to table with identifiers of persons and genotypes in cohort for analysis
path_genotype_chromosome=${2} # full path to file for chromosome genotype information
path_sample_chromosome=${3} # full path to file for chromosome sample information
path_allele_frequency_chromosome=${4} # full path to directory for chromosome report
threshold_allele_frequency=${5} # threshold filter by minor allele frequency
threads=${6} # count of processing threads to use
path_plink2=${7} # full path to executable installation of PLINK2

################################################################################
# Organize variables.

# Initialize directories.
###rm -r $path_allele_frequency_chromosome # be careful!
if [ ! -d $path_allele_frequency_chromosome ]; then
    # Directory does not already exist.
    # Create directory.
    mkdir -p $path_allele_frequency_chromosome
fi

###########################################################################
# Calculate allele frequencies in PLINK2.

cd $path_allele_frequency_chromosome
# Call PLINK2.
# This call to PLINK2 includes "--freq" and produces a report of allele
# frequencies.
# 90,000 Mebibytes (MiB) is 94.372 Gigabytes (GB)
# Argument "--reference-allele" allows to give an explicit list of alleles to designate as "A1".
# "Warning: No --bgen REF/ALT mode specified ('ref-first', 'ref-last', or 'ref-unknown'). This will be required as of alpha 3."
$path_plink2 \
--memory 90000 \
--threads $threads \
--bgen $path_genotype_chromosome ref-first \
--sample $path_sample_chromosome \
--keep $path_table_cohort \
--maf $threshold_allele_frequency \
--freq \
--out report



##########
