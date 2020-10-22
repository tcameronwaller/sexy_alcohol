#!/bin/bash

#chmod u+x script.sh

# Read in private file paths.
echo "read private file path variables and organize paths..."
cd ~/paths
path_temporary=$(<"./temporary_sexy_alcohol.txt")
path_waller="$path_temporary/waller"
path_dock="$path_waller/dock"
path_sexy_alcohol="$path_waller/sexy_alcohol"
path_package="$path_sexy_alcohol/package"

# Echo each command to console.
set -x

python3 $path_package/interface.py main --path_dock $path_dock --assembly
