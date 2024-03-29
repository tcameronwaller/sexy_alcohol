#!/bin/bash

###########################################################################
# Organize paths.
# Read private, local file paths.
#echo "read private file path variables and organize paths..."
cd ~/paths
path_process=$(<"./process_sexy_alcohol.txt")

path_dock="${path_process}/dock"
path_genetic_reference="${path_dock}/access/genetic_reference_ldsc"

path_promiscuity_scripts="${path_process}/promiscuity/scripts"
path_script_access_ldsc_genetic_references="${path_promiscuity_scripts}/utility/ldsc/access_ldsc_genetic_references.sh"

###########################################################################
# Execute procedure.
###########################################################################

/usr/bin/bash "${path_script_access_ldsc_genetic_references}" \
$path_genetic_reference
