#!/bin/bash

#chmod u+x script.sh

###########################################################################
###########################################################################
###########################################################################

# version check: 1

###########################################################################
###########################################################################
###########################################################################
# Organize paths.
# Read private, local file paths.
echo "read private file path variables and organize paths..."
cd ~/paths
path_process=$(<"./process_sexy_alcohol.txt")
path_scripts_record="$path_process/sexy_alcohol/scripts/record/2021-11-04"
path_dock="$path_process/dock"
path_allele_frequency="${path_dock}/allele_frequency"

path_allele_frequency_report="${path_allele_frequency}/allele_frequency_filter_0_05.afreq.gz"

################################################################################
# Filter SNPs by their Allele Frequencies.
