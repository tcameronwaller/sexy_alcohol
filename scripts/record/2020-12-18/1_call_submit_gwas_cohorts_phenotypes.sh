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
path_temporary=$(<"./temporary_sexy_alcohol.txt")
path_waller="$path_temporary/waller"
path_scripts="$path_waller/sexy_alcohol/scripts/record/2020-12-18"
path_dock="$path_temporary/waller/dock"
path_gwas="$path_dock/gwas"

# Initialize directories.
#rm -r $path_gwas
if [ ! -d $path_gwas ]; then
    # Directory does not already exist.
    # Create directory.
    mkdir -p $path_gwas
fi

if false; then
  # Jobs: 1958101, 1958102
  # Parameters.
  sex="female"
  alcoholism="alcoholism_1"
  hormone="testosterone"
  /usr/bin/bash "$path_scripts/2_submit_gwas_cohorts_phenotypes.sh" \
  $sex \
  $alcoholism \
  $hormone \
  $path_scripts \
  $path_dock

  # Jobs: 1958108, 1958109
  # Parameters.
  sex="female"
  alcoholism="alcoholism_2"
  hormone="testosterone"
  /usr/bin/bash "$path_scripts/2_submit_gwas_cohorts_phenotypes.sh" \
  $sex \
  $alcoholism \
  $hormone \
  $path_scripts \
  $path_dock

  # Jobs: 1958182, 1958183
  # Parameters.
  sex="female"
  alcoholism="alcoholism_3"
  hormone="testosterone"
  /usr/bin/bash "$path_scripts/2_submit_gwas_cohorts_phenotypes.sh" \
  $sex \
  $alcoholism \
  $hormone \
  $path_scripts \
  $path_dock

  # Jobs: 1958184, 1958185
  # Parameters.
  sex="female"
  alcoholism="alcoholism_4"
  hormone="testosterone"
  /usr/bin/bash "$path_scripts/2_submit_gwas_cohorts_phenotypes.sh" \
  $sex \
  $alcoholism \
  $hormone \
  $path_scripts \
  $path_dock

  # Jobs: 1958186, 1958187
  # Parameters.
  sex="male"
  alcoholism="alcoholism_1"
  hormone="testosterone"
  /usr/bin/bash "$path_scripts/2_submit_gwas_cohorts_phenotypes.sh" \
  $sex \
  $alcoholism \
  $hormone \
  $path_scripts \
  $path_dock

  # Jobs: 1958259, 1958260
  # Parameters.
  sex="male"
  alcoholism="alcoholism_2"
  hormone="testosterone"
  /usr/bin/bash "$path_scripts/2_submit_gwas_cohorts_phenotypes.sh" \
  $sex \
  $alcoholism \
  $hormone \
  $path_scripts \
  $path_dock

  # Jobs: 1958261, 1958262
  # Parameters.
  sex="male"
  alcoholism="alcoholism_3"
  hormone="testosterone"
  /usr/bin/bash "$path_scripts/2_submit_gwas_cohorts_phenotypes.sh" \
  $sex \
  $alcoholism \
  $hormone \
  $path_scripts \
  $path_dock

fi

if true; then

  # Jobs: 1959146, 1959147
  # Parameters.
  sex="male"
  alcoholism="alcoholism_4"
  hormone="testosterone"
  /usr/bin/bash "$path_scripts/2_submit_gwas_cohorts_phenotypes.sh" \
  $sex \
  $alcoholism \
  $hormone \
  $path_scripts \
  $path_dock

fi
