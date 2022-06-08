#!/bin/bash

#chmod u+x script.sh

###########################################################################
###########################################################################
###########################################################################
# This script organizes directories and iteration instances then submits
# script "regress_metabolite_heritability.sh" to the Sun Grid Engine.

# version check: 2

###########################################################################
###########################################################################
###########################################################################


# Organize paths.
# Read private, local file paths.
echo "read private file path variables and organize paths..."
cd ~/paths
path_process=$(<"./process_psychiatric_metabolism.txt")
path_scripts_record="$path_process/psychiatric_metabolism/scripts/record/2022-03-07/gwas_association"
path_dock="$path_process/dock"

path_stratification_tables="${path_dock}/stratification_2022-02-27/vitamin_d"

path_gwas_container="${path_dock}/gwas_raw/vitamin_d_linear"   # 24 GWAS; TCW started at ___ on 27 February 2022; job ___

# Initialize directories.
rm -r $path_gwas_container
mkdir -p $path_gwas_container

##########
##########
##########
# Assemble a list of analysis instances with common patterns.

# Assemble array of batch instance details.
path_batch_instances="${path_gwas_container}/batch_instances.txt"
rm $path_batch_instances

##########
# General models.

##########
# Define covariates common for all cohorts.
covariates_genotype="genotype_array_axiom,genotype_pc_1,genotype_pc_2,genotype_pc_3,genotype_pc_4,genotype_pc_5,genotype_pc_6,genotype_pc_7,genotype_pc_8,genotype_pc_9,genotype_pc_10"

##########
# Basis covariates

# "vitamin_d"
covariates_joint_1="age,body_log,region,season,medication_vitamin_d"
covariates_joint_2="age,body_log,region,season,medication_vitamin_d,alteration_sex_hormone,cholesterol_imputation,oestradiol_imputation,testosterone_imputation"
covariates_joint_3="age,body_log,region,season,medication_vitamin_d,alteration_sex_hormone,cholesterol_imputation,oestradiol_imputation,testosterone_imputation,steroid_globulin_imputation,albumin_imputation"

##########
# Define multi-dimensional array of cohorts and model covariates.
# [name of cohort and model for analysis description];[table name cohort-model prefix];[independent variable columns in table, beginning with cohort-specific variables]
cohorts_models_instances=()

### female_male
cohorts_models_instances+=("female_male_unadjust;table_female_male_priority_male_unadjust;sex_y,")
cohorts_models_instances+=("female_male_priority_male_joint_1;table_female_male_priority_male_joint_1;sex_y,${covariates_joint_1},")
cohorts_models_instances+=("female_male_priority_male_joint_2;table_female_male_priority_male_joint_2;sex_y,${covariates_joint_2},")
cohorts_models_instances+=("female_male_priority_male_joint_3;table_female_male_priority_male_joint_3;sex_y,${covariates_joint_3},")

##########
# Define array of phenotypes.
# [name of phenotype for analysis description];[table name phenotype suffix];[dependent variable column in table]
phenotypes_instances=()
phenotypes_instances+=("vitamin_d_imputation;_vitamin_d_imputation;vitamin_d_imputation")

##########
# Assemble details for batch instances.
for cohort_model_instance in "${cohorts_models_instances[@]}"; do
  # Separate fields from instance.
  IFS=";" read -r -a array <<< "${cohort_model_instance}"
  cohort_model_name="${array[0]}" # name of cohort and model for analysis description
  table_cohort_prefix="${array[1]}" # table name prefix specific to cohort and model
  covariates_specific="${array[2]}" # names of columns in table for covariate variables specific to analysis
  for phenotype_instance in "${phenotypes_instances[@]}"; do
    # Separate fields from instance.
    IFS=";" read -r -a array <<< "${phenotype_instance}"
    phenotype_name="${array[0]}" # name of phenotype for unique analysis description
    table_phenotype_suffix="${array[1]}" # phenotype specific suffix to identify table
    phenotypes="${array[2]}" # names of columns in table for phenotype variables
    # Organize variables.
    name_study="${cohort_model_name}_${phenotype_name}" # unique name for study analysis for parent directory
    table_phenotypes_covariates="${table_cohort_prefix}${table_phenotype_suffix}.tsv" # name of table of phenotypes and covariates
    covariates="${covariates_specific}${covariates_genotype}" # names of columns in table for covariate variables
    # Assemble details for batch instance.
    instance="${name_study};${table_phenotypes_covariates};${phenotypes};${covariates}"
    echo $instance
    echo $instance >> $path_batch_instances
  done
done

##########
# Summary of batch instances.

# Array pattern.
#name_study="${array[0]}"
#table_phenotypes_covariates="${array[1]}"
#phenotypes="${array[2]}"
#covariates="${array[3]}"

# Read batch instances.
readarray -t batch_instances < $path_batch_instances
batch_instances_count=${#batch_instances[@]}
echo "----------"
echo "count of batch instances: " $batch_instances_count
echo "first batch instance: " ${batch_instances[0]} # notice base-zero indexing
echo "last batch instance: " ${batch_instances[batch_instances_count - 1]}

if true; then
  # Submit array batch to Sun Grid Engine.
  # Array batch indices must start at one (not zero).
  echo "----------------------------------------------------------------------"
  echo "Submit array of batches to Sun Grid Engine."
  echo "----------------------------------------------------------------------"
  qsub -t 1-${batch_instances_count}:1 \
  -o "${path_gwas_container}/out.txt" -e "${path_gwas_container}/error.txt" \
  "${path_scripts_record}/2-1_organize_call_run_gwas_chromosomes_plink_association.sh" \
  $path_batch_instances \
  $batch_instances_count \
  $path_stratification_tables \
  $path_gwas_container \
  $path_scripts_record \
  $path_process
fi
