#!/bin/bash

#chmod u+x script.sh

# Read in private file paths.
echo "read private file path variables and organize paths..."
cd ~/path
path_process=$(<"./process_temporary.txt")
path_temporary="$path_process/waller_sexy_alcohol"
path_project=$(<"./project_sexy_alcohol.txt")
path_repository="$path_project/sexy_alcohol"
path_package="$path_project/sexy_alcohol/package"
path_dock="$path_project/dock"

# Echo each command to console.
set -x

python3 $path_package/interface.py main --temporary $path_temporary --dock $path_dock --albumin
