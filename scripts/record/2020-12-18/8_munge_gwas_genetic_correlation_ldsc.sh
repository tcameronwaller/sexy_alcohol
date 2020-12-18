#!/bin/bash

###########################################################################
###########################################################################
###########################################################################
# ...
###########################################################################
###########################################################################
###########################################################################

echo "----------------------------------------------------------------------"
echo "----------------------------------------------------------------------"
echo "----------------------------------------------------------------------"
echo "Munge GWAS summary statistics for LDSC."
echo "----------------------------------------------------------------------"
echo "----------------------------------------------------------------------"
echo "----------------------------------------------------------------------"
echo ""
echo ""
echo ""

# Organize variables.
path_gwas_one=$1 # path to GWAS report files for phenotype one
path_gwas_two=$2 # path to GWAS report files for phenotype two
path_munge=$3 # path for munge GWAS report files
path_report=$4 # path to directory for genetic correlation report
phenotype_one=$5 # name of phenotype one
phenotype_two=$6 # name of phenotype two
path_alleles=$7 # path to reference for alleles
path_disequilibrium=$8 # path to reference for linkage disequilibrium
path_ldsc=$9 # path to LDSC

###########################################################################
# Munge GWAS summary statistics for LDSC.

path_munge_one="$path_munge/${phenotype_one}"
$path_ldsc/munge_sumstats.py \
--sumstats $path_gwas_one \
--out $path_munge_one \
#--merge-alleles $path_alleles/w_hm3.snplist

path_munge_two="$path_munge/${phenotype_two}"
$path_ldsc/munge_sumstats.py \
--sumstats $path_gwas_two \
--out $path_munge_two \
#--merge-alleles $path_alleles/w_hm3.snplist

###########################################################################
# Estimate genetic correlation in LDSC.

path_munge_one_complete="$path_munge/${phenotype_one}.sumstats.gz"
path_munge_two_complete="$path_munge/${phenotype_two}.sumstats.gz"

$path_ldsc/ldsc.py \
--rg $path_munge_one_complete,$path_munte_two_complete \
--ref-ld-chr $path_disequilibrium/eur_w_ld_chr/ \
--w-ld-chr $path_disequilibrium/eur_w_ld_chr/ \
--out $path_report
