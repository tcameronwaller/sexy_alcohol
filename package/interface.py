"""
...
"""

###############################################################################
# Notes

###############################################################################
# Installation and importation

# Standard.
import argparse
import textwrap

# Relevant.

# Custom.

import scratch
import assembly
import organization
import description
import stratification
import genetic_correlation
#import plot
#import utility

#dir()
#importlib.reload()

###############################################################################
# Functionality


def define_interface_parsers():
    """
    Defines and parses arguments from terminal's interface.

    arguments:

    raises:

    returns:
        (object): arguments from terminal

    """

    # Define description.
    description = define_general_description()
    # Define epilog.
    epilog = define_general_epilog()
    # Define arguments.
    parser = argparse.ArgumentParser(
        description=description,
        epilog=epilog,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    subparsers = parser.add_subparsers(title="procedures")
    parser_main = define_main_subparser(subparsers=subparsers)
    # TODO: add other subparsers here...
    # Parse arguments.
    return parser.parse_args()


def define_general_description():
    """
    Defines description for terminal interface.

    arguments:

    raises:

    returns:
        (str): description for terminal interface

    """

    description = textwrap.dedent("""\
        --------------------------------------------------
        --------------------------------------------------
        --------------------------------------------------

        Access data from UK Biobank and do other stuff.

        --------------------------------------------------
    """)
    return description


def define_general_epilog():
    """
    Defines epilog for terminal interface.

    arguments:

    raises:

    returns:
        (str): epilog for terminal interface

    """

    epilog = textwrap.dedent("""\

        --------------------------------------------------
        --------------------------------------------------
        --------------------------------------------------
    """)
    return epilog


def define_main_subparser(subparsers=None):
    """
    Defines subparser for procedures that adapt a model of human metabolism.

    arguments:
        subparsers (object): reference to subparsers' container

    raises:

    returns:
        (object): reference to parser

    """

    # Define description.
    description = define_main_description()
    # Define epilog.
    epilog = define_main_epilog()
    # Define parser.
    parser_main = subparsers.add_parser(
        name="main",
        description=description,
        epilog=epilog,
        help="Help for main routine.",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    # Define arguments.
    parser_main.add_argument(
        "-path_dock", "--path_dock", dest="path_dock", type=str, required=True,
        help=(
            "Path to dock directory for source and product " +
            "directories and files."
        )
    )
    parser_main.add_argument(
        "-scratch", "--scratch",
        dest="scratch",
        action="store_true",
        help=(
            "Scratch, temporary module for method development and testing."
        )
    )
    parser_main.add_argument(
        "-assembly", "--assembly", dest="assembly", action="store_true",
        help=(
            "Organization of information for further analyses."
        )
    )
    parser_main.add_argument(
        "-organization", "--organization", dest="organization",
        action="store_true",
        help=(
            "Organization of variables, definition of cohorts and phenotypes."
        )
    )
    parser_main.add_argument(
        "-description", "--description",
        dest="description",
        action="store_true",
        help=(
            "Description of cohorts and phenotypes with summary statistics " +
            "and plots."
        )
    )
    parser_main.add_argument(
        "-stratification", "--stratification",
        dest="stratification",
        action="store_true",
        help=(
            "Stratification of cohorts and formatting tables of phenotypes " +
            "and covariates for genetic analyses (especially GWAS in PLINK2)."
        )
    )
    parser_main.add_argument(
        "-genetic_correlation", "--genetic_correlation",
        dest="genetic_correlation",
        action="store_true",
        help=(
            "Collection of genetic correlation estimates for phenotypes from " +
            "multiple GWAS."
        )
    )
    # Define behavior.
    parser_main.set_defaults(func=evaluate_main_parameters)
    # Return parser.
    return parser_main


def define_main_description():
    """
    Defines description for terminal interface.

    arguments:

    raises:

    returns:
        (str): description for terminal interface

    """

    description = textwrap.dedent("""\
        --------------------------------------------------
        --------------------------------------------------
        --------------------------------------------------

        Package's main procedure

        Do stuff.

        --------------------------------------------------
    """)
    return description


def define_main_epilog():
    """
    Defines epilog for terminal interface.

    arguments:

    raises:

    returns:
        (str): epilog for terminal interface

    """

    epilog = textwrap.dedent("""\

        --------------------------------------------------
        main routine

        --------------------------------------------------
        additional notes...


        --------------------------------------------------
        --------------------------------------------------
        --------------------------------------------------
    """)
    return epilog


def evaluate_main_parameters(arguments):
    """
    Evaluates parameters for model procedure.

    arguments:
        arguments (object): arguments from terminal

    raises:

    returns:

    """

    print("--------------------------------------------------")
    print("... call to main routine ...")
    # Execute procedure.
    if arguments.scratch:
        # Report status.
        print("... executing scratch procedure ...")
        # Execute procedure.
        scratch.execute_procedure(
            path_dock=arguments.path_dock
        )
    if arguments.assembly:
        # Report status.
        print("... executing assembly procedure ...")
        # Execute procedure.
        assembly.execute_procedure(
            path_dock=arguments.path_dock
        )
    if arguments.organization:
        # Report status.
        print("... executing organization procedure ...")
        # Execute procedure.
        organization.execute_procedure(
            path_dock=arguments.path_dock
        )
    if arguments.description:
        # Report status.
        print("... executing description procedure ...")
        # Execute procedure.
        description.execute_procedure(
            path_dock=arguments.path_dock
        )
    if arguments.stratification:
        # Report status.
        print("... executing stratification procedure ...")
        # Execute procedure.
        stratification.execute_procedure(
            path_dock=arguments.path_dock
        )

    pass


###############################################################################
# Procedure


def execute_procedure():
    """
    Function to execute module's main behavior.

    arguments:

    returns:

    raises:

    """

    # TODO: I want 2 separate procedures: 1. definition, 2. analysis

    # Parse arguments from terminal.
    arguments = define_interface_parsers()
    # Call the appropriate function.
    arguments.func(arguments)


if (__name__ == "__main__"):
    execute_procedure()
