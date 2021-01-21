#!/bin/bash

#chmod u+x script.sh

###########################################################################
###########################################################################
###########################################################################
# This script organizes directories and iteration instances then submits
# script "regress_metabolite_heritability.sh" to the Sun Grid Engine.

# version check: 6

###########################################################################
###########################################################################
###########################################################################

# Organize paths.
# Read private, local file paths.
echo "read private file path variables and organize paths..."
cd ~/paths
path_temporary=$(<"./processing_sexy_alcohol.txt")
path_waller="$path_temporary/waller"
path_scripts="$path_waller/sexy_alcohol/scripts/record/2021-01-21"
path_dock="$path_temporary/waller/dock"
path_gwas="$path_dock/gwas"

# Initialize directories.
#rm -r $path_gwas
if [ ! -d $path_gwas ]; then
    # Directory does not already exist.
    # Create directory.
    mkdir -p $path_gwas
fi

# table_female_alcoholism-1_case_auditc_testosterone.tsv
# table_male_alcoholism-1_case_auditc_testosterone.tsv
# table_female_alcoholism-2_case_auditc_testosterone.tsv
# table_male_alcoholism-2_case_auditc_testosterone.tsv

# table_female_alcoholism-1_case_auditp_testosterone.tsv
# table_male_alcoholism-1_case_auditp_testosterone.tsv
# table_female_alcoholism-2_case_auditp_testosterone.tsv
# table_male_alcoholism-2_case_auditp_testosterone.tsv

if false; then

  # Jobs: 2841910, 2841911
  # Parameters.
  table_name="table_female_alcoholism-1_case_auditc_testosterone.tsv"
  cohort_comparison="female_alcoholism-1_case_auditc_testosterone"
  alcoholism="alcohol_auditc"
  hormone="testosterone"
  /usr/bin/bash "$path_scripts/2_submit_gwas_cohorts_phenotypes.sh" \
  $table_name \
  $cohort_comparison \
  $alcoholism \
  $hormone \
  $path_scripts \
  $path_dock

  # Jobs: 2841977, 2841978
  # Parameters.
  table_name="table_male_alcoholism-1_case_auditc_testosterone.tsv"
  cohort_comparison="male_alcoholism-1_case_auditc_testosterone"
  alcoholism="alcohol_auditc"
  hormone="testosterone"
  /usr/bin/bash "$path_scripts/2_submit_gwas_cohorts_phenotypes.sh" \
  $table_name \
  $cohort_comparison \
  $alcoholism \
  $hormone \
  $path_scripts \
  $path_dock

  # Jobs: 2841979, 2841980
  # Parameters.
  table_name="table_female_alcoholism-2_case_auditc_testosterone.tsv"
  cohort_comparison="female_alcoholism-2_case_auditc_testosterone"
  alcoholism="alcohol_auditc"
  hormone="testosterone"
  /usr/bin/bash "$path_scripts/2_submit_gwas_cohorts_phenotypes.sh" \
  $table_name \
  $cohort_comparison \
  $alcoholism \
  $hormone \
  $path_scripts \
  $path_dock

  # Jobs: 2841981, 2841982
  # Parameters.
  table_name="table_male_alcoholism-2_case_auditc_testosterone.tsv"
  cohort_comparison="male_alcoholism-2_case_auditc_testosterone"
  alcoholism="alcohol_auditc"
  hormone="testosterone"
  /usr/bin/bash "$path_scripts/2_submit_gwas_cohorts_phenotypes.sh" \
  $table_name \
  $cohort_comparison \
  $alcoholism \
  $hormone \
  $path_scripts \
  $path_dock


fi

if true; then

  # Jobs: 2842801, 2842802
  # Parameters.
  table_name="table_female_alcoholism-1_case_auditp_testosterone.tsv"
  cohort_comparison="female_alcoholism-1_case_auditp_testosterone"
  alcoholism="alcohol_auditp"
  hormone="testosterone"
  /usr/bin/bash "$path_scripts/2_submit_gwas_cohorts_phenotypes.sh" \
  $table_name \
  $cohort_comparison \
  $alcoholism \
  $hormone \
  $path_scripts \
  $path_dock

  # Jobs: 2842803, 2842804
  # Parameters.
  table_name="table_male_alcoholism-1_case_auditp_testosterone.tsv"
  cohort_comparison="male_alcoholism-1_case_auditp_testosterone"
  alcoholism="alcohol_auditp"
  hormone="testosterone"
  /usr/bin/bash "$path_scripts/2_submit_gwas_cohorts_phenotypes.sh" \
  $table_name \
  $cohort_comparison \
  $alcoholism \
  $hormone \
  $path_scripts \
  $path_dock

  # Jobs: 2842805, 2842806
  # Parameters.
  table_name="table_female_alcoholism-2_case_auditp_testosterone.tsv"
  cohort_comparison="female_alcoholism-2_case_auditp_testosterone"
  alcoholism="alcohol_auditp"
  hormone="testosterone"
  /usr/bin/bash "$path_scripts/2_submit_gwas_cohorts_phenotypes.sh" \
  $table_name \
  $cohort_comparison \
  $alcoholism \
  $hormone \
  $path_scripts \
  $path_dock

  # Jobs: 2842807, 2842808
  # Parameters.
  table_name="table_male_alcoholism-2_case_auditp_testosterone.tsv"
  cohort_comparison="male_alcoholism-2_case_auditp_testosterone"
  alcoholism="alcohol_auditp"
  hormone="testosterone"
  /usr/bin/bash "$path_scripts/2_submit_gwas_cohorts_phenotypes.sh" \
  $table_name \
  $cohort_comparison \
  $alcoholism \
  $hormone \
  $path_scripts \
  $path_dock

fi
