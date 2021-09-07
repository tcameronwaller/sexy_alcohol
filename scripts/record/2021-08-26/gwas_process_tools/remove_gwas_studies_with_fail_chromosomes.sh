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

#path_gwas_container="${path_dock}/gwas/cohorts_models_linear_order"
path_gwas_container="${path_dock}/gwas/cohorts_models_linear_order_unadjust"

path_batch_instances="${path_gwas_container}/post_process_fail_batch_instances.txt"

###########################################################################
# Execute procedure.

##########
# Initialize match instances.
rm $path_batch_instances

##########
# Iterate on directories for GWAS studies on cohorts, models, and phenotypes.
pattern_gwas_chromosome_file="report.*.glm.linear" # do not expand with full path yet
cd $path_gwas_container
for path_directory in `find . -maxdepth 1 -mindepth 1 -type d -not -name .`; do
  if [ -d "$path_directory" ]; then
    # Current content item is a directory.
    # Extract directory's base name.
    study="$(basename -- $path_directory)"
    #echo $directory

    # Assume that study's GWAS were successful across all chromosomes.
    fail="false"

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
      matches_chromosome=$(find "${path_gwas_container}/${study}/${name_chromosome}" -name "$pattern_gwas_chromosome_file")
      match_chromosome_file=${matches_chromosome[0]}
      if ! [[ -n $matches_chromosome && -f $match_chromosome_file ]]; then
        # Study's GWAS failed for current chromosome.
        fail="true"
      fi
    done

    ##########
    # Determine whether study's GWAS failed for any chromosomes.
    if [[ "$fail" == "true" ]]; then
      echo "----------"
      echo "study GWAS failed for at least one chromosome:"
      echo $study
      batch_instance="${path_gwas_container}/${study}"
      echo $batch_instance >> $path_batch_instances

    else
      echo "----------"
      echo "----------"
      echo "----------"
      echo "study GWAS SUCCESS for all chromosomes:"
      echo $study
    fi

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

for batch_instance in "${batch_instances[@]}"; do
  IFS=";" read -r -a array <<< "${batch_instance}"
  path_directory="${array[0]}"
  rm -r $path_directory
done
