#!/bin/bash

################################################################################
# Organize paths.
# Read private, local file paths.
echo "read private file path variables and organize paths..."
cd ~/paths
path_temporary=$(<"./processing_sexy_alcohol.txt")

path_waller="$path_temporary/waller"
path_sexy_alcohol="$path_waller/sexy_alcohol"
path_scripts_record="$path_waller/sexy_alcohol/scripts/record/2021-04-01"
path_promiscuity_scripts="$path_waller/promiscuity/scripts"

path_dock="$path_waller/dock"
path_genetic_reference="$path_dock/access/genetic_reference"
path_gwas="$path_dock/gwas"
path_heritability="$path_dock/heritability"
path_genetic_correlation="$path_dock/genetic_correlation"

###########################################################################
# Execute procedure.
###########################################################################

# Echo each command to console.
#set -x
# Suppress echo each command to console.
set +x

# Organize consistent parameters.
phenotype_study="30482948_walters_2018"
path_phenotype_gwas="${path_gwas}/${phenotype_study}"
regression_type="linear"

# Define multi-dimensional array of cohorts and hormones.
cohorts_hormones=()
cohorts_hormones+=( "female_male;oestradiol_log" "female_male;oestradiol_free_log")
cohorts_hormones+=( "female_male;testosterone_log" "female_male;testosterone_free_log")
cohorts_hormones+=( "female;oestradiol_log" "female;oestradiol_free_log")
cohorts_hormones+=( "female;testosterone_log" "female;testosterone_free_log")
cohorts_hormones+=( "female_premenopause;oestradiol_log" "female_premenopause;oestradiol_free_log")
cohorts_hormones+=( "female_premenopause;testosterone_log" "female_premenopause;testosterone_free_log")
cohorts_hormones+=( "female_postmenopause;oestradiol_log" "female_postmenopause;oestradiol_free_log")
cohorts_hormones+=( "female_postmenopause;testosterone_log" "female_postmenopause;testosterone_free_log")
cohorts_hormones+=( "male;oestradiol_log" "male;oestradiol_free_log")
cohorts_hormones+=( "male;testosterone_log" "male;testosterone_free_log")

for pair in "${cohorts_hormones[@]}"; do
  # Separate fields from pair.
  IFS=";" read -r -a array <<< "${pair}"
  cohort="${array[0]}"
  hormone="${array[1]}"
  cohort_hormone="${cohort}_${hormone}"
  echo ${cohort_hormone}
  path_study_gwas="${path_gwas}/${cohort_hormone}"
  path_source_directory=$path_study_gwas
  path_study_heritability="${path_heritability}/${cohort_hormone}"
  path_study_genetic_correlation="${path_genetic_correlation}/${phenotype_study}/${cohort_hormone}" # notice the directory structure for phenotype and metabolite studies
  report="true" # "true" or "false"
  /usr/bin/bash "$path_scripts_record/8_collect_format_heritability_correlation.sh" \
  $phenotype_study \
  $cohort_hormone \
  $hormone \
  $regression_type \
  $path_source_directory \
  $path_genetic_reference \
  $path_phenotype_gwas \
  $path_study_gwas \
  $path_study_heritability \
  $path_study_genetic_correlation \
  $path_scripts_record \
  $path_promiscuity_scripts \
  $report
done
