
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
import promiscuity.regression as regression
import uk_biobank.organization as ukb_organ
import uk_biobank.stratification as ukb_strat
import uk_biobank.description as ukb_descr

###############################################################################
# Functionality



##########
# Initialization


def initialize_directories(
    restore=None,
    path_dock=None,
):
    """
    Initialize directories for procedure's product files.

    arguments:
        restore (bool): whether to remove previous versions of data
        path_dock (str): path to dock directory for source and product
            directories and files

    raises:

    returns:
        (dict<str>): collection of paths to directories for procedure's files

    """

    # Collect paths.
    paths = dict()
    # Define paths to directories.
    paths["dock"] = path_dock
    paths["regression"] = os.path.join(path_dock, "regression")

    # Remove previous files to avoid version or batch confusion.
    if restore:
        utility.remove_directory(path=paths["regression"])
    # Initialize directories.
    utility.create_directories(
        path=paths["regression"]
    )
    # Return information.
    return paths


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
        path_dock, "organization",
        "table_phenotypes.pickle",
    )

    # Read information from file.
    table_phenotypes = pandas.read_pickle(
        path_table_phenotypes
    )
    # Compile and return information.
    return {
        "table_phenotypes": table_phenotypes,
        #"table_ukb_samples": table_ukb_samples,
    }



# TODO: filter to current alcohol consumers
# TODO: then alcohol_frenquency as ordinal outcome



def organize_cohorts_models_phenotypes_regressions_alcohol(
    table=None,
    report=None,
):
    """
    Organize regressions.

    arguments:
        table (object): Pandas data frame of phenotype variables across UK
            Biobank cohort
        report (bool): whether to print reports

    raises:

    returns:
        (dict): information from regressions

    """

    # Define relevant cohorts.
    cohorts_records = ukb_strat.stratify_set_alcohol_sex_menopause_age(
        table=table
    )

    # TODO: TCW 19 August 2021
    # TODO: eventually... I will need cohort-specific models...

    # Define outcome dependent variables.
    outcomes = [
        "alcohol_frequency",
    ]
    # Define predictor independent variables.
    predictors_region = ["assessment_region",]
    predictors_season = ["assessment_season",]
    predictors_site_components = [
        "site-component_1", "site-component_2", "site-component_3",
        "site-component_4", "site-component_5", "site-component_6",
        "site-component_7", "site-component_8", "site-component_9",
        "site-component_10", "site-component_11", "site-component_12",
        "site-component_13", "site-component_14", "site-component_15",
        "site-component_16", "site-component_17", "site-component_18",
        "site-component_19", "site-component_20",
    ]
    predictors_month_components = [
        "month-component_1", "month-component_2", "month-component_3",
        "month-component_4", "month-component_5", "month-component_6",
        "month-component_7", "month-component_8", "month-component_9",
        "month-component_10",
    ]
    predictors_month_indicators = [
        "month-indicator_January", "month-indicator_February",
        "month-indicator_March", #"month-indicator_April",
        "month-indicator_May", "month-indicator_June",
        "month-indicator_July", "month-indicator_August",
        "month-indicator_September", "month-indicator_October",
        "month-indicator_November", "month-indicator_December",
    ]

    # Iterate across cohorts.
    for cohort_record in cohorts_records:
        cohort = cohort_record["cohort"]
        menstruation = cohort_record["menstruation"]
        table_cohort = cohort_record["table"]
        # Iterate across outcomes (dependent variables).
        for outcome in outcomes:
            # Specify predictors.
            #predictors = predictors_month_components
            #predictors = predictors_month_indicators
            #predictors = predictors_site_components
            #predictors = predictors_region
            predictors = predictors_season

            # Report.
            if report:
                utility.print_terminal_partition(level=3)
                print("report: ")
                print("organize_cohorts_models_phenotypes_regressions()")
                utility.print_terminal_partition(level=5)
                print("cohort: " + str(cohort))
                print("outcome: " + str(outcome))
                utility.print_terminal_partition(level=5)
            pail_regression = regression.regress_linear_ordinary_least_squares(
                dependence=outcome, # parameter
                independence=predictors, # parameter
                threshold_samples=100,
                table=table_cohort,
                report=report,
            )
            pass
        pass

    # Compile information.
    pail = dict()
    # Return information.
    return pail


