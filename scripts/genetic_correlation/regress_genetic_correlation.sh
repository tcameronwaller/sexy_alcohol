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

path_gwas="$path_temporary/waller/dock/gwas"
path_gwas_testosterone="$path_temporary/waller/dock/gwas/female_alcohol_testosterone"
path_gwas_alcohol="$path_temporary/waller/dock/gwas/female_alcohol_quantity"

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
fi

###########################################################################
# Access references for LDSC.

if false; then
    cd $path_access
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

    # Definitions of Simple Nucleotide Variant alleles.
    wget https://data.broadinstitute.org/alkesgroup/LDSCORE/w_hm3.snplist.bz2
    bunzip2 "$path_access/w_hm3.snplist.bz2"
    mv "$path_access/w_hm3.snplist" "$path_alleles/w_hm3.snplist"
    # w_hm3.snplist

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

# Iterate on chromosomes.
echo "----------------------------------------------------------------------"
echo "Iterate on that simple array with indices."
echo "----------------------------------------------------------------------"
count=22 # 22 # Count of chromosomes on which to run GWAS
for (( index=0; index<=$count; index+=1 )); do
    directory="chromosome_${index}"
    path_directory="$path_gwas_testosterone/$directory"
    echo "current chromosome path: "
    echo $path_directory
done


if false; then
    # Read instance.
    readarray -t files < $path_instances
    file=${files[$index]}
    path_file="$path_metabolite_summaries/$file"

    #file="$(basename $path_file)"
    identifier="$(cut -d'.' -f1 <<<$file)"
    #echo "metabolite identifier: " $identifier

    # Extract and organize information from summary.
    # Write information to new, temporary file.
    cd $path_heritability_metabolites
    echo "SNP A1 A2 N BETA P" > ${identifier}_new.txt
    zcat $path_file | awk 'NR > 1 {print $1, $2, $3, $16, $8, $10}' >> ${identifier}_new.txt
    #head -10 ${identifier}_new.txt

    $path_ldsc/munge_sumstats.py \
    --sumstats ${identifier}_new.txt \
    --out ${identifier}_munge \
    --merge-alleles $path_alleles/w_hm3.snplist

    # Partitioned heritability by stratified LD score regression.
    #https://github.com/bulik/ldsc/wiki/Partitioned-Heritability-from-Continuous-Annotations

    $path_ldsc/ldsc.py \
    --h2 $path_heritability_metabolites/${identifier}_munge.sumstats.gz \
    --ref-ld-chr $path_baseline/baselineLD. \
    --w-ld-chr $path_weights/1000G_Phase3_weights_hm3_no_MHC/weights.hm3_noMHC. \
    --frqfile-chr $path_frequencies/1000G_Phase3_frq/1000G.EUR.QC. \
    --overlap-annot \
    --print-coefficients \
    --print-delete-vals \
    --out ${identifier}_heritability
fi
