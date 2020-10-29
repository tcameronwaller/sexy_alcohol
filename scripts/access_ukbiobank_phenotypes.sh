#!/bin/bash

#chmod u+x script.sh

###########################################################################
###########################################################################
###########################################################################
# This script accesses local information about persons and phenotypes in
# the UKBiobank.
# argument 1: path to local file with variable identifiers
# --- format is text file with new line delimiters
# argument 2: path to local file matching IID to EID
# --- format is text file with comma delimiters and two columns with
# --- headers
# arument 3: path to local file with identifiers of UK Biobank participants to
# exclude
# argument 4: path to local directory with UK Biobank phenotype data
# argument 5: path to local directory with UK Biobank ukbconv tool
# argument 6: path to local directory in which to organize product files
###########################################################################
###########################################################################
###########################################################################

echo "----------------------------------------------------------------------"
echo "----------------------------------------------------------------------"
echo "----------------------------------------------------------------------"
echo "The script accesses local information about persons and phenotypes in "
echo "the UK Biobank."
echo "----------"
echo "Hooray! :)"
echo "----------------------------------------------------------------------"
echo "----------------------------------------------------------------------"
echo "----------------------------------------------------------------------"

###########################################################################
# Organize arguments.
path_variables=$1
path_identifier_pairs=$2
path_exclusion=$3
path_phenotype_data=$4
path_tools=$5
path_destination=$6

echo $path_variables
echo $path_identifier_pairs
echo $path_exclusion
echo $path_phenotype_data
echo $path_tools
echo $path_destination

###########################################################################
# Copy auxiliary files.

# Copy UK Biobank phenotype variables to destination directory.
cp $path_variables "$path_destination/uk_biobank_phenotype_variables.txt"

# Copy table of identifier pairs to destination directory.
cp $path_identifier_pairs "$path_destination/table_identifier_pairs.csv"

# Copy table of exclusion identifiers to destination directory.
cp $path_exclusion "$path_destination/table_exclusion_identifiers.csv"

###########################################################################
# Access variables from each phenotype data release of UK Biobank.
# Access names of all current phenotype data releases.
# https://biobank.ctsu.ox.ac.uk/crystal/exinfo.cgi?src=accessing_data_guide
# https://biobank.ctsu.ox.ac.uk/~bbdatan/Accessing_UKB_data_v2.3.pdf
#cd $path_destination
#accessions=($(ls -d $path_phenotype_data/ukb*))
#for i in "${accessions[@]}"; do
#    echo $i
#    dir=`basename $i`
#    # Remove log file to avoid error.
#    rm $path_phenotype_data/$dir/$dir.log
#    # Convert data to text file with comma ("csv") or tab ("txt") delimiters.
#    $path_tools/ukbconv $path_phenotype_data/$dir/$dir.enc_ukb txt \
#    -i $path_variables -o $path_destination/$dir.raw
#    # Remove log file to avoid error.
#    rm $path_phenotype_data/$dir/$dir.log
#done

echo "----------------------------------------------------------------------"
echo "----------------------------------------------------------------------"
echo "----------------------------------------------------------------------"
echo "Now let us see whether that worked."
echo "----------------------------------------------------------------------"
echo "----------------------------------------------------------------------"
echo "----------------------------------------------------------------------"
