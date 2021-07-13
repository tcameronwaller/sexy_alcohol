
"""
...

"""

###############################################################################
# Notes

###############################################################################
# Installation and importation

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
import time

# Relevant

import numpy
import scipy.stats
import pandas
pandas.options.mode.chained_assignment = None # default = "warn"

# Custom
import promiscuity.utility as utility
import promiscuity.plot as plot
import uk_biobank.organization as ukb_organization



###############################################################################
# Functionality

##########
# Read


def read_source(
    path_dock=None,
    report=None,
):
    """
    Reads and organizes source information from file.

    Notice that Pandas does not accommodate missing values within series of
    integer variable types.

    arguments:
        path_dock (str): path to dock directory for source and product
            directories and files
        report (bool): whether to print reports

    raises:

    returns:
        (object): source information

    """

    # Specify directories and files.
    path_table_phenotypes = os.path.join(
        path_dock, "organization_freeze_2021-07-08", "cohorts_models",
        "table_female_premenopause_ordinal_testosterone.tsv",
    )

    # Read information from file.
    table_phenotypes = pandas.read_csv(
        path_table_phenotypes,
        sep="\t", # "," or "\t"
        header=0,
        #dtype="string",
        na_values=["NA", "<NA>"],
        keep_default_na=True,
    )
    # Compile and return information.
    return {
        "table_phenotypes": table_phenotypes,
        #"table_ukb_samples": table_ukb_samples,
    }


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

    utility.print_terminal_partition(level=1)
    print(path_dock)
    print("version check: 21")
    # Pause procedure.
    time.sleep(5.0)

    # Read source information from file.
    # Exclusion identifiers are "eid".
    source = read_source(
        path_dock=path_dock,
        report=False,
    )

    figure = ukb_organization.plot_variable_means_bars_by_day(
        label="hello world",
        column_phenotype="testosterone",
        column_day="menstruation_days",
        threshold_days=35,
        table=source["table_phenotypes"],
    )

    pass



if (__name__ == "__main__"):
    execute_procedure()
