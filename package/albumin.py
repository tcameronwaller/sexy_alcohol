
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
import statsmodels.api
import statsmodels.stats.outliers_influence
import matplotlib
matplotlib.use("agg")
matplotlib.rcParams.update({'figure.max_open_warning': 0})
import matplotlib.pyplot
import matplotlib.lines


# Custom

#import plot
import utility


###############################################################################
# Functionality



def define_font_properties():
    """
    Defines font properties.

    arguments:

    raises:

    returns:
        (dict<object>): references to definitions of font properties

    """

    # Define font values.
    values_one = {
        "family": "sans-serif",
        "style": "normal",
        "variant": "normal",
        "stretch": 1000,
        "weight": 1000,
        "size": 30
    }
    values_two = {
        "family": "sans-serif",
        "style": "normal",
        "variant": "normal",
        "stretch": 900,
        "weight": 1000,
        "size": 25
    }
    values_three = {
        "family": "sans-serif",
        "style": "normal",
        "variant": "normal",
        "stretch": 750,
        "weight": 1000,
        "size": 20
    }
    values_four = {
        "family": "sans-serif",
        "style": "normal",
        "variant": "normal",
        "stretch": 500,
        "weight": 500,
        "size": 17
    }
    values_five = {
        "family": "sans-serif",
        "style": "normal",
        "variant": "normal",
        "stretch": 400,
        "weight": 400,
        "size": 15
    }
    values_six = {
        "family": "sans-serif",
        "style": "normal",
        "variant": "normal",
        "stretch": 300,
        "weight": 300,
        "size": 13
    }
    values_seven = {
        "family": "sans-serif",
        "style": "normal",
        "variant": "normal",
        "stretch": 300,
        "weight": 300,
        "size": 10
    }
    values_eight = {
        "family": "sans-serif",
        "style": "normal",
        "variant": "normal",
        "stretch": 200,
        "weight": 200,
        "size": 7
    }
    values_nine = {
        "family": "sans-serif",
        "style": "normal",
        "variant": "normal",
        "stretch": 150,
        "weight": 150,
        "size": 5
    }
    values_ten = {
        "family": "sans-serif",
        "style": "normal",
        "variant": "normal",
        "stretch": 100,
        "weight": 100,
        "size": 3
    }
    # Define font properties.
    properties_one = matplotlib.font_manager.FontProperties(
        family=values_one["family"],
        style=values_one["style"],
        variant=values_one["variant"],
        stretch=values_one["stretch"],
        weight=values_one["weight"],
        size=values_one["size"]
    )
    properties_two = matplotlib.font_manager.FontProperties(
        family=values_two["family"],
        style=values_two["style"],
        variant=values_two["variant"],
        stretch=values_two["stretch"],
        weight=values_two["weight"],
        size=values_two["size"]
    )
    properties_three = matplotlib.font_manager.FontProperties(
        family=values_three["family"],
        style=values_three["style"],
        variant=values_three["variant"],
        stretch=values_three["stretch"],
        weight=values_three["weight"],
        size=values_three["size"]
    )
    properties_four = matplotlib.font_manager.FontProperties(
        family=values_four["family"],
        style=values_four["style"],
        variant=values_four["variant"],
        stretch=values_four["stretch"],
        weight=values_four["weight"],
        size=values_four["size"]
    )
    properties_five = matplotlib.font_manager.FontProperties(
        family=values_five["family"],
        style=values_five["style"],
        variant=values_five["variant"],
        stretch=values_five["stretch"],
        weight=values_five["weight"],
        size=values_five["size"]
    )
    properties_six = matplotlib.font_manager.FontProperties(
        family=values_six["family"],
        style=values_six["style"],
        variant=values_six["variant"],
        stretch=values_six["stretch"],
        weight=values_six["weight"],
        size=values_six["size"]
    )
    properties_seven = matplotlib.font_manager.FontProperties(
        family=values_seven["family"],
        style=values_seven["style"],
        variant=values_seven["variant"],
        stretch=values_seven["stretch"],
        weight=values_seven["weight"],
        size=values_seven["size"]
    )
    properties_eight = matplotlib.font_manager.FontProperties(
        family=values_eight["family"],
        style=values_eight["style"],
        variant=values_eight["variant"],
        stretch=values_eight["stretch"],
        weight=values_eight["weight"],
        size=values_eight["size"]
    )
    properties_nine = matplotlib.font_manager.FontProperties(
        family=values_nine["family"],
        style=values_nine["style"],
        variant=values_nine["variant"],
        stretch=values_nine["stretch"],
        weight=values_nine["weight"],
        size=values_nine["size"]
    )
    properties_ten = matplotlib.font_manager.FontProperties(
        family=values_ten["family"],
        style=values_ten["style"],
        variant=values_ten["variant"],
        stretch=values_ten["stretch"],
        weight=values_ten["weight"],
        size=values_ten["size"]
    )
    # Compile and return references.
    return {
        "values": {
            "one": values_one,
            "two": values_two,
            "three": values_three,
            "four": values_four,
            "five": values_five,
            "six": values_six,
            "seven": values_seven,
            "eight": values_eight,
            "nine": values_nine,
            "ten": values_ten,
        },
        "properties": {
            "one": properties_one,
            "two": properties_two,
            "three": properties_three,
            "four": properties_four,
            "five": properties_five,
            "six": properties_six,
            "seven": properties_seven,
            "eight": properties_eight,
            "nine": properties_nine,
            "ten": properties_ten,
        }
    }


