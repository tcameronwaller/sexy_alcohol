#!/bin/bash

###########################################################################
# Organize general paths.
###########################################################################
# Read private, local file paths.
#echo "read private file path variables and organize paths..."
cd ~/paths
path_ldsc=$(<"./tools_ldsc.txt")

path_temporary=$(<"./processing_sexy_alcohol.txt")
path_waller="$path_temporary/waller"
path_dock="$path_temporary/waller/dock"
path_gwas_scripts="$path_waller/sexy_alcohol/scripts/record/2021-01-21"
path_correlation_scripts="$path_waller/sexy_alcohol/scripts/record/2021-01-21"

path_gwas="$path_temporary/waller/dock/gwas"
path_genetic_correlation="$path_temporary/waller/dock/genetic_correlation"

path_access="$path_temporary/waller/dock/genetic_correlation/access"
path_disequilibrium="$path_access/disequilibrium"
path_baseline="$path_access/baseline"
path_weights="$path_access/weights"
path_frequencies="$path_access/frequencies"
path_alleles="$path_access/alleles"

###########################################################################
# Organize directories.

# Genetic correlation directory should already exist and have reference
# information from access script.

# Determine whether the temporary directory structure already exists.
if [ ! -d $path_genetic_correlation ]; then
    # Directory does not already exist.
    # Create directory.
    mkdir -p $path_genetic_correlation
fi

###########################################################################
# Execute procedure.
###########################################################################

# Echo each command to console.
#set -x
# Suppress echo each command to console.
set +x

###########################################################################
# ...

# female_alcoholism-1_case_auditc_testosterone
# male_alcoholism-1_case_auditc_testosterone
# female_alcoholism-2_case_auditc_testosterone
# male_alcoholism-2_case_auditc_testosterone

# female_alcoholism-1_case_auditp_testosterone
# male_alcoholism-1_case_auditp_testosterone
# female_alcoholism-2_case_auditp_testosterone
# male_alcoholism-2_case_auditp_testosterone ... not done

# Parameters.
cohort_comparison="female_alcoholism-1_case_auditc_testosterone"
alcoholism="alcohol_auditc"
hormone="testosterone"
/usr/bin/bash "$path_correlation_scripts/6_regress_genetic_correlation_sex_hormone.sh" \
$cohort_comparison \
$alcoholism \
$hormone \
"linear" \
"linear" \
$path_gwas \
$path_genetic_correlation \
$path_gwas_scripts \
$path_correlation_scripts \
$path_ldsc \
$path_alleles \
$path_disequilibrium

# Parameters.
cohort_comparison="male_alcoholism-1_case_auditc_testosterone"
alcoholism="alcohol_auditc"
hormone="testosterone"
/usr/bin/bash "$path_correlation_scripts/6_regress_genetic_correlation_sex_hormone.sh" \
$cohort_comparison \
$alcoholism \
$hormone \
"linear" \
"linear" \
$path_gwas \
$path_genetic_correlation \
$path_gwas_scripts \
$path_correlation_scripts \
$path_ldsc \
$path_alleles \
$path_disequilibrium

# Parameters.
cohort_comparison="female_alcoholism-2_case_auditc_testosterone"
alcoholism="alcohol_auditc"
hormone="testosterone"
/usr/bin/bash "$path_correlation_scripts/6_regress_genetic_correlation_sex_hormone.sh" \
$cohort_comparison \
$alcoholism \
$hormone \
"linear" \
"linear" \
$path_gwas \
$path_genetic_correlation \
$path_gwas_scripts \
$path_correlation_scripts \
$path_ldsc \
$path_alleles \
$path_disequilibrium

# Parameters.
cohort_comparison="male_alcoholism-2_case_auditc_testosterone"
alcoholism="alcohol_auditc"
hormone="testosterone"
/usr/bin/bash "$path_correlation_scripts/6_regress_genetic_correlation_sex_hormone.sh" \
$cohort_comparison \
$alcoholism \
$hormone \
"linear" \
"linear" \
$path_gwas \
$path_genetic_correlation \
$path_gwas_scripts \
$path_correlation_scripts \
$path_ldsc \
$path_alleles \
$path_disequilibrium

# Parameters.
cohort_comparison="female_alcoholism-1_case_auditp_testosterone"
alcoholism="alcohol_auditp"
hormone="testosterone"
/usr/bin/bash "$path_correlation_scripts/6_regress_genetic_correlation_sex_hormone.sh" \
$cohort_comparison \
$alcoholism \
$hormone \
"linear" \
"linear" \
$path_gwas \
$path_genetic_correlation \
$path_gwas_scripts \
$path_correlation_scripts \
$path_ldsc \
$path_alleles \
$path_disequilibrium

# Parameters.
cohort_comparison="male_alcoholism-1_case_auditp_testosterone"
alcoholism="alcohol_auditp"
hormone="testosterone"
/usr/bin/bash "$path_correlation_scripts/6_regress_genetic_correlation_sex_hormone.sh" \
$cohort_comparison \
$alcoholism \
$hormone \
"linear" \
"linear" \
$path_gwas \
$path_genetic_correlation \
$path_gwas_scripts \
$path_correlation_scripts \
$path_ldsc \
$path_alleles \
$path_disequilibrium

# Parameters.
cohort_comparison="female_alcoholism-2_case_auditp_testosterone"
alcoholism="alcohol_auditp"
hormone="testosterone"
/usr/bin/bash "$path_correlation_scripts/6_regress_genetic_correlation_sex_hormone.sh" \
$cohort_comparison \
$alcoholism \
$hormone \
"linear" \
"linear" \
$path_gwas \
$path_genetic_correlation \
$path_gwas_scripts \
$path_correlation_scripts \
$path_ldsc \
$path_alleles \
$path_disequilibrium

# Parameters.
cohort_comparison="male_alcoholism-2_case_auditp_testosterone"
alcoholism="alcohol_auditp"
hormone="testosterone"
/usr/bin/bash "$path_correlation_scripts/6_regress_genetic_correlation_sex_hormone.sh" \
$cohort_comparison \
$alcoholism \
$hormone \
"linear" \
"linear" \
$path_gwas \
$path_genetic_correlation \
$path_gwas_scripts \
$path_correlation_scripts \
$path_ldsc \
$path_alleles \
$path_disequilibrium
