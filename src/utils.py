"""A python file containing project-wide constants and functions."""

import csv
import pandas as pd


# CONSTANTS
TEXT_COLS_KEY = "text"
LABEL_COLS_KEY = "labels"


def convert_file_to_dataframe(data_filepath, cols_type):
    """A function that, given an input filepath and information about the columns type (i.e., names or
    indexes), checks the format the file (csv, tsv, or other), reads it, and stores it in a pandas 
    dataframe. Files ending in ".tsv" and ".csv" are considered TSV and CSV files, respectively. By 
    default, a file with no (or other) extension is considered a TSV file. Input files with no header 
    are assigned index numbers as header, whereas column names are preserved in the ones with a header.

    Parameters
    ----------
    data_filepath: str
        A string denoting the path to an input dataset file
    cols_type: str
        A string denoting if the column strings are to be considered as names or indexes

    Returns
    -------
    dataframe: pandas.core.frame.DataFrame
        A Pandas dataframe with a header (either expressed with names or indexes)
    """
    if data_filepath.lower().endswith('.tsv'):
        print(f"INFO: '{data_filepath}' is loaded as a TSV file.")
        if cols_type == "names":
            dataframe = pd.read_csv(data_filepath, sep="\t", quoting=csv.QUOTE_NONE, header=0)
            print("INFO: given the provided column names, we consider the first line as the header.")
        else:
            dataframe = pd.read_csv(data_filepath, sep="\t", quoting=csv.QUOTE_NONE, header=None)
            dataframe.columns = dataframe.columns.astype(str)
            print("INFO: given the provided column indices, we add and use those as the header.")

    elif data_filepath.lower().endswith('.csv'):
        print(f"INFO: '{data_filepath}' is loaded as a CSV file.")
        if cols_type == "names":
            dataframe = pd.read_csv(data_filepath, sep=",", header=0)
            print("INFO: given the provided column names, we consider the first line as the header.")
        else:
            dataframe = pd.read_csv(data_filepath, sep=",", header=None)
            dataframe.columns = dataframe.columns.astype(str)
            print("INFO: given the provided column indices, we add and use those as the header.")

    else:
        print(f"WARNING. '{data_filepath}' has no '.tsv' or '.csv' extension and will thus be considered\
            as a TSV file by default. If this is not expected, we suggest the user to convert their file\
            to either a '.tsv' or '.csv' format and run Variationist again.")
        print(f"INFO: '{data_filepath}' is loaded as a TSV file.")
        if cols_type == "names":
            dataframe = pd.read_csv(data_filepath, sep="\t", quoting=csv.QUOTE_NONE, header=0)
            print("INFO: given the provided column names, we consider the first line as the header.")
        else:
            dataframe = pd.read_csv(data_filepath, sep="\t", quoting=csv.QUOTE_NONE, header=None)
            dataframe.columns = dataframe.columns.astype(str)
            print("INFO: given the provided column indices, we add and use those as the header.")

    return dataframe


def check_column_type(cols):
    """A function that checks if a list of column strings have to be considered as names or indexes. We 
    employ a simple rule to determine it: if there is at least a numeric string in the list of columns, 
    the whole comprises column indexes, o.w., the list consists of named columns.

    Parameters
    ----------
    cols: List[str]
        A list of column strings

    Returns
    -------
    cols_type: str
        A string that specifies how column strings in the list have to be considered: "names" or "indexes"
    """
    cols_type = "names"
    for col in cols:
        if col.isnumeric():
            cols_type = "indexes"
            break

    return cols_type