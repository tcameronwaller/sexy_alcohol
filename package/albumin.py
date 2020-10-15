
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

#import plot
import utility


###############################################################################
# Functionality

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

    # T-tests

    # bar charts

    # histograms




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
        :, data_scale.columns.isin(["sex", "age_scale", "albumin_scale"])
    ]
    # Regress.
    bin_case = regress_signal_ordinary_residuals(
        dependence="albumin_scale",
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

    # Organize plot person sets.
    organize_plot_person_sets(
        data=data_raw,
        temporary=temporary,
        dock=dock,
    )

    # Organize regression persons properties.
    organize_regression_persons_properties(
        data=data_raw,
        temporary=temporary,
        dock=dock,
    )

    pass



if (__name__ == "__main__"):
    execute_procedure()
