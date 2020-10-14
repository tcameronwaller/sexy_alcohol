#!/bin/bash

#chmod u+x script.sh

# Read in private file paths.
echo "read private file path variables..."
cd ~/path
path_temporary=$(<"./process_temporary.txt")
path_out="$path_temporary/waller_test"
path_project=$(<"./project_sexy_alcohol.txt")
path_ukbiobank_scripts=$(<"./ukbiobank_scripts.txt")
path_pull_ukbiobank="$path_ukbiobank_scripts/pullUKBclinical.sh"
path_variables="$path_temporary/waller_variables.txt"
echo $path_temporary

# Echo each command to console.
set -x

# Remove previous version of program.

echo "specify phenotype variables to access from UKBiobank"
cd $path_temporary
echo "1558 1568 1578 1588" | tr -s " " "\n" > $path_variables

# Access phenotype variables from UKBiobank using script from Anthony Batzler.

/usr/bin/bash $path_pull_ukbiobank waller_test $path_variables $path_out
