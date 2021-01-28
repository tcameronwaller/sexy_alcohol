#!/bin/bash

###########################################################################
# Organize general paths.
###########################################################################
# Read private, local file paths.
#echo "read private file path variables and organize paths..."
cd ~/paths
path_ldsc=$(<"./tools_ldsc.txt")

path_temporary=$(<"./processing_sexy_alcohol.txt")
path_waller="$path_temporary/waller"
path_dock="$path_temporary/waller/dock"
path_gwas_scripts="$path_waller/sexy_alcohol/scripts/record/2021-01-28"
path_correlation_scripts="$path_waller/sexy_alcohol/scripts/record/2021-01-28"

path_gwas="$path_temporary/waller/dock/gwas"
path_genetic_correlation="$path_temporary/waller/dock/genetic_correlation"

path_access="$path_temporary/waller/dock/genetic_correlation/access"
path_disequilibrium="$path_access/disequilibrium"
path_baseline="$path_access/baseline"
path_weights="$path_access/weights"
path_frequencies="$path_access/frequencies"
path_alleles="$path_access/alleles"

###########################################################################
# Organize directories.

# Genetic correlation directory should already exist and have reference
# information from access script.

# Determine whether the temporary directory structure already exists.
if [ ! -d $path_genetic_correlation ]; then
    # Directory does not already exist.
    # Create directory.
    mkdir -p $path_genetic_correlation
fi

###########################################################################
# Execute procedure.
###########################################################################

# Echo each command to console.
#set -x
# Suppress echo each command to console.
set +x

###########################################################################
# ...

# female_alcoholism-1_testosterone
# female_alcoholism-2_testosterone
# female_alcoholism-3_testosterone
# female_alcoholism-4_testosterone
# female_alcoholism-5_testosterone

# male_alcoholism-1_testosterone
# male_alcoholism-2_testosterone
# male_alcoholism-3_testosterone
# male_alcoholism-4_testosterone
# male_alcoholism-5_testosterone

if true; then
  # Parameters.
  cohort_comparison="female_alcoholism-1_testosterone"
  alcoholism="alcoholism_1"
  hormone="testosterone"
  /usr/bin/bash "$path_correlation_scripts/6_regress_genetic_correlation_sex_hormone.sh" \
  $cohort_comparison \
  $alcoholism \
  $hormone \
  "logistic" \
  "linear" \
  $path_gwas \
  $path_genetic_correlation \
  $path_gwas_scripts \
  $path_correlation_scripts \
  $path_ldsc \
  $path_alleles \
  $path_disequilibrium
fi
