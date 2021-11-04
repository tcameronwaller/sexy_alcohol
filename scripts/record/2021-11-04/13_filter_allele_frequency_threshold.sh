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

path_source_report="${path_allele_frequency}/allele_frequency_concatenation.afreq.gz"
path_target_report="${path_allele_frequency}/allele_frequency_filter_0_1.afreq"
path_target_report_compress="${path_allele_frequency}/allele_frequency_filter_0_1.afreq.gz"

################################################################################
# Organize variables.

threshold_allele_frequency=0.1 # threshold filter by minor allele frequency

################################################################################
# Filter SNPs by their Allele Frequencies.

zcat $path_source_report | awk 'BEGIN { FS=" "; OFS=" " } NR == 1' > $path_target_report
zcat $path_source_report | awk -v threshold="$threshold_allele_frequency" \
'BEGIN { FS=" "; OFS=" " } NR > 1 {
  if ( NF != 6)
    # Skip any rows with incorrect count of column fields.
    # Lesser count of column fields might indicate missing fields.
    next
  else if ( ( $5 == "NA" ) )
    # Skip any rows with missing value of the SNPs allele frequency.
    next
  else if ( ( $5 < threshold ) )
    # Skip any rows with SNP allele frequency less than threshold.
    next
  else
    # Keep row.
    print $0
  }' >> $path_target_report

# Compress file format.
gzip -cvf $path_target_report > $path_target_report_compress

###########################################################################
# Remove temporary files.
rm $path_target_report
