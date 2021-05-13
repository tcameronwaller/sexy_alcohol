
"""
...

This module collects and organizes information about heritability estimates for
metabolites.

Source of GWAS summary statistics is Shin et al, Nature Genetics, 2014
(PubMed:24816252). Metabolite identifiers are from Metabolon Inc.

Method for estimation of heritability from GWAS summary statistics was linkage
disequilibrium score (LDSC) regression in tool LD SCore
(https://github.com/bulik/ldsc).

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

###############################################################################
# Functionality


##########
# Initialization


def initialize_heritability_directories(
    heritability_studies=None,
    paths=None,
    path_dock=None,
    restore=None,
):
    """
    Initialize directories for procedure's product files.

    arguments:
        heritability_studies (list<str>): identifiers of studies with
            heritability reports
        paths (dict<str>): collection of paths to directories for procedure's
            files
        path_dock (str): path to dock directory for source and product
            directories and files
        restore (bool): whether to remove previously existing directories

    raises:

    returns:
        (dict<str>): collection of paths to directories for procedure's files

    """

    paths = copy.deepcopy(paths)
    paths["heritability"] = os.path.join(
        path_dock, "heritability",
    )
    paths["heritability_studies"] = dict()
    for study in heritability_studies:
        paths["heritability_studies"][study] = os.path.join(
            path_dock, "heritability", study
        )
    return paths


def initialize_correlation_directories(
    primary_studies=None,
    secondary_studies=None,
    paths=None,
    path_dock=None,
    restore=None,
):
    """
    Initialize directories for procedure's product files.

    arguments:
        primary_studies (list<str>): identifiers of studies for primary
            phenotypes, first in correlation hierarchy
        secondary_studies (list<str>): identifiers of studies for secondary
            phenotypes, second in correlation hierarchy
        paths (dict<str>): collection of paths to directories for procedure's
            files
        path_dock (str): path to dock directory for source and product
            directories and files
        restore (bool): whether to remove previously existing directories

    raises:

    returns:
        (dict<str>): collection of paths to directories for procedure's files

    """

    paths = copy.deepcopy(paths)
    paths["genetic_correlation"] = os.path.join(
        path_dock, "genetic_correlation",
    )
    paths["correlation_studies"] = dict()
    for study_first in primary_studies:
        for study_second in secondary_studies:
            paths["correlation_studies"][study_first] = dict()
            paths["correlation_studies"][study_first][study_second] = (
                os.path.join(
                    path_dock, "genetic_correlation",
                    study_first, study_second
                )
            )
    return paths


def initialize_directories(
    primary_study=None,
    secondary_study=None,
    restore=None,
    path_dock=None,
):
    """
    Initialize directories for procedure's product files.

    arguments:
        primary_study (str): identifier of primary study, consisting of a single
            GWAS
        secondary_study (str): identifier of secondary study, consisting of
            multiple GWASes
        restore (bool): whether to remove previously existing directories
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
    heritability_studies = [
        primary_study,
        secondary_study,
    ]
    primary_studies = [
        primary_study,
    ]
    secondary_studies = [
        secondary_study,
    ]
    paths = initialize_heritability_directories(
        heritability_studies=heritability_studies,
        paths=paths,
        path_dock=path_dock,
        restore=restore,
    )
    paths = initialize_correlation_directories(
        primary_studies=primary_studies,
        secondary_studies=secondary_studies,
        paths=paths,
        path_dock=path_dock,
        restore=restore,
    )
    # Return information.
    return paths


##########
# Read


