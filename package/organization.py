
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


def initialize_directories_cohorts(
    path_parent=None,
):
    """
    Initialize directories for procedure's product files.

    arguments:
        path_parent (str): path to parent directory

    raises:

    returns:
        (dict<str>): collection of paths to directories for procedure's files

    """

    # Collect information.
    paths = dict()

    sexes = ["female", "male",]
    alcoholisms = [
        "alcoholism_1", "alcoholism_2", "alcoholism_3", "alcoholism_4",
    ]
    hormones = ["oestradiol", "testosterone",]
    for sex in sexes:
        paths[sex] = dict()
        for alcoholism in alcoholisms:
            paths[sex][alcoholism] = dict()
            for hormone in hormones:
                paths[sex][alcoholism][hormone] = os.path.join(
                    path_parent, "cohorts", sex, alcoholism, hormone
                )
                # Initialize directories.
                utility.create_directories(
                    path=paths[sex][alcoholism][hormone]
                )
                pass
            pass
        pass
    # Return information.
    return paths


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
    paths["quality"] = os.path.join(
        path_dock, "organization", "quality"
    )
    # Remove previous files to avoid version or batch confusion.
    if restore:
        utility.remove_directory(path=paths["organization"])
    # Initialize directories.
    utility.create_directories(
        path=paths["organization"]
    )
    utility.create_directories(
        path=paths["quality"]
    )

    # Directory tiers.
    paths["cohorts"] = initialize_directories_cohorts(
        path_parent=paths["organization"],
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
    path_table_ukb_samples = os.path.join(
        path_dock, "access", "ukb46237_imp_chr21_v3_s487320.sample"
    )
    # Read information from file.
    table_assembly = pandas.read_pickle(
        path_table_assembly
    )
    table_ukb_samples = pandas.read_csv(
        path_table_ukb_samples,
        sep="\s+",
        header=0,
        dtype="string",
    )
    # Compile and return information.
    return {
        "table_assembly": table_assembly,
        "table_ukb_samples": table_ukb_samples,
    }


##########
# Sex hormones


def determine_sex_text(
    sex=None,
):
    """
    Translate information from UK Biobank about whether person
    never consumes any alcohol.

    Accommodate inexact float values.

    arguments:
        sex (float): person's sex, UK Biobank field 31

    raises:

    returns:
        (str): text representation of person's sex

    """

    # Determine whether the variable has a valid (non-missing) value.
    if (
        (not pandas.isna(sex)) and
        (-0.5 <= sex and sex < 1.5)
    ):
        # The variable has a valid value.
        if (-0.5 <= sex and sex < 0.5):
            # "female"
            sex_text = "female"
        elif (0.5 <= sex and sex < 1.5):
            # "male"
            sex_text = "male"
    else:
        # null
        sex_text = float("nan")
    # Return information.
    return sex_text


def organize_general_attribute_variables(
    table=None,
    report=None,
):
    """
    Organizes information about general attributes.

    arguments:
        table (object): Pandas data frame of phenotype variables across UK
            Biobank cohort
        report (bool): whether to print reports

    raises:

    returns:
        (dict): collection of information about phenotype variables

    """

    # Copy data.
    table = table.copy(deep=True)
    # Translate column names.
    translations = dict()
    #translations["31-0.0"] = "sex"
    # Use genotypic sex to avoid data entry errors or confusion with gender.
    translations["22001-0.0"] = "sex"
    translations["21022-0.0"] = "age"
    translations["21001-0.0"] = "body_mass_index"
    table.rename(
        columns=translations,
        inplace=True,
    )
    # Convert variable types.
    columns_type = [
        "sex", "age", "body_mass_index"
    ]
    table_type = convert_table_columns_variables_types_float(
        columns=columns_type,
        table=table,
    )
    # Determine text representation of person's sex.
    table["sex_text"] = table.apply(
        lambda row:
            determine_sex_text(
                sex=row["sex"],
            ),
        axis="columns", # apply across rows
    )
    # Report.
    if report:
        # Column name translations.
        utility.print_terminal_partition(level=2)
        print("translations of general attribute column names...")
        for old in translations.keys():
            print("   " + old + ": " + translations[old])
        utility.print_terminal_partition(level=3)
        # Organize data for report.
        table_report = table.copy(deep=True)
        table_report = table_report.loc[
            :, table_report.columns.isin([
                "eid", "IID",
                "sex", "sex_text", "age", "body_mass_index",
            ])
        ]
        utility.print_terminal_partition(level=2)
        print("Translation of columns for general attributes: ")
        print(table_report)
        utility.print_terminal_partition(level=3)
        # Variable types.
        utility.print_terminal_partition(level=2)
        print("After type conversion")
        print(table_report.dtypes)
        utility.print_terminal_partition(level=3)
    # Return information.
    return table


##########
# Genotype


def match_column_field(
    column=None,
    field=None,
):
    """
    Determine whether a column represents an original instance of a field.

    arguments:
        column (str): name of column
        field (str): identifier of field for which to collect columns

    raises:

    returns:
        (bool): whether column name matches field

    """

    # Determine whether column matches format of an original field instance.
    if ("-" in str(column)):
        # Column is an original instance of the field.
        # Only original instance columns have the "-" delimiter.
        column_field = str(column).split("-")[0].strip()
        if (str(column_field) == str(field)):
            match = True
        else:
            match = False
    else:
        match = False
    # Return information.
    return match


def collect_sort_table_field_instance_columns(
    field=None,
    table=None,
    report=None,
):
    """
    Collects names of columns that represent instances of a specific field.

    arguments:
        field (str): identifier of field for which to collect columns
        table (object): Pandas data frame of phenotype variables across UK
            Biobank cohort
        report (bool): whether to print reports

    raises:

    returns:
        (list<str>): names of columns

    """

    # Extract table columns.
    columns = copy.deepcopy(table.columns.to_list())
    # Collect columns that represent instances of the field.
    columns_field = list(filter(
        lambda column: match_column_field(column=column, field=field),
        columns
    ))
    # Sort columns.
    # Be careful to sort by the integer value of the instance.
    #columns_sort = sorted(columns_field, reverse=False)
    columns_instance = list()
    for column in columns_field:
        column_instance = str(column).split("-")[1].strip()
        columns_instance.append(column_instance)
    columns_integer = list()
    for column in columns_instance:
        column_integer = str(column).split(".")[1].strip()
        columns_integer.append(int(column_integer))
    table_columns = pandas.DataFrame(
        data={
            "column_name": columns_field,
            "column_instance": columns_instance,
            "column_integer": columns_integer,
        }
    )
    # Sort table rows.
    table_columns.sort_values(
        by=["column_integer"],
        axis="index",
        ascending=True,
        inplace=True,
    )
    columns_sort = table_columns["column_name"].to_list()
    # Report.
    if report:
        utility.print_terminal_partition(level=2)
        print("Sorted column names")
        print(table_columns)
    # Return information.
    return columns_sort


def translate_column_field_instance_names(
    columns=None,
    prefix=None,
    base=None,
):
    """
    Translates names of columns.

    arguments:
        columns (list<str>): names of columns for field instances
        prefix (str): prefix for translations of column names
        base (int): initial integer for index

    raises:

    returns:
        (list<str>): names of columns

    """

    index = base
    translations = dict()
    for column in columns:
        translations[str(column)] = str(prefix + str(index))
        index += 1
    return translations


def convert_table_columns_variables_types_float(
    columns=None,
    table=None,
):
    """
    Converts data variable types.

    arguments:
        columns (list<str>): names of columns
        table (object): Pandas data frame of phenotype variables across UK
            Biobank cohort

    raises:

    returns:
        (object): Pandas data frame of phenotype variables across UK Biobank
            cohort

    """

    # Copy data.
    table = table.copy(deep=True)
    # Convert data variable types.
    for column in columns:
        table[column] = pandas.to_numeric(
            table[column],
            errors="coerce", # force any invalid values to missing or null
            downcast="float",
        )
    # Return information.
    return table


def convert_table_prefix_columns_variables_types_float(
    prefix=None,
    table=None,
):
    """
    Converts data variable types.

    The UK Biobank encodes several nominal variables with integers. Missing
    values for these variables necessitates some attention to type conversion
    from string to float for analysis.

    arguments:
        prefix (str): prefix for translations of column names
        table (object): Pandas data frame of phenotype variables across UK
            Biobank cohort

    raises:

    returns:
        (object): Pandas data frame of phenotype variables across UK Biobank
            cohort

    """

    # Copy data.
    table = table.copy(deep=True)
    # Determine which columns to convert.
    columns = table.columns.to_list()
    columns_match = list(filter(
        lambda column: (str(prefix) in str(column)),
        columns
    ))
    # Convert data variable types.
    table_type = convert_table_columns_variables_types_float(
        columns=columns_match,
        table=table,
    )
    # Return information.
    return table_type


def organize_genotype_principal_component_variables(
    table=None,
    report=None,
):
    """
    Organizes information about principal components on genotypes.

    arguments:
        table (object): Pandas data frame of phenotype variables across UK
            Biobank cohort
        report (bool): whether to print reports

    raises:

    returns:
        (dict): collection of information about phenotype variables

    """

    # Copy data.
    table = table.copy(deep=True)
    # Extract columns for genotype principal components.
    columns = collect_sort_table_field_instance_columns(
        field="22009",
        table=table,
        report=report,
    )
    # Translate column names.
    translations = translate_column_field_instance_names(
        columns=columns,
        prefix="genotype_pc_",
        base=1,
    )
    table.rename(
        columns=translations,
        inplace=True,
    )
    # Convert variable types.
    table = convert_table_prefix_columns_variables_types_float(
        prefix="genotype_pc_",
        table=table,
    )
    # Report.
    if report:
        # Column name translations.
        utility.print_terminal_partition(level=2)
        print("translations of genotype PC column names...")
        for old in translations.keys():
            print("   " + old + ": " + translations[old])
        utility.print_terminal_partition(level=3)
        # Column names and values.
        table_report = table.loc[
            :, table.columns.str.startswith("genotype_pc_")
        ]
        utility.print_terminal_partition(level=2)
        print("Translation of columns for genotype principal components: ")
        print(table_report)
        utility.print_terminal_partition(level=3)
        # Variable types.
        utility.print_terminal_partition(level=2)
        print("After type conversion")
        print(table_report.dtypes)
        utility.print_terminal_partition(level=3)
    # Return information.
    return table


##########
# Sex hormones


def organize_sex_hormone_variables(
    table=None,
    report=None,
):
    """
    Organizes information about sex hormones.

    arguments:
        table (object): Pandas data frame of phenotype variables across UK
            Biobank cohort
        report (bool): whether to print reports

    raises:

    returns:
        (dict): collection of information about phenotype variables

    """

    # Copy data.
    table = table.copy(deep=True)
    # Translate column names.
    translations = dict()
    translations["30600-0.0"] = "albumin"
    translations["30830-0.0"] = "steroid_globulin"
    translations["30850-0.0"] = "testosterone"
    translations["30800-0.0"] = "oestradiol"
    table.rename(
        columns=translations,
        inplace=True,
    )
    # Convert variable types.
    columns_hormones = [
        "albumin", "steroid_globulin", "testosterone", "oestradiol"
    ]
    table_type = convert_table_columns_variables_types_float(
        columns=columns_hormones,
        table=table,
    )
    # Report.
    if report:
        # Column name translations.
        utility.print_terminal_partition(level=2)
        print("translations of hormone column names...")
        for old in translations.keys():
            print("   " + old + ": " + translations[old])
        utility.print_terminal_partition(level=3)
        # Column names and values.
        table_report = table.loc[
            :, table.columns.isin(columns_hormones)
        ]
        utility.print_terminal_partition(level=2)
        print("Translation of columns for hormones: ")
        print(table_report)
        utility.print_terminal_partition(level=3)
        # Variable types.
        utility.print_terminal_partition(level=2)
        print("After type conversion")
        print(table_report.dtypes)
        utility.print_terminal_partition(level=3)
    # Return information.
    return table


##########
# Alcohol consumption


def determine_alcohol_consumption_frequency(
    frequency=None,
):
    """
    Translate information from UK Biobank about whether person
    never consumes any alcohol.

    Accommodate inexact float values.

    arguments:
        frequency (float): frequency of alcohol consumption, UK Biobank field
            1558

    raises:

    returns:
        (float): ordinal representation of person's frequency of alcohol
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
        # "prefer not to answer" or null
        alcohol_frequency = float("nan")
    # Return information.
    return alcohol_frequency


def determine_current_alcohol_consumption(
    consumer=None,
    alcohol_frequency=None,
):
    """
    Translate information from UK Biobank about whether person consumes alcohol
    currently.

    Accommodate inexact float values.

    arguments:
        consumer (float): status of alcohol consumption, UK Biobank field
            20117
        alcohol_frequency (float): ordinal representation of person's frequency
            of alcohol consumption, derivation of UK Biobank field 1558

    raises:

    returns:
        (float): binary representation of whether person consumes alcohol
            currently

    """

    # Interpret consumer status.
    if (
        (not pandas.isna(consumer)) and
        (-0.5 <= consumer and consumer < 2.5)
    ):
        # The variable has a valid value.
        if (1.5 <= consumer and consumer < 2.5):
            # "current"
            consumer_boolean = True
        else:
            # "never", or "previous"
            consumer_boolean = False
    else:
        # "prefer not to answer" or null
        consumer_boolean = float("nan")
    # Interpret consumption frequency.
    if (not math.isnan(alcohol_frequency)):
        # The variable has a valid value.
        if (0.5 <= alcohol_frequency and alcohol_frequency < 5.5):
            # The person consumes alcohol currently.
            frequency_boolean = True
        else:
            frequency_boolean = False
    else:
        frequency_boolean = float("nan")
    # Integrate information from multiple variables.
    if (
        (not math.isnan(consumer_boolean)) or
        (not math.isnan(frequency_boolean))
    ):
        if (consumer_boolean or frequency_boolean):
            alcohol_current = 1
        else:
            alcohol_current = 0
    else:
        alcohol_current = float("nan")
    # Return information.
    return alcohol_current


def determine_previous_alcohol_consumption(
    consumer=None,
    former=None,
    comparison=None,
    alcohol_current=None,
):
    """
    Translate information from UK Biobank about whether person
    never consumes any alcohol.

    Accommodate inexact float values.

    arguments:
        consumer (float): status of alcohol consumption, UK Biobank field
            20117
        former (float): former alcohol consumption, UK Biobank field
            3731
        comparison (float): comparison to previous alcohol consumption, UK
            Biobank field 1628
        alcohol_current (float): binary representation of whether person
            consumes alcohol currently

    raises:

    returns:
        (float): binary representation of whether person consumed alcohol
            previously

    """

    # Interpret consumer.
    if (
        (not pandas.isna(consumer)) and
        (-0.5 <= consumer and consumer < 2.5)
    ):
        # The variable has a valid value.
        if (0.5 <= consumer and consumer < 2.5):
            # "current" or "previous"
            consumer_boolean = True
        else:
            # "never"
            consumer_boolean = False
    else:
        # "prefer not to answer" or null
        consumer_boolean = float("nan")
    # Interpret former.
    if (
        (not pandas.isna(former)) and
        (-0.5 <= former and former < 1.5)
    ):
        # The variable has a valid value.
        if (0.5 <= former and former < 1.5):
            # "yes"
            former_boolean = True
        else:
            # "no"
            former_boolean = False
    else:
        # "prefer not to answer" or null
        former_boolean = float("nan")
    # Interpret comparison.
    if (
        (not pandas.isna(comparison)) and
        (-0.5 <= former and former < 3.5)
    ):
        # "less nowadays", "about the same", or "more nowadays"
        comparison_boolean = True
    else:
        # "do not know", "prefer not to answer", or null
        comparison_boolean = float("nan")
    # Interpret alcohol current.
    if (not math.isnan(alcohol_current)):
        # The variable has a valid value.
        if (0.5 <= alcohol_current and alcohol_current < 1.5):
            # The person consumes alcohol currently.
            alcohol_current_boolean = True
        else:
            alcohol_current_boolean = False
    else:
        alcohol_current_boolean = float("nan")
    # Integrate information from multiple variables.
    if (
        (not math.isnan(consumer_boolean)) or
        (not math.isnan(former_boolean)) or
        (not math.isnan(comparison_boolean)) or
        (not math.isnan(alcohol_current_boolean))
    ):
        if (
            consumer_boolean or
            former_boolean or
            comparison_boolean or
            alcohol_current_boolean
        ):
            alcohol_previous = 1
        else:
            alcohol_previous = 0
    else:
        alcohol_previous = float("nan")
    # Return information.
    return alcohol_previous


def determine_alcohol_none(
    alcohol_frequency=None,
    alcohol_current=None,
    alcohol_previous=None,
):
    """
    Translate information from UK Biobank about whether person
    never consumes any alcohol.

    Accommodate inexact float values.

    arguments:
        alcohol_frequency (float): ordinal representation of person's frequency
            of alcohol consumption, derivation of UK Biobank field 1558
        alcohol_current (float): binary representation of whether person
            consumes alcohol currently
        alcohol_previous (float): binary representation of whether person
            consumed alcohol previously

    raises:

    returns:
        (bool): whether person never consumes any alcohol

    """

    # Interpret consumption frequency.
    if (not math.isnan(alcohol_frequency)):
        # The variable has a valid value.
        if (-0.5 <= alcohol_frequency and alcohol_frequency < 0.5):
            # The person never consumes alcohol currently.
            frequency_boolean = True
        else:
            frequency_boolean = False
    else:
        frequency_boolean = float("nan")
    # Interpret current consumption.
    if (not math.isnan(alcohol_current)):
        # The variable has a valid value.
        if (-0.5 <= alcohol_current and alcohol_current < 0.5):
            # The person never consumes alcohol currently.
            current_boolean = True
        else:
            current_boolean = False
    else:
        current_boolean = float("nan")
    # Interpret previous consumption.
    if (not math.isnan(alcohol_previous)):
        # The variable has a valid value.
        if (-0.5 <= alcohol_previous and alcohol_previous < 0.5):
            # The person never consumed alcohol previously.
            previous_boolean = True
        else:
            previous_boolean = False
    else:
        previous_boolean = float("nan")
    # Integrate information from multiple variables.
    if (
        (not math.isnan(frequency_boolean)) and
        (not math.isnan(current_boolean)) and
        (not math.isnan(previous_boolean))
    ):
        if (
            frequency_boolean and
            current_boolean and
            previous_boolean
        ):
            # Person has never consumed alcohol, previously or currently.
            alcohol_none = 1
        else:
            # Person has consumed alcohol.
            alcohol_none = 0
    else:
        alcohol_none = float("nan")
    # Return information.
    return alcohol_none


def organize_alcohol_consumption_frequency_variables(
    table=None,
    report=None,
):
    """
    Organizes information about previous and current alcohol consumption.

    "frequency", field 1558: "Alcohol intake frequency"
    UK Biobank data coding 100402 for variable field 1558.
    "daily or almost daily": 1
    "three or four times a week": 2
    "once or twice a week": 3
    "one to three times a month": 4
    "special occasions only": 5
    "never": 6
    "prefer not to answer": -3

    "former", field 3731: "Former alcohol drinker"
    Variable 3731 was only collected for persons who never consume any alcohol
    currently (UK Biobank variable 1558).
    UK Biobank data coding 100352 for variable field 3731.
    "yes": 1
    "no": 0
    "prefer not to answer": -3

    "consumer", field 20117: "Alcohol drinker status"
    Variable 20117 is a derivation of variables 1558 and 3731.
    UK Biobank data coding 90 for variable field 20117.
    "current": 2
    "previous": 1
    "never": 0
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
    # Convert variable types.
    columns_type = [
        "1558-0.0", "3731-0.0", "1628-0.0", "20117-0.0",
    ]
    table = convert_table_columns_variables_types_float(
        columns=columns_type,
        table=table,
    )
    # Determine person's frequency of alcohol consumption.
    table["alcohol_frequency"] = table.apply(
        lambda row:
            determine_alcohol_consumption_frequency(
                frequency=row["1558-0.0"],
            ),
        axis="columns", # apply across rows
    )
    # Determine whether person consumes alcohol currently.
    table["alcohol_current"] = table.apply(
        lambda row:
            determine_current_alcohol_consumption(
                consumer=row["20117-0.0"],
                alcohol_frequency=row["alcohol_frequency"],
            ),
        axis="columns", # apply across rows
    )
    # Determine whether person never consumes any alcohol.
    table["alcohol_previous"] = table.apply(
        lambda row:
            determine_previous_alcohol_consumption(
                consumer=row["20117-0.0"],
                former=row["3731-0.0"],
                comparison=row["1628-0.0"],
                alcohol_current=row["alcohol_current"],
            ),
        axis="columns", # apply across rows
    )
    # Determine whether person never consumes any alcohol, either currently or
    # previously.
    table["alcohol_none"] = table.apply(
        lambda row:
            determine_alcohol_none(
                alcohol_frequency=row["alcohol_frequency"],
                alcohol_current=row["alcohol_current"],
                alcohol_previous=row["alcohol_previous"]
            ),
        axis="columns", # apply across rows
    )
    # Remove columns for variables that are not necessary anymore.
    table_clean = table.copy(deep=True)
    table_clean.drop(
        labels=["1558-0.0", "3731-0.0", "1628-0.0", "20117-0.0",],
        axis="columns",
        inplace=True
    )
    # Organize data for report.
    table_report = table.copy(deep=True)
    table_report = table_report.loc[
        :, table_report.columns.isin([
            "eid", "IID",
            "1558-0.0", "3731-0.0", "1628-0.0", "20117-0.0",
            "alcohol_frequency",
            "alcohol_previous",
            "alcohol_current",
            "alcohol_none",
        ])
    ]
    # Report.
    if report:
        utility.print_terminal_partition(level=2)
        print("Summary of alcohol consumption variables: ")
        print(table_report)
    # Collect information.
    pail = dict()
    pail["table"] = table
    pail["table_clean"] = table_clean
    pail["table_report"] = table_report
    # Return information.
    return pail


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

    arguments:
        beer_cider (int): count of drinks by type
        wine_red (int): count of drinks by type
        wine_white (int): count of drinks by type
        port (int): count of drinks by type
        liquor (int): count of drinks by type
        other (int): count of drinks by type

    raises:

    returns:
        (int): sum of counts of drinks

    """

    # Consider all types of alcoholic beverage.
    types = [beer_cider, wine_red, wine_white, port, liquor, other]
    # Determine whether any relevant variables have missing values.
    valid = False
    for type in types:
        if (not pandas.isna(type) and (type > -0.5)):
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
    alcohol_current=None,
    drinks_weekly=None,
    drinks_monthly=None,
    weeks_per_month=None,
):
    """
    Calculate monthly alcohol consumption in drinks.

    Accommodate inexact float values.

    arguments:
        alcohol_current (float): binary representation of whether person
            consumes alcohol currently
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
    # Consider current alcohol consumption.
    if (
        (not math.isnan(alcohol_current)) and
        (-0.5 <= alcohol_current and alcohol_current < 0.5)
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


def organize_alcohol_consumption_quantity_variables(
    table=None,
    report=None,
):
    """
    Organizes information about alcohol consumption in standard drinks monthly.

    UK Biobank data coding 100291.
    "do not know": -1
    "prefer not to answer": -3

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
    # Convert variable types.
    columns_type = [
        "1588-0.0", "1568-0.0", "1578-0.0", "1608-0.0", "1598-0.0", "5364-0.0",
        "4429-0.0", "4407-0.0", "4418-0.0", "4451-0.0", "4440-0.0", "4462-0.0",
    ]
    table = convert_table_columns_variables_types_float(
        columns=columns_type,
        table=table,
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
                alcohol_current=row["alcohol_current"],
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
            "1588-0.0", "1568-0.0", "1578-0.0", "1608-0.0", "1598-0.0",
            "5364-0.0",
            "4429-0.0", "4407-0.0", "4418-0.0", "4451-0.0", "4440-0.0",
            "4462-0.0",
            "drinks_weekly",
            "drinks_monthly",
            "alcohol_drinks_monthly",
            "alcohol_current",
        ])
    ]
    # Report.
    if report:
        utility.print_terminal_partition(level=2)
        print("Summary of alcohol consumption quantity variables: ")
        print(table_report)
    # Collect information.
    pail = dict()
    pail["table"] = table
    pail["table_clean"] = table_clean
    pail["table_report"] = table_report
    # Return information.
    return pail


def organize_alcohol_consumption_variables(
    table=None,
    report=None,
):
    """
    Organizes information about previous and current alcohol consumption.

    arguments:
        table (object): Pandas data frame of phenotype variables across UK
            Biobank cohort
        report (bool): whether to print reports

    raises:

    returns:
        (dict): collection of information about phenotype variables

    """

    # Organize information about alcohol consumption and frequency.
    pail_consumption = organize_alcohol_consumption_frequency_variables(
        table=table,
        report=report,
    )
    # Organize information about current alcohol consumption quantity.
    pail_quantity = organize_alcohol_consumption_quantity_variables(
        table=pail_consumption["table_clean"],
        report=report,
    )
    # Collect information.
    pail = dict()
    pail["consumption"] = pail_consumption
    pail["quantity"] = pail_quantity
    # Return information.
    return pail


##########
# Alcohol AUDIT questionnaire


def interpret_alcohol_auditc_one(
    value=None,
):
    """
    Intepret UK Biobank's coding for AUDIT-C questionnaire question 1.

    "audit_1", field "20414": "Frequency of drinking alcohol"
    UK Biobank data coding "521" for variable field "20414".
    "never": 0
    "monthly or less": 1
    "two to four times a month": 2
    "two to three times a week": 3
    "four or more times a week": 4
    "prefer not to answer": -818

    Accommodate inexact float values.

    arguments:
        value (float): raw value from UK Biobank's coding

    raises:

    returns:
        (float): interpretation value

    """

    # Determine whether the variable has a valid (non-missing) value.
    if (
        (not pandas.isna(value)) and
        (-0.5 <= value and value < 4.5)
    ):
        # The variable has a valid value.
        if (-0.5 <= value and value < 0.5):
            # "never"
            value_clean = 0
        elif (0.5 <= value and value < 1.5):
            # "monthly or less"
            value_clean = 1
        elif (1.5 <= value and value < 2.5):
            # "two to four times a month"
            value_clean = 2
        elif (2.5 <= value and value < 3.5):
            # "two to three times a week"
            value_clean = 3
        elif (3.5 <= value and value < 4.5):
            # "four or more times a week"
            value_clean = 4
    else:
        # "prefer not to answer" or null
        value_clean = float("nan")
    # Return information.
    return value_clean


def interpret_alcohol_audit_two_to_eight(
    value=None,
):
    """
    Intepret UK Biobank's coding for AUDIT questionnaire questions 2 to 8.

    UK Biobank data coding "522" for variable field "20403".
    "one or two": 1
    "three or four": 2
    "five or six": 3
    "seven, eight, or nine": 4
    "ten or more": 5
    "prefer not to answer": -818

    UK Biobank data coding "523" for variable fields "20416", "20413", "20407",
    "20412", "20409", and "20408".
    "never": 1
    "less than monthly": 2
    "monthly": 3
    "weekly": 4
    "daily or almost daily": 5
    "prefer not to answer": -818

    Notice that UK Biobank encodes these variables from 1 to 5; however, AUDIT
    encodes these from 0 to 4. Adjust the values accordingly.

    Accommodate inexact float values.

    arguments:
        value (float): raw value from UK Biobank's coding

    raises:

    returns:
        (float): interpretation value

    """

    # Determine whether the variable has a valid (non-missing) value.
    if (
        (not pandas.isna(value)) and
        (0.5 <= value and value < 5.5)
    ):
        # The variable has a valid value.
        if (0.5 <= value and value < 1.5):
            # code "522": "one or two"
            # code "523": "never"
            value_clean = 0
        elif (1.5 <= value and value < 2.5):
            # code "522": "three or four"
            # code "523": "less than monthly"
            value_clean = 1
        elif (2.5 <= value and value < 3.5):
            # code "522": "five or six"
            # code "523": "monthly"
            value_clean = 2
        elif (3.5 <= value and value < 4.5):
            # code "522": "seven, eight, or nine"
            # code "523": "weekly"
            value_clean = 3
        elif (4.5 <= value and value < 5.5):
            # code "522": "ten or more"
            # code "523": "daily or almost daily"
            value_clean = 4
    else:
        # "prefer not to answer" or null
        value_clean = float("nan")
    # Return information.
    return value_clean


def interpret_alcohol_audit_nine_ten(
    value=None,
):
    """
    Intepret UK Biobank's coding for AUDIT questionnaire questions 9 and 10.

    UK Biobank data coding "524" for variable fields "20411", and "20405".
    "no": 0
    "yes, but not in the last year": 1
    "yes, during the last year": 2
    "prefer not to answer": -818

    Notice that UK Biobank encodes these variables as 0, 1, or 2; however,
    AUDIT encodes these as 0, 2, or 4. Adjust the values accordingly.

    Accommodate inexact float values.

    arguments:
        value (float): raw value from UK Biobank's coding

    raises:

    returns:
        (float): interpretation value

    """

    # Determine whether the variable has a valid (non-missing) value.
    if (
        (not pandas.isna(value)) and
        (-0.5 <= value and value < 2.5)
    ):
        # The variable has a valid value.
        if (-0.5 <= value and value < 0.5):
            # code "524": "no"
            value_clean = 0
        elif (0.5 <= value and value < 1.5):
            # code "524": "yes, but not in the last year"
            value_clean = 2
        elif (1.5 <= value and value < 2.5):
            # code "524": "yes, during the last year"
            value_clean = 4
    else:
        # "prefer not to answer" or null
        value_clean = float("nan")
    # Return information.
    return value_clean


def determine_alcohol_auditc_score(
    audit_1=None,
    audit_2=None,
    audit_3=None,
):
    """
    Determine a person's score from the AUDIT-C questionnaire.

    Accommodate inexact float values.

    arguments:
        audit_1 (float): AUDIT questionnaire question 1, UK Biobank field
            20414
        audit_2 (float): AUDIT questionnaire question 2, UK Biobank field
            20403
        audit_3 (float): AUDIT questionnaire question 3, UK
            Biobank field 20416

    raises:

    returns:
        (float): combination score for AUDIT-C questionnaire

    """

    # Interpret raw variables.
    audit_1_clean = interpret_alcohol_auditc_one(
        value=audit_1,
    )
    audit_2_clean = interpret_alcohol_audit_two_to_eight(
        value=audit_2,
    )
    audit_3_clean = interpret_alcohol_audit_two_to_eight(
        value=audit_3,
    )
    # Integrate information from multiple variables.
    if (
        (not math.isnan(audit_1_clean)) and
        (not math.isnan(audit_2_clean)) and
        (not math.isnan(audit_3_clean))
    ):
        auditc_score = (audit_1_clean + audit_2_clean + audit_3_clean)
    else:
        auditc_score = float("nan")
    # Return information.
    return auditc_score


def organize_alcohol_auditc_variables(
    table=None,
    report=None,
):
    """
    Organizes information about alcohol AUDIT-C questionnaire.

    "audit_1", field "20414": "Frequency of drinking alcohol"
    UK Biobank data coding "521" for variable field "20414".
    "never": 0
    "monthly or less": 1
    "two to four times a month": 2
    "two to three times a week": 3
    "four or more times a week": 4
    "prefer not to answer": -818

    "audit_2", field "20403": "Amount of alcohol drunk on a typical drinking
    day"
    UK Biobank data coding "522" for variable field "20403".
    "one or two": 1
    "three or four": 2
    "five or six": 3
    "seven, eight, or nine": 4
    "ten or more": 5
    "prefer not to answer": -818

    "audit_3", field "20416": "Frequency of consuming six or more units of
    alcohol"
    UK Biobank data coding "523" for variable field "20416".
    "never": 1
    "less than monthly": 2
    "monthly": 3
    "weekly": 4
    "daily or almost daily": 5
    "prefer not to answer": -818

    The official AUDIT-C questionnaire scores each question on 0 to 4 points.
    https://cde.drugabuse.gov/instrument/f229c68a-67ce-9a58-e040-bb89ad432be4

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
    # Convert variable types.
    columns_type = [
        "20414-0.0", "20403-0.0", "20416-0.0",
    ]
    table = convert_table_columns_variables_types_float(
        columns=columns_type,
        table=table,
    )
    # Determine person's AUDIT-C score.
    table["alcohol_auditc"] = table.apply(
        lambda row:
            determine_alcohol_auditc_score(
                audit_1=row["20414-0.0"],
                audit_2=row["20403-0.0"],
                audit_3=row["20416-0.0"],
            ),
        axis="columns", # apply across rows
    )
    # Remove columns for variables that are not necessary anymore.
    table_clean = table.copy(deep=True)
    table_clean.drop(
        labels=["20414-0.0", "20403-0.0", "20416-0.0",],
        axis="columns",
        inplace=True
    )
    # Organize data for report.
    table_report = table.copy(deep=True)
    table_report = table_report.loc[
        :, table_report.columns.isin([
            "eid", "IID",
            "20414-0.0", "20403-0.0", "20416-0.0",
            "alcohol_auditc",
        ])
    ]
    # Report.
    if report:
        utility.print_terminal_partition(level=2)
        print("Summary of alcohol AUDIT-C variables: ")
        print(table_report)
    # Collect information.
    pail = dict()
    pail["table"] = table
    pail["table_clean"] = table_clean
    pail["table_report"] = table_report
    # Return information.
    return pail


def determine_alcohol_audit_score(
    audit_c=None,
    audit_4=None,
    audit_5=None,
    audit_6=None,
    audit_7=None,
    audit_8=None,
    audit_9=None,
    audit_10=None,
):
    """
    Determine a person's score from the AUDIT questionnaire.

    Accommodate inexact float values.

    arguments:
        audit_c ((float): combination score for AUDIT-C questionnaire
        audit_4 (float): AUDIT questionnaire question 4, UK Biobank field
            20413
        audit_5 (float): AUDIT questionnaire question 5, UK Biobank field
            20407
        audit_6 (float): AUDIT questionnaire question 6, UK Biobank field
            20412
        audit_7 (float): AUDIT questionnaire question 7, UK Biobank field
            20409
        audit_8 (float): AUDIT questionnaire question 8, UK Biobank field
            20408
        audit_9 (float): AUDIT questionnaire question 9, UK Biobank field
            20411
        audit_10 (float): AUDIT questionnaire question 10, UK Biobank field
            20405

    raises:

    returns:
        (float): combination score for AUDIT questionnaire

    """

    # Interpret raw variables.
    audit_4_clean = interpret_alcohol_audit_two_to_eight(
        value=audit_4,
    )
    audit_5_clean = interpret_alcohol_audit_two_to_eight(
        value=audit_5,
    )
    audit_6_clean = interpret_alcohol_audit_two_to_eight(
        value=audit_6,
    )
    audit_7_clean = interpret_alcohol_audit_two_to_eight(
        value=audit_7,
    )
    audit_8_clean = interpret_alcohol_audit_two_to_eight(
        value=audit_8,
    )
    audit_9_clean = interpret_alcohol_audit_nine_ten(
        value=audit_9,
    )
    audit_10_clean = interpret_alcohol_audit_nine_ten(
        value=audit_10,
    )

    # Integrate information from multiple variables.
    if (
        (not math.isnan(audit_c)) and
        (not math.isnan(audit_4_clean)) and
        (not math.isnan(audit_5_clean)) and
        (not math.isnan(audit_6_clean)) and
        (not math.isnan(audit_7_clean)) and
        (not math.isnan(audit_8_clean)) and
        (not math.isnan(audit_9_clean)) and
        (not math.isnan(audit_10_clean))
    ):
        audit_score = (
            audit_c +
            audit_4_clean + audit_5_clean + audit_6_clean + audit_7_clean +
            audit_8_clean +
            audit_9_clean + audit_10_clean
        )
    else:
        audit_score = float("nan")
    # Return information.
    return audit_score


def organize_alcohol_audit_variables(
    table=None,
    report=None,
):
    """
    Organizes information about alcohol AUDIT questionnaire.

    "audit_4", field "20413": "Frequency of inability to cease drinking in last
    year"
    UK Biobank data coding "523" for variable field "20413".
    "never": 1
    "less than monthly": 2
    "monthly": 3
    "weekly": 4
    "daily or almost daily": 5
    "prefer not to answer": -818

    "audit_5", field "20407": "Frequency of failure to fulfil normal
    expectations due to drinking alcohol in last year"
    UK Biobank data coding "523" for variable field "20407".
    "never": 1
    "less than monthly": 2
    "monthly": 3
    "weekly": 4
    "daily or almost daily": 5
    "prefer not to answer": -818

    "audit_6", field "20412": "Frequency of needing morning drink of alcohol
    after heavy drinking session in last year"
    UK Biobank data coding "523" for variable field "20412".
    "never": 1
    "less than monthly": 2
    "monthly": 3
    "weekly": 4
    "daily or almost daily": 5
    "prefer not to answer": -818

    "audit_7", field "20409": "Frequency of feeling guilt or remorse after
    drinking alcohol in last year"
    UK Biobank data coding "523" for variable field "20409".
    "never": 1
    "less than monthly": 2
    "monthly": 3
    "weekly": 4
    "daily or almost daily": 5
    "prefer not to answer": -818

    "audit_8", field "20408": "Frequency of memory loss due to drinking alcohol
    in last year"
    UK Biobank data coding "523" for variable field "20408".
    "never": 1
    "less than monthly": 2
    "monthly": 3
    "weekly": 4
    "daily or almost daily": 5
    "prefer not to answer": -818

    "audit_9", field "20411": "Ever been injured or injured someone else
    through drinking alcohol"
    UK Biobank data coding "524" for variable field "20411".
    "no": 0
    "yes, but not in the last year": 1
    "yes, during the last year": 2
    "prefer not to answer": -818

    "audit_10", field "20405": "Ever had known person concerned about, or
    recommend reduction of, alcohol consumption"
    UK Biobank data coding "524" for variable field "20405".
    "no": 0
    "yes, but not in the last year": 1
    "yes, during the last year": 2
    "prefer not to answer": -818

    The official AUDIT questionnaire scores questions 1-8 on 0 to 4 points and
    questions 9-10 on 0, 2, or 4 points.
    https://auditscreen.org/about/scoring-audit/

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
    # Convert variable types.
    columns_type = [
        "20413-0.0", "20407-0.0", "20412-0.0", "20409-0.0", "20408-0.0",
        "20411-0.0", "20405-0.0",
    ]
    table = convert_table_columns_variables_types_float(
        columns=columns_type,
        table=table,
    )
    # Determine person's AUDIT-C score.
    table["alcohol_audit"] = table.apply(
        lambda row:
            determine_alcohol_audit_score(
                audit_c=row["alcohol_auditc"],
                audit_4=row["20413-0.0"],
                audit_5=row["20407-0.0"],
                audit_6=row["20412-0.0"],
                audit_7=row["20409-0.0"],
                audit_8=row["20408-0.0"],
                audit_9=row["20411-0.0"],
                audit_10=row["20405-0.0"],
            ),
        axis="columns", # apply across rows
    )
    # Remove columns for variables that are not necessary anymore.
    table_clean = table.copy(deep=True)
    table_clean.drop(
        labels=columns_type,
        axis="columns",
        inplace=True
    )
    # Organize data for report.
    table_report = table.copy(deep=True)
    table_report = table_report.loc[
        :, table_report.columns.isin([
            "eid", "IID",
            "20413-0.0", "20407-0.0", "20412-0.0", "20409-0.0", "20408-0.0",
            "20411-0.0", "20405-0.0",
            "alcohol_auditc",
            "alcohol_audit",
        ])
    ]
    # Report.
    if report:
        utility.print_terminal_partition(level=2)
        print("Summary of alcohol AUDIT variables: ")
        print(table_report)
    # Collect information.
    pail = dict()
    pail["table"] = table
    pail["table_clean"] = table_clean
    pail["table_report"] = table_report
    # Return information.
    return pail


def organize_alcohol_audit_questionnaire_variables(
    table=None,
    report=None,
):
    """
    Organizes information about alcohol AUDIT questionnaire.

    arguments:
        table (object): Pandas data frame of phenotype variables across UK
            Biobank cohort
        report (bool): whether to print reports

    raises:

    returns:
        (dict): collection of information about phenotype variables

    """

    # Organize information about alcohol AUDIT-C.
    pail_auditc = organize_alcohol_auditc_variables(
        table=table,
        report=report,
    )
    # Organize information about alcohol AUDIT.
    pail_audit = organize_alcohol_audit_variables(
        table=pail_auditc["table_clean"],
        report=report,
    )
    # Collect information.
    pail = dict()
    pail["auditc"] = pail_auditc
    pail["audit"] = pail_audit
    # Return information.
    return pail


##########
# Alcoholism diagnoses


def specify_icd_alcoholism_diagnosis_groups_codes():
    """
    Specifies the codes for diagnostic groups relevant to alcoholism.

    arguments:

    raises:

    returns:
        (dict<dict<str>>): collections of codes for diagnostic groups

    """

    # Determine whether the variable has a valid (non-missing) value.
    codes = dict()

    codes["group_a"] = dict()
    codes["group_a"]["icd_9"] = [
        "3039", "291", "2910", "2918",
    ]
    codes["group_a"]["icd_10"] = [
        "F102", "F103", "F104", "F105", "F106", "F107", "F108",
    ]

    codes["group_b"] = dict()
    codes["group_b"]["icd_9"] = []
    codes["group_b"]["icd_10"] = [
        "F10", "F100", "F109",
    ]

    codes["group_c"] = dict()
    codes["group_c"]["icd_9"] = [
        "3050",
    ]
    codes["group_c"]["icd_10"] = [
        "F101",
    ]

    codes["group_d"] = dict()
    codes["group_d"]["icd_9"] = [
        "3575", "4255", "5353", "5710", "5711", "5712", "5713",
    ]
    codes["group_d"]["icd_10"] = [
        "G621", "I426", "K292", "K70", "K700", "K701", "K702", "K703", "K704",
        "K709",
    ]

    # Return information.
    return codes


def specify_self_alcoholism_diagnosis_codes():
    """
    Specifies the codes for diagnostic groups relevant to alcoholism.

    arguments:

    raises:

    returns:
        (list<str>): codes for self diagnosis

    """

    # Specify codes.
    codes = [
        "1408", "1604",
    ]
    # Return information.
    return codes


def parse_field_array_codes(
    collection=None,
    delimiter=None,
):
    """
    Parse the field's array codes.

    arguments:
        collection (str): raw string of field's array codes
        delimiter (str): delimiter between codes

    raises:

    returns:
        (list<str>): field's array codes

    """

    if (
        (len(str(collection)) > 0) and (delimiter in str(collection))
    ):
        codes_raw = str(collection).split(delimiter)
        codes = list()
        for code_raw in codes_raw:
            code = str(code_raw).strip()
            if (len(code) > 0):
                codes.append(str(code))
            pass
    else:
        codes = list()
    return codes


def parse_interpret_match_diagnosis_codes(
    row=None,
    fields=None,
    codes_match=None,
):
    """
    Parses and interprets ICD diagnosis codes.

    arguments:
        row (object): Pandas series corresponding to a row of a Pandas data
            frame
        fields (list<str>): names of columns for UK Biobank fields for
            diagnostic codes
        codes_match (list<str>): codes corresponding to a diagnostic
            group

    raises:

    returns:
        (bool): whether values in the current row match the diagnostic group

    """

    match = False
    for field in fields:
        collection = row[field]
        codes = parse_field_array_codes(
            collection=collection,
            delimiter=";",
        )
        if (len(codes) > 0):
            for code in codes:
                if (code in codes_match):
                    match = True
            pass
        pass
    return match


def determine_diagnosis_icd_alcoholism_group(
    row=None,
    fields_icd_9=None,
    fields_icd_10=None,
    codes_icd_group=None,
):
    """
    Organizes information about diagnoses relevant to alcoholism.

    arguments:
        row (object): Pandas series corresponding to a row of a Pandas data
            frame
        fields_icd_9 (list<str>): names of columns for UK Biobank fields for
            ICD9 diagnostic codes
        fields_icd_10 (list<str>): names of columns for UK Biobank fields for
            ICD10 diagnostic codes
        codes_icd_group (dict<list<str>>): ICD9 and ICD10 codes corresponding
            to a diagnostic group

    raises:

    returns:
        (bool): whether values in the current row match the diagnostic group

    """

    # Determine whether any codes in any ICD9 fields match diagnostic group.
    icd_9_group = parse_interpret_match_diagnosis_codes(
        row=row,
        fields=fields_icd_9,
        codes_match=codes_icd_group["icd_9"],
    )
    # Determine whether any codes in any ICD10 fields match diagnostic group.
    icd_10_group = parse_interpret_match_diagnosis_codes(
        row=row,
        fields=fields_icd_10,
        codes_match=codes_icd_group["icd_10"],
    )
    # Interpret matches from either ICD9 or ICD10 codes.
    if (icd_9_group or icd_10_group):
        match = True
    else:
        match = False
    # Return information.
    return match


def organize_alcoholism_diagnosis_variables(
    table=None,
    report=None,
):
    """
    Organizes information about diagnoses relevant to alcoholism.

    arguments:
        table (object): Pandas data frame of phenotype variables across UK
            Biobank cohort
        report (bool): whether to print reports

    raises:

    returns:
        (dict): collection of information about alcoholism diagnoses

    """

    # Copy data.
    table = table.copy(deep=True)
    # Specify ICD9 and ICD10 diagnostic codes relevant to alcoholism.
    codes_icd = specify_icd_alcoholism_diagnosis_groups_codes()
    # Specify relevant codes from self diagnosis.
    codes_self = specify_self_alcoholism_diagnosis_codes()

    # Determine whether person has diagnoses in group A.
    table["alcohol_diagnosis_a"] = table.apply(
        lambda row:
            determine_diagnosis_icd_alcoholism_group(
                row=row.copy(deep=True),
                fields_icd_9=["41271_array", "41203_array", "41205_array",],
                fields_icd_10=["41270_array", "41202_array", "41204_array",],
                codes_icd_group=codes_icd["group_a"],
            ),
        axis="columns", # apply across rows
    )
    # Determine whether person has diagnoses in group B.
    table["alcohol_diagnosis_b"] = table.apply(
        lambda row:
            determine_diagnosis_icd_alcoholism_group(
                row=row.copy(deep=True),
                fields_icd_9=["41271_array", "41203_array", "41205_array",],
                fields_icd_10=["41270_array", "41202_array", "41204_array",],
                codes_icd_group=codes_icd["group_b"],
            ),
        axis="columns", # apply across rows
    )
    # Determine whether person has diagnoses in group C.
    table["alcohol_diagnosis_c"] = table.apply(
        lambda row:
            determine_diagnosis_icd_alcoholism_group(
                row=row.copy(deep=True),
                fields_icd_9=["41271_array", "41203_array", "41205_array",],
                fields_icd_10=["41270_array", "41202_array", "41204_array",],
                codes_icd_group=codes_icd["group_c"],
            ),
        axis="columns", # apply across rows
    )
    # Determine whether person has diagnoses in group D.
    table["alcohol_diagnosis_d"] = table.apply(
        lambda row:
            determine_diagnosis_icd_alcoholism_group(
                row=row.copy(deep=True),
                fields_icd_9=["41271_array", "41203_array", "41205_array",],
                fields_icd_10=["41270_array", "41202_array", "41204_array",],
                codes_icd_group=codes_icd["group_d"],
            ),
        axis="columns", # apply across rows
    )
    # Determine whether person has self diagnoses.
    table["alcohol_diagnosis_self"] = table.apply(
        lambda row:
            parse_interpret_match_diagnosis_codes(
                row=row.copy(deep=True),
                fields=["20002_array"],
                codes_match=codes_self,
            ),
        axis="columns", # apply across rows
    )

    # Remove columns for variables that are not necessary anymore.
    table_clean = table.copy(deep=True)
    table_clean.drop(
        labels=[
            "41271_array", "41203_array", "41205_array",
            "41270_array", "41202_array", "41204_array",
            "20002_array",
        ],
        axis="columns",
        inplace=True
    )
    # Organize data for report.
    table_report = table.copy(deep=True)
    #table_report = table_report.loc[
    #    table_report["alcohol_diagnosis_a"] == True, :
    #]
    table_report = table_report.loc[
        :, table_report.columns.isin([
            "eid", "IID",
            "41271_array", "41203_array", "41205_array", "41270_array",
            "41202_array", "41204_array", "20002_array",
            "alcohol_diagnosis_a",
            "alcohol_diagnosis_b",
            "alcohol_diagnosis_c",
            "alcohol_diagnosis_d",
            "alcohol_diagnosis_self",
        ])
    ]
    # Report.
    if report:
        utility.print_terminal_partition(level=2)
        print("Summary of alcohol diagnosis variables: ")
        print(table_report)
    # Collect information.
    pail = dict()
    pail["table"] = table
    pail["table_clean"] = table_clean
    pail["table_report"] = table_report
    # Return information.
    return pail


##########
# Alcoholism cases and controls


def determine_control_alcoholism_one_two(
    alcohol_none=None,
    alcohol_diagnosis_a=None,
    alcohol_diagnosis_b=None,
    alcohol_diagnosis_c=None,
    alcohol_diagnosis_d=None,
    alcohol_diagnosis_self=None,
    alcohol_auditc=None,
    alcohol_audit=None,
    threshold_auditc=None,
    threshold_audit=None,
):
    """
    Determines whether person qualifies as a control for alcoholism.

    arguments:
        alcohol_none (float): binary representation of whether person has never
            consumed alcohol, formerly or currently
        alcohol_diagnosis_a (bool): whether person has diagnosis in alcoholism
            group A
        alcohol_diagnosis_b (bool): whether person has diagnosis in alcoholism
            group B
        alcohol_diagnosis_c (bool): whether person has diagnosis in alcoholism
            group C
        alcohol_diagnosis_d (bool): whether person has diagnosis in alcoholism
            group D
        alcohol_diagnosis_self (bool): whether person has self diagnosis of
            alcoholism
        alcohol_auditc (float): combination score for AUDIT-C questionnaire
        alcohol_audit (float): combination score for AUDIT questionnaire
        threshold_auditc (float): diagnostic threshold for AUDIT-C score
        threshold_audit (float): diagnostic threshold for AUDIT score

    raises:

    returns:
        (bool): whether person qualifies as a control for alcoholism

    """

    # Determine whether person has consumed alcohol, previously or currently.
    # Only persons who have consumed alcohol, previously or currently, ought to
    # qualify as controls for alcoholism.
    if (math.isnan(alcohol_none)):
        match_consumption = False
    else:
        if (alcohol_none < 0.5):
            # Person has consumed alcohol, previously or currently.
            match_consumption = True
        else:
            # Person has never consumed alcohol, previously or currently.
            match_consumption = False

    # Determine whether person's AUDIT-C and AUDIT scores are within
    # thresholds.
    if (math.isnan(alcohol_auditc)):
        comparison_auditc = False
    else:
        if (alcohol_auditc <= threshold_auditc):
            comparison_auditc = True
        else:
            comparison_auditc = False
    if (math.isnan(alcohol_audit)):
        comparison_audit = False
    else:
        if (alcohol_audit <= threshold_audit):
            comparison_audit = True
        else:
            comparison_audit = False
    # Interpret both AUDIT-C and AUDIT socres.
    if (comparison_auditc and comparison_audit):
        match_audit = True
    else:
        match_audit = False

    # Determine whether person has diagnoses in any relevant groups.
    # Diagnoses from ICD9 and ICD10 cannot be null or missing under current
    # interpretation.
    if (
        (not alcohol_diagnosis_a) and
        (not alcohol_diagnosis_b) and
        (not alcohol_diagnosis_c) and
        (not alcohol_diagnosis_d) and
        (not alcohol_diagnosis_self)
    ):
        match_diagnosis = True
    else:
        match_diagnosis = False
    # Integrate information from both criteria.
    if (match_consumption and match_audit and match_diagnosis):
        # Person qualifies as a control for alcoholism.
        # Person's AUDIT-C and AUDIT scores are below diagnostic
        # thresholds.
        # Person does not have any ICD9 or ICD10 diagnostic codes
        # indicative of alcoholism.
        match = True
    else:
        match = False

    # Return information.
    return match


def determine_case_control_alcoholism_one(
    alcohol_none=None,
    alcohol_diagnosis_a=None,
    alcohol_diagnosis_b=None,
    alcohol_diagnosis_c=None,
    alcohol_diagnosis_d=None,
    alcohol_diagnosis_self=None,
    alcohol_auditc=None,
    alcohol_audit=None,
    threshold_auditc=None,
    threshold_audit=None,
):
    """
    Organizes information about alcoholism cases and controls.

    arguments:
        alcohol_none (float): binary representation of whether person has never
            consumed alcohol, formerly or currently
        alcohol_diagnosis_a (bool): whether person has diagnosis in alcoholism
            group A
        alcohol_diagnosis_b (bool): whether person has diagnosis in alcoholism
            group B
        alcohol_diagnosis_c (bool): whether person has diagnosis in alcoholism
            group C
        alcohol_diagnosis_d (bool): whether person has diagnosis in alcoholism
            group D
        alcohol_diagnosis_self (bool): whether person has self diagnosis of
            alcoholism
        alcohol_auditc (float): combination score for AUDIT-C questionnaire
        alcohol_audit (float): combination score for AUDIT questionnaire
        threshold_auditc (float): diagnostic threshold for AUDIT-C score
        threshold_audit (float): diagnostic threshold for AUDIT score

    raises:

    returns:
        (float): binary representation whether person qualifies as a case or
            control by specific definition of alcoholism

    """

    # Determine whether person qualifies as a case of alcoholism.
    #case = bool(alcohol_diagnosis_a)
    if (
        (alcohol_diagnosis_a)
    ):
        case = True
    else:
        case = False

    # Determine whether person qualifies as a control of alcoholism.
    # Person's control status can have null or missing values.
    control = determine_control_alcoholism_one_two(
        alcohol_none=alcohol_none,
        alcohol_diagnosis_a=alcohol_diagnosis_a,
        alcohol_diagnosis_b=alcohol_diagnosis_b,
        alcohol_diagnosis_c=alcohol_diagnosis_c,
        alcohol_diagnosis_d=alcohol_diagnosis_d,
        alcohol_diagnosis_self=alcohol_diagnosis_self,
        alcohol_auditc=alcohol_auditc,
        alcohol_audit=alcohol_audit,
        threshold_auditc=threshold_auditc,
        threshold_audit=threshold_audit,
    )

    # Interpret case and control and assign value.
    # Interpretation variables "case" and "control" do not have null values.
    # Assign missing value to persons who qualify neither as case nor control.
    if case:
        value = 1
    elif control:
        value = 0
    else:
        value = float("nan")
    # Return information.
    return value


def determine_case_control_alcoholism_two(
    alcohol_none=None,
    alcohol_diagnosis_a=None,
    alcohol_diagnosis_b=None,
    alcohol_diagnosis_c=None,
    alcohol_diagnosis_d=None,
    alcohol_diagnosis_self=None,
    alcohol_auditc=None,
    alcohol_audit=None,
    threshold_auditc=None,
    threshold_audit=None,
):
    """
    Organizes information about alcoholism cases and controls.

    arguments:
        alcohol_none (float): binary representation of whether person has never
            consumed alcohol, formerly or currently
        alcohol_diagnosis_a (bool): whether person has diagnosis in alcoholism
            group A
        alcohol_diagnosis_b (bool): whether person has diagnosis in alcoholism
            group B
        alcohol_diagnosis_c (bool): whether person has diagnosis in alcoholism
            group C
        alcohol_diagnosis_d (bool): whether person has diagnosis in alcoholism
            group D
        alcohol_diagnosis_self (bool): whether person has self diagnosis of
            alcoholism
        alcohol_auditc (float): combination score for AUDIT-C questionnaire
        alcohol_audit (float): combination score for AUDIT questionnaire
        threshold_auditc (float): diagnostic threshold for AUDIT-C score
        threshold_audit (float): diagnostic threshold for AUDIT score

    raises:

    returns:
        (float): binary representation whether person qualifies as a case or
            control by specific definition of alcoholism

    """

    # Determine whether person qualifies as a case of alcoholism.
    if (
        (alcohol_diagnosis_a) or
        (alcohol_diagnosis_b) or
        (alcohol_diagnosis_c) or
        (alcohol_diagnosis_d)
    ):
        case = True
    else:
        case = False

    # Determine whether person qualifies as a control of alcoholism.
    # Person's control status can have null or missing values.
    control = determine_control_alcoholism_one_two(
        alcohol_none=alcohol_none,
        alcohol_diagnosis_a=alcohol_diagnosis_a,
        alcohol_diagnosis_b=alcohol_diagnosis_b,
        alcohol_diagnosis_c=alcohol_diagnosis_c,
        alcohol_diagnosis_d=alcohol_diagnosis_d,
        alcohol_diagnosis_self=alcohol_diagnosis_self,
        alcohol_auditc=alcohol_auditc,
        alcohol_audit=alcohol_audit,
        threshold_auditc=threshold_auditc,
        threshold_audit=threshold_audit,
    )

    # Interpret case and control and assign value.
    # Interpretation variables "case" and "control" do not have null values.
    # Assign missing value to persons who qualify neither as case nor control.
    if case:
        value = 1
    elif control:
        value = 0
    else:
        value = float("nan")
    # Return information.
    return value


def determine_case_control_alcoholism_three(
    alcohol_none=None,
    alcohol_diagnosis_a=None,
    alcohol_diagnosis_b=None,
    alcohol_diagnosis_c=None,
    alcohol_diagnosis_d=None,
    alcohol_diagnosis_self=None,
    alcohol_auditc=None,
    alcohol_audit=None,
    threshold_auditc=None,
    threshold_audit=None,
):
    """
    Organizes information about alcoholism cases and controls.

    arguments:
        alcohol_none (float): binary representation of whether person has never
            consumed alcohol, formerly or currently
        alcohol_diagnosis_a (bool): whether person has diagnosis in alcoholism
            group A
        alcohol_diagnosis_b (bool): whether person has diagnosis in alcoholism
            group B
        alcohol_diagnosis_c (bool): whether person has diagnosis in alcoholism
            group C
        alcohol_diagnosis_d (bool): whether person has diagnosis in alcoholism
            group D
        alcohol_diagnosis_self (bool): whether person has self diagnosis of
            alcoholism
        alcohol_auditc (float): combination score for AUDIT-C questionnaire
        alcohol_audit (float): combination score for AUDIT questionnaire
        threshold_auditc (float): diagnostic threshold for AUDIT-C score
        threshold_audit (float): diagnostic threshold for AUDIT score

    raises:

    returns:
        (float): binary representation whether person qualifies as a case or
            control by specific definition of alcoholism

    """

    # Determine whether person qualifies as a case of alcoholism.
    if (math.isnan(alcohol_auditc)):
        case = False
    else:
        if (alcohol_auditc > threshold_auditc):
            case = True
        else:
            case = False

    # Determine whether person qualifies as a control of alcoholism.
    # Person's control status can have null or missing values.
    control = determine_control_alcoholism_one_two(
        alcohol_none=alcohol_none,
        alcohol_diagnosis_a=alcohol_diagnosis_a,
        alcohol_diagnosis_b=alcohol_diagnosis_b,
        alcohol_diagnosis_c=alcohol_diagnosis_c,
        alcohol_diagnosis_d=alcohol_diagnosis_d,
        alcohol_diagnosis_self=alcohol_diagnosis_self,
        alcohol_auditc=alcohol_auditc,
        alcohol_audit=alcohol_audit,
        threshold_auditc=threshold_auditc,
        threshold_audit=threshold_audit,
    )

    # Interpret case and control and assign value.
    # Interpretation variables "case" and "control" do not have null values.
    # Assign missing value to persons who qualify neither as case nor control.
    if case:
        value = 1
    elif control:
        value = 0
    else:
        value = float("nan")
    # Return information.
    return value


def determine_case_control_alcoholism_four(
    alcohol_none=None,
    alcohol_diagnosis_a=None,
    alcohol_diagnosis_b=None,
    alcohol_diagnosis_c=None,
    alcohol_diagnosis_d=None,
    alcohol_diagnosis_self=None,
    alcohol_auditc=None,
    alcohol_audit=None,
    threshold_auditc=None,
    threshold_audit=None,
):
    """
    Organizes information about alcoholism cases and controls.

    arguments:
        alcohol_none (float): binary representation of whether person has never
            consumed alcohol, formerly or currently
        alcohol_diagnosis_a (bool): whether person has diagnosis in alcoholism
            group A
        alcohol_diagnosis_b (bool): whether person has diagnosis in alcoholism
            group B
        alcohol_diagnosis_c (bool): whether person has diagnosis in alcoholism
            group C
        alcohol_diagnosis_d (bool): whether person has diagnosis in alcoholism
            group D
        alcohol_diagnosis_self (bool): whether person has self diagnosis of
            alcoholism
        alcohol_auditc (float): combination score for AUDIT-C questionnaire
        alcohol_audit (float): combination score for AUDIT questionnaire
        threshold_auditc (float): diagnostic threshold for AUDIT-C score
        threshold_audit (float): diagnostic threshold for AUDIT score

    raises:

    returns:
        (float): binary representation whether person qualifies as a case or
            control by specific definition of alcoholism

    """

    # Determine whether person qualifies as a case of alcoholism.
    if (math.isnan(alcohol_audit)):
        case = False
    else:
        if (alcohol_audit > threshold_audit):
            case = True
        else:
            case = False
    # Determine whether person qualifies as a control of alcoholism.
    # Person's control status can have null or missing values.
    control = determine_control_alcoholism_one_two(
        alcohol_none=alcohol_none,
        alcohol_diagnosis_a=alcohol_diagnosis_a,
        alcohol_diagnosis_b=alcohol_diagnosis_b,
        alcohol_diagnosis_c=alcohol_diagnosis_c,
        alcohol_diagnosis_d=alcohol_diagnosis_d,
        alcohol_diagnosis_self=alcohol_diagnosis_self,
        alcohol_auditc=alcohol_auditc,
        alcohol_audit=alcohol_audit,
        threshold_auditc=threshold_auditc,
        threshold_audit=threshold_audit,
    )

    # Interpret case and control and assign value.
    # Interpretation variables "case" and "control" do not have null values.
    # Assign missing value to persons who qualify neither as case nor control.
    if case:
        value = 1
    elif control:
        value = 0
    else:
        value = float("nan")
    # Return information.
    return value


def report_alcoholism_candidates_by_sex(
    sex_text=None,
    table=None,
):
    """
    Selects variable columns and record rows with valid values across all
    variables.

    arguments:
        sex_text (str): textual representation of sex selection
        table (object): Pandas data frame of phenotype variables across UK
            Biobank cohort

    raises:

    returns:

    """

    # Copy data.
    table = table.copy(deep=True)
    # Select records with valid (non-null) values of relevant variables.
    table = select_valid_records_all_specific_variables(
        names=[
            "eid", "IID",
            "sex", "sex_text", "age", "body_mass_index",
            "alcohol_none",
        ],
        prefixes=["genotype_pc_",],
        table=table,
        drop_columns=True,
        report=False,
    )
    # Select records by sex.
    table = table.loc[
        table["sex_text"] == sex_text, :
    ]
    # Determine whether person has consumed alcohol, previously or currently.
    # Only persons who have consumed alcohol, previously or currently, ought to
    # qualify as controls for alcoholism.
    table = table.loc[
        table["alcohol_none"] < 0.5, :
    ]
    # Report.
    utility.print_terminal_partition(level=2)
    print(
        "Persons who consume alcohol previously or currently are candidates"
        " for alcoholism cases or controls."
    )
    utility.print_terminal_partition(level=3)
    print("sex: " + str(sex_text))
    utility.print_terminal_partition(level=3)
    print("Table dimensions after selection candidates by sex and alcohol.")
    print("table shape: " + str(table.shape))

    pass


def report_alcoholism_candidates_females_males(
    table=None,
):
    """
    Reports the counts of females and males who are candidates for alcoholism
    cases and controls.

    arguments:
        table (object): Pandas data frame of phenotype variables across UK
            Biobank cohort

    raises:

    returns:

    """

    # Females.
    report_alcoholism_candidates_by_sex(
        sex_text="female",
        table=table,
    )
    # Males.
    report_alcoholism_candidates_by_sex(
        sex_text="male",
        table=table,
    )

    pass


def report_alcoholism_cases_controls_by_sex(
    alcoholism=None,
    sex_text=None,
    table=None,
):
    """
    Selects variable columns and record rows with valid values across all
    variables.

    arguments:
        alcoholism (str): name of column defining alcoholism cases and controls
        sex_text (str): textual representation of sex selection
        table (object): Pandas data frame of phenotype variables across UK
            Biobank cohort

    raises:

    returns:

    """

    # Copy data.
    table = table.copy(deep=True)
    # Select records with valid (non-null) values of relevant variables.
    table = select_valid_records_all_specific_variables(
        names=[
            "eid", "IID",
            "sex", "sex_text", "age", "body_mass_index",
            alcoholism,
        ],
        prefixes=["genotype_pc_",],
        table=table,
        drop_columns=True,
        report=False,
    )
    # Select records by sex.
    table = table.loc[
        table["sex_text"] == sex_text, :
    ]
    # Select cases and controls.
    table_case = table.loc[
        table[alcoholism] > 0.5, :
    ]
    table_control = table.loc[
        table[alcoholism] < 0.5, :
    ]
    # Report.
    utility.print_terminal_partition(level=2)
    print(
        "Cases and controls by sex."
    )
    utility.print_terminal_partition(level=3)
    print("sex: " + str(sex_text))
    utility.print_terminal_partition(level=3)
    print("Table dimensions for cases and controls.")
    print("Cases table shape: " + str(table_case.shape))
    print("Controls table shape: " + str(table_control.shape))

    pass


def report_alcoholism_cases_controls_females_males(
    alcoholism=None,
    table=None,
):
    """
    Reports the counts of females and males who are candidates for alcoholism
    cases and controls.

    arguments:
        alcoholism (str): name of column defining alcoholism cases and controls
        table (object): Pandas data frame of phenotype variables across UK
            Biobank cohort

    raises:

    returns:

    """

    # Report.
    utility.print_terminal_partition(level=2)
    print(
        "Cases and controls by sex and definitions of alcoholism."
    )
    utility.print_terminal_partition(level=3)
    print("Alcoholism variable: " + str(alcoholism))

    # Females.
    report_alcoholism_cases_controls_by_sex(
        alcoholism=alcoholism,
        sex_text="female",
        table=table,
    )
    # Males.
    report_alcoholism_cases_controls_by_sex(
        alcoholism=alcoholism,
        sex_text="male",
        table=table,
    )

    pass


def organize_alcoholism_cases_controls_variables(
    table=None,
    report=None,
):
    """
    Organizes information about alcoholism cases and controls.

    arguments:
        table (object): Pandas data frame of phenotype variables across UK
            Biobank cohort
        report (bool): whether to print reports

    raises:

    returns:
        (dict): collection of information about alcoholism cases and controls

    """

    # Copy data.
    table = table.copy(deep=True)
    # Specify diagnostic thresholds for AUDIT-C and AUDIT scores.
    # https://auditscreen.org/about/scoring-audit/
    # Use less than or equal.
    threshold_auditc = 7
    threshold_audit = 14

    # Determine whether person is a case or control for alcoholism type 1.
    # case: ICD9 or ICD10 codes in diagnostic group A
    # control:
    # - only persons who have consumed alcohol, previously or currently
    # - no ICD9 or ICD10 codes in diagnostic groups A, B, C, or D
    # - no self diagnoses of alcoholism
    # - below AUDIT-C and AUDIT thresholds
    table["alcoholism_1"] = table.apply(
        lambda row:
            determine_case_control_alcoholism_one(
                alcohol_none=row["alcohol_none"],
                alcohol_diagnosis_a=row["alcohol_diagnosis_a"],
                alcohol_diagnosis_b=row["alcohol_diagnosis_b"],
                alcohol_diagnosis_c=row["alcohol_diagnosis_c"],
                alcohol_diagnosis_d=row["alcohol_diagnosis_d"],
                alcohol_diagnosis_self=row["alcohol_diagnosis_self"],
                alcohol_auditc=row["alcohol_auditc"],
                alcohol_audit=row["alcohol_audit"],
                threshold_auditc=threshold_auditc,
                threshold_audit=threshold_audit,
            ),
        axis="columns", # apply across rows
    )
    # Determine whether person is a case or control for alcoholism type 2.
    # case: ICD9 or ICD10 codes in diagnostic group A, B, C, or D
    # control:
    # - only persons who have consumed alcohol, previously or currently
    # - no ICD9 or ICD10 codes in diagnostic groups A, B, C, or D
    # - no self diagnoses of alcoholism
    # - below AUDIT-C and AUDIT thresholds
    table["alcoholism_2"] = table.apply(
        lambda row:
            determine_case_control_alcoholism_two(
                alcohol_none=row["alcohol_none"],
                alcohol_diagnosis_a=row["alcohol_diagnosis_a"],
                alcohol_diagnosis_b=row["alcohol_diagnosis_b"],
                alcohol_diagnosis_c=row["alcohol_diagnosis_c"],
                alcohol_diagnosis_d=row["alcohol_diagnosis_d"],
                alcohol_diagnosis_self=row["alcohol_diagnosis_self"],
                alcohol_auditc=row["alcohol_auditc"],
                alcohol_audit=row["alcohol_audit"],
                threshold_auditc=threshold_auditc,
                threshold_audit=threshold_audit,
            ),
        axis="columns", # apply across rows
    )
    # Determine whether person is a case or control for alcoholism type 3.
    # case:
    # AUDIT-C score > threshold_auditc
    # control:
    # - only persons who have consumed alcohol, previously or currently
    # - no ICD9 or ICD10 codes in diagnostic groups A, B, C, or D
    # - no self diagnoses of alcoholism
    # - below AUDIT-C and AUDIT thresholds
    table["alcoholism_3"] = table.apply(
        lambda row:
            determine_case_control_alcoholism_three(
                alcohol_none=row["alcohol_none"],
                alcohol_diagnosis_a=row["alcohol_diagnosis_a"],
                alcohol_diagnosis_b=row["alcohol_diagnosis_b"],
                alcohol_diagnosis_c=row["alcohol_diagnosis_c"],
                alcohol_diagnosis_d=row["alcohol_diagnosis_d"],
                alcohol_diagnosis_self=row["alcohol_diagnosis_self"],
                alcohol_auditc=row["alcohol_auditc"],
                alcohol_audit=row["alcohol_audit"],
                threshold_auditc=threshold_auditc,
                threshold_audit=threshold_audit,
            ),
        axis="columns", # apply across rows
    )
    # Determine whether person is a case or control for alcoholism type 4.
    # case:
    # AUDIT score > threshold_audit
    # control:
    # - only persons who have consumed alcohol, previously or currently
    # - no ICD9 or ICD10 codes in diagnostic groups A, B, C, or D
    # - no self diagnoses of alcoholism
    # - below AUDIT-C and AUDIT thresholds
    table["alcoholism_4"] = table.apply(
        lambda row:
            determine_case_control_alcoholism_four(
                alcohol_none=row["alcohol_none"],
                alcohol_diagnosis_a=row["alcohol_diagnosis_a"],
                alcohol_diagnosis_b=row["alcohol_diagnosis_b"],
                alcohol_diagnosis_c=row["alcohol_diagnosis_c"],
                alcohol_diagnosis_d=row["alcohol_diagnosis_d"],
                alcohol_diagnosis_self=row["alcohol_diagnosis_self"],
                alcohol_auditc=row["alcohol_auditc"],
                alcohol_audit=row["alcohol_audit"],
                threshold_auditc=threshold_auditc,
                threshold_audit=threshold_audit,
            ),
        axis="columns", # apply across rows
    )

    # Remove columns for variables that are not necessary anymore.
    table_clean = table.copy(deep=True)
    table_clean.drop(
        labels=[
            "alcohol_diagnosis_a", "alcohol_diagnosis_b",
            "alcohol_diagnosis_c", "alcohol_diagnosis_d",
            "alcohol_diagnosis_self",
            "alcohol_auditc",
            "alcohol_audit",
        ],
        axis="columns",
        inplace=True
    )
    # Organize data for report.
    table_report = table.copy(deep=True)
    table_report = table_report.loc[
        :, table_report.columns.isin([
            "eid", "IID",
            "alcohol_none",
            "alcohol_diagnosis_a",
            "alcohol_diagnosis_b",
            "alcohol_diagnosis_c",
            "alcohol_diagnosis_d",
            "alcohol_diagnosis_self",
            "alcohol_auditc",
            "alcohol_audit",
            "alcoholism_1", "alcoholism_2", "alcoholism_3", "alcoholism_4",
        ])
    ]
    # Report.
    if report:
        utility.print_terminal_partition(level=2)
        print("Summary of alcoholism cases and controls variables: ")
        print(table_report)
        # Report females and males who consume alcohol and are candidates for
        # either controls or cases of alcoholism.
        utility.print_terminal_partition(level=2)
        print("Alcoholism candidates by sex.")
        report_alcoholism_candidates_females_males(
            table=table_clean
        )
        # Report females and males who are either controls or cases by each
        # definition of alcoholism.
        utility.print_terminal_partition(level=2)
        print("Alcoholism cases and controls by definition of alcoholism.")
        report_alcoholism_cases_controls_females_males(
            alcoholism="alcoholism_1",
            table=table_clean
        )
        report_alcoholism_cases_controls_females_males(
            alcoholism="alcoholism_2",
            table=table_clean
        )
        report_alcoholism_cases_controls_females_males(
            alcoholism="alcoholism_3",
            table=table_clean
        )
        report_alcoholism_cases_controls_females_males(
            alcoholism="alcoholism_4",
            table=table_clean
        )

    # Collect information.
    pail = dict()
    pail["table"] = table
    pail["table_clean"] = table_clean
    pail["table_report"] = table_report
    # Return information.
    return pail


##########
# Cohort selection


def select_valid_records_all_specific_variables(
    names=None,
    prefixes=None,
    table=None,
    drop_columns=None,
    report=None,
):
    """
    Selects variable columns and record rows with valid values across all
    variables.

    arguments:
        names (list<str>): explicit names of columns to keep
        prefixes (list<str>): prefixes of names of columns to keep
        table (object): Pandas data frame of phenotype variables across UK
            Biobank cohort
        drop_columns (bool): whether to drop other columns
        report (bool): whether to print reports

    raises:

    returns:
        (dict): collection of information about phenotype variables

    """

    # Copy data.
    table = table.copy(deep=True)
    # Extract table columns.
    columns_all = copy.deepcopy(table.columns.to_list())
    # Collect columns to keep.
    columns_keep = list()
    columns_names = list(filter(
        lambda column: (str(column) in names),
        columns_all
    ))
    columns_keep.extend(columns_names)
    for prefix in prefixes:
        columns_prefix = list(filter(
            lambda column: (str(prefix) in str(column)),
            columns_all
        ))
        columns_keep.extend(columns_prefix)
    # Report.
    if report:
        utility.print_terminal_partition(level=2)
        print("Columns to keep: ")
        print(columns_keep)
    # Select columns.
    if drop_columns:
        table = table.loc[
            :, table.columns.isin(columns_keep)
        ]
    # Remove any record rows with null values.
    table.dropna(
        axis="index",
        how="any",
        subset=columns_keep,
        inplace=True,
    )
    # Report.
    if report:
        utility.print_terminal_partition(level=2)
        print("After dropping rows with null values in specific columns.")
        print("Selection of table columns and rows: ")
        print(table)
    # Return information.
    return table


def select_valid_cohort_records_variables(
    sex_text=None,
    alcoholism=None,
    hormone=None,
    table=None,
):
    """
    Selects variable columns and record rows with valid values across all
    variables.

    arguments:
        sex_text (str): textual representation of sex selection
        alcoholism (str): name of column defining alcoholism cases and controls
        hormone (str): name of column for relevant sex hormone
        table (object): Pandas data frame of phenotype variables across UK
            Biobank cohort

    raises:

    returns:
        (dict): collection of information about phenotype variables

    """

    # Copy data.
    table = table.copy(deep=True)
    # Select records by sex.
    table = table.loc[
        table["sex_text"] == sex_text, :
    ]
    # Select records with valid (non-null) values of relevant variables.
    table = select_valid_records_all_specific_variables(
        names=[
            "eid", "IID",
            "sex", "sex_text", "age", "body_mass_index",
            hormone,
            alcoholism,
        ],
        prefixes=["genotype_pc_",],
        table=table,
        drop_columns=True,
        report=False,
    )
    # Return information.
    return table


def select_organize_cohorts_variables_by_hormone(
    sex_text=None,
    alcoholism=None,
    table=None,
):
    """
    Organizes information about previous and current alcohol consumption.

    arguments:
        sex_text (str): textual representation of sex selection
        alcoholism (str): name of column defining alcoholism cases and controls
        table (object): Pandas data frame of phenotype variables across UK
            Biobank cohort

    raises:

    returns:
        (dict): collection of information about phenotype variables

    """

    # Select and organize variables across cohorts.
    # Collect information.
    pail = dict()
    pail["oestradiol"] = select_valid_cohort_records_variables(
        sex_text=sex_text,
        alcoholism=alcoholism,
        hormone="oestradiol",
        table=table,
    )
    pail["testosterone"] = select_valid_cohort_records_variables(
        sex_text=sex_text,
        alcoholism=alcoholism,
        hormone="testosterone",
        table=table,
    )
    # Return information.
    return pail


def select_organize_cohorts_variables_by_alcoholism_hormone(
    sex_text=None,
    table=None,
):
    """
    Organizes information about previous and current alcohol consumption.

    arguments:
        sex_text (str): textual representation of sex selection
        table (object): Pandas data frame of phenotype variables across UK
            Biobank cohort

    raises:

    returns:
        (dict): collection of information about phenotype variables

    """


    # Select and organize variables across cohorts.
    # Collect information.
    pail = dict()

    pail["alcoholism_1"] = select_organize_cohorts_variables_by_hormone(
        sex_text=sex_text,
        alcoholism="alcoholism_1",
        table=table,
    )
    pail["alcoholism_2"] = select_organize_cohorts_variables_by_hormone(
        sex_text=sex_text,
        alcoholism="alcoholism_2",
        table=table,
    )
    pail["alcoholism_3"] = select_organize_cohorts_variables_by_hormone(
        sex_text=sex_text,
        alcoholism="alcoholism_3",
        table=table,
    )
    pail["alcoholism_4"] = select_organize_cohorts_variables_by_hormone(
        sex_text=sex_text,
        alcoholism="alcoholism_4",
        table=table,
    )
    # Return information.
    return pail


def select_organize_cohorts_variables_by_sex_alcoholism_hormone(
    table=None,
    report=None,
):
    """
    Organizes information about previous and current alcohol consumption.

    arguments:
        table (object): Pandas data frame of phenotype variables across UK
            Biobank cohort
        report (bool): whether to print reports

    raises:

    returns:
        (dict): collection of information about phenotype variables

    """


    # Select and organize variables across cohorts.
    # Collect information.
    pail = dict()

    pail["female"] = select_organize_cohorts_variables_by_alcoholism_hormone(
        sex_text="female",
        table=table,
    )
    pail["male"] = select_organize_cohorts_variables_by_alcoholism_hormone(
        sex_text="male",
        table=table,
    )
    # Report.
    if report:
        table_report = pail["female"]["alcoholism_1"]["testosterone"].copy(
            deep=True
        )
        table_control = table_report.loc[
            table_report["alcoholism_1"] < 0.5, :
        ]
        table_case = table_report.loc[
            table_report["alcoholism_1"] > 0.5, :
        ]
        utility.print_terminal_partition(level=2)
        print("Females, alcoholism_1, testosterone")
        print("Controls table shape: " + str(table_control.shape))
        utility.print_terminal_partition(level=3)
        print("Cases table shape: " + str(table_case.shape))
        utility.print_terminal_partition(level=3)
    # Return information.
    return pail


##########
# PLINK format


def translate_binary_phenotype_plink(
    binary_value=None,
):
    """
    Translate information from simple binary representation to plink
    representation.

    Accommodate inexact float values and null values.

    arguments:
        binary_value (float): binary (0, 1) representation of a phenotype

    raises:

    returns:
        (float): plink binary representation of a phenotype

    """

    # Determine whether the variable has a valid (non-missing) value.
    if (
        (not math.isnan(binary_value)) and
        (-0.5 <= binary_value and binary_value < 1.5)
    ):
        # The variable has a valid value.
        if (-0.5 <= binary_value and binary_value < 0.5):
            # 0: control
            value = 1
        elif (0.5 <= binary_value and binary_value < 1.5):
            # 1: case
            value = 2
    else:
        # null
        value = float("nan")
    # Return information.
    return value


def organize_phenotype_covariate_table_plink_format(
    binary_phenotypes=None,
    table=None,
    report=None,
):
    """
    Organize table for phenotypes and covariates in format for PLINK.

    1. Remove any rows with missing, empty values.
    PLINK cannot accommodate rows with empty cells.

    2. Introduce family identifiers.
    Family (FID) and individual (IID) identifiers must match the ID_1 and ID_2
    columns in the sample table.

    3. Sort column sequence.
    PLINK requires FID and IID columns to come first.

    arguments:
        binary_phenotypes (list<str>): names of columns with binary phenotypes
            (control: 0, case: 1) that need conversion to PLINK format
            (control: 1, case: 2)
        table (object): Pandas data frame of information about phenotype and
            covariate variables for GWAS
        report (bool): whether to print reports

    raises:

    returns:
        (object): Pandas data frame of information about phenotype and
            covariate variables in format for GWAS in PLINK

    """

    # Copy data.
    table = table.copy(deep=True)
    # Translate binary phenotype variables.
    for binary_phenotype in binary_phenotypes:
        table[binary_phenotype] = table.apply(
            lambda row:
                translate_binary_phenotype_plink(
                    binary_value=row[binary_phenotype],
                ),
            axis="columns", # apply across rows
        )
        pass
    # Organize.
    table.reset_index(
        level=None,
        inplace=True
    )
    # Remove table rows with any empty cells or missing values.
    table.dropna(
        axis="index",
        how="any",
        subset=None,
        inplace=True,
    )
    # Introduce family identifier.
    table["FID"] = table["IID"]
    # Sort column sequence.
    columns = table.columns.to_list()
    columns_sequence = list(filter(
        lambda element: element not in ["eid", "IID", "FID"],
        columns
    ))
    columns_sequence.insert(0, "IID") # second column
    columns_sequence.insert(0, "FID") # first column
    table_columns = table.loc[
        :, table.columns.isin(columns_sequence)
    ]
    table_sequence = table_columns[[*columns_sequence]]
    # Report.
    if report:
        utility.print_terminal_partition(level=2)
        print("... phenotype covariate table in format for PLINK ...")
        print("table shape: " + str(table_sequence.shape))
        print(table_sequence)
        utility.print_terminal_partition(level=4)
    # Return information.
    return table_sequence


def organize_phenotype_covariate_tables_alcoholism(
    binary_phenotypes=None,
    tables=None,
    report=None,
):
    """
    Organize table for phenotypes and covariates in format for PLINK.

    arguments:
        binary_phenotypes (list<str>): names of columns with binary phenotypes
            (control: 0, case: 1) that need conversion to PLINK format
            (control: 1, case: 2)
        tables (dict<object>): collection of Pandas data frames with
            information about genotype and phenotype variables across cohorts
            of persons
        report (bool): whether to print reports

    raises:

    returns:
        (dict<object>): collection of Pandas data frames with
            information about genotype and phenotype variables across cohorts
            of persons

    """

    # Initialize collection.
    pail = dict()
    # Organize format.
    pail["oestradiol"] = organize_phenotype_covariate_table_plink_format(
        binary_phenotypes=binary_phenotypes,
        table=tables["oestradiol"],
        report=report,
    )
    pail["testosterone"] = organize_phenotype_covariate_table_plink_format(
        binary_phenotypes=binary_phenotypes,
        table=tables["testosterone"],
        report=report,
    )
    # Return information.
    return pail


def organize_phenotype_covariate_tables_sex(
    tables=None,
    report=None,
):
    """
    Organize table for phenotypes and covariates in format for PLINK.

    1. Remove any rows with missing, empty values.
    PLINK cannot accommodate rows with empty cells.

    2. Introduce family identifiers.
    Family (FID) and individual (IID) identifiers must match the ID_1 and ID_2
    columns in the sample table.

    3. Sort column sequence.
    PLINK requires FID and IID columns to come first.

    arguments:
        tables (dict<dict<object>>): collection of Pandas data frames with
            information about genotype and phenotype variables across cohorts
            of persons
        report (bool): whether to print reports

    raises:

    returns:
        (dict<dict<object>>): collection of Pandas data frames with
            information about genotype and phenotype variables across cohorts
            of persons

    """

    # Initialize collection.
    pail = dict()
    # Convert format.
    pail["alcoholism_1"] = organize_phenotype_covariate_tables_alcoholism(
        binary_phenotypes=["alcoholism_1"],
        tables=tables["alcoholism_1"],
        report=report,
    )
    pail["alcoholism_2"] = organize_phenotype_covariate_tables_alcoholism(
        binary_phenotypes=["alcoholism_2"],
        tables=tables["alcoholism_2"],
        report=report,
    )
    pail["alcoholism_3"] = organize_phenotype_covariate_tables_alcoholism(
        binary_phenotypes=["alcoholism_3"],
        tables=tables["alcoholism_3"],
        report=report,
    )
    pail["alcoholism_4"] = organize_phenotype_covariate_tables_alcoholism(
        binary_phenotypes=["alcoholism_4"],
        tables=tables["alcoholism_4"],
        report=report,
    )
    # Return information.
    return pail


def organize_phenotype_covariate_tables_plink_format(
    tables=None,
    report=None,
):
    """
    Organize table for phenotypes and covariates in format for PLINK.

    1. Remove any rows with missing, empty values.
    PLINK cannot accommodate rows with empty cells.

    2. Introduce family identifiers.
    Family (FID) and individual (IID) identifiers must match the ID_1 and ID_2
    columns in the sample table.

    3. Sort column sequence.
    PLINK requires FID and IID columns to come first.

    arguments:
        tables (dict<dict<object>>): collection of Pandas data frames with
            information about genotype and phenotype variables across cohorts
            of persons
        report (bool): whether to print reports

    raises:

    returns:
        (dict<dict<object>>): collection of Pandas data frames with
            information about genotype and phenotype variables across cohorts
            of persons

    """

    # Initialize collection.
    pail = dict()
    # Conver format.
    pail["female"] = organize_phenotype_covariate_tables_sex(
        tables=tables["female"],
        report=report,
    )
    pail["male"] = organize_phenotype_covariate_tables_sex(
        tables=tables["male"],
        report=report,
    )
    # Return information.
    return pail


def match_ukb_genotype_phenotype_sample_identifiers(
    table_phenotypes=None,
    table_ukb_samples=None,
    report=None,
):
    """
    Organize table of phenotypes and covariates for GWAS.

    arguments:
        table_phenotypes (object): Pandas data frame of information about UK
            Biobank phenotype variables
        table_ukb_samples (object): Pandas data frame of information about UK
            Biobank genotype samples
        report (bool): whether to print reports

    raises:

    returns:

    """

    # Copy data.
    table_phenotypes = table_phenotypes.copy(deep=True)
    table_ukb_samples = table_ukb_samples.copy(deep=True)
    # Report.
    if report:
        utility.print_terminal_partition(level=2)
        print("... before match ...")
        print(table_phenotypes)
        utility.print_terminal_partition(level=3)
        print(table_ukb_samples)
        utility.print_terminal_partition(level=3)
    # Select random identifiers.
    table_phenotypes["IID"].astype("string")
    table_phenotypes.set_index(
        "IID",
        drop=True,
        inplace=True,
    )
    table_ukb_samples["ID_1"].astype("string")
    table_ukb_samples.set_index(
        "ID_1",
        drop=True,
        inplace=True,
    )
    samples = table_ukb_samples.index.to_list()
    identifiers_random = random.sample(samples, 100)
    # Select table records for identifiers.
    table_phenotypes_match = table_phenotypes.loc[
        table_phenotypes.index.isin(identifiers_random), :
    ]
    table_ukb_samples_match = table_ukb_samples.loc[
        table_ukb_samples.index.isin(identifiers_random), :
    ]
    # Report.
    if report:
        utility.print_terminal_partition(level=2)
        print("... match IID's between phenotype and genotype ...")
        print(table_phenotypes_match)
        utility.print_terminal_partition(level=4)
        print(table_ukb_samples_match)
        utility.print_terminal_partition(level=4)
    pass






##########
# ... in progress...


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


def write_product_quality(
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
    path_table_auditc = os.path.join(
        path_parent, "table_auditc.tsv"
    )
    path_table_audit = os.path.join(
        path_parent, "table_audit.tsv"
    )
    path_table_diagnosis = os.path.join(
        path_parent, "table_diagnosis.tsv"
    )
    path_table_alcoholism = os.path.join(
        path_parent, "table_alcoholism.tsv"
    )
    # Write information to file.
    information["table_auditc"].to_csv(
        path_or_buf=path_table_auditc,
        sep="\t",
        header=True,
        index=False,
    )
    information["table_audit"].to_csv(
        path_or_buf=path_table_audit,
        sep="\t",
        header=True,
        index=False,
    )
    information["table_diagnosis"].to_csv(
        path_or_buf=path_table_diagnosis,
        sep="\t",
        header=True,
        index=False,
    )
    information["table_alcoholism"].to_csv(
        path_or_buf=path_table_alcoholism,
        sep="\t",
        header=True,
        index=False,
    )
    pass


def write_product_cohorts_sex_alcoholism_hormone(
    sex_text=None,
    alcoholism=None,
    hormone=None,
    information=None,
    path_parent=None,
):
    """
    Writes product information to file.

    arguments:
        sex_text (str): textual representation of sex selection
        alcoholism (str): name of column defining alcoholism cases and controls
        hormone (str): name of column for relevant sex hormone
        information (object): information to write to file
        path_parent (str): path to parent directory

    raises:

    returns:

    """

    # Specify directories and files.
    path_table = os.path.join(
        path_parent[sex_text][alcoholism][hormone],
        "table_phenotypes_covariates.tsv"
    )
    # Write information to file.
    information[sex_text][alcoholism][hormone].to_csv(
        path_or_buf=path_table,
        sep="\t",
        header=True,
        index=False,
    )
    pass


def write_product_cohorts(
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

    sexes = ["female", "male",]
    alcoholisms = [
        "alcoholism_1", "alcoholism_2", "alcoholism_3", "alcoholism_4",
    ]
    hormones = ["oestradiol", "testosterone",]
    for sex in sexes:
        for alcoholism in alcoholisms:
            for hormone in hormones:
                write_product_cohorts_sex_alcoholism_hormone(
                    sex_text=sex,
                    alcoholism=alcoholism,
                    hormone=hormone,
                    information=information,
                    path_parent=path_parent,
                )
    pass


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
        index=False,
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

    # Quality control reports.
    write_product_quality(
        information=information["quality"],
        path_parent=paths["quality"],
    )
    # Cohort tables in PLINK format.
    write_product_cohorts(
        information=information["cohorts"],
        path_parent=paths["cohorts"],
    )

    # Trial organization.
    if False:
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
    # Organize information about general attributes.
    table_attribute = organize_general_attribute_variables(
        table=source["table_assembly"],
        report=True,
    )
    # Organize information about genotype principal components.
    table_genotype = organize_genotype_principal_component_variables(
        table=table_attribute,
        report=True,
    )
    # Organize information about hormones.
    table_hormone = organize_sex_hormone_variables(
        table=table_genotype,
        report=True,
    )
    # Organize information about alcohol consumption.
    pail_alcohol_consumption = organize_alcohol_consumption_variables(
        table=table_hormone,
        report=True,
    )
    print(pail_alcohol_consumption["quantity"]["table_clean"])
    # Organize Alchol Use Disorders Identification Test (AUDIT) and
    # AUDIT-Concise (AUDIT-C) questionnaire scores.
    pail_audit = organize_alcohol_audit_questionnaire_variables(
        table=pail_alcohol_consumption["quantity"]["table_clean"],
        report=True,
    )
    print(pail_audit["audit"]["table_clean"])

    # Organize International Classification of Disease (ICD) ICD9 and ICD10
    # codes for diagnoses relevant to alcoholism.
    # Organize codes for self diagnoses relevant to alcoholism.
    pail_diagnosis = organize_alcoholism_diagnosis_variables(
        table=pail_audit["audit"]["table_clean"],
        report=True,
    )
    print(pail_diagnosis["table_clean"])

    # Organize alcoholism cases and controls.
    # Report females and males who consume alcohol and are candidates for
    # either controls or cases of alcoholism.
    pail_alcoholism = organize_alcoholism_cases_controls_variables(
        table=pail_diagnosis["table_clean"],
        report=True,
    )
    print(pail_alcoholism["table_clean"])

    # Select and organize variables across cohorts.
    pail_cohorts = select_organize_cohorts_variables_by_sex_alcoholism_hormone(
        table=pail_alcoholism["table_clean"],
        report=True,
    )

    # Organize phenotypes and covariates in format for analysis in PLINK.
    pail_format = organize_phenotype_covariate_tables_plink_format(
        tables=pail_cohorts,
        report=True,
    )

    # Collect information.
    information = dict()
    information["quality"] = dict()
    information["quality"]["table_auditc"] = (
        pail_audit["auditc"]["table_report"]
    )
    information["quality"]["table_audit"] = (
        pail_audit["audit"]["table_report"]
    )
    information["quality"]["table_diagnosis"] = (
        pail_diagnosis["table_report"]
    )
    information["quality"]["table_alcoholism"] = (
        pail_alcoholism["table_report"]
    )
    information["cohorts"] = pail_format
    # Write product information to file.
    write_product(
        paths=paths,
        information=information
    )

    if False:
        # Match UKB genotype sample identifiers to phenotype identifiers.
        match_ukb_genotype_phenotype_sample_identifiers(
            table_phenotypes=table_format,
            table_ukb_samples=source["table_ukb_samples"],
            report=True,
        )

        # Collect information.
        information = dict()
        information["trial"] = dict()
        information["trial"]["table_phenotypes_covariates"] = (
            table_format
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
