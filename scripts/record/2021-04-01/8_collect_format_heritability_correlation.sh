#!/bin/bash

###########################################################################
###########################################################################
###########################################################################
# ...
###########################################################################
###########################################################################
###########################################################################

################################################################################
# Organize argument variables.

phenotype_study=${1} # identifier of GWAS study for phenotype
cohort_hormone=${2} # identifier of GWAS study for cohort and hormone
path_source_directory=${3} # full path to source directory with GWAS summary statistics for a single cohort and hormone
path_genetic_reference=${4} # full path to parent directory with genetic reference files for LDSC
path_phenotype_gwas=${5} # full path to parent directory for formatted GWAS summary statistics for phenotype
path_study_gwas=${6} # full path to parent directory for formatted GWAS summary statistics for metabolites in study
path_study_heritability=${7} # full path to parent directory for LDSC heritability estimation for metabolites in study
path_study_genetic_correlation=${8} # full path to parent directory for LDSC genetic correlation for metabolites in study
path_scripts_record=${9} # full path to pipeline scripts
path_promiscuity_scripts=${10} # complete path to directory of scripts for z-score standardization
report=${11} # whether to print reports

################################################################################
# Derive variables.

# Report.
if [[ "$report" == "true" ]]; then
  echo "----------------------------------------------------------------------"
  echo "----------------------------------------------------------------------"
  echo "----------------------------------------------------------------------"
  echo "8_collect_format_heritability_correlation.sh"
  echo "----------------------------------------------------------------------"
  echo "----------------------------------------------------------------------"
  echo "----------------------------------------------------------------------"
  echo "phenotype study: " $phenotype_study
  echo "cohort and hormone: " $cohort_hormone
  echo "path to cohort and hormone GWAS source: " $path_source_directory
  echo "----------"
fi

###########################################################################
# Organize paths.
# Read private, local file paths.
cd ~/paths
path_ldsc=$(<"./tools_ldsc.txt")

path_alleles="$path_genetic_reference/alleles"
path_disequilibrium="$path_genetic_reference/disequilibrium"
path_baseline="$path_genetic_reference/baseline"
path_weights="$path_genetic_reference/weights"
path_frequencies="$path_genetic_reference/frequencies"

path_phenotype_gwas_munge_suffix="${path_phenotype_gwas}/gwas_munge.sumstats.gz"

path_gwas_collection="${path_study_gwas}/gwas_collection.txt"
path_gwas_format="${path_study_gwas}/gwas_format.txt"
path_gwas_format_compress="${path_gwas_format}.gz"
path_gwas_munge="${path_study_gwas}/gwas_munge"
path_gwas_munge_suffix="${path_gwas_munge}.sumstats.gz"
path_gwas_munge_log="${path_gwas_munge}.log"

path_heritability_report="${path_study_heritability}/heritability"
path_heritability_report_suffix="${path_heritability_report}.log"

path_genetic_correlation_report="${path_study_genetic_correlation}/correlation"
path_genetic_correlation_report_suffix="${path_genetic_correlation_report}.log"

###########################################################################
# Execute procedure.

# Collect information across chromosomes.
# Organize information in format for LDSC.
# Parameters.
#report="false" # "true" or "false"
/usr/bin/bash "$path_scripts_record/9_collect_format_gwas_ldsc.sh" \
$path_source_directory \
$regression_type \
$path_gwas_collection \
$path_gwas_format \
$path_gwas_format_compress \
$path_promiscuity_scripts \
$report

# Munge metabolite GWAS.
$path_ldsc/munge_sumstats.py \
--sumstats $path_gwas_format \
--out $path_gwas_munge \
--merge-alleles $path_alleles/w_hm3.snplist \
#--a1-inc

# Heritability.
$path_ldsc/ldsc.py \
--h2 $path_gwas_munge_suffix \
--ref-ld-chr $path_disequilibrium/eur_w_ld_chr/ \
--w-ld-chr $path_disequilibrium/eur_w_ld_chr/ \
--out $path_heritability_report

# Genetic correlation between metabolite and phenotype.
$path_ldsc/ldsc.py \
--rg $path_phenotype_gwas_munge_suffix,$path_gwas_munge_suffix \
--ref-ld-chr $path_disequilibrium/eur_w_ld_chr/ \
--w-ld-chr $path_disequilibrium/eur_w_ld_chr/ \
--out $path_genetic_correlation_report

###########################################################################
# Remove temporary files.
rm $path_gwas_collection
rm $path_gwas_format
rm $path_gwas_munge_suffix
rm $path_gwas_munge_log
