
################################################################################
# General parameters.

cohorts_models="cohorts_models_linear_measurement"          # 72 GWAS started at 19:21 on 7 September 2021
#cohorts_models="cohorts_models_linear_measurement_unadjust" # 72 GWAS started at 19:22 on 7 September 2021
#cohorts_models="cohorts_models_linear_imputation"           # 72 GWAS started at 19:37 on 7 September 2021
#cohorts_models="cohorts_models_linear_imputation_unadjust"  # 72 GWAS started at 19:39 on 7 September 2021

#cohorts_models="cohorts_models_linear_order"
#cohorts_models="cohorts_models_linear_order_unadjust"
#cohorts_models="cohorts_models_logistic_detection"
#cohorts_models="cohorts_models_logistic_detection_unadjust"

pattern_gwas_report_file="report.*.glm.linear" # do not expand with full path yet
response="coefficient" # "coefficient" or "z_score" if "response_standard_scale" is "yes"
response_standard_scale="no" # "no" or "yes"

study="male_age_high_testosterone_bioavailable_log"

################################################################################
# Organize paths.
# Read private, local file paths.
cd ~/paths
path_process=$(<"./process_sexy_alcohol.txt")
path_dock="$path_process/dock"

path_gwas_source_container="${path_dock}/gwas/${cohorts_models}" # selection
path_gwas_target_container="${path_dock}/gwas_process/${cohorts_models}" # selection ... notice appended "_z"
path_heritability_container="${path_dock}/heritability/${cohorts_models}" # selection ... notice appended "_z"

path_scripts_record="$path_process/sexy_alcohol/scripts/record/2021-08-26"
path_batch_instances="${path_gwas_target_container}/post_process_batch_instances.txt"

###########################################################################
# Execute procedure.

# Concatenate GWAS across chromosomes.
/usr/bin/bash "${path_scripts_record}/10_drive_gwas_concatenation_format_munge_heritability.sh" \
$study \
$pattern_gwas_report_file \
$response \
$response_standard_scale \
$path_gwas_source_container \
$path_gwas_target_container \
$path_heritability_container
