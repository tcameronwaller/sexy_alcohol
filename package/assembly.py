
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
import promiscuity.utility as utility


###############################################################################
# Functionality


def extract_organize_variables_types(
    data_ukbiobank_variables=None,
):
    """
    Organize information about data types of UK Biobank phenotype variables.

    arguments:
        data_identifier_pairs (object): Pandas data frame of information about
            UK Biobank phenotype variables

    raises:

    returns:
        (dict<str>): pairs of variables and data types

    """

    # Copy data.
    data_variables = data_ukbiobank_variables.copy(deep=True)
    # Organize information.
    data_variables = data_variables.loc[
        :, data_variables.columns.isin(["field", "type", "instances_total"])
    ]
    records = utility.convert_dataframe_to_records(data=data_variables)
    # Iterate across records for rows.
    # Collect variables' names and types.
    variables_types = dict()
    for record in records:
        field = str(record["field"])
        type = str(record["type"])
        instances_total_raw = str(record["instances_total"])
        instances_raw = instances_total_raw.split(",")
        for instance_raw in instances_raw:
            instance = str(instance_raw).strip()
            if len(instance) > 0:
                name = str(field + "-" + instance)
                # Create entry for variable's name and type.
                variables_types[name] = type
                pass
            pass
        pass
    # Return information.
    return variables_types


def read_source(path_dock=None):
    """
    Reads and organizes source information from file.

    arguments:
        path_dock (str): path to dock directory for source and product
            directories and files

    raises:

    returns:
        (object): source information

    """

    # Specify directories and files.
    path_data_ukbiobank_variables = os.path.join(
        path_dock, "access", "table_ukbiobank_phenotype_variables.tsv"
    )
    path_exclusion_identifiers = os.path.join(
        path_dock, "access", "list_exclusion_identifiers.txt"
    )
    path_data_identifier_pairs = os.path.join(
        path_dock, "access", "table_identifier_pairs.csv"
    )
    path_data_ukb_41826 = os.path.join(
        path_dock, "access", "ukb41826.raw.tsv"
    )
    path_data_ukb_43878 = os.path.join(
        path_dock, "access", "ukb43878.raw.tsv"
    )
    # Determine variable types.
    data_ukbiobank_variables = pandas.read_csv(
        path_data_ukbiobank_variables,
        sep="\t",
        header=0,
    )
    variables_types = extract_organize_variables_types(
        data_ukbiobank_variables=data_ukbiobank_variables,
    )
    #utility.print_terminal_partition(level=2)
    #print(variables_types["31-0.0"])
    #print(variables_types["22009-0.11"])
    # Read information from file.
    exclusion_identifiers = utility.read_file_text_list(
        delimiter="\n",
        path_file=path_exclusion_identifiers
    )
    data_identifier_pairs = pandas.read_csv(
        path_data_identifier_pairs,
        sep=",",
        header=0,
        dtype="str",
    )
    # Designate variable types to conserve memory.
    data_ukb_41826 = pandas.read_csv(
        path_data_ukb_41826,
        sep="\t",
        header=0,
        dtype=variables_types,
    )
    data_ukb_43878 = pandas.read_csv(
        path_data_ukb_43878,
        sep="\t",
        header=0,
        dtype=variables_types,
    )
    # Compile and return information.
    return {
        "data_ukbiobank_variables": data_ukbiobank_variables,
        "exclusion_identifiers": exclusion_identifiers,
        "data_identifier_pairs": data_identifier_pairs,
        "data_ukb_41826": data_ukb_41826,
        "data_ukb_43878": data_ukb_43878,
    }


