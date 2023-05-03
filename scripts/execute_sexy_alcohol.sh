#!/bin/bash

#chmod u+x script.sh
#chmod -R 777


################################################################################
# Activate Python Virtual Environment.
# Read private, local file paths.
#echo "read private file path variables and organize paths..."
cd ~/paths
path_tools=$(<"./waller_tools.txt")
path_environment_main="${path_tools}/python/environments/main"
source "${path_environment_main}/bin/activate"
echo "----------"
echo "confirm activation of Python Virtual Environment..."
which python3
sleep 5s

################################################################################
# Read private, local file paths.
echo "read private file path variables and organize paths..."
cd ~/paths
path_process=$(<"./process_sexy_alcohol.txt")
path_dock="$path_process/dock"
path_package="${path_process}/sexy_alcohol/sexy_alcohol"

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

# Routine: main
#python3 $path_package/interface.py main --path_dock $path_dock --scratch

# Routine: uk_biobank
#python3 $path_package/interface.py uk_biobank --path_dock $path_dock --assembly # TCW; 08 August 2022
#python3 $path_package/interface.py uk_biobank --path_dock $path_dock --importation # TCW; 08 August 2022
#python3 $path_package/interface.py uk_biobank --path_dock $path_dock --organization # TCW; 23 February 2023
#python3 $path_package/interface.py uk_biobank --path_dock $path_dock --stratification # TCW; ___ 2022 <-- no longer executable
#python3 $path_package/interface.py uk_biobank --path_dock $path_dock --genotype # TCW; 13 October 2022
python3 $path_package/interface.py uk_biobank --path_dock $path_dock --description # TCW; 3 May 2023
#python3 $path_package/interface.py uk_biobank --path_dock $path_dock --plot # TCW; 24 October 2022
#python3 $path_package/interface.py uk_biobank --path_dock $path_dock --regression # TCW; 24 October 2022
#python3 $path_package/interface.py uk_biobank --path_dock $path_dock --collection # TCW; 24 October 2022

# Routine: stragglers
#python3 $path_package/interface.py stragglers --path_dock $path_dock --mbpdb_assembly # TCW; 15 June 2022
#python3 $path_package/interface.py stragglers --path_dock $path_dock --mbpdb_organization # TCW; 20 June 2022
#python3 $path_package/interface.py stragglers --path_dock $path_dock --mbpdb_extraction # TCW; 2 March 2023
#python3 $path_package/interface.py stragglers --path_dock $path_dock --mbpdb_regression # TCW; 20 June 2022
#python3 $path_package/interface.py stragglers --path_dock $path_dock --mcita_assembly # TCW; 24 August 2022
#python3 $path_package/interface.py stragglers --path_dock $path_dock --mcita_organization # TCW; 24 August 2022

################################################################################
# Deactivate Python Virtual Environment.
deactivate
echo "----------"
echo "confirm deactivation of Python Virtual Environment..."
which python3
