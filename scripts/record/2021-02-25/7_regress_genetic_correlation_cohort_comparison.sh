#!/bin/bash

# Organize variables.
cohort_comparison=${1} # name of cohort and comparison
hormone=${2} # name of hormone
type_regression_hormone=${3} # type of regression for hormone, either "logistic" or "linear"
path_gwas_hormone=${4} # path to directory for GWAS summary statistics files for hormone
path_gwas_alcoholism=${5} # path to file of GWAS summary statistics for alcoholism in format
path_genetic_correlation=${6} # path to directory for genetic correlations
path_scripts=${7} # path to directory with relevant scripts
path_ldsc=${8} # path to LDSC
path_alleles=${9} # path to reference for alleles
path_disequilibrium=${10} # path to reference for linkage disequilibrium

# Paths for organization and genetic correlation.
path_cohort_comparison="$path_genetic_correlation/$cohort_comparison"
path_munge="$path_genetic_correlation/$cohort_comparison/munge"

###########################################################################
# Report progress.

echo "----------------------------------------------------------------------"
echo "----------------------------------------------------------------------"
echo "----------------------------------------------------------------------"
echo "Report from: 7_regress_genetic_correlation_sex_hormone.sh"
echo "cohort_comparison: ${cohort_comparison}"
echo "hormone: ${hormone}"
echo "----------------------------------------------------------------------"
echo "----------------------------------------------------------------------"
echo "----------------------------------------------------------------------"
echo ""
echo ""
echo ""

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
/usr/bin/bash "$path_scripts/8_concatenate_organize_gwas_ldsc.sh" \
$path_gwas_hormone \
"report" \
$hormone \
$type_regression_hormone \
22 \
$path_scripts \

###########################################################################
# Munge GWAS summary statistics for LDSC.

path_gwas_hormone_concatenation="$path_gwas_hormone/concatenation.${hormone}.glm.${type_hormone}"

/usr/bin/bash "$path_scripts/9_munge_gwas_genetic_correlation_ldsc.sh" \
$path_gwas_alcoholism \
$path_gwas_hormone_concatenation \
$path_munge \
$path_cohort_comparison \
"alcoholism" \
$hormone \
$path_alleles \
$path_disequilibrium \
$path_ldsc
