#!/bin/bash

###########################################################################
###########################################################################
###########################################################################
# ...
###########################################################################
###########################################################################
###########################################################################

################################################################################
# Organize paths.
# Read private, local file paths.
cd ~/paths

path_process=$(<"./process_sexy_alcohol.txt")
path_dock="$path_process/dock"

path_scripts_record="$path_process/sexy_alcohol/scripts/record/2021-07-21"

# General paths.
path_gwas_source_container="${path_dock}/gwas_complete/cohorts_models"
path_gwas_target_container="${path_dock}/test/gwas"

################################################################################
# Define array of studies.
studies=()
studies+=("female_steroid_globulin_log")
studies+=("male_steroid_globulin_log")


for study in "${studies[@]}"; do
  # Concatenate GWAS across chromosomes.
  /usr/bin/bash "${path_scripts_record}/8_drive_gwas_concatenation_format_munge_heritability.sh" \
  $study \
  $path_gwas_source_container \
  $path_gwas_target_container
done
