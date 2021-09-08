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
path_process=$(<"./process_sexy_alcohol.txt")
path_dock="$path_process/dock"
path_scripts_record="$path_process/sexy_alcohol/scripts/record/2021-08-26/gwas_process_tools"

path_gwas_container="${path_dock}/gwas/cohorts_models_linear_measurement_test"
#path_gwas_container="${path_dock}/gwas/cohorts_models_linear_measurement"
#path_gwas_container="${path_dock}/gwas/cohorts_models_linear_measurement_unadjust"
#path_gwas_container="${path_dock}/gwas/cohorts_models_linear_imputation"
#path_gwas_container="${path_dock}/gwas/cohorts_models_linear_imputation_unadjust"
#path_gwas_container="${path_dock}/gwas/cohorts_models_linear_order" <-- incomplete... first filter to complete
#path_gwas_container="${path_dock}/gwas/cohorts_models_linear_order_unadjust" <-- incomplete... first filter to complete
#path_gwas_container="${path_dock}/gwas/cohorts_models_logistic_detection" <-- next
#path_gwas_container="${path_dock}/gwas/cohorts_models_logistic_detection_unadjust"

path_batch_instances="${path_gwas_container}/post_process_compress_batch_instances.txt"

###########################################################################
# Execute procedure.

##########
# Initialize match instances.
rm $path_batch_instances

##########
# Iterate on directories for GWAS studies on cohorts, models, and phenotypes.
pattern_gwas_report_file="report.*.glm.linear" # do not expand with full path yet
cd $path_gwas_container
for path_directory in `find . -maxdepth 1 -mindepth 1 -type d -not -name .`; do
  if [ -d "$path_directory" ]; then
    # Current content item is a directory.
    # Extract directory's base name.
    study="$(basename -- $path_directory)"
    #echo $directory

    ##########
    # Iterate on chromosomes.
    start=1
    end=22
    for (( index=$start; index<=$end; index++ )); do
      #echo "chromosome: ${index}"
      # Set chromosome name.
      name_chromosome="chromosome_${index}"

      # Determine whether directory contains valid GWAS summary statistics
      # for current chromosomes.
      matches_chromosome=$(find "${path_gwas_container}/${study}/${name_chromosome}" -name "$pattern_gwas_report_file")
      match_chromosome_file=${matches_chromosome[0]}
      if [[ -n $matches_chromosome && -f $match_chromosome_file ]]; then
        #echo "----------"
        #echo "----------"
        #echo "----------"
        #echo "Found ${name_chromosome} summary statistics for: ${study}"
        #echo $matches_chromosome
        #echo "Found match file: ${match_chromosome_file}"
        ##########
        # Define match instance for file conversion.
        batch_instance="${match_chromosome_file};${match_chromosome_file}.gz"
        echo $batch_instance >> $path_batch_instances
      fi
    done
  fi
done

##########
# Read match instances.
readarray -t batch_instances < $path_batch_instances
batch_instances_count=${#batch_instances[@]}
echo "----------"
echo "count of batch instances: " $batch_instances_count
echo "first batch instance: " ${batch_instances[0]} # notice base-zero indexing
echo "last batch instance: " ${batch_instances[$batch_instances_count - 1]}

##########
# Iterate across batch instances.

#for match_instance in "${match_instances[@]}"; do
#  IFS=";" read -r -a array <<< "${match_instance}"
#  path_file="${array[0]}"
#  path_file_compress="${array[1]}"
#  gzip -cvf $path_file > $path_file_compress
#  rm $path_file
#done

# Execute batch with grid scheduler.
if true; then
  # Submit array batch to Sun Grid Engine.
  # Array batch indices must start at one (not zero).
  qsub -t 1-${batch_instances_count}:1 \
  -o "${path_gwas_container}/post_process_compress_out.txt" \
  -e "${path_gwas_container}/post_process_compress_error.txt" \
  "${path_scripts_record}/run_batch_jobs_compress_gwas.sh" \
  $path_batch_instances \
  $batch_instances_count \
  $path_gwas_container
fi