def read_extract_phenotype_heritability(
    file=None,
    file_suffix=None,
    path_source_directory=None,
):
    """
    Reads and extracts information from log of LDSC for heritability estimation
    from GWAS summary statistics.

    arguments:
        file (str): name of a file
        file_suffix (str): file name suffix to recognize relevant files and to
            extract identifier
        path_source_directory (str): path to source parent directory for files
            with heritability estimations for phenotype

    raises:

    returns:
        (dict): information about estimation of a phenotype's heritability

    """

    # Extract metabolite's identifier.
    identifier = str(
        file.replace(str(file_suffix), "")
    )
    # Define path to file.
    path_file = os.path.join(
        path_source_directory, file
    )
    # Initialize variables.
    variants = float("nan")
    heritability = float("nan")
    heritability_error = float("nan")
    ratio = float("nan")
    ratio_error = float("nan")
    # Read relevant lines from file.
    lines = utility.read_file_text_lines(
        path_file=path_file,
        start=22,
        stop=30,
    )
    # Extract information from lines.
    prefix_variants = "After merging with regression SNP LD, "
    suffix_variants = " SNPs remain."
    prefix_heritability = "Total Observed scale h2: "
    prefix_ratio = "Ratio: "
    for line in lines:
        if prefix_variants in line:
            variants = float(
                line.replace(prefix_variants, "").replace(suffix_variants, "")
            )
        elif prefix_heritability in line:
            content = line.replace(prefix_heritability, "")
            contents = content.split(" (")
            heritability_test = contents[0]
            if (not "NA" in heritability_test):
                heritability = float(contents[0])
                heritability_error = float(contents[1].replace(")", ""))
            pass
        elif (
            (not math.isnan(heritability)) and
            (prefix_ratio in line)
        ):
            content = line.replace(prefix_ratio, "")
            contents = content.split(" (")
            ratio_test = contents[0]
            if (not "NA" in ratio_test):
                ratio = float(contents[0])
                ratio_error = float(
                    contents[1].replace(")", "")
                )
            pass
        pass
    # Collect information.
    record = dict()
    record["identifier"] = identifier
    record["heritability_variants"] = variants
    record["heritability"] = heritability
    record["heritability_standard_error"] = heritability_error
    record["heritability_ratio"] = ratio
    record["heritability_ratio_standard_error"] = ratio_error
    # Return information.
    return record


def read_collect_phenotypes_heritabilities_by_files(
    file_suffix=None,
    path_source_directory=None,
):
    """
    Reads, collects, and organizes heritability estimates across phenotypes.

    arguments:
        file_suffix (str): file name suffix to recognize relevant files and to
            extract identifier
        path_source_directory (str): path to source directory that contains
            files with heritability estimations for phenotypes

    raises:

    returns:
        (object): Pandas data frame of metabolites' heritability estimates

    """

    # Collect names of files for metabolites' heritabilities.
    files = utility.extract_directory_file_names(path=path_source_directory)
    files_relevant = list(filter(
        lambda content: (str(file_suffix) in content), files
    ))
    records = list()
    for file in files_relevant:
        record = read_extract_phenotype_heritability(
            file=file,
            file_suffix=file_suffix,
            path_source_directory=path_source_directory,
        )
        records.append(record)
        pass
    # Organize heritability table.
    table = utility.convert_records_to_dataframe(
        records=records
    )
    table.sort_values(
        by=["heritability"],
        axis="index",
        ascending=False,
        inplace=True,
    )
    table.reset_index(
        level=None,
        inplace=True
    )
    table["identifier"].astype("string")
    table.set_index(
        "identifier",
        drop=True,
        inplace=True,
    )
    # Return information.
    return table


def read_collect_phenotypes_heritabilities_by_directories(
    file=None,
    path_parent_directory=None,
):
    """
    Reads, collects, and organizes heritability estimates across phenotypes.

    arguments:
        file (str): name of a file
        path_parent_directory (str): path to source parent directory for files
            with heritability estimations for metabolites

    raises:

    returns:
        (object): Pandas data frame of metabolites' heritability estimates

    """

    # Collect names of child directories within the parent directory.
    child_directories = utility.extract_subdirectory_names(
        path=path_parent_directory
    )
    # Filter child directories to those that contain relevant files.
    child_directories_relevant = list()
    for child_directory in child_directories:
        path_file = os.path.join(
            path_parent_directory, child_directory, file,
        )
        if os.path.isfile(path_file):
            child_directories_relevant.append(child_directory)
    # Collect and organize phenotype heritabilities.
    records = list()
    for child_directory in child_directories_relevant:
        path_child_directory = os.path.join(
            path_parent_directory, child_directory,
        )
        record = read_extract_phenotype_heritability(
            file=file,
            file_suffix="",
            path_source_directory=path_child_directory,
        )
        # Set name of cohort and hormone.
        record["identifier"] = child_directory
        records.append(record)
        pass
    # Organize heritability table.
    table = utility.convert_records_to_dataframe(
        records=records
    )
    table.sort_values(
        by=["heritability"],
        axis="index",
        ascending=False,
        inplace=True,
    )
    table.reset_index(
        level=None,
        inplace=True
    )
    table["identifier"].astype("string")
    table.set_index(
        "identifier",
        drop=True,
        inplace=True,
    )
    # Return information.
    return table


