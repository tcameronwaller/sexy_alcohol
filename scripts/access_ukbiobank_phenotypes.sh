#!/bin/bash

#chmod u+x script.sh

# Read in private file paths.
echo "read private file path variables and organize paths..."
cd ~/path
path_temporary=$(<"./process_temporary.txt")
path_process="$path_temporary/waller_albumin"
path_variables="$path_process/variables.txt"
path_project=$(<"./project_sexy_alcohol.txt")
path_dock="$path_project/dock"
path_dock_albumin="$path_dock/albumin"
path_ukbiobank_scripts=$(<"./ukbiobank_scripts.txt")
path_pull_ukbiobank="$path_project/script/pullUKBclinical_edit.sh"
echo $path_process

# TODO: eventually edit the pullUKBclinical_edit.sh further
# TODO: introduce column headers within this script?
# TODO: the UKBiobank converter tool seems to sort the variables by their field identifiers (ex: 31 before 21022)

# Echo each command to console.
set -x

# Organize directories.
rm -r $path_process
mkdir -p $path_process
#rm -r $path_dock_albumin

# Specify UKBiobank phenotype variables of interest.
echo "specify phenotype variables to access from UKBiobank"
echo "31 21022 30600" | tr -s " " "\n" > $path_variables

# Access phenotype variables from UKBiobank using script from Anthony Batzler.
/usr/bin/bash $path_pull_ukbiobank waller_albumin $path_variables $path_process

# Organize information.

#mv $path_process $path_dock_albumin
