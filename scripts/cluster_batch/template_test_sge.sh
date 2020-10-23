#!/bin/bash

###########################################################################
# Specify arguments for qsub command.
# Note that bash does not interpret qsub parameters, which are bash comments.
# Bash will not expand variables in qsub parameters.
# Shell.
#$ -S /bin/bash
# Name of job.
#$ -N waller_test
# Contact.
#$ -M waller.tcameron@mayo.edu
#$ -m abes
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
#$ -l h_vmem=1G
# Concurrent threads; assigns value to variable NSLOTS.
#$ -pe threaded 16
# Range of indices.
# Specify as argument when calling qsub.
# Array batch indices cannot start at zero.
### -t 1-100:1
# Limit on concurrent processes.
#$ -tc 10

###########################################################################
###########################################################################
###########################################################################
# This script organizes an array batch job for the Sun Grid Engine.
# mForge
# 120 worker nodes, each with 32 CPUs and 512 Gigabytes memory
# 3 worker nodes, each with 64 CPUs and 1.5 Terabytes memory
###########################################################################
###########################################################################
###########################################################################


###########################################################################
# Organize variables.
index=$((SGE_TASK_ID-1))
path_source=$1
path_product=$2
count=$3

###########################################################################
# Execute procedure.

# Read source.
readarray -t names < "$path_source/names.txt"
name=${names[$index]}

# Create directory and file.
mkdir -p "$path_product/$name"
echo $name > "$path_product/$name/$name.txt"

# Report.
echo "----------"
echo "task index: " $index
echo "name: " $name
hostname
date
