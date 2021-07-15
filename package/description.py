
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
    paths["description"] = os.path.join(path_dock, "description")
    paths["export"] = os.path.join(
        path_dock, "description", "export"
    )
    paths["plots"] = os.path.join(
        path_dock, "description", "plots"
    )

    # Remove previous files to avoid version or batch confusion.
    if restore:
        utility.remove_directory(path=paths["description"])
    # Initialize directories.
    utility.create_directories(
        path=paths["description"]
    )
    utility.create_directories(
        path=paths["export"]
    )
    utility.create_directories(
        path=paths["plots"]
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



##########
# Data export


def organize_hormone_female_export_table(
    table=None,
    select_columns=None,
    report=None,
):
    """
    Organizes information for export.

    arguments:
        table (object): Pandas data frame of phenotype variables across UK
            Biobank cohort
        select_columns (bool): whether to select specific columns from table
        report (bool): whether to print reports

    raises:

    returns:
        (object): Pandas data frame of phenotype variables across UK Biobank

    """

    table = table.copy(deep=True)
    if (select_columns):
        columns_export = [
            #"eid",
            "IID",
            "sex", "sex_text", "age", "body_mass_index", "body_mass_index_log",
            "pregnancy",
            "hysterectomy", "oophorectomy", "hysterectomy_or_oophorectomy",
            "menopause_binary", "menopause_ordinal",
            "menstruation_days", "menstruation_phase",
            "oral_contraception", "hormone_replacement",
            "hormone_alteration",
            "albumin", "albumin_log", "steroid_globulin", "steroid_globulin_log",
            "oestradiol", "oestradiol_log",
            "oestradiol_free", "oestradiol_free_log",
            "oestradiol_bioavailable", "oestradiol_bioavailable_log",
            "testosterone", "testosterone_log",
            "testosterone_free", "testosterone_free_log",
            "testosterone_bioavailable", "testosterone_bioavailable_log",

        ]
        table = table.loc[
            :, table.columns.isin(columns_export)
        ]
        table = table[[*columns_export]]
    # Report.
    if report:
        # Column name translations.
        utility.print_terminal_partition(level=2)
        print("report: organize_hormone_export_table()")
        utility.print_terminal_partition(level=3)
        print(table)
        print("table shape (rows, columns): " + str(table.shape))
        print(table.columns.to_list())
    # Return information.
    return table




##########
# Write



def write_product_export_table(
    name=None,
    information=None,
    path_parent=None,
):
    """
    Writes product information to file.

    arguments:
        name (str): base name for file
        information (object): information to write to file
        path_parent (str): path to parent directory

    raises:

    returns:

    """

    # Specify directories and files.
    path_table = os.path.join(
        path_parent, str(name + ".tsv")
    )
    # Write information to file.
    information.to_csv(
        path_or_buf=path_table,
        sep="\t",
        header=True,
        index=True,
    )
    pass


def write_product_export(
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

    for name in information.keys():
        write_product_export_table(
            name=name,
            information=information[name],
            path_parent=path_parent,
        )
    pass


def write_product_plot_figure(
    name=None,
    figure=None,
    path_parent=None,
):
    """
    Writes product information to file.

    arguments:
        name (str): base name for file
        figure (object): figure object to write to file
        path_parent (str): path to parent directory

    raises:

    returns:

    """

    # Specify directories and files.
    path_file = os.path.join(
        path_parent, str(name + ".png")
    )
    # Write information to file.
    plot.write_figure(
        figure=figure,
        format="png",
        resolution=300,
        path=path_file,
    )
    pass


def write_product_plots(
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

    for name in information.keys():
        write_product_plot_figure(
            name=name,
            figure=information[name],
            path_parent=path_parent,
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

    # Export information.
    write_product_export(
        information=information["export"],
        path_parent=paths["export"],
    )
    # Plots.
    write_product_plots(
        information=information["plots"],
        path_parent=paths["plots"],
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
    print("version check: 1")
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

    # Describe variables within cohorts and models.
    pail_summary = (
        ukb_organization.execute_describe_cohorts_models_phenotypes(
            table=source["table_phenotypes"],
            set="sex_hormones",
            path_dock=path_dock,
            report=True,
    ))

    # Plot figures for cohorts, models, and phenotypes.
    pail_plot = ukb_organization.execute_plot_cohorts_models_phenotypes(
        table=source["table_phenotypes"],
        report=True,
    )

    # Organize information for export.
    table_hormone_female_export = organize_hormone_female_export_table(
        table=source["table_phenotypes"],
        select_columns=False,
        report=True,
    )

    # Collect information.
    information = dict()
    information["export"] = dict()
    information["export"]["table_hormone_female_export"] = (
        table_hormone_female_export
    )
    information["export"]["table_summary_cohorts_models_phenotypes"] = (
        pail_summary["table_summary_cohorts_models_phenotypes"]
    )
    information["export"]["table_summary_cohorts_models_genotypes"] = (
        pail_summary["table_summary_cohorts_models_genotypes"]
    )
    information["plots"] = pail_plot
    # Write product information to file.
    write_product(
        paths=paths,
        information=information
    )
    pass


if (__name__ == "__main__"):
    execute_procedure()
