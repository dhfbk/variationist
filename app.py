import csv
import os
import pandas as pd
import shutil
import streamlit as st
import subprocess
import sys
import time

from datetime import datetime
from io import StringIO
from PIL import Image

from src.visualization import visualizer


# @TODO: Directly get those from a constants file in the repo
LABEL_TYPES = ["---", "time", "space"]
METRICS = ["most-frequent", "pmi"]
STOPWORDS = ["---", "en", "it"]
N_TOKENS = ["1", "2", "3"]
TEMP_DATA_FOLDER_NAME = "data-temp"


def run_variationist(args, content_sections):
    """A function that calls the main.py variationist script with the defined commands.

    Parameters
    ----------
    args: Dict[str->type]
        The set of command line arguments as key-value pairs
    content_sections: 
        A list of handles for the content section objects
    """

    # @TODO: Temporary handling of interface-only markers
    label_cols = ""
    label_type_cols = ""
    # if args["label_cols"] == "---": label_cols = ""
    if args["label_type_cols"] == "---": label_type_cols = ""
    
    try:
        result = subprocess.run([
            f"{sys.executable}", "main.py",
            "--dataset_filepath", args["dataset_filepath"], # @TODO: Manage path
            "--text_cols", " ".join([col for col in args["text_cols"]]),
            "--label_cols", args["label_cols"], # @TODO: Generalize to multiple labels
            # @TODO: --label_type_cols
            "--metrics", " ".join([metric for metric in args["metrics"]])
            # @TODO: --lowercase, --stopwords, --n_tokens
        ], capture_output=True, text=True)
    except Exception as err: # @TODO: Not a real handle
        st.error(err, icon="⚠️")

    # Quite a hack just for temp visualization
    print(result)
    content_sections[1].write(result.stdout)
    # @TODO: Make them not to disappear when changing settings


def initialize_session_states():
    """A function that initializes the session states."""

    if "args_options" not in st.session_state:
        st.session_state["args_options"] = dict()
        st.session_state["args_options"]["dataset_filepath"] = ""
        st.session_state["args_options"]["text_cols"] = []
        st.session_state["args_options"]["label_cols"] = []
        st.session_state["args_options"]["label_type_cols"] = [] # @TODO: Not implemented yet
        st.session_state["args_options"]["metrics"] = ["pmi"]
        st.session_state["args_options"]["lowercase"] = True
        st.session_state["args_options"]["stopwords"] = False
        st.session_state["args_options"]["n_tokens"] = 1
    if "dataframe" not in st.session_state:
        st.session_state["dataframe"] = pd.DataFrame()
    if "dataset_name" not in st.session_state:
        st.session_state["dataset_name"] = ""


def set_session_state(element_states_dict, is_args=False):
    """A function that sets the session state of a dictionary of named elements.

    Parameters
    ----------
    element_states_dict: Dict[str->type]
        A dictionary enclosing element-state key-value pairs
    """

    if not is_args:
        for element, state in element_states_dict.items():
            st.session_state[element] = state
    else:
        for element, state in element_states_dict.items():
            st.session_state["args_options"][element] = state


def customize_css():
    """A function that updates the CSS of the page."""

    # /* 4rem instead of 6rem */, /* 2rem instead of 6rem */
    top_padding = """
        <style>
            .css-1544g2n { padding: 4rem 1rem 1.5rem; }
            .css-z5fcl4 { padding: 2rem 6rem 1rem 6rem; }
        </style>
    """
    st.markdown(top_padding, unsafe_allow_html=True)

    file_uploader = """
        <style>
            .css-1txgwv8 .eqdbnj015 { flex-direction: row; align-items: center; }
            .css-1txgwv8 .eqdbnj014 { margin-bottom: 0rem; }
            .css-1aehpvj { font-size: 12px; }
        </style>
    """
    st.markdown(file_uploader, unsafe_allow_html=True)


