#!/bin/bash

#chmod u+x script.sh

# Read in private file paths.
echo "read private file path variables..."
cd ~/path
path_temporary=$(<"./temporary_sexy_alcohol.txt")
path_waller="$path_temporary/waller"
path_repository="$path_waller/sexy_alcohol"
path_package="$path_repository/package"
path_subpackage="$path_package/promiscuity"

# Echo each command to console.
set -x

# Remove previous version of program.

echo "remove previous version of the repository..."
rm -r $path_repository

# Access current version of the program.

echo "access current version of the sexy_alcohol repository..."
cd $path_waller
wget https://github.com/tcameronwaller/sexy_alcohol/archive/main.zip
unzip main.zip
rm main.zip
mv sexy_alcohol-main $path_repository

echo "access current version of the promiscuity repository..."
echo "organize promiscuity as a subpackage within sexy_alcohol..."
cd $path_package
wget https://github.com/tcameronwaller/promiscuity/archive/main.zip
unzip main.zip
rm main.zip
mv promiscuity-main $path_subpackage
