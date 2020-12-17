#!/bin/bash

#chmod u+x script.sh

###########################################################################
###########################################################################
###########################################################################
# This script organizes directories and iteration instances then submits
# script "regress_metabolite_heritability.sh" to the Sun Grid Engine.
###########################################################################
###########################################################################
###########################################################################

echo "----------------------------------------------------------------------"
echo "----------------------------------------------------------------------"
echo "----------------------------------------------------------------------"
echo "----------"
echo "The script organizes and submits an array batch job."
echo "----------"
echo "version check: 9"
echo "----------------------------------------------------------------------"
echo "----------------------------------------------------------------------"
echo "----------------------------------------------------------------------"

# Organize paths.
# Read private, local file paths.
echo "read private file path variables and organize paths..."
cd ~/paths
path_temporary=$(<"./temporary_sexy_alcohol.txt")
path_waller="$path_temporary/waller"
path_dock="$path_temporary/waller/dock"
path_scripts="$path_waller/sexy_alcohol/scripts/gwas"

# female_alcoholism_1_oestradiol: job 1943204, job 1943205
# male_alcoholism_1_oestradiol: job 1943206, job 1943207
# female_alcoholism_1_testosterone: job 1943208, job 1943209
# male_alcoholism_1_testosterone: job 1943210, job 1943211

# female_alcoholism_2_oestradiol: job 1943213, job 1943214
# male_alcoholism_2_oestradiol: job 1943353, job 1943354
# female_alcoholism_2_testosterone: job 1943363, job 1943364
# male_alcoholism_2_testosterone: job 1943366, job 1943367

# female_alcoholism_3_oestradiol: job 1943373, job 1943374
# male_alcoholism_3_oestradiol:
# female_alcoholism_3_testosterone:
# male_alcoholism_3_testosterone:

# Case-specific parameters.
threads=16
maf=0.01
count=22 # 22 # Count of chromosomes on which to run GWAS
covariates="age,body_mass_index,genotype_pc_1,genotype_pc_2,genotype_pc_3,genotype_pc_4,genotype_pc_5,genotype_pc_6,genotype_pc_7,genotype_pc_8,genotype_pc_9,genotype_pc_10"
sex="male"
alcoholism="alcoholism_3"
hormone="oestradiol"
analysis="${sex}_${alcoholism}_${hormone}"
phenotypes_alcoholism=$alcoholism
phenotypes_hormone=$hormone

# Case-specific paths.
path_table_phenotypes_covariates="$path_temporary/waller/dock/organization/cohorts/$alcoholism/$sex/$hormone/table_phenotypes_covariates.tsv"
path_report_alcoholism="$path_temporary/waller/dock/gwas/$analysis/$alcoholism"
path_report_hormone="$path_temporary/waller/dock/gwas/$analysis/$hormone"

# Echo each command to console.
#set -x
# Suppress echo each command to console.
set +x

# Determine whether the temporary directory structure already exists.
if [ ! -d $path_report_alcoholism ]; then
    # Directory does not already exist.
    # Create directory.
    mkdir -p $path_report_alcoholism
fi

# Determine whether the temporary directory structure already exists.
if [ ! -d $path_report_hormone ]; then
    # Directory does not already exist.
    # Create directory.
    mkdir -p $path_report_hormone
fi

# Submit array batch to Sun Grid Engine.
# Array batch indices cannot start at zero.
echo "----------------------------------------------------------------------"
echo "Submit array batch to Sun Grid Engine."
echo "----------------------------------------------------------------------"
qsub -t 1-${count}:1 \
-o "$path_report_alcoholism/out.txt" -e "$path_report_alcoholism/error.txt" \
$path_scripts/run_gwas.sh \
$path_table_phenotypes_covariates \
$path_report_alcoholism \
$analysis \
$phenotypes_alcoholism \
$covariates \
$threads \
$maf \

# Submit array batch to Sun Grid Engine.
# Array batch indices cannot start at zero.
echo "----------------------------------------------------------------------"
echo "Submit array batch to Sun Grid Engine."
echo "----------------------------------------------------------------------"
qsub -t 1-${count}:1 \
-o "$path_report_hormone/out.txt" -e "$path_report_hormone/error.txt" \
$path_scripts/run_gwas.sh \
$path_table_phenotypes_covariates \
$path_report_hormone \
$analysis \
$phenotypes_hormone \
$covariates \
$threads \
$maf \