def initialize_content_sections():
    """A function that creates content sections and returns a their handles as list.

    Returns
    -------
    content_sections: 
        A list of handles for the content section objects
    """

    content_sections = [
        st.expander(label=":mag: **DATASET PREVIEW**", expanded=True),
        st.expander(label=":bar_chart: **RESULTS**", expanded=True)]

    return content_sections


def make_disappear(component, seconds=3):
    """A function that makes a component disappear after a certain number of seconds.

    Parameters
    ----------
    component: 
        The return value of a component (e.g., of a st.warning component)
    seconds: int
        The number of seconds to make the interface sleep before the component disappears
    """

    time.sleep(seconds)
    component.empty()


def show_arguments_for_debugging():
    """A helper function that shows the dictionary or command line arguments in the interface."""

    st.write("**args_options** session state", st.session_state["args_options"])


def serialize_dataframe(dataframe, orig_filename):
    """A function that writes a dataframe into a file and return its path.

    Parameters
    ----------
    dataframe: pandas.core.frame.DataFrame
        A Pandas dataframe for the input_file with a header
    orig_filename: str
        The original filename from which the data has been read and the dataframe created

    Returns
    -------
    current_filepath: str
        The filepath to the file containing data
    """

    # Create the folder containing temp data if does not exist yet
    if not os.path.exists(TEMP_DATA_FOLDER_NAME):
        os.makedirs(TEMP_DATA_FOLDER_NAME)

    # Get current datetime
    current_datetime = datetime.now().strftime("%Y%m%d-%H%M%S")

    # Clean directory from previous executions
    current_datetime = current_datetime.replace("-", "")
    current_datatime_as_int = int(current_datetime)
    for f in os.listdir(TEMP_DATA_FOLDER_NAME):
        if os.path.isdir(os.path.join(TEMP_DATA_FOLDER_NAME, f)):
            old_datetime_as_int = int(f.replace("-", ""))
            if old_datetime_as_int < current_datatime_as_int:
                shutil.rmtree(os.path.join(TEMP_DATA_FOLDER_NAME, f))

    # Write dataframe as a TSV or CSV file in a directory named datetime, keeping its original name
    if not os.path.exists(os.path.join(TEMP_DATA_FOLDER_NAME, current_datetime)):
        os.makedirs(os.path.join(TEMP_DATA_FOLDER_NAME, current_datetime))
    current_filepath = os.path.join(TEMP_DATA_FOLDER_NAME, current_datetime, orig_filename)

    if orig_filename.lower().endswith('.csv'):
        dataframe.to_csv(current_filepath, sep=",", index=False)
    else:
        dataframe.to_csv(current_filepath, sep="\t", quoting=csv.QUOTE_NONE, index=False)

    return current_filepath


