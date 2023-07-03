import argparse
import csv
import numpy as np
import os
import pandas as pd
import sys

from src.data_handler import preprocess
from src.data_handler import data_dispatcher
from src.methods import lexical_artifacts


def import_args():
    """A function that defines and parses the command line arguments of Variationist.

    Returns
    -------
    args: argparse.Namespace
        An object holding command line arguments
    """
    parser = argparse.ArgumentParser()

    parser.add_argument("--dataset_filepath", "-D",
                        type=str, required=True,
                        help="Path to the csv/tsv file containing the data.")
    parser.add_argument("--text_cols", "-T",
                        required=True, nargs='+', 
                        help="List of column name(s) or index(es) indicating text data to be analyzed.\
                              In the case of multiple columns, provide names/indexes separated by space.\
                              If you provide indexes, we will consider 1 as the first column, 2 as the second\
                              column, etc.")
    parser.add_argument("--label_cols", "-L",
                        type=str, required=False, nargs='+', 
                        help="List of column name(s) or index(es) indicating the labels to be analyzed.\
                              In the case of multiple columns, provide names/indexes separated by space.\
                              Note that if none is provided, only basic statistics at the text-only level\
                              will be computed. If you provide indexes, we will consider 1 as the first column,\
                              2 as the second column, etc.")
    parser.add_argument("--metrics", "-M",
                        # @TODO: Specify a set of default metrics for unlabeled and labeled scenarios
                        type=str, required=False, default="most-frequent", nargs='+',
                        help="List of metric name(s) to compute.\
                              Possible metrics are: 'most-frequent', 'pmi'.")

    args = parser.parse_args()

    return args


def convert_file_to_dataframe(data_filepath, cols_type):
    """A function that checks the data format, reads the input file, and store relevant 
    columns in a pandas dataframe. Files ending in ".tsv" and ".csv" are considered TSV and CSV files,
    respectively. By default, a file with no or different extension is considered a TSV file.

    Parameters
    ----------
    data_filepath: str
        A string denoting the path to the input dataset file
    cols_type: str
        A string denoting if the column identifiers have to be considered as names or indexes

    Returns
    -------
    dataframe: pandas.core.frame.DataFrame
        A Pandas dataframe containing all rows and the subset of the columns of interest
    """
    if data_filepath.lower().endswith('.tsv'):
        print(f"INFO: '{data_filepath}' is loaded as a TSV file.")
        # @TODO: Use cols_type in the function below to use or not headers or indexes
        return pd.read_csv(data_filepath, sep="\t", quoting=csv.QUOTE_NONE, names=["label", "text"])
    elif data_filepath.lower().endswith('.csv'):
        print(f"INFO: '{data_filepath}' is loaded as a CSV file.")
        # @TODO: Use cols_type in the function below to use or not headers or indexes
        return pd.read_csv(data_filepath, sep=",", names=["label", "text"])
    else:
        print(f"WARNING. '{data_filepath}' has no '.tsv' or '.csv' extension and will thus be considered\
            as a TSV file by default. If this is not expected, we suggest the user to convert their file\
            to either a '.tsv' or '.csv' format and run Variationist again.")
        # @TODO: Use cols_type in the function below to use or not headers or indexes
        return pd.read_csv(data_filepath, sep="\t", quoting=csv.QUOTE_NONE, names=["label", "text"])


def check_column_type(cols):
    """A function that checks if column identifiers in the input list have to be considered as names 
    or indexes. We employ a simple rule to determine it, namely if there is at least a numeric label
    in the list, the whole list is likely to comprise indexes, o.w., the list consists of name identifiers.

    Parameters
    ----------
    cols: List[str]
        A list of column identifiers as given by the relevant command line parameters

    Returns
    -------
    cols_type: str
        A string denoting if the column identifiers in the list have to be considered as names or indexes
    """
    cols_type = "names"
    for col in cols:
        if col.isnumeric():
            cols_type = "indexes"

    return cols_type


def main():
    """A function that orchestrates all the operations of Variationist."""

    # Get values for the command line arguments
    args = import_args()

    # Check if the file exists: if not, exit
    if not os.path.isfile(args.dataset_filepath):
        sys.exit(f"ERROR! The file '{args.dataset_filepath}' does not exist. Exit.")

    # Check if column identifiers are names or indices (for both texts and labels)
    text_cols_type = check_column_type(args.text_cols)
    label_cols_type = check_column_type(args.label_cols)

    # Since the input file is the same, we require texts and labels columns to be of the same type
    if text_cols_type != label_cols_type:
        sys.exit(f"ERROR! text_cols are {text_cols_type} while label_cols are {label_cols_type}.\
            Please provide all column identifiers as names (as in the header line) or indexes.")
    cols_type = text_cols_type
    print(f"INFO: all column identifiers are treated as column {cols_type}.")

    # Read the input file and store relevant columns in a pandas dataframe
    # @TODO: for now I am supposing all datasets will have two columns, of which the first
    # containing the label and the second the text. To be generalized to actual columns
    dataframe = convert_file_to_dataframe(args.dataset_filepath, cols_type=cols_type)

    column_names_dict = {"text": args.text_cols,
                         "labels": args.label_cols}

    # Run the actual computation
    series_dict = data_dispatcher.process_dataset(dataframe,
                                                  column_names_dict,
                                                  metrics=args.metrics)


if __name__ == "__main__":
    main()

