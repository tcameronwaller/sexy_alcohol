#!/bin/bash

#chmod u+x script.sh

###########################################################################
###########################################################################
###########################################################################
# This script organizes directories and iteration instances then submits
# script "regress_metabolite_heritability.sh" to the Sun Grid Engine.

# version check: 1

###########################################################################
###########################################################################
###########################################################################

# Organize paths.
# Read private, local file paths.
echo "read private file path variables and organize paths..."
cd ~/paths
path_temporary=$(<"./processing_sexy_alcohol.txt")
path_waller="$path_temporary/waller"
path_scripts="$path_waller/sexy_alcohol/scripts/record/2021-02-25"
path_dock="$path_temporary/waller/dock"
path_gwas="$path_dock/gwas"

# Initialize directories.
#rm -r $path_gwas
if [ ! -d $path_gwas ]; then
    # Directory does not already exist.
    # Create directory.
    mkdir -p $path_gwas
fi


if false; then

  # Covariates: sex, age, body_mass_index_log
  # table_female_male_oestradiol.tsv ... "oestradiol_log"
  # table_female_male_testosterone.tsv ... "testosterone_log"
  # table_female_male_steroid_globulin.tsv ... "steroid_globulin_log"
  # table_female_male_albumin.tsv ... "albumin_log"

  # Jobs: ___, ___
  # Parameters.
  table_name="table_female_male_oestradiol.tsv"
  cohort_comparison="female_male_oestradiol"
  hormone="oestradiol_log"
  covariates="sex,age,body_mass_index_log,genotype_pc_1,genotype_pc_2,genotype_pc_3,genotype_pc_4,genotype_pc_5,genotype_pc_6,genotype_pc_7,genotype_pc_8,genotype_pc_9,genotype_pc_10"
  /usr/bin/bash "$path_scripts/2_submit_gwas_cohorts_phenotypes.sh" \
  $table_name \
  $cohort_comparison \
  $hormone \
  $covariates \
  $path_scripts \
  $path_dock

  # Jobs: ___, ___
  # Parameters.
  table_name="table_female_male_testosterone.tsv"
  cohort_comparison="female_male_testosterone"
  hormone="testosterone_log"
  covariates="sex,age,body_mass_index_log,genotype_pc_1,genotype_pc_2,genotype_pc_3,genotype_pc_4,genotype_pc_5,genotype_pc_6,genotype_pc_7,genotype_pc_8,genotype_pc_9,genotype_pc_10"
  /usr/bin/bash "$path_scripts/2_submit_gwas_cohorts_phenotypes.sh" \
  $table_name \
  $cohort_comparison \
  $hormone \
  $covariates \
  $path_scripts \
  $path_dock

  # Jobs: ___, ___
  # Parameters.
  table_name="table_female_male_steroid_globulin.tsv"
  cohort_comparison="female_male_steroid_globulin"
  hormone="steroid_globulin_log"
  covariates="sex,age,body_mass_index_log,genotype_pc_1,genotype_pc_2,genotype_pc_3,genotype_pc_4,genotype_pc_5,genotype_pc_6,genotype_pc_7,genotype_pc_8,genotype_pc_9,genotype_pc_10"
  /usr/bin/bash "$path_scripts/2_submit_gwas_cohorts_phenotypes.sh" \
  $table_name \
  $cohort_comparison \
  $hormone \
  $covariates \
  $path_scripts \
  $path_dock

  # Jobs: ___, ___
  # Parameters.
  table_name="table_female_male_albumin.tsv"
  cohort_comparison="female_male_albumin"
  hormone="albumin_log"
  covariates="sex,age,body_mass_index_log,genotype_pc_1,genotype_pc_2,genotype_pc_3,genotype_pc_4,genotype_pc_5,genotype_pc_6,genotype_pc_7,genotype_pc_8,genotype_pc_9,genotype_pc_10"
  /usr/bin/bash "$path_scripts/2_submit_gwas_cohorts_phenotypes.sh" \
  $table_name \
  $cohort_comparison \
  $hormone \
  $covariates \
  $path_scripts \
  $path_dock

  # Covariates: age, body_mass_index_log, menopause
  # table_female_oestradiol.tsv ... "oestradiol_log"
  # table_female_testosterone.tsv ... "testosterone_log"
  # table_female_steroid_globulin.tsv ... "steroid_globulin_log"
  # table_female_albumin.tsv ... "albumin_log"

  # Jobs: ___, ___
  # Parameters.
  table_name="table_female_oestradiol.tsv"
  cohort_comparison="female_oestradiol"
  hormone="oestradiol_log"
  covariates="age,body_mass_index_log,menopause,genotype_pc_1,genotype_pc_2,genotype_pc_3,genotype_pc_4,genotype_pc_5,genotype_pc_6,genotype_pc_7,genotype_pc_8,genotype_pc_9,genotype_pc_10"
  /usr/bin/bash "$path_scripts/2_submit_gwas_cohorts_phenotypes.sh" \
  $table_name \
  $cohort_comparison \
  $hormone \
  $covariates \
  $path_scripts \
  $path_dock

  # Jobs: ___, ___
  # Parameters.
  table_name="table_female_testosterone.tsv"
  cohort_comparison="female_testosterone"
  hormone="testosterone_log"
  covariates="age,body_mass_index_log,menopause,genotype_pc_1,genotype_pc_2,genotype_pc_3,genotype_pc_4,genotype_pc_5,genotype_pc_6,genotype_pc_7,genotype_pc_8,genotype_pc_9,genotype_pc_10"
  /usr/bin/bash "$path_scripts/2_submit_gwas_cohorts_phenotypes.sh" \
  $table_name \
  $cohort_comparison \
  $hormone \
  $covariates \
  $path_scripts \
  $path_dock

  # Jobs: ___, ___
  # Parameters.
  table_name="table_female_steroid_globulin.tsv"
  cohort_comparison="female_steroid_globulin"
  hormone="steroid_globulin_log"
  covariates="age,body_mass_index_log,menopause,genotype_pc_1,genotype_pc_2,genotype_pc_3,genotype_pc_4,genotype_pc_5,genotype_pc_6,genotype_pc_7,genotype_pc_8,genotype_pc_9,genotype_pc_10"
  /usr/bin/bash "$path_scripts/2_submit_gwas_cohorts_phenotypes.sh" \
  $table_name \
  $cohort_comparison \
  $hormone \
  $covariates \
  $path_scripts \
  $path_dock

  # Jobs: ___, ___
  # Parameters.
  table_name="table_female_albumin.tsv"
  cohort_comparison="female_albumin"
  hormone="albumin_log"
  covariates="age,body_mass_index_log,menopause,genotype_pc_1,genotype_pc_2,genotype_pc_3,genotype_pc_4,genotype_pc_5,genotype_pc_6,genotype_pc_7,genotype_pc_8,genotype_pc_9,genotype_pc_10"
  /usr/bin/bash "$path_scripts/2_submit_gwas_cohorts_phenotypes.sh" \
  $table_name \
  $cohort_comparison \
  $hormone \
  $covariates \
  $path_scripts \
  $path_dock

  # Covariates: age, body_mass_index_log
  # table_female_premenopause_oestradiol.tsv ... "oestradiol_log"
  # table_female_premenopause_testosterone.tsv ... "testosterone_log"
  # table_female_premenopause_steroid_globulin.tsv ... "steroid_globulin_log"
  # table_female_premenopause_albumin.tsv ... "albumin_log"

  # Jobs: ___, ___
  # Parameters.
  table_name="table_female_premenopause_oestradiol.tsv"
  cohort_comparison="female_premenopause_oestradiol"
  hormone="oestradiol_log"
  covariates="age,body_mass_index_log,genotype_pc_1,genotype_pc_2,genotype_pc_3,genotype_pc_4,genotype_pc_5,genotype_pc_6,genotype_pc_7,genotype_pc_8,genotype_pc_9,genotype_pc_10"
  /usr/bin/bash "$path_scripts/2_submit_gwas_cohorts_phenotypes.sh" \
  $table_name \
  $cohort_comparison \
  $hormone \
  $covariates \
  $path_scripts \
  $path_dock

  # Jobs: ___, ___
  # Parameters.
  table_name="table_female_premenopause_testosterone.tsv"
  cohort_comparison="female_premenopause_testosterone"
  hormone="testosterone_log"
  covariates="age,body_mass_index_log,genotype_pc_1,genotype_pc_2,genotype_pc_3,genotype_pc_4,genotype_pc_5,genotype_pc_6,genotype_pc_7,genotype_pc_8,genotype_pc_9,genotype_pc_10"
  /usr/bin/bash "$path_scripts/2_submit_gwas_cohorts_phenotypes.sh" \
  $table_name \
  $cohort_comparison \
  $hormone \
  $covariates \
  $path_scripts \
  $path_dock

  # Jobs: ___, ___
  # Parameters.
  table_name="table_female_premenopause_steroid_globulin.tsv"
  cohort_comparison="female_premenopause_steroid_globulin"
  hormone="steroid_globulin_log"
  covariates="age,body_mass_index_log,genotype_pc_1,genotype_pc_2,genotype_pc_3,genotype_pc_4,genotype_pc_5,genotype_pc_6,genotype_pc_7,genotype_pc_8,genotype_pc_9,genotype_pc_10"
  /usr/bin/bash "$path_scripts/2_submit_gwas_cohorts_phenotypes.sh" \
  $table_name \
  $cohort_comparison \
  $hormone \
  $covariates \
  $path_scripts \
  $path_dock

  # Jobs: ___, ___
  # Parameters.
  table_name="table_female_premenopause_albumin.tsv"
  cohort_comparison="female_premenopause_albumin"
  hormone="albumin_log"
  covariates="age,body_mass_index_log,genotype_pc_1,genotype_pc_2,genotype_pc_3,genotype_pc_4,genotype_pc_5,genotype_pc_6,genotype_pc_7,genotype_pc_8,genotype_pc_9,genotype_pc_10"
  /usr/bin/bash "$path_scripts/2_submit_gwas_cohorts_phenotypes.sh" \
  $table_name \
  $cohort_comparison \
  $hormone \
  $covariates \
  $path_scripts \
  $path_dock


  # Covariates: age, body_mass_index_log
  # table_male_oestradiol.tsv ... "oestradiol_log"
  # table_male_testosterone.tsv ... "testosterone_log"
  # table_male_steroid_globulin.tsv ... "steroid_globulin_log"
  # table_male_albumin.tsv ... "albumin_log"

  # Jobs: ___, ___
  # Parameters.
  table_name="table_male_oestradiol.tsv"
  cohort_comparison="male_oestradiol"
  hormone="oestradiol_log"
  covariates="age,body_mass_index_log,genotype_pc_1,genotype_pc_2,genotype_pc_3,genotype_pc_4,genotype_pc_5,genotype_pc_6,genotype_pc_7,genotype_pc_8,genotype_pc_9,genotype_pc_10"
  /usr/bin/bash "$path_scripts/2_submit_gwas_cohorts_phenotypes.sh" \
  $table_name \
  $cohort_comparison \
  $hormone \
  $covariates \
  $path_scripts \
  $path_dock

  # Jobs: ___, ___
  # Parameters.
  table_name="table_male_testosterone.tsv"
  cohort_comparison="male_testosterone"
  hormone="testosterone_log"
  covariates="age,body_mass_index_log,genotype_pc_1,genotype_pc_2,genotype_pc_3,genotype_pc_4,genotype_pc_5,genotype_pc_6,genotype_pc_7,genotype_pc_8,genotype_pc_9,genotype_pc_10"
  /usr/bin/bash "$path_scripts/2_submit_gwas_cohorts_phenotypes.sh" \
  $table_name \
  $cohort_comparison \
  $hormone \
  $covariates \
  $path_scripts \
  $path_dock

  # Jobs: ___, ___
  # Parameters.
  table_name="table_male_steroid_globulin.tsv"
  cohort_comparison="male_steroid_globulin"
  hormone="steroid_globulin_log"
  covariates="age,body_mass_index_log,genotype_pc_1,genotype_pc_2,genotype_pc_3,genotype_pc_4,genotype_pc_5,genotype_pc_6,genotype_pc_7,genotype_pc_8,genotype_pc_9,genotype_pc_10"
  /usr/bin/bash "$path_scripts/2_submit_gwas_cohorts_phenotypes.sh" \
  $table_name \
  $cohort_comparison \
  $hormone \
  $covariates \
  $path_scripts \
  $path_dock

  # Jobs: ___, ___
  # Parameters.
  table_name="table_male_albumin.tsv"
  cohort_comparison="male_albumin"
  hormone="albumin_log"
  covariates="age,body_mass_index_log,genotype_pc_1,genotype_pc_2,genotype_pc_3,genotype_pc_4,genotype_pc_5,genotype_pc_6,genotype_pc_7,genotype_pc_8,genotype_pc_9,genotype_pc_10"
  /usr/bin/bash "$path_scripts/2_submit_gwas_cohorts_phenotypes.sh" \
  $table_name \
  $cohort_comparison \
  $hormone \
  $covariates \
  $path_scripts \
  $path_dock


