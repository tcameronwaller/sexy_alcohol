#!/bin/bash

#chmod u+x script.sh
#chmod -R 777

# Read private, local file paths.
echo "read private file path variables and organize paths..."
cd ~/paths
path_python_library=$(<"./tools_python_library.txt")
path_process=$(<"./process_sexy_alcohol.txt")
path_dock="$path_process/dock"
path_sexy_alcohol="$path_process/sexy_alcohol"
path_package="$path_sexy_alcohol/sexy_alcohol"

# Organize paths to custom package installations.
PYTHONPATH=$path_python_library:$PYTHONPATH
export PYTHONPATH

# Echo each command to console.
set -x

# Determine whether the temporary directory structure already exists.
if [ ! -d $path_dock ]
then
    # Directory does not already exist.
    # Create directory.
    mkdir -p $path_dock
fi

# Execute procedure(s).

#python3 $path_package/interface.py main --path_dock $path_dock --scratch

#python3 $path_package/interface.py main --path_dock $path_dock --assembly
python3 $path_package/interface.py main --path_dock $path_dock --organization
#python3 $path_package/interface.py main --path_dock $path_dock --description
#python3 $path_package/interface.py main --path_dock $path_dock --stratification
#python3 $path_package/interface.py main --path_dock $path_dock --genetic_correlation
