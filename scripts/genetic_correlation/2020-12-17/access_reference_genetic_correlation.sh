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
    mkdir -p $path_alleles
    mkdir -p $path_disequilibrium
    mkdir -p $path_baseline
    mkdir -p $path_weights
    mkdir -p $path_frequencies
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
