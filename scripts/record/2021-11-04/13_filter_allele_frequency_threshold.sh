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
path_plink2=$(<"./tools_plink2.txt")
path_process=$(<"./process_sexy_alcohol.txt")
path_scripts_record="$path_process/sexy_alcohol/scripts/record/2021-11-04"
path_dock="$path_process/dock"
path_allele_frequency="${path_dock}/allele_frequency"
path_source_report="${path_allele_frequency}/allele_frequency_concatenation.afreq"
#path_target_report="${path_allele_frequency}/allele_frequency_0_1.afreq"

################################################################################
# Organize variables.

threshold_allele_frequency=0.1 # threshold filter by minor allele frequency
threads=32 # count of processing threads to use

cd $path_allele_frequency
# Call PLINK2.
# This call to PLINK2 includes "--freq" and produces a report of allele
# frequencies.
# 90,000 Mebibytes (MiB) is 94.372 Gigabytes (GB)
# Argument "--reference-allele" allows to give an explicit list of alleles to designate as "A1".
# "Warning: No --bgen REF/ALT mode specified ('ref-first', 'ref-last', or 'ref-unknown'). This will be required as of alpha 3."
$path_plink2 \
--memory 90000 \
--threads $threads \
--read-freq $path_source_report \
--maf $threshold_allele_frequency \
--freq \
--out allele_frequency_0_1
