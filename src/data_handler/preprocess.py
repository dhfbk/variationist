import pandas as pd

def whitespace_tokenization(text_column):
    tok_column = text_column.squeeze().apply(lambda x: x.split(" "))
    return tok_column

def tokenize_column(text_column, tokenization_type="whitespace"):
    """"""
    #TODO take an array/series of texts and tokenize it, return same array/series but tokenized
    if tokenization_type == "whitespace":
        tokenized_text_column = whitespace_tokenization(text_column)
    else:
        raise Exception("Only whitespace tokenization is currently supported")
    return tokenized_text_column


def tokenize_add_tok_column(input_dataframe, col_names_dict):
    # Tokenize and create new columns with tokenized text, name them "tok_{original_column}"
    # returns also a dictionary mapping text columns to their tokenized counterparts
    tokenized_col_names = {}
    for text_column in col_names_dict["text"]:
        tokenized_col_names[text_column] = f"tok_{text_column}"
        input_dataframe[tokenized_col_names[text_column]] = tokenize_column(input_dataframe[[str(text_column)]])
    return input_dataframe, tokenized_col_names


def get_label_values(input_dataframe, col_names_dict):
    """returns a dictionary with all unique label values for the specified labels"""
    current_labels = col_names_dict["labels"]
    
    # Create dictionary with names of label columns and label values
    label_values_dict = {}
    for label in current_labels:
        label_values_dict[label] = pd.unique(input_dataframe[label].values.tolist()).tolist()
    return label_values_dict