def define_color_properties():
    """
    Defines color properties.

    arguments:

    raises:

    returns:
        (dict<tuple>): references to definitions of color properties

    """

    # Black.
    black = (0.0, 0.0, 0.0, 1.0)
    # Gray.
    gray = (0.7, 0.7, 0.7, 1.0)
    # White.
    white = (1.0, 1.0, 1.0, 1.0)
    white_faint = (1.0, 1.0, 1.0, 0.75)
    # Clear.
    clear = (1.0, 1.0, 1.0, 0.0)
    clear_faint = (1.0, 1.0, 1.0, 0.25)
    # Blue.
    blue = (0.0, 0.2, 0.5, 1.0)
    blue_faint = (0.0, 0.2, 0.5, 0.75)
    # Orange.
    orange = (1.0, 0.6, 0.2, 1.0)
    orange_faint = (1.0, 0.6, 0.2, 0.75)
    # Compile and return references.
    return {
        "black": black,
        "gray": gray,
        "white": white,
        "white_faint": white_faint,
        "clear": clear,
        "clear_faint": clear_faint,
        "blue": blue,
        "blue_faint": blue_faint,
        "orange": orange,
        "orange_faint": orange_faint
    }



def write_figure_png(path=None, figure=None):
    """
    Writes figure to file.

    arguments:
        path (str): path to directory and file
        figure (object): figure object

    raises:

    returns:

    """

    # Write information to file.
    figure.savefig(
        path,
        format="png",
        dpi=300,
        facecolor="w",
        edgecolor="w",
        transparent=False
    )
    pass






# Utility...


def read_file_text(
    path_file=None
):
    """
    Reads information from file as a text string.

    arguments:
        path_file (str): path to directory and file

    returns:
        (str): information from file

    raises:

    """

    # Read information from file
    #with open(path_file_source, "r") as file_source:
    #    content = file_source.read()
    with open(path_file, "r") as file_source:
        content = file_source.read()
    # Return information
    return content


def read_file_text_list(
    delimiter=None,
    path_file=None
):
    """
    Reads and organizes source information from file.

    Delimiters include "\n", "\t", ",", " ".

    arguments:
        delimiter (str): delimiter between elements in list
        path_file (str): path to directory and file

    returns:
        (list<str>): information from file

    raises:

    """

    # Read information from file
    content = read_file_text(path_file=path_file)
    # Split content by line delimiters.
    values_split = content.split(delimiter)
    values_strip = list(map(lambda value: value.strip(), values_split))
    # Return information
    return values_strip


# This stuff

# TODO: currently uses hard-coded column names... not good
# TODO: read in column names from last row
# TODO: also need to handle multi-instance columns, either taking the mean or only the most recent one...
def read_source(dock=None):
    """
    Reads and organizes source information from file

    arguments:
        dock (str): path to root or dock directory for source and product
            directories and files

    raises:

    returns:
        (object): source information

    """

    # Specify directories and files.
    path_variables = os.path.join(
        dock, "albumin", "variables.txt"
    )
    path_data_raw = os.path.join(
        dock, "albumin", "data_raw.csv"
    )
    # Read information from file.
    variables = read_file_text_list(
        delimiter="\n",
        path_file=path_variables,
    )
    variables_sort = sorted(variables, reverse=False)
    variables_sort.insert(0, "person")
    variables_sort.append("unknown")
    variables_sort.append("person_extra")
    data_raw = pandas.read_csv(
        path_data_raw,
        sep=",", # ",", "\t"
        header=None,
        names=["person", "sex", "age", "albumin", "albumin_extra", "person_extra"],
        skipfooter=1,
    )

    # Compile and return information.
    return {
        "variables": variables_sort,
        "data_raw": data_raw,
    }





# Stratification

def determine_stratification_bin_thresholds(
    bin=None,
    values_sort=None,
    indices=None,
    thresholds=None,
    report=None,
):
    """
    Determine values of thresholds for three stratification bins.
    Lower and upper thresholds for a bin cannot be identical.

    arguments:
        bin (list<float>): proportions for one stratification bin
        values_sort (list<float>): values of continuous variable in ascending
            sort order
        indices (list<list<int>>): indices for each low and high threshold
        thresholds (list<list<float>>): thresholds for bins
        report (bool): whether to print reports

    raises:

    returns:
        (list<list<int>>, list<list<float>>): indices, thresholds

    """

    # Count total values.
    count_total = len(values_sort)

    # Low threshold.
    count_low = round(bin[0] * count_total)
    if (count_low == 0):
        index_low = 0
    else:
        index_low = (count_low - 1)
    value_low = values_sort[index_low]
    # Ensure that low threshold is at least as great as the previous bin's high
    # threshold.
    if len(thresholds) > 0:
        if (value_low < thresholds[-1][1]):
            value_low = thresholds[-1][1]

    # High threshold.
    count_high = round(bin[1] * count_total)
    index_high = (count_high - 1)
    value_high = values_sort[index_high]
    # Ensure that high threshold is greater than low threshold.
    if value_low == value_high:
        # Iterate on values until finding the next greater value.
        while values_sort[index_high] == value_low:
            index_high += 1
        value_high = values_sort[index_high]

    # Collect indices.
    indices_bin = list()
    indices_bin.append(index_low)
    indices_bin.append(index_high)
    indices.append(indices_bin)
    # Collect thresholds.
    thresholds_bin = list()
    thresholds_bin.append(value_low)
    thresholds_bin.append(value_high)
    thresholds.append(thresholds_bin)
    # Report.
    if report:
        utility.print_terminal_partition(level=4)
        print("count_low: " + str(count_low))
        print("index_low: " + str(index_low))
        print("value_low: " + str(value_low))
        print("count_high: " + str(count_high))
        print("index_high: " + str(index_high))
        print("value_high: " + str(value_high))
    # Return information.
    return indices, thresholds


def collect_stratification_bins_thresholds(
    values=None,
    bins=None,
    report=None,
):
    """
    Determine values of thresholds for three stratification bins.
    Lower and upper thresholds for a bin cannot be identical.

    arguments:
        values (list<float>): values of continuous variable
        bins (list<list<float>>): proportions for three stratification bins
        report (bool): whether to print reports

    raises:

    returns:
        (list<list<int>>): values of thresholds for each stratification bin

    """

    # Organize values.
    values = copy.deepcopy(values)
    values_sort = sorted(values, reverse=False)
    # Collect thresholds.
    indices = list()
    thresholds = list()
    for bin in bins:
        # Determine low and high thresholds for bin.
        indices, thresholds = determine_stratification_bin_thresholds(
            bin=bin,
            values_sort=values_sort,
            indices=indices,
            thresholds=thresholds,
            report=report,
        )
    # Return information.
    return thresholds


