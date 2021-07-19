#!/bin/bash

###########################################################################
###########################################################################
###########################################################################
# ...
###########################################################################
###########################################################################
###########################################################################



# need GWAS container
# need "study"

################################################################################
# Organize paths.
# Read private, local file paths.
cd ~/paths

path_process=$(<"./process_sexy_alcohol.txt")
path_dock="$path_process/dock"

path_correlation_parent="${path_scramble}/correlation"

path_scripts_record="$path_process/sexy_alcohol/scripts/record/2021-07-21"

# General paths.
path_gwas_source_container="${path_dock}/gwas_complete/cohorts_models"
path_gwas_target_container="${path_dock}/scramble/gwas"




###########################################################################
# Organize variables.
path_script_gwas_collect_concatenate="${path_promiscuity_scripts}/collect_concatenate_gwas_chromosomes.sh"
path_promiscuity_scripts_ldsc_heritability="${path_promiscuity_scripts}/ldsc_genetic_heritability_correlation"
path_script_format_munge_heritability="${path_promiscuity_scripts_ldsc_heritability}/format_munge_gwas_heritability_ldsc.sh"
path_scripts_format="${path_promiscuity_scripts}/format_gwas_ldsc"
path_script_gwas_format="${path_scripts_format}/format_gwas_ldsc_plink_linear.sh"

###########################################################################
# Execute procedure.


phenotype_study="30482948_walters_2018_eur_unrel"
path_gwas_phenotype="${path_gwas}/${phenotype_study}"
path_gwas_phenotype_format_compress="${path_gwas_phenotype}/gwas_format.txt.gz"
path_gwas_phenotype_munge_suffix="${path_gwas_phenotype}/gwas_munge.sumstats.gz"

cohorts_models_phenotypes=()
cohorts_models_phenotypes+=("female_premenopause_ordinal_testosterone_log")
cohorts_models_phenotypes+=("female_perimenopause_ordinal_testosterone_log")
cohorts_models_phenotypes+=("female_postmenopause_ordinal_testosterone_log")
cohorts_models_phenotypes+=("male_testosterone_log")

for cohort_model_phenotype in "${cohorts_models_phenotypes[@]}"; do


  # TODO: TCW (16 July 2021)
  # Put everything below into a new function script...
  # ... then I can call that for a specific cohort_model_phenotype ("secondary_phenotype") + main_phenotype



  ##############################################################################
  # Concatenation and format.
  # Paths.
  path_gwas_source_parent="${path_gwas_source_container}/${cohort_model_phenotype}"
  path_gwas_target_parent="${path_gwas_target_container}/${cohort_model_phenotype}"
  rm -r $path_gwas_target_parent
  mkdir -p $path_gwas_target_parent
  # Scripts.
  path_promiscuity_scripts="${path_process}/promiscuity/scripts"
  path_script_drive_gwas_concatenation_format="${path_promiscuity_scripts}/drive_gwas_concatenation_format.sh"
  # Parameters.
  report="true" # "true" or "false"
  /usr/bin/bash "$path_script_drive_gwas_concatenation_format" \
  $path_gwas_source_parent \
  $path_gwas_target_parent \
  $path_promiscuity_scripts \
  $report

  ##############################################################################
  # LDSC Munge and Heritability.
  # Paths.
  path_genetic_reference="${path_dock}/access/genetic_reference"
  path_gwas_source_parent="${path_gwas_target_container}/${cohort_model_phenotype}"
  path_gwas_target_parent="${path_gwas_target_container}/${cohort_model_phenotype}"
  path_heritability_parent="${path_dock}/heritability/${cohort_model_phenotype}"
  rm -r $path_heritability_parent
  mkdir -p $path_gwas_target_parent
  mkdir -p $path_heritability_parent
  # Scripts.
  path_script_drive_ldsc_gwas_munge_heritability="${path_promiscuity_scripts}/drive_ldsc_gwas_munge_heritability.sh"
  # Parameters.
  report="true" # "true" or "false"
  /usr/bin/bash "$path_script_drive_ldsc_gwas_munge_heritability" \
  $path_gwas_source_parent \
  $path_gwas_target_parent \
  $path_heritability_parent \
  $path_genetic_reference \
  $report

  ##############################################################################
  # LDSC Genetic Correlation.
  # Paths.
  study_primary=""
  study_secondary=""
  path_correlation_comparison="${path_dock}/genetic_correlation/${study_primary}/${study_secondary}"
  rm -r $path_correlation_comparison
  mkdir -p $path_correlation_comparison


  # TODO: write a new driver function for genetic correlation... keep it SIMPLE!



  # OLD STUFF scrap below here...

  # Genetic correlation.
  if true; then

    # Organize paths.

    path_gwas_munge="${path_target_gwas_study}/gwas_munge"
    path_gwas_munge_suffix="${path_gwas_munge}.sumstats.gz"

    path_gwas_one_munge_suffix=$path_gwas_phenotype_munge_suffix
    path_gwas_two_munge_suffix=$path_gwas_munge_suffix
    # Organize paths.
    path_genetic_correlation_report="${path_correlation_comparison}/correlation"
    path_genetic_correlation_report_suffix="${path_genetic_correlation_report}.log"
    # Estimate genetic correlation in LDSC.
    $path_ldsc/ldsc.py \
    --rg $path_gwas_one_munge_suffix,$path_gwas_two_munge_suffix \
    --ref-ld-chr $path_disequilibrium/eur_w_ld_chr/ \
    --w-ld-chr $path_disequilibrium/eur_w_ld_chr/ \
    --out $path_genetic_correlation_report

  fi

done
