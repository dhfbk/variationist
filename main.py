import streamlit as st
import pandas as pd
import numpy as np

from src.data_handler import preprocess
from src.methods import lexical_artifacts
from src.visualization import visualizer


def calc_artifacts(string_data, label_of_interest):
    """"""

    texts = []
    labels = []
    
    for line in string_data:
        label, text = line.split("\t")
        texts.append(text)
        labels.append(label)

    # Compute lexical artifacts for the dataset with focus on label "abusive"
    artifacts_df = lexical_artifacts.compute(
        texts=texts, labels=labels, label_of_interest=label_of_interest)

    return artifacts_df


def visualize(artifacts_df):
    # Visualize table (top 10)
    visualizer.raw_table(artifacts_df[:10])

    # Visualize bar chart
    visualizer.bar_chart(artifacts_df)


def main():
    """Create interface and do main operations"""

    # Set page title
    st.title('Variation explorer')

    # Create file uploader on the sidebar
    uploaded_file = st.sidebar.file_uploader("Upload dataset")

    # Read the input file
    # @TODO: the function implicitly assumes the file has an header, the text is on a specific
    # column, and so on. But all this may not be true. We need to limit as much as possible the 
    # forms and thus unneeded or too technical inputs from users to avoid a messy interface and
    # a bad user experience: a good way is to have defaults and clearly state them (again, 
    # without being wordy in the interface). The unexperienced users should have to do as less
    # as possible to have a result (max 3-4 interactions), and the experienced user should have 
    # the possibility to do much more but in an intuitive way (hidden from the default interface).
    # @TODO: as for now, "dataframe" is a list tuple ([texts], [labels])
    # @TODO: this should be executed only once: when streamlit reload the interface the dataset
    # is readed again and again (not sure, recheck)
    dataframe = preprocess.read_dataset(
        input_file=uploaded_file, has_header=True)

    # Tokenize the text
    # @TODO: this should be executed only once: when streamlit reload the interface the dataset
    # is tokenized again and again (not sure, recheck)
    dataframe = preprocess.tokenize(dataframe)

    # Create the selector for variables of interest on the sidebar
    options = st.sidebar.multiselect(
        'What are your favorite colors',
        dataframe[1])
        #default=[])

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
            visualize(artifacts_df)


if __name__ == "__main__":
    main()

