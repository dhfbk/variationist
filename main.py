# import streamlit as st
import pandas as pd
import numpy as np
import argparse

from src.data_handler import preprocess
from src.data_handler import data_dispatcher
from src.methods import lexical_artifacts
# from src.visualization import visualizer


def import_args():
    """Define the command line arguments to use when running Variationist."""
    parser = argparse.ArgumentParser()
    parser.add_argument("dataset_filename", 
                        help="Path to the csv/tsv file containing the data.")
    parser.add_argument("--text_cols", nargs='+', 
                        help="List columns containing text data to be analyzed.")
    parser.add_argument("--label_cols", nargs='+', 
                        help="List columns containing the labels to be analyzed.")
    
    # This clearly has to be made easier. Right now it takes n arguments given by the user
    # of metrics to calculate. Ideally we could have flags for specific things that
    # one could want to measure. Also have a default set of tests to run.
    # It now does most frequent only as a default just as a placeholder, since this
    # was already there.
    parser.add_argument("--metrics", default="most-frequent", nargs='+',
                        help="List names of measures to apply to current dataset")
    
    # TODO add argument that lets the user input column names
    # TODO allow for users to only input indices of columns if the dataset has
    # no header and no column names are provided (see main())
    args = parser.parse_args()
    return args


def main():
    """Do main operations"""

    # import arguments    
    args = import_args()
    df_filename = args.dataset_filename
    text_columns = args.text_cols
    label_columns = args.label_cols
    metrics_to_do = args.metrics
    
    
    # read input file into pandas dataframe. 
    # TODO don't make TSV the default maybe? add more options for file reading
    # e.g.: no header, only use some columns, use column names or indices etc...
    # at the very least let's add a function that infers if tsv or csv based on
    # the file name.
    # for now I am supposing all datasets will have two columns, of which the first
    # containing the label and the second the text.
    dataframe = pd.read_csv(df_filename, sep="\t", names=["label", "text"])

    column_names_dict = {"text": text_columns,
                         "labels": label_columns}
    

    # Tokenize the text
    # TODO remove the streamlit stuff
    # @TODO: this should be executed only once: when streamlit reload the interface the dataset
    # is tokenized again and again (not sure, recheck)


    series_list = data_dispatcher.process_dataset(dataframe,
                                                  column_names_dict,
                                                  metrics=metrics_to_do)
    
    # @TODO: Check user input.

    # Create text input on the sidebar
    #label_of_interest = st.sidebar.text_input("Label of interest")

    # Create compute button on the sidebar
    # @TODO: After the last edits, this does not work anymore (to generalize)
    #st.sidebar.button(
    #    "Compute artifacts", 
    #    on_click=compute(uploaded_file, label_of_interest)
    #)


def compute(uploaded_file, label_of_interest):
    """"""

    if uploaded_file and label_of_interest:
        if uploaded_file is not None:
            # Convert input file to a string based IO
            stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))

            artifacts_df = calc_artifacts(stringio, label_of_interest)


if __name__ == "__main__":
    main()

