#!/bin/bash

#chmod u+x script.sh

###########################################################################
###########################################################################
###########################################################################
# This script organizes directories and iteration instances then submits
# script "regress_metabolite_heritability.sh" to the Sun Grid Engine.
###########################################################################
###########################################################################
###########################################################################

echo "----------------------------------------------------------------------"
echo "----------------------------------------------------------------------"
echo "----------------------------------------------------------------------"
echo "----------"
echo "The script organizes and submits an array batch job."
echo "----------"
echo "version check: 1"
echo "----------------------------------------------------------------------"
echo "----------------------------------------------------------------------"
echo "----------------------------------------------------------------------"

# Organize paths.
# Read private, local file paths.
echo "read private file path variables and organize paths..."
cd ~/paths
path_temporary=$(<"./temporary_sexy_alcohol.txt")
path_waller="$path_temporary/waller"
path_dock="$path_temporary/waller/dock"
path_scripts="$path_waller/sexy_alcohol/scripts/gwas"

# Case-specific paths.
path_table_phenotypes_covariates="$path_temporary/waller/dock/organization/trial/table_phenotypes_covariates.tsv"
path_report="$path_temporary/waller/dock/gwas/female_alcohol_testosterone"

# Parameters.
count=2 # 22 # Count of chromosomes on which to run GWAS
analysis="female_alcohol_testosterone"
phenotypes="testosterone"
covariates="age,body_mass_index,genotype_pc_1,genotype_pc_2,genotype_pc_3,genotype_pc_4,genotype_pc_5,genotype_pc_6,genotype_pc_7,genotype_pc_8,genotype_pc_9,genotype_pc_10"
threads=16
maf=0.01

# Echo each command to console.
#set -x
# Suppress echo each command to console.
set +x

# Determine whether the temporary directory structure already exists.
if [ ! -d $path_report ]; then
    # Directory does not already exist.
    # Create directory.
    mkdir -p $path_report
fi

# Submit array batch to Sun Grid Engine.
# Array batch indices cannot start at zero.
echo "----------------------------------------------------------------------"
echo "Submit array batch to Sun Grid Engine."
echo "----------------------------------------------------------------------"
qsub -t 1-${count}:1 \
-o "$path_report/out.txt" -e "$path_report/error.txt" \
$path_scripts/run_gwas.sh \
$path_table_phenotypes_covariates \
$path_report \
$analysis \
$phenotypes \
$covariates \
$threads \
$maf \
