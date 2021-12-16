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


# TODO: TCW 14 December 2021
# TODO: specify dependent variable separately from table name
# TODO: needs to mirror however I implement for the "detection" logistic phenotypes

# Organize paths.
# Read private, local file paths.
echo "read private file path variables and organize paths..."
cd ~/paths
path_process=$(<"./process_sexy_alcohol.txt")
path_scripts_record="$path_process/sexy_alcohol/scripts/record/2021-12-02"
path_dock="$path_process/dock"

path_cohorts_models="${path_dock}/stratification_2021-11-24/cohorts_models_linear"
#path_cohorts_models="${path_dock}/stratification/cohorts_models_logistic"

#path_gwas="${path_dock}/gwas_raw/cohorts_models_linear_measurement"          # 72 GWAS; TCW started at 23:20 on 24 November 2021
#path_gwas="${path_dock}/gwas_raw/cohorts_models_linear_measurement_unadjust" # 72 GWAS; TCW started at 23:36 on 24 November 2021
path_gwas="${path_dock}/gwas_raw/cohorts_models_linear_measurement_unadjust" # 36 GWAS; TCW started at 13:58 on 1 December 2021
# Note (TCW 1 December 2021):
# It was necessary to repeat the GWAS run for batch "cohorts_models_linear_measurement_unadjust" in females.
# I deleted this batch by accident during post-processing.
# I copied the batch "cohorts_models_linear_measurement_unadjust" in males.

#path_gwas="${path_dock}/gwas_raw/cohorts_models_linear_imputation"           # 72 GWAS; TCW started at 23:12 on 24 November 2021
#path_gwas="${path_dock}/gwas_raw/cohorts_models_linear_imputation_unadjust"  # 72 GWAS; TCW started at 00:08 on 25 November 2021

#path_gwas="${path_dock}/gwas_raw/cohorts_models_logistic_detection"          # 63 GWAS; TCW started at ___ on 24 November 2021
#path_gwas="${path_dock}/gwas_raw/cohorts_models_logistic_detection_unadjust" # 63 GWAS; TCW started at ___ on 24 November 2021

# TODO: TCW 27 October 2021
# Too complex... consider dropping?
#path_gwas="${path_dock}/gwas/cohorts_models_linear_order"                # 40 GWAS; TCW started at ___ on ___ 2021
#path_gwas="${path_dock}/gwas/cohorts_models_linear_order_unadjust"       # 40 GWAS; TCW started at ___ on ___ 2021

# Initialize directories.
rm -r $path_gwas
mkdir -p $path_gwas

##########
##########
##########
# Assemble a list of analysis instances with common patterns.

# Assemble array of batch instance details.
path_batch_instances="${path_gwas}/batch_instances.txt"
rm $path_batch_instances

##########
# General models.

# Define covariates common for all cohorts.
covariates_common="genotype_pc_1,genotype_pc_2,genotype_pc_3,genotype_pc_4,genotype_pc_5,genotype_pc_6,genotype_pc_7,genotype_pc_8,genotype_pc_9,genotype_pc_10"

# Define multi-dimensional array of cohorts and model covariates.
cohorts_models=()

# Adjusted.
#cohorts_models+=("female;table_female;age,body_log,menopause_ordinal,hormone_alteration,")
#cohorts_models+=("female_premenopause;table_female_premenopause;age,body_log,menstruation_phase_cycle,hormone_alteration,")
#cohorts_models+=("female_perimenopause;table_female_perimenopause;age,body_log,menstruation_phase_cycle,hormone_alteration,")
#cohorts_models+=("female_postmenopause;table_female_postmenopause;age,body_log,hormone_alteration,")
#cohorts_models+=("male;table_male;age,body_log,")
#cohorts_models+=("male_age_low;table_male_age_low;age,body_log,")
#cohorts_models+=("male_age_middle;table_male_age_middle;age,body_log,")
#cohorts_models+=("male_age_high;table_male_age_high;age,body_log,")

# Unadjusted.
cohorts_models+=("female;table_female;")
cohorts_models+=("female_premenopause;table_female_premenopause;")
cohorts_models+=("female_perimenopause;table_female_perimenopause;")
cohorts_models+=("female_postmenopause;table_female_postmenopause;")
#cohorts_models+=("male;table_male;")
#cohorts_models+=("male_age_low;table_male_age_low;")
#cohorts_models+=("male_age_middle;table_male_age_middle;")
#cohorts_models+=("male_age_high;table_male_age_high;")

# Define array of phenotypes.
phenotypes=()

phenotypes+=("albumin") # cohorts_models_linear_measurement
#phenotypes+=("albumin_imputation") # cohorts_models_linear_imputation
###phenotypes+=("albumin_order")
###phenotypes+=("albumin_detection")

phenotypes+=("steroid_globulin_log") # cohorts_models_linear_measurement
#phenotypes+=("steroid_globulin_imputation_log") # cohorts_models_linear_imputation
###phenotypes+=("steroid_globulin_order")
###phenotypes+=("steroid_globulin_detection")

phenotypes+=("oestradiol_log") # cohorts_models_linear_measurement
phenotypes+=("oestradiol_bioavailable_log") # cohorts_models_linear_measurement
phenotypes+=("oestradiol_free_log") # cohorts_models_linear_measurement
#phenotypes+=("oestradiol_imputation") # cohorts_models_linear_imputation
#phenotypes+=("oestradiol_bioavailable_imputation") # cohorts_models_linear_imputation
#phenotypes+=("oestradiol_free_imputation") # cohorts_models_linear_imputation
###phenotypes+=("oestradiol_order")
###phenotypes+=("oestradiol_detection")

