#!/bin/bash

#chmod u+x script.sh

# Read in private file paths.
echo "read private file path variables and organize paths..."
cd ~/path
path_temporary=$(<"./process_temporary.txt")
path_process="$path_temporary/waller_sexy_alcohol"
path_project=$(<"./project_sexy_alcohol.txt")
path_repository="$path_project/sexy_alcohol"
path_dock="$path_project/dock"

# Echo each command to console.
set -x

# Organize directories.
rm -r $path_process
rm -r $path_dock_albumin

# Specify UKBiobank phenotype variables of interest.
echo "specify phenotype variables to access from UKBiobank"
echo "31 22001 21022 30600 30500 30850 30830" | tr -s " " "\n" > $path_variables

# Access phenotype variables from UKBiobank using script from Anthony Batzler.
/usr/bin/bash $path_pull_ukbiobank waller_albumin $path_variables $path_process

# Organize information.

mv $path_process $path_dock_albumin
