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
path_temporary=$(<"./processing_sexy_alcohol.txt")
path_waller="$path_temporary/waller"
path_scripts_record="$path_waller/sexy_alcohol/scripts/record/2021-04-26"
path_dock="$path_temporary/waller/dock"
path_cohorts="${path_dock}/organization/cohorts"
path_gwas="${path_dock}/gwas"

# Initialize directories.
#rm -r $path_gwas
#mkdir -p $path_gwas

# TODO: simplify this array... create a variable for "common covariates", and then append these to all...

# Define covariates common for all cohorts.
covariates_common="genotype_pc_1,genotype_pc_2,genotype_pc_3,genotype_pc_4,genotype_pc_5,genotype_pc_6,genotype_pc_7,genotype_pc_8,genotype_pc_9,genotype_pc_10"

# Define multi-dimensional array of cohorts and covariates.
cohorts_covariates=()
cohorts_covariates+=("female_male;sex,age,body_mass_index_log")
cohorts_covariates+=("female;age,body_mass_index_log,menopause_ordinal,hormone_alteration")
cohorts_covariates+=("female_combination;age,body_mass_index_log,menopause_hormone_category_1,menopause_hormone_category_3,menopause_hormone_category_4")
cohorts_covariates+=("female_premenopause_binary;age,body_mass_index_log,menstruation_day,hormone_alteration")
cohorts_covariates+=("female_postmenopause_binary;age,body_mass_index_log,hormone_alteration")
cohorts_covariates+=("female_premenopause_ordinal;age,body_mass_index_log,menstruation_day,hormone_alteration")
cohorts_covariates+=("female_perimenopause_ordinal;age,body_mass_index_log,menstruation_day,hormone_alteration")
cohorts_covariates+=("female_postmenopause_ordinal;age,body_mass_index_log,hormone_alteration")
cohorts_covariates+=("male;age,body_mass_index_log")
#cohorts_covariates+=("male_unadjust;table_male_unadjust_;")

# Define array of hormones.
hormones=()
hormones+=("albumin_log")
hormones+=("steroid_globulin_log")
hormones+=("oestradiol_log")
hormones+=("oestradiol_free_log")
hormones+=("testosterone_log")
hormones+=("testosterone_free_log")

# Assemble array of batch instance details.
path_batch_instances="${path_gwas}/batch_instances.txt"
rm $path_batch_instances

for cohort_covariates in "${cohorts_covariates[@]}"; do
  for hormone in "${hormones[@]}"; do
    instance="${hormone};${cohort_covariates},${covariates_common}"
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

if false; then
  # Submit array batch to Sun Grid Engine.
  # Array batch indices must start at one (not zero).
  echo "----------------------------------------------------------------------"
  echo "Submit array of batches to Sun Grid Engine."
  echo "----------------------------------------------------------------------"
  qsub -t 1-${batch_instances_count}:1 \
  -o "${path_gwas}/out.txt" -e "${path_gwas}/error.txt" \
  "${path_scripts_record}/2_organize_call_run_batch_gwas.sh" \
  $path_batch_instances \
  $batch_instances_count \
  $path_cohorts \
  $path_gwas \
  $path_scripts_record
fi
