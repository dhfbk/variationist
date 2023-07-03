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
                        # @TODO: Allow column indices too in the case of input files with no headers (be aware
                        # of possible clashes with column names that may actually be numbers)
                        type=str, required=True, nargs='+', 
                        help="List of column name(s) indicating text data to be analyzed.\
                              In the case of multiple columns, provide names separated by space.")
    parser.add_argument("--label_cols", "-L",
                        # @TODO: Allow column indices too in the case of input files with no headers (be aware
                        # of possible clashes with column names that may actually be numbers)
                        type=str, required=False, nargs='+', 
                        help="List of column name(s) indicating the labels to be analyzed.\
                              In the case of multiple columns, provide names separated by space.\
                              Note that if none is provided, only basic text-level statistics will be computed.")
    parser.add_argument("--metrics", "-M",
                        # @TODO: Specify a set of default metrics for unlabeled and labeled scenarios
                        type=str, required=False, default="most-frequent", nargs='+',
                        help="List of metric name(s) to compute.\
                              Possible metrics are: 'most-frequent', 'pmi'.")

    args = parser.parse_args()

    return args


def convert_file_to_dataframe(data_filepath):
    """A function that checks the data format, reads the input file, and store relevant 
    columns in a pandas dataframe. Files ending in ".tsv" and ".csv" are considered TSV and CSV files,
    respectively. By default, a file with no or different extension is considered a TSV file.

    Returns
    -------
    args: argparse.Namespace
        An object holding command line arguments
    """
    if data_filepath.lower().endswith('.tsv'):
        return pd.read_csv(data_filepath, sep="\t", quoting=csv.QUOTE_NONE, names=["label", "text"])
    elif data_filepath.lower().endswith('.csv'):
        return pd.read_csv(data_filepath, sep=",", names=["label", "text"])
    else:
        print("WARNING. '{data_filepath}' has no '.tsv' or '.csv' extension and will thus be considered\
            as a TSV file by default. If this is not expected, we suggest the user to convert their file\
            to either a '.tsv' or '.csv' format and run Variationist again.")
        return pd.read_csv(data_filepath, sep="\t", quoting=csv.QUOTE_NONE, names=["label", "text"])


def main():
    """A function that orchestrates all the operations of Variationist."""

    # Get values for the command line arguments
    args = import_args()

    # Check if the file exists: if not, exit
    if not os.path.isfile(args.dataset_filepath):
        sys.exit(f"ERROR! The file '{args.dataset_filepath}' does not exist. Exit.")

    # Read the input file and store relevant columns in a pandas dataframe
    # @TODO: add more options for file reading
    # e.g.: no header, only use some columns, use column names or indices etc...
    # for now I am supposing all datasets will have two columns, of which the first
    # containing the label and the second the text.
    dataframe = convert_file_to_dataframe(args.dataset_filepath)

    column_names_dict = {"text": args.text_cols,
                         "labels": args.label_cols}

    # Run the actual computation
    series_dict = data_dispatcher.process_dataset(dataframe,
                                                  column_names_dict,
                                                  metrics=args.metrics)


if __name__ == "__main__":
    main()

