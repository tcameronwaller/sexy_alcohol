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

import albumin
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
        "-temporary", "--temporary", dest="temporary", type=str, required=True,
        help=(
            "Path to temporary directory for source and product " +
            "directories and files."
        )
    )
    parser_main.add_argument(
        "-dock", "--dock", dest="dock", type=str, required=True,
        help=(
            "Path to dock directory for source and product " +
            "directories and files."
        )
    )
    parser_main.add_argument(
        "-albumin", "--albumin", dest="albumin", action="store_true",
        help=(
            "Prediction of blood or serum albumin."
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
    if arguments.albumin:
        # Report status.
        print("... executing albumin procedure ...")
        # Execute procedure.
        albumin.execute_procedure(
            temporary=arguments.temporary,
            dock=arguments.dock
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
