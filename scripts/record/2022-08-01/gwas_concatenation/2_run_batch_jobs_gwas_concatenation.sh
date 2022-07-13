#!/bin/bash

###########################################################################
# Specify arguments for qsub command.
# Note that bash does not interpret qsub parameters, which are bash comments.
# Bash will not expand variables in qsub parameters.
# Shell.
#$ -S /bin/bash
# Name of job.
#$ -N tcw_gwas_concatenate
# Contact.
# "b": beginning, "e": end, "a": abortion, "s": suspension, "n": never
#$ -M waller.tcameron@mayo.edu
#$ -m as
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
#$ -l h_vmem=4G
# Concurrent threads; assigns value to variable NSLOTS.
#$ -pe threaded 1
# Range of indices.
# Specify as argument when calling qsub.
# Array batch indices cannot start at zero.
### -t 1-100:1
# Limit on concurrent processes.
#$ -tc 25

# http://gridscheduler.sourceforge.net/htmlman/htmlman1/qsub.html

################################################################################
# Note.

# Collection and concatenation of GWAS summary statistics runs with 4 thread
# slots ("-pe threaded 4") and 1 Gigabyte of memory ("-l h_vmem=1G"), even for
# GWAS on > 300,000 persons.

################################################################################
# Organize argument variables.

path_file_batch_instances=${1} # full path to file for text list of information about each job instance in batch
batch_instances_count=${2} # count of job instances in batch
path_script_concatenate=${3} # full path to script to concatenate information from GWAS across chromosomes

###########################################################################
# Organize variables.

# Determine batch instance.
batch_index=$((SGE_TASK_ID-1))
readarray -t batch_instances < $path_file_batch_instances
instance=${batch_instances[$batch_index]}

# Separate fields from instance.
IFS=";" read -r -a array <<< "${instance}"
pattern_file_gwas_source="${array[0]}"
pattern_file_frequency_source="${array[1]}"
pattern_file_log_source="${array[2]}"
path_directory_chromosomes_source="${array[3]}"
path_file_gwas_product="${array[4]}"
path_file_frequency_product="${array[5]}"
name_directory_log_product="${array[6]}"
prefix_file_log_product="${array[7]}"
suffix_file_log_product="${array[8]}"
chromosome_xy="${array[9]}"
report="${array[10]}"

###########################################################################
# Execute procedure.

/usr/bin/bash "${path_script_concatenate}" \
$pattern_file_gwas_source \
$pattern_file_frequency_source \
$pattern_file_log_source \
$path_directory_chromosomes_source \
$path_file_gwas_product \
$path_file_frequency_product \
$name_directory_log_product \
$prefix_file_log_product \
$suffix_file_log_product \
$chromosome_xy \
$report

#
