#!/bin/bash

# Organize variables.
sex=$1 # name of sex
alcoholism=$2 # name of definition of alcoholism
hormone=$3 # name of hormone
path_genetic_correlation=$4 # path to directory for genetic correlations
path_gwas_scripts=$5 # path to directory with utility scripts for GWAS
path_correlation_scripts=$6 # path to directory with utility scripts for genetic correlation
path_ldsc=$7 # path to LDSC
path_alleles=$8 # path to reference for alleles
path_disequilibrium=$9 # path to reference for linkage disequilibrium

cohort_comparison="${sex}_${alcoholism}_${hormone}"

# Paths to GWAS summary statistics.
path_gwas_alcoholism="$path_temporary/waller/dock/gwas/$cohort_comparison/$alcoholism"
path_gwas_hormone="$path_temporary/waller/dock/gwas/$cohort_comparison/$hormone"

# Paths for organization and genetic correlation.
path_cohort_comparison="$path_temporary/waller/dock/genetic_correlation/$cohort_comparison"
path_munge="$path_temporary/waller/dock/genetic_correlation/$cohort_comparison/munge"

###########################################################################
# Organize directories.

rm -r $path_cohort_comparison

# Determine whether the temporary directory structure already exists.
if [ ! -d $path_cohort_comparison ]; then
    # Directory does not already exist.
    # Create directory.
    mkdir -p $path_cohort_comparison
    mkdir -p $path_munge
fi

###########################################################################
# Execute procedure.
###########################################################################

# Echo each command to console.
#set -x
# Suppress echo each command to console.
set +x

###########################################################################
# Organize GWAS summary statistics for LDSC.

# Access phenotype variables and auxiliary information from UKBiobank.
/usr/bin/bash "$path_gwas_scripts/concatenate_organize_gwas_ldsc.sh" \
$path_gwas_alcoholism \
"report" \
$alcoholism \
22 \

# Access phenotype variables and auxiliary information from UKBiobank.
/usr/bin/bash "$path_gwas_scripts/concatenate_organize_gwas_ldsc.sh" \
$path_gwas_hormone \
"report" \
$hormone \
22 \

###########################################################################
# Munge GWAS summary statistics for LDSC.

path_gwas_alcoholism_concatenation="$path_gwas_alcoholism/concatenation.${alcoholism}.glm.linear"
path_gwas_hormone_concatenation="$path_gwas_hormone/concatenation.${hormone}.glm.linear"

/usr/bin/bash "$path_correlation_scripts/munge_gwas_genetic_correlation_ldsc.sh" \
$path_gwas_alcoholism_concatenation \
$path_gwas_hormone_concatenation \
$path_munge \
$path_cohort_comparison \
$alcoholism \
$hormone \
$path_alleles \
$path_disequilibrium \
$path_ldsc
