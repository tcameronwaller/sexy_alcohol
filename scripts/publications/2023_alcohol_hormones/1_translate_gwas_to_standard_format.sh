#!/bin/bash

################################################################################
################################################################################
################################################################################
# Author: T. Cameron Waller
# Date, first execution: 2 March 2023
# Date, last execution: 2 March 2023
################################################################################
################################################################################
################################################################################
# Note

# TODO: write temporary files to a temporary directory other than the source directory

################################################################################
################################################################################
################################################################################



################################################################################
# Organize paths.

# Directories.
cd ~/paths
path_bgzip=$(<"./tools_bgzip.txt")
path_directory_process=$(<"./process_sexy_alcohol.txt")
path_directory_gwas_summaries=$(<"./gwas_summaries_waller_metabolism.txt")
path_directory_parent_source="${path_directory_gwas_summaries}"
path_directory_dock="${path_directory_process}/dock"
path_directory_parameters="${path_directory_dock}/parameters/sexy_alcohol"
path_directory_product="${path_directory_dock}/alcohol_genetics_tcw_2023-03-02/gwas_format_standard"
# Files.
path_file_translation="${path_directory_parameters}/table_gwas_translation_tcw_2023-03-02.tsv"
# Scripts.
path_promiscuity_scripts="${path_directory_process}/promiscuity/scripts"
path_directory_script="${path_promiscuity_scripts}/gwas_format/translate_format_raw_to_standard"
path_script_drive_translations="${path_promiscuity_scripts}/gwas_format/drive_translations_gwas_to_standard_format.sh"

# Initialize directories.
rm -r $path_directory_product
mkdir -p $path_directory_product
cd $path_directory_product

###########################################################################
# Organize parameters.

report="true"

###########################################################################
# Execute procedure.
###########################################################################

/usr/bin/bash $path_script_drive_translations \
$path_file_translation \
$path_directory_parent_source \
$path_directory_script \
$path_directory_product \
$path_bgzip \
$report