def check_and_load_dataset(local_dataset, hf_name, hf_split, mode):
    """A function that checks the existence of a dataset and loads it, either from a local file or from
    the HuggingFace datasets hub. It also handles a variety of error, warning, and success messages that
    are related to it.

    Parameters
    ----------
    local_dataset: UploadedFile
        An UploadedFile object denoting the local dataset. It can be None if data has not been uploaded
    hf_name: str
        A string that identifies a dataset from the HuggingFace datasets hub. It can be an empty string
        ("") if it has not been defined
    hf_split: str
        A string that identifies a split for the "hf_name" dataset from the HuggingFace datasets hub. It
        can be an empty string ("") if it has not been defined
    mode: str
        A string denoting from which button the function has been triggered. It can be "local", if the
        button is the one from the "Local file" tab, or "hf" if it is from the "HuggingFace datasets" tab

    Returns
    -------
    local_dataset: UploadedFile
        An UploadedFile object denoting the local dataset. It can be None if data has not been uploaded
    hf_name: str
        A string that identifies a dataset from the HuggingFace datasets hub. It can be an empty string
        ("") if it has not been defined
    hf_split: str
        A string that identifies a split for the "hf_name" dataset from the HuggingFace datasets hub. It
        can be an empty string ("") if it has not been defined
    """

    def load_local_dataset(input_file):
        """A function that loads a local dataset file into a dataframe.

        Parameters
        ----------
        input_file: UploadedFile
            An UploadedFile object denoting the local dataset. It can be None if data has not been 
            uploaded

        Returns
        -------
        dataframe: pandas.core.frame.DataFrame
            A Pandas dataframe for the input_file with a header
        """

        stringio = StringIO(input_file.getvalue().decode("utf-8"))

        # Handle both CSV and TSV file formats, assuming a header is present in the data file
        if input_file.name.lower().endswith('.csv'):
            dataframe = pd.read_csv(stringio, sep=",", header=0)
        else:
            dataframe = pd.read_csv(stringio, sep="\t", quoting=csv.QUOTE_NONE, header=0)

        return dataframe


    def load_hf_dataset(hf_name, hf_split):
        """A function that loads a dataset from the HuggingFace datasets hub into a dataframe.
        Parameters
        ----------
        hf_name: str
            A string that identifies a dataset from the HuggingFace datasets hub. It can be an 
            empty string ("") if it has not been defined
        hf_split: str
            A string that identifies a split for the "hf_name" dataset from the HuggingFace 
            datasets hub. It can be an empty string ("") if it has not been defined
        
        Returns
        -------
        dataframe: pandas.core.frame.DataFrame
            A Pandas dataframe for the hf_name and hf_split dataset with a header
        """

        from datasets import load_dataset # here, so it is loaded only if needed
        dataframe = pd.DataFrame(load_dataset(hf_name)[hf_split])

        return dataframe


    # Initialize the dataframe and variables to know if data has been loaded from 0+ modes
    dataframe = pd.DataFrame()
    is_local_defined = True if (local_dataset != None) else False
    is_hf_defined = True if (hf_name != "" or hf_split != "") else False

    # Case "Confirm" has been triggered from the "Local file" tab
    if mode == "local":
        if is_local_defined:
            if is_hf_defined:
                alert_w = st.warning(f"Both the local dataset \"**{local_dataset.name}**\" and the "
                    f"HuggingFace dataset \"**{hf_name}**\" (\"**{hf_split}**\" split) have been "
                    f"defined. We replace the HuggingFace's one with this local one.", icon="❗")

            try:
                with st.spinner(f"Loading \"**{local_dataset.name}**\"..."):
                    dataframe = load_local_dataset(local_dataset)
                    temp_filepath = serialize_dataframe(dataframe, local_dataset.name)
                    set_session_state({"dataframe": dataframe})
                    set_session_state({"dataset_name": local_dataset.name})
                    set_session_state({"dataset_filepath": temp_filepath}, is_args=True)
                alert_s = st.success(f"The local dataset from the file \"**{local_dataset.name}**\" "
                    f"has been successfully loaded!", icon="🎉")
                hf_name = ""
                hf_split = ""
            except Exception as err:
                st.error(f"An error occurred when reading the dataset named "
                f"\"**{local_dataset.name}**\". Please ensure it is in a TSV/CSV format and follows ", 
                f"the format requirements.", icon="⚠️")
                if not is_hf_defined:
                    set_session_state({"dataframe": pd.DataFrame()})
                    set_session_state({"dataset_name": ""})
                    set_session_state({"dataset_filepath": ""}, is_args=True)
        
        else:
            st.error(f"**No local dataset has been defined**.", icon="⚠️")
            if not is_hf_defined:
                set_session_state({"dataframe": pd.DataFrame()})
                set_session_state({"dataset_name": ""})
                set_session_state({"dataset_filepath": ""}, is_args=True)

    # Case "Confirm" has been triggered from the "HuggingFace datasets" tab
    elif mode == "hf":
        if is_hf_defined:
            
            if (hf_split == ""):
                st.error(f"A dataset named \"**{hf_name}**\" from the HuggingFace datasets hub has "
                    f"been defined, but **no data split has been specified**.", icon="⚠️")
                if not is_local_defined:
                    set_session_state({"dataframe": pd.DataFrame()})
                    set_session_state({"dataset_name": ""})
                    set_session_state({"dataset_filepath": ""}, is_args=True)
            
            elif (hf_name == ""):
                st.error(f"A split name \"**{hf_split}**\" has been defined but **no information "
                    f"about to which dataset from the HuggingFace datasets hub it belongs has ", 
                    f"been specified**.", icon="⚠️")
                if not is_local_defined:
                    set_session_state({"dataframe": pd.DataFrame()})
                    set_session_state({"dataset_name": ""})
                    set_session_state({"dataset_filepath": ""}, is_args=True)
            
            else:
                try:
                    with st.spinner(f"Loading \"**{hf_name}**\" (\"**{hf_split}**\" split) from the "
                        "HuggingFace datasets hub..."):
                        dataframe = load_hf_dataset(hf_name, hf_split)
                        set_session_state({"dataframe": dataframe})
                        set_session_state({"dataset_name": hf_name + " (" + hf_split + ")"})
                        set_session_state({
                            "dataset_filepath": "hf::" + hf_name + "::" + hf_split}, is_args=True)
                    
                    if is_local_defined:
                        alert_w = st.warning(f"Both the local dataset \"**{local_dataset.name}**\" "
                            f"and the HuggingFace dataset \"**{hf_name}**\" (\"**{hf_split}**\" "
                            f"split) have been defined. We replace the local one with this "
                            f"HuggingFace's one.", icon="❗")
                    
                    alert_s = st.success(f"The dataset named \"**{hf_name}**\" (\"**{hf_split}**\" "
                        f"split) from the HuggingFace datasets hub has been successfully loaded!", 
                        icon="🎉")
                    local_dataset = None
                except Exception as err:
                    st.error(f"The dataset named \"**{hf_name}**\" (or its \"**{hf_split}**\" split) "
                        f"seems not to exist on the HuggingFace datasets hub.", icon="⚠️")
                    if not is_local_defined:
                        set_session_state({"dataframe": pd.DataFrame()})
                        set_session_state({"dataset_name": ""})
                        set_session_state({"dataset_filepath": ""}, is_args=True)
        
        else:
            st.error(f"**No dataset from the HuggingFace datasets hub has been defined**.", icon="⚠️")
            if not is_local_defined:
                set_session_state({"dataframe": pd.DataFrame()})
                set_session_state({"dataset_name": ""})
                set_session_state({"dataset_filepath": ""}, is_args=True)

    # Case Unknown
    else:
        st.error(f"The mode \"**{mode}**\" is not defined.", icon="⚠️")

    return local_dataset, hf_name, hf_split


