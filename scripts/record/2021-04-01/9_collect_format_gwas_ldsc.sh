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
hormone=${2} # identifier of hormone phenotype for GWAS
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

###########################################################################
# Execute procedure.

# Report.
if [[ "$report" == "true" ]]; then
  echo "----------"
  echo "cohort and hormone: " $cohort_hormone
  echo "hormone: " $hormone
  echo "path to original directory: " $path_source_directory
  echo "path to new file: " $path_gwas_format
fi

# Format of GWAS summary statistics for LDSC.
# https://github.com/bulik/ldsc/wiki/Heritability-and-Genetic-Correlation#reformatting-summary-statistics
# description: ............................ LDSC column ........... source column .......... position
# variant identifier (RS ID): .............  "SNP" ................  "SNP" ................. 2
# alternate allele (effect allele): .......  "A1" .................  "A1" .................. 4
# reference allele (non-effect allele): ...  "A2" .................  "A2" .................. 5
# sample size: ............................  "N" ..................  None .................. [samples = 52,848]
# effect (coefficient or odds ratio): .....  "BETA" or "OR" .......  "Z" ................... 6
# probability (p-value): ..................  "P" ..................  "P" ................... 7

# Remove any previous versions of temporary files.
rm $path_gwas_collection
rm $path_gwas_format


# TODO: need to update variable names below...


# Concatenate GWAS reports from all chromosomes.
# Extract relevant information and format for LDSC.
# Initialize concatenation.
cd $path_gwas

echo "interpreting ${phenotype} as ${suffix}..."

# Organize and concatenate information from linear GWAS.
if [ "$regression_type" = "linear" ]; then
  path_concatenation="$path_gwas/concatenation.${phenotype}.glm.${suffix}"
  rm $path_concatenation
  path_raw="$path_gwas/concatenation.${phenotype}.glm.${suffix}_raw"
  echo "SNP A1 A2 N BETA P" > $path_raw
  for (( index=1; index<=$chromosomes; index+=1 )); do
    path_gwas_chromosome="$path_gwas/chromosome_${index}"
    echo "gwas chromosome path: "
    echo $path_gwas_chromosome
    path_report="$path_gwas_chromosome/${prefix}.${phenotype}.glm.${suffix}"
    # Select and concatenate relevant information from chromosome reports.
    # Format of GWAS reports by PLINK2 for linear regression (".glm.linear").
    # https://www.cog-genomics.org/plink/2.0/formats
    # Format of GWAS summary for LDSC.
    # https://github.com/bulik/ldsc/wiki/Heritability-and-Genetic-Correlation#reformatting-summary-statistics
    # description: ............................ PLINK2 column ... LDSC column
    # variant identifier: ..................... "ID" ............ "SNP"
    # alternate allele (effect allele): ....... "A1" ............ "A1"
    # reference allele (non-effect allele): ... "REF" ........... "A2"
    # sample size: ............................ "OBS_CT" ........ "N"
    # effect (beta): .......................... "BETA" .......... "BETA"
    # probability (p-value): .................. "P" ............. "P"
    cat $path_report | awk 'NR > 1 {print $3, $6, $4, $8, $9, $12}' >> $path_raw
  done
  echo "after concatenation... before z-score"
  head -30 $path_raw
  # Calculate Z-score standardization of Beta coefficients.
  /usr/bin/bash $path_calculate_z_score 5 $path_raw $path_concatenation
fi

# Organize and concatenate information from logistic GWAS.
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
    # Format of GWAS reports by PLINK2 for logistic regression (".glm.logistic").
    # https://www.cog-genomics.org/plink/2.0/formats

    # PLINK2 report format is similar for logistic regression (".glm.logistic").
    # Logistic report has "OR" in place of "BETA", but positions are the same.
    # https://www.cog-genomics.org/plink/2.0/formats

    # Format of GWAS summary for LDSC.
    # https://github.com/bulik/ldsc/wiki/Heritability-and-Genetic-Correlation#reformatting-summary-statistics
    # description: ............................ PLINK2 column ... LDSC column
    # variant identifier: ..................... "ID" ............ "SNP"
    # alternate allele (effect allele): ....... "A1" ............ "A1"
    # reference allele (non-effect allele): ... "REF" ........... "A2"
    # sample size: ............................ "OBS_CT" ........ "N"
    # effect (odds ratio): .................... "OR" ............ "OR"
    # probability (p-value): .................. "P" ............. "P"
    cat $path_report | awk 'NR > 1 {print $3, $6, $4, $8, $9, $12}' >> $path_concatenation
    #cat $path_report | awk 'NR > 1 {print $3, $6, $4, $8, log($9), $12}' >> $path_concatenation
    #cat $path_report | awk 'NR > 1 {beta=log($9);print $3, $6, $4, $8, beta, $12}' >> $path_concatenation
  done
fi

echo "----------"
echo "----------"
echo "----------"
echo "after concatenation..."
head -30 $path_concatenation
