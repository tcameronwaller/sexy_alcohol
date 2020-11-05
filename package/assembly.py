
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


def read_ukbiobank_data_column_names(
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
    column_names = line.split("\t")
    # Return information.
    return column_names


def extract_organize_variables_types(
    data_ukbiobank_variables=None,
    extra_pairs=None,
):
    """
    Organize information about data types of UK Biobank phenotype variables.

    arguments:
        data_ukbiobank_variables (object): Pandas data frame of information
            about UK Biobank phenotype variables
        extra_pairs (dict<str>): extra key value pairs to include

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
    variables_types.update(extra_pairs)
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
        path_dock, "access", "ukb41826.raw.csv"
    )
    path_data_ukb_43878 = os.path.join(
        path_dock, "access", "ukb43878.raw.csv"
    )
    # Determine variable types.
    data_ukbiobank_variables = pandas.read_csv(
        path_data_ukbiobank_variables,
        sep="\t",
        header=0,
    )
    variables_types = extract_organize_variables_types(
        data_ukbiobank_variables=data_ukbiobank_variables,
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
    data_identifier_pairs = pandas.read_csv(
        path_data_identifier_pairs,
        sep=",",
        header=0,
        dtype="string",
    )
    # Designate variable types to conserve memory.
    column_names = read_ukbiobank_data_column_names(
        path_file=path_data_ukb_41826,
        delimiter=",", # "," or "\t"
        start=0,
        stop=1,
    )
    row_values = read_ukbiobank_data_column_names(
        path_file=path_data_ukb_41826,
        delimiter=",", # "," or "\t"
        start=1,
        stop=2,
    )
    # Report.
    if report:
        utility.print_terminal_partition(level=2)
        print(column_names)
        print(len(column_names))
        utility.print_terminal_partition(level=2)
        print(row_values)
        print(len(row_values))
        utility.print_terminal_partition(level=2)
    data_ukb_41826 = pandas.read_csv(
        path_data_ukb_41826,
        sep=",", # "," or "\t"
        header=0,
        dtype=variables_types,
        na_values=["<NA>"],
        keep_default_na=True,
    )
    data_ukb_43878 = pandas.read_csv(
        path_data_ukb_43878,
        sep=",", # "," or "\t"
        header=0,
        dtype=variables_types,
        na_values=["<NA>"],
        keep_default_na=True,
    )
    # Compile and return information.
    return {
        "data_ukbiobank_variables": data_ukbiobank_variables,
        "exclusion_identifiers": exclusion_identifiers,
        "data_identifier_pairs": data_identifier_pairs,
        "data_ukb_41826": data_ukb_41826,
        "data_ukb_43878": data_ukb_43878,
    }


def extract_organize_variable_fields_instances_names(
    data_ukbiobank_variables=None,
    extra_names=None,
):
    """
    Organizes column names for variable fields and instances.

    arguments:
        data_ukbiobank_variables (object): Pandas data frame of information
            about UK Biobank phenotype variables
        extra_names (list<str>): extra names to include

    raises:

    returns:
        (list<str>): column names for variable fields and instances

    """

    # Copy data.
    data_variables = data_ukbiobank_variables.copy(deep=True)
    # Organize information.
    data_variables = data_variables.loc[
        :, data_variables.columns.isin(["field", "instances_keep"])
    ]
    records = utility.convert_dataframe_to_records(data=data_variables)
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


def remove_data_irrelevant_variable_instances_entries(
    data_ukbiobank_variables=None,
    data_ukb_41826=None,
    data_ukb_43878=None,
    report=None,
):
    """
    Removes irrelevant columns and rows from data.

    arguments:
        data_ukbiobank_variables (object): Pandas data frame of information
            about UK Biobank phenotype variables
        data_ukb_41826 (object): Pandas data frame of variables from UK Biobank
            phenotype accession 41826
        data_ukb_43878 (object): Pandas data frame of variables from UK Biobank
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
        print("data_ukb_41826 shape: " + str(data_ukb_41826.shape))
        utility.print_terminal_partition(level=4)
        print("data_ukb_43878 shape: " + str(data_ukb_43878.shape))

    # Extract names of columns for relevant variable fields and instances.
    column_names = extract_organize_variable_fields_instances_names(
        data_ukbiobank_variables=data_ukbiobank_variables,
        extra_names=["IID", "eid"],
    )
    print(column_names)
    # Remove all irrelevant columns.
    data_ukb_41826 = data_ukb_41826.loc[
        :, data_ukb_41826.columns.isin(column_names)
    ]
    data_ukb_43878 = data_ukb_43878.loc[
        :, data_ukb_43878.columns.isin(column_names)
    ]
    # Remove rows with all missing values.
    data_ukb_41826.dropna(
        axis="index",
        how="all",
        inplace=True,
    )
    data_ukb_41826.dropna(
        axis="index",
        how="any",
        subset=["eid"],
        inplace=True,
    )
    data_ukb_43878.dropna(
        axis="index",
        how="all",
        inplace=True,
    )
    data_ukb_43878.dropna(
        axis="index",
        how="any",
        subset=["eid"],
        inplace=True,
    )
    # Report.
    if report:
        utility.print_terminal_partition(level=2)
        print("...after pruning...")
        print("data_ukb_41826 shape: " + str(data_ukb_41826.shape))
        utility.print_terminal_partition(level=4)
        print("data_ukb_43878 shape: " + str(data_ukb_43878.shape))

    # Compile and return information.
    bucket = dict()
    bucket["data_ukb_41826"] = data_ukb_41826
    bucket["data_ukb_43878"] = data_ukb_43878
    return bucket


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
        (object): Pandas data frame of phenotype variables across UK Biobank
            cohort

    """

    # Report.
    if report:
        utility.print_terminal_partition(level=2)
        print(data_identifier_pairs)
        utility.print_terminal_partition(level=2)
        print(data_ukb_41826)
        utility.print_terminal_partition(level=2)
        print(data_ukb_43878)
    # Organize data.
    print(data_identifier_pairs.dtypes)
    data_identifier_pairs.astype("string")
    print(data_identifier_pairs.dtypes)
    data_identifier_pairs.set_index(
        "eid",
        drop=True,
        inplace=True,
    )
    print(data_ukb_41826.dtypes)
    data_ukb_41826["eid"].astype("string")
    print(data_ukb_41826.dtypes)
    data_ukb_41826.set_index(
        "eid",
        drop=True,
        inplace=True,
    )
    print(data_ukb_43878.dtypes)
    data_ukb_43878["eid"].astype("string")
    print(data_ukb_43878.dtypes)
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
        print(data_merge)
    # Return information.
    return data_merge


def exclude_persons_ukbiobank_consent(
    exclusion_identifiers=None,
    data=None,
    report=None,
):
    """
    Removes entries with specific identifiers from data.

    arguments:
        exclusion_identifiers (list<str>): identifiers of persons who withdrew
            consent from UK Biobank
        data (object): Pandas data frame of phenotype variables across UK
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
        print("Initial data dimensions: " + str(data.shape))
        utility.print_terminal_partition(level=4)
        print("Exclusion of persons: " + str(len(exclusion_identifiers)))
    # Copy data.
    data = data.copy(deep=True)
    # Filter data entries.
    data_exclusion = data.loc[
        ~data.index.isin(exclusion_identifiers), :
    ]
    # Report.
    if report:
        utility.print_terminal_partition(level=4)
        print("Final data dimensions: " + str(data_exclusion.shape))
    # Return information.
    return data_exclusion


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
    # Determine whether all relevant variables have missing values.
    valid = False
    for type in types:
        if ((type != -1) and (type != -3)):
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
    elif (not math.isnan(alcohol_monthly)):
        alcohol_drinks_monthly = drinks_monthly
    else:
        # There is no valid information about alcohol consumption quantity.
        alcohol_drinks_monthly = float("nan")
        pass
    return alcohol_drinks_monthly


def determine_total_alcohol_consumption_monthly(
    status=None,
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
        status (str): person's status of alcohol consumption
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
    if (not pandas.isna(status)):
        if (-0.5 < status and status < 0.5):
            # Confirm that alcohol consumption is none.
            if (not math.isnan(alcohol_monthly)):
                alcohol_drinks_monthly = alcohol_monthly
            else:
                alcohol_drinks_monthly = 0.0
            pass
        elif (
            (1.5 < status and status < 2.5) or
            (0.5 < status and status < 1.5) or
            (-3.5 < status and status < -2.5)
        ):
            # Determine alcohol consumption quantity.
            alcohol_drinks_monthly = alcohol_monthly
            pass
        else:
            print("****************************")
            print("alcohol status not missing but weird")
            print(status)
            print(type(status))
            alcohol_drinks_monthly = alcohol_monthly
    else:
        print("****************************")
        print("alcohol status missing")
        print(status)
        print(type(status))
        alcohol_drinks_monthly = alcohol_monthly
        pass
    # Return information.
    return alcohol_drinks_monthly


def organize_alcohol_consumption_monthly_drinks(
    data=None,
    report=None,
):
    """
    Organizes information about alcohol consumption in standard drinks monthly.

    arguments:
        data (object): Pandas data frame of phenotype variables across UK
            Biobank cohort
        report (bool): whether to print reports

    raises:

    returns:
        (object): Pandas data frame of phenotype variables across UK Biobank
            cohort

    """

    # Copy data.
    data = data.copy(deep=True)
    utility.print_terminal_partition(level=1)
    print(data["20117-0.0"].value_counts())
    print(data["20117-0.0"].dtypes)
    utility.print_terminal_partition(level=2)
    data["20117-0.0"] = pandas.to_numeric(
        data["20117-0.0"],
        errors="coerce",
        downcast="float",
    )
    if False:
        data["20117-0.0"].fillna(
            value="-3",
            axis="index",
            inplace=True,
        )
        data["20117-0.0"].astype(
            "float32",
            copy=True,
        )
    print(data["20117-0.0"].value_counts())
    print(data["20117-0.0"].dtypes)
    utility.print_terminal_partition(level=2)

    # Calculate sum of drinks weekly.
    data["drinks_weekly"] = data.apply(
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
    data["drinks_monthly"] = data.apply(
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
    data["alcohol_drinks_monthly"] = data.apply(
        lambda row:
            determine_total_alcohol_consumption_monthly(
                status=row["20117-0.0"],
                drinks_weekly=row["drinks_weekly"],
                drinks_monthly=row["drinks_monthly"],
                weeks_per_month=4.345, # 52.143 weeks per year (12 months)
            ),
        axis="columns", # apply across rows
    )
    # Remove columns for variables that are not necessary anymore.
    data_clean = data.copy(deep=True)
    data_clean.drop(
        labels=[
            "1588-0.0", "1568-0.0", "1578-0.0", "1608-0.0", "1598-0.0",
            "5364-0.0",
            "4429-0.0", "4407-0.0", "4418-0.0", "4451-0.0", "4440-0.0",
            "4462-0.0",
            #"20117-0.0",
            #"drinks_weekly",
            #"drinks_monthly",
        ],
        axis="columns",
        inplace=True
    )
    # Report.
    if report:
        # Copy data.
        data_report = data.copy(deep=True)
        # Organize data for report.
        data_report = data_report.loc[
            :, data_report.columns.isin([
                "eid", "IID",
                "1588-0.0", "1568-0.0", "1578-0.0", "1608-0.0", "1598-0.0",
                "5364-0.0",
                "4429-0.0", "4407-0.0", "4418-0.0", "4451-0.0", "4440-0.0",
                "4462-0.0",
                "20117-0.0",
                "drinks_weekly",
                "drinks_monthly",
                "alcohol_drinks_monthly",
            ])
        ]
        utility.print_terminal_partition(level=2)
        print("Summary of alcohol consumption quantity variables: ")
        print(data_report)
    # Return information.
    return data_clean



# TODO: organize AUDIT-C variables... sum of AUDIT-C questions 1-3
# TODO: handle the specific missing value codes




# TODO: derive "hysterectomy" and "oophrectomy" separately
# TODO: then derive "menopause"

def organize_female_menopause(
    data=None,
    report=None,
):
    """
    Organizes information about whether female persons have experienced
    menopause.

    arguments:
        data (object): Pandas data frame of phenotype variables across UK
            Biobank cohort
        report (bool): whether to print reports

    raises:

    returns:
        (object): Pandas data frame of phenotype variables across UK Biobank
            cohort

    """

    # Copy data.
    data = data.copy(deep=True)
    # Calculate sum of drinks weekly.
    data["menopause"] = data.apply(
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
    data["hysterectomy"] = data.apply(
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
    data["oophorectomy"] = data.apply(
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
        print("Final data dimensions: " + str(data_exclusion.shape))
    # Return information.
    return data_exclusion







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
    print("version check: 5")

    # Read source information from file.
    # Exclusion identifiers are "eid".
    source = read_source(
        path_dock=path_dock,
        report=True,
    )
    # Remove data columns for irrelevant variable instances.
    prune = remove_data_irrelevant_variable_instances_entries(
        data_ukbiobank_variables=source["data_ukbiobank_variables"],
        data_ukb_41826=source["data_ukb_41826"],
        data_ukb_43878=source["data_ukb_43878"],
        report=True,
    )
    # Merge tables.
    data_raw = merge_data_variables_identifiers(
        data_identifier_pairs=source["data_identifier_pairs"],
        data_ukb_41826=prune["data_ukb_41826"],
        data_ukb_43878=prune["data_ukb_43878"],
        report=True,
    )
    # Exclude persons who withdrew consent from the UK Biobank.
    data_exclusion = exclude_persons_ukbiobank_consent(
        exclusion_identifiers=source["exclusion_identifiers"],
        data=data_raw,
        report=True,
    )
    # Derive total monthly alcohol consumption in standard UK drinks.
    data_consumption = organize_alcohol_consumption_monthly_drinks(
        data=data_exclusion,
        report=True,
    )


    # TODO: 2) derive alcohol consumption quantity and frequency variables
    # TODO: 3) organize menopause variable


    # Organize general phenotypes.

    # Organize genotype principal components.

    # Organize alcohol phenotypes.

    pass



if (__name__ == "__main__"):
    execute_procedure()
