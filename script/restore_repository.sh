#!/bin/bash

#chmod u+x script.sh

# Read in private file paths.
echo "read private file path variables..."
cd ~/path
path_repository=$(<"./sexy_alcohol.txt")
path_temporary=$(<"./process_temporary.txt")
echo $path_repository
echo $path_temporary

# Echo each command to console.
#set -x

# Remove previous version of program.

echo "remove previous version of the repository..."
#rm -r $path_repository

# Access current version of the program.

echo "access current version of the program..."
cd $path_temporary
#wget https://github.com/tcameronwaller/sexy_alcohol/archive/main.zip
#unzip sexy_alcohol.zip
#mv sexy_alcohol-main $path_repository
#rm main.zip