def placeholder_function():
    """A dummy function to bypass the unwanted calls that originate from a streamlit bug."""
    pass


def set_container_data_loading():
    """A function that creates and handles the container with data loading options."""

    def section_data_upload():
        """A function that creates and handles the widgets for the data upload section.

        Returns
        -------
        local_dataset: UploadedFile
            An UploadedFile object denoting the local dataset. It can be None if data has not been 
            uploaded
        load_button_local: 
            The value of the load button
        """

        local_dataset = st.file_uploader(
            label="TSV/CSV data **file**",
            help="Upload a **TSV or CSV file** containing the data. **Instances must be one per "
                "line, with text(s) or their label(s) as columns**. The first line is considered "
                "as the header. For files >200MB or with no header, we suggest using our python "
                "package instead (https://github.com/dhfbk/variationist).",
            type=["tsv", "csv"])
        load_button_local = st.button(label="Confirm", key="load_local", on_click=placeholder_function)

        return local_dataset, load_button_local


    def section_huggingface_datasets():
        """A function that creates and handles the widgets for the HuggingFace datasets section.

        Returns
        -------
        hf_name: str
            A string that identifies a dataset from the HuggingFace datasets hub. It can be an empty 
            string ("") if it has not been defined
        hf_split: str
            A string that identifies a split for the "hf_name" dataset from the HuggingFace datasets 
            hub. It can be an empty string ("") if it has not been defined
        load_button_hf: 
            The value of the load button
        """

        hf_name = st.text_input(
            label="**Dataset** name",
            placeholder="Insert here",
            help="Insert the dataset name as indicated in the HuggingFace datasets hub "
                "(https://huggingface.co/datasets).")
        hf_split = st.text_input(
            label="**Split** name",
            placeholder="Insert here",
            help="Insert the split name for the dataset specified above, as indicated in the HuggingFace "
                "datasets hub (https://huggingface.co/datasets).")
        load_button_hf = st.button(label="Confirm", key="load_hf", on_click=placeholder_function)

        return hf_name, hf_split, load_button_hf


    # Create the container
    container_data_loading = st.sidebar.expander(label=":package: **LOAD DATASET**", expanded=True)

    # Add tabs and relevant widgets for both local and HuggingFace datasets to the container
    with container_data_loading:
        dataset_upload_tab, dataset_hf_tab = st.tabs(
            [":floppy_disk: Local file", ":hugging_face: HuggingFace datasets"])
        with dataset_upload_tab: 
            local_dataset, load_button_local = section_data_upload()
        with dataset_hf_tab: 
            hf_name, hf_split, load_button_hf = section_huggingface_datasets()
    
    # Check and load the dataset if a button is clicked (also showing a preview)
    if load_button_local:
        local_dataset, hf_name, hf_split = check_and_load_dataset(
            local_dataset, hf_name, hf_split, "local")
    if load_button_hf:
        local_dataset, hf_name, hf_split = check_and_load_dataset(
            local_dataset, hf_name, hf_split, "hf")