def merge_data_variables_identifiers(
    data_identifier_pairs=None,
    data_ukb_41826=None,
    data_ukb_43878=None,
    report=None,
):
    """
    Reads and organizes source information from file.

    arguments:
        data_identifier_pairs (object): Pandas data frame of associations
            between "IID" and "eid"
        data_ukb_41826 (object): Pandas data frame of variables from UK Biobank
            phenotype accession 41826
        data_ukb_43878 (object): Pandas data frame of variables from UK Biobank
            phenotype accession 43878
        report (bool): whether to print reports

    raises:

    returns:

    """

    # Organize data.
    data_identifier_pairs.set_index(
        "eid",
        drop=True,
        inplace=True,
    )
    data_ukb_41826.set_index(
        "eid",
        drop=True,
        inplace=True,
    )
    data_ukb_43878.set_index(
        "eid",
        drop=True,
        inplace=True,
    )
    # Merge data tables using database-style join.
    # Alternative is to use DataFrame.join().
    data_merge = data_identifier_pairs.merge(
        data_ukb_41826,
        how="outer",
        left_on="eid",
        right_on="eid",
        suffixes=("_pairs", "_41826"),
    )
    data_merge = data_merge.merge(
        data_ukb_43878,
        how="outer",
        left_on="eid",
        right_on="eid",
        suffixes=("_41826", "_43878"),
    )
    # Remove excess columns.

    # Report.
    if report:
        utility.print_terminal_partition(level=2)
        print(data_ukb_41826)
        utility.print_terminal_partition(level=2)
        print(data_ukb_43878)
        utility.print_terminal_partition(level=2)
        print(data_merge)
    # Return information.
    return data_merge


def calculate_alcohol_consumption_monthly(
    alcohol_status=None,
    alcohol_weekly=None,
    alcohol_monthly=None,
    weeks_per_month=None,
):
    """
    Calculate monthly alcohol consumption in drinks.

    arguments:
        alcohol_status (str): person's status of alcohol consumption
        alcohol_weekly (float): sum of weekly drinks from weekly variables
        alcohol_monthly (float): sum of monthly drinks from monthly variables
        weeks_per_month (float): factor to use for weeks per month

    raises:

    returns:
        (float): person's monthly alcohol consumption in drinks

    """

    # Calculate monthly drinks.
    if alcohol_status == "Never":
        drinks_monthly = 0.0
    elif alcohol_status == "Current":
        # Use as much information as is available.
        if not math.isnan(alcohol_weekly) and not math.isnan(alcohol_monthly):
            drinks_monthly = (
                alcohol_monthly + (weeks_per_month * alcohol_weekly)
            )
        elif not math.isnan(alcohol_weekly):
            drinks_monthly = (weeks_per_month * alcohol_weekly)
        elif not math.isnan(alcohol_monthly):
            drinks_monthly = alcohol_monthly
        else:
            # There is no available information about alcohol consumption
            # in drinks.
            drinks_monthly = float("nan")
    # Return information.
    return drinks_monthly


###############################################################################
# Procedure


def execute_procedure(
    path_dock=None,
):
    """
    Function to execute module's main behavior.

    arguments:
        path_dock (str): path to dock directory for source and product
            directories and files

    raises:

    returns:

    """

    # TODO: 1) remove data columns for variable instances we don't want to use
    # TODO: 2) get merge to work as efficiently as practical
    # TODO: 3) derive alcohol consumption quantity and frequency variables


    utility.print_terminal_partition(level=1)
    print(path_dock)
    print("version check: 1")

    # Read source information from file.
    # Exclusion identifiers are "eid".
    source = read_source(path_dock=path_dock)

    if False:
        # Remove data columns for irrelevant variable instances.
        prune = remove_data_irrelevant_variable_instances(
            data_ukbiobank_variables=source["data_ukbiobank_variables"],
            data_ukb_41826=source["data_ukb_41826"],
            data_ukb_43878=source["data_ukb_43878"],
            report=True,
        )

    # Merge tables.
    data_raw = merge_data_variables_identifiers(
        data_identifier_pairs=prune["data_identifier_pairs"],
        data_ukb_41826=prune["data_ukb_41826"],
        data_ukb_43878=prune["data_ukb_43878"],
        report=True,
    )


    # Organize general phenotypes.

    # Organize genotype principal components.

    # Organize alcohol phenotypes.

    pass



if (__name__ == "__main__"):
    execute_procedure()
