
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
import promiscuity.plot as plot

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
    paths["organization"] = os.path.join(path_dock, "organization")
    paths["trial"] = os.path.join(
        path_dock, "organization", "trial"
    )
    paths["alcohol"] = os.path.join(
        path_dock, "organization", "alcohol"
    )
    paths["plot"] = os.path.join(
        path_dock, "organization", "plot"
    )
    # Remove previous files to avoid version or batch confusion.
    if restore:
        utility.remove_directory(path=paths["organization"])
    # Initialize directories.
    utility.create_directories(
        path=paths["organization"]
    )
    utility.create_directories(
        path=paths["trial"]
    )
    utility.create_directories(
        path=paths["alcohol"]
    )
    utility.create_directories(
        path=paths["plot"]
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
    path_table_assembly = os.path.join(
        path_dock, "assembly", "table_phenotypes.pickle"
    )
    # Read information from file.
    table_assembly = pandas.read_pickle(
        path_table_assembly
    )
    # Compile and return information.
    return {
        "table_assembly": table_assembly,
    }


##########
# Organization


def convert_table_variable_types(
    table=None,
    report=None,
):
    """
    Converts data variable types.

    The UK Biobank encodes several nominal variables with integers. Missing
    values for these variables necessitates some attention to type conversion
    from string to float for analysis.

    arguments:
        table (object): Pandas data frame of phenotype variables across UK
            Biobank cohort
        report (bool): whether to print reports

    raises:

    returns:
        (object): Pandas data frame of phenotype variables across UK Biobank
            cohort

    """

    # Report.
    if report:
        utility.print_terminal_partition(level=2)
        print("Before type conversion")
        utility.print_terminal_partition(level=3)
        print(table.dtypes)
    # Copy data.
    table = table.copy(deep=True)
    # Convert data variable types.
    # Alcohol variables.
    table["1558-0.0"] = pandas.to_numeric(
        table["1558-0.0"],
        errors="coerce", # force any invalid values to missing or null
        downcast="float",
    )
    table["3731-0.0"] = pandas.to_numeric(
        table["3731-0.0"],
        errors="coerce", # force any invalid values to missing or null
        downcast="float",
    )
    table["1628-0.0"] = pandas.to_numeric(
        table["1628-0.0"],
        errors="coerce", # force any invalid values to missing or null
        downcast="float",
    )
    table["20117-0.0"] = pandas.to_numeric(
        table["20117-0.0"],
        errors="coerce", # force any invalid values to missing or null
        downcast="float",
    )
    table["20414-0.0"] = pandas.to_numeric(
        table["20414-0.0"],
        errors="coerce", # force any invalid values to missing or null
        downcast="float",
    )
    table["20403-0.0"] = pandas.to_numeric(
        table["20403-0.0"],
        errors="coerce", # force any invalid values to missing or null
        downcast="float",
    )
    table["20416-0.0"] = pandas.to_numeric(
        table["20416-0.0"],
        errors="coerce", # force any invalid values to missing or null
        downcast="float",
    )
    # Menopause variables.
    table["2724-0.0"] = pandas.to_numeric(
        table["2724-0.0"],
        errors="coerce", # force any invalid values to missing or null
        downcast="float",
    )
    table["3591-0.0"] = pandas.to_numeric(
        table["3591-0.0"],
        errors="coerce", # force any invalid values to missing or null
        downcast="float",
    )
    table["2834-0.0"] = pandas.to_numeric(
        table["2834-0.0"],
        errors="coerce", # force any invalid values to missing or null
        downcast="float",
    )

    if False:
        table["20117-0.0"].fillna(
            value="-3",
            axis="index",
            inplace=True,
        )
        table["20117-0.0"].astype(
            "float32",
            copy=True,
        )
    # Report.
    if report:
        utility.print_terminal_partition(level=2)
        print("After type conversion")
        utility.print_terminal_partition(level=3)
        print(table.dtypes)
        utility.print_terminal_partition(level=4)
        print("20117-0.0 value counts: ")
        print(table["20117-0.0"].value_counts())
    # Return information.
    return table


def translate_alcohol_none(
    frequency=None,
    previous=None,
):
    """
    Translate information from UK Biobank about whether person
    never consumes any alcohol.

    "frequency", field 1558: "Alcohol intake frequency"
    UK Biobank data coding 100402 for variable field 1558.
    "daily or almost daily": 1
    "three or four times a week": 2
    "once or twice a week": 3
    "one to three times a month": 4
    "special occasions only": 5
    "never": 6
    "prefer not to answer": -3

    "previous", field 3731: "Former alcohol drinker"
    Variable 3731 was only collected for persons who never consume any alcohol
    currently (UK Biobank variable 1558).
    UK Biobank data coding 100352 for variable field 3731.
    "yes": 1
    "no": 0
    "prefer not to answer": -3

    Accommodate inexact float values.

    arguments:
        frequency (float): frequency of alcohol consumption, UK Biobank field
            1558
        previous (float): previous alcohol consumption, UK Biobank field
            3731

    raises:

    returns:
        (bool): whether person never consumes any alcohol

    """

    # Determine whether the variable has a valid (non-missing) value.
    # Only consider interpretable values to be valid.
    if (
        (not pandas.isna(frequency)) and
        (0.5 <= frequency and frequency < 6.5)
    ):
        # The variable has a valid value.
        # Determine whether the person ever consumes any alcohol currently.
        if (5.5 <= frequency and frequency < 6.5):
            # frequency = "never"
            # Determine whether the person ever consumed any alcohol
            # previously.
            if (
                (not pandas.isna(previous)) and
                (-0.5 <= previous and previous < 1.5)
            ):
                if (0.5 <= previous and previous < 1.5):
                    # previous = "yes"
                    # The person consumed alcohol previously.
                    alcohol_none = False
                elif (-0.5 <= previous and previous < 0.5):
                    # previous = "no"
                    # The person does not consume alcohol currently and did not
                    # consume alcohol previously.
                    alcohol_none = True
            else:
                # No valid information about previous alcohol consumption.
                # The person does not consume alcohol currently, but we do not
                # know about any previous consumption.
                alcohol_none = True
        else:
            # Persons consumes alcohol currently.
            alcohol_none = False
    else:
        alcohol_none = float("nan")
    # Return information.
    return alcohol_none


def translate_alcohol_consumption_frequency(
    frequency=None,
):
    """
    Translate information from UK Biobank about whether person
    never consumes any alcohol.

    "frequency", field 1558: "Alcohol intake frequency"
    UK Biobank data coding 100402 for variable field 1558.
    "daily or almost daily": 1
    "three or four times a week": 2
    "once or twice a week": 3
    "one to three times a month": 4
    "special occasions only": 5
    "never": 6
    "prefer not to answer": -3

    Accommodate inexact float values.

    arguments:
        frequency (float): frequency of alcohol consumption, UK Biobank field
            1558

    raises:

    returns:
        (int): ordinal representation of person's frequency of alcohol
            consumption

    """

    # Determine whether the variable has a valid (non-missing) value.
    if (
        (not pandas.isna(frequency)) and
        (0.5 <= frequency and frequency < 6.5)
    ):
        # The variable has a valid value.
        if (5.5 <= frequency and frequency < 6.5):
            # "never"
            alcohol_frequency = 0
        elif (4.5 <= frequency and frequency < 5.5):
            # "special occasions only"
            alcohol_frequency = 1
        elif (3.5 <= frequency and frequency < 4.5):
            # "one to three times a month"
            alcohol_frequency = 2
        elif (2.5 <= frequency and frequency < 3.5):
            # "once or twice a week"
            alcohol_frequency = 3
        elif (1.5 <= frequency and frequency < 2.5):
            # "three or four times a week"
            alcohol_frequency = 4
        elif (0.5 <= frequency and frequency < 1.5):
            # "daily or almost daily"
            alcohol_frequency = 5
    else:
        alcohol_frequency = float("nan")
    # Return information.
    return alcohol_frequency


def calculate_sum_drinks(
    beer_cider=None,
    wine_red=None,
    wine_white=None,
    port=None,
    liquor=None,
    other=None,
):
    """
    Calculates the sum of drinks.

    UK Biobank data coding 100291.
    "do not know": -1
    "prefer not to answer": -3

    arguments:
        beer_cider (int): count of drinks by type
        wine_red (int): count of drinks by type
        wine_white (int): count of drinks by type
        port (int): count of drinks by type
        liquor (int): count of drinks by type
        other (int): count of drinks by type
        report (bool): whether to print reports

    raises:

    returns:
        (int): sum of counts of drinks

    """

    # Consider all types of alcoholic beverage.
    types = [beer_cider, wine_red, wine_white, port, liquor, other]
    # Determine whether any relevant variables have missing values.
    valid = False
    for type in types:
        if (not pandas.isna(type) and (type != -1) and (type != -3)):
            valid = True
            pass
        pass
    if valid:
        # Variables have valid values.
        # Calculate sum of drinks.
        drinks = 0
        for type in types:
            if ((not pandas.isna(type)) and (type >= 0)):
                drinks = drinks + type
                pass
            pass
    else:
        drinks = float("nan")
    return drinks


def calculate_total_alcohol_consumption_monthly(
    drinks_weekly=None,
    drinks_monthly=None,
    weeks_per_month=None,
):
    """
    Calculate monthly alcohol consumption in drinks.

    arguments:
        drinks_weekly (float): sum of weekly drinks from weekly variables
        drinks_monthly (float): sum of monthly drinks from monthly variables
        weeks_per_month (float): factor to use for weeks per month

    raises:

    returns:
        (float): person's monthly alcohol consumption in drinks

    """

    # Use as much valid information as is available.
    if (not math.isnan(drinks_weekly) and not math.isnan(drinks_monthly)):
        alcohol_drinks_monthly = (
            drinks_monthly + (weeks_per_month * drinks_weekly)
        )
    elif (not math.isnan(drinks_weekly)):
        alcohol_drinks_monthly = (weeks_per_month * drinks_weekly)
    elif (not math.isnan(drinks_monthly)):
        alcohol_drinks_monthly = drinks_monthly
    else:
        # There is no valid information about alcohol consumption quantity.
        alcohol_drinks_monthly = float("nan")
        pass
    return alcohol_drinks_monthly


def determine_total_alcohol_consumption_monthly(
    alcohol_frequency=None,
    drinks_weekly=None,
    drinks_monthly=None,
    weeks_per_month=None,
):
    """
    Calculate monthly alcohol consumption in drinks.

    UK Biobank data coding 90.
    "current": 2
    "previous": 1
    "never": 0
    "prefer not to answer": -3

    Accommodate inexact float values.

    arguments:
        alcohol_frequency (int): ordinal representation of person's frequency
            of alcohol consumption
        drinks_weekly (float): sum of weekly drinks from weekly variables
        drinks_monthly (float): sum of monthly drinks from monthly variables
        weeks_per_month (float): factor to use for weeks per month

    raises:

    returns:
        (float): person's monthly alcohol consumption in drinks

    """

    # Calculate alcohol consumption quantity.
    alcohol_monthly = calculate_total_alcohol_consumption_monthly(
        drinks_weekly=drinks_weekly,
        drinks_monthly=drinks_monthly,
        weeks_per_month=weeks_per_month,
    )
    # Consider alcohol consumption status.
    if (
        (not math.isnan(alcohol_frequency)) and
        (-0.5 <= alcohol_frequency and alcohol_frequency < 0.5)
    ):
        # Person never consumes any alcohol currently.
        if (not math.isnan(alcohol_monthly)):
            alcohol_drinks_monthly = alcohol_monthly
        else:
            alcohol_drinks_monthly = 0.0
    else:
        if (not math.isnan(alcohol_monthly)):
            alcohol_drinks_monthly = alcohol_monthly
        else:
            alcohol_drinks_monthly = float("nan")
    # Return information.
    return alcohol_drinks_monthly


def organize_current_alcohol_consumption_variables(
    table=None,
    report=None,
):
    """
    Organizes information about alcohol consumption in standard drinks monthly.

    arguments:
        table (object): Pandas data frame of phenotype variables across UK
            Biobank cohort
        report (bool): whether to print reports

    raises:

    returns:
        (dict): collection of information about quantity of alcohol consumption

    """

    # Copy data.
    table = table.copy(deep=True)
    # Determine whether person never consumes any alcohol, either currently or
    # previously.
    table["alcohol_none"] = table.apply(
        lambda row:
            translate_alcohol_none(
                frequency=row["1558-0.0"],
                previous=row["3731-0.0"],
            ),
        axis="columns", # apply across rows
    )
    # Determine person's frequency of alcohol consumption.
    table["alcohol_frequency"] = table.apply(
        lambda row:
            translate_alcohol_consumption_frequency(
                frequency=row["1558-0.0"],
            ),
        axis="columns", # apply across rows
    )
    # Calculate sum of drinks weekly.
    table["drinks_weekly"] = table.apply(
        lambda row:
            calculate_sum_drinks(
                beer_cider=row["1588-0.0"],
                wine_red=row["1568-0.0"],
                wine_white=row["1578-0.0"],
                port=row["1608-0.0"],
                liquor=row["1598-0.0"],
                other=row["5364-0.0"],
            ),
        axis="columns", # apply across rows
    )
    # Calculate sum of drinks monthly.
    table["drinks_monthly"] = table.apply(
        lambda row:
            calculate_sum_drinks(
                beer_cider=row["4429-0.0"],
                wine_red=row["4407-0.0"],
                wine_white=row["4418-0.0"],
                port=row["4451-0.0"],
                liquor=row["4440-0.0"],
                other=row["4462-0.0"],
            ),
        axis="columns", # apply across rows
    )
    # Determine sum of total drinks monthly.
    table["alcohol_drinks_monthly"] = table.apply(
        lambda row:
            determine_total_alcohol_consumption_monthly(
                alcohol_frequency=row["alcohol_frequency"],
                drinks_weekly=row["drinks_weekly"],
                drinks_monthly=row["drinks_monthly"],
                weeks_per_month=4.345, # 52.143 weeks per year (12 months)
            ),
        axis="columns", # apply across rows
    )
    # Remove columns for variables that are not necessary anymore.
    table_clean = table.copy(deep=True)
    table_clean.drop(
        labels=[
            "1588-0.0", "1568-0.0", "1578-0.0", "1608-0.0", "1598-0.0",
            "5364-0.0",
            "4429-0.0", "4407-0.0", "4418-0.0", "4451-0.0", "4440-0.0",
            "4462-0.0",
            #"20117-0.0",
            "drinks_weekly",
            "drinks_monthly",
        ],
        axis="columns",
        inplace=True
    )
    # Organize data for report.
    table_report = table.copy(deep=True)
    table_report = table_report.loc[
        :, table_report.columns.isin([
            "eid", "IID",
            "1558-0.0", "3731-0.0",
            "1588-0.0", "1568-0.0", "1578-0.0", "1608-0.0", "1598-0.0",
            "5364-0.0",
            "4429-0.0", "4407-0.0", "4418-0.0", "4451-0.0", "4440-0.0",
            "4462-0.0",
            "20117-0.0",
            "alcohol_none",
            "alcohol_frequency",
            "drinks_weekly",
            "drinks_monthly",
            "alcohol_drinks_monthly",
        ])
    ]
    # Report.
    if report:
        utility.print_terminal_partition(level=2)
        print("Summary of alcohol consumption quantity variables: ")
        print(table_report)
    # Collect information.
    bucket = dict()
    bucket["table"] = table
    bucket["table_clean"] = table_clean
    bucket["table_report"] = table_report
    # Return information.
    return bucket


def determine_previous_alcohol_consumption(
    status=None,
    previous=None,
    comparison=None,
):
    """
    Translate information from UK Biobank about whether person
    never consumes any alcohol.

    "status", field 20117: "Alcohol drinker status"
    UK Biobank data coding 90 for variable field 20117.
    "current": 2
    "previous": 1
    "never": 0
    "prefer not to answer": -3

    "previous", field 3731: "Former alcohol drinker"
    Variable 3731 was only collected for persons who never consume any alcohol
    currently (UK Biobank variable 1558).
    UK Biobank data coding 100352 for variable field 3731.
    "yes": 1
    "no": 0
    "prefer not to answer": -3

    "comparison", field 1628: "Alcohol intake versus 10 years previously"
    Variable 1628 was only collected for persons who consume alcohol currently
    (UK Biobank variable 1558).
    UK Biobank data coding 100417 for variable field 1628.
    "more nowadays": 1
    "about the same": 2
    "less nowadays": 3
    "do not know": -1
    "prefer not to answer": -3

    Accommodate inexact float values.

    arguments:
        status (float): status of alcohol consumption, UK Biobank field
            20117
        previous (float): previous alcohol consumption, UK Biobank field
            3731
        comparison (float): comparison to previous alcohol consumption, UK
            Biobank field 1628

    raises:

    returns:
        (int): ordinal representation of person's frequency of alcohol
            consumption

    """

    # Determine whether the person consumed alcohol previously.
    if (
        (not pandas.isna(previous)) and
        (-0.5 <= previous and previous < 1.5)
    ):
        if (0.5 <= previous and previous < 1.5):
            # The person consumed alcohol previously.
            alcohol_previous = 1
        elif (-0.5 <= previous and previous < 0.5):
            # The person did not consume alcohol previously.
            alcohol_previous = 0
    else:
        alcohol_previous = float("nan")
    # Determine how current alcohol consumption compares to previous.
    if (
        (not pandas.isna(comparison)) and
        (-0.5 <= comparison and comparison < 3.5)
    ):
        if (0.5 <= comparison and comparison < 1.5):
            # "more nowadays"
            alcohol_comparison = 1
        elif (1.5 <= comparison and comparison < 2.5):
            # "about the same"
            alcohol_comparison = 2
        elif (2.5 <= comparison and comparison < 3.5):
            # "less nowadays"
            alcohol_comparison = 3
    else:
        alcohol_comparison = float("nan")
    # Combine variables.
    if (
        (not math.isnan(alcohol_previous)) and
        (not math.isnan(alcohol_comparison))
    ):
        if (alcohol_previous >= alcohol_comparison):
            alcohol_combination = alcohol_previous
        elif (alcohol_previous < alcohol_comparison):
            alcohol_combination = alcohol_comparison
    elif (not math.isnan(alcohol_previous)):
        alcohol_combination = alcohol_previous
    elif (not math.isnan(alcohol_comparison)):
        alcohol_combination = alcohol_comparison
    else:
        alcohol_combination = float("nan")
    # Return information.
    return alcohol_combination


def organize_previous_alcohol_consumption_variables(
    table=None,
    report=None,
):
    """
    Organizes information about previous alcohol consumption.

    arguments:
        table (object): Pandas data frame of phenotype variables across UK
            Biobank cohort
        report (bool): whether to print reports

    raises:

    returns:
        (dict): collection of information about quantity of alcohol consumption

    """

    # Copy data.
    table = table.copy(deep=True)
    # Determine whether person never consumes any alcohol.
    table["alcohol_previous"] = table.apply(
        lambda row:
            determine_previous_alcohol_consumption(
                status=row["20117-0.0"],
                previous=row["3731-0.0"],
                comparison=row["1628-0.0"],
            ),
        axis="columns", # apply across rows
    )
    # Remove columns for variables that are not necessary anymore.
    table_clean = table.copy(deep=True)
    table_clean.drop(
        labels=[
            "3731-0.0", "1628-0.0", "20117-0.0",
        ],
        axis="columns",
        inplace=True
    )
    # Organize data for report.
    table_report = table.copy(deep=True)
    table_report = table_report.loc[
        :, table_report.columns.isin([
            "eid", "IID",
            "alcohol_previous",
            "3731-0.0", "1628-0.0", "20117-0.0",
        ])
    ]
    # Report.
    if report:
        utility.print_terminal_partition(level=2)
        print("Summary of alcohol consumption quantity variables: ")
        print(table_report)
    # Collect information.
    bucket = dict()
    bucket["table"] = table
    bucket["table_clean"] = table_clean
    bucket["table_report"] = table_report
    # Return information.
    return bucket


##########
# Trial


def insert_family_identifier_sort_column_sequence_plink(
    table=None,
):
    """
    Insert empty family identifiers and sort column sequence for PLINK format.

    arguments:
        table (object): Pandas data frame of information about phenotype and
            covariate variables for GWAS

    raises:

    returns:
        (object): Pandas data frame of information about phenotype and
            covariate variables in format for GWAS in PLINK

    """

    # Copy data.
    table = table.copy(deep=True)
    # Introduce family identifier.
    table["#FID"] = 0
    # Sort column sequence.
    columns = table.columns.to_list()
    columns_sequence = list(filter(
        lambda element: element not in ["IID", "FID"],
        elements
    ))
    columns_sequence.insert(0, "IID") # second column
    columns_sequence.insert(0, "#FID") # first column
    table_columns = table.loc[
        :, table.columns.isin(columns_sequence)
    ]
    table_sequence = table_columns[[*columns_sequence]]
    # Return information.
    return table_sequence


def organize_trial_phenotypes_covariates(
    table=None,
    report=None,
):
    """
    Organize table of phenotypes and covariates for GWAS.

    arguments:
        table (object): Pandas data frame of information about UK Biobank
            phenotype variables
        report (bool): whether to print reports

    raises:

    returns:
        (object): Pandas data frame of information about UK Biobank phenotype
            variables

    """

    # Copy data.
    table = table.copy(deep=True)
    # Organize variables.
    table["sex"] = table["31-0.0"]
    table["age"] = table["21022-0.0"]
    table["testosterone"] = table["30850-0.0"]
    # Select records.
    table.dropna(
        axis="index",
        how="any",
        subset=["alcohol_none"],
        inplace=True,
    )
    table_alcohol = table.loc[(table["alcohol_none"] == False), :]
    table_male = table.loc[(table["sex"] == 1.0), :]
    table_testosterone = table_male.loc[
        (~pandas.isna(table_male["testosterone"])), :
    ]
    table_relevance = table_testosterone.loc[
        :, table_testosterone.columns.isin([
            "eid", "IID",
            "sex", "age", "testosterone",
            "alcohol_none",
            "alcohol_frequency",
            "alcohol_drinks_monthly",
        ])
    ]
    # Introduce family identifiers and sort columns for PLINK format.
    table_format = insert_family_identifier_sort_column_sequence_plink(
        table=table_relevance,
    )
    # Report.
    if report:
        utility.print_terminal_partition(level=2)
        print("...after organization...")
        print("table shape: " + str(table_format.shape))
        print(table_format)
        utility.print_terminal_partition(level=4)
    # Return information.
    return table_format





def translate_alcohol_none_auditc(
    frequency=None,
):
    """
    Translates information from AUDIT-C questionnaire about whether person
    never consumes any alcohol.

    "frequency", field 20414: "Frequency of drinking alcohol"
    UK Biobank data coding 521 for variable field 20414.
    "four or more times a week": 4
    "two to three times a week": 3
    "two to four times a month": 2
    "monthly or less": 1
    "never": 0
    "prefer not to answer": -818

    Accommodate inexact float values.

    arguments:
        frequency (float): AUDIT-C question 1, UK Biobank field 20414

    raises:

    returns:
        (bool): whether person never consumes any alcohol

    """

    # Determine whether the variable has a valid (non-missing) value.
    if (
        (not pandas.isna(frequency)) and
        (-0.5 <= frequency and frequency < 4.5)
    ):
        # The variable has a valid value.
        # Determine whether the person ever consumes any alcohol.
        if (-0.5 <= frequency and frequency < 0.5):
            # Person never consumes any alcohol.
            alcohol_none_auditc = True
        else:
            # Persons consumes alcohol.
            alcohol_none_auditc = False
    else:
        alcohol_none_auditc = float("nan")
    # Return information.
    return alcohol_none_auditc


def determine_auditc_questionnaire_alcoholism_score(
    frequency=None,
    quantity=None,
    binge=None,
):
    """
    Determine aggregate alcoholism score from responses to the AUDIT-C
    questionnaire.

    "frequency", field 20414: "Frequency of drinking alcohol"
    UK Biobank data coding 521 for variable field 20414.
    "four or more times a week": 4
    "two to three times a week": 3
    "two to four times a month": 2
    "monthly or less": 1
    "never": 0
    "prefer not to answer": -818

    UK Biobank only asked questions "quantity" and "binge" if question
    "frequency" was not "never".

    "quantity", field 20403: "Amount of alcohol drunk on a typical drinking
    day"
    UK Biobank data coding 522 for variable field 20403.
    "ten or more": 5
    "seven, eight, or nine": 4
    "five or six": 3
    "three or four": 2
    "one or two": 1
    "prefer not to answer": -818

    "binge", field 20416: "Frequency of consuming six or more units of alcohol"
    UK Biobank data coding 523 for variable field 20416.
    "daily or almost daily": 5
    "weekly": 4
    "monthly": 3
    "less than monthly": 2
    "never": 1
    "prefer not to answer": -818

    Accommodate inexact float values.

    arguments:
        frequency (float): AUDIT-C question 1, UK Biobank field 20414
        quantity (float): AUDIT-C question 2, UK Biobank field 20403
        binge (float): AUDIT-C question 3, UK Biobank field 20416

    raises:

    returns:
        (float): person's monthly alcohol consumption in drinks

    """

    # Only consider cases with valid responses to all three questions.
    if (
        (
            (not pandas.isna(frequency)) and
            (-0.5 <= frequency and frequency < 4.5)
        ) and
        (
            (not pandas.isna(quantity)) and
            (0.5 <= quantity and quantity < 5.5)
        ) and
        (
            (not pandas.isna(binge)) and
            (0.5 <= binge and binge < 5.5)
        )
    ):
        score = (frequency + quantity + binge)
    else:
        score = float("nan")
    # Return information.
    return score


def organize_auditc_questionnaire_alcoholism_variables(
    table=None,
    report=None,
):
    """
    Organizes information about alcoholism from the AUDIT-C questionnaire.

    arguments:
        table (object): Pandas data frame of phenotype variables across UK
            Biobank cohort
        report (bool): whether to print reports

    raises:

    returns:
        (dict): collection of information about quantity of alcohol consumption

    """

    # Copy data.
    table = table.copy(deep=True)
    # Determine whether person never consumes any alcohol.
    table["alcohol_none_auditc"] = table.apply(
        lambda row:
            translate_alcohol_none_auditc(
                frequency=row["20414-0.0"],
            ),
        axis="columns", # apply across rows
    )
    # Determine alcoholism aggregate score.
    table["alcoholism"] = table.apply(
        lambda row:
            determine_auditc_questionnaire_alcoholism_score(
                frequency=row["20414-0.0"],
                quantity=row["20403-0.0"],
                binge=row["20416-0.0"],
            ),
        axis="columns", # apply across rows
    )
    # Remove columns for variables that are not necessary anymore.
    table_clean = table.copy(deep=True)
    table_clean.drop(
        labels=[
            "20414-0.0", "20403-0.0", "20416-0.0",
        ],
        axis="columns",
        inplace=True
    )
    # Organize data for report.
    table_report = table.copy(deep=True)
    table_report = table_report.loc[
        :, table_report.columns.isin([
            "eid", "IID",
            "20414-0.0", "20403-0.0", "20416-0.0",
            "alcohol_none_auditc",
            "alcoholism",
        ])
    ]
    # Report.
    if report:
        utility.print_terminal_partition(level=2)
        print("Summary of alcohol consumption quantity variables: ")
        print(table_report)
    # Collect information.
    bucket = dict()
    bucket["table"] = table
    bucket["table_clean"] = table_clean
    bucket["table_report"] = table_report
    # Return information.
    return bucket





def plot_variable_series_histogram(
    series=None,
    bins=None,
    file=None,
    path_directory=None,
):
    """
    Plots charts from the analysis process.

    arguments:
        comparison (dict): information for chart
        path_directory (str): path for directory

    raises:

    returns:

    """

    # Specify path to directory and file.
    path_file = os.path.join(
        path_directory, file
    )

    # Define fonts.
    fonts = plot.define_font_properties()
    # Define colors.
    colors = plot.define_color_properties()

    # Report.
    utility.print_terminal_partition(level=1)
    print(file)
    print(len(series))
    # Create figure.
    figure = plot.plot_distribution_histogram(
        series=series,
        name="",
        bin_method="count",
        bin_count=bins,
        label_bins="values",
        label_counts="counts of persons per bin",
        fonts=fonts,
        colors=colors,
        line=False,
        position=1,
        text="",
    )
    # Write figure.
    plot.write_figure_png(
        path=path_file,
        figure=figure
    )

    pass


def organize_plot_variable_histogram_summary_charts(
    table=None,
    paths=None,
):
    """
    Organizes information about alcoholism from the AUDIT-C questionnaire.

    arguments:
        table (object): Pandas data frame of phenotype variables across UK
            Biobank cohort
        paths (dict<str>): collection of paths to directories for procedure's
            files

    raises:

    returns:
        (dict): collection of information about quantity of alcohol consumption

    """

    # Copy data.
    table = table.copy(deep=True)

    # Specify directories and files.
    # Create figures.
    plot_variable_series_histogram(
        series=table["alcohol_frequency"].dropna().to_list(),
        bins=6,
        file="histogram_alcohol_frequency.png",
        path_directory=paths["plot"],
    )
    plot_variable_series_histogram(
        series=table["alcohol_previous"].dropna().to_list(),
        bins=4,
        file="histogram_alcohol_previous.png",
        path_directory=paths["plot"],
    )
    plot_variable_series_histogram(
        series=table["alcohol_drinks_monthly"].dropna().to_list(),
        bins=50,
        file="histogram_alcohol_drinks_monthly.png",
        path_directory=paths["plot"],
    )
    plot_variable_series_histogram(
        series=table["alcoholism"].dropna().to_list(),
        bins=15,
        file="histogram_alcoholism.png",
        path_directory=paths["plot"],
    )

    pass




# TODO: derive "hysterectomy" and "oophrectomy" separately
# TODO: then derive "menopause"

def organize_female_menopause(
    table=None,
    report=None,
):
    """
    Organizes information about whether female persons have experienced
    menopause.

    arguments:
        table (object): Pandas data frame of phenotype variables across UK
            Biobank cohort
        report (bool): whether to print reports

    raises:

    returns:
        (object): Pandas data frame of phenotype variables across UK Biobank
            cohort

    """

    # Copy data.
    table = table.copy(deep=True)
    # Calculate sum of drinks weekly.
    table["menopause"] = table.apply(
        lambda row:
            calculate_sum_drinks(
                beer_cider=row["1588-0.0"],
                wine_red=row["1568-0.0"],
                wine_white=row["1578-0.0"],
                port=row["1608-0.0"],
                liquor=row["1598-0.0"],
                other=row["5364-0.0"],
            ),
        axis="columns", # apply across rows
    )
    table["hysterectomy"] = table.apply(
        lambda row:
            calculate_sum_drinks(
                beer_cider=row["1588-0.0"],
                wine_red=row["1568-0.0"],
                wine_white=row["1578-0.0"],
                port=row["1608-0.0"],
                liquor=row["1598-0.0"],
                other=row["5364-0.0"],
            ),
        axis="columns", # apply across rows
    )
    table["oophorectomy"] = table.apply(
        lambda row:
            calculate_sum_drinks(
                beer_cider=row["1588-0.0"],
                wine_red=row["1568-0.0"],
                wine_white=row["1578-0.0"],
                port=row["1608-0.0"],
                liquor=row["1598-0.0"],
                other=row["5364-0.0"],
            ),
        axis="columns", # apply across rows
    )

    # Report.
    if report:
        utility.print_terminal_partition(level=4)
        print("Final data dimensions: " + str(table_exclusion.shape))
    # Return information.
    return table_exclusion





##########
# Write


def write_product_trial(
    information=None,
    path_parent=None,
):
    """
    Writes product information to file.

    arguments:
        information (object): information to write to file
        path_parent (str): path to parent directory

    raises:

    returns:

    """

    # Specify directories and files.
    path_table_phenotypes = os.path.join(
        path_parent, "table_phenotypes_covariates.pickle"
    )
    path_table_phenotypes_text = os.path.join(
        path_parent, "table_phenotypes_covariates.tsv"
    )
    # Write information to file.
    information["table_phenotypes_covariates"].to_pickle(
        path_table_phenotypes
    )
    information["table_phenotypes_covariates"].to_csv(
        path_or_buf=path_table_phenotypes_text,
        sep="\t",
        header=True,
        index=True,
    )
    pass


def write_product(
    information=None,
    paths=None,
):
    """
    Writes product information to file.

    arguments:
        information (object): information to write to file
        paths (dict<str>): collection of paths to directories for procedure's
            files

    raises:

    returns:

    """

    # Trial organization.
    write_product_trial(
        information=information["trial"],
        path_parent=paths["trial"],
    )
    pass


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
    print("version check: 4")

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
    # Convert variable types for further analysis.
    table_type = convert_table_variable_types(
        table=source["table_assembly"],
        report=True,
    )
    # Derive alcohol consumption variables.
    bin_consumption_current = organize_current_alcohol_consumption_variables(
        table=table_type,
        report=True,
    )
    bin_consumption_previous = organize_previous_alcohol_consumption_variables(
        table=bin_consumption_current["table_clean"],
        report=True,
    )
    # Organize information for trial GWAS.
    table = organize_trial_phenotypes_covariates(
        table=bin_consumption_previous["table_clean"],
        report=True,
    )


    # Collect information.
    information = dict()
    information["trial"] = dict()
    information["trial"]["table_phenotypes_covariates"] = (
        table
    )
    # Write product information to file.
    write_product(
        paths=paths,
        information=information
    )

    if False:
        # Derive aggregate of AUDIT-C alcohol use questionnaire.
        bin_alcoholism = organize_auditc_questionnaire_alcoholism_variables(
            table=bin_consumption_previous["table_clean"],
            report=True,
        )

        # Temporary charts
        organize_plot_variable_histogram_summary_charts(
            table=bin_alcoholism["table_clean"],
            paths=paths,
        )

        # TODO: 3) organize menopause variable

        # TODO: 3) evaluate person sub-cohorts by variable availability etc

        # Organize general phenotypes.

        # Organize genotype principal components.

        # Organize alcohol phenotypes.

        # Collect information.
        information = dict()
        information["alcohol"] = dict()
        information["alcohol"]["table_report_current"] = (
            bin_consumption_current["table_report"]
        )
        information["alcohol"]["table_report_previous"] = (
            bin_consumption_previous["table_report"]
        )
        information["alcohol"]["table_report_alcoholism"] = (
            bin_alcoholism["table_report"]
        )
        information["assembly"]["table_phenotypes"] = bin_alcoholism["table_clean"]
        # Write product information to file.
        write_product(
            paths=paths,
            information=information
        )


    pass



if (__name__ == "__main__"):
    execute_procedure()
