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
path_concatenation="${path_allele_frequency}/allele_frequency_concatenation.afreq"
path_concatenation_compress="${path_allele_frequency}/allele_frequency_concatenation.afreq.gz"

# Remove any previous versions of target files.
rm $path_concatenation
rm $path_concatenation_compress


# Initialize table columns by file for chromosome 1.
# echo "#CHROM POS ID REF ALT A1 TEST OBS_CT BETA SE T_STAT P" > $path_gwas_concatenation
path_source_chromosome="$path_allele_frequency/chromosome_1"
matches=$(find "${path_source_chromosome}" -name "$pattern_frequency_report_file")
path_source_file=${matches[0]}
echo "source file for table column headers: " $path_source_file
cat $path_source_file | awk 'BEGIN { FS=" "; OFS=" " } NR == 1' > $path_concatenation

# Concatenate GWAS reports from selection chromosomes.
#for (( index=$chromosome_start; index<=$chromosome_end; index+=1 )); do
chromosomes=("1" "2" "3" "4" "5" "6" "7" "8" "9" "10" "11" "12" "13" "14" "15" "16" "17" "18" "19" "20" "21" "22" "x")
for chromosome in "${chromosomes[@]}"; do
  path_source_chromosome="$path_allele_frequency/chromosome_${chromosome}"
  matches=$(find "${path_source_chromosome}" -name "$pattern_frequency_report_file")
  path_source_file=${matches[0]}
  echo "source file: " $path_source_file
  # Concatenate information from chromosome reports.
  #cat $path_source_file >> $path_gwas_concatentation
  #cat $path_source_file | awk 'BEGIN { FS=" "; OFS=" " } NR > 1 { print $1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12 }' >> $path_gwas_concatenation
  cat $path_source_file | awk 'BEGIN { FS=" "; OFS=" " } NR > 1 { print $0 }' >> $path_concatenation
done
# Compress file format.
gzip -cvf $path_concatenation > $path_concatenation_compress

###########################################################################
# Remove temporary files.
rm $path_concatenation
