import streamlit as st
import pandas as pd
import numpy as np
from io import StringIO

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


def create_interface():
    """"""

    # Set page title
    st.title('Variation explorer')

    # Create file uploader on the sidebar
    uploaded_file = st.sidebar.file_uploader("Upload dataset")

    # Create text input on the sidebar
    label_of_interest = st.sidebar.text_input("Label of interest")

    # Create compute button on the sidebar
    st.sidebar.button(
        "Compute artifacts", 
        on_click=compute(uploaded_file, label_of_interest)
    )


def compute(uploaded_file, label_of_interest):
    """"""

    if uploaded_file and label_of_interest:
        if uploaded_file is not None:
            # Convert input file to a string based IO
            stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))

            artifacts_df = calc_artifacts(stringio, label_of_interest)
            visualize(artifacts_df)


if __name__ == "__main__":
    create_interface()

