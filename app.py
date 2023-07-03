import streamlit as st

from src.visualization import visualizer


# Tokenize the text
# @TODO: this should be executed only once: when streamlit reload the interface the dataset
# is tokenized again and again (not sure, recheck)

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