def determine_stratification_bin(
    value=None,
    thresholds=None,
):
    """
    Stratify persons to ordinal bins by their values of continuous variables.

    arguments:
        value (float): value of continuous variable
        thresholds (list<list<int>>): values of thresholds for each
            stratification bin

    raises:

    returns:
        (int): integer bin

    """

    if not math.isnan(value):
        if (thresholds[0][0] <= value and value < thresholds[0][1]):
            return 0
        elif (thresholds[1][0] <= value and value < thresholds[1][1]):
            return 1
        elif len(thresholds) > 2:
            if (thresholds[2][0] <= value and value <= thresholds[2][1]):
                return 2
            else:
                return float("nan")
        else:
            return float("nan")
    else:
        return float("nan")


def stratify_persons_continuous_variable_ordinal(
    variable=None,
    variable_grade=None,
    bins=None,
    data_persons_properties=None,
    report=None,
):
    """
    Stratify persons to ordinal bins by their values of continuous variables.

    arguments:
        variable (str): name of continuous variable for stratification
        variable_grade (str): name for new ordinal variable
        bins (list<list<float>>): proportions for three stratification bins
        data_persons_properties (object): Pandas data frame of persons'
            properties
        report (bool): whether to print reports

    raises:

    returns:
        (object): Pandas data frame of information about persons

    """

    # Copy data.
    data = data_persons_properties.copy(deep=True)
    # Determine whether variable qualifies for stratification.
    series, values_unique = pandas.factorize(
        data[variable],
        sort=True
    )
    if len(values_unique) < 2:
        data[variable_grade] = float("nan")
    else:
        # Report.
        if report:
            utility.print_terminal_partition(level=2)
            print("variable: " + str(variable))
            utility.print_terminal_partition(level=2)
        # Determine thresholds for stratification bins.
        thresholds = collect_stratification_bins_thresholds(
            values=data[variable].to_list(),
            bins=bins,
            report=report,
        )
        # Determine bins.
        data[variable_grade] = data[variable].apply(
            lambda value:
                determine_stratification_bin(
                    value=value,
                    thresholds=thresholds,
                )
        )
        # Report.
        if report:
            utility.print_terminal_partition(level=2)
            for threshold in thresholds:
                print("low threshold: " + str(threshold[0]))
                print("high threshold: " + str(threshold[1]))
                utility.print_terminal_partition(level=3)
    # Return information.
    return data


# Sets of persons


def organize_persons_properties_sets(
    data_persons_properties=None,
    report=None,
):
    """
    Extracts identifiers of persons.

    arguments:
        data_persons_properties (object): Pandas data frame of persons'
            properties
        report (bool): whether to print reports

    raises:

    returns:
        (dict<list<str>>): identifiers of persons in groups by their properties

    """

    # Copy data.
    data_persons_properties = data_persons_properties.copy(deep=True)
    # Organize data.
    bin = dict()
    # Sex.
    bin["female"] = data_persons_properties.loc[
        data_persons_properties["sex"] == 0.0, :
    ].index.to_list()
    bin["male"] = data_persons_properties.loc[
        data_persons_properties["sex"] == 1.0, :
    ].index.to_list()
    # Age.
    bin["young"] = data_persons_properties.loc[
        data_persons_properties["age_grade"] == 0, :
    ].index.to_list()
    bin["old"] = data_persons_properties.loc[
        data_persons_properties["age_grade"] == 2, :
    ].index.to_list()
    # Report.
    if report:
        utility.print_terminal_partition(level=2)
        print("Count of persons in each group...")
        utility.print_terminal_partition(level=2)
        for group in bin.keys():
            #utility.print_terminal_partition(level=4)
            print(group + " persons: " + str(len(bin[group])))
            pass
        utility.print_terminal_partition(level=2)
        pass
    # Return information.
    return bin


def compare_signals_persons_groups_two(
    variable_identifier=None,
    comparison=None,
    group_1_persons=None,
    group_2_persons=None,
    group_1_label=None,
    group_2_label=None,
    data_persons_properties=None,
    report=None,
):
    """
    Organizes and combines information about dependent and independent
    variables for regression.

    arguments:
        variable_identifier (str): identifier of variable for signal
        comparison (str): name for comparison
        group_1_persons (list<str>): identifiers of persons in first group
        group_2_persons (list<str>): identifiers of persons in second group
        group_1_label (str): name of first group of persons
        group_2_label (str): name of first group of persons
        data_persons_properties (object): Pandas data frame of pan-tissue
            signals across genes and persons
        report (bool): whether to print reports

    raises:

    returns:
        (dict): information about comparison

    """

    # Compile information.
    bin = dict()
    bin["variable_identifier"] = variable_identifier
    bin["variable_name"] = "albumin"
    bin["comparison"] = comparison
    bin["title"] = str(bin["variable_name"] + "_" + comparison)
    bin["group_1_persons"] = len(group_1_persons)
    bin["group_2_persons"] = len(group_2_persons)
    bin["group_1_label"] = group_1_label
    bin["group_2_label"] = group_2_label
    # Copy data.
    data_signals = data_persons_properties.copy(deep=True)
    # Select data for persons in groups.
    data_group_1 = data_signals.loc[
        data_signals.index.isin(group_1_persons), :
    ]
    data_group_2 = data_signals.loc[
        data_signals.index.isin(group_2_persons), :
    ]
    # Select gene's signals for each group.
    bin["group_1_values"] = data_group_1[variable_identifier].dropna().to_numpy()
    bin["group_2_values"] = data_group_2[variable_identifier].dropna().to_numpy()
    bin["group_1_valids"] = bin["group_1_values"].size
    bin["group_2_valids"] = bin["group_2_values"].size
    # Calculate probability by t test.
    t_statistic, p_value = scipy.stats.ttest_ind(
        bin["group_1_values"],
        bin["group_2_values"],
        equal_var=True,
        nan_policy="omit",
    )
    bin["probability"] = p_value
    # Report.
    if report:
        utility.print_terminal_partition(level=2)
        print("variable: " + bin["variable_name"])
        print("comparison: " + bin["comparison"])
        print(
            bin["group_1_label"] + " (" + str(bin["group_1_valids"]) + ")" +
            " versus " +
            bin["group_2_label"] + " (" + str(bin["group_2_valids"]) + ")"
        )
        print("t test p-value: " + str(bin["probability"]))
    # Return information.
    return bin


