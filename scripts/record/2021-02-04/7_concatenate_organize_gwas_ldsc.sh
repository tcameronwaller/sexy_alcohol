#!/bin/bash

###########################################################################
###########################################################################
###########################################################################
# ...
###########################################################################
###########################################################################
###########################################################################

echo "----------------------------------------------------------------------"
echo "----------------------------------------------------------------------"
echo "----------------------------------------------------------------------"
echo "Concatenate GWAS summary statistics across chromosomes."
echo "version 1"
echo "----------------------------------------------------------------------"
echo "----------------------------------------------------------------------"
echo "----------------------------------------------------------------------"
echo ""
echo ""
echo ""

# Organize variables.
path_gwas=$1 # path to directory with GWAS report files
prefix=$2 # prefix for GWAS report files
phenotype=$3 # name of phenotype in names of GWAS report files
suffix=$4 # suffix for GWAS report files
chromosomes=$5 # count of chromosomes
path_scripts=$6 # scripts

path_calculate_z_score="$path_scripts/calculate_z_score.sh"

# Concatenate GWAS reports from all chromosomes.
# Extract relevant information and format for LDSC.
# Initialize concatenation.
cd $path_gwas

# dock/gwas/female_alcoholism_1_testosterone/testosterone/chromosome_1/report.testosterone.glm.linear
# dock/gwas/female_alcoholism_1_testosterone/alcoholism_1/chromosome_1/report.alcoholism_1.glm.linear

echo "interpreting ${phenotype} as ${suffix}..."

# Organize and concatenate information from linear GWAS.
if [ "$suffix" = "linear" ]; then
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

  # Calculate Z-score standardization of Beta coefficients.
  $path_calculate_z_score 5 $path_raw $path_concatenation
fi

# Organize and concatenate information from logistic GWAS.
if [ "$suffix" = "logistic" ]; then
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
