#!/bin/bash

###########################################################################
###########################################################################
###########################################################################
# ...
###########################################################################
###########################################################################
###########################################################################

################################################################################
# Organize paths.
# Read private, local file paths.
cd ~/paths
path_gwas_summaries=$(<"./gwas_summaries_waller_metabolism.txt")
path_process=$(<"./process_sexy_alcohol.txt")

path_promiscuity_scripts="${path_process}/promiscuity/scripts"

path_dock="$path_process/dock"
path_genetic_reference="${path_dock}/access/genetic_reference"

#path_gwas_source="${path_dock}/gwas" # selection
path_gwas_target="${path_dock}/gwas_process" # selection

path_heritability="${path_dock}/heritability/community_studies" # store in container to parallel "cohorts_models" containers

###########################################################################
# Execute procedure.

# Version check...

# Initialize directories.
#rm -r $path_gwas_target
#rm -r $path_heritability
#mkdir -p $path_gwas_target
#mkdir -p $path_heritability

# Organize information about studies.

# Define multi-dimensional array of cohorts and covariates.
# Review:
# 3 May 2021: TCW reviewed study README's, confirmed source files, and confirmed format scripts


studies=()
#studies+=("30124842_yengo_2018;coefficient;${path_gwas_summaries}/30124842_yengo_2018/Meta-analysis_Locke_et_al+UKBiobank_2018_UPDATED.txt.gz")
#studies+=("30239722_pulit_2018;${path_gwas_summaries}/30239722_pulit_2018/whradjbmi.giant-ukbb.meta-analysis.combined.23May2018.txt.gz")
#studies+=("30482948_walters_2018_all;${path_gwas_summaries}/30482948_walters_2018/pgc_alcdep.discovery.aug2018_release.txt.gz")
#studies+=("30482948_walters_2018_eur;${path_gwas_summaries}/30482948_walters_2018/pgc_alcdep.eur_discovery.aug2018_release.txt.gz")
studies+=("30482948_walters_2018_eur_unrel;z_score;${path_gwas_summaries}/30482948_walters_2018/pgc_alcdep.eur_unrelated.aug2018_release.txt.gz")
studies+=("30482948_walters_2018_female;odds_ratio;${path_gwas_summaries}/30482948_walters_2018/sex_stratification/pgc_alcdep_eur_female_public.gz")
studies+=("30482948_walters_2018_male;odds_ratio;${path_gwas_summaries}/30482948_walters_2018/sex_stratification/pgc_alcdep_eur_male_public.gz")

#studies+=("30718901_howard_2019;${path_gwas_summaries}/30718901_howard_2019/PGC_UKB_depression_genome-wide.txt.gz")
#studies+=("29906448_ruderfer_2018_scz_vs_ctl;${path_gwas_summaries}/29906448_ruderfer_2018/sczvscont-sumstat.gz")
#studies+=("29906448_ruderfer_2018_scz_bpd_vs_ctl;${path_gwas_summaries}/29906448_ruderfer_2018/BDSCZvsCONT.sumstats.gz")
#studies+=("29906448_ruderfer_2018_scz_vs_bpd;${path_gwas_summaries}/29906448_ruderfer_2018/SCZvsBD.sumstats.gz")
#studies+=("29906448_ruderfer_2018_bpd_vs_ctl;${path_gwas_summaries}/29906448_ruderfer_2018/BDvsCONT.sumstats.gz")
#studies+=("00000000_ripke_2021;${path_gwas_summaries}/00000000_ripke_2021/PGC3_SCZ_wave3_public.v2.tsv.gz")
#studies+=("31043756_stahl_2019;${path_gwas_summaries}/31043756_stahl_2019/daner_PGC_BIP32b_mds7a_0416a.gz")
studies+=("34002096_mullins_2021_all;coefficient;${path_gwas_summaries}/34002096_mullins_2021/pgc-bip2021-all.vcf.tsv.gz")
studies+=("34002096_mullins_2021_bpd1;coefficient;${path_gwas_summaries}/34002096_mullins_2021/pgc-bip2021-BDI.vcf.tsv.gz")
studies+=("34002096_mullins_2021_bpd2;coefficient;${path_gwas_summaries}/34002096_mullins_2021/pgc-bip2021-BDII.vcf.tsv.gz")

# Organize information in format for LDSC.
for study_details in "${studies[@]}"; do
  # Read information.
  IFS=";" read -r -a array <<< "${study_details}"
  study="${array[0]}"
  response="${array[1]}"
  path_gwas_source_file="${array[2]}"
  # Organize paths.
  path_gwas_target_parent="${path_gwas_target}/${study}"
  path_gwas_concatenation_compress="${path_gwas_target_parent}/gwas_concatenation.txt.gz"
  path_heritability_parent="${path_heritability}/${study}"
  # Initialize directories.
  rm -r $path_gwas_target_parent
  rm -r $path_heritability_parent
  mkdir -p $path_gwas_target_parent
  mkdir -p $path_heritability_parent
  # Copy source file to parent directory.
  cp ${path_gwas_source_file} ${path_gwas_concatenation_compress}

  # Scripts.
  path_script_drive_gwas_format="${path_promiscuity_scripts}/gwas_process/drive_gwas_format.sh"
  path_script_gwas_format="${path_promiscuity_scripts}/gwas_process/format_gwas_ldsc/format_gwas_ldsc_${study}.sh"
  path_script_drive_ldsc_gwas_munge_heritability="${path_promiscuity_scripts}/gwas_process/drive_ldsc_gwas_munge_heritability.sh"

  ##########
  # Format adjustment.
  # Parameters.
  report="true" # "true" or "false"
  /usr/bin/bash "${path_script_drive_gwas_format}" \
  $path_gwas_concatenation_compress \
  $path_gwas_target_parent \
  $path_promiscuity_scripts \
  $path_script_gwas_format \
  $report

  ##########
  # Munge and heritability.
  # Parameters.
  path_gwas_source_parent=$path_gwas_target_parent
  report="true" # "true" or "false"
  /usr/bin/bash "${path_script_drive_ldsc_gwas_munge_heritability}" \
  $path_gwas_source_parent \
  $path_gwas_target_parent \
  $path_heritability_parent \
  $path_genetic_reference \
  $response \
  $report

done
