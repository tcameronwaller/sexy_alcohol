
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
import time

# Relevant

import numpy
import pandas
import scipy.stats

# Custom
import promiscuity.utility as utility
#import promiscuity.plot as plot
import uk_biobank.assembly
#import uk_biobank.organization



###############################################################################
# Functionality

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
    print("version check: 1")
    # Pause procedure.
    time.sleep(5.0)

    # Execute assembly procedure from uk_biobank package.
    uk_biobank.assembly.execute_procedure(path_dock=path_dock)
    utility.print_terminal_partition(level=1)
    print("From package 'uk_biobank', procedure 'assembly' is complete.")

    pass



if (__name__ == "__main__"):
    execute_procedure()
