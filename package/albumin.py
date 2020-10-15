
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
#import utility


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


    print(data_raw)
    pass



if (__name__ == "__main__"):
    execute_procedure()
