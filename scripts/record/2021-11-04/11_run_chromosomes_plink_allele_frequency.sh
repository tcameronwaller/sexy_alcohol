#!/bin/bash

# Note:
# Each linear GWAS (30,000 - 200,000 records; 22 chromosomes) requires about
# 5-7 hours to run on the grid.


###########################################################################
# Organize paths.
# Read private, local file paths.
echo "read private file path variables and organize paths..."
cd ~/paths
path_process=$(<"./process_sexy_alcohol.txt")
path_scripts_record="$path_process/sexy_alcohol/scripts/record/2021-11-04"
path_dock="$path_process/dock"

path_reference_population="${path_dock}/stratification/reference_population"
path_table_phenotypes_covariates="${path_reference_population}/table_white_unrelated_female_male.tsv"

path_allele_frequency="${path_dock}/allele_frequency"

################################################################################
# Organize argument variables.

path_report=${2} # full path to parent directory for GWAS summary statistics
analysis=${3} # unique name for association analysis

threads=32 # count of processing threads to use


#threshold_allele_frequency=0.0 # threshold filter by minor allele frequency
# use this threshold in "--maf $threshold_allele_frequency" after reading in the allele frequencies

###########################################################################
# Organize variables.

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
--bgen $path_genotype ref-first \
--sample $path_sample \
--keep $path_table_phenotypes_covariates \
--maf $threshold_allele_frequency \
--freq \
--out report



##########
