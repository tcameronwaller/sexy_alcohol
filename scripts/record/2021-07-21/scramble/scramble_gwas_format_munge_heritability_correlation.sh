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

path_dock="$path_process/dock"
path_genetic_reference="${path_dock}/access/genetic_reference"
path_alleles="$path_genetic_reference/alleles"
path_disequilibrium="$path_genetic_reference/disequilibrium"
path_baseline="$path_genetic_reference/baseline"
path_weights="$path_genetic_reference/weights"
path_frequencies="$path_genetic_reference/frequencies"

path_gwas="${path_dock}/gwas"
path_gwas_source_parent="${path_dock}/gwas_complete/cohorts_models" # selection

path_scramble="${path_dock}/scramble"
path_gwas_target_parent="${path_scramble}/gwas"
path_heritability_parent="${path_scramble}/heritability"
path_correlation_parent="${path_scramble}/correlation"

path_scripts_record="$path_process/sexy_alcohol/scripts/record/2021-07-21"
path_promiscuity_scripts="${path_process}/promiscuity/scripts"

# Initialize directories.
rm -r $path_gwas_target_parent
rm -r $path_heritability_parent
rm -r $path_correlation_parent
mkdir -p $path_gwas_target_parent
mkdir -p $path_heritability_parent
mkdir -p $path_correlation_parent

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
  ###########################################################################
  # Execute procedure.

  path_target_gwas_study="${path_gwas_target_parent}/${cohort_model_phenotype}"
  path_heritability_study="${path_heritability_parent}/${cohort_model_phenotype}"
  path_correlation_comparison="${path_correlation_parent}/${phenotype_study}/${cohort_model_phenotype}"
  # Initialize directories.
  mkdir -p $path_target_gwas_study
  mkdir -p $path_heritability_study
  mkdir -p $path_correlation_comparison

  # Concatenate GWAS across chromosomes.
  if true; then
    # Organize variables.
    pattern_source_file="report.*.glm.linear" # do not expand with full path yet
    path_source_directory="${path_gwas_source_parent}/${cohort_model_phenotype}"
    chromosome_start=1
    chromosome_end=22
    path_gwas_concatenation="${path_target_gwas_study}/gwas_concatenation.txt"
    path_gwas_concatenation_compress="${path_target_gwas_study}/gwas_concatenation.txt.gz"
    /usr/bin/bash "$path_script_gwas_collect_concatenate" \
    $pattern_source_file \
    $path_source_directory \
    $chromosome_start \
    $chromosome_end \
    $path_gwas_concatenation \
    $path_gwas_concatenation_compress \
    $report
  fi

  # Format and munge GWAS summary statistics.
  if true; then
    # Organize information in format for LDSC.
    # Parameters.
    study=${cohort_model_phenotype}
    path_source_file="${path_target_gwas_study}/gwas_concatenation.txt.gz"
    path_gwas_collection="${path_target_gwas_study}/gwas_collection.txt"
    path_gwas_format="${path_target_gwas_study}/gwas_format.txt"
    path_gwas_format_compress="${path_gwas_format}.gz"
    report="true" # "true" or "false"
    /usr/bin/bash "$path_script_gwas_format" \
    $study \
    $path_source_file \
    $path_gwas_collection \
    $path_gwas_format \
    $path_gwas_format_compress \
    $path_promiscuity_scripts \
    $report
  fi

  ################################################################################
  # Activate Virtual Environment.
  # Read private, local file paths.
  #echo "read private file path variables and organize paths..."
  cd ~/paths
  path_tools=$(<"./waller_tools.txt")
  path_environment_ldsc="${path_tools}/python/environments/ldsc"
  source "${path_environment_ldsc}/bin/activate"
  echo "confirm Python Virtual Environment path..."
  which python2
  sleep 5s

  # Munge GWAS summary statistics.
  if true; then
    path_gwas_format="${path_target_gwas_study}/gwas_format.txt"
    path_gwas_format_compress="${path_gwas_format}.gz"
    path_gwas_munge="${path_target_gwas_study}/gwas_munge"
    path_gwas_munge_suffix="${path_gwas_munge}.sumstats.gz"
    path_gwas_munge_log="${path_gwas_munge}.log"
    # Munge GWAS summary statistics for use in LDSC.
    rm $path_gwas_munge_suffix
    rm $path_gwas_munge_log
    $path_ldsc/munge_sumstats.py \
    --sumstats $path_gwas_format_compress \
    --out $path_gwas_munge \
    --merge-alleles $path_alleles/w_hm3.snplist
  fi

  # Estimate genotype heritability.
  if true; then
    path_gwas_munge="${path_target_gwas_study}/gwas_munge"
    path_gwas_munge_suffix="${path_gwas_munge}.sumstats.gz"
    path_heritability_report="${path_heritability_study}/heritability_report"
    path_heritability_report_suffix="${path_heritability_report}.log"
    # Heritability.
    $path_ldsc/ldsc.py \
    --h2 $path_gwas_munge_suffix \
    --ref-ld-chr $path_disequilibrium/eur_w_ld_chr/ \
    --w-ld-chr $path_disequilibrium/eur_w_ld_chr/ \
    --out $path_heritability_report
  fi

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

  ################################################################################
  # Deactivate Virtual Environment.
  echo "confirm deactivation of Python Virtual Environment..."
  deactivate
  which python2

done