def organize_person_two_groups_signal_comparisons(
    sets_persons=None,
    data_persons_properties=None,
    report=None,
):
    """
    Organizes and comparisons between two groups across multiple genes.

    arguments:
        sets_persons (dict<list<str>>): identifiers of persons in groups by
            their properties
        data_persons_properties (object): Pandas data frame of pan-tissue
            signals across genes and persons
        report (bool): whether to print reports

    raises:

    returns:
        (list<dict>): information about comparisons

    """

    comparisons = list()
    comparisons.append(compare_signals_persons_groups_two(
        variable_identifier="albumin",
        comparison="sex",
        group_1_persons=sets_persons["female"],
        group_2_persons=sets_persons["male"],
        group_1_label="female",
        group_2_label="male",
        data_persons_properties=data_persons_properties,
        report=report,
    ))
    comparisons.append(compare_signals_persons_groups_two(
        variable_identifier="albumin",
        comparison="age",
        group_1_persons=sets_persons["young"],
        group_2_persons=sets_persons["old"],
        group_1_label="young",
        group_2_label="old",
        data_persons_properties=data_persons_properties,
        report=report,
    ))
    return comparisons




##########
# Box plots


def plot_boxes(
    arrays=None,
    labels_groups=None,
    label_vertical=None,
    label_horizontal=None,
    label_top_center=None,
    label_top_left=None,
    label_top_right=None,
    orientation=None,
    fonts=None,
    colors=None,
):
    """
    Creates a figure of a chart of type histogram to represent the frequency
    distribution of a single series of values.

    arguments:
        arrays (list<array>): NumPy arrays of values for each group
        labels_groups (list<str>): labels for each group
        label_vertical (str): label for vertical axis
        label_horizontal (str): label for horizontal axis
        label_top_center (str): label for top center of plot area
        label_top_left (str): label for top left of plot area
        label_top_right (str): label for top right of plot area
        orientation (str): orientation of figure, either "portrait" or
            "landscape"
        fonts (dict<object>): references to definitions of font properties
        colors (dict<tuple>): references to definitions of color properties

    raises:

    returns:
        (object): figure object

    """

    # Define colors.
    color_count = len(arrays)
    if color_count == 1:
        colors_series = [colors["blue"]]
    elif color_count == 2:
        colors_series = [colors["gray"], colors["blue"]]
    elif color_count == 3:
        colors_series = [colors["gray"], colors["blue"], colors["orange"]]
    elif color_count > 3:
        colors_series = list(
            seaborn.color_palette("hls", n_colors=color_count)
        )
    # Create figure.
    if orientation == "portrait":
        figure = matplotlib.pyplot.figure(
            figsize=(11.811, 15.748),
            tight_layout=True
        )
    elif orientation == "landscape":
        figure = matplotlib.pyplot.figure(
            figsize=(15.748, 11.811),
            tight_layout=True
        )
    # Create axes.
    axes = matplotlib.pyplot.axes()
    # Create boxes.
    handle = axes.boxplot(
        arrays,
        notch=False,
        vert=True,
        widths=0.7,
        patch_artist=True,
        labels=labels_groups,
        manage_ticks=True,
    )
    # Fill boxes with colors.
    for box_patch, color_box in zip(handle["boxes"], colors_series):
        box_patch.set_facecolor(color_box)
        pass
    # Label axes.
    axes.set_ylabel(
        ylabel=label_vertical,
        labelpad=20,
        alpha=1.0,
        backgroundcolor=colors["white"],
        color=colors["black"],
        fontproperties=fonts["properties"]["two"]
    )
    if len(label_horizontal) > 0:
        axes.set_xlabel(
            xlabel=label_horizontal,
            labelpad=20,
            alpha=1.0,
            backgroundcolor=colors["white"],
            color=colors["black"],
            fontproperties=fonts["properties"]["one"],
            rotation="horizontal",
        )
    axes.tick_params(
        axis="both",
        which="both",
        direction="out",
        length=5.0,
        width=3.0,
        color=colors["black"],
        pad=5,
        labelsize=fonts["values"]["two"]["size"],
        labelcolor=colors["black"]
    )
    if len(label_top_center) > 0:
        axes.text(
            0.5,
            0.9,
            label_top_center,
            horizontalalignment="center",
            verticalalignment="top",
            transform=axes.transAxes,
            backgroundcolor=colors["white"],
            color=colors["black"],
            fontproperties=fonts["properties"]["one"]
        )
    if len(label_top_left) > 0:
        axes.text(
            0.25,
            0.9,
            label_top_left,
            horizontalalignment="center",
            verticalalignment="top",
            transform=axes.transAxes,
            backgroundcolor=colors["white"],
            color=colors["black"],
            fontproperties=fonts["properties"]["two"]
        )
    if len(label_top_right) > 0:
        axes.text(
            0.75,
            0.9,
            label_top_right,
            horizontalalignment="center",
            verticalalignment="top",
            transform=axes.transAxes,
            backgroundcolor=colors["white"],
            color=colors["black"],
            fontproperties=fonts["properties"]["two"]
        )
    return figure


