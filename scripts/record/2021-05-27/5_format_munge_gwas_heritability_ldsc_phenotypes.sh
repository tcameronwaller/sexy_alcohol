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
path_ldsc=$(<"./tools_ldsc.txt")
path_gwas_summaries=$(<"./gwas_summaries_waller_metabolism.txt")
path_process=$(<"./process_sexy_alcohol.txt")

path_promiscuity_scripts="${path_process}/promiscuity/scripts"
path_promiscuity_scripts_ldsc_heritability="${path_promiscuity_scripts}/ldsc_genetic_heritability_correlation"
path_scripts_format="${path_promiscuity_scripts}/format_gwas_ldsc"
#path_scripts_record="$path_process/psychiatric_metabolism/scripts/record/2021-05-04"

path_dock="$path_process/dock"
path_genetic_reference="${path_dock}/access/genetic_reference"
path_gwas="${path_dock}/gwas"
path_heritability="${path_dock}/heritability"

###########################################################################
# Execute procedure.

# Version check...

# Initialize directories.
#rm -r $path_gwas
rm -r $path_heritability
mkdir -p $path_gwas
mkdir -p $path_heritability

# Organize information about studies.

# Define multi-dimensional array of cohorts and covariates.
# Review:
# 3 May 2021: TCW reviewed study README's, confirmed source files, and confirmed format scripts

studies=()
studies+=("30482948_walters_2018_all;${path_gwas_summaries}/30482948_walters_2018/pgc_alcdep.discovery.aug2018_release.txt.gz")
studies+=("30482948_walters_2018_eur;${path_gwas_summaries}/30482948_walters_2018/pgc_alcdep.eur_discovery.aug2018_release.txt.gz")
studies+=("30482948_walters_2018_eur_unrel;${path_gwas_summaries}/30482948_walters_2018/pgc_alcdep.eur_unrelated.aug2018_release.txt.gz")

# Organize information in format for LDSC.
for study_details in "${studies[@]}"; do
  # Read information.
  IFS=";" read -r -a array <<< "${study_details}"
  study="${array[0]}"
  path_source_file="${array[1]}"
  # Organize paths.
  path_gwas_study="${path_gwas}/${study}"
  path_heritability_study="${path_heritability}/${study}"
  # Initialize directories.
  mkdir -p $path_gwas_study
  mkdir -p $path_heritability_study
  # Organize variables.
  name_prefix="null"
  path_script_gwas_format="${path_scripts_format}/format_gwas_ldsc_${study}.sh"
  report="true" # "true" or "false"
  /usr/bin/bash "$path_promiscuity_scripts_ldsc_heritability/format_munge_gwas_heritability_ldsc.sh" \
  $study \
  $name_prefix \
  $path_source_file \
  $path_genetic_reference \
  $path_gwas_study \
  $path_heritability_study \
  $path_script_gwas_format \
  $path_promiscuity_scripts \
  $path_ldsc \
  $report
done
