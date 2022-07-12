#!/bin/bash

################################################################################
################################################################################
################################################################################
# Note:
# This set of scripts concatenates across chromosomes the summary statistics
# from Genome-Wide Association Studies (GWAS) that T. Cameron Waller ran on data
# from the UK Biobank in scripts from record collection "2022-05-04".
# Before these scripts, T. Cameron Waller consolidated information from sets of
# GWAS that were originally separate for convenience in execution.
# For example, sets "albumin_linear_1" and "albumin_linear_2" consolidated to
# set "albumin_linear".
# Sets "oestradiol_logistic" and "oestradiol_logistic_long_rescue" consolidated
# to set "oestradiol_logistic".
# Sets "testosterone_logistic" and "testosterone_logistic_long_rescue"
# consolidated to set "testosterone_logistic".
################################################################################
################################################################################
################################################################################

# TODO: TCW; 11 July 2022
# TODO: ***1*** before anything else...
# TODO: I need to combine the chromosomes from "oestradiol_logistic" and "oestradiol_logistic_long_rescue"
# TODO: for both "female_joint_1..." and "male_joint_1..."
# TODO: Be careful... prioritize chromosome directories from the rescue that did not fail early

# TODO: TCW; 11 July 2022
# TODO: ***2*** move the "gwas_raw" directory over to the "sexy_alcohol" project processing space...

# TODO: TCW; 11 July 2022
# TODO: Maybe I could use a for-loop to drive creation and submission of the the multiple batch jobs
# TODO: maybe I only need 1 thread/slot on each node for the instance job

################################################################################
# General parameters.

# TODO: TCW; 12 July 2022
# TODO: execution plan
# TODO: Call each of these "sets" or "containers"
# TODO: define these names in an array
# TODO: iterate across "sets" before iterating along individual "studies"
# TODO: keep track of the name of the "set" and the "study" for each GWAS
# TODO: pass the "set" and "study" on to the next scripts

#cohorts_models="oestradiol_logistic"                # 18? GWAS; __ July 2022
#cohorts_models="oestradiol_linear"                  # 30? GWAS; __ July 2022
#cohorts_models="oestradiol_bioavailable_linear"     # 18 GWAS; __ July 2022
#cohorts_models="oestradiol_free_linear"             # 18 GWAS; __ July 2022
#cohorts_models="testosterone_logistic"              # 18? GWAS; __ July 2022
#cohorts_models="testosterone_linear"                # 54 GWAS; __ July 2022
#cohorts_models="testosterone_bioavailable_linear"   # 18 GWAS; __ July 2022
#cohorts_models="testosterone_free_linear"           # 18 GWAS; __ July 2022
#cohorts_models="steroid_globulin_linear"            # 20? GWAS; __ July 2022
#cohorts_models="albumin_linear"                     # 20? GWAS; __ July 2022

chromosome_x="true" # whether to collect GWAS summary statistics report for Chromosome X and XY

################################################################################
# Organize paths.
# Read private, local file paths.
cd ~/paths
path_process=$(<"./process_psychiatric_metabolism.txt")
path_dock="$path_process/dock"

path_gwas_source_container="${path_dock}/gwas_raw/${cohorts_models}"
path_gwas_target_container="${path_dock}/gwas_concatenation/${cohorts_models}"

path_scripts_record="$path_process/psychiatric_metabolism/scripts/record/2022-05-04/gwas_concatenation"
path_batch_instances="${path_gwas_target_container}/batch_instances_concatenation.txt"

###########################################################################
# Execute procedure.

# Initialize batch instances.
rm -r $path_gwas_target_container
mkdir -p $path_gwas_target_container
rm $path_batch_instances

# Define patterns for file names.
# Do not expand with full path until after passing as argument.
#pattern_gwas_report_file="report.*.glm.linear" # do not expand with full path yet <-- must choose here!!!
pattern_gwas_report_file="report.*.glm.logistic" # do not expand with full path yet <-- must choose here!!!
pattern_gwas_concatenation_file="gwas_concatenation.txt.gz"

# Iterate on directories for GWAS on cohorts and hormones.
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
        echo "-----"
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
echo "----------"
echo "----------"
echo "count of batch instances: " $batch_instances_count
echo "first batch instance: " ${batch_instances[0]} # notice base-zero indexing
echo "last batch instance: " ${batch_instances[$batch_instances_count - 1]}
echo "----------"
echo "----------"
echo "----------"

# Execute batch with grid scheduler.
if true; then
  # Submit array batch to Sun Grid Engine.
  # Array batch indices must start at one (not zero).
  qsub -t 1-${batch_instances_count}:1 -o \
  "${path_gwas_target_container}/out_concatenation.txt" -e "${path_gwas_target_container}/error_concatenation.txt" \
  "${path_scripts_record}/2_run_batch_jobs_gwas_concatenation.sh" \
  $path_batch_instances \
  $batch_instances_count \
  $pattern_gwas_report_file \
  $path_gwas_source_container \
  $path_gwas_target_container \
  $path_scripts_record \
  $path_process \
  $chromosome_x
fi
