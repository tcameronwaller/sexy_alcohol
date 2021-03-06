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
chromosomes=$4 # count of chromosomes

# Concatenate GWAS reports from all chromosomes.
# Extract relevant information and format for LDSC.
# Initialize concatenation.
cd $path_gwas
path_concatenation="$path_gwas/concatenation.${phenotype}.glm.linear"

rm $path_concatenation

# dock/gwas/female_alcoholism_1_testosterone/testosterone/chromosome_1/report.testosterone.glm.linear
# dock/gwas/female_alcoholism_1_testosterone/alcoholism_1/chromosome_1/report.alcoholism_1.glm.linear


echo "SNP A1 A2 N BETA P" > $path_concatenation
for (( index=1; index<=$chromosomes; index+=1 )); do
  path_gwas_chromosome="$path_gwas/chromosome_${index}"
  echo "gwas chromosome path: "
  echo $path_gwas_chromosome
  path_report="$path_gwas_chromosome/${prefix}.${phenotype}.glm.linear"
  # Select and concatenate relevant information from chromosome reports.
  # Format of GWAS reports (".glm.linear") by PLINK2.
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
  cat $path_report | awk 'NR > 1 {print $3, $6, $4, $8, $9, $12}' >> $path_concatenation
done
echo "----------"
echo "----------"
echo "----------"
echo "after concatenation..."
head -30 $path_concatenation
