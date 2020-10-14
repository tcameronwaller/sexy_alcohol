#!/bin/bash

#chmod u+x script.sh

# Read in private file paths.
echo "read private file path variables..."
cd ~/path
path_temporary=$(<"./process_temporary.txt")
path_project=$(<"./project_sexy_alcohol.txt")
path_repository=$(<"./sexy_alcohol.txt")
echo $path_temporary
echo $path_project
echo $path_repository

# Echo each command to console.
set -x

# Remove previous version of program.

echo "remove previous version of the repository..."
cd $path_project
rm -r $path_repository

# Access current version of the program.

echo "access current version of the program..."
cd $path_temporary
wget https://github.com/tcameronwaller/sexy_alcohol/archive/main.zip
unzip main.zip
rm main.zip
mv sexy_alcohol-main $path_repository
