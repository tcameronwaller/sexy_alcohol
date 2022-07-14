#!/bin/bash

###########################################################################
###########################################################################
###########################################################################
# ...
###########################################################################
###########################################################################
###########################################################################

# TODO: TCW; 14 July 2022
# TODO: Change the structure of this process.
# TODO: Use a model more similar to the new concatenation procedure.
# TODO: Define paths to ALL relevant down-stream scripts here in the top level driver script.
# TODO: Enable the same submit driver to control both "1. format" and "2. munge" but just changing source directory, target directory, and process script(s)



################################################################################
# General parameters.

#cohorts_models="oestradiol_logistic"                   # 18 GWAS; completed on 14 July 2022
#cohorts_models="oestradiol_linear"                     # 30 GWAS; completed on 14 July 2022
#cohorts_models="oestradiol_bioavailable_linear"        # 18 GWAS; started on 14 July 2022
cohorts_models="oestradiol_free_linear"                # 18 GWAS
#cohorts_models="testosterone_logistic"                 # 18 GWAS; completed on 14 July 2022
#cohorts_models="testosterone_linear"                   # 54 GWAS; started on 14 July 2022
#cohorts_models="testosterone_bioavailable_linear"      # 18 GWAS
#cohorts_models="testosterone_free_linear"              # 18 GWAS
#cohorts_models="steroid_globulin_linear"               # 20 GWAS; started on 14 July 2022
#cohorts_models="albumin_linear"                        # 20 GWAS; started on 14 July 2022

# Parameters.
regression_type="linear" # "linear" or "logistic"
response="coefficient" # "coefficient", "odds_ratio", or "z_score"; for linear GWAS, use "coefficient" unless "response_standard_scale" is "true", in which case "z_score"
response_standard_scale="false" # whether to convert reponse (effect, coefficient) to z-score standard scale ("true" or "false")
restore_target_study_directories="true" # whether to delete any previous directories for each study's format and munge GWAS ("true" or "false")

################################################################################
# Organize paths.
# Read private, local file paths.
cd ~/paths
path_process=$(<"./process_sexy_alcohol.txt")
path_dock="$path_process/dock"

path_gwas_concatenation_container="${path_dock}/gwas_concatenation/${cohorts_models}"
path_gwas_format_container="${path_dock}/gwas_ldsc_format/${cohorts_models}"
path_gwas_munge_container="${path_dock}/gwas_ldsc_munge/${cohorts_models}"
path_heritability_container="${path_dock}/heritability/${cohorts_models}"

path_scripts_record="$path_process/sexy_alcohol/scripts/record/2022-08-01/ldsc_heritability_correlation"
path_batch_instances="${path_gwas_munge_container}/batch_instances_format_munge.txt"

# Initialize directories and batch instances.
rm -r $path_gwas_format_container
mkdir -p $path_gwas_format_container
rm -r $path_gwas_munge_container
mkdir -p $path_gwas_munge_container
rm -r $path_heritability_container
mkdir -p $path_heritability_container
rm $path_batch_instances

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

# Iterate on directories for GWAS on cohorts and hormones.
name_gwas_concatenation_file="gwas.txt.gz"
cd $path_gwas_concatenation_container
for path_directory in `find . -maxdepth 1 -mindepth 1 -type d -not -name .`; do
  if [ -d "$path_directory" ]; then
    # Current content item is a directory.
    # Extract directory's base name.
    study="$(basename -- $path_directory)"
    #echo $directory
    # Determine whether directory contains valid GWAS summary statistics.
    matches=$(find "${path_gwas_concatenation_container}/${study}" -name "$name_gwas_concatenation_file")
    match_file=${matches[0]}
    if [[ -n $matches && -f $match_file ]]; then
      instance="$study;${path_gwas_concatenation_container}/${study}/${name_gwas_concatenation_file}"
      echo $instance >> $path_batch_instances
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
  "${path_gwas_munge_container}/post_process_out.txt" -e "${path_gwas_munge_container}/post_process_error.txt" \
  "${path_scripts_record}/3_run_batch_jobs_gwas_format_munge_heritability.sh" \
  $path_batch_instances \
  $batch_instances_count \
  $regression_type \
  $response \
  $response_standard_scale \
  $path_gwas_format_container \
  $path_gwas_munge_container \
  $path_heritability_container \
  $path_scripts_record \
  $path_process \
  $restore_target_study_directories
fi
