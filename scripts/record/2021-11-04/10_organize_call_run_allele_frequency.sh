#!/bin/bash

###########################################################################
# Specify arguments for qsub command.
# Note that bash does not interpret qsub parameters, which are bash comments.
# Bash will not expand variables in qsub parameters.
# Shell.
#$ -S /bin/bash
# Name of job.
#$ -N waller_allele
# Contact.
# "b": beginning, "e": end, "a": abortion, "s": suspension, "n": never
#$ -M tcameronwaller@gmail.com
#$ -m as
# Standard output and error.
# Specify as arguments when calling qsub.
### -o "./out"
### -e "./error"
# Queue.
# "1-hour", "1-day", "4-day", "7-day", "30-day", "lg-mem"
#$ -q 1-hour
# Priority 0-15.
### -p -10
# Memory per iteration.
# Segmentation errors commonly indicate a memory error.
#$ -l h_vmem=5G
# Concurrent threads; assigns value to variable NSLOTS.
# Important to specify 32 threads to avoid inconsistency with interactive
# calculations.
#$ -pe threaded 32
# Range of indices.
# Specify as argument when calling qsub.
# Array batch indices cannot start at zero.
### -t 1-100:1
##########
# Limit on concurrent processes.
# Allow simultaneous processes for this count of GWAS studies.
# For large cohorts (20,000 - 500,000), limit to 10-20 total simultaneous GWAS
# on NCSA.
# At this scale, about 15 simultaneous GWAS in PLINK2 require approximately 1.5
# Terabytes of storage (not memory).
# PLINK2 seems to require the most storage during the initial reads of variants
# such that simultaneous starts to multiple GWAS cause the requirement to peak
# temporarily.
# Also remember that as large batches complete, the final GWAS summary
# statistics accumulate and consume some of the available storage space.
#$ -tc 24

# http://gridscheduler.sourceforge.net/htmlman/htmlman1/qsub.html

################################################################################
# Organize argument variables.

path_batch_instances=${1} # text list of information for each instance in batch
batch_instances_count=${2} # count of instances in batch
path_table_cohort=${3} # full path to table with identifiers of persons and genotypes in cohort for analysis
path_scripts_record=${4} # full path to parent directory for date-specific record scripts
path_process=${5} # full path to directory for all processes relevant to current project
path_plink2=${6} # full path to executable installation of PLINK2

###########################################################################
# Organize variables.

# Determine batch instance.
batch_index=$((SGE_TASK_ID-1))
readarray -t batch_instances < $path_batch_instances
instance=${batch_instances[$batch_index]}

# Separate fields from instance.
IFS=";" read -r -a array <<< "${instance}"
chromosome="${array[0]}"
path_genotype_chromosome="${array[1]}"
path_sample_chromosome="${array[2]}"
path_allele_frequency_chromosome="${array[3]}"

threshold_allele_frequency=0.0 # threshold filter by minor allele frequency
threads=32 # count of processing threads to use

###########################################################################
# Execute procedure.

/usr/bin/bash "${path_scripts_record}/11_run_chromosomes_plink_allele_frequency.sh" \
$path_table_cohort \
$path_genotype_chromosome \
$path_sample_chromosome \
$path_allele_frequency_chromosome \
$threshold_allele_frequency \
$threads \
$path_plink2



################################################################################
