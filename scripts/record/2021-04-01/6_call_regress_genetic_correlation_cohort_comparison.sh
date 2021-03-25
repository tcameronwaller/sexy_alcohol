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
path_scripts="$path_waller/sexy_alcohol/scripts/record/2021-02-25"

path_gwas="$path_temporary/waller/dock/gwas"
path_genetic_correlation="$path_temporary/waller/dock/genetic_correlation"
path_access="$path_temporary/waller/dock/genetic_correlation/access"
path_disequilibrium="$path_access/disequilibrium"
path_baseline="$path_access/baseline"
path_weights="$path_access/weights"
path_frequencies="$path_access/frequencies"
path_alleles="$path_access/alleles"

path_gwas_alcohol_format_directory="$path_temporary/waller/dock/gwas/female_male_alcoholism_pgc"
path_gwas_alcoholism="$path_gwas_alcohol_format_directory/gwas_format_pgc_alcoholism.txt.gz"

###########################################################################
# Execute procedure.
###########################################################################

# Echo each command to console.
#set -x
# Suppress echo each command to console.
set +x

###########################################################################
# ...

# alcoholism_female_male_oestradiol
# alcoholism_female_oestradiol
# alcoholism_female_premenopause_oestradiol
# alcoholism_female_postmenopause_oestradiol
# alcoholism_male_oestradiol

if true; then

  # observation: error (chi-square too small)
  # Parameters.
  cohort_comparison="alcoholism_female_postmenopause_oestradiol"
  hormone="oestradiol_log" # name of original phenotype variable
  type_regression_hormone="linear"
  path_gwas_hormone="$path_gwas/female_postmenopause_oestradiol"
  /usr/bin/bash "$path_scripts/7_regress_genetic_correlation_cohort_comparison.sh" \
  $cohort_comparison \
  $hormone \
  $type_regression_hormone \
  $path_gwas_hormone \
  $path_gwas_alcoholism\
  $path_genetic_correlation \
  $path_scripts \
  $path_ldsc \
  $path_alleles \
  $path_disequilibrium

  # Parameters.
  cohort_comparison="alcoholism_female_postmenopause_testosterone"
  hormone="testosterone_log" # name of original phenotype variable
  type_regression_hormone="linear"
  path_gwas_hormone="$path_gwas/female_postmenopause_testosterone"
  /usr/bin/bash "$path_scripts/7_regress_genetic_correlation_cohort_comparison.sh" \
  $cohort_comparison \
  $hormone \
  $type_regression_hormone \
  $path_gwas_hormone \
  $path_gwas_alcoholism\
  $path_genetic_correlation \
  $path_scripts \
  $path_ldsc \
  $path_alleles \
  $path_disequilibrium

  # Parameters.
  cohort_comparison="alcoholism_female_postmenopause_steroid_globulin"
  hormone="steroid_globulin_log" # name of original phenotype variable
  type_regression_hormone="linear"
  path_gwas_hormone="$path_gwas/female_postmenopause_steroid_globulin"
  /usr/bin/bash "$path_scripts/7_regress_genetic_correlation_cohort_comparison.sh" \
  $cohort_comparison \
  $hormone \
  $type_regression_hormone \
  $path_gwas_hormone \
  $path_gwas_alcoholism\
  $path_genetic_correlation \
  $path_scripts \
  $path_ldsc \
  $path_alleles \
  $path_disequilibrium

  # Parameters.
  cohort_comparison="alcoholism_female_postmenopause_albumin"
  hormone="albumin_log" # name of original phenotype variable
  type_regression_hormone="linear"
  path_gwas_hormone="$path_gwas/female_postmenopause_albumin"
  /usr/bin/bash "$path_scripts/7_regress_genetic_correlation_cohort_comparison.sh" \
  $cohort_comparison \
  $hormone \
  $type_regression_hormone \
  $path_gwas_hormone \
  $path_gwas_alcoholism\
  $path_genetic_correlation \
  $path_scripts \
  $path_ldsc \
  $path_alleles \
  $path_disequilibrium

fi
