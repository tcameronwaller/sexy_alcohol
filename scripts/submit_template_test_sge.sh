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
path_sexy_alcohol="$path_waller/sexy_alcohol"
path_scripts="$path_sexy_alcohol/scripts"

# Echo each command to console.
#set -x
# Suppress echo each command to console.
set +x

# Determine whether the temporary directory structure already exists.
if [ ! -d $path_play ]
then
    # Directory does not already exist.
    # Create directory.
    mkdir -p $path_play
fi

# Organize instances for iteration.
echo "becky marissa amanda avianna bethany" | tr -s " " "\n" > "$path_play/names.txt"
readarray -t names < "$path_play/names.txt"
echo ${names[@]}
count=${#names[@]}
indices_maximum=$((count-1))
indices={0..${count}..1}
echo "count of names: "
echo $count
echo ${indices[@]}

# Iterate on instances.
#for name in "${names[@]:0:100}"
for (( index=0; index<=$indices_maximum; index+=1 )); do
    echo "current name: "
    echo $names[$index]
done

# Execute procedure(s).

#qsub $path_scripts/template_test_sge.sh $path_play
