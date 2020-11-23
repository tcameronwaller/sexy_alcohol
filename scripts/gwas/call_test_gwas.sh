#!/bin/bash

#chmod u+x script.sh

###########################################################################
###########################################################################
###########################################################################
# This script organizes paths and parameters to access local information
# about persons and phenotypes in the UKBiobank.
###########################################################################
###########################################################################
###########################################################################

# Read private, local file paths.
echo "read private file path variables and organize paths..."
cd ~/paths
path_temporary=$(<"./temporary_sexy_alcohol.txt")
path_waller="$path_temporary/waller"
path_scripts="$path_waller/sexy_alcohol/scripts"
path_gwas="$path_waller/dock/gwas"
path_table_phenotypes_covariates="$path_waller/dock/organization/table_phenotypes_covariates.tsv"
path_plink2=$(<"./tools_plink2.txt")
path_ukb_genotype=$(<"./ukbiobank_genotype.txt")

# Echo each command to console.
#set -x
# Suppress echo each command to console.
set +x

mkdir -p $path_gwas

# Set parameters.
threads=16
maf=0.01
chromosome=3
phenotype_name="testosterone"
covariate_names="age,bmi"

# Call PLINK2.
$path_plink2 \
--memory 90000 \
--threads $threads \
--bgen $path_ukb_genotype/Chromosome/ukb_imp_chr${chromosome}_v3.bgen \
--sample $path_ukb_genotype/Chromosome/ukb46237_imp_chr${chromosome}_v3_s487320.sample \
--keep $path_table_phenotypes_covariates \
--maf $maf \
--freq --glm hide-covar \
--pfilter 1 \
--pheno $path_table_phenotypes_covariates \
--pheno-name $phenotype_name \
--covar $path_table_phenotypes_covariates \
--covar-name $covariate_names \
--out report \
