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
path_scripts="$path_waller/sexy_alcohol/scripts/record/2021-02-25"
path_dock="$path_temporary/waller/dock"
path_gwas="$path_dock/gwas"

# Initialize directories.
#rm -r $path_gwas
if [ ! -d $path_gwas ]; then
    # Directory does not already exist.
    # Create directory.
    mkdir -p $path_gwas
fi

# TODO: pass a variable with names of columns to include as covariates in each GWAS!!!

# Covariates: sex, age, body_mass_index_log

# table_female_male_oestradiol.tsv ... "oestradiol_log"
# table_female_male_testosterone.tsv ... "testosterone_log"
# table_female_male_steroid_globulin.tsv ... "steroid_globulin_log"
# table_female_male_albumin.tsv ... "albumin_log"

if false; then

  # Jobs: ___, ___
  # Parameters.
  table_name="table_female_alcoholism-1_albumin.tsv"
  cohort_comparison="female_alcoholism-1_albumin"
  alcoholism="alcoholism_1"
  hormone="albumin"
  /usr/bin/bash "$path_scripts/2_submit_gwas_cohorts_phenotypes.sh" \
  $table_name \
  $cohort_comparison \
  $alcoholism \
  $hormone \
  $path_scripts \
  $path_dock

fi

if true; then

  # Jobs: ___, ___
  # Parameters.
  table_name="table_male_alcoholism-1_albumin.tsv"
  cohort_comparison="male_alcoholism-1_albumin"
  alcoholism="alcoholism_1"
  hormone="albumin"
  /usr/bin/bash "$path_scripts/2_submit_gwas_cohorts_phenotypes.sh" \
  $table_name \
  $cohort_comparison \
  $alcoholism \
  $hormone \
  $path_scripts \
  $path_dock

fi