def set_container_column_selectors():
    """A function that creates and handles the container with column selectors options."""

    dataframe = st.session_state["dataframe"]

    # Create the container
    container_column_selectors = st.sidebar.expander(
        label=":pushpin: **SELECT COLUMNS AND METRICS**", 
        expanded=True if (not dataframe.empty) else False)

    with container_column_selectors:
        # Show a warning message if the dataframe is empty
        if dataframe.empty:
            st.warning("Please load a dataset from above.", icon="⚠️")

        # Otherwise, show all the relevant widgets
        else:
            column_names = list(dataframe.columns.values)

            text_cols = st.multiselect(
                label=":pencil: **Text** column(s)",
                help="Select relevant column name(s) indicating text data to be analyzed.",
                options=column_names,
                default=[])
            st.session_state["args_options"]["text_cols"] = text_cols

            # Create a side-by-side container for selection of label names and types
            with st.container():
                side_col_left, side_col_right = st.columns(2)

                with side_col_left:
                    label_name_cols = st.selectbox(
                        label=":label: **Label** column",
                        help="Select a column name indicating the label to be analyzed. On the right, "
                            "you will also have to choose how this column has to be treated. If you "
                            "choose \"---\", basic statistics only will be computed.",
                        options=["---"]+column_names)
                    # @TODO: To generalize as list
                    st.session_state["args_options"]["label_cols"] = label_name_cols

                with side_col_right:
                    label_type_cols = st.selectbox(
                        label=":question: **Label** type",
                        help="Select how the column name defined on the left has to be treated. If you "
                            "choose \"---\" it will be a) treated as generic in the presence of a label "
                            "column, or b) basic statistics only will be computed if also the column name "
                            "is not defined.",
                        options=LABEL_TYPES)
                    # @TODO: To generalize as list
                    st.session_state["args_options"]["label_type_cols"] = label_type_cols

                add_label_button = st.button(label="Add another label", on_click=placeholder_function)

                metrics = st.multiselect(
                    label=":triangular_ruler: **Metrics** to compute",
                    help="List of metrics to compute.",
                    options=METRICS,
                    default=[METRICS[1]])
                st.session_state["args_options"]["metrics"] = metrics


