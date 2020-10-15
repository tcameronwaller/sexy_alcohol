#!/bin/bash

#chmod u+x script.sh

# Read in private file paths.
echo "read private file path variables and organize paths..."
cd ~/path
path_temporary=$(<"./process_temporary.txt")
path_process_one="$path_temporary/waller_albumin"
path_variables="$path_process_one/variables.txt"
path_process_two="$path_temporary/waller_albumin_script"
path_project=$(<"./project_sexy_alcohol.txt")
path_dock="$path_project/dock"
path_dock_albumin="$path_dock/albumin"
path_ukbiobank_scripts=$(<"./ukbiobank_scripts.txt")
path_pull_ukbiobank="$path_project/script/pullUKBclinical.sh"
echo $path_process

# Echo each command to console.
set -x

# Organize directories.
rm -r $path_process_one
mkdir $path_process_one
#rm -r $path_dock_albumin

# Specify UKBiobank phenotype variables of interest.
echo "specify phenotype variables to access from UKBiobank"
echo "31 22001 21022 30600 30500 30850 30830" | tr -s " " "\n" > $path_variables

# Access phenotype variables from UKBiobank using script from Anthony Batzler.
/usr/bin/bash $path_pull_ukbiobank waller_albumin $path_variables $path_process_two

# Organize information.

#mv $path_process $path_dock_albumin
