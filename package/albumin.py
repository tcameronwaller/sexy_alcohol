
"""
...

"""

###############################################################################
# Notes

###############################################################################
# Installation and importation

# Import modules from specific path without having to install a general package
# I would have to figure out how to pass a path variable...
# https://stackoverflow.com/questions/67631/how-to-import-a-module-given-the-full-path


# Standard

import sys
#print(sys.path)
import os
import math
import statistics
import pickle
import copy
import random
import itertools

# Relevant

import numpy
import pandas
import scipy.stats

# Custom

#import plot
import utility


###############################################################################
# Functionality

# Utility...


def read_file_text(
    path_file=None
):
    """
    Reads information from file as a text string.

    arguments:
        path_file (str): path to directory and file

    returns:
        (str): information from file

    raises:

    """

    # Read information from file
    #with open(path_file_source, "r") as file_source:
    #    content = file_source.read()
    with open(path_file, "r") as file_source:
        content = file_source.read()
    # Return information
    return content


def read_file_text_list(
    delimiter=None,
    path_file=None
):
    """
    Reads and organizes source information from file.

    Delimiters include "\n", "\t", ",", " ".

    arguments:
        delimiter (str): delimiter between elements in list
        path_file (str): path to directory and file

    returns:
        (list<str>): information from file

    raises:

    """

    # Read information from file
    content = read_file_text(path_file=path_file)
    # Split content by line delimiters.
    values_split = content.split(delimiter)
    values_strip = list(map(lambda value: value.strip(), values_split))
    # Return information
    return values_strip


# This stuff

# TODO: currently uses hard-coded column names... not good
# TODO: read in column names from last row
# TODO: also need to handle multi-instance columns, either taking the mean or only the most recent one...
def read_source(dock=None):
    """
    Reads and organizes source information from file

    arguments:
        dock (str): path to root or dock directory for source and product
            directories and files

    raises:

    returns:
        (object): source information

    """

    # Specify directories and files.
    path_variables = os.path.join(
        dock, "albumin", "variables.txt"
    )
    path_data_raw = os.path.join(
        dock, "albumin", "data_raw.csv"
    )
    # Read information from file.
    variables = read_file_text_list(
        delimiter="\n",
        path_file=path_variables,
    )
    variables_sort = sorted(variables, reverse=False)
    variables_sort.insert(0, "person")
    variables_sort.append("unknown")
    variables_sort.append("person_extra")
    data_raw = pandas.read_csv(
        path_data_raw,
        sep=",", # ",", "\t"
        header=None,
        names=["person", "sex", "age", "albumin", "albumin_extra", "person_extra"],
        skipfooter=1,
    )

    # Compile and return information.
    return {
        "variables": variables_sort,
        "data_raw": data_raw,
    }





# Stratification

def determine_stratification_bin_thresholds(
    bin=None,
    values_sort=None,
    indices=None,
    thresholds=None,
    report=None,
):
    """
    Determine values of thresholds for three stratification bins.
    Lower and upper thresholds for a bin cannot be identical.

    arguments:
        bin (list<float>): proportions for one stratification bin
        values_sort (list<float>): values of continuous variable in ascending
            sort order
        indices (list<list<int>>): indices for each low and high threshold
        thresholds (list<list<float>>): thresholds for bins
        report (bool): whether to print reports

    raises:

    returns:
        (list<list<int>>, list<list<float>>): indices, thresholds

    """

    # Count total values.
    count_total = len(values_sort)

    # Low threshold.
    count_low = round(bin[0] * count_total)
    if (count_low == 0):
        index_low = 0
    else:
        index_low = (count_low - 1)
    value_low = values_sort[index_low]
    # Ensure that low threshold is at least as great as the previous bin's high
    # threshold.
    if len(thresholds) > 0:
        if (value_low < thresholds[-1][1]):
            value_low = thresholds[-1][1]

    # High threshold.
    count_high = round(bin[1] * count_total)
    index_high = (count_high - 1)
    value_high = values_sort[index_high]
    # Ensure that high threshold is greater than low threshold.
    if value_low == value_high:
        # Iterate on values until finding the next greater value.
        while values_sort[index_high] == value_low:
            index_high += 1
        value_high = values_sort[index_high]

    # Collect indices.
    indices_bin = list()
    indices_bin.append(index_low)
    indices_bin.append(index_high)
    indices.append(indices_bin)
    # Collect thresholds.
    thresholds_bin = list()
    thresholds_bin.append(value_low)
    thresholds_bin.append(value_high)
    thresholds.append(thresholds_bin)
    # Report.
    if report:
        utility.print_terminal_partition(level=4)
        print("count_low: " + str(count_low))
        print("index_low: " + str(index_low))
        print("value_low: " + str(value_low))
        print("count_high: " + str(count_high))
        print("index_high: " + str(index_high))
        print("value_high: " + str(value_high))
    # Return information.
    return indices, thresholds


