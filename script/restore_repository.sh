#!/bin/bash

#chmod u+x script.sh

# Read in private file paths.
echo "read private file path variables..."
path_path="~/path"
path_repository=$(<"$path_path/sexy_alcohol.txt")
echo $path_repository

# Echo each command to console.
#set -x

# Remove previous version of program.

#echo "remove previous version of the repository..."

#rm -r $path_repository

# Access current version of the program.

#echo "access current version of the program..."

#wget https://github.com/tcameronwaller/sexy_alcohol/archive/main.zip
#mv main.zip sexy_alcohol.zip
#unzip sexy_alcohol.zip
