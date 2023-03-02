#!/bin/bash

###########################################################################
###########################################################################
###########################################################################
# Author: T. Cameron Waller
# Date, first execution: 2 March 2023
# Date, last execution: 2 March 2023

###########################################################################
###########################################################################
###########################################################################

# TODO: TCW; 2 March 2023
# TODO: Currently will need information from "sexy alcohol" and from "psychiatric metabolism"
# TODO: maybe better to consolidate these in the future?


################################################################################
# Organize paths.

# Directories.
cd ~/paths
path_directory_process_sa=$(<"./process_sexy_alcohol.txt")
path_directory_process_pm=$(<"./process_psychiatric_metabolism.txt")

path_directory_dock_sa="${path_directory_process_sa}/dock"
path_directory_dock_pm="${path_directory_process_pm}/dock"

path_directory_source_sa="${path_directory_dock_sa}/alcohol_genetics_tcw_2023-03-02/gwas_munge_ldsc"
path_directory_source_pm="${path_directory_dock_pm}/hormone_genetics_tcw_2023-02-24/gwas_munge_ldsc"

path_directory_product="${path_directory_dock}/alcohol_genetics_tcw_2023-03-02/gwas_correlation_ldsc"
path_directory_reference="${path_directory_dock}/alcohol_genetics_tcw_2023-03-02/reference_ldsc"
path_directory_disequilibrium="${path_directory_reference}/disequilibrium/eur_w_ld_chr"

# Scripts.
path_directory_promiscuity_scripts="${path_directory_process}/promiscuity/scripts"
path_directory_ldsc="${path_directory_promiscuity_scripts}/ldsc"
path_file_script="${path_directory_ldsc}/estimate_gwas_genetic_correlation_ldsc.sh"

# Initialize directories.
rm -r $path_directory_product
mkdir -p $path_directory_product

################################################################################
# Organize parameters.

##########
# Common parameters.
threads=8
report="true"

##########
# Organize multi-dimensional array of information about studies.
# [full path to base name of product file] ; \
# [full path to primary source file of LDSC munge GWAS summary statistics] ; \
# [full path to secondary source file of LDSC munge GWAS summary statistics]

comparisons=()

comparisons+=(
  "${path_directory_product}/alcohol_consumption_quantity_against_blankblankblank;\
  ${path_directory_source_sa}/30643251_liu_2019_alcohol_no_ukb.sumstats.gz;\
  ${path_directory_source_pm}/blankblankblank.sumstats.gz"
)

comparisons+=(
  "${path_directory_product}/alcohol_dependence_against_blankblankblank;\
  ${path_directory_source_sa}/30482948_walters_2018_eur_unrel_genotype.sumstats.gz;\
  ${path_directory_source_pm}/blankblankblank.sumstats.gz"
)




###########################################################################
# Execute procedure.

# Organize information for batch instances.
for comparison in "${comparisons[@]}"; do
  # Separate fields from instance.
  # [regression type] ; [full path to source file of GWAS summary statistics] ; [full path to product file of GWAS summary statistics]
  IFS=";" read -r -a array <<< "${comparison}"
  path_file_base_product="${array[0]}"
  path_file_source_primary="${array[1]}"
  path_file_source_secondary="${array[2]}"
  # Estimate Genetic Correlation by LDSC.
  /usr/bin/bash "${path_file_script}" \
  $path_file_source_primary \
  $path_file_source_secondary \
  $path_file_base_product \
  $path_directory_disequilibrium \
  $threads \
  $report
  # Report.
  if [[ "$report" == "true" ]]; then
    echo "----------"
    echo "Script path:"
    echo $path_script
    echo "Primary source file path:"
    echo $path_file_source_primary
    echo "Secondary source file path:"
    echo $path_file_source_secondary
    echo "Product file path:"
    echo $path_file_base_product
    echo "----------"
  fi
done

################################################################################
# Report.
if [[ "$report" == "true" ]]; then
  echo "----------"
  echo "Script complete:"
  echo "7_estimate_gwas_genetic_correlation_ldsc.sh"
  echo "----------"
fi



#
