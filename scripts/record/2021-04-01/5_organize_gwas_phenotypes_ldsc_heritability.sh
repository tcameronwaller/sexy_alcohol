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
echo "read private file path variables and organize paths..."
cd ~/paths
path_gwas_summaries=$(<"./gwas_summaries_waller_metabolism.txt")
path_temporary=$(<"./processing_sexy_alcohol.txt")

path_waller="$path_temporary/waller"
path_sexy_alcohol="$path_waller/sexy_alcohol"
path_scripts_record="$path_waller/sexy_alcohol/scripts/record/2021-04-01"
path_promiscuity_scripts="$path_waller/promiscuity/scripts"
path_scripts_format="$path_waller/promiscuity/scripts/format_gwas_ldsc"

path_dock="$path_waller/dock"
path_genetic_reference="$path_dock/access/genetic_reference"
path_gwas="$path_dock/gwas"
path_heritability="$path_dock/heritability"
path_genetic_correlation="$path_dock/genetic_correlation"

###########################################################################
# Execute procedure.

# Initialize directories.
#rm -r $path_gwas
#rm -r $path_heritability
#rm -r $path_genetic_correlation
if [ ! -d $path_gwas ]; then
    # Directory does not already exist.
    # Create directory.
    mkdir -p $path_gwas
fi
if [ ! -d $path_heritability ]; then
    # Directory does not already exist.
    # Create directory.
    mkdir -p $path_heritability
fi
if [ ! -d $path_genetic_correlation ]; then
    # Directory does not already exist.
    # Create directory.
    mkdir -p $path_genetic_correlation
fi

# Organize information in format for LDSC.

# Walters et al, Nature Neuroscience, 2018 (PubMed:30482948)
# phenotype: alcohol dependence
study="30482948_walters_2018"
source_file="pgc_alcdep.discovery.aug2018_release.txt.gz"
path_source_directory="${path_gwas_summaries}/${study}"
path_source_file="${path_source_directory}/${source_file}"
path_script_gwas_format="${path_scripts_format}/format_gwas_ldsc_${study}.sh"
report="true" # "true" or "false"
/usr/bin/bash "$path_scripts_record/6_organize_gwas_phenotype_ldsc_heritability.sh" \
$study \
$source_file \
$path_source_file \
$path_genetic_reference \
$path_gwas \
$path_heritability \
$path_genetic_correlation \
$path_script_gwas_format \
$path_promiscuity_scripts \
$report