def read_extract_primary_secondary_genetic_correlation(
    file=None,
    file_suffix=None,
    path_source_directory=None,
):
    """
    Reads and extracts information from log of LDSC for estimation of
    genetic correlation between a phenotype of interest and a metabolite.

    phenotype 1: phenotype of interest compared accross all metabolites
    phenotype 2: single metabolite of interest

    arguments:
        file (str): name of a file
        file_suffix (str): file name suffix to recognize relevant files and to
            extract identifier
        path_source_directory (str): path to source parent directory for files
            with genetic correlation estimations for metabolites

    raises:

    returns:
        (dict): information about estimation of a metabolite's genetic
            correlation to phenotype

    """

    # Extract metabolite's identifier.
    identifier = str(
        file.replace(str(file_suffix), "")
    )
    # Define path to file.
    path_file = os.path.join(
        path_source_directory, file
    )
    # Initialize variables.
    variants = float("nan")
    correlation = float("nan")
    correlation_error = float("nan")
    correlation_absolute = float("nan")
    probability = float("nan")
    # Read relevant lines from file.
    lines = utility.read_file_text_lines(
        path_file=path_file,
        start=25,
        stop=57,
    )
    # Extract information from lines.
    prefix_variants = ""
    suffix_variants = " SNPs with valid alleles."
    prefix_correlation = "Genetic Correlation: "
    prefix_probability = "P: "
    for line in lines:
        if suffix_variants in line:
            variants = float(
                line.replace(prefix_variants, "").replace(suffix_variants, "")
            )
        elif prefix_correlation in line:
            content = line.replace(prefix_correlation, "")
            contents = content.split(" (")
            correlation_test = contents[0]
            if (not "nan" in correlation_test):
                correlation = float(contents[0])
                correlation_absolute = math.fabs(correlation)
                correlation_error = float(contents[1].replace(")", ""))
            pass
        elif (
            (not math.isnan(correlation)) and
            (prefix_probability in line)
        ):
            probability = float(line.replace(prefix_probability, ""))
            pass
        pass
    # Collect information.
    record = dict()
    record["identifier"] = identifier
    record["correlation_variants"] = variants
    record["correlation"] = correlation
    record["correlation_standard_error"] = correlation_error
    record["correlation_absolute"] = correlation_absolute
    record["correlation_probability"] = probability
    # Return information.
    return record


def read_collect_primary_secondaries_genetic_correlations_by_files(
    file_suffix=None,
    path_source_directory=None,
):
    """
    Reads and collects estimations of genetic correlation between phenotype and
        metabolites.

    arguments:
        file_suffix (str): file name suffix to recognize relevant files and to
            extract identifier
        path_source_directory (str): path to source parent directory for files
            with genetic correlation estimations for metabolites

    raises:

    returns:
        (object): Pandas data frame of metabolites' heritability estimates

    """

    # Collect names of files for metabolites' heritabilities.
    files = utility.extract_directory_file_names(path=path_source_directory)
    files_relevant = list(filter(
        lambda content: (str(file_suffix) in content), files
    ))
    records = list()
    for file in files_relevant:
        record = read_extract_primary_secondary_genetic_correlation(
            file=file,
            file_suffix=file_suffix,
            path_source_directory=path_source_directory,
        )
        records.append(record)
        pass
    # Organize heritability table.
    table = utility.convert_records_to_dataframe(
        records=records
    )
    table.sort_values(
        by=["correlation_probability"],
        axis="index",
        ascending=True,
        na_position="last",
        inplace=True,
    )
    table.reset_index(
        level=None,
        inplace=True
    )
    table["identifier"].astype("string")
    table.set_index(
        "identifier",
        drop=True,
        inplace=True,
    )
    # Return information.
    return table