def plot_chart_genes_signals_persons_two_groups_comparison(
    comparison=None,
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
        path_directory, str(comparison["title"] + ".png")
    )
    # Organize group labels.
    label_1 = str(
        comparison["group_1_label"] +
        " (" + str(comparison["group_1_valids"]) + ")"
    )
    label_2 = str(
        comparison["group_2_label"] +
        " (" + str(comparison["group_2_valids"]) + ")"
    )
    labels_groups = [label_1, label_2]

    # Define fonts.
    fonts = define_font_properties()
    # Define colors.
    colors = define_color_properties()

    # Create figure.
    figure = plot_boxes(
        arrays=[comparison["group_1_values"], comparison["group_2_values"]],
        labels_groups=labels_groups,
        label_vertical=str(comparison["variable_name"] + " in blood"),
        label_horizontal="",
        label_top_center=str("p: " + numpy.format_float_scientific(
            comparison["probability"], precision=3
        )),
        label_top_left="",
        label_top_right="",
        orientation="portrait",
        fonts=fonts,
        colors=colors,
    )
    # Write figure.
    write_figure_png(
        path=path_file,
        figure=figure
    )

    pass


def prepare_charts_genes_signals_persons_groups(
    comparisons=None,
    dock=None,
):
    """
    Plots charts from the analysis process.

    arguments:
        comparisons (object): info
        dock (str): path to root or dock directory for source and product
            directories and files

    raises:

    returns:

    """

    # Specify directories and files.
    path_plot = os.path.join(dock, "plot")
    utility.create_directory(path_plot)
    path_directory = os.path.join(path_plot, "sets")
    utility.remove_directory(path=path_directory)
    utility.create_directories(path=path_directory)
    # Create figures.
    for comparison in comparisons:
        plot_chart_genes_signals_persons_two_groups_comparison(
            comparison=comparison,
            path_directory=path_directory,
        )
        pass
    pass


def organize_plot_persons_sets_boxes(
    sets_persons=None,
    data=None,
    temporary=None,
    dock=None,
):
    """
    Function to execute module's main behavior.

    arguments:
        sets_persons (dict<list<str>>): identifiers of persons in groups by
            their properties
        data (object): Pandas data frame of persons' properties
        temporary (str): path to temporary directory for source and product
            directories and files
        dock (str): path to dock directory for source and product
            directories and files

    raises:

    returns:

    """

    comparisons_two = organize_person_two_groups_signal_comparisons(
        sets_persons=sets_persons,
        data_persons_properties=data,
        report=True,
    )
    prepare_charts_genes_signals_persons_groups(
        comparisons=comparisons_two,
        dock=dock,
    )

    pass


##########
# Scatter plots



def plot_scatter(
    data=None,
    abscissa=None,
    ordinate=None,
    title_abscissa=None,
    title_ordinate=None,
    fonts=None,
    colors=None,
    size=None,
):
    """
    Creates a figure of a chart of type scatter.

    arguments:
        data (object): Pandas data frame of groups, series, and values
        abscissa (str): name of data column with variable for horizontal (x)
            axis
        ordinate (str): name of data column with variable for vertical (y) axis
        title_abscissa (str): title for abscissa on horizontal axis
        title_ordinate (str): title for ordinate on vertical axis
        factor (str): name of data column with groups or factors of samples
        fonts (dict<object>): references to definitions of font properties
        colors (dict<tuple>): references to definitions of color properties
        size (int): size of marker

    raises:

    returns:
        (object): figure object

    """

    # Organize data.
    data_copy = data.copy(deep=True)
    data_selection = data_copy.loc[:, [abscissa, ordinate]]
    data_selection.dropna(
        axis="index",
        how="any",
        inplace=True,
    )
    values_abscissa = data_selection[abscissa].values
    values_ordinate = data_selection[ordinate].values

    ##########
    # Create figure.
    figure = matplotlib.pyplot.figure(
        figsize=(15.748, 11.811),
        tight_layout=True
    )
    # Create axes.
    axes = matplotlib.pyplot.axes()
    axes.set_xlabel(
        xlabel=title_abscissa,
        labelpad=20,
        alpha=1.0,
        backgroundcolor=colors["white"],
        color=colors["black"],
        fontproperties=fonts["properties"]["one"]
    )
    axes.set_ylabel(
        ylabel=title_ordinate,
        labelpad=20,
        alpha=1.0,
        backgroundcolor=colors["white"],
        color=colors["black"],
        fontproperties=fonts["properties"]["one"]
    )
    axes.tick_params(
        axis="both",
        which="both",
        direction="out",
        length=5.0,
        width=3.0,
        color=colors["black"],
        pad=5,
        labelsize=fonts["values"]["one"]["size"],
        labelcolor=colors["black"]
    )
    # Plot points for values from each group.
    handle = axes.plot(
        values_abscissa,
        values_ordinate,
        linestyle="",
        marker="o",
        markersize=size, # 5, 15
        markeredgecolor=colors["blue"],
        markerfacecolor=colors["blue"]
    )

    # Return figure.
    return figure


