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
path_process=$(<"./process_sexy_alcohol.txt")
path_scripts_record="$path_process/sexy_alcohol/scripts/record/2021-07-21"
path_dock="$path_process/dock"
#path_cohorts_models="${path_dock}/organization_freeze_2021-07-08/cohorts_models"
path_cohorts_models="${path_dock}/organization_freeze_2021-07-14/cohorts_models"
path_gwas="${path_dock}/gwas/cohorts_models"

# Initialize directories.
#rm -r $path_gwas
mkdir -p $path_gwas

# Define covariates common for all cohorts.
covariates_common="genotype_pc_1,genotype_pc_2,genotype_pc_3,genotype_pc_4,genotype_pc_5,genotype_pc_6,genotype_pc_7,genotype_pc_8,genotype_pc_9,genotype_pc_10"

# Define multi-dimensional array of cohorts and covariates.

# Note:
# Each GWAS (30,000 - 200,000 persons; 22 chromosomes) requires about 5-7 hours to run on the grid.

cohorts_models=()

#cohorts_models+=("female_male;table_female_male;sex,age,body_mass_index_log,")
#cohorts_models+=("female;table_female;age,body_mass_index_log,menopause_ordinal,hormone_alteration,")
#cohorts_models+=("female_premenopause_binary;table_female_premenopause_binary;age,body_mass_index_log,menstruation_phase,hormone_alteration,")
cohorts_models+=("female_premenopause_binary_cycle;table_female_premenopause_binary;age,body_mass_index_log,menstruation_phase_cycle,hormone_alteration,")
#cohorts_models+=("female_postmenopause_binary;table_female_postmenopause_binary;age,body_mass_index_log,hormone_alteration,")
#cohorts_models+=("female_premenopause_ordinal;table_female_premenopause_ordinal;age,body_mass_index_log,menstruation_phase,hormone_alteration,")
cohorts_models+=("female_premenopause_ordinal_cycle;table_female_premenopause_ordinal;age,body_mass_index_log,menstruation_phase_cycle,hormone_alteration,")
#cohorts_models+=("female_perimenopause_ordinal;table_female_perimenopause_ordinal;age,body_mass_index_log,menstruation_phase,hormone_alteration,")
cohorts_models+=("female_perimenopause_ordinal_cycle;table_female_perimenopause_ordinal;age,body_mass_index_log,menstruation_phase_cycle,hormone_alteration,")
#cohorts_models+=("female_postmenopause_ordinal;table_female_postmenopause_ordinal;age,body_mass_index_log,hormone_alteration,")
#cohorts_models+=("male;table_male;age,body_mass_index_log,")
#cohorts_models+=("male_young;table_male_young;age,body_mass_index_log,")
#cohorts_models+=("male_old;table_male_old;age,body_mass_index_log,")

#cohorts_models+=("female_male_unadjust;table_female_male;")
#cohorts_models+=("female_unadjust;table_female;")
#cohorts_models+=("female_premenopause_binary_unadjust;table_female_premenopause_binary;")
#cohorts_models+=("female_postmenopause_binary_unadjust;table_female_postmenopause_binary;")
#cohorts_models+=("female_premenopause_ordinal_unadjust;table_female_premenopause_ordinal;")
#cohorts_models+=("female_perimenopause_ordinal_unadjust;table_female_perimenopause_ordinal;")
#cohorts_models+=("female_postmenopause_ordinal_unadjust;table_female_postmenopause_ordinal;")
#cohorts_models+=("male_unadjust;table_male;")
#cohorts_models+=("male_young_unadjust;table_male_young;")
#cohorts_models+=("male_old_unadjust;table_male_old;")

# Define array of phenotypes.
phenotypes=()
phenotypes+=("albumin_log")
phenotypes+=("albumin_imputation_log")
phenotypes+=("steroid_globulin_log")
phenotypes+=("steroid_globulin_imputation_log")
phenotypes+=("oestradiol_log")
phenotypes+=("oestradiol_free_log")
phenotypes+=("oestradiol_bioavailable_log")
phenotypes+=("oestradiol_imputation_log")
phenotypes+=("testosterone_log")
phenotypes+=("testosterone_free_log")
phenotypes+=("testosterone_bioavailable_log")
phenotypes+=("testosterone_imputation_log")
phenotypes+=("vitamin_d_log")
phenotypes+=("vitamin_d_imputation_log")

# Assemble array of batch instance details.
path_batch_instances="${path_gwas}/batch_instances.txt"
rm $path_batch_instances
for cohort_model in "${cohorts_models[@]}"; do
  for phenotype in "${phenotypes[@]}"; do
    instance="${phenotype};${cohort_model}${covariates_common}"
    echo $instance
    echo $instance >> $path_batch_instances
  done
done

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
  -o "${path_gwas}/out.txt" -e "${path_gwas}/error.txt" \
  "${path_scripts_record}/2_organize_call_run_chromosomes_plink_gwas.sh" \
  $path_batch_instances \
  $batch_instances_count \
  $path_cohorts_models \
  $path_gwas \
  $path_scripts_record
fi
