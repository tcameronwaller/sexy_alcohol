
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
    groups = ["all", "case", "control"]
    for sex in sexes:
        paths[sex] = dict()
        for alcoholism in alcoholisms:
            paths[sex][alcoholism] = dict()
            for group in groups:
                paths[sex][alcoholism][group] = os.path.join(
                    path_parent, "cohorts", sex, alcoholism, group
                )
                # Initialize directories.
                utility.create_directories(
                    path=paths[sex][alcoholism][group]
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
    paths["export"] = os.path.join(
        path_dock, "organization", "export"
    )
    paths["cohorts"] = os.path.join(
        path_dock, "organization", "cohorts"
    )
    paths["plots"] = os.path.join(
        path_dock, "organization", "plots"
    )

    # Remove previous files to avoid version or batch confusion.
    if restore:
        utility.remove_directory(path=paths["organization"])
    # Initialize directories.
    utility.create_directories(
        path=paths["organization"]
    )
    utility.create_directories(
        path=paths["export"]
    )
    utility.create_directories(
        path=paths["cohorts"]
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
        path_dock, "assembly", "table_phenotypes.pickle"
    )
    # Read information from file.
    table_phenotypes = pandas.read_pickle(
        path_table_phenotypes
    )
    if False:
        path_table_ukb_samples = os.path.join(
            path_dock, "access", "ukb46237_imp_chr21_v3_s487320.sample"
        )
        table_ukb_samples = pandas.read_csv(
            path_table_ukb_samples,
            sep="\s+",
            header=0,
            dtype="string",
        )
    # Compile and return information.
    return {
        "table_phenotypes": table_phenotypes,
        #"table_ukb_samples": table_ukb_samples,
    }


############################
# A LOT below here should not be duplicated from uk_biobank package...
################################


##########
# Alcoholism cases and controls


# TODO: do not change alcohol_none to True/False/None like the diagnosis flags
def determine_control_alcoholism(
    alcohol_none=None,
    alcohol_diagnosis_a=None,
    alcohol_diagnosis_b=None,
    alcohol_diagnosis_c=None,
    alcohol_diagnosis_d=None,
    alcohol_diagnosis_self=None,
    alcohol_auditc=None,
    alcohol_auditp=None,
    alcohol_audit=None,
    threshold_auditc_control=None,
    threshold_auditc_case=None,
    threshold_auditp_control=None,
    threshold_auditp_case=None,
    threshold_audit_control=None,
    threshold_audit_case=None,
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
        alcohol_auditp (float): combination score for AUDIT-P questionnaire
        alcohol_audit (float): combination score for AUDIT questionnaire
        threshold_auditc_control (float): diagnostic control threshold (less
            than or equal) for AUDIT-C score
        threshold_auditc_case (float): diagnostic case threshold (greater than
            or equal) for AUDIT-C score
        threshold_auditp_control (float): diagnostic control threshold (less
            than or equal) for AUDIT-P score
        threshold_auditp_case (float): diagnostic case threshold (greater than
            or equal) for AUDIT-P score
        threshold_audit_control (float): diagnostic control threshold (less
            than or equal) for AUDIT score
        threshold_audit_case (float): diagnostic case threshold (greater than
            or equal) for AUDIT score

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

    # Determine whether person's AUDIT scores are within thresholds.
    if (math.isnan(alcohol_audit)):
        comparison_audit = False
    else:
        if (alcohol_audit <= threshold_audit_control):
            comparison_audit = True
        else:
            comparison_audit = False
    # Interpret comparisons from all AUDIT socre combinations.
    if (comparison_audit):
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
        # Person's AUDIT scores are below diagnostic thresholds.
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
    alcohol_auditp=None,
    alcohol_audit=None,
    threshold_auditc_control=None,
    threshold_auditc_case=None,
    threshold_auditp_control=None,
    threshold_auditp_case=None,
    threshold_audit_control=None,
    threshold_audit_case=None,
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
        alcohol_auditp (float): combination score for AUDIT-P questionnaire
        alcohol_audit (float): combination score for AUDIT questionnaire
        threshold_auditc_control (float): diagnostic control threshold (less
            than or equal) for AUDIT-C score
        threshold_auditc_case (float): diagnostic case threshold (greater than
            or equal) for AUDIT-C score
        threshold_auditp_control (float): diagnostic control threshold (less
            than or equal) for AUDIT-P score
        threshold_auditp_case (float): diagnostic case threshold (greater than
            or equal) for AUDIT-P score
        threshold_audit_control (float): diagnostic control threshold (less
            than or equal) for AUDIT score
        threshold_audit_case (float): diagnostic case threshold (greater than
            or equal) for AUDIT score

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
    control = determine_control_alcoholism(
        alcohol_none=alcohol_none,
        alcohol_diagnosis_a=alcohol_diagnosis_a,
        alcohol_diagnosis_b=alcohol_diagnosis_b,
        alcohol_diagnosis_c=alcohol_diagnosis_c,
        alcohol_diagnosis_d=alcohol_diagnosis_d,
        alcohol_diagnosis_self=alcohol_diagnosis_self,
        alcohol_auditc=alcohol_auditc,
        alcohol_auditp=alcohol_auditp,
        alcohol_audit=alcohol_audit,
        threshold_auditc_control=threshold_auditc_control,
        threshold_auditc_case=threshold_auditc_case,
        threshold_auditp_control=threshold_auditp_control,
        threshold_auditp_case=threshold_auditp_case,
        threshold_audit_control=threshold_audit_control,
        threshold_audit_case=threshold_audit_case,
    )

    # Interpret case and control and assign value.
    # Interpretation variables "case" and "control" do not have null values.
    # Assign missing value to persons who qualify neither as case nor control.
    if case:
        value = True
    elif control:
        value = False
    else:
        value = None
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
    alcohol_auditp=None,
    alcohol_audit=None,
    threshold_auditc_control=None,
    threshold_auditc_case=None,
    threshold_auditp_control=None,
    threshold_auditp_case=None,
    threshold_audit_control=None,
    threshold_audit_case=None,
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
        alcohol_auditp (float): combination score for AUDIT-P questionnaire
        alcohol_audit (float): combination score for AUDIT questionnaire
        threshold_auditc_control (float): diagnostic control threshold (less
            than or equal) for AUDIT-C score
        threshold_auditc_case (float): diagnostic case threshold (greater than
            or equal) for AUDIT-C score
        threshold_auditp_control (float): diagnostic control threshold (less
            than or equal) for AUDIT-P score
        threshold_auditp_case (float): diagnostic case threshold (greater than
            or equal) for AUDIT-P score
        threshold_audit_control (float): diagnostic control threshold (less
            than or equal) for AUDIT score
        threshold_audit_case (float): diagnostic case threshold (greater than
            or equal) for AUDIT score

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
    control = determine_control_alcoholism(
        alcohol_none=alcohol_none,
        alcohol_diagnosis_a=alcohol_diagnosis_a,
        alcohol_diagnosis_b=alcohol_diagnosis_b,
        alcohol_diagnosis_c=alcohol_diagnosis_c,
        alcohol_diagnosis_d=alcohol_diagnosis_d,
        alcohol_diagnosis_self=alcohol_diagnosis_self,
        alcohol_auditc=alcohol_auditc,
        alcohol_auditp=alcohol_auditp,
        alcohol_audit=alcohol_audit,
        threshold_auditc_control=threshold_auditc_control,
        threshold_auditc_case=threshold_auditc_case,
        threshold_auditp_control=threshold_auditp_control,
        threshold_auditp_case=threshold_auditp_case,
        threshold_audit_control=threshold_audit_control,
        threshold_audit_case=threshold_audit_case,
    )

    # Interpret case and control and assign value.
    # Interpretation variables "case" and "control" do not have null values.
    # Assign missing value to persons who qualify neither as case nor control.
    if case:
        value = True
    elif control:
        value = False
    else:
        value = None
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
    alcohol_auditp=None,
    alcohol_audit=None,
    threshold_auditc_control=None,
    threshold_auditc_case=None,
    threshold_auditp_control=None,
    threshold_auditp_case=None,
    threshold_audit_control=None,
    threshold_audit_case=None,
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
        alcohol_auditp (float): combination score for AUDIT-P questionnaire
        alcohol_audit (float): combination score for AUDIT questionnaire
        threshold_auditc_control (float): diagnostic control threshold (less
            than or equal) for AUDIT-C score
        threshold_auditc_case (float): diagnostic case threshold (greater than
            or equal) for AUDIT-C score
        threshold_auditp_control (float): diagnostic control threshold (less
            than or equal) for AUDIT-P score
        threshold_auditp_case (float): diagnostic case threshold (greater than
            or equal) for AUDIT-P score
        threshold_audit_control (float): diagnostic control threshold (less
            than or equal) for AUDIT score
        threshold_audit_case (float): diagnostic case threshold (greater than
            or equal) for AUDIT score

    raises:

    returns:
        (float): binary representation whether person qualifies as a case or
            control by specific definition of alcoholism

    """

    # Determine whether person qualifies as a case of alcoholism.
    if (math.isnan(alcohol_auditc)):
        case = False
    else:
        if (alcohol_auditc >= threshold_auditc_case):
            case = True
        else:
            case = False

    # Determine whether person qualifies as a control of alcoholism.
    # Person's control status can have null or missing values.
    control = determine_control_alcoholism(
        alcohol_none=alcohol_none,
        alcohol_diagnosis_a=alcohol_diagnosis_a,
        alcohol_diagnosis_b=alcohol_diagnosis_b,
        alcohol_diagnosis_c=alcohol_diagnosis_c,
        alcohol_diagnosis_d=alcohol_diagnosis_d,
        alcohol_diagnosis_self=alcohol_diagnosis_self,
        alcohol_auditc=alcohol_auditc,
        alcohol_auditp=alcohol_auditp,
        alcohol_audit=alcohol_audit,
        threshold_auditc_control=threshold_auditc_control,
        threshold_auditc_case=threshold_auditc_case,
        threshold_auditp_control=threshold_auditp_control,
        threshold_auditp_case=threshold_auditp_case,
        threshold_audit_control=threshold_audit_control,
        threshold_audit_case=threshold_audit_case,
    )

    # Interpret case and control and assign value.
    # Interpretation variables "case" and "control" do not have null values.
    # Assign missing value to persons who qualify neither as case nor control.
    if case:
        value = True
    elif control:
        value = False
    else:
        value = None
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
    alcohol_auditp=None,
    alcohol_audit=None,
    threshold_auditc_control=None,
    threshold_auditc_case=None,
    threshold_auditp_control=None,
    threshold_auditp_case=None,
    threshold_audit_control=None,
    threshold_audit_case=None,
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
        alcohol_auditp (float): combination score for AUDIT-P questionnaire
        alcohol_audit (float): combination score for AUDIT questionnaire
        threshold_auditc_control (float): diagnostic control threshold (less
            than or equal) for AUDIT-C score
        threshold_auditc_case (float): diagnostic case threshold (greater than
            or equal) for AUDIT-C score
        threshold_auditp_control (float): diagnostic control threshold (less
            than or equal) for AUDIT-P score
        threshold_auditp_case (float): diagnostic case threshold (greater than
            or equal) for AUDIT-P score
        threshold_audit_control (float): diagnostic control threshold (less
            than or equal) for AUDIT score
        threshold_audit_case (float): diagnostic case threshold (greater than
            or equal) for AUDIT score

    raises:

    returns:
        (float): binary representation whether person qualifies as a case or
            control by specific definition of alcoholism

    """

    # Determine whether person qualifies as a case of alcoholism.
    if (math.isnan(alcohol_auditp)):
        case = False
    else:
        if (alcohol_auditp >= threshold_auditp_case):
            case = True
        else:
            case = False
    # Determine whether person qualifies as a control of alcoholism.
    # Person's control status can have null or missing values.
    control = determine_control_alcoholism(
        alcohol_none=alcohol_none,
        alcohol_diagnosis_a=alcohol_diagnosis_a,
        alcohol_diagnosis_b=alcohol_diagnosis_b,
        alcohol_diagnosis_c=alcohol_diagnosis_c,
        alcohol_diagnosis_d=alcohol_diagnosis_d,
        alcohol_diagnosis_self=alcohol_diagnosis_self,
        alcohol_auditc=alcohol_auditc,
        alcohol_auditp=alcohol_auditp,
        alcohol_audit=alcohol_audit,
        threshold_auditc_control=threshold_auditc_control,
        threshold_auditc_case=threshold_auditc_case,
        threshold_auditp_control=threshold_auditp_control,
        threshold_auditp_case=threshold_auditp_case,
        threshold_audit_control=threshold_audit_control,
        threshold_audit_case=threshold_audit_case,
    )

    # Interpret case and control and assign value.
    # Interpretation variables "case" and "control" do not have null values.
    # Assign missing value to persons who qualify neither as case nor control.
    if case:
        value = True
    elif control:
        value = False
    else:
        value = None
    # Return information.
    return value


def determine_case_control_alcoholism_five(
    alcohol_none=None,
    alcohol_diagnosis_a=None,
    alcohol_diagnosis_b=None,
    alcohol_diagnosis_c=None,
    alcohol_diagnosis_d=None,
    alcohol_diagnosis_self=None,
    alcohol_auditc=None,
    alcohol_auditp=None,
    alcohol_audit=None,
    threshold_auditc_control=None,
    threshold_auditc_case=None,
    threshold_auditp_control=None,
    threshold_auditp_case=None,
    threshold_audit_control=None,
    threshold_audit_case=None,
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
        alcohol_auditp (float): combination score for AUDIT-P questionnaire
        alcohol_audit (float): combination score for AUDIT questionnaire
        threshold_auditc_control (float): diagnostic control threshold (less
            than or equal) for AUDIT-C score
        threshold_auditc_case (float): diagnostic case threshold (greater than
            or equal) for AUDIT-C score
        threshold_auditp_control (float): diagnostic control threshold (less
            than or equal) for AUDIT-P score
        threshold_auditp_case (float): diagnostic case threshold (greater than
            or equal) for AUDIT-P score
        threshold_audit_control (float): diagnostic control threshold (less
            than or equal) for AUDIT score
        threshold_audit_case (float): diagnostic case threshold (greater than
            or equal) for AUDIT score

    raises:

    returns:
        (float): binary representation whether person qualifies as a case or
            control by specific definition of alcoholism

    """

    # Determine whether person qualifies as a case of alcoholism.
    if (math.isnan(alcohol_audit)):
        case = False
    else:
        if (alcohol_audit >= threshold_audit_case):
            case = True
        else:
            case = False
    # Determine whether person qualifies as a control of alcoholism.
    # Person's control status can have null or missing values.
    control = determine_control_alcoholism(
        alcohol_none=alcohol_none,
        alcohol_diagnosis_a=alcohol_diagnosis_a,
        alcohol_diagnosis_b=alcohol_diagnosis_b,
        alcohol_diagnosis_c=alcohol_diagnosis_c,
        alcohol_diagnosis_d=alcohol_diagnosis_d,
        alcohol_diagnosis_self=alcohol_diagnosis_self,
        alcohol_auditc=alcohol_auditc,
        alcohol_auditp=alcohol_auditp,
        alcohol_audit=alcohol_audit,
        threshold_auditc_control=threshold_auditc_control,
        threshold_auditc_case=threshold_auditc_case,
        threshold_auditp_control=threshold_auditp_control,
        threshold_auditp_case=threshold_auditp_case,
        threshold_audit_control=threshold_audit_control,
        threshold_audit_case=threshold_audit_case,
    )

    # Interpret case and control and assign value.
    # Interpretation variables "case" and "control" do not have null values.
    # Assign missing value to persons who qualify neither as case nor control.
    if case:
        value = True
    elif control:
        value = False
    else:
        value = None
    # Return information.
    return value


def organize_report_cohort_by_sex_alcoholism_split_hormone(
    sex_text=None,
    alcohol_consumption=None,
    alcoholism=None,
    alcoholism_split=None,
    hormone=None,
    variables_names_valid=None,
    variables_prefixes_valid=None,
    table=None,
):
    """
    Organizes information about previous and current alcohol consumption.

    arguments:
        sex_text (str): textual representation of sex selection
        alcohol_consumption (bool): whether to filter to persons who are past or
            present consumers of alcohol
        alcoholism (str): name of column defining alcoholism cases and controls
        alcoholism_split (str): how to divide cohort by alcoholism, either
            "all", "case", or "control"
        hormone (str): name of column for hormone
        variables_names_valid (list<str>): names of columns for variables in
            which rows must have valid values
        variables_prefixes_valid (list<str>): prefixes of columns for variables
            in which rows must have valid values
        table (object): Pandas data frame of phenotype variables across UK
            Biobank cohort

    raises:

    returns:

    """

    # Report.
    utility.print_terminal_partition(level=4)
    print("sex: " + str(sex_text))
    print("alcoholism: " + str(alcoholism))
    print("alcoholism split: " + str(alcoholism_split))
    print("hormone: " + str(hormone))
    # Select cohort's variables and records with valid values.
    table_valid = select_sex_alcoholism_cohort_variables_valid_records(
        sex_text=sex_text,
        alcohol_consumption=alcohol_consumption,
        alcoholism=alcoholism,
        alcoholism_split=alcoholism_split,
        variables_names_valid=variables_names_valid,
        variables_prefixes_valid=variables_prefixes_valid,
        table=table,
    )
    # Report.
    print("table shape: " + str(table_valid.shape))
    pass


def organize_report_cohorts_by_sex_alcoholism_split_hormone(
    table=None,
):
    """
    Organizes report of cohorts by combinations of sex, alcoholism definition,
    alcoholism split (all, case, control), and valid hormone values.

    arguments:
        table (object): Pandas data frame of phenotype variables across UK
            Biobank cohort

    raises:

    returns:

    """

    # Iterate on cohort permutations.
    sexes = ["female", "male",]
    alcoholisms = [
        "alcoholism_1", "alcoholism_2", "alcoholism_3", "alcoholism_4",
        "alcoholism_5",
    ]
    alcoholism_splits = [
        "all", "case", "control",
    ]
    #hormones = ["oestradiol", "testosterone",]
    hormones = ["albumin", "steroid_globulin",]
    for sex in sexes:
        utility.print_terminal_partition(level=2)
        for alcoholism in alcoholisms:
            for alcoholism_split in alcoholism_splits:
                utility.print_terminal_partition(level=3)
                organize_report_cohort_by_sex_alcoholism_split_hormone(
                    sex_text=sex,
                    alcohol_consumption=True,
                    alcoholism=alcoholism,
                    alcoholism_split=alcoholism_split,
                    hormone="None... not specific",
                    variables_names_valid=[
                        "eid", "IID",
                        "sex", "sex_text", "age", "body_mass_index",
                        "alcohol_none",
                        alcoholism,
                    ],
                    variables_prefixes_valid=["genotype_pc_",],
                    table=table,
                )
                for hormone in hormones:
                    organize_report_cohort_by_sex_alcoholism_split_hormone(
                        sex_text=sex,
                        alcohol_consumption=True,
                        alcoholism=alcoholism,
                        alcoholism_split=alcoholism_split,
                        hormone=hormone,
                        variables_names_valid=[
                            "eid", "IID",
                            "sex", "sex_text", "age", "body_mass_index",
                            "alcohol_none",
                            alcoholism,
                            hormone,
                        ],
                        variables_prefixes_valid=["genotype_pc_",],
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

    # Copy information.
    table = table.copy(deep=True)
    # Specify diagnostic thresholds for AUDIT-C and AUDIT scores.
    # https://auditscreen.org/about/scoring-audit/
    # https://cde.drugabuse.gov/instrument/f229c68a-67ce-9a58-e040-bb89ad432be4
    # Use less than or equal for control thresholds.
    # Use greater than or equal for case thresholds.
    threshold_auditc_control = 4
    threshold_auditc_case = 10
    threshold_auditp_control = 3
    threshold_auditp_case = 5
    threshold_audit_control = 7
    threshold_audit_case = 15

    # Determine whether person is a case or control for alcoholism type 1.
    # case: ICD9 or ICD10 codes in diagnostic group A
    # control:
    # - only persons who have consumed alcohol, previously or currently
    # - no ICD9 or ICD10 codes in diagnostic groups A, B, C, or D
    # - no self diagnoses of alcoholism
    # - below AUDIT control thresholds
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
                alcohol_auditp=row["alcohol_auditp"],
                alcohol_audit=row["alcohol_audit"],
                threshold_auditc_control=threshold_auditc_control,
                threshold_auditc_case=threshold_auditc_case,
                threshold_auditp_control=threshold_auditp_control,
                threshold_auditp_case=threshold_auditp_case,
                threshold_audit_control=threshold_audit_control,
                threshold_audit_case=threshold_audit_case,
            ),
        axis="columns", # apply across rows
    )
    # Determine whether person is a case or control for alcoholism type 2.
    # case: ICD9 or ICD10 codes in diagnostic group A, B, C, or D
    # control:
    # - only persons who have consumed alcohol, previously or currently
    # - no ICD9 or ICD10 codes in diagnostic groups A, B, C, or D
    # - no self diagnoses of alcoholism
    # - below AUDIT control thresholds
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
                alcohol_auditp=row["alcohol_auditp"],
                alcohol_audit=row["alcohol_audit"],
                threshold_auditc_control=threshold_auditc_control,
                threshold_auditc_case=threshold_auditc_case,
                threshold_auditp_control=threshold_auditp_control,
                threshold_auditp_case=threshold_auditp_case,
                threshold_audit_control=threshold_audit_control,
                threshold_audit_case=threshold_audit_case,
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
    # - below AUDIT control thresholds
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
                alcohol_auditp=row["alcohol_auditp"],
                alcohol_audit=row["alcohol_audit"],
                threshold_auditc_control=threshold_auditc_control,
                threshold_auditc_case=threshold_auditc_case,
                threshold_auditp_control=threshold_auditp_control,
                threshold_auditp_case=threshold_auditp_case,
                threshold_audit_control=threshold_audit_control,
                threshold_audit_case=threshold_audit_case,
            ),
        axis="columns", # apply across rows
    )

    # Determine whether person is a case or control for alcoholism type 4.
    # case:
    # AUDIT-P score > threshold_auditp_case
    # control:
    # - only persons who have consumed alcohol, previously or currently
    # - no ICD9 or ICD10 codes in diagnostic groups A, B, C, or D
    # - no self diagnoses of alcoholism
    # - below AUDIT control thresholds
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
                alcohol_auditp=row["alcohol_auditp"],
                alcohol_audit=row["alcohol_audit"],
                threshold_auditc_control=threshold_auditc_control,
                threshold_auditc_case=threshold_auditc_case,
                threshold_auditp_control=threshold_auditp_control,
                threshold_auditp_case=threshold_auditp_case,
                threshold_audit_control=threshold_audit_control,
                threshold_audit_case=threshold_audit_case,
            ),
        axis="columns", # apply across rows
    )

    # Determine whether person is a case or control for alcoholism type 5.
    # case:
    # AUDIT score > threshold_audit
    # control:
    # - only persons who have consumed alcohol, previously or currently
    # - no ICD9 or ICD10 codes in diagnostic groups A, B, C, or D
    # - no self diagnoses of alcoholism
    # - below AUDIT control thresholds
    table["alcoholism_5"] = table.apply(
        lambda row:
            determine_case_control_alcoholism_five(
                alcohol_none=row["alcohol_none"],
                alcohol_diagnosis_a=row["alcohol_diagnosis_a"],
                alcohol_diagnosis_b=row["alcohol_diagnosis_b"],
                alcohol_diagnosis_c=row["alcohol_diagnosis_c"],
                alcohol_diagnosis_d=row["alcohol_diagnosis_d"],
                alcohol_diagnosis_self=row["alcohol_diagnosis_self"],
                alcohol_auditc=row["alcohol_auditc"],
                alcohol_auditp=row["alcohol_auditp"],
                alcohol_audit=row["alcohol_audit"],
                threshold_auditc_control=threshold_auditc_control,
                threshold_auditc_case=threshold_auditc_case,
                threshold_auditp_control=threshold_auditp_control,
                threshold_auditp_case=threshold_auditp_case,
                threshold_audit_control=threshold_audit_control,
                threshold_audit_case=threshold_audit_case,
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
            #"alcohol_auditc",
            #"alcohol_audit",
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
            "alcoholism_5",
        ])
    ]
    # Report.
    if report:
        utility.print_terminal_partition(level=2)
        print("Summary of alcoholism cases and controls variables: ")
        print(table_report)
        organize_report_cohorts_by_sex_alcoholism_split_hormone(
            table=table_clean,
        )
        pass

    # Collect information.
    pail = dict()
    pail["table"] = table
    pail["table_clean"] = table_clean
    pail["table_report"] = table_report
    # Return information.
    return pail


##########
# Cohort selection, hormone and alcoholism in matching cohort


def select_sex_alcoholism_cohort_variables_valid_records(
    sex_text=None,
    alcohol_consumption=None,
    alcoholism=None,
    alcoholism_split=None,
    variables_names_valid=None,
    variables_prefixes_valid=None,
    table=None,
):
    """
    Selects variable columns and record rows with valid values across all
    variables.

    arguments:
        sex_text (str): textual representation of sex selection
        alcohol_consumption (bool): whether to filter to persons who are past or
            present consumers of alcohol
        alcoholism (str): name of column defining alcoholism cases and controls
        alcoholism_split (str): how to divide cohort by alcoholism, either
            "all", "case", or "control"
        variables_names_valid (list<str>): names of columns for variables in
            which rows must have valid values
        variables_prefixes_valid (list<str>): prefixes of columns for variables
            in which rows must have valid values
        table (object): Pandas data frame of phenotype variables across UK
            Biobank cohort

    raises:

    returns:
        (object): Pandas data frame of phenotype variables across UK Biobank
            cohort

    """

    # Copy information.
    table = table.copy(deep=True)
    # Select records with valid (non-null) values of relevant variables.
    # Exclude missing values first to avoid interpretation of "None" as False.
    table = ukb_organization.select_valid_records_all_specific_variables(
        names=variables_names_valid,
        prefixes=variables_prefixes_valid,
        table=table,
        drop_columns=True,
        report=False,
    )
    # Select cohort by values of specific variables.
    # Select records by sex.
    table = table.loc[
        (table["sex_text"] == sex_text), :
    ]
    # Select records by alcohol consumption.
    #table["alcohol_none"].astype(bool)
    if (alcohol_consumption):
        # Select records with valid values of "alcohol_none".
        table = table.loc[
            (pandas.notna(table["alcohol_none"])), :
        ]
        table = table.loc[
            (table["alcohol_none"] < 0.5), :
        ]
    # Select records by alcoholism.
    # Must first confirm column type is Boolean so that inverse is accurate.
    table[alcoholism] = table[alcoholism].astype("bool")
    if (not (str(alcoholism_split) == "all")):
        if (str(alcoholism_split) == "case"):
            table = table.loc[(table[alcoholism]), :]
        elif (str(alcoholism_split) == "control"):
            table = table.loc[(~table[alcoholism]), :]
    # Return information.
    return table


def organize_plink_cohort_variables_by_sex_alcoholism_split(
    sex_text=None,
    alcohol_consumption=None,
    alcoholism=None,
    alcoholism_split=None,
    phenotype_1=None,
    phenotype_2=None,
    table=None,
    report=None,
):
    """
    Organizes information about previous and current alcohol consumption.

    arguments:
        sex_text (str): textual representation of sex selection
        alcohol_consumption (bool): whether to filter to persons who are past or
            present consumers of alcohol
        alcoholism (str): name of column defining alcoholism cases and controls
        alcoholism_split (str): how to divide cohort by alcoholism, either
            "all", "case", or "control"
        phenotype_1 (str): name of a column for first phenotype variable,
            normally the alcoholism variable, which is binary when "split" is
            "all"
        phenotype_2 (str): name of a column for second phenotype variable,
            normally the hormone variable
        table (object): Pandas data frame of phenotype variables across UK
            Biobank cohort
        report (bool): whether to print reports

    raises:

    returns:
        (object): Pandas data frame of phenotype variables across UK Biobank
            cohort

    """

    # Select cohort's variables and records with valid values.
    table_valid = select_sex_alcoholism_cohort_variables_valid_records(
        sex_text=sex_text,
        alcohol_consumption=alcohol_consumption,
        alcoholism=alcoholism,
        alcoholism_split=alcoholism_split,
        variables_names_valid=[
            "eid", "IID",
            "sex", "sex_text", "age", "body_mass_index",
            "alcohol_none",
            alcoholism,
            phenotype_1,
            phenotype_2,
        ],
        variables_prefixes_valid=["genotype_pc_",],
        table=table,
    )

    # Translate variable encodings and table format for analysis in PLINK.
    if (str(alcoholism_split) == "all"):
        table_format = (
            ukb_organization.organize_phenotype_covariate_table_plink_format(
                boolean_phenotypes=[phenotype_1],
                binary_phenotypes=[],
                continuous_variables=[phenotype_2],
                table=table_valid,
        ))
    elif (
        (str(alcoholism_split) == "case") or
        (str(alcoholism_split) == "control")
    ):
        table_format = (
            ukb_organization.organize_phenotype_covariate_table_plink_format(
                boolean_phenotypes=[],
                binary_phenotypes=[],
                continuous_variables=[phenotype_1, phenotype_2],
                table=table_valid,
        ))
        pass
    # Report.
    if report:
        utility.print_terminal_partition(level=2)
        print("... phenotype covariate table in format for PLINK ...")
        print("sex: " + str(sex_text))
        print("alcoholism: " + str(alcoholism))
        print("alcoholism split: " + str(alcoholism_split))
        print(str(phenotype_1) + " versus " + str(phenotype_2))
        print("table shape: " + str(table_format.shape))
        print(table_format)
        utility.print_terminal_partition(level=4)
    # Return information.
    return table_format


def organize_plink_cohorts_variables_by_sex_alcoholism_split(
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

    # Iterate on cohort permutations.
    sexes = ["female", "male",]
    alcoholisms = [
        "alcoholism_1", "alcoholism_2", "alcoholism_3", "alcoholism_4",
        "alcoholism_5",
    ]
    alcoholism_splits = [
        "all", "case", "control",
    ]
    hormones = ["oestradiol", "testosterone",]

    # Compile information.
    pail = dict()
    # Select and organize variables across cohorts.

    pail["table_female_alcoholism-1_albumin"] = (
        organize_plink_cohort_variables_by_sex_alcoholism_split(
            sex_text="female",
            alcohol_consumption=True,
            alcoholism="alcoholism_1",
            alcoholism_split="all",
            phenotype_1="alcoholism_1",
            phenotype_2="albumin",
            table=table,
            report=report,
    ))
    pail["table_female_alcoholism-2_albumin"] = (
        organize_plink_cohort_variables_by_sex_alcoholism_split(
            sex_text="female",
            alcohol_consumption=True,
            alcoholism="alcoholism_2",
            alcoholism_split="all",
            phenotype_1="alcoholism_2",
            phenotype_2="albumin",
            table=table,
            report=report,
    ))
    pail["table_female_alcoholism-3_albumin"] = (
        organize_plink_cohort_variables_by_sex_alcoholism_split(
            sex_text="female",
            alcohol_consumption=True,
            alcoholism="alcoholism_3",
            alcoholism_split="all",
            phenotype_1="alcoholism_3",
            phenotype_2="albumin",
            table=table,
            report=report,
    ))
    pail["table_female_alcoholism-4_albumin"] = (
        organize_plink_cohort_variables_by_sex_alcoholism_split(
            sex_text="female",
            alcohol_consumption=True,
            alcoholism="alcoholism_4",
            alcoholism_split="all",
            phenotype_1="alcoholism_4",
            phenotype_2="albumin",
            table=table,
            report=report,
    ))
    pail["table_female_alcoholism-5_albumin"] = (
        organize_plink_cohort_variables_by_sex_alcoholism_split(
            sex_text="female",
            alcohol_consumption=True,
            alcoholism="alcoholism_5",
            alcoholism_split="all",
            phenotype_1="alcoholism_5",
            phenotype_2="albumin",
            table=table,
            report=report,
    ))

    pail["table_male_alcoholism-1_albumin"] = (
        organize_plink_cohort_variables_by_sex_alcoholism_split(
            sex_text="male",
            alcohol_consumption=True,
            alcoholism="alcoholism_1",
            alcoholism_split="all",
            phenotype_1="alcoholism_1",
            phenotype_2="albumin",
            table=table,
            report=report,
    ))
    pail["table_male_alcoholism-2_albumin"] = (
        organize_plink_cohort_variables_by_sex_alcoholism_split(
            sex_text="male",
            alcohol_consumption=True,
            alcoholism="alcoholism_2",
            alcoholism_split="all",
            phenotype_1="alcoholism_2",
            phenotype_2="albumin",
            table=table,
            report=report,
    ))
    pail["table_male_alcoholism-3_albumin"] = (
        organize_plink_cohort_variables_by_sex_alcoholism_split(
            sex_text="male",
            alcohol_consumption=True,
            alcoholism="alcoholism_3",
            alcoholism_split="all",
            phenotype_1="alcoholism_3",
            phenotype_2="albumin",
            table=table,
            report=report,
    ))
    pail["table_male_alcoholism-4_albumin"] = (
        organize_plink_cohort_variables_by_sex_alcoholism_split(
            sex_text="male",
            alcohol_consumption=True,
            alcoholism="alcoholism_4",
            alcoholism_split="all",
            phenotype_1="alcoholism_4",
            phenotype_2="albumin",
            table=table,
            report=report,
    ))
    pail["table_male_alcoholism-5_albumin"] = (
        organize_plink_cohort_variables_by_sex_alcoholism_split(
            sex_text="male",
            alcohol_consumption=True,
            alcoholism="alcoholism_5",
            alcoholism_split="all",
            phenotype_1="alcoholism_5",
            phenotype_2="albumin",
            table=table,
            report=report,
    ))
    # Return information.
    return pail


def scrap_record_cohorts_variables_by_sex_alcoholism_split(
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

    # Iterate on cohort permutations.
    sexes = ["female", "male",]
    alcoholisms = [
        "alcoholism_1", "alcoholism_2", "alcoholism_3", "alcoholism_4",
        "alcoholism_5",
    ]
    alcoholism_splits = [
        "all", "case", "control",
    ]
    hormones = ["oestradiol", "testosterone",]

    # Compile information.
    pail = dict()
    # Select and organize variables across cohorts.
    pail["table_female_alcoholism-1_steroid-globulin"] = (
        organize_plink_cohort_variables_by_sex_alcoholism_split(
            sex_text="female",
            alcohol_consumption=True,
            alcoholism="alcoholism_1",
            alcoholism_split="all",
            phenotype_1="alcoholism_1",
            phenotype_2="steroid_globulin",
            table=table,
            report=report,
    ))
    pail["table_female_alcoholism-1_oestradiol"] = (
        organize_plink_cohort_variables_by_sex_alcoholism_split(
            sex_text="female",
            alcohol_consumption=True,
            alcoholism="alcoholism_1",
            alcoholism_split="all",
            phenotype_1="alcoholism_1",
            phenotype_2="oestradiol",
            table=table,
            report=report,
    ))
    pail["table_female_alcoholism-1_testosterone"] = (
        organize_plink_cohort_variables_by_sex_alcoholism_split(
            sex_text="female",
            alcohol_consumption=True,
            alcoholism="alcoholism_1",
            alcoholism_split="all",
            phenotype_1="alcoholism_1",
            phenotype_2="testosterone",
            table=table,
            report=report,
    ))
    pail["table_female_alcoholism-1_case_auditc_testosterone"] = (
        organize_plink_cohort_variables_by_sex_alcoholism_split(
            sex_text="female",
            alcohol_consumption=True,
            alcoholism="alcoholism_1",
            alcoholism_split="case",
            phenotype_1="alcohol_auditc",
            phenotype_2="testosterone",
            table=table,
            report=report,
    ))
    # Return information.
    return pail


##########
# Cohort selection, hormone

    pail["table_female_male_oestradiol"] = (
        organize_plink_cohort_variables_by_sex_hormone(
            sex_text="both",
            exclude_pregnancy=True,
            menopause="both", # "both", "pre", "post"
            hormone="oestradiol_log",
            table=table,
            report=report,
    ))


##########
# Data export


def organize_hormone_export_table(
    table=None,
    report=None,
):
    """
    Organizes information for export.

    arguments:
        table (object): Pandas data frame of phenotype variables across UK
            Biobank cohort
        report (bool): whether to print reports

    raises:

    returns:
        (object): Pandas data frame of phenotype variables across UK Biobank

    """

    table = table.copy(deep=True)
    columns_export = [
        #"eid",
        "IID",
        "sex", "sex_text", "age", "body_mass_index", "body_mass_index_log",
        "menopause",
        "pregnancy_broad", "pregnancy",
        "menstruation_day",
        "oral_contraception",
        "hormone_therapy",
        "albumin", "albumin_log", "steroid_globulin", "steroid_globulin_log",
        "oestradiol", "oestradiol_log",
        "oestradiol_free", "oestradiol_free_log",
        "testosterone", "testosterone_log",
        "testosterone_free", "testosterone_free_log",
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
    # Return information.
    return table






##########
# ... in progress...

# Scrap now...


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


def write_product_cohort_table(
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

    for name in information.keys():
        write_product_cohort_table(
            name=name,
            information=information[name],
            path_parent=path_parent,
        )
    pass


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
    figure=None,
    file_name=None,
    path_parent=None,
):
    """
    Writes product information to file.

    arguments:
        figure (object): figure object to write to file
        file_name (str): base name for file
        path_parent (str): path to parent directory

    raises:

    returns:

    """

    # Specify directories and files.
    path_file = os.path.join(
        path_parent, str(file_name + ".png")
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

    for key in information.keys():
        write_product_plot_figure(
            figure=information[key]["figure"],
            file_name=information[key]["name"],
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

    # Plots.
    if False:
        write_product_plots(
            information=information["plots"],
            path_parent=paths["plots"],
        )
    # Export information.
    if False:
        write_product_quality(
            information=information["quality"],
            path_parent=paths["quality"],
        )
    # Export information.
    write_product_export(
        information=information["export"],
        path_parent=paths["export"],
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
        report=False,
    )
    # Organize variables for persons' genotypes, sex, age, and body mass index
    # across the UK Biobank.
    table_basis = ukb_organization.execute_genotype_sex_age_body(
        table=source["table_phenotypes"],
        report=False,
    )
    # Organize variables for persons' sex hormones across the UK Biobank.
    table_hormone = ukb_organization.execute_sex_hormones(
        table=table_basis,
        clean=False,
        report=True,
    )
    # Plot figures for hormones.
    if False:
        pail_figures_hormone = ukb_organization.execute_plot_hormones(
            table=table_hormone,
            report=False,
        )

    # Select and organize variables across cohorts.
    # Organize phenotypes and covariates in format for analysis in PLINK.
    pail_cohorts = (
        ukb_organization.select_organize_plink_cohorts_by_sex_hormones(
            table=table_hormone,
            report=False,
    ))

    # Organize information for export.
    table_hormone_export = organize_hormone_export_table(
        table=table_hormone,
        report=False,
    )


    # Collect information.
    information = dict()
    information["export"] = dict()
    information["export"]["table_hormone_export"] = table_hormone_export
    #information["plots"] = pail_figures_hormone
    information["cohorts"] = pail_cohorts
    # Write product information to file.
    write_product(
        paths=paths,
        information=information
    )


    # Organize variables for persons' alcohol consumption across the UK Biobank.
    if False:
        table_alcohol = ukb_organization.execute_alcohol(
            table=table_hormone,
            report=None,
        )

    if False:
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
        information["cohorts"] = pail_cohorts
        # Write product information to file.
        write_product(
            paths=paths,
            information=information
        )

    pass



if (__name__ == "__main__"):
    execute_procedure()