phenotypes+=("testosterone_log") # cohorts_models_linear_measurement
phenotypes+=("testosterone_bioavailable_log") # cohorts_models_linear_measurement
phenotypes+=("testosterone_free_log") # cohorts_models_linear_measurement
#phenotypes+=("testosterone_imputation") # cohorts_models_linear_imputation
#phenotypes+=("testosterone_bioavailable_imputation") # cohorts_models_linear_imputation
#phenotypes+=("testosterone_free_imputation") # cohorts_models_linear_imputation
###phenotypes+=("testosterone_order")
###phenotypes+=("testosterone_detection")

for cohort_model in "${cohorts_models[@]}"; do
  for phenotype in "${phenotypes[@]}"; do
    instance="${phenotype};${cohort_model}${covariates_common}"
    echo $instance
    echo $instance >> $path_batch_instances
  done
done

##########
# Vitamin D models.

# Define multi-dimensional array of cohorts and model covariates.
cohorts_models=()

# Adjusted.
#cohorts_models+=("female;table_female;assessment_region,assessment_season,age,body_log,menopause_ordinal,hormone_alteration,")
#cohorts_models+=("female_premenopause;table_female_premenopause;assessment_region,assessment_season,age,body_log,menstruation_phase_cycle,hormone_alteration,")
#cohorts_models+=("female_perimenopause;table_female_perimenopause;assessment_region,assessment_season,age,body_log,menstruation_phase_cycle,hormone_alteration,")
#cohorts_models+=("female_postmenopause;table_female_postmenopause;assessment_region,assessment_season,age,body_log,hormone_alteration,")
#cohorts_models+=("male;table_male;assessment_region,assessment_season,age,body_log,")
#cohorts_models+=("male_age_low;table_male_age_low;assessment_region,assessment_season,age,body_log,")
#cohorts_models+=("male_age_middle;table_male_age_middle;assessment_region,assessment_season,age,body_log,")
#cohorts_models+=("male_age_high;table_male_age_high;assessment_region,assessment_season,age,body_log,")

# Unadjusted.
cohorts_models+=("female;table_female;assessment_region,assessment_season,")
cohorts_models+=("female_premenopause;table_female_premenopause;assessment_region,assessment_season,")
cohorts_models+=("female_perimenopause;table_female_perimenopause;assessment_region,assessment_season,")
cohorts_models+=("female_postmenopause;table_female_postmenopause;assessment_region,assessment_season,")
#cohorts_models+=("male;table_male;assessment_region,assessment_season,")
#cohorts_models+=("male_age_low;table_male_age_low;assessment_region,assessment_season,")
#cohorts_models+=("male_age_middle;table_male_age_middle;assessment_region,assessment_season,")
#cohorts_models+=("male_age_high;table_male_age_high;assessment_region,assessment_season,")

# Define array of phenotypes.
phenotypes=()

phenotypes+=("vitamin_d_log") # cohorts_models_linear_measurement
#phenotypes+=("vitamin_d_imputation_log") # cohorts_models_linear_imputation
###phenotypes+=("vitamin_d_order")
###phenotypes+=("vitamin_d_detection")

for cohort_model in "${cohorts_models[@]}"; do
  for phenotype in "${phenotypes[@]}"; do
    instance="${phenotype};${cohort_model}${covariates_common}"
    echo $instance
    echo $instance >> $path_batch_instances
  done
done

##########
# Summary of batch instances.

# Array pattern.
#phenotype="${array[0]}"
#cohort_model="${array[1]}"
#table_cohort_model="${array[2]}"
#covariates="${array[3]}"
#path_table_phenotypes_covariates="${path_cohorts_models}/${table_cohort_model}_${phenotype}.tsv"

# Read batch instances.
readarray -t batch_instances < $path_batch_instances
batch_instances_count=${#batch_instances[@]}
echo "----------"
echo "count of batch instances: " $batch_instances_count
echo "first batch instance: " ${batch_instances[0]} # notice base-zero indexing
echo "last batch instance: " ${batch_instances[batch_instances_count - 1]}

# Batches before 1 December 2021 used script "4-1..." below.
if false; then
  # Submit array batch to Sun Grid Engine.
  # Array batch indices must start at one (not zero).
  echo "----------------------------------------------------------------------"
  echo "Submit array of batches to Sun Grid Engine."
  echo "----------------------------------------------------------------------"
  qsub -t 1-${batch_instances_count}:1 \
  -o "${path_gwas}/out.txt" -e "${path_gwas}/error.txt" \
  "${path_scripts_record}/4-1_organize_call_run_chromosomes_plink_linear_gwas.sh" \
  $path_batch_instances \
  $batch_instances_count \
  $path_cohorts_models \
  $path_gwas \
  $path_scripts_record
fi

# Batches on 1 December 2021 used script "4-2..." below.
if true; then
  # Submit array batch to Sun Grid Engine.
  # Array batch indices must start at one (not zero).
  echo "----------------------------------------------------------------------"
  echo "Submit array of batches to Sun Grid Engine."
  echo "----------------------------------------------------------------------"
  qsub -t 1-${batch_instances_count}:1 \
  -o "${path_gwas}/out.txt" -e "${path_gwas}/error.txt" \
  "${path_scripts_record}/4-2_organize_call_run_gwas_chromosomes_plink_association.sh" \
  $path_batch_instances \
  $batch_instances_count \
  $path_cohorts_models \
  $path_gwas \
  $path_scripts_record \
  $path_process
fi
