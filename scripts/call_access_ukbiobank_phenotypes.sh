#!/bin/bash

#chmod u+x script.sh

###########################################################################
###########################################################################
###########################################################################
# This script organizes paths and parameters to access local information
# about persons and phenotypes in the UKBiobank.
###########################################################################
###########################################################################
###########################################################################

# Read private, local file paths.
echo "read private file path variables and organize paths..."
cd ~/paths
path_temporary=$(<"./temporary_sexy_alcohol.txt")
path_waller="$path_temporary/waller"
path_scripts="$path_waller/sexy_alcohol/scripts"
path_parameter="$path_waller/sexy_alcohol/parameter"
path_variables="$path_parameter/uk_biobank_phenotype_variables.txt"
path_dock="$path_waller/dock"
path_access="$path_dock/access"
path_ukb_phenotype=$(<"./ukbiobank_phenotype.txt")
path_exclusion="$path_ukb_phenotype/exclude.csv"
path_ukb_parameter=$(<"./ukbiobank_parameter.txt")
path_identifier_pairs="$path_ukb_parameter/link.file.csv"
path_ukb_tools=$(<"./ukbiobank_tools.txt")

# Echo each command to console.
#set -x
# Suppress echo each command to console.
set +x

# Determine whether the temporary directory structure already exists.
if [ ! -d $path_access ]; then
    # Directory does not already exist.
    # Create directory.
    mkdir -p $path_dock
    mkdir -p $path_access
fi

# Specify UKBiobank phenotype variables of interest.
# Only use this method if not using the file in the parameter directory.
#echo "specify phenotype variables to access from UKBiobank"
#echo "31 22001 21022 21002 30600" | tr -s " " "\n" > $path_variables

# Access phenotype variables and auxiliary information from UKBiobank.
/usr/bin/bash "$path_scripts/access_ukbiobank_phenotypes.sh" \
$path_variables \
$path_identifier_pairs \
$path_exclusion \
$path_ukb_phenotype \
$path_ukb_tools \
$path_access
