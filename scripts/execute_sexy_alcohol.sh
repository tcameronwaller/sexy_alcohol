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

python3 $path_package/interface.py main --path_dock $path_dock --assembly # TCW; 07 June 2022
#python3 $path_package/interface.py main --path_dock $path_dock --importation # TCW; __ June 2022
#python3 $path_package/interface.py main --path_dock $path_dock --organization # TCW; __ June 2022
#python3 $path_package/interface.py main --path_dock $path_dock --stratification # TCW; 09 April 2022, 11 April 2022

#python3 $path_package/interface.py main --path_dock $path_dock --collection # TCW; 20 April 2022
#python3 $path_package/interface.py main --path_dock $path_dock --regression # TCW; 20 April 2022
#python3 $path_package/interface.py main --path_dock $path_dock --description # TCW; 01 June 2022

#python3 $path_package/interface.py main --path_dock $path_dock --scratch

# Collect and organize heritability estimations for metabolites from GWAS
# summary statistics of multiple studies on the human metabolome.
#python3 $path_package/interface.py main --path_dock $path_dock --genetic_correlation

# Collect and aggregate genetic scores for metabolites across the UK Biobank.
#python3 $path_package/interface.py main --path_dock $path_dock --aggregation



################################################################################
# Deactivate Python Virtual Environment.
deactivate
echo "----------"
echo "confirm deactivation of Python Virtual Environment..."
which python3
