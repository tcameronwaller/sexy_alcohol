#!/bin/bash

###########################################################################
# Organize paths.
# Read private, local file paths.
#echo "read private file path variables and organize paths..."
cd ~/paths
path_ldsc=$(<"./tools_ldsc.txt")

path_temporary=$(<"./temporary_sexy_alcohol.txt")
path_waller="$path_temporary/waller"
path_dock="$path_temporary/waller/dock"
path_genetic_correlation="$path_temporary/waller/dock/genetic_correlation"

path_access="$path_temporary/waller/dock/genetic_correlation/access"
path_disequilibrium="$path_access/disequilibrium"
path_baseline="$path_access/baseline"
path_weights="$path_access/weights"
path_frequencies="$path_access/frequencies"
path_alleles="$path_access/alleles"




###########################################################################
# Case-specific parameters and paths.
###########################################################################


path_gwas="$path_temporary/waller/dock/gwas"
path_gwas_testosterone="$path_temporary/waller/dock/gwas/female_alcohol_testosterone"
path_gwas_alcohol="$path_temporary/waller/dock/gwas/female_alcohol_quantity"

path_munge="$path_temporary/waller/dock/genetic_correlation/munge"



###########################################################################
# Execute procedure.
###########################################################################

# Echo each command to console.
#set -x
# Suppress echo each command to console.
set +x

###########################################################################
# Organize directories.

rm -r $path_genetic_correlation

# Determine whether the temporary directory structure already exists.
if [ ! -d $path_genetic_correlation ]; then
    # Directory does not already exist.
    # Create directory.
    mkdir -p $path_genetic_correlation
    mkdir -p $path_access
    mkdir -p $path_disequilibrium
    mkdir -p $path_baseline
    mkdir -p $path_weights
    mkdir -p $path_frequencies
    mkdir -p $path_alleles
    mkdir -p $path_munge
fi

###########################################################################
# Access references for LDSC.

cd $path_access

# Definitions of Simple Nucleotide Variant alleles.
wget https://data.broadinstitute.org/alkesgroup/LDSCORE/w_hm3.snplist.bz2
bunzip2 "$path_access/w_hm3.snplist.bz2"
mv "$path_access/w_hm3.snplist" "$path_alleles/w_hm3.snplist"
# w_hm3.snplist

# Linkage disequilibrium scores for European population.
# For simple heritability estimation.
wget https://data.broadinstitute.org/alkesgroup/LDSCORE/eur_w_ld_chr.tar.bz2
tar -xjvf eur_w_ld_chr.tar.bz2 -C $path_disequilibrium
# dock/access/disequilibrium/eur_w_ld_chr/*

if false; then

    # Baseline model linkage disequilibrium scores.
    # For partitioned heritability estimation by stratified LD score regression.
    wget https://data.broadinstitute.org/alkesgroup/LDSCORE/1000G_Phase3_baselineLD_v2.2_ldscores.tgz
    tar -xzvf 1000G_Phase3_baselineLD_v2.2_ldscores.tgz -C $path_baseline
    # dock/access/baseline/baselineLD.*

    # Weights.
    # For partitioned heritability estimation by stratified LD score regression.
    wget https://data.broadinstitute.org/alkesgroup/LDSCORE/1000G_Phase3_weights_hm3_no_MHC.tgz
    tar -xzvf 1000G_Phase3_weights_hm3_no_MHC.tgz -C $path_weights
    # dock/access/weights/1000G_Phase3_weights_hm3_no_MHC/weights.hm3_noMHC.*

    # Frequencies.
    # For partitioned heritability estimation by stratified LD score regression.
    wget https://data.broadinstitute.org/alkesgroup/LDSCORE/1000G_Phase3_frq.tgz
    tar -xzvf 1000G_Phase3_frq.tgz -C $path_frequencies
    # dock/access/frequencies/1000G_Phase3_frq/1000G.EUR.QC.*
fi

###########################################################################
# Organize GWAS summary statistics for LDSC.

echo "----------------------------------------------------------------------"
echo "----------------------------------------------------------------------"
echo "----------------------------------------------------------------------"
echo "Concatenate GWAS summary statistics across chromosomes."
echo "version 1"
echo "----------------------------------------------------------------------"
echo "----------------------------------------------------------------------"
echo "----------------------------------------------------------------------"
echo ""
echo ""
echo ""
echo "----------------------------------------------------------------------"
echo "Testosterone in females who consume alcohol previously or currently."
echo "----------------------------------------------------------------------"
count=22 # 22: count of chromosomes on which ran GWAS
path_gwas=$path_gwas_testosterone
#path_gwas=$path_gwas_alcohol
phenotype="testosterone"
#phenotype="alcohol_drinks_monthly"
# Concatenate GWAS reports from all chromosomes.
# Extract relevant information and format for LDSC.
# Initialize concatenation.
cd $path_gwas
path_concatenation="$path_gwas/concatenation.${phenotype}.glm.linear"
echo "SNP A1 A2 N BETA P" > $path_concatenation
for (( index=1; index<=$count; index+=1 )); do
  path_gwas_chromosome="$path_gwas/chromosome_${index}"
  echo "gwas chromosome path: "
  echo $path_gwas_chromosome
  path_report="$path_gwas_chromosome/report.${phenotype}.glm.linear"
  # Select and concatenate relevant information from chromosome reports.
  # Format of GWAS reports (".glm.linear") by PLINK2.
  # https://www.cog-genomics.org/plink/2.0/formats
  # Format of GWAS summary for LDSC.
  # https://github.com/bulik/ldsc/wiki/Heritability-and-Genetic-Correlation#reformatting-summary-statistics
  # description: ............................ PLINK2 column ... LDSC column
  # variant identifier: ..................... "ID" ............ "SNP"
  # alternate allele (effect allele): ....... "A1" ............ "A1"
  # reference allele (non-effect allele): ... "REF" ........... "A2"
  # sample size: ............................ "OBS_CT" ........ "N"
  # effect (beta): .......................... "BETA" .......... "BETA"
  # probability (p-value): .................. "P" ............. "P"
  cat $path_report | awk 'NR > 1 {print $3, $6, $4, $8, $9, $12}' >> $path_concatenation
