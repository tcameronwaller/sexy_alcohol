#!/bin/bash

#chmod u+x script.sh

# Read private, local file paths.
echo "read private file path variables..."
cd ~/paths
path_temporary=$(<"./temporary_sexy_alcohol.txt")
path_waller="$path_temporary/waller"
path_sexy_alcohol="$path_waller/sexy_alcohol"
path_uk_biobank="$path_waller/uk_biobank"
path_promiscuity="$path_waller/promiscuity"

path_parameters="$path_temporary/waller/sexy_alcohol/parameters"
path_parameters_table_variables="$path_parameters/table_ukbiobank_phenotype_variables.tsv"
path_access="$path_temporary/waller/dock/access"
path_access_table_variables="$path_access/table_ukbiobank_phenotype_variables.tsv"

# Echo each command to console.
set -x

# Remove previous version of program.

echo "remove previous versions of the repositories..."
rm -r $path_sexy_alcohol
rm -r $path_uk_biobank
rm -r $path_promiscuity

##########
# Access and organize current version of the main repository.

echo "access current version of the sexy_alcohol repository..."
cd $path_waller
wget https://github.com/tcameronwaller/sexy_alcohol/archive/main.zip
unzip main.zip
rm main.zip
mv sexy_alcohol-main $path_sexy_alcohol
mv "$path_sexy_alcohol/package" "$path_sexy_alcohol/sexy_alcohol"

##########
# Organize and restore parameters.

# TODO: copy the "parameters" directory from the repository to the "dock"...
# TODO: modify the access procedure to copy this parameters information to dock, also...
# Transfer new version of parameters.
#rm $path_access_table_variables
#cp $path_parameters_table_variables $path_access_table_variables

##########
# Organize and restore supplemental sub-repositories.

# Repository: uk_biobank
# Scripts remain within original repository's structure.
# Python code transfers to a sub-package within main package.
echo "access current version of the uk_biobank repository..."
cd $path_waller
wget https://github.com/tcameronwaller/uk_biobank/archive/main.zip
unzip main.zip
rm main.zip
mv uk_biobank-main $path_uk_biobank
mv "$path_uk_biobank/package" "$path_uk_biobank/uk_biobank"
cp -r "$path_uk_biobank/uk_biobank" "$path_sexy_alcohol/sexy_alcohol/uk_biobank"

# Repository: promiscuity
# Scripts remain within original repository's structure.
# Python code transfers to sub-package.
echo "access current version of the promiscuity repository..."
cd $path_waller
wget https://github.com/tcameronwaller/promiscuity/archive/main.zip
unzip main.zip
rm main.zip
mv promiscuity-main $path_promiscuity
mv "$path_promiscuity/package" "$path_promiscuity/promiscuity"
cp -r "$path_promiscuity/promiscuity" "$path_sexy_alcohol/sexy_alcohol/promiscuity"