def set_container_custom_selectors():
    """A function that creates and handles the container with custom selectors options."""

    dataframe = st.session_state["dataframe"]

    # Create the container
    container_custom_selectors = st.sidebar.expander(label=":gear: **CUSTOM SETTINGS**", expanded=False)
    
    with container_custom_selectors:
        # Show a warning message if the dataframe is empty
        if dataframe.empty:
            st.warning("Please load a dataset from above.", icon="⚠️")

        # Otherwise, show all the relevant widgets
        else:
            side_exp_col_left, side_exp_col_right = st.columns(2)

            with side_exp_col_left:
                stopwords = st.selectbox(
                    label=":paperclip: Select **stopwords**",
                    help="A list of stopwords, i.e., tokens not to be considered for the purpose of "
                        "the analysis. By default, we assume no stopwords (i.e., None) and thus all "
                        "tokens contribute to the results. Stopword lists can be declared by their "
                        "ISO-639-1 code (e.g., \"en\", \"it\"): a list from NLTK will be automatically "
                        "downloaded and used.",
                    options=STOPWORDS)
                st.session_state["args_options"]["stopwords"] = stopwords

            with side_exp_col_right:
                n_tokens = st.selectbox(
                    label=":snowflake: Num of **tokens**",
                    help="An integer denoting the number of contiguous tokens from instances in the "
                        "\"Text column(s)\" field to be considered in the analysis. Note that values "
                        "higher than 1 will significantly slow down the computation, especially in "
                        "the case of large datasets.",
                    options=N_TOKENS,
                    disabled=True)

            lowercasing = st.checkbox(
                label="Lowercase texts", 
                help="Whether or not to lowercase the texts from \"Text column(s)\" before running "
                    "the analysis.",
                value=True)
            st.session_state["args_options"]["lowercase"] = lowercasing


def main():
    """A function that orchestrates the whole application."""

    # Configure the default settings of the page
    st.set_page_config(
        page_title="Variationist", 
        page_icon="🕵️‍♀️", 
        layout="wide", 
        initial_sidebar_state="expanded", 
        menu_items={
            "Get Help": 'https://github.com/dhfbk/variationist/',
            "Report a bug": "https://github.com/dhfbk/variationist/issues",
            "About": "# 🕵️‍♀️ Variationist"})

    # Adjust the stylesheets
    customize_css()

    # Initialize session states
    initialize_session_states()

    # Set the page title
    st.title("🕵️‍♀️ Variationist")
    st.markdown("---")

    # Initialize the content sections
    content_sections = initialize_content_sections()

    # SIDEBAR #################################################################
    
    # Create all containers of the sidebar with their own relevant widgets
    set_container_data_loading()
    set_container_column_selectors()
    set_container_custom_selectors()

    # Define the run button
    is_run_disabled = True if st.session_state["dataframe"].empty else False
    run_button = st.sidebar.button(
        "**RUN** 🕵️‍♀️", 
        disabled=is_run_disabled, 
        on_click=placeholder_function)

    if run_button:
        with st.spinner(f"🕵️‍♀️ **Running**... (*depending on the size of the dataset, label space, "
            "and the chosen configuration this step may take a while, time for a coffee?* :coffee:)"):
            run_variationist(st.session_state["args_options"], content_sections)

    # MAIN CONTENT ############################################################

    # show_arguments_for_debugging()

    if not st.session_state["dataframe"].empty:
        content_sections[0].markdown(f"**Dataset \"{st.session_state['dataset_name']}\"**")
        content_sections[0].dataframe(data=st.session_state["dataframe"])


if __name__ == "__main__":
    main()
