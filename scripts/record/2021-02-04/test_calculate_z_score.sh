#!/bin/bash

# Organize variables.
column=$1 # column for which to calculate z-score
path_table_original=$2 # original table

count=$(cat $path_table_original | awk -v N=$column 'NR > 1 { n++ } END { print n }')
sum=$(cat $path_table_original | awk -v N=$column 'NR > 1 { sum += $N } END { print sum }')
sum_squares=$(cat $path_table_original | awk -v N=$column 'NR > 1 { sum_sq += ($N)^2 } END { print sum_sq }')
mean=$(cat $path_table_original | awk -v N=$column 'NR > 1 { sum += $N; n++ } END { if (n > 0) print sum / n; }')

term=$($sum_squares - (($sum^2)/$count))/($count - 1))
square_root=$(awk -v term=$term 'BEGIN {print (sqrt($term))}')

#st_dev=$(awk -v count=$count sum=$sum sum_squares=$sum_squares 'BEGIN { print (sqrt($sum_squares - (($sum^2)/$count))/($count - 1))}')

echo $count
echo $sum
echo $sum_squares
echo $mean
echo $term
echo $square_root
#echo $st_dev
