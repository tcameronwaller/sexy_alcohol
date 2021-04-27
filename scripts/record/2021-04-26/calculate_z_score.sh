#!/bin/bash

# Organize variables.
column=$1 # column for which to calculate z-score
path_table_original=$2 # original table
path_table_novel=$3 # novel table

echo "----------"
echo "Note that this program currently is hard-coded for 6 column tables with"
echo "the column to z-score in the 5th column. Not ideal."
echo "----------"
echo "----------"

# Set column delimiter.
# Calculate cumulative statistics.
count=$(cat $path_table_original | awk 'BEGIN { FS=" " } NR > 1 { n++ } END { print n }')
sum=$(cat $path_table_original | awk -v column=$column 'BEGIN { FS=" " } NR > 1 { sum += $column } END { print sum }')
sum_squares=$(cat $path_table_original | awk -v column=$column 'BEGIN { FS=" " } NR > 1 { sum_squares += ($column)^2 } END { print sum_squares }')
mean=$(cat $path_table_original | awk -v column=$column 'BEGIN { FS=" " } NR > 1 { sum += $column; n++ } END { if (n > 0) print (sum / n); }')
variations=$(cat $path_table_original | awk -v column="$column" -v mean="$mean" \
'BEGIN { FS=" " } NR > 1 { value += (($column - mean)^2) } END { print value }')

# The following formulas for standard deviation are equivalent.
#standard_deviation=$(echo "scale=3; sqrt(($sum_squares - (($sum^2)/$count))/($count - 1))" | bc -l)
#standard_deviation="echo 'sqrt(($sum_squares - (($sum^2)/$count))/($count - 1))' | bc -l"
#standard_deviation=$(bc -l <<< "sqrt(($variations)/($count - 1))")

standard_deviation=$(awk -v variations=$variations -v count=$count 'BEGIN {print sqrt(variations / (count - 1)) }')

# Report statistics.
echo "----------"
echo "----------"
echo "----------"
echo "Count: ${count}"
echo "Sum: ${sum}"
echo "Sum of squares: ${sum_squares}"
echo "Mean: ${mean}"
echo "Variations: ${variations}"
echo "Standard deviation: ${standard_deviation}"
echo "----------"
echo "----------"
echo "----------"

#head $path_table_original
#rm $path_table_novel
cat $path_table_original | awk 'BEGIN { FS=OFS=" "} NR == 1' > $path_table_novel
cat $path_table_original | \
awk -v column="$column" -v mean="$mean" -v stdev="$standard_deviation" \
'BEGIN { FS=" "; OFS=" " } NR > 1 {print $1, $2, $3, $4, (($column - mean) / stdev), $6}' >> $path_table_novel
head $path_table_novel
