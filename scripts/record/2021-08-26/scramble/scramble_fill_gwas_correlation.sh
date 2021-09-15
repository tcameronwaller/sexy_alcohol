#!/bin/bash

###########################################################################
###########################################################################
###########################################################################
# ...
###########################################################################
###########################################################################
###########################################################################

################################################################################
# General parameters.

cohorts_models="cohorts_models_linear_measurement" # 8 September 2021
#cohorts_models="cohorts_models_linear_measurement_unadjust"
#cohorts_models="cohorts_models_linear_imputation"
#cohorts_models="cohorts_models_linear_imputation_unadjust"

name_gwas_munge_file="gwas_munge.sumstats.gz"

study="male_age_high_testosterone_bioavailable_log"

################################################################################
# Organize paths.
# Read private, local file paths.
cd ~/paths
path_process=$(<"./process_sexy_alcohol.txt")
path_dock="$path_process/dock"

path_gwas_source_container="${path_dock}/gwas_process/${cohorts_models}"

###########################################################################
# Define main comparisons.

# Define array of primary studies.
primaries=()
primaries+=("30482948_walters_2018_eur_unrel;${path_dock}/gwas_process/30482948_walters_2018_eur_unrel/${name_gwas_munge_file}")
###primaries+=("30482948_walters_2018_female;${path_dock}/gwas_process/30482948_walters_2018_female/${name_gwas_munge_file}") # heritability < 0
primaries+=("30482948_walters_2018_male;${path_dock}/gwas_process/30482948_walters_2018_male/${name_gwas_munge_file}")
primaries+=("34002096_mullins_2021_all;${path_dock}/gwas_process/34002096_mullins_2021_all/${name_gwas_munge_file}")
primaries+=("34002096_mullins_2021_bpd1;${path_dock}/gwas_process/34002096_mullins_2021_bpd1/${name_gwas_munge_file}")
primaries+=("34002096_mullins_2021_bpd2;${path_dock}/gwas_process/34002096_mullins_2021_bpd2/${name_gwas_munge_file}")

# Define array of secondary studies.
secondaries=()
secondaries+=("$study;${path_gwas_source_container}/${study}/${name_gwas_munge_file}")

# Assemble array of batch instance details.
comparisons=()
for primary in "${primaries[@]}"; do
  for secondary in "${secondaries[@]}"; do
    comparisons+=("${primary};${secondary}")
  done
done

################################################################################
# Drive genetic correlations across comparisons.
# Format for array of comparisons.
# "study_primary;path_gwas_primary_munge_suffix;study_secondary;path_gwas_secondary_munge_suffix"

for comparison in "${comparisons[@]}"; do

  ##############################################################################
  # Extract details for comparison.
  IFS=";" read -r -a array <<< "${comparison}"
  study_primary="${array[0]}"
  path_gwas_primary_munge_suffix="${array[1]}"
  study_secondary="${array[2]}"
  path_gwas_secondary_munge_suffix="${array[3]}"
  echo "----------"
  echo "primary study: ${study_primary}"
  echo "path: ${path_gwas_primary_munge_suffix}"
  echo "secondary study: ${study_secondary}"
  echo "path: ${path_gwas_secondary_munge_suffix}"

  if true; then
    ##############################################################################
    # LDSC Genetic Correlation.
    # Paths.
    path_genetic_reference="${path_dock}/access/genetic_reference"
    #study_primary=""
    #study_secondary=""
    #path_gwas_primary_munge_suffix=""
    #path_gwas_secondary_munge_suffix=""
    path_genetic_correlation_parent="${path_dock}/genetic_correlation/${cohorts_models}/${study_primary}/${study_secondary}"
    rm -r $path_genetic_correlation_parent
    mkdir -p $path_genetic_correlation_parent
    # Scripts.
    path_promiscuity_scripts="${path_process}/promiscuity/scripts"
    path_scripts_gwas_process="${path_promiscuity_scripts}/gwas_process"
    path_script_drive_ldsc_gwas_genetic_correlation="${path_scripts_gwas_process}/drive_ldsc_gwas_genetic_correlation.sh"
    # Parameters.
    report="true" # "true" or "false"
    /usr/bin/bash "$path_script_drive_ldsc_gwas_genetic_correlation" \
    $path_gwas_primary_munge_suffix \
    $path_gwas_secondary_munge_suffix \
    $path_genetic_correlation_parent \
    $path_genetic_reference \
    $report
  fi
done
