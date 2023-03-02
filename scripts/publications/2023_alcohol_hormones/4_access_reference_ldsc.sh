#!/bin/bash

###########################################################################
# Organize paths.

# Read private, local file paths.
cd ~/paths
path_directory_process=$(<"./process_sexy_alcohol.txt")

path_directory_dock="${path_directory_process}/dock"
path_directory_reference="${path_directory_dock}/alcohol_genetics_tcw_2023-03-02/reference_ldsc"

path_promiscuity_scripts="${path_directory_process}/promiscuity/scripts"
path_script_access="${path_promiscuity_scripts}/ldsc/access_ldsc_genetic_references.sh"

###########################################################################
# Execute procedure.
###########################################################################

/usr/bin/bash "${path_script_access}" \
$path_directory_reference

################################################################################
# Report.
if [[ "$report" == "true" ]]; then
  echo "----------"
  echo "Script complete:"
  echo "3_access_reference_ldsc.sh"
  echo "----------"
fi