def organize_cohorts_models_phenotypes_regressions(
    table=None,
    report=None,
):
    """
    Organize regressions.

    arguments:
        table (object): Pandas data frame of phenotype variables across UK
            Biobank cohort
        report (bool): whether to print reports

    raises:

    returns:
        (dict): information from regressions

    """

    # Define relevant cohorts.
    cohorts_records = ukb_strat.stratify_set_primary_sex_menopause_age(
        table=table
    )
    cohorts_relevant = [
        "female-premenopause", "female-perimenopause", "female-postmenopause",
        "male", "male-younger", "male-older"
    ]
    cohorts_records = list(filter(
        lambda cohort_record: (cohort_record["cohort"] in cohorts_relevant),
        cohorts_records
    ))

    # TODO: TCW 19 August 2021
    # TODO: eventually... I will need cohort-specific models...

    # Define outcome dependent variables.
    hormones = [
        "vitamin_d", "albumin", "steroid_globulin",
        "oestradiol", "testosterone",
    ]
    # Define predictor independent variables.
    predictors_region = ["assessment_region",]
    predictors_season = ["assessment_season",]
    predictors_site_components = [
        "site-component_1", "site-component_2", "site-component_3",
        "site-component_4", "site-component_5", "site-component_6",
        "site-component_7", "site-component_8", "site-component_9",
        "site-component_10", "site-component_11", "site-component_12",
        "site-component_13", "site-component_14", "site-component_15",
        "site-component_16", "site-component_17", "site-component_18",
        "site-component_19", "site-component_20",
    ]
    predictors_month_components = [
        "month-component_1", "month-component_2", "month-component_3",
        "month-component_4", "month-component_5", "month-component_6",
        "month-component_7", "month-component_8", "month-component_9",
        "month-component_10",
    ]
    predictors_month_indicators = [
        "month-indicator_January", "month-indicator_February",
        "month-indicator_March", #"month-indicator_April",
        "month-indicator_May", "month-indicator_June",
        "month-indicator_July", "month-indicator_August",
        "month-indicator_September", "month-indicator_October",
        "month-indicator_November", "month-indicator_December",
    ]

    # Iterate across cohorts.
    for cohort_record in cohorts_records:
        cohort = cohort_record["cohort"]
        menstruation = cohort_record["menstruation"]
        table_cohort = cohort_record["table"]
        # Iterate across outcomes (dependent variables).
        for hormone in hormones:
            # Define cohort-specific ordinal representation.
            hormone_ordinal = str(str(hormone) + "_" + str(cohort) + "_ordinal")

            # Specify outcome and predictors.

            outcome = hormone
            #outcome = hormone_ordinal

            #predictors = predictors_month_components
            #predictors = predictors_site_components
            #predictors = predictors_region
            predictors = predictors_season


            # Report.
            if report:
                utility.print_terminal_partition(level=3)
                print("report: ")
                print("organize_cohorts_models_phenotypes_regressions()")
                utility.print_terminal_partition(level=5)
                print("cohort: " + str(cohort))
                print("outcome: " + str(outcome))
                utility.print_terminal_partition(level=5)
            pail_regression = regression.regress_linear_ordinary_least_squares(
                dependence=outcome, # parameter
                independence=predictors, # parameter
                threshold_samples=100,
                table=table_cohort,
                report=report,
            )
            pass
        pass

    # Compile information.
    pail = dict()
    # Return information.
    return pail


################################################################################
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
    print("version check: 3")
    # Pause procedure.
    time.sleep(5.0)

    # Initialize directories.
    paths = initialize_directories(
        restore=True,
        path_dock=path_dock,
    )
    # Read source information from file.
    # Exclusion identifiers are "eid".
    source = read_source(
        path_dock=path_dock,
        report=True,
    )

    # Preliminary organization of regressions.
    pail = organize_cohorts_models_phenotypes_regressions(
        table=source["table_phenotypes"],
        report=True
    )


    pass


if (__name__ == "__main__"):
    execute_procedure()