def collect_stratification_bins_thresholds(
    values=None,
    bins=None,
    report=None,
):
    """
    Determine values of thresholds for three stratification bins.
    Lower and upper thresholds for a bin cannot be identical.

    arguments:
        values (list<float>): values of continuous variable
        bins (list<list<float>>): proportions for three stratification bins
        report (bool): whether to print reports

    raises:

    returns:
        (list<list<int>>): values of thresholds for each stratification bin

    """

    # Organize values.
    values = copy.deepcopy(values)
    values_sort = sorted(values, reverse=False)
    # Collect thresholds.
    indices = list()
    thresholds = list()
    for bin in bins:
        # Determine low and high thresholds for bin.
        indices, thresholds = determine_stratification_bin_thresholds(
            bin=bin,
            values_sort=values_sort,
            indices=indices,
            thresholds=thresholds,
            report=report,
        )
    # Return information.
    return thresholds


def determine_stratification_bin(
    value=None,
    thresholds=None,
):
    """
    Stratify persons to ordinal bins by their values of continuous variables.

    arguments:
        value (float): value of continuous variable
        thresholds (list<list<int>>): values of thresholds for each
            stratification bin

    raises:

    returns:
        (int): integer bin

    """

    if not math.isnan(value):
        if (thresholds[0][0] <= value and value < thresholds[0][1]):
            return 0
        elif (thresholds[1][0] <= value and value < thresholds[1][1]):
            return 1
        elif len(thresholds) > 2:
            if (thresholds[2][0] <= value and value <= thresholds[2][1]):
                return 2
            else:
                return float("nan")
        else:
            return float("nan")
    else:
        return float("nan")


def stratify_persons_continuous_variable_ordinal(
    variable=None,
    variable_grade=None,
    bins=None,
    data_persons_properties=None,
    report=None,
):
    """
    Stratify persons to ordinal bins by their values of continuous variables.

    arguments:
        variable (str): name of continuous variable for stratification
        variable_grade (str): name for new ordinal variable
        bins (list<list<float>>): proportions for three stratification bins
        data_persons_properties (object): Pandas data frame of persons'
            properties
        report (bool): whether to print reports

    raises:

    returns:
        (object): Pandas data frame of information about persons

    """

    # Copy data.
    data = data_persons_properties.copy(deep=True)
    # Determine whether variable qualifies for stratification.
    series, values_unique = pandas.factorize(
        data[variable],
        sort=True
    )
    if len(values_unique) < 2:
        data[variable_grade] = float("nan")
    else:
        # Report.
        if report:
            utility.print_terminal_partition(level=2)
            print("variable: " + str(variable))
            utility.print_terminal_partition(level=2)
        # Determine thresholds for stratification bins.
        thresholds = collect_stratification_bins_thresholds(
            values=data[variable].to_list(),
            bins=bins,
            report=report,
        )
        # Determine bins.
        data[variable_grade] = data[variable].apply(
            lambda value:
                determine_stratification_bin(
                    value=value,
                    thresholds=thresholds,
                )
        )
        # Report.
        if report:
            utility.print_terminal_partition(level=2)
            for threshold in thresholds:
                print("low threshold: " + str(threshold[0]))
                print("high threshold: " + str(threshold[1]))
                utility.print_terminal_partition(level=3)
    # Return information.
    return data



###############################################################################
# Procedure


def execute_procedure(
    temporary=None,
    dock=None,
):
    """
    Function to execute module's main behavior.

    arguments:
        temporary (str): path to temporary directory for source and product
            directories and files
        dock (str): path to dock directory for source and product
            directories and files

    raises:

    returns:

    """

    # Read source information from file.
    source = read_source(dock=dock)
    print(source["data_raw"])

    # Organize data.
    data_raw = source["data_raw"].copy(deep=True)
    data_raw.drop(
        labels=[
            "albumin_extra", "person_extra",
        ],
        axis="columns",
        inplace=True
    )
    data_raw.set_index(
        "person",
        drop=True,
        inplace=True,
    )
    # Remove observations with missing values for either feature.
    data_raw.dropna(
        axis="index",
        how="any",
        inplace=True,
    )

    # Determine bins of persons by age.
    data_age = stratify_persons_continuous_variable_ordinal(
        variable="age",
        variable_grade="age_grade",
        bins=[[0.0, 0.33], [0.33, 0.67], [0.67, 1.0]],
        data_persons_properties=data_raw,
        report=True,
    )

    # Determine sets of persons by sex and age.

    print(data_age)
    pass



if (__name__ == "__main__"):
    execute_procedure()
