#!/bin/bash

###########################################################################
# Organize paths.
# Read private, local file paths.
#echo "read private file path variables and organize paths..."
cd ~/paths
path_temporary=$(<"./processing_sexy_alcohol.txt")
path_waller="$path_temporary/waller"
path_dock="$path_temporary/waller/dock"
path_genetic_reference="$path_dock/access/genetic_reference"
path_promiscuity_scripts="$path_waller/promiscuity/scripts"

###########################################################################
# Execute procedure.
###########################################################################

/usr/bin/bash "$path_promiscuity_scripts/access_ldsc_genetic_references.sh" \
$path_genetic_reference
