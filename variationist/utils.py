"""A python file containing project-wide constants and functions."""

import csv
import emoji
import json
import os
import pandas as pd
from typing import Union


# CONSTANTS
TEXT_COLS_KEY = "text"
LABEL_COLS_KEY = "labels"
MULTI_VAR_SEP = "::"


def load_json_data_from_filepath_or_dict(
    input_json: Union[str, dict],
) -> dict:
    """
    A function that loads the json/dict object from either a user-defined json 
    filepath or a dict variable (in the latter case, it returns the dict itself).

    Parameters
    ----------
    input_json: Union[str, dict]
        A path to the json file or a json/dict object storing metadata and results 
        from a prior analysis using Variationist.

    Returns
    -------
    json_data: dict
        A json/dict object storing metadata and results of a prior analysis.
    """

    # If the input is a json filepath, read it and store it
    if type(input_json) == str:
        print(f"Loading json data from the filepath \"{input_json}\"...")
        json_data = json.load(open(input_json))
    # If the input is already a json/dict object, use it
    elif type(input_json) == dict:
        print(f"Reading json data...")
        json_data = input_json
    # Otherwise, raise an error
    else:
        raise TypeError(f"ERROR: The input should be a json object or a json filepath.")
    
    return json_data


def convert_file_to_dataframe(data_filepath, cols_type):
    """A function that, given an input filepath and information about the columns type (i.e., names or
    indexes), checks the format the file (csv, tsv, or other), reads it, and stores it in a pandas 
    dataframe. Files ending in ".tsv" and ".csv" are considered TSV and CSV files, respectively. By 
    default, a file with no (or other) extension is considered a TSV file. Input files with no header 
    are assigned index numbers as header, whereas column names are preserved in the ones with a header.
    Moreover, if the input is a string of the format "hf::DATASET_NAME::SPLIT", this is considered as a
    HuggingFace dataset, and thus the function takes care of downloading and storing the relevant SPLIT 
    portion of DATASET_NAME as a pandas dataframe. 

    Parameters
    ----------
    data_filepath: str
        A string denoting the path to an input file/dataset
    cols_type: str
        A string denoting if the column strings are to be considered as names or indexes

    Returns
    -------
    dataframe: pandas.core.frame.DataFrame
        A Pandas dataframe with a header (either expressed with names or indexes)
    """
    if data_filepath.lower().startswith('hf::'):
        from datasets import load_dataset
        string_parts = data_filepath.split("::")
        if len(string_parts) == 3:
            prefix, dataset_name, split = string_parts
            print(f"INFO: 'Loading {data_filepath}' as a HuggingFace dataset. We assume the last element in the specified string is the split (\"{split}\").")
            dataframe = pd.DataFrame(load_dataset(dataset_name)[split])
        elif len(string_parts) == 4:
            prefix, dataset_name, subset, split = string_parts
            print(f"INFO: 'Loading {data_filepath}' as a HuggingFace dataset. We assume the third element in the specified string is the subset (\"{subset}\") and the last is the split (\"{split}\").")
            dataframe = pd.DataFrame(load_dataset(dataset_name, subset)[split])

        else:
            raise Exception(f"ERROR: {data_filepath} seems to refer to a HuggingFace dataset, however " 
                "there is no specification about the split to use, or they are not specified as expected. Please ensure that \"data_filepath\" "
                "follows the format hf::DATASET_NAME::SPLIT or hf::DATASET_NAME::SUBSET::SPLIT.")
    
    elif (type(data_filepath) == str) and (not os.path.isfile(data_filepath)):
        raise ValueError(f"ERROR: the '{data_filepath}' filepath does not exist.")

    elif data_filepath.lower().endswith('.tsv'):
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


# Partly taken from https://github.com/explosion/spaCy/blob/master/spacy/lang/char_classes.py
merge_chars = lambda char: list(char.strip().split(" "))


SYMBOLS = (
    # Punctuation chars
    ". … , : ; ! ? ¿ ؟ ¡ ( ) [ ] { } < > _ # * @ ° § % "
    "+ ^ = | \\ / & 。 ？ ！ ， 、 ； ： ～ · । ، ۔ ؛ ٪ "
    # Other symbols
    "© ¶ × • ‿ ᴗ ◉ ʘ ◕ ｡ ・ ∀ ™ "
    # Quote chars
    "' \" ” “ ` ‘ ´ ’ ‚ , „ » « 「 」 『 』 （ ） 〔 〕 "
    "【 】 《 》 〈 〉 〈 〉  ⟦ ⟧ "
    # Hyphen chars
    "- – — ~ "
    # Currency chars
    "$ £ € ¥ ฿ ₽ ﷼ ₴ ₠ ₡ ₢ ₣ ₤ ₥ ₦ ₧ ₨ ₩ ₪ ₫ € ₭ ₮ ₯ ₰ "
    "₱ ₲ ₳ ₴ ₵ ₶ ₷ ₸ ₹ ₺ ₻ ₼ ₽ ₾ ₿ ¢ "
    # Empty chars (plus tag latin small letters)
    "￼ ​ ‍ 󠁧 󠁢 󠁣 󠁤 󠁥 󠁦 󠁧 󠁨 󠁩 󠁪 󠁫 󠁬 󠁭 󠁮 󠁯 󠁰 󠁱 󠁲 󠁳 󠁴 󠁵 󠁶 󠁷 󠁸 󠁹 󠁺 󠁿 "
    # Remove variant selector (@TODO handle this for emojis in the future)
    "\ufe0f "
)


def replace_symbols(text):
    symbols_list = merge_chars(SYMBOLS)
    
    for char in SYMBOLS:
        if char in text:
            text = text.replace(char, " ")

    temp_text = ""
    for char in text:
        if emoji.is_emoji(char):
            temp_text += " " + char + " "
        else:
            temp_text += char

    return temp_text

