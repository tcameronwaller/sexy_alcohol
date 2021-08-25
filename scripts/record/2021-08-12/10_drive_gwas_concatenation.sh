#!/bin/bash

###########################################################################
###########################################################################
###########################################################################
# ...
###########################################################################
###########################################################################
###########################################################################

################################################################################
# Organize argument variables.

study=${1} # text name of GWAS study and also name of study's parent directory
path_gwas_source_container=${2} # full path to parent directories of GWAS summary statistics for each study
path_gwas_target_container=${3} # full path to parent directories of GWAS summary statistics for each study

################################################################################
# Organize paths.
# Read private, local file paths.
cd ~/paths

path_process=$(<"./process_sexy_alcohol.txt")
path_dock="$path_process/dock"

# General paths.
#path_gwas_source_container="${path_dock}/gwas_complete/cohorts_models"
#path_gwas_target_container="${path_dock}/gwas_process/cohorts_models"

###########################################################################
# Execute procedure.

##############################################################################
# Concatenation and format.
# Paths.
path_gwas_source_parent="${path_gwas_source_container}/${study}"
path_gwas_target_parent="${path_gwas_target_container}/${study}"
rm -r $path_gwas_target_parent
mkdir -p $path_gwas_target_parent
path_gwas_concatenation="${path_gwas_target_parent}/gwas_concatenation.txt"
path_gwas_concatenation_compress="${path_gwas_target_parent}/gwas_concatenation.txt.gz"
# Scripts.
path_promiscuity_scripts="${path_process}/promiscuity/scripts"
path_scripts_gwas_process="${path_promiscuity_scripts}/gwas_process"
path_script_gwas_collect_concatenate="${path_scripts_gwas_process}/collect_concatenate_gwas_chromosomes.sh"
# Parameters.
pattern_source_file="report.*.glm.linear" # do not expand with full path yet
chromosome_start=1
chromosome_end=22
report="true" # "true" or "false"
/usr/bin/bash "$path_script_gwas_collect_concatenate" \
$pattern_source_file \
$path_gwas_source_parent \
$chromosome_start \
$chromosome_end \
$path_gwas_concatenation \
$path_gwas_concatenation_compress \
$report
