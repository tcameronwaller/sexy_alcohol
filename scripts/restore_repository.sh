#!/bin/bash

#chmod u+x script.sh

# Read in private file paths.
echo "read private file path variables..."
cd ~/paths
path_temporary=$(<"./temporary_sexy_alcohol.txt")
path_waller="$path_temporary/waller"
path_sexy_alcohol="$path_waller/sexy_alcohol"
path_promiscuity="$path_waller/promiscuity"

# Echo each command to console.
set -x

# Remove previous version of program.

echo "remove previous versions of the repositories..."
rm -r $path_sexy_alcohol
rm -r $path_promiscuity

# Access current version of the program.

echo "access current version of the sexy_alcohol repository..."
cd $path_waller
wget https://github.com/tcameronwaller/sexy_alcohol/archive/main.zip
unzip main.zip
rm main.zip
mv sexy_alcohol-main $path_sexy_alcohol

echo "access current version of the promiscuity repository..."
cd $path_waller
wget https://github.com/tcameronwaller/promiscuity/archive/main.zip
unzip main.zip
rm main.zip
mv promiscuity-main $path_promiscuity

echo "organize promiscuity as a subpackage within sexy_alcohol..."
cp -r "$path_promiscuity/package" "$path_sexy_alcohol/package/package"
mv "$path_sexy_alcohol/package/package" "$path_sexy_alcohol/package/promiscuity"