def read_collect_primary_secondaries_genetic_correlations_by_directories(
    file=None,
    path_parent_directory=None,
):
    """
    Reads and collects estimations of genetic correlation between phenotype and
        metabolites.

    arguments:
        file (str): name of a file
        path_parent_directory (str): path to source parent directory for files
            with heritability estimations for metabolites

    raises:

    returns:
        (object): Pandas data frame of metabolites' heritability estimates

    """

    # Collect names of child directories within the parent directory.
    child_directories = utility.extract_subdirectory_names(
        path=path_parent_directory
    )
    # Filter child directories to those that contain relevant files.
    child_directories_relevant = list()
    for child_directory in child_directories:
        path_file = os.path.join(
            path_parent_directory, child_directory, file,
        )
        if os.path.isfile(path_file):
            child_directories_relevant.append(child_directory)
    # Collect and organize phenotype genetic correlations.
    records = list()
    for child_directory in child_directories_relevant:
        path_child_directory = os.path.join(
            path_parent_directory, child_directory,
        )
        record = read_extract_primary_secondary_genetic_correlation(
            file=file,
            file_suffix="",
            path_source_directory=path_child_directory,
        )
        # Set name of cohort and hormone.
        record["identifier"] = child_directory
        records.append(record)
        pass
    # Organize heritability table.
    table = utility.convert_records_to_dataframe(
        records=records
    )
    table.sort_values(
        by=["correlation_probability"],
        axis="index",
        ascending=True,
        na_position="last",
        inplace=True,
    )
    table.reset_index(
        level=None,
        inplace=True
    )
    table["identifier"].astype("string")
    table.set_index(
        "identifier",
        drop=True,
        inplace=True,
    )
    # Return information.
    return table


def read_source(
    primary_study=None,
    secondary_study=None,
    paths=None,
    report=None,
):
    """
    Reads and organizes source information from file.

    arguments:
        primary_study (str): identifier of primary study, consisting of a single
            GWAS
        secondary_study (str): identifier of secondary study, consisting of
            multiple GWASes
        paths (dict<str>): collection of paths to directories for procedure's
            files
        report (bool): whether to print reports

    raises:

    returns:
        (object): source information

    """

    # Primary phenotype heritability.
    primary_heritability = read_extract_phenotype_heritability(
        file="heritability_report.log",
        file_suffix="",
        path_source_directory=paths["heritability_studies"][primary_study],
    )
    # Secondary phenotypes heritability table.
    table_secondary_heritability = (
        read_collect_phenotypes_heritabilities_by_directories(
            file="heritability_report.log",
            path_parent_directory=(
                paths["heritability_studies"][secondary_study]
            ),
    ))
    # Genetic correlations between primary and secondary phenotypes.
    table_correlations = (
        read_collect_primary_secondaries_genetic_correlations_by_directories(
            file="correlation.log",
            path_parent_directory=(
                paths["correlation_studies"][primary_study][secondary_study]
            ),
    ))

    # Report.
    if report:
        utility.print_terminal_partition(level=2)
        print(primary_heritability)
        print(table_secondary_heritability)
        print(table_correlations)
        utility.print_terminal_partition(level=2)
    # Compile and return information.
    return {
        "primary_heritability": primary_heritability,
        "table_secondary_heritability": table_secondary_heritability,
        "table_correlations": table_correlations,
    }


##########
# Summary


def combine_organize_phenotypes_summary_table(
    primary_heritability=None,
    table_secondary_heritability=None,
    table_correlations=None,
    threshold_secondary_heritability=None,
    threshold_false_discovery_rate=None,
    report=None,
):
    """
    Reads, collects, and organizes metabolite heritability estimates.

    arguments:
        primary_heritability (dict): information about estimation of a
            phenotype's heritability
        table_secondary_heritability (object): Pandas data frame of
            metabolites' heritability estimates
        table_correlations (object): Pandas data frame of genetic correlations
        threshold_secondary_heritability (float): threshold for heritability of
            secondary phenotypes, or missing null
        threshold_false_discovery_rate (float): threshold for false discovery
            rate
        report (bool): whether to print reports

    raises:

    returns:
        (object): Pandas data frame of metabolites' heritability estimates and
            genetic correlation estimates against a phenotype of interest

    """

    # Merge tables for metabolite heritabilities and correlations.
    # Merge data tables using database-style join.
    # Alternative is to use DataFrame.join().
    table = table_secondary_heritability.merge(
        table_correlations,
        how="outer",
        left_on="identifier",
        right_on="identifier",
        suffixes=("_heritability", "_correlation"),
    )

    # Introduce columns for phenotype heritability.
    table["phenotype_heritability"] = primary_heritability["heritability"]
    table["phenotype_heritability_error"] = (
        primary_heritability["heritability_standard_error"]
    )

    # Select table rows for secondary phenotypes with valid heritability
    # estimates.
    # Only filter if threshold is not missing or null.
    if (not math.isnan(threshold_secondary_heritability)):
        table = table.loc[
            (table["heritability"] >= threshold_secondary_heritability), :
        ]

    # Calculate False Discovery Rates (FDRs).
    table = utility.calculate_table_false_discovery_rates(
        threshold=threshold_false_discovery_rate,
        probability="correlation_probability",
        discovery="correlation_discovery",
        significance="correlation_significance",
        table=table,
    )
    # Sort table rows.
    table.sort_values(
        by=["correlation_absolute"],
        axis="index",
        ascending=False,
        na_position="last",
        inplace=True,
    )
    table.sort_values(
        by=["correlation_discovery",],
        axis="index",
        ascending=True,
        na_position="last",
        inplace=True,
    )
    # Sort table columns.
    columns_sequence = [
        #"identifier",
        #"name",
        "correlation_discovery",
        "correlation", "correlation_standard_error",
        "correlation_absolute",
        "correlation_probability",
        "correlation_significance",
        "correlation_variants",
        "heritability", "heritability_standard_error",
        "heritability_ratio",
        "heritability_ratio_standard_error",
        "heritability_variants",
        "phenotype_heritability",
        "phenotype_heritability_error",
    ]
    table = table[[*columns_sequence]]
    # Report.
    if report:
        utility.print_terminal_partition(level=2)
        print("combine_organize_phenotype_metabolites_summary_table()")
        print(table)
    # Return information.
    return table


