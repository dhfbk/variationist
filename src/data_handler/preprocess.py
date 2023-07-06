import pandas as pd
import re
from src import utils

def whitespace_tokenization(text_column, lowercase):
    # Takes as input an array/series of texts and tokenize it, return same array/series but tokenized splitting on whitespaces
    # Remove punctuation and any not alphanumeric charachter
    # ONLY WORKS ON LATIN ALPHABET
    
    if lowercase:
        tok_column = text_column.squeeze().apply(lambda x: x.lower())

    tok_column = tok_column.squeeze().apply(lambda x: re.sub(r'[^a-zA-Z0-9àèìòùÀÈÌÒÙáéíóúýÁÉÍÓÚÝâêîôûÂÊÎÔÛãñõÃÑÕäëïöüÿÄËÏÖÜŸçÇßØøÅåÆæœ]', ' ', x))
    tok_column = tok_column.squeeze().apply(lambda x: re.sub(r' +', ' ', x))
    tok_column = tok_column.squeeze().apply(lambda x: x.split(" "))
    
    return tok_column

def tokenize_column(text_column, n_tokens, stopwords, lowercase, tokenization_type="whitespace"):
    """"""
    #TODO take an array/series of texts and tokenize it, return same array/series but tokenized
    if tokenization_type == "whitespace":
        if n_tokens == 1:
            print("x", lowercase)
            tokenized_text_column = whitespace_tokenization(text_column, lowercase)
        else:
            raise Exception("Only n_tokens=1 is currently supported")
        
        if stopwords != None:
            raise Exception("Stopword removal is not currently supported")
    else:
        raise Exception("Only whitespace tokenization is currently supported")
    # if stopwords:
    
    return tokenized_text_column

def remove_stopwords(text_column, language):
    # Takes as input an already tokenized array/series of texts and a language and return it without stopwords
    # Language need to be ISO 639-1  two-letter codes e.g en, it, fr, de 
    # TODO to be done
    with open(os.path.join('stopwords', language+'txt')) as file: 
        stopwords = [line.rstrip() for line in file]

def tokenize_add_tok_column(input_dataframe, col_names_dict, n_tokens, stopwords, lowercase):
    # Tokenize and create new columns with tokenized text, name them "tok_{original_column}"
    # returns also a dictionary mapping text columns to their tokenized counterparts
    tokenized_col_names = {}
    for text_column in col_names_dict[utils.TEXT_COLS_KEY]:
        tokenized_col_names[text_column] = f"tok_{text_column}"
        input_dataframe[tokenized_col_names[text_column]] = tokenize_column(
            input_dataframe[[str(text_column)]], n_tokens, stopwords, lowercase)
    return input_dataframe, tokenized_col_names


def get_label_values(input_dataframe, col_names_dict):
    """returns a dictionary with all unique label values for the specified labels"""
    current_labels = col_names_dict[utils.LABEL_COLS_KEY]
    
    # Create dictionary with names of label columns and label values
    label_values_dict = {}
    for label in current_labels:
        label_values_dict[label] = pd.unique(input_dataframe[label].values.tolist()).tolist()
    return label_values_dict