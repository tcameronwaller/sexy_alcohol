#!/bin/bash

###########################################################################
###########################################################################
###########################################################################
# ...
###########################################################################
###########################################################################
###########################################################################

################################################################################
# Organize arguments.
cohort_hormone=${1} # unique identifier of GWAS study for cohort and hormone
hormone=${2} # identifier of hormone phenotype in GWAS study
path_source_directory=${3} # full path to source directory with GWAS summary statistics for a single cohort and hormone
regression_type=${4} # type of regression for GWAS, either "logistic" or "linear"
path_gwas_collection=${5} # full path to temporary file for collection of GWAS summary statistics
path_gwas_format=${6} # full path to file for formatted GWAS summary statistics
path_gwas_format_compress=${7} # full path to file for formatted GWAS summary statistics after compression
path_promiscuity_scripts=${8} # complete path to directory of scripts for z-score standardization
report=${9} # whether to print reports

################################################################################
# Organize variables.

#path_calculate_z_score="$path_promiscuity_scripts/calculate_z_score_column_4_of_5.sh"
path_calculate_z_score="$path_promiscuity_scripts/calculate_z_score_column_5_of_6.sh"

prefix="report"
chromosomes=22

###########################################################################
# Execute procedure.

# Report.
if [[ "$report" == "true" ]]; then
  echo "----------"
  echo "cohort and hormone: " $cohort_hormone
  echo "hormone: " $hormone
  echo "regression type: " $regression_type
  echo "path to original directory: " $path_source_directory
  echo "path to new file: " $path_gwas_format
fi

# Format of GWAS summary statistics for LDSC.
# https://github.com/bulik/ldsc/wiki/Heritability-and-Genetic-Correlation#reformatting-summary-statistics
# Format of GWAS reports by PLINK2 for linear regression (".glm.linear").
# https://www.cog-genomics.org/plink/2.0/formats
# PLINK2 report format is similar for logistic regression (".glm.logistic").
# Logistic report has "OR" in place of "BETA", but positions are the same.
# description: ............................ LDSC column ........... source column .......... position
# variant identifier (RS ID): .............  "SNP" ................  "ID" .................. 3
# alternate allele (effect allele): .......  "A1" .................  "A1" .................. 6
# reference allele (non-effect allele): ...  "A2" .................  "REF" ................. 4
# sample size: ............................  "N" ..................  "OBS_CT" .............. 8
# effect (coefficient or odds ratio): .....  "BETA" or "OR" .......  "BETA" ................ 9
# probability (p-value): ..................  "P" ..................  "P" ................... 12

# Remove any previous versions of temporary files.
rm $path_gwas_collection
rm $path_gwas_format

# Concatenate GWAS reports from all chromosomes.
# Extract relevant information and format for LDSC.

# Collect and organize information from linear GWAS.
if [ "$regression_type" = "linear" ]; then
  echo "SNP A1 A2 N BETA P" > $path_gwas_collection
  for (( index=1; index<=$chromosomes; index+=1 )); do
    path_source_chromosome="$path_source_directory/chromosome_${index}"
    path_source_file="$path_source_chromosome/${prefix}.${hormone}.glm.${regression_type}"
    # Select and concatenate relevant information from chromosome reports.
    cat $path_source_file | awk 'BEGIN { FS=" "; OFS=" " } NR > 1 {print $3, $6, $4, $8, $9, $12}' >> $path_gwas_collection
  done
  # Calculate Z-score standardization of Beta coefficients.
  /usr/bin/bash $path_calculate_z_score \
  5 \
  $path_gwas_collection \
  $path_gwas_format \
  $report
  # Compress file format.
  # No need in this situation, since each iteration replaces the previous file.
  gzip -cvf $path_gwas_format > $path_gwas_format_compress
fi

# Collect and organize information from logistic GWAS.
if [ "$regression_type" = "logistic" ]; then
  path_concatenation="$path_gwas/concatenation.${phenotype}.glm.${suffix}"
  rm $path_concatenation
  echo "SNP A1 A2 N OR P" > $path_concatenation
  for (( index=1; index<=$chromosomes; index+=1 )); do
    path_gwas_chromosome="$path_gwas/chromosome_${index}"
    echo "gwas chromosome path: "
    echo $path_gwas_chromosome
    path_report="$path_gwas_chromosome/${prefix}.${phenotype}.glm.${suffix}"
    # Select and concatenate relevant information from chromosome reports.
    cat $path_report | awk 'NR > 1 {print $3, $6, $4, $8, $9, $12}' >> $path_concatenation
    #cat $path_report | awk 'NR > 1 {print $3, $6, $4, $8, log($9), $12}' >> $path_concatenation
    #cat $path_report | awk 'NR > 1 {beta=log($9);print $3, $6, $4, $8, beta, $12}' >> $path_concatenation
  done
fi

# Report.
if [[ "$report" == "true" ]]; then
  echo "----------"
  echo "before standardization:"
  head -10 $path_gwas_collection
  echo "after standardization:"
  head -10 $path_gwas_format
  echo "----------"
fi