fi

if true; then

  # Covariates: age, body_mass_index_log
  # table_female_postmenopause_oestradiol.tsv ... "oestradiol_log"
  # table_female_postmenopause_testosterone.tsv ... "testosterone_log"
  # table_female_postmenopause_steroid_globulin.tsv ... "steroid_globulin_log"
  # table_female_postmenopause_albumin.tsv ... "albumin_log"

  # Jobs: ___, ___
  # Parameters.
  table_name="table_female_postmenopause_oestradiol.tsv"
  cohort_comparison="female_postmenopause_oestradiol"
  hormone="oestradiol_log"
  covariates="age,body_mass_index_log,genotype_pc_1,genotype_pc_2,genotype_pc_3,genotype_pc_4,genotype_pc_5,genotype_pc_6,genotype_pc_7,genotype_pc_8,genotype_pc_9,genotype_pc_10"
  /usr/bin/bash "$path_scripts/2_submit_gwas_cohorts_phenotypes.sh" \
  $table_name \
  $cohort_comparison \
  $hormone \
  $covariates \
  $path_scripts \
  $path_dock

  # Jobs: ___, ___
  # Parameters.
  table_name="table_female_postmenopause_testosterone.tsv"
  cohort_comparison="female_postmenopause_testosterone"
  hormone="testosterone_log"
  covariates="age,body_mass_index_log,genotype_pc_1,genotype_pc_2,genotype_pc_3,genotype_pc_4,genotype_pc_5,genotype_pc_6,genotype_pc_7,genotype_pc_8,genotype_pc_9,genotype_pc_10"
  /usr/bin/bash "$path_scripts/2_submit_gwas_cohorts_phenotypes.sh" \
  $table_name \
  $cohort_comparison \
  $hormone \
  $covariates \
  $path_scripts \
  $path_dock

  # Jobs: ___, ___
  # Parameters.
  table_name="table_female_postmenopause_steroid_globulin.tsv"
  cohort_comparison="female_postmenopause_steroid_globulin"
  hormone="steroid_globulin_log"
  covariates="age,body_mass_index_log,genotype_pc_1,genotype_pc_2,genotype_pc_3,genotype_pc_4,genotype_pc_5,genotype_pc_6,genotype_pc_7,genotype_pc_8,genotype_pc_9,genotype_pc_10"
  /usr/bin/bash "$path_scripts/2_submit_gwas_cohorts_phenotypes.sh" \
  $table_name \
  $cohort_comparison \
  $hormone \
  $covariates \
  $path_scripts \
  $path_dock

  # Jobs: ___, ___
  # Parameters.
  table_name="table_female_postmenopause_albumin.tsv"
  cohort_comparison="female_postmenopause_albumin"
  hormone="albumin_log"
  covariates="age,body_mass_index_log,genotype_pc_1,genotype_pc_2,genotype_pc_3,genotype_pc_4,genotype_pc_5,genotype_pc_6,genotype_pc_7,genotype_pc_8,genotype_pc_9,genotype_pc_10"
  /usr/bin/bash "$path_scripts/2_submit_gwas_cohorts_phenotypes.sh" \
  $table_name \
  $cohort_comparison \
  $hormone \
  $covariates \
  $path_scripts \
  $path_dock

fi
