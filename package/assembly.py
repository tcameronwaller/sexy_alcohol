
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
    paths["assembly"] = os.path.join(path_dock, "assembly")
    paths["raw"] = os.path.join(
        path_dock, "assembly", "raw"
    )
    paths["alcohol"] = os.path.join(
        path_dock, "assembly", "alcohol"
    )
    paths["plot"] = os.path.join(
        path_dock, "assembly", "plot"
    )
    # Remove previous files to avoid version or batch confusion.
    if restore:
        utility.remove_directory(path=paths["assembly"])
    # Initialize directories.
    utility.create_directories(
        path=paths["assembly"]
    )
    utility.create_directories(
        path=paths["raw"]
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


def read_ukbiobank_table_column_names(
    path_file=None,
    delimiter=None,
    start=None,
    stop=None,
):
    """
    Reads and extracts column names from UK Biobank data.

    The UK Biobank ukbconv tool's "txt" option exports to a text file with tab
    delimiters between columns; however, there are some quirks about the
    format.

    arguments:
        path_file (str): path to file of data export from UK Biobank ukbconv
            tool
        delimiter (str): delimiter between columns
        start (int): index of line at which to start reading
        stop (int): index of line at which to stop reading

    raises:

    returns:
        (list<str>): list of column names

    """

    # Read lines for samples with genes' signals.
    lines = utility.read_file_text_lines(
        path_file=path_file,
        start=start,
        stop=stop,
    )
    line = lines[0]
    # Split line's content by delimiter.
    names = line.split(delimiter)
    # Remove excess quotation marks.
    names_simple = list()
    for name in names:
        name = name.replace("\'", "")
        name = name.replace("\"", "")
        names_simple.append(name)
    # Return information.
    return names_simple


def extract_organize_variables_types(
    table_ukbiobank_variables=None,
    columns=None,
    extra_pairs=None,
):
    """
    Organize information about data types of UK Biobank phenotype variables.

    arguments:
        table_ukbiobank_variables (object): Pandas data frame of information
            about UK Biobank phenotype variables
        columns (list<str>): unique names of columns in UK Biobank tables
        extra_pairs (dict<str>): extra key value pairs to include

    raises:

    returns:
        (dict<str>): pairs of variables and data types

    """

    # Copy data.
    table_variables = table_ukbiobank_variables.copy(deep=True)
    # Organize information.
    table_variables = table_variables.loc[
        :, table_variables.columns.isin(["field", "type", "instances_total"])
    ]
    records = utility.convert_dataframe_to_records(data=table_variables)
    # Iterate across records for rows.
    # Collect variables' names and types.
    variables_types = dict()
    variables_types.update(extra_pairs)
    for record in records:
        field = str(record["field"]).strip()
        type = str(record["type"]).strip()
        # Search UK Biobank table columns for matches.
        for column in columns:
            column_field = column.split("-")[0].strip()
            if (field == column_field):
                variables_types[column] = type
                pass
            pass
        pass
    # Return information.
    return variables_types


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
    path_table_ukbiobank_variables = os.path.join(
        path_dock, "access", "table_ukbiobank_phenotype_variables.tsv"
    )
    path_exclusion_identifiers = os.path.join(
        path_dock, "access", "list_exclusion_identifiers.txt"
    )
    path_table_identifier_pairs = os.path.join(
        path_dock, "access", "table_identifier_pairs.csv"
    )
    path_table_ukb_41826 = os.path.join(
        path_dock, "access", "ukb41826.raw.csv"
    )
    path_table_ukb_43878 = os.path.join(
        path_dock, "access", "ukb43878.raw.csv"
    )
    # Read all column names from UK Biobank tables.
    columns = read_ukbiobank_table_column_names(
        path_file=path_table_ukb_41826,
        delimiter=",", # "," or "\t"
        start=0,
        stop=1,
    )
    columns_new = read_ukbiobank_table_column_names(
        path_file=path_table_ukb_43878,
        delimiter=",", # "," or "\t"
        start=0,
        stop=1,
    )
    columns.extend(columns_new)
    columns_unique = utility.collect_unique_elements(
        elements=columns,
    )
    # Report.
    if report:
        utility.print_terminal_partition(level=2)
        print("unique column names: " + str(len(columns_unique)))
        print(columns_unique)
        utility.print_terminal_partition(level=2)
        pass
    # Determine variable types.
    table_ukbiobank_variables = pandas.read_csv(
        path_table_ukbiobank_variables,
        sep="\t",
        header=0,
    )
    variables_types = extract_organize_variables_types(
        table_ukbiobank_variables=table_ukbiobank_variables,
        columns=columns_unique,
        extra_pairs={
            "IID": "string",
            "eid": "string",
        },
    )
    # Report.
    if report:
        utility.print_terminal_partition(level=2)
        print(variables_types["31-0.0"])
        print("20117-0.0: " + str(variables_types["20117-0.0"]))
    # Read information from file.
    exclusion_identifiers = utility.read_file_text_list(
        delimiter="\n",
        path_file=path_exclusion_identifiers
    )
    table_identifier_pairs = pandas.read_csv(
        path_table_identifier_pairs,
        sep=",",
        header=0,
        dtype="string",
    )
    table_ukb_41826 = pandas.read_csv(
        path_table_ukb_41826,
        sep=",", # "," or "\t"
        header=0,
        dtype=variables_types,
        na_values=["<NA>"],
        keep_default_na=True,
    )
    table_ukb_43878 = pandas.read_csv(
        path_table_ukb_43878,
        sep=",", # "," or "\t"
        header=0,
        dtype=variables_types,
        na_values=["<NA>"],
        keep_default_na=True,
    )
    # Compile and return information.
    return {
        "table_ukbiobank_variables": table_ukbiobank_variables,
        "exclusion_identifiers": exclusion_identifiers,
        "table_identifier_pairs": table_identifier_pairs,
        "table_ukb_41826": table_ukb_41826,
        "table_ukb_43878": table_ukb_43878,
    }


##########
# Organization raw


def merge_table_variables_identifiers(
    table_identifier_pairs=None,
    table_ukb_41826=None,
    table_ukb_43878=None,
    report=None,
):
    """
    Reads and organizes source information from file.

    arguments:
        table_identifier_pairs (object): Pandas data frame of associations
            between "IID" and "eid"
        table_ukb_41826 (object): Pandas data frame of variables from UK Biobank
            phenotype accession 41826
        table_ukb_43878 (object): Pandas data frame of variables from UK Biobank
            phenotype accession 43878
        report (bool): whether to print reports

    raises:

    returns:
        (object): Pandas data frame of phenotype variables across UK Biobank
            cohort

    """

    # Report.
    if report:
        utility.print_terminal_partition(level=2)
        print(table_identifier_pairs)
        utility.print_terminal_partition(level=2)
        print(table_ukb_41826)
        utility.print_terminal_partition(level=2)
        print(table_ukb_43878)
    # Organize data.
    table_identifier_pairs.astype("string")
    table_identifier_pairs.set_index(
        "eid",
        drop=True,
        inplace=True,
    )
    table_ukb_41826["eid"].astype("string")
    table_ukb_41826.set_index(
        "eid",
        drop=True,
        inplace=True,
    )
    table_ukb_43878["eid"].astype("string")
    table_ukb_43878.set_index(
        "eid",
        drop=True,
        inplace=True,
    )

    # Merge data tables using database-style join.
    # Alternative is to use DataFrame.join().
    table_merge = table_identifier_pairs.merge(
        table_ukb_41826,
        how="outer",
        left_on="eid",
        right_on="eid",
        suffixes=("_pairs", "_41826"),
    )
    table_merge = table_merge.merge(
        table_ukb_43878,
        how="outer",
        left_on="eid",
        right_on="eid",
        suffixes=("_41826", "_43878"),
    )
    # Remove excess columns.

    # Report.
    if report:
        utility.print_terminal_partition(level=2)
        print(table_merge)
    # Return information.
    return table_merge


def exclude_persons_ukbiobank_consent(
    exclusion_identifiers=None,
    table=None,
    report=None,
):
    """
    Removes entries with specific identifiers from data.

    arguments:
        exclusion_identifiers (list<str>): identifiers of persons who withdrew
            consent from UK Biobank
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
        print("Initial table dimensions: " + str(table.shape))
        utility.print_terminal_partition(level=4)
        print("Exclusion of persons: " + str(len(exclusion_identifiers)))
    # Copy data.
    table = table.copy(deep=True)
    # Filter data entries.
    table_exclusion = table.loc[
        ~table.index.isin(exclusion_identifiers), :
    ]
    # Report.
    if report:
        utility.print_terminal_partition(level=4)
        print("Final data dimensions: " + str(table_exclusion.shape))
    # Return information.
    return table_exclusion


##########
# Organization


def extract_organize_variable_fields_instances_names(
    table_ukbiobank_variables=None,
    extra_names=None,
):
    """
    Organizes column names for variable fields and instances.

    arguments:
        table_ukbiobank_variables (object): Pandas data frame of information
            about UK Biobank phenotype variables
        extra_names (list<str>): extra names to include

    raises:

    returns:
        (list<str>): column names for variable fields and instances

    """

    # Copy data.
    table_variables = table_ukbiobank_variables.copy(deep=True)
    # Organize information.
    table_variables = table_variables.loc[
        :, table_variables.columns.isin(["field", "instances_keep"])
    ]
    records = utility.convert_dataframe_to_records(data=table_variables)
    # Iterate across records for rows.
    # Collect variables' names and types.
    names = list()
    names.extend(extra_names)
    for record in records:
        field = str(record["field"])
        instances_total_raw = str(record["instances_keep"])
        instances_raw = instances_total_raw.split(",")
        for instance_raw in instances_raw:
            instance = str(instance_raw).strip()
            if len(instance) > 0:
                name = str(field + "-" + instance)
                # Create entry for variable's name and type.
                names.append(name)
                pass
            pass
        pass
    # Return information.
    return names


def remove_table_irrelevant_variable_instances_entries(
    table_ukbiobank_variables=None,
    table_ukb_41826=None,
    table_ukb_43878=None,
    report=None,
):
    """
    Removes irrelevant columns and rows from data.

    arguments:
        table_ukbiobank_variables (object): Pandas data frame of information
            about UK Biobank phenotype variables
        table_ukb_41826 (object): Pandas data frame of variables from UK Biobank
            phenotype accession 41826
        table_ukb_43878 (object): Pandas data frame of variables from UK Biobank
            phenotype accession 43878
        report (bool): whether to print reports

    raises:

    returns:
        (dict<object>): collection of Pandas data frames after removal of
            irrelevant columns and rows

    """

    # Report.
    if report:
        utility.print_terminal_partition(level=2)
        print("...before pruning...")
        print("table_ukb_41826 shape: " + str(table_ukb_41826.shape))
        utility.print_terminal_partition(level=4)
        print("table_ukb_43878 shape: " + str(table_ukb_43878.shape))

    # Extract names of columns for relevant variable fields and instances.
    column_names = extract_organize_variable_fields_instances_names(
        table_ukbiobank_variables=table_ukbiobank_variables,
        extra_names=["IID", "eid"],
    )
    print(column_names)
    # Remove all irrelevant columns.
    table_ukb_41826 = table_ukb_41826.loc[
        :, table_ukb_41826.columns.isin(column_names)
    ]
    table_ukb_43878 = table_ukb_43878.loc[
        :, table_ukb_43878.columns.isin(column_names)
    ]
    # Remove rows with all missing values.
    table_ukb_41826.dropna(
        axis="index",
        how="all",
        inplace=True,
    )
    table_ukb_41826.dropna(
        axis="index",
        how="any",
        subset=["eid"],
        inplace=True,
    )
    table_ukb_43878.dropna(
        axis="index",
        how="all",
        inplace=True,
    )
    table_ukb_43878.dropna(
        axis="index",
        how="any",
        subset=["eid"],
        inplace=True,
    )
    # Report.
    if report:
        utility.print_terminal_partition(level=2)
        print("...after pruning...")
        print("table_ukb_41826 shape: " + str(table_ukb_41826.shape))
        utility.print_terminal_partition(level=4)
        print("table_ukb_43878 shape: " + str(table_ukb_43878.shape))

    # Compile and return information.
    bucket = dict()
    bucket["table_ukb_41826"] = table_ukb_41826
    bucket["table_ukb_43878"] = table_ukb_43878
    return bucket


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



def write_product_raw(
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

    # Specify directories and files.
    path_table_ukb_41826 = os.path.join(
        paths["raw"], "table_ukb_41826.tsv"
    )
    path_table_ukb_43878 = os.path.join(
        paths["raw"], "table_ukb_43878.tsv"
    )
    path_table_merge_exclusion = os.path.join(
        paths["raw"], "table_merge_exclusion.tsv"
    )
    # Write information to file.
    if False:
        information["table_ukb_41826"].to_csv(
            path_or_buf=path_table_ukb_41826,
            sep="\t",
            header=True,
            index=True,
        )
        information["table_ukb_43878"].to_csv(
            path_or_buf=path_table_ukb_43878,
            sep="\t",
            header=True,
            index=True,
        )
    information["table_merge_exclusion"].to_csv(
        path_or_buf=path_table_merge_exclusion,
        sep="\t",
        header=True,
        index=True,
    )
    pass


def write_product_alcohol(
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
    path_table_report_current = os.path.join(
        path_parent, "table_report_current.tsv"
    )
    path_table_report_previous = os.path.join(
        path_parent, "table_report_previous.tsv"
    )
    path_table_report_alcoholism = os.path.join(
        path_parent, "table_report_alcoholism.tsv"
    )
    # Write information to file.
    information["table_report_current"].to_csv(
        path_or_buf=path_table_report_current,
        sep="\t",
        header=True,
        index=True,
    )
    information["table_report_previous"].to_csv(
        path_or_buf=path_table_report_previous,
        sep="\t",
        header=True,
        index=True,
    )
    if False:
        information["table_report_alcoholism"].to_csv(
            path_or_buf=path_table_report_alcoholism,
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

    # Alcohol consumption.
    write_product_alcohol(
        information=information["alcohol"],
        path_parent=paths["alcohol"],
    )

    # Specify directories and files.
    path_table_phenotypes = os.path.join(
        paths["assembly"], "table_phenotypes.tsv"
    )
    # Write information to file.
    information["table_phenotypes"].to_csv(
        path_or_buf=path_table_phenotypes,
        sep="\t",
        header=True,
        index=True,
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
    print("version check: 3")

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
    # Merge tables.
    table_merge = merge_table_variables_identifiers(
        table_identifier_pairs=source["table_identifier_pairs"],
        table_ukb_41826=source["table_ukb_41826"],
        table_ukb_43878=source["table_ukb_43878"],
        report=True,
    )
    # Exclude persons who withdrew consent from the UK Biobank.
    table_exclusion = exclude_persons_ukbiobank_consent(
        exclusion_identifiers=source["exclusion_identifiers"],
        table=table_merge,
        report=True,
    )
    if True:
        # Write out raw tables for inspection.
        # Collect information.
        information = dict()
        information["table_ukb_41826"] = source["table_ukb_41826"]
        information["table_ukb_43878"] = source["table_ukb_43878"]
        information["table_merge_exclusion"] = table_exclusion
        # Write product information to file.
        write_product_raw(
            paths=paths,
            information=information
        )

    if False:
        # Remove data columns for irrelevant variable instances.
        prune = remove_table_irrelevant_variable_instances_entries(
            table_ukbiobank_variables=source["table_ukbiobank_variables"],
            table_ukb_41826=source["table_ukb_41826"],
            table_ukb_43878=source["table_ukb_43878"],
            report=True,
        )
        # Convert variable types for further analysis.
        table_type = convert_table_variable_types(
            table=table_exclusion,
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
