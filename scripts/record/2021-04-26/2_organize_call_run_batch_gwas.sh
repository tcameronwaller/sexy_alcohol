#!/bin/bash

###########################################################################
# Specify arguments for qsub command.
# Note that bash does not interpret qsub parameters, which are bash comments.
# Bash will not expand variables in qsub parameters.
# Shell.
#$ -S /bin/bash
# Name of job.
#$ -N waller_gwas
# Contact.
# "b": beginning, "e": end, "a": abortion, "s": suspension, "n": never
#$ -M tcameronwaller@gmail.com
#$ -m ase
# Standard output and error.
# Specify as arguments when calling qsub.
### -o "./out"
### -e "./error"
# Queue.
# "1-hour", "1-day", "4-day", "7-day", "30-day", "lg-mem"
#$ -q 1-day
# Priority 0-15.
### -p -10
# Memory per iteration.
# Segmentation errors commonly indicate a memory error.
#$ -l h_vmem=10G
# Concurrent threads; assigns value to variable NSLOTS.
# Important to specify 32 threads to avoid inconsistency with interactive
# calculations.
#$ -pe threaded 32
# Range of indices.
# Specify as argument when calling qsub.
# Array batch indices cannot start at zero.
### -t 1-100:1
# Limit on concurrent processes.
# Process this count of chromosomes at a time for each job.
# For large cohorts (20,000 - 500,000), limit to 10-20 total simultaneous GWAS
# on NCSA.
# Beyond 10-20 simultaneous GWAS, PLINK2 begins to use more than 2 TB storage.
#$ -tc 4

# http://gridscheduler.sourceforge.net/htmlman/htmlman1/qsub.html

################################################################################
# Organize argument variables.

path_batch_instances=${1} # text list of information for each instance in batch
batch_instances_count=${2} # count of instances in batch
path_cohorts=${3} # full path to parent directory for tables of variables across cohorts
path_gwas=${4} # full path to parent directory for GWAS summary statistics
path_scripts_record=${5}

###########################################################################
# Organize variables.

# Determine batch instance.
batch_index=$((SGE_TASK_ID-1))
readarray -t batch_instances < $path_batch_instances
instance=${batch_instances[$batch_index]}

# Separate fields from instance.
IFS=";" read -r -a array <<< "${instance}"
phenotype="${array[0]}"
cohort="${array[1]}"
covariates="${array[2]}"

echo "phenotype: " ${phenotype}
echo "cohort: " ${cohort}
echo "covariates: " ${covariates}

# Organize variables.
path_table_phenotypes_covariates="${path_cohorts}/table_${cohort}_${phenotype}.tsv"
path_cohort_phenotype="${path_gwas}/${cohort}_${phenotype}"

# General parameters.
threads=32 # 32, needs to match the "pe threaded" argument to scheduler
maf=0.01
chromosomes=22 # 22 # Count of chromosomes on which to run GWAS

# Echo each command to console.
#set -x
# Suppress echo each command to console.
set +x

# Initialize directories.
rm -r $path_cohort_phenotype
mkdir -p $path_cohort_phenotype

###########################################################################
# Execute procedure.

path_report=$path_cohort_phenotype
analysis="${cohort}_${phenotype}"
/usr/bin/bash "${path_scripts_record}/3_run_plink_gwas.sh" \
$path_table_phenotypes_covariates \
$path_report \
$cohort_phenotype \
$phenotype \
$covariates \
$threads \
$maf \
$chromosomes
