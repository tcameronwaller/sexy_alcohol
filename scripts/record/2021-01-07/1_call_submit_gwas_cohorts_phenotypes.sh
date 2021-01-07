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
path_scripts="$path_waller/sexy_alcohol/scripts/record/2021-01-07"
path_dock="$path_temporary/waller/dock"
path_gwas="$path_dock/gwas"

# Initialize directories.
#rm -r $path_gwas
if [ ! -d $path_gwas ]; then
    # Directory does not already exist.
    # Create directory.
    mkdir -p $path_gwas
fi

#if false; then
#fi

if true; then

  # Jobs: 2336701.1-22:1, 2336702.1-22:1
  # Parameters.
  sex="female"
  alcoholism="alcohol_auditc"
  hormone="testosterone"
  /usr/bin/bash "$path_scripts/2_submit_gwas_cohorts_phenotypes.sh" \
  $sex \
  $alcoholism \
  $hormone \
  $path_scripts \
  $path_dock

  # Jobs: 2336703.1-22:1, 2336704.1-22:1
  # Parameters.
  sex="female"
  alcoholism="alcohol_audit"
  hormone="testosterone"
  /usr/bin/bash "$path_scripts/2_submit_gwas_cohorts_phenotypes.sh" \
  $sex \
  $alcoholism \
  $hormone \
  $path_scripts \
  $path_dock

  # Jobs: 2336705.1-22:1, 2336706.1-22:1
  # Parameters.
  sex="male"
  alcoholism="alcohol_auditc"
  hormone="testosterone"
  /usr/bin/bash "$path_scripts/2_submit_gwas_cohorts_phenotypes.sh" \
  $sex \
  $alcoholism \
  $hormone \
  $path_scripts \
  $path_dock

  # Jobs: 2336707.1-22:1, 2336708.1-22:1
  # Parameters.
  sex="male"
  alcoholism="alcohol_audit"
  hormone="testosterone"
  /usr/bin/bash "$path_scripts/2_submit_gwas_cohorts_phenotypes.sh" \
  $sex \
  $alcoholism \
  $hormone \
  $path_scripts \
  $path_dock

fi
