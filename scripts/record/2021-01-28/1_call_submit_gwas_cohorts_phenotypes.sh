#!/bin/bash

#chmod u+x script.sh

###########################################################################
###########################################################################
###########################################################################
# This script organizes directories and iteration instances then submits
# script "regress_metabolite_heritability.sh" to the Sun Grid Engine.

# version check: 1

###########################################################################
###########################################################################
###########################################################################

# Organize paths.
# Read private, local file paths.
echo "read private file path variables and organize paths..."
cd ~/paths
path_temporary=$(<"./processing_sexy_alcohol.txt")
path_waller="$path_temporary/waller"
path_scripts="$path_waller/sexy_alcohol/scripts/record/2021-01-28"
path_dock="$path_temporary/waller/dock"
path_gwas="$path_dock/gwas"

# Initialize directories.
#rm -r $path_gwas
if [ ! -d $path_gwas ]; then
    # Directory does not already exist.
    # Create directory.
    mkdir -p $path_gwas
fi

# table_female_alcoholism-1_testosterone.tsv
# table_female_alcoholism-2_testosterone.tsv
# table_female_alcoholism-3_testosterone.tsv
# table_female_alcoholism-4_testosterone.tsv
# table_female_alcoholism-5_testosterone.tsv

if false; then

  # Jobs: 3314662, 3314663
  # Parameters.
  table_name="table_female_alcoholism-1_testosterone.tsv"
  cohort_comparison="female_alcoholism-1_testosterone"
  alcoholism="alcoholism_1"
  hormone="testosterone"
  /usr/bin/bash "$path_scripts/2_submit_gwas_cohorts_phenotypes.sh" \
  $table_name \
  $cohort_comparison \
  $alcoholism \
  $hormone \
  $path_scripts \
  $path_dock

  # Jobs: 3314664, 3314665
  # Parameters.
  table_name="table_female_alcoholism-2_testosterone.tsv"
  cohort_comparison="female_alcoholism-2_testosterone"
  alcoholism="alcoholism_2"
  hormone="testosterone"
  /usr/bin/bash "$path_scripts/2_submit_gwas_cohorts_phenotypes.sh" \
  $table_name \
  $cohort_comparison \
  $alcoholism \
  $hormone \
  $path_scripts \
  $path_dock

  # Jobs: 3314666, 3314667
  # Parameters.
  table_name="table_female_alcoholism-3_testosterone.tsv"
  cohort_comparison="female_alcoholism-3_testosterone"
  alcoholism="alcoholism_3"
  hormone="testosterone"
  /usr/bin/bash "$path_scripts/2_submit_gwas_cohorts_phenotypes.sh" \
  $table_name \
  $cohort_comparison \
  $alcoholism \
  $hormone \
  $path_scripts \
  $path_dock

  # Jobs: 3314668, 3314669
  # Parameters.
  table_name="table_female_alcoholism-4_testosterone.tsv"
  cohort_comparison="female_alcoholism-4_testosterone"
  alcoholism="alcoholism_4"
  hormone="testosterone"
  /usr/bin/bash "$path_scripts/2_submit_gwas_cohorts_phenotypes.sh" \
  $table_name \
  $cohort_comparison \
  $alcoholism \
  $hormone \
  $path_scripts \
  $path_dock

  # Jobs: 3314671, 3314672
  # Parameters.
  table_name="table_female_alcoholism-5_testosterone.tsv"
  cohort_comparison="female_alcoholism-5_testosterone"
  alcoholism="alcoholism_5"
  hormone="testosterone"
  /usr/bin/bash "$path_scripts/2_submit_gwas_cohorts_phenotypes.sh" \
  $table_name \
  $cohort_comparison \
  $alcoholism \
  $hormone \
  $path_scripts \
  $path_dock

fi

# table_male_alcoholism-1_testosterone.tsv
# table_male_alcoholism-2_testosterone.tsv
# table_male_alcoholism-3_testosterone.tsv
# table_male_alcoholism-4_testosterone.tsv
# table_male_alcoholism-5_testosterone.tsv

if true; then

  # Jobs: ___, ___
  # Parameters.
  table_name="table_male_alcoholism-1_testosterone.tsv"
  cohort_comparison="male_alcoholism-1_testosterone"
  alcoholism="alcoholism_1"
  hormone="testosterone"
  /usr/bin/bash "$path_scripts/2_submit_gwas_cohorts_phenotypes.sh" \
  $table_name \
  $cohort_comparison \
  $alcoholism \
  $hormone \
  $path_scripts \
  $path_dock

  # Jobs: ___, ___
  # Parameters.
  table_name="table_male_alcoholism-2_testosterone.tsv"
  cohort_comparison="male_alcoholism-2_testosterone"
  alcoholism="alcoholism_2"
  hormone="testosterone"
  /usr/bin/bash "$path_scripts/2_submit_gwas_cohorts_phenotypes.sh" \
  $table_name \
  $cohort_comparison \
  $alcoholism \
  $hormone \
  $path_scripts \
  $path_dock

  # Jobs: ___, ___
  # Parameters.
  table_name="table_male_alcoholism-3_testosterone.tsv"
  cohort_comparison="male_alcoholism-3_testosterone"
  alcoholism="alcoholism_3"
  hormone="testosterone"
  /usr/bin/bash "$path_scripts/2_submit_gwas_cohorts_phenotypes.sh" \
  $table_name \
  $cohort_comparison \
  $alcoholism \
  $hormone \
  $path_scripts \
  $path_dock

  # Jobs: ___, ___
  # Parameters.
  table_name="table_male_alcoholism-4_testosterone.tsv"
  cohort_comparison="male_alcoholism-4_testosterone"
  alcoholism="alcoholism_4"
  hormone="testosterone"
  /usr/bin/bash "$path_scripts/2_submit_gwas_cohorts_phenotypes.sh" \
  $table_name \
  $cohort_comparison \
  $alcoholism \
  $hormone \
  $path_scripts \
  $path_dock

  # Jobs: ___, ___
  # Parameters.
  table_name="table_male_alcoholism-5_testosterone.tsv"
  cohort_comparison="male_alcoholism-5_testosterone"
  alcoholism="alcoholism_5"
  hormone="testosterone"
  /usr/bin/bash "$path_scripts/2_submit_gwas_cohorts_phenotypes.sh" \
  $table_name \
  $cohort_comparison \
  $alcoholism \
  $hormone \
  $path_scripts \
  $path_dock

fi
