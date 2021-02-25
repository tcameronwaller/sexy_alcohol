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

# Organize variables.
table_name=$1 # name of file with phenotypes and covariates
cohort_comparison=$2 # name of cohort and comparison
hormone=$3 # name of hormone
covariates=$4 # covariates for GWAS
path_scripts=$5 # path to directory with relevant scripts
path_dock=$6 # path to directory for GWAS summary statistics

# Organize paths and parameters.
path_table_phenotypes_covariates="$path_dock/organization/cohorts/${table_name}"
path_gwas="$path_dock/gwas"
path_gwas_hormone="$path_gwas/$cohort_comparison"

phenotypes_hormone=$hormone

# General parameters.
threads=32 # 32, needs to match the "pe threaded" argument to scheduler
maf=0.01
chromosomes=22 # 22 # Count of chromosomes on which to run GWAS

# Echo each command to console.
#set -x
# Suppress echo each command to console.
set +x

# Initialize directories.
rm -r $path_gwas_hormone
if [ ! -d $path_gwas_hormone ]; then
    # Directory does not already exist.
    # Create directory.
    mkdir -p $path_gwas_hormone
fi

# Submit array batch to Sun Grid Engine.
# Array batch indices cannot start at zero.
echo "----------------------------------------------------------------------"
echo "Submit array batch to Sun Grid Engine."
echo "----------------------------------------------------------------------"
qsub -t 1-${chromosomes}:1 \
-o "$path_gwas_hormone/out.txt" -e "$path_gwas_hormone/error.txt" \
$path_scripts/3_run_gwas.sh \
$path_table_phenotypes_covariates \
$path_gwas_hormone \
$cohort_comparison \
$phenotypes_hormone \
$covariates \
$threads \
$maf \
