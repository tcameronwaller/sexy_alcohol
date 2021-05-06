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
# Execute procedure.

# TODO: iterate on all cohort-hormone subdirectories
#find . -maxdepth 1 -mindepth 1 -type d

#
cd $path_gwas_cohorts_hormones
for path_directory in `find . -type d -maxdepth 1 -mindepth 1`; do
  if [ -d "$path_directory" ]; then
    # Current content item is a directory.
    echo $path_directory
  fi
done
