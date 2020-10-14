#!/bin/bash

#chmod u+x script.sh

# Read in private file paths.
echo "read private file path variables..."
cd ~/path
path_temporary=$(<"./process_temporary.txt")
path_project=$(<"./project_sexy_alcohol.txt")
path_repository=$(<"./sexy_alcohol.txt")
echo $path_temporary
echo $path_project
echo $path_repository

# Echo each command to console.
set -x

# Remove previous version of program.

echo "specify phenotype variables to access from UKBiobank"
cd $path_temporary
echo "1558 1568 1578 1588" | tr -s " " "\n" > waller_variables.txt
