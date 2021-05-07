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
phenotype_studies+=("30482948_walters_2018_eur")
phenotype_studies+=("30482948_walters_2018_eur_unrel")

# TODO: create the genetic_correlation_comparison directory in the next script for individual cohort-hormone

# Organize information in format for LDSC.
for phenotype_study in "${phenotype_studies[@]}"; do
  # Organize paths.
  path_gwas_phenotype="${path_gwas}/${phenotype_study}"
  path_gwas_phenotype_format_compress="${path_gwas_phenotype}/gwas_format.txt.gz"
  path_gwas_phenotype_munge_suffix="${path_gwas_phenotype}/gwas_munge.sumstats.gz"

  #path_genetic_correlation_comparison="${path_genetic_correlation}/${phenotype_study}/${metabolite_study}"
  # Initialize directories.
  #rm -r $path_genetic_correlation_comparison
  #mkdir -p $path_genetic_correlation_comparison

  # Organize variables.
  file_gwas_cohorts_hormones_munge_suffix="gwas_munge.sumstats.gz"
  report="true" # "true" or "false"
  /usr/bin/bash "${path_scripts_record}/8_organize_phenotype_cohorts_hormones_correlations.sh" \
  $phenotype_study \
  $path_gwas_phenotype \
  $path_gwas_phenotype_munge_suffix \
  $path_gwas_cohorts_hormones \
  $file_gwas_cohorts_hormones_munge_suffix \
  $path_genetic_reference \
  $path_promiscuity_scripts \
  $path_scripts_record \
  $path_ldsc \
  $report
done

# Define specific pairs for genetic correlation.

pairs=()
pairs+=("female_premenopause_ordinal_testosterone_log;female_postmenopause_ordinal_testosterone_log")
pairs+=("female_premenopause_ordinal_testosterone_log;male_testosterone_log")
pairs+=("female_postmenopause_ordinal_testosterone_log;male_testosterone_log")

for pair in "${pairs[@]}"; do
  # Organize paths.
  # TODO: read the sub-arrays...
  echo "hello world"

  # Organize variables.
  file_gwas_cohorts_hormones_munge_suffix="gwas_munge.sumstats.gz"
  report="true" # "true" or "false"


  # TODO: now define the path to the GWAS munge suffix file for each "study"

  # TODO: now call the genetic correlation directly...

done
