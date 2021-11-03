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
pattern_frequency_report_file="report.afreq"

################################################################################
# Paths.
path_allele_frequency_report="${path_allele_frequency}/allele_frequency_concatenation.afreq.gz"





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
--read_freq $path_allele_frequency_report ref-first \
--maf $threshold_allele_frequency \
--out report