##########
# Write


def write_product_study_table(
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


def write_product_studies(
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
        write_product_study_table(
            name=name,
            information=information[name],
            path_parent=path_parent,
        )
    pass


def write_product(
    primary_study=None,
    secondary_study=None,
    information=None,
    paths=None,
):
    """
    Writes product information to file.

    arguments:
        primary_study (str): identifier of primary study, consisting of a single
            GWAS
        secondary_study (str): identifier of secondary study, consisting of
            multiple GWASes
        information (object): information to write to file
        paths (dict<str>): collection of paths to directories for procedure's
            files

    raises:

    returns:

    """

    # Specify directories and files.
    path_table = os.path.join(
        paths["genetic_correlation"],
        str("table_" + primary_study + "_" + secondary_study + ".tsv")
    )
    # Write information to file.
    information["table_summary"].to_csv(
        path_or_buf=path_table,
        sep="\t",
        header=True,
        index=True,
    )
    pass


##########
# Driver


def drive_collection_report_primary_secondary_studies(
    primary_study=None,
    secondary_study=None,
    path_dock=None,
    report=None,
):
    """
    Function to execute module's main behavior.

    arguments:
        primary_study (str): identifier of primary study, consisting of a single
            GWAS
        secondary_study (str): identifier of secondary study, consisting of
            multiple GWASes
        path_dock (str): path to dock directory for source and product
            directories and files
        report (bool): whether to print reports

    raises:

    returns:

    """

    # Report.
    if report:
        utility.print_terminal_partition(level=2)
        print("report: drive_collection_report_primary_secondary_studies()")
        print(primary_study)
        print(secondary_study)

    # Initialize directories.
    paths = initialize_directories(
        primary_study=primary_study,
        secondary_study=secondary_study,
        restore=False,
        path_dock=path_dock,
    )

    # Read source information from file.
    source = read_source(
        primary_study=primary_study,
        secondary_study=secondary_study,
        paths=paths,
        report=False,
    )
    # Organize summary table.
    table_summary = combine_organize_phenotypes_summary_table(
        primary_heritability=source["primary_heritability"],
        table_secondary_heritability=source["table_secondary_heritability"],
        table_correlations=source["table_correlations"],
        threshold_secondary_heritability=float("nan"),
        threshold_false_discovery_rate=0.05,
        report=False,
    )

    # Report.
    if report:
        utility.print_terminal_partition(level=5)
        print(table_summary)

    # Collect information.
    information = dict()
    information["table_summary"] = table_summary
    # Write product information to file.
    write_product(
        primary_study=primary_study,
        secondary_study=secondary_study,
        paths=paths,
        information=information
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

    # Report version.
    utility.print_terminal_partition(level=1)
    print(path_dock)
    print("version check: 1")
    # Pause procedure.
    time.sleep(5.0)

    # Define phenotype studies.
    primary_studies = [
        "30482948_walters_2018_all",
        #"30482948_walters_2018_eur",
        #"30482948_walters_2018_eur_unrel",
    ]
    # Define container for secondary studies.
    secondary_studies = [
        "cohorts_hormones",
    ]
    for primary_study in primary_studies:
        for secondary_study in secondary_studies:
            drive_collection_report_primary_secondary_studies(
                primary_study=primary_study,
                secondary_study=secondary_study,
                path_dock=path_dock,
                report=True,
            )
            pass
        pass
    pass



if (__name__ == "__main__"):
    execute_procedure()
