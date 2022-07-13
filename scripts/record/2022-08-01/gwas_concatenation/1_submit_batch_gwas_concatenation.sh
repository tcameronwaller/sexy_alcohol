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



################################################################################
# Organize paths.
# Read private, local file paths.
cd ~/paths
path_process=$(<"./process_sexy_alcohol.txt")
path_dock="$path_process/dock"
path_directory_gwas_raw="${path_dock}/gwas_raw_test"
path_directory_gwas_concatenation="${path_dock}/gwas_concatenation_test"

# Scripts.
path_promiscuity_scripts="${path_process}/promiscuity/scripts"
path_script_concatenate="${path_promiscuity_scripts}/utility/plink/concatenate_plink_gwas_frequency_log_across_chromosomes.sh"

################################################################################
# General parameters.

# Organize multi-dimensional array of information about sets of studies.
# [name of set] ; [regression type: "linear" or "logistic"] ; [whether to include chromosomes X and XY]
instances_sets=()
#instances_sets+=("oestradiol_logistic;logistic;true")              # 18 GWAS
instances_sets+=("oestradiol_linear;linear;true")                  # 30 GWAS
#instances_sets+=("oestradiol_bioavailable_linear;linear;true")     # 18 GWAS
#instances_sets+=("oestradiol_free_linear;linear;true")             # 18 GWAS
#instances_sets+=("testosterone_logistic;logistic;true")            # 18 GWAS
#instances_sets+=("testosterone_linear;linear;true")                # 54 GWAS
#instances_sets+=("testosterone_bioavailable_linear;linear;true")   # 18 GWAS
#instances_sets+=("testosterone_free_linear;linear;true")           # 18 GWAS
#instances_sets+=("steroid_globulin_linear;linear;true")            # 20 GWAS
#instances_sets+=("albumin_linear;linear;true")                     # 20 GWAS

################################################################################
# Execute procedure.

##########
# Navigate directories and files.

# Iterate across sets of GWAS studies.
for instance_set in "${instances_sets[@]}"; do

  # Separate fields from instance.
  IFS=";" read -r -a array <<< "${instance_set}"
  name_set="${array[0]}"
  type_regression="${array[1]}"
  chromosome_xy="${array[2]}"

  # Define patterns for names of source files.
  # Do not expand with full path until after passing as argument.
  if [[ "$type_regression" == "linear" ]]; then
    pattern_file_gwas_source="report.*.glm.linear" # do not yet expand pattern to full path
  elif [[ "$type_regression" == "logistic" ]]; then
    pattern_file_gwas_source="report.*.glm.logistic" # do not yet expand pattern to full path
  fi
  pattern_file_frequency_source="report.afreq"
  pattern_file_log_source="report.log"

  # Iterate across GWAS studies within current set.
  path_directory_set="${path_directory_gwas_raw}/${name_set}"
  # `find "${path_directory_set}" -maxdepth 1 -mindepth 1 -type d -not -name "."`
  paths_directories_studies=($(find ${path_directory_set} -maxdepth 1 -mindepth 1 -type d -not -name .))
  echo "array of paths found..."
  count=${#paths_directories_studies[@]}
  echo "----------"
  echo "----------"
  echo "----------"
  echo "count of batch instances: " $count
  echo "first batch instance: " ${paths_directories_studies[0]} # notice base-zero indexing
  echo "last batch instance: " ${paths_directories_studies[$count - 1]}
  echo "----------"
  echo "----------"
  echo "----------"

  for path_directory_study in ${paths_directories_studies[@]}; do
    # Confirm that path is a directory.
    #if [ -d "$path_directory_study" ]; then

    echo "New path: " ${path_directory_study}

    # Extract name of study.
    name_study="$(basename -- $path_directory_study)"

    echo "Name of study: " ${name_study}

    # Confirm that directory contains a file for GWAS summary statistics.
    matches=$(find "${path_directory_gwas_raw}/${name_set}/${name_study}/chromosome_22" -name "$pattern_file_gwas_source")
    path_file_gwas_source=${matches[0]}
    if [[ -n $matches && -f $path_file_gwas_source ]]; then

      # Define paths and names of product files.
      path_directory_chromosomes_source="${path_directory_gwas_raw}/${name_set}/${name_study}"
      path_directory_set_study_product="${path_directory_gwas_concatenation}/${name_set}/${name_study}"
      name_directory_log_product="plink_execution_logs"
      path_file_gwas_product="${path_directory_gwas_concatenation}/${name_set}/${name_study}/gwas.txt.gz"
      path_file_frequency_product="${path_directory_gwas_concatenation}/${name_set}/${name_study}/allele_frequency.afreq.gz"
      prefix_file_log_product="chromosome_"
      suffix_file_log_product=".log"

      # Initialize directory.
      rm -r $path_directory_set_study_product # Caution: removes the parent directory of the product files

      # Parameters.
      report="true"

      # Define and append a new instance for a batch job.
      instance_array=()
      instance_array+=(${pattern_file_gwas_source})
      instance_array+=($pattern_file_frequency_source)
      instance_array+=($pattern_file_log_source)
      instance_array+=($path_directory_chromosomes_source)
      instance_array+=($path_file_gwas_product)
      instance_array+=($path_file_frequency_product)
      instance_array+=($name_directory_log_product)
      instance_array+=($prefix_file_log_product)
      instance_array+=($suffix_file_log_product)
      instance_array+=($chromosome_xy)
      instance_array+=($report)
      instance=$(IFS=";"; echo "${instance_array[*]}") # write array to string with custom delimiter
      echo "batch instance: " ${instance}
      #echo $instance >> $path_batch_instances
    fi
  done
done





#
