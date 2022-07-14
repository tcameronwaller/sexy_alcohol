#!/bin/bash

###########################################################################
# Specify arguments for qsub command.
# Note that bash does not interpret qsub parameters, which are bash comments.
# Bash will not expand variables in qsub parameters.
# Shell.
#$ -S /bin/bash
# Name of job.
#$ -N tcw_ldsc
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
#$ -q 1-hour
# Priority 0-15.
### -p -10
# Memory per iteration.
# Segmentation errors commonly indicate a memory error.
#$ -l h_vmem=4G
# Concurrent threads; assigns value to variable NSLOTS.
# Important to specify 32 threads to avoid inconsistency with interactive
# calculations.
#$ -pe threaded 1
# Range of indices.
# Specify as argument when calling qsub.
# Array batch indices cannot start at zero.
### -t 1-100:1
# Limit on concurrent processes.
#$ -tc 200

# http://gridscheduler.sourceforge.net/htmlman/htmlman1/qsub.html

################################################################################
# Note.

# LDSC Genetic Correlation on previously munged GWAS summary statistics throws a
# memory error ("Segmentation fault") with 1 thread slot ("-pe threaded 1") and
# 2 Gigabyte of memory ("-l h_vmem=2G") (TCW; 14 July 2022).

# LDSC Genetic Correlation on previously munged GWAS summary statistics runs
# with 1 thread slot ("-pe threaded 1") and 4 Gigabytes of memory
# ("-l h_vmem=4G") (TCW; 14 July 2022).

################################################################################
# Organize argument variables.

path_batch_instances=${1} # text list of information for each instance in batch
batch_instances_count=${2} # count of instances in batch
path_genetic_correlation_container=${3} # full path to parent directory for genetic correlation comparisons
path_genetic_reference=${4} # full path to directory for all processes relevant to current project
path_scripts_record=${5} # full path to directory for scripts in current procedure
path_process=${6} # full path to directory for all processes relevant to current project
report=${7} # full path to directory for all processes relevant to current project

###########################################################################
# Organize batch instance variables.

# Determine batch instance.
batch_index=$((SGE_TASK_ID-1))
readarray -t batch_instances < $path_batch_instances
comparison_instance=${batch_instances[$batch_index]}

################################################################################
# Call driver script.

/usr/bin/bash "${path_scripts_record}/8_run_drive_gwas_ldsc_genetic_correlation.sh" \
$comparison_instance \
$path_genetic_correlation_container \
$path_genetic_reference \
$path_process \
$report \
