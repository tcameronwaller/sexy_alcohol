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

#cohorts_models="cohorts_models_linear_measurement"          # 72 GWAS started at 19:21 on 7 September 2021
#cohorts_models="cohorts_models_linear_measurement_unadjust" # 72 GWAS started at 19:22 on 7 September 2021
#cohorts_models="cohorts_models_linear_imputation"           # 72 GWAS started at 19:37 on 7 September 2021
#cohorts_models="cohorts_models_linear_imputation_unadjust"  # 72 GWAS started at 19:39 on 7 September 2021

#cohorts_models="cohorts_models_linear_measurement"          # z-score coefficients 72 GWAS started at 23:05 on 8 September 2021
#cohorts_models="cohorts_models_linear_measurement_unadjust" # z-score coefficients 72 GWAS started at 23:38 on 8 September 2021
#cohorts_models="cohorts_models_linear_imputation"           # z-score coefficients 72 GWAS started at 23:40 on 8 September 2021
#cohorts_models="cohorts_models_linear_imputation_unadjust"  # z-score coefficients 72 GWAS started at 23:42 on 8 September 2021

#cohorts_models="cohorts_models_linear_order"
#cohorts_models="cohorts_models_linear_order_unadjust"
#cohorts_models="cohorts_models_logistic_detection"
#cohorts_models="cohorts_models_logistic_detection_unadjust"

pattern_gwas_report_file="report.*.glm.linear" # do not expand with full path yet
response="z_score" # "coefficient" unless "response_standard_scale" is "yes"
response_standard_scale="yes"

################################################################################
# Organize paths.
# Read private, local file paths.
cd ~/paths
path_process=$(<"./process_sexy_alcohol.txt")
path_dock="$path_process/dock"

path_gwas_source_container="${path_dock}/gwas/${cohorts_models}" # selection
path_gwas_target_container="${path_dock}/gwas_process/${cohorts_models}_z" # selection ... notice appended "_z"
path_heritability_container="${path_dock}/heritability/${cohorts_models}_z" # selection ... notice appended "_z"

path_scripts_record="$path_process/sexy_alcohol/scripts/record/2021-08-26"
path_batch_instances="${path_gwas_target_container}/post_process_batch_instances.txt"

###########################################################################
# Define explicit inclusions and exclusions.
# Use inclusions to run procedure for a few specific cohort-hormone combinations that are missing from the set.
# Use exclusions to omit a few cohort-hormone combinations that are not complete yet.

#delimiter=" "
#IFS=${delimiter}
#exclusions=()
#exclusions+=("female_combination_unadjust_albumin_log")
#unset IFS

###########################################################################
# Execute procedure.

# Initialize batch instances.
#rm -r $path_gwas_target_container
mkdir -p $path_gwas_target_container
rm $path_batch_instances

# Iterate on directories for GWAS on cohorts and hormones.
pattern_gwas_concatenation_file="gwas_concatenation.txt.gz"
cd $path_gwas_source_container
for path_directory in `find . -maxdepth 1 -mindepth 1 -type d -not -name .`; do
  if [ -d "$path_directory" ]; then
    # Current content item is a directory.
    # Extract directory's base name.
    study="$(basename -- $path_directory)"
    #echo $directory
    # Determine whether directory contains valid GWAS summary statistics
    # across chromosomes.
    # Check for chromosome 22, assuming that all chromosomes completed
    # sequentially.
    matches_chromosome=$(find "${path_gwas_source_container}/${study}/chromosome_22" -name "$pattern_gwas_report_file")
    match_chromosome_file=${matches_chromosome[0]}
    if [[ -n $matches_chromosome && -f $match_chromosome_file ]]; then
      echo "----------"
      echo "----------"
      echo "----------"
      echo "Found chromosome-22 sum stats for: ${study}"
      echo $matches_chromosome
      echo "Found match file: ${match_chromosome_file}"
      # Determine whether target directory already contains a concatenation file.
      mkdir -p "${path_gwas_target_container}/${study}"
      matches_concatenation=$(find "${path_gwas_target_container}/${study}" -name "$pattern_gwas_concatenation_file")
      match_concatenation_file=${matches_concatenation[0]}
      if [[ -n $matches_concatenation && -f $match_concatenation_file ]]; then
        echo "-----"
        echo "Found GWAS concatenation for: ${study}"
        echo "Found match file: ${match_concatenation_file}"
      else
        echo "Study has chromosome GWAS summary statistics but no concatenation."
        echo $study >> $path_batch_instances
      fi
    fi
  fi
done

# Read batch instances.
readarray -t batch_instances < $path_batch_instances
batch_instances_count=${#batch_instances[@]}
echo "----------"
echo "count of batch instances: " $batch_instances_count
echo "first batch instance: " ${batch_instances[0]} # notice base-zero indexing
echo "last batch instance: " ${batch_instances[$batch_instances_count - 1]}

# Execute batch with grid scheduler.
if true; then
  # Submit array batch to Sun Grid Engine.
  # Array batch indices must start at one (not zero).
  qsub -t 1-${batch_instances_count}:1 -o \
  "${path_gwas_target_container}/post_process_out.txt" -e "${path_gwas_target_container}/post_process_error.txt" \
  "${path_scripts_record}/9_run_batch_jobs_gwas_concatenation_format_munge_heritability.sh" \
  $pattern_gwas_report_file \
  $response \
  $response_standard_scale \
  $path_batch_instances \
  $batch_instances_count \
  $path_gwas_source_container \
  $path_gwas_target_container \
  $path_heritability_container \
  $path_scripts_record
fi
