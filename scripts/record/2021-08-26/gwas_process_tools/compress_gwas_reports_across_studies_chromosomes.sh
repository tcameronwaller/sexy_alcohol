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

path_gwas_container="${path_dock}/gwas/cohorts_models_linear_measurement_test"
#path_gwas_container="${path_dock}/gwas/cohorts_models_linear_measurement"
#path_gwas_container="${path_dock}/gwas/cohorts_models_linear_measurement_unadjust"
#path_gwas_container="${path_dock}/gwas/cohorts_models_linear_imputation"
#path_gwas_container="${path_dock}/gwas/cohorts_models_linear_imputation_unadjust"
#path_gwas_container="${path_dock}/gwas/cohorts_models_linear_order" <-- incomplete... first filter to complete
#path_gwas_container="${path_dock}/gwas/cohorts_models_linear_order_unadjust" <-- incomplete... first filter to complete
#path_gwas_container="${path_dock}/gwas/cohorts_models_logistic_detection" <-- next
#path_gwas_container="${path_dock}/gwas/cohorts_models_logistic_detection_unadjust"

path_match_instances="${path_gwas_container}/post_process_match_instances.txt"

###########################################################################
# Execute procedure.

##########
# Initialize match instances.
rm $path_match_instances

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
      if [[ -n $matches_chromosome && -f $match_chromosome_file ]]; then
        #echo "----------"
        #echo "----------"
        #echo "----------"
        #echo "Found ${name_chromosome} summary statistics for: ${study}"
        #echo $matches_chromosome
        #echo "Found match file: ${match_chromosome_file}"
        ##########
        # Define match instance for file conversion.
        match_instance="${match_chromosome_file};${match_chromosome_file}.gz"
        echo $match_instance >> $path_match_instances
      fi
    done
  fi
done

##########
# Read match instances.
readarray -t match_instances < $path_match_instances
match_instances_count=${#match_instances[@]}
echo "----------"
echo "count of match instances: " $match_instances_count
echo "first match instance: " ${match_instances[0]} # notice base-zero indexing
echo "last match instance: " ${match_instances[$match_instances_count - 1]}

##########
# Iterate across match instances.

for match_instance in "${match_instances[@]}"; do
  IFS=";" read -r -a array <<< "${match_instance}"
  path_file="${array[0]}"
  path_file_compress="${array[1]}"
  gzip -cvf $path_file > $path_file_compress
  rm $path_file
done
