#!/bin/bash

# Note:
# Each linear GWAS (30,000 - 200,000 records; 22 chromosomes) requires about
# 5-7 hours to run on the grid.


###########################################################################
# Organize paths.
# Read private, local file paths.
echo "read private file path variables and organize paths..."
cd ~/paths
path_process=$(<"./process_sexy_alcohol.txt")
path_scripts_record="$path_process/sexy_alcohol/scripts/record/2021-11-04"
path_dock="$path_process/dock"

path_reference_population="${path_dock}/stratification/reference_population"
path_table_phenotypes_covariates="${path_reference_population}/table_white_unrelated_female_male.tsv"

path_allele_frequency="${path_dock}/allele_frequency"

################################################################################
# Organize argument variables.

path_report=${2} # full path to parent directory for GWAS summary statistics
analysis=${3} # unique name for association analysis

threads=32 # count of processing threads to use
threshold_allele_frequency=0.0 # threshold filter by minor allele frequency

###########################################################################
# Organize variables.

# Read private, local file paths.
#echo "read private file path variables and organize paths..."
cd ~/paths
path_plink2=$(<"./tools_plink2.txt")
path_ukb_genotype=$(<"./ukbiobank_genotype.txt")

# Iterate on chromosomes.
#chromosomes=("x")
chromosomes=("1" "2" "3" "4" "5" "6" "7" "8" "9" "10" "11" "12" "13" "14" "15" "16" "17" "18" "19" "20" "21" "22" "x")
for chromosome in "${chromosomes[@]}"; do
  #echo "chromosome: ${chromosome}"

  # Specify target directory.
  path_chromosome="$path_allele_frequency/chromosome_${chromosome}"
  # Determine whether the temporary directory structure already exists.
  if [ ! -d $path_chromosome ]; then
      # Directory does not already exist.
      # Create directory.
      mkdir -p $path_chromosome
  fi
  cd $path_chromosome

  # Specify source directory and files.
  if [[ "$chromosome" == "x" ]]; then
    # On 25 October 2021, Gregory Jenkins told me:
    # "I believe you are right on 'ukb22828_cX_b0_v3_s486620.sample' and 'ukb22828_cX_b0_v3.bgen'"
    # "They were missing chrom X and I asked them to download that in March/April of this year I think?  So that's why it looks different."
    path_genotype="$path_ukb_genotype/Chromosome/ukb22828_cX_b0_v3.bgen"
    path_sample="$path_ukb_genotype/Chromosome/ukb22828_cX_b0_v3_s486620.sample"
  else
    path_genotype="$path_ukb_genotype/Chromosome/ukb_imp_chr${chromosome}_v3.bgen"
    path_sample="$path_ukb_genotype/Chromosome/ukb46237_imp_chr${chromosome}_v3_s487320.sample"
  fi

  if true; then
    # Call PLINK2.
    # This call to PLINK2 includes "--freq" and produces a report of allele
    # frequencies.
    # 90,000 Mebibytes (MiB) is 94.372 Gigabytes (GB)
    # Argument "--reference-allele" allows to give an explicit list of alleles to designate as "A1".
    # "Warning: No --bgen REF/ALT mode specified ('ref-first', 'ref-last', or 'ref-unknown'). This will be required as of alpha 3."
    $path_plink2 \
    --memory 90000 \
    --threads $threads \
    --bgen $path_genotype ref-first \
    --sample $path_sample \
    --keep $path_table_phenotypes_covariates \
    --maf $threshold_allele_frequency \
    --freq \
    --out report
  fi
done



##########
