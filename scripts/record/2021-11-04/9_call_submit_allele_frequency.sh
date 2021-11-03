#!/bin/bash

#chmod u+x script.sh

###########################################################################
###########################################################################
###########################################################################

# version check: 1

###########################################################################
###########################################################################
###########################################################################
# Organize paths.
# Read private, local file paths.
echo "read private file path variables and organize paths..."
cd ~/paths
path_plink2=$(<"./tools_plink2.txt")
path_ukb_genotype=$(<"./ukbiobank_genotype.txt")
path_process=$(<"./process_sexy_alcohol.txt")
path_scripts_record="$path_process/sexy_alcohol/scripts/record/2021-11-04"
path_dock="$path_process/dock"
path_reference_population="${path_dock}/stratification/reference_population"
path_table_cohort="${path_reference_population}/table_white_unrelated_female_male.tsv"
path_allele_frequency="${path_dock}/allele_frequency"

# Initialize directories.
rm -r $path_allele_frequency
mkdir -p $path_allele_frequency

##########
##########
##########
# Assemble a list of analysis instances with common patterns.

# Assemble array of batch instance details.
path_batch_instances="${path_allele_frequency}/batch_instances_allele_frequency.txt"
rm $path_batch_instances

##########
# General models.

# Iterate on chromosomes.
#chromosomes=("x")
chromosomes=("1" "2" "3" "4" "5" "6" "7" "8" "9" "10" "11" "12" "13" "14" "15" "16" "17" "18" "19" "20" "21" "22" "x")
for chromosome in "${chromosomes[@]}"; do
  # Specify target directory.
  path_allele_frequency_chromosome="$path_allele_frequency/chromosome_${chromosome}"
  # Determine whether the temporary directory structure already exists.
  if [ ! -d $path_allele_frequency_chromosome ]; then
      # Directory does not already exist.
      # Create directory.
      mkdir -p $path_allele_frequency_chromosome
  fi
  # Specify source genotypes and samples.
  if [[ "$chromosome" == "x" ]]; then
    # On 25 October 2021, Gregory Jenkins told me:
    # "I believe you are right on 'ukb22828_cX_b0_v3_s486620.sample' and 'ukb22828_cX_b0_v3.bgen'"
    # "They were missing chrom X and I asked them to download that in March/April of this year I think?  So that's why it looks different."
    path_genotype_chromosome="${path_ukb_genotype}/Chromosome/ukb22828_cX_b0_v3.bgen"
    path_sample_chromosome="${path_ukb_genotype}/Chromosome/ukb22828_cX_b0_v3_s486620.sample"
  else
    path_genotype_chromosome="${path_ukb_genotype}/Chromosome/ukb_imp_chr${chromosome}_v3.bgen"
    path_sample_chromosome="${path_ukb_genotype}/Chromosome/ukb46237_imp_chr${chromosome}_v3_s487320.sample"
  fi
  # Assemble details for batch instance.
  instance="${chromosome};${path_genotype_chromosome};${path_sample_chromosome};${path_allele_frequency_chromosome}"
  echo $instance >> $path_batch_instances
done

##########
# Summary of batch instances.

# Array pattern.
#chromosome="${array[0]}"
#path_genotype_chromosome="${array[1]}"
#path_sample_chromosome="${array[2]}"
#path_allele_frequency_chromosome="${array[3]}"

# Read batch instances.
readarray -t batch_instances < $path_batch_instances
batch_instances_count=${#batch_instances[@]}
echo "----------"
echo "count of batch instances: " $batch_instances_count
echo "first batch instance: " ${batch_instances[0]} # notice base-zero indexing
echo "last batch instance: " ${batch_instances[batch_instances_count - 1]}

if true; then
  # Submit array batch to Sun Grid Engine.
  # Array batch indices must start at one (not zero).
  echo "----------------------------------------------------------------------"
  echo "Submit array of batches to Sun Grid Engine."
  echo "----------------------------------------------------------------------"
  qsub -t 1-${batch_instances_count}:1 \
  -o "${path_allele_frequency}/out.txt" -e "${path_allele_frequency}/error.txt" \
  "${path_scripts_record}/10_organize_call_run_allele_frequency.sh" \
  $path_batch_instances \
  $batch_instances_count \
  $path_table_cohort \
  $path_scripts_record \
  $path_process \
  $path_plink2
fi
