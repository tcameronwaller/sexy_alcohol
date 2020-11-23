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



path_parameter="$path_waller/sexy_alcohol/parameters"
path_variables="$path_parameter/uk_biobank_phenotype_variables.txt"
path_table_variables="$path_parameter/table_ukbiobank_phenotype_variables.tsv"
path_dock="$path_waller/dock"
path_access="$path_dock/access"
path_ukb_phenotype=$(<"./ukbiobank_phenotype.txt")
path_exclusion="$path_ukb_phenotype/exclude.csv"
path_ukb_parameter=$(<"./ukbiobank_parameter.txt")
path_identifier_pairs="$path_ukb_parameter/link.file.csv"
path_ukb_tools=$(<"./ukbiobank_tools.txt")

# Echo each command to console.
#set -x
# Suppress echo each command to console.
set +x


# Set parameters.
threads=16
maf=0.01
chromosome=3
phenotype_name="testosterone"
covariate_names="age,bmi,blah"

$path_plink2 \
--memory 90000 \
--threads $threads \
--bgen $ukbdir/Chromosome/ukb_imp_chr${chromosome}_v3.bgen \
--sample --sample $ukbdir/Chromosome/ukb46237_imp_chr${chromosome}_v3_s487320.sample \
--keep $clinical \
--maf $maf \
--freq --glm hide-covar \
--pfilter 1 \
--pheno $path_table_phenotypes_covariates \
--pheno-name $phenotype_name \
--covar $path_table_phenotypes_covariates \
--covar-name $covariate_names \
--out report \
