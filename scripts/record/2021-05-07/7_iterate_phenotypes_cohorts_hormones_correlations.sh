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
path_process=$(<"./process_sexy_alcohol.txt")

path_promiscuity_scripts="${path_process}/promiscuity/scripts"
path_scripts_record="$path_process/psychiatric_metabolism/scripts/record/2021-05-07"

path_dock="$path_process/dock"
path_genetic_reference="${path_dock}/access/genetic_reference"
path_gwas="${path_dock}/gwas"
path_gwas_cohorts_hormones="${path_gwas}/cohorts_hormones"
path_genetic_correlation="${path_dock}/genetic_correlation"

###########################################################################
# Execute procedure.

# Define main phenotype studies.
phenotype_studies=()
phenotype_studies+=("30482948_walters_2018_all")
#phenotype_studies+=("30482948_walters_2018_eur")
#phenotype_studies+=("30482948_walters_2018_eur_unrel")

file_gwas_cohorts_hormones_munge_suffix="gwas_munge.sumstats.gz"

# Organize information in format for LDSC.
for phenotype_study in "${phenotype_studies[@]}"; do
  # Organize paths.
  path_gwas_phenotype="${path_gwas}/${phenotype_study}"
  path_gwas_phenotype_format_compress="${path_gwas_phenotype}/gwas_format.txt.gz"
  path_gwas_phenotype_munge_suffix="${path_gwas_phenotype}/gwas_munge.sumstats.gz"

  # Organize variables.
  report="true" # "true" or "false"
  /usr/bin/bash "${path_scripts_record}/8_organize_phenotype_cohorts_hormones_correlations.sh" \
  $phenotype_study \
  $path_gwas_phenotype \
  $path_gwas_phenotype_munge_suffix \
  $path_gwas_cohorts_hormones \
  $file_gwas_cohorts_hormones_munge_suffix \
  $path_genetic_correlation \
  $path_genetic_reference \
  $path_promiscuity_scripts \
  $path_scripts_record \
  $path_ldsc \
  $report
done

# Define specific pairs for genetic correlation.
if false; then
  pairs=()
  pairs+=("female_premenopause_ordinal_testosterone_log;female_postmenopause_ordinal_testosterone_log")
  pairs+=("female_premenopause_ordinal_testosterone_log;male_testosterone_log")
  pairs+=("female_postmenopause_ordinal_testosterone_log;male_testosterone_log")

  for pair in "${pairs[@]}"; do
    # Read information.
    IFS=";" read -r -a array <<< "${pair}"
    study_one="${array[0]}"
    study_two="${array[1]}"
    # Organize paths.
    path_gwas_one_munge_suffix="${path_gwas_cohorts_hormones}/${study_one}/${file_gwas_cohorts_hormones_munge_suffix}"
    path_gwas_two_munge_suffix="${path_gwas_cohorts_hormones}/${study_two}/${file_gwas_cohorts_hormones_munge_suffix}"

    # Organize paths.
    path_genetic_correlation_comparison="${path_genetic_correlation}/${study_one}/${study_two}"
    path_genetic_correlation_report="${path_genetic_correlation_comparison}/correlation"
    path_genetic_correlation_report_suffix="${path_genetic_correlation_report}.log"
    # Initialize directories.
    rm -r $path_genetic_correlation_comparison
    mkdir -p $path_genetic_correlation_comparison
    # Estimate genetic correlation in LDSC.
    $path_ldsc/ldsc.py \
    --rg $path_gwas_one_munge_suffix,$path_gwas_two_munge_suffix \
    --ref-ld-chr $path_disequilibrium/eur_w_ld_chr/ \
    --w-ld-chr $path_disequilibrium/eur_w_ld_chr/ \
    --out $path_genetic_correlation_report
  done
fi
