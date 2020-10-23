#!/bin/bash

#chmod u+x script.sh


###########################################################################
###########################################################################
###########################################################################
# This script organizes directories and submits "template_test_sge.sh" to
# the Sun Grid Engine.
###########################################################################
###########################################################################
###########################################################################

echo "----------------------------------------------------------------------"
echo "----------------------------------------------------------------------"
echo "----------------------------------------------------------------------"
echo "----------"
echo "The script is a test template for the Sun Grid Engine."
echo "----------"
echo "----------------------------------------------------------------------"
echo "----------------------------------------------------------------------"
echo "----------------------------------------------------------------------"

# Read private, local file paths.
echo "read private file path variables and organize paths..."
cd ~/paths
path_temporary=$(<"./temporary_sexy_alcohol.txt")
path_waller="$path_temporary/waller"
path_play="$path_waller/play_with_sge"
path_source="$path_play/source"
path_product="$path_play/product"
path_sexy_alcohol="$path_waller/sexy_alcohol"
path_scripts="$path_sexy_alcohol/scripts"

# Echo each command to console.
#set -x
# Suppress echo each command to console.
set +x

# Determine whether the temporary directory structure already exists.
if [ ! -d $path_play ]; then
    # Directory does not already exist.
    # Create directory.
    mkdir -p $path_play
    mkdir -p $path_source
    mkdir -p $path_product
fi

# Organize instances for iteration.
echo "----------------------------------------------------------------------"
echo "Demonstrate a simple array."
echo "----------------------------------------------------------------------"
echo "becky marissa amanda avianna bethany" | tr -s " " "\n" > "$path_source/names.txt"
readarray -t names < "$path_source/names.txt"
echo ${names[@]}
count=${#names[@]}
# Adjust index for base zero.
index_maximum=$((count-1))
echo "count of names: "
echo $count
echo ${indices[@]}

# Iterate on instances.
echo "----------------------------------------------------------------------"
echo "Iterate on that simple array with indices."
echo "----------------------------------------------------------------------"
#for name in "${names[@]}"; do
#for name in "${names[@]:0:100}"; do
for (( index=0; index<=$index_maximum; index+=1 )); do
    name=${names[$index]}
    echo "current name: "
    echo $name
done

# Submit array batch to Sun Grid Engine.
# Array batch indices cannot start at zero.
echo "----------------------------------------------------------------------"
echo "Submit array batch to Sun Grid Engine."
echo "----------------------------------------------------------------------"
qsub -t 1-${count}:1 -o "$path_product/out.txt" -e "$path_product/error.txt" \
$path_scripts/template_test_sge.sh $path_source $path_product $count
