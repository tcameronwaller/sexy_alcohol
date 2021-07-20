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
#studies+=("female_steroid_globulin_log")
studies+=("male_steroid_globulin_log")

for study in "${studies[@]}"; do
  ##############################################################################
  # Concatenation and format.
  # Paths.
  path_gwas_source_parent="${path_gwas_source_container}/${study}"
  path_gwas_target_parent="${path_gwas_target_container}/${study}"
  #rm -r $path_gwas_target_parent
  mkdir -p $path_gwas_target_parent
  # Scripts.
  path_promiscuity_scripts="${path_process}/promiscuity/scripts"

  ################################################################################
  # Paths.
  path_gwas_concatenation="${path_gwas_target_parent}/gwas_concatenation.txt"
  path_gwas_concatenation_compress="${path_gwas_target_parent}/gwas_concatenation.txt.gz"
  path_gwas_collection="${path_gwas_target_parent}/gwas_collection.txt"
  path_gwas_format="${path_gwas_target_parent}/gwas_format.txt"
  path_gwas_standard="${path_gwas_target_parent}/gwas_standard.txt"
  path_gwas_format_compress="${path_gwas_target_parent}/gwas_format.txt.gz"

  ################################################################################
  # Scripts.
  path_scripts_gwas_process="${path_promiscuity_scripts}/gwas_process"
  path_script_gwas_collect_concatenate="${path_scripts_gwas_process}/collect_concatenate_gwas_chromosomes.sh"
  path_script_gwas_format="${path_scripts_gwas_process}/format_gwas_ldsc/format_gwas_ldsc_plink_linear.sh"
  path_script_calculate_z_score="${path_scripts_gwas_process}/calculate_z_score_column_5_of_6.sh"

  ################################################################################
  # Concatenation across chromosomes
  report="true"
  if false; then
    pattern_source_file="report.*.glm.linear" # do not expand with full path yet
    chromosome_start=1
    chromosome_end=22
    /usr/bin/bash "$path_script_gwas_collect_concatenate" \
    $pattern_source_file \
    $path_gwas_source_parent \
    $chromosome_start \
    $chromosome_end \
    $path_gwas_concatenation \
    $path_gwas_concatenation_compress \
    $report
  fi

  ################################################################################
  # Format adaptation
  path_gwas_source=$path_gwas_concatenation_compress
  /usr/bin/bash "$path_script_gwas_format" \
  $path_gwas_source \
  $path_gwas_collection \
  $path_gwas_format \
  $path_gwas_standard \
  $path_gwas_format_compress \
  $path_script_calculate_z_score \
  $report
done
