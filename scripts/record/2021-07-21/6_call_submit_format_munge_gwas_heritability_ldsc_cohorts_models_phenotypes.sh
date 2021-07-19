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
path_gwas_container="${path_dock}/gwas_complete/cohorts_models" # selection

path_scripts_record="$path_process/sexy_alcohol/scripts/record/2021-07-21"
path_promiscuity_scripts="${path_process}/promiscuity/scripts"

###########################################################################
# Define explicit inclusions and exclusions.
# Use inclusions to run procedure for a few specific cohort-hormone combinations that are missing from the set.
# Use exclusions to omit a few cohort-hormone combinations that are not complete yet.

delimiter=" "
IFS=${delimiter}
exclusions=()
#exclusions+=("female_combination_unadjust_albumin_log")
unset IFS

###########################################################################
# Execute procedure.

# Initialize batch instances.
path_batch_instances="${path_gwas_container}/batch_instances_post_process.txt"
rm $path_batch_instances

# Iterate on directories for GWAS on cohorts and hormones.
# Set "nullglob" option to expand null wildcard matches to empty list.
#shopt -s nullglob
pattern_gwas_chromosome_file="report.*.glm.linear" # do not expand with full path yet
pattern_gwas_concatenation_file="gwas_concatenation.txt.gz"
cd $path_gwas_container
for path_directory in `find . -maxdepth 1 -mindepth 1 -type d -not -name .`; do
  if [ -d "$path_directory" ]; then
    # Current content item is a directory.
    # Extract directory's base name.
    directory="$(basename -- $path_directory)"
    #echo $directory
    # Determine whether directory contains valid GWAS summary statistics
    # across chromosomes.
    # Check for chromosome 22, assuming that all chromosomes completed
    # sequentially.
    matches_chromosome=$(find "${path_gwas_container}/${directory}/chromosome_22" -name "$pattern_gwas_chromosome_file")
    match_chromosome_file=${matches_chromosome[0]}
    if [[ -n $matches_chromosome && -f $match_chromosome_file ]]; then
      echo "----------"
      echo "Found chromosome-22 sum stats for: ${directory}"
      echo $matches_chromosome
      echo "Found match file: ${match_chromosome_file}"
      # Determine whether directory already contains a concatenation file.
      matches_concatenation=$(find "${path_gwas_container}/${directory}" -name "$pattern_gwas_concatenation_file")
      match_concatenation_file=${matches_concatenation[0]}
      if [[ -n $matches_concatenation && -f $match_concatenation_file ]]; then
        echo "-----"
        echo "Found GWAS concatenation for: ${directory}"
        echo "Found match file: ${match_concatenation_file}"
        #echo $directory >> $path_batch_instances
    fi

  fi
done

if false; then
  # Read batch instances.
  readarray -t batch_instances < $path_batch_instances
  batch_instances_count=${#batch_instances[@]}
  echo "----------"
  echo "count of batch instances: " $batch_instances_count
  echo "first batch instance: " ${batch_instances[0]} # notice base-zero indexing
  echo "last batch instance: " ${batch_instances[batch_instances_count - 1]}
fi

# Execute batch with grid scheduler.
if false; then
  report="true" # "true" or "false"
  # Submit array batch to Sun Grid Engine.
  # Array batch indices must start at one (not zero).
  qsub -t 1-${batch_instances_count}:1 -o \
  "${path_gwas_parent}/out.txt" -e "${path_gwas_parent}/error.txt" \
  "${path_promiscuity_scripts}/run_plink_gwas_collection_format_munge_heritability.sh" \
  $path_batch_instances \
  $batch_instances_count \
  $path_gwas_parent \
  $path_heritability_parent \
  $path_genetic_reference \
  $path_promiscuity_scripts \
  $path_ldsc \
  $report
fi
