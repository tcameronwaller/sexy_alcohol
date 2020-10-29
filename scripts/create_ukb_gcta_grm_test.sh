#!/bin/bash

#chmod u+x script.sh


###########################################################################


# Read private, local file paths.
echo "read private file path variables and organize paths..."
cd ~/paths
path_temporary=$(<"./temporary_sexy_alcohol.txt")
path_waller="$path_temporary/waller"
path_dock="$path_waller/dock"
path_relation="$path_dock/relation"
path_plink2=$(<"./tools_plink2.txt")
path_gcta=$(<"./tools_gcta.txt")
path_ukb_genotype=$(<"./ukbiobank_genotype.txt")


# Echo each command to console.
set -x

# Determine whether the temporary directory structure already exists.
if [ ! -d $path_relation ]; then
    # Directory does not already exist.
    # Create directory.
    mkdir -p $path_dock
    mkdir -p $path_relation
    mkdir -p "$path_relation/chromosome_21"
fi

###########################################################################
##########
# Plan
##########
# 1. calculate GRMs separately for each chromosome 1-22
# 2. calculate chromosomal GRMs in 10 parts
# 3. combine GRM parts for each chromosome
# 4. merge chromosomal GRMs

# Combine parts...
# https://cnsgenomics.com/software/gcta/#MakingaGRM

# Combine separate GRMs for each chromosome...
# https://cnsgenomics.com/software/gcta/#Tutorial
# $path_gcta --mgrm grm_chrs.txt --make-grm --out test
###########
# grm_chrs.txt
# path-to-chr1
# path-to-chr2
# etc...
###########################################################################


# Create Genetic Relationship Matrix in GCTA.
chromosome=21

$path_gcta --bgen "$path_ukb_genotype/Chromosome/ukb_imp_chr${chromosome}_v3.bgen" \
--sample "$path_ukb_genotype/Chromosome/ukb46237_imp_chr${chromosome}_v3_s487320.sample" \
--maf 0.01 --make-grm-part 50 1 \
--threads 4 \
--out "$path_relation/chromosome_${chromosome}"


###########################################################################