def plot_chart_persons_sex_age_albumin(
    data=None,
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
    fonts = define_font_properties()
    # Define colors.
    colors = define_color_properties()

    # Create figure.
    figure = plot_scatter(
        data=data,
        abscissa="age",
        ordinate="albumin",
        title_abscissa="age in years",
        title_ordinate="blood albumin in g/L",
        fonts=fonts,
        colors=colors,
        size=7,
    )
    # Write figure.
    write_figure_png(
        path=path_file,
        figure=figure
    )

    pass


def prepare_charts_persons_sex_age_albumin(
    data_female=None,
    data_male=None,
    dock=None,
):
    """
    Plots charts from the analysis process.

    arguments:
        comparisons (object): info
        dock (str): path to root or dock directory for source and product
            directories and files

    raises:

    returns:

    """

    # Specify directories and files.
    path_plot = os.path.join(dock, "plot")
    utility.create_directory(path_plot)
    path_directory = os.path.join(path_plot, "scatter")
    utility.remove_directory(path=path_directory)
    utility.create_directories(path=path_directory)
    # Create figures.
    plot_chart_persons_sex_age_albumin(
        data=data_female,
        file="female_age_albumin.png",
        path_directory=path_directory,
    )
    plot_chart_persons_sex_age_albumin(
        data=data_male,
        file="male_age_albumin.png",
        path_directory=path_directory,
    )
    pass


def organize_plot_persons_sets_scatter(
    sets_persons=None,
    data=None,
    temporary=None,
    dock=None,
):
    """
    Function to execute module's main behavior.

    arguments:
        sets_persons (dict<list<str>>): identifiers of persons in groups by
            their properties
        data (object): Pandas data frame of persons' properties
        temporary (str): path to temporary directory for source and product
            directories and files
        dock (str): path to dock directory for source and product
            directories and files

    raises:

    returns:

    """

    # Select data for persons in groups.
    data_female = data.loc[
        data.index.isin(sets_persons["female"]), :
    ]
    data_male = data.loc[
        data.index.isin(sets_persons["male"]), :
    ]
    prepare_charts_persons_sex_age_albumin(
        data_female=data_female,
        data_male=data_male,
        dock=dock,
    )

    pass


def plot_distribution_histogram(
    series=None,
    name=None,
    bin_method=None,
    bin_count=None,
    label_bins=None,
    label_counts=None,
    fonts=None,
    colors=None,
    line=None,
    position=None,
    text=None,
):
    """
    Creates a figure of a chart of type histogram to represent the frequency
    distribution of a single series of values.

    arguments:
        series (list<float>): series of counts
        name (str): name of series
        bin_method (str): method to define bins
        bin_count (int): count of bins to define and populate
        label_bins (str): label for bins
        label_counts (str): label for counts
        fonts (dict<object>): references to definitions of font properties
        colors (dict<tuple>): references to definitions of color properties
        line (bool): whether to draw a vertical line
        position (float): position for vertical line
        text (str): text to include on figure

    raises:

    returns:
        (object): figure object

    """

    # Define and populate bins.
    # Bin method "auto" is useful.
    #values, edges = numpy.histogram(series, bins=count_bins)
    if bin_method == "count":
        bin_edges = numpy.histogram_bin_edges(series, bins=bin_count)
    else:
        bin_edges = numpy.histogram_bin_edges(series, bins=bin_method)

    # Create figure.
    figure = matplotlib.pyplot.figure(
        figsize=(15.748, 11.811),
        tight_layout=True
    )
    axes = matplotlib.pyplot.axes()
    values, bins, patches = axes.hist(
        series,
        bins=bin_edges,
        histtype="bar",
        align="left",
        orientation="vertical",
        rwidth=0.35,
        log=False,
        color=colors["blue"],
        label=name,
        stacked=False
    )
    if False:
        axes.set_title(
            name,
            #fontdict=fonts["properties"]["one"],
            loc="center",
        )
        axes.legend(
            loc="upper right",
            markerscale=2.5,
            markerfirst=True,
            prop=fonts["properties"]["one"],
            edgecolor=colors["black"]
        )
    axes.set_xlabel(
        xlabel=label_bins,
        labelpad=20,
        alpha=1.0,
        backgroundcolor=colors["white"],
        color=colors["black"],
        fontproperties=fonts["properties"]["one"]
    )
    axes.set_ylabel(
        ylabel=label_counts,
        labelpad=20,
        alpha=1.0,
        backgroundcolor=colors["white"],
        color=colors["black"],
        fontproperties=fonts["properties"]["two"]
    )
    axes.tick_params(
        axis="both",
        which="both",
        direction="out",
        length=5.0,
        width=3.0,
        color=colors["black"],
        pad=5,
        labelsize=fonts["values"]["two"]["size"],
        labelcolor=colors["black"]
    )
    if line:
        axes.axvline(
            x=position,
            ymin=0,
            ymax=1,
            alpha=1.0,
            color=colors["orange"],
            linestyle="--",
            linewidth=5.0, # 3.0, 7.5
        )
    if len(text) > 0:
        matplotlib.pyplot.text(
            1,
            1,
            text,
            horizontalalignment="right",
            verticalalignment="top",
            transform=axes.transAxes,
            backgroundcolor=colors["white"],
            color=colors["black"],
            fontproperties=fonts["properties"]["one"]
        )
    return figure


def plot_chart_persons_sex_age_albumin_histogram(
    data=None,
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
    fonts = define_font_properties()
    # Define colors.
    colors = define_color_properties()

    # Create figure.
    figure = plot_distribution_histogram(
        series=data["albumin"].to_list(),
        name="",
        bin_method="count",
        bin_count=70,
        label_bins="blood albumin in g/L",
        label_counts="counts of persons per bin",
        fonts=fonts,
        colors=colors,
        line=False,
        position=1,
        text="",
    )
    # Write figure.
    write_figure_png(
        path=path_file,
        figure=figure
    )

    pass



def prepare_charts_persons_sex_age_albumin_histograms(
    data_female=None,
    data_male=None,
    data_young=None,
    data_old=None,
    dock=None,
):
    """
    Plots charts from the analysis process.

    arguments:
        comparisons (object): info
        dock (str): path to root or dock directory for source and product
            directories and files

    raises:

    returns:

    """

    # Specify directories and files.
    path_plot = os.path.join(dock, "plot")
    utility.create_directory(path_plot)
    path_directory = os.path.join(path_plot, "histogram")
    utility.remove_directory(path=path_directory)
    utility.create_directories(path=path_directory)
    # Create figures.
    plot_chart_persons_sex_age_albumin_histogram(
        data=data_female,
        file="histogram_female_albumin.png",
        path_directory=path_directory,
    )
    plot_chart_persons_sex_age_albumin_histogram(
        data=data_male,
        file="histogram_male_albumin.png",
        path_directory=path_directory,
    )
    plot_chart_persons_sex_age_albumin_histogram(
        data=data_young,
        file="histogram_young_albumin.png",
        path_directory=path_directory,
    )
    plot_chart_persons_sex_age_albumin_histogram(
        data=data_old,
        file="histogram_old_albumin.png",
        path_directory=path_directory,
    )
    pass


def organize_plot_persons_sets_histograms(
    sets_persons=None,
    data=None,
    temporary=None,
    dock=None,
):
    """
    Function to execute module's main behavior.

    arguments:
        sets_persons (dict<list<str>>): identifiers of persons in groups by
            their properties
        data (object): Pandas data frame of persons' properties
        temporary (str): path to temporary directory for source and product
            directories and files
        dock (str): path to dock directory for source and product
            directories and files

    raises:

    returns:

    """

    # Select data for persons in groups.
    data_female = data.loc[
        data.index.isin(sets_persons["female"]), :
    ]
    data_male = data.loc[
        data.index.isin(sets_persons["male"]), :
    ]
    data_young = data.loc[
        data.index.isin(sets_persons["young"]), :
    ]
    data_old = data.loc[
        data.index.isin(sets_persons["old"]), :
    ]
    prepare_charts_persons_sex_age_albumin_histograms(
        data_female=data_female,
        data_male=data_male,
        data_young=data_young,
        data_old=data_old,
        dock=dock,
    )

    pass



def organize_plot_person_sets(
    data=None,
    temporary=None,
    dock=None,
):
    """
    Function to execute module's main behavior.

    arguments:
        data (object): Pandas data frame of persons' properties
        temporary (str): path to temporary directory for source and product
            directories and files
        dock (str): path to dock directory for source and product
            directories and files

    raises:

    returns:

    """

    # Copy data.
    data = data.copy(deep=True)
    # Determine bins of persons by age.
    data_age = stratify_persons_continuous_variable_ordinal(
        variable="age",
        variable_grade="age_grade",
        bins=[[0.0, 0.33], [0.33, 0.67], [0.67, 1.0]],
        data_persons_properties=data,
        report=True,
    )
    # Organize sets of persons by their properties.
    sets_persons = organize_persons_properties_sets(
        data_persons_properties=data_age,
        report=True,
    )

    # Organize and plot boxes.
    organize_plot_persons_sets_boxes(
        sets_persons=sets_persons,
        data=data_age,
        temporary=temporary,
        dock=dock,
    )

    # Organize and plot scatters.
    organize_plot_persons_sets_scatter(
        sets_persons=sets_persons,
        data=data_age,
        temporary=temporary,
        dock=dock,
    )
    # histograms
    organize_plot_persons_sets_histograms(
        sets_persons=sets_persons,
        data=data_age,
        temporary=temporary,
        dock=dock,
    )
    pass


# Regression


def standardize_scale_variables(
    variables=None,
    data_persons_properties=None,
):
    """
    Standardizes variables' values to z-score scale.

    arguments:
        variables (list<str>): names of numerical variables
        data_persons_properties_raw (object): Pandas data frame of persons'
            properties

    raises:

    returns:
        (object): Pandas data frame of information about persons

    """

    # Copy data.
    data = data_persons_properties.copy(deep=True)
    # Iterate on variables.
    for variable in variables:
        variable_scale = str(variable + ("_scale"))
        data[variable] = data[variable].astype(numpy.float32)
        data[variable_scale] = data[variable].pipe(
            lambda series: scipy.stats.zscore(
                series.to_numpy(),
                axis=0,
                ddof=1, # Sample standard deviation.
                nan_policy="omit",
            ),
        )
        pass
    # Return information.
    return data


def regress_signal_ordinary_residuals(
    dependence=None,
    independence=None,
    proportion=None,
    data=None,
):
    """
    Regresses a quantitative continuous dependent variable against multiple
    independent variables and returns relevant parameters and statistics.

    Data format must have observations across rows and dependent and
    independent variables (features) across columns.

    Description of formats for StatsModels...

    Format of dependent variable is a vector of scalar values.
    [1.3, 1.5, 1.2, 1.0, 1.7, 1.5, 1.9, 1.1, 1.3, 1.4]

    Format of independent variable(s) is a matrix: a first dimension vector of
    observations and for each observation a second dimension vector of scalar
    values.
    StatsModels also requires a constant for the intercept.
    [
        [1.3, 5.2, 1.0],
        [1.5, 5.1, 1.0],
        [1.2, 5.5, 1.0],
        ...
    ]

    Description of formats for SKLearn...

    Format of dependent variable is an array of observations, and each
    observation is an array of features.
    [
        [1.3],
        [1.5],
        [1.2],
        ...
    ]

    arguments:
        dependence (str): name of dependent variable
        independence (list<str>): names of independent variables
        proportion (float): minimal proportion of total observations that must
            have nonmissing values
        data (object): Pandas data frame of values and associations between
            dependent and independent variables

    raises:

    returns:
        (dict): collection of residuals for regression summary of information
            about regression model


    """

    # Organize data.
    data = data.copy(deep=True)
    # Determine minimal count of observations.
    count = data.shape[0]
    threshold = proportion * count
    # Remove observations with any missing values.
    columns = copy.deepcopy(independence)
    columns.insert(0, dependence)
    data = data.loc[
        :, data.columns.isin(columns)
    ]
    data.dropna(
        axis="index",
        how="any",
        #subset=[dependence],
        inplace=True,
    )
    data = data[[*columns]]

    # Note
    # It is very important to keep track of the order of independent variables
    # in order to match parameters and probabilities to the correct variables.

    # Determine whether data have sufficient observations for regression.
    if data.shape[0] > threshold:
        # Extract values of dependent and independent variables.
        values_dependence = data[dependence].to_numpy()
        #values_independence = data.loc[ :, independence].to_numpy()
        data_independence = data.loc[ :, independence]
        # Introduce constant value for intercept.
        # If any column in the independent variables already has constant
        # values, then the function skips it by default.
        # It is necessary to change parameter "has_constant" to avoid this
        # conditional behavior.
        data_independence_intercept = statsmodels.api.add_constant(
            data_independence,
            prepend=True, # insert intercept constant first
            has_constant="add", # Introduce new intercept constant regardless
        )
        # Define model.
        model = statsmodels.api.OLS(
            values_dependence,
            data_independence_intercept,
            missing="drop",
        )
        report = model.fit()
        utility.print_terminal_partition(level=2)
        #print(data)
        #print(independence)
        #print(values_independence)
        print(report.summary())
        utility.print_terminal_partition(level=3)
        #print(dir(report))
        #print(report.params)
        #print(report.pvalues)

        # Organize residuals.
        residuals = report.resid
        # Collect parameters, probabilities, and statistics.
        report_parameters = pandas.Series(data=report.params)
        report_probabilities = pandas.Series(data=report.pvalues)
        parameters = dict()
        probabilities = dict()
        inflations = dict()
        if ("const" in report_parameters.index):
            #parameters["intercept_parameter"] = report.params[0]
            parameters["intercept_parameter"] = report_parameters["const"]
        else:
            parameters["intercept_parameter"] = float("nan")
            utility.print_terminal_partition(level=4)
            print("Warning: regression data does not have constant intercept.")
            print(dependence)
            utility.print_terminal_partition(level=4)
        if ("const" in report_probabilities.index):
            #probabilities["intercept_probability"] = report.pvalues[0]
            probabilities["intercept_probability"] = (
                report_probabilities["const"]
            )
        else:
            probabilities["intercept_probability"] = float("nan")
            utility.print_terminal_partition(level=4)
            print("Warning: regression data does not have constant intercept.")
            print(dependence)
            utility.print_terminal_partition(level=4)
        inflations["intercept_inflation"] = float("nan")
        # Iterate on each independent variable.
        # Initiate counter at 1 to assume that intercept is at index 0.
        counter = 1
        # Accommodate index for intercept.
        for variable in independence:
            # Coefficient or parameter.
            parameter = str(variable + ("_parameter"))
            #parameters[parameter] = report.params[counter]
            parameters[parameter] = report_parameters[variable]
            # Probability.
            probability = str(variable + ("_probability"))
            #probabilities[probability] = report.pvalues[counter]
            probabilities[probability] = report_probabilities[variable]
            # Variance Inflation Factor (VIF).
            inflation = str(variable + ("_inflation"))
            inflation_value = (
                statsmodels.stats.outliers_influence.variance_inflation_factor(
                    data_independence_intercept.to_numpy(),
                    counter
                )
            )
            inflations[inflation] = round(inflation_value, 2)
            # Increment index.
            counter += 1
            pass
        summary = {
            "freedom": report.df_model,
            "observations": report.nobs,
            "r_square": report.rsquared,
            "r_square_adjust": report.rsquared_adj,
            "log_likelihood": report.llf,
            "akaike": report.aic,
            "bayes": report.bic,
            "condition": report.condition_number,
        }
        summary.update(parameters)
        summary.update(probabilities)
        summary.update(inflations)
    else:
        # Compile information.
        #probabilities = list(
        #    itertools.repeat(float("nan"), len(values_independence_intercept))
        #)
        parameters = dict()
        probabilities = dict()
        inflations = dict()
        parameters["intercept_parameter"] = float("nan")
        probabilities["intercept_probability"] = float("nan")
        inflations["intercept_inflation"] = float("nan")
        for variable in independence:
            parameter = str(variable + ("_parameter"))
            parameters[parameter] = float("nan")
            probability = str(variable + ("_probability"))
            probabilities[probability] = float("nan")
            inflation = str(variable + ("_inflation"))
            inflations[inflation] = float("nan")
            pass
        summary = {
            "freedom": float("nan"),
            "observations": float("nan"),
            "r_square": float("nan"),
            "r_square_adjust": float("nan"),
            "log_likelihood": float("nan"),
            "akaike": float("nan"),
            "bayes": float("nan"),
            "condition": float("nan"),
        }
        summary.update(parameters)
        summary.update(probabilities)
        summary.update(inflations)
        residuals = numpy.empty(0)
    # Compile information.
    bin = dict()
    bin["report"] = summary
    bin["residuals"] = residuals
    # Return information.
    return bin


def organize_regression_persons_properties(
    data=None,
    temporary=None,
    dock=None,
):
    """
    Function to execute module's main behavior.

    arguments:
        data (object): Pandas data frame of persons' properties
        temporary (str): path to temporary directory for source and product
            directories and files
        dock (str): path to dock directory for source and product
            directories and files

    raises:

    returns:

    """

    # Copy data.
    data = data.copy(deep=True)
    # Scale age and albumin.
    data_scale = standardize_scale_variables(
        variables=["age", "albumin"],
        data_persons_properties=data,
    )
    # Select relevant varialbes.
    data_variables = data_scale.loc[
        :, data_scale.columns.isin([
            "sex", "age_scale", "albumin", "albumin_scale"
        ])
    ]
    # Regress.
    bin_case = regress_signal_ordinary_residuals(
        dependence="albumin",
        independence=["sex", "age_scale"],
        proportion=0.5,
        data=data_variables,
    )




    pass



###############################################################################
# Procedure


def execute_procedure(
    temporary=None,
    dock=None,
):
    """
    Function to execute module's main behavior.

    arguments:
        temporary (str): path to temporary directory for source and product
            directories and files
        dock (str): path to dock directory for source and product
            directories and files

    raises:

    returns:

    """

    # Read source information from file.
    source = read_source(dock=dock)
    print(source["data_raw"])

    # Organize data.
    data_raw = source["data_raw"].copy(deep=True)
    data_raw.drop(
        labels=[
            "albumin_extra", "person_extra",
        ],
        axis="columns",
        inplace=True
    )
    data_raw.set_index(
        "person",
        drop=True,
        inplace=True,
    )
    # Remove observations with missing values for either feature.
    data_raw.dropna(
        axis="index",
        how="any",
        inplace=True,
    )

    # Organize regression persons properties.
    organize_regression_persons_properties(
        data=data_raw,
        temporary=temporary,
        dock=dock,
    )

    # Organize plot person sets.
    organize_plot_person_sets(
        data=data_raw,
        temporary=temporary,
        dock=dock,
    )

    print("version check: 5")

    pass



if (__name__ == "__main__"):
    execute_procedure()
