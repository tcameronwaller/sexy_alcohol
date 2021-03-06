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
alcoholism=$3 # name of definition of alcoholism
hormone=$4 # name of hormone
path_scripts=$5 # path to directory with relevant scripts
path_dock=$6 # path to directory for GWAS summary statistics

# Organize paths and parameters.
path_table_phenotypes_covariates="$path_dock/organization/cohorts/${table_name}"
path_gwas="$path_dock/gwas"
path_gwas_alcoholism="$path_gwas/$cohort_comparison/$alcoholism"
path_gwas_hormone="$path_gwas/$cohort_comparison/$hormone"

phenotypes_alcoholism=$alcoholism
phenotypes_hormone=$hormone

# General parameters.
threads=32 # 32, needs to match the "pe threaded" argument to scheduler
maf=0.01
chromosomes=22 # 22 # Count of chromosomes on which to run GWAS
covariates="age,body_mass_index,genotype_pc_1,genotype_pc_2,genotype_pc_3,genotype_pc_4,genotype_pc_5,genotype_pc_6,genotype_pc_7,genotype_pc_8,genotype_pc_9,genotype_pc_10"

# Echo each command to console.
#set -x
# Suppress echo each command to console.
set +x

# Initialize directories.
rm -r $path_gwas_alcoholism
if [ ! -d $path_gwas_alcoholism ]; then
    # Directory does not already exist.
    # Create directory.
    mkdir -p $path_gwas_alcoholism
fi
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
-o "$path_gwas_alcoholism/out.txt" -e "$path_gwas_alcoholism/error.txt" \
$path_scripts/3_run_gwas.sh \
$path_table_phenotypes_covariates \
$path_gwas_alcoholism \
$cohort_comparison \
$phenotypes_alcoholism \
$covariates \
$threads \
$maf \

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
