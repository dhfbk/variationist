import argparse
import os
import sys

from src import utils
from src.data_handler import data_dispatcher


def import_args():
    """A function that defines and parses the command line arguments of Variationist.

    Returns
    -------
    args: argparse.Namespace
        An object holding command line arguments
    """
    parser = argparse.ArgumentParser()

    parser.add_argument("--dataset_filepath", "-D",
                        # @TODO: Eventually support the processing/comparison of multiple datasets
                        type=str, required=True,
                        help="Path to the csv/tsv file containing the data.")
    parser.add_argument("--text_cols", "-T",
                        required=True, nargs='+', 
                        help="List of column name(s) or index(es) indicating text data to be analyzed.\
                              In the case of multiple columns, provide names/indexes separated by space.\
                              Note that column names with spaces must be enclosed by quotation marks (e.g.,\
                              \"my col\"). If you provide indexes, we will consider 0 as the first column,\
                              1 as the second column, etc.")
    parser.add_argument("--label_cols", "-L",
                        type=str, required=False, nargs='+', 
                        help="List of column name(s) or index(es) indicating the labels to be analyzed.\
                              In the case of multiple columns, provide names/indexes separated by space.\
                              Note that column names with spaces must be enclosed by quotation marks (e.g.,\
                              \"my col\"). If none is provided, basic statistics at the text-only level\
                              will be computed. If you provide indexes, we will consider 0 as the first\
                              column, 1 as the second column, etc.")
    parser.add_argument("--metrics", "-M",
                        # @TODO: Specify a set of default metrics for unlabeled and labeled scenarios
                        type=str, required=False, default="most-frequent", nargs='+',
                        help="List of metric name(s) to compute.\
                              Possible metrics are: 'most-frequent', 'pmi'.")

    args = parser.parse_args()

    return args


def main():
    """A function that orchestrates all the operations of Variationist."""

    # Get values for the command line arguments
    args = import_args()

    # Check if the file exists: if not, exit
    if not os.path.isfile(args.dataset_filepath):
        sys.exit(f"ERROR! The file '{args.dataset_filepath}' does not exist. Exit.")

    # Check if column strings are names or indices (for both texts and labels)
    text_cols_type = utils.check_column_type(args.text_cols)
    label_cols_type = utils.check_column_type(args.label_cols)

    # Since the input file is the same, we require texts and labels columns to be of the same type
    if text_cols_type != label_cols_type:
        sys.exit(f"ERROR! text_cols are {text_cols_type} while label_cols are {label_cols_type}.\
            Please provide all column identifiers as names (as in the header line) or indexes.")
    cols_type = text_cols_type
    print(f"INFO: all column identifiers are treated as column {cols_type}.")

    # Read the input file and store its content in a pandas dataframe
    dataframe = utils.convert_file_to_dataframe(args.dataset_filepath, cols_type=cols_type)

    # Check if the specified columns are actually in the dataframe
    dataframe_cols = [col_name for col_name in dataframe.columns]
    for col in args.text_cols+args.label_cols:
        if col not in dataframe_cols:
            sys.exit(f"ERROR: the '{col}' column is not present in the dataframe.")

    # Create a dictionary containing the specified column strings (values) for texts and labels (keys)
    column_names_dict = {
        utils.TEXT_COLS_KEY: args.text_cols,
        utils.LABEL_COLS_KEY: args.label_cols
    }

    # Run the actual computation
    series_dict = data_dispatcher.process_dataset(
        dataframe, column_names_dict, metrics=args.metrics)


if __name__ == "__main__":
    main()