done
echo "----------"
echo "----------"
echo "----------"
echo "after concatenation..."
head -30 $path_concatenation

echo ""
echo ""
echo ""
echo "----------------------------------------------------------------------"
echo "Alcohol consumption in females who consume alcohol previously or currently."
echo "----------------------------------------------------------------------"
count=22 # 22: count of chromosomes on which ran GWAS
path_gwas=$path_gwas_alcohol
phenotype="alcohol_drinks_monthly"
# Concatenate GWAS reports from all chromosomes.
# Extract relevant information and format for LDSC.
# Initialize concatenation.
cd $path_gwas
path_concatenation="$path_gwas/concatenation.${phenotype}.glm.linear"
echo "SNP A1 A2 N BETA P" > $path_concatenation
for (( index=1; index<=$count; index+=1 )); do
  path_gwas_chromosome="$path_gwas/chromosome_${index}"
  echo "gwas chromosome path: "
  echo $path_gwas_chromosome
  path_report="$path_gwas_chromosome/report.${phenotype}.glm.linear"
  # Select and concatenate relevant information from chromosome reports.
  cat $path_report | awk 'NR > 1 {print $3, $6, $4, $8, $9, $12}' >> $path_concatenation
done
echo "----------"
echo "----------"
echo "----------"
echo "after concatenation..."
head -30 $path_concatenation

###########################################################################
# Munge GWAS summary statistics for LDSC.

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
echo "----------------------------------------------------------------------"
echo "Testosterone in females who consume alcohol previously or currently."
echo "----------------------------------------------------------------------"
path_gwas=$path_gwas_testosterone
#path_gwas=$path_gwas_alcohol
phenotype="testosterone"
#phenotype="alcohol_drinks_monthly"
path_concatenation="$path_gwas/concatenation.${phenotype}.glm.linear"
path_munge_phenotype="$path_munge/${phenotype}"

$path_ldsc/munge_sumstats.py \
--sumstats $path_concatenation \
--out $path_munge_phenotype \
--merge-alleles $path_alleles/w_hm3.snplist

echo ""
echo ""
echo ""
echo "----------------------------------------------------------------------"
echo "Alcohol consumption in females who consume alcohol previously or currently."
echo "----------------------------------------------------------------------"
path_gwas=$path_gwas_alcohol
phenotype="alcohol_drinks_monthly"
path_concatenation="$path_gwas/concatenation.${phenotype}.glm.linear"
path_munge_phenotype="$path_munge/${phenotype}"

$path_ldsc/munge_sumstats.py \
--sumstats $path_concatenation \
--out $path_munge_phenotype \
--merge-alleles $path_alleles/w_hm3.snplist

echo "done without problem"

###########################################################################
# Estimate phenotype heritability in LDSC.

echo "----------------------------------------------------------------------"
echo "----------------------------------------------------------------------"
echo "----------------------------------------------------------------------"
echo "LDSC simple heritability estimation."
echo "----------------------------------------------------------------------"
echo "----------------------------------------------------------------------"
echo "----------------------------------------------------------------------"
echo ""
echo ""
echo ""
echo "----------------------------------------------------------------------"
echo "Testosterone in females who consume alcohol previously or currently."
echo "----------------------------------------------------------------------"

if false; then
  $path_ldsc/ldsc.py \
  --h2 $path_heritability_metabolites/${identifier}_munge.sumstats.gz \
  --ref-ld-chr $path_disequilibrium/eur_w_ld_chr/ \
  --w-ld-chr $path_disequilibrium/eur_w_ld_chr/ \
  --out ${identifier}_heritability
fi


###########################################################################
# Estimate genetic correlation in LDSC.

echo "----------------------------------------------------------------------"
echo "----------------------------------------------------------------------"
echo "----------------------------------------------------------------------"
echo "LDSC genetic correlation."
echo "----------------------------------------------------------------------"
echo "----------------------------------------------------------------------"
echo "----------------------------------------------------------------------"
echo ""
echo ""
echo ""

path_testosterone="$path_munge/testosterone.sumstats.gz"
path_alcohol="$path_munge/alcohol_drinks_monthly.sumstats.gz"

$path_ldsc/ldsc.py \
--rg $path_testosterone,$path_alcohol \
--ref-ld-chr $path_disequilibrium/eur_w_ld_chr/ \
--w-ld-chr $path_disequilibrium/eur_w_ld_chr/ \
--out "$path_genetic_correlation/testosterone_alcohol_correlation"
