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
path_gwas_summaries=$(<"./gwas_summaries_waller_metabolism.txt")
path_process=$(<"./process_sexy_alcohol.txt")

path_promiscuity_scripts="${path_process}/promiscuity/scripts"
path_promiscuity_scripts_ldsc_heritability="${path_promiscuity_scripts}/ldsc_genetic_heritability_correlation"
path_scripts_format="${path_promiscuity_scripts}/format_gwas_ldsc"
#path_scripts_record="$path_process/psychiatric_metabolism/scripts/record/2021-05-04"

path_dock="$path_process/dock"
path_genetic_reference="${path_dock}/access/genetic_reference"
path_gwas="${path_dock}/gwas"
path_heritability="${path_dock}/heritability"

path_gwas_cohorts_hormones="${path_gwas}/cohorts_hormones"

###########################################################################
# Define explicit inclusions and exclusions.

delimiter=" "
IFS=${delimiter}
inclusions=()
inclusions+=("female_combination_albumin_log")
inclusions+=("female_combination_steroid_globulin_log")
inclusions+=("female_combination_oestradiol_log")
inclusions+=("female_combination_oestradiol_free_log")
inclusions+=("female_combination_testosterone_log")
inclusions+=("female_combination_testosterone_free_log")
inclusions+=("female_premenopause_binary_albumin_log")
inclusions+=("female_premenopause_binary_steroid_globulin_log")
inclusions+=("female_premenopause_binary_oestradiol_log")
inclusions+=("female_premenopause_binary_oestradiol_free_log")
inclusions+=("female_premenopause_binary_testosterone_log")
inclusions+=("female_premenopause_binary_testosterone_free_log")
inclusions+=("female_premenopause_ordinal_albumin_log")
inclusions+=("female_premenopause_ordinal_steroid_globulin_log")
inclusions+=("female_premenopause_ordinal_oestradiol_log")
inclusions+=("female_premenopause_ordinal_oestradiol_free_log")
#inclusions+=("female_premenopause_ordinal_testosterone_log")
#inclusions+=("female_premenopause_ordinal_testosterone_free_log")

exclusions=()
unset IFS

###########################################################################
# Execute procedure.

# Iterate on directories for GWAS on cohorts and hormones.
cd $path_gwas_cohorts_hormones
for path_directory in `find . -maxdepth 1 -mindepth 1 -type d -not -name .`; do
  if [ -d "$path_directory" ]; then
    # Current content item is a directory.
    directory="$(basename -- $path_directory)"

    # Determine specific inclusions or exclusions.
    # inclusions: [[ " ${array[@]} " =~ " ${value} " ]]
    # exclusions: [[ ! " ${array[@]} " =~ " ${value} " ]]
    if [[ " ${inclusions[@]} " =~ "${directory}" ]]; then

      echo $directory

      # Concatenate GWAS across chromosomes.
      if false; then
        # Organize variables.
        pattern_source_file="report.*.glm.linear" # do not expand with full path yet
        path_source_directory="${path_gwas_cohorts_hormones}/${directory}"
        chromosome_start=1
        chromosome_end=22
        path_gwas_concatenation="${path_source_directory}/gwas_concatenation.txt"
        path_gwas_concatenation_compress="${path_source_directory}/gwas_concatenation.txt.gz"
        report="true" # "true" or "false"
        /usr/bin/bash "${path_promiscuity_scripts}/collect_concatenate_gwas_chromosomes.sh" \
        $pattern_source_file \
        $path_source_directory \
        $chromosome_start \
        $chromosome_end \
        $path_gwas_concatenation \
        $path_gwas_concatenation_compress \
        $report
      fi

      # Format and munge GWAS summary statistics.
      # Estimate genotype heritability.
      if false; then
        # Organize paths.
        path_gwas_study="${path_gwas_cohorts_hormones}/${directory}"
        path_heritability_study="${path_heritability}/cohorts_hormones/${directory}"
        # Initialize directories.
        mkdir -p $path_gwas_study
        mkdir -p $path_heritability_study
        # Organize variables.
        study="${directory}"
        name_prefix="null"
        path_source_file="${path_gwas_study}/gwas_concatenation.txt.gz"
        path_script_gwas_format="${path_scripts_format}/format_gwas_ldsc_plink_linear.sh"
        report="true" # "true" or "false"
        /usr/bin/bash "$path_promiscuity_scripts_ldsc_heritability/format_munge_gwas_heritability_ldsc.sh" \
        $study \
        $name_prefix \
        $path_source_file \
        $path_genetic_reference \
        $path_gwas_study \
        $path_heritability_study \
        $path_script_gwas_format \
        $path_promiscuity_scripts \
        $path_ldsc \
        $report
      fi
    fi
  fi
done
