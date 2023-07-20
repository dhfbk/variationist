import pandas as pd
import re
import os
from src import utils

def whitespace_tokenization(text_column, lowercase):
    # Takes as input an array/series of texts and tokenize it, return same array/series but tokenized splitting on whitespaces
    # Remove punctuation and any not alphanumeric charachter
    # ONLY WORKS ON LATIN ALPHABET
    print(text_column)
    if lowercase:
        tok_column = text_column.squeeze().apply(lambda x: str(x).lower())
    else:
        tok_column = text_column.squeeze().astype(str)
        
    print(tok_column)

    tok_column = tok_column.apply(lambda x: re.sub(r'[^a-zA-Z0-9àèìòùÀÈÌÒÙáéíóúýÁÉÍÓÚÝâêîôûÂÊÎÔÛãñõÃÑÕäëïöüÿÄËÏÖÜŸçÇßØøÅåÆæœ]', ' ', x))
    tok_column = tok_column.apply(lambda x: re.sub(r' +', ' ', x))
    tok_column = tok_column.apply(lambda x: x.split(" "))
    # tok_column = tok_column.squeeze().apply(lambda x: pd.Series(x.split(" ")))
    return tok_column

def tokenize_column(text_column, n_tokens, lowercase, stopwords, tokenization_type="whitespace"):
    # print(stopwords)
    """"""
    #TODO take an array/series of texts and tokenize it, return same array/series but tokenized
    if tokenization_type == "whitespace":
        if n_tokens == 1:
            
            tokenized_text_column = whitespace_tokenization(text_column, lowercase)
        else:
            raise Exception("Only n_tokens=1 is currently supported")
        
        # if stopwords != None:
        #     raise Exception("Stopword removal is not currently supported")
    else:
        raise Exception("Only whitespace tokenization is currently supported")
    
    if stopwords != None:        
        tokenized_text_column = remove_stopwords(tokenized_text_column,stopwords)
    # print(tokenized_text_column)    
    return tokenized_text_column


def remove_elements(token_list, stopwords):
 
    # Take as input two lists first the list of tokens of the sentences and as second the list of stopwords
    # Removes elements in  'stopwords' from 'token_list'.
    # Returns token_list without stopwords
    
    new_array = []
    for element in token_list:
        if element not in stopwords:
            new_array.append(element)
    
    return new_array


def remove_stopwords(text_column, language):
    # Takes as input an already tokenized array/series of texts and a language and return it without stopwords
    # Language need to be ISO 639-1  two-letter codes e.g en, it, fr, de 
    # TODO to be done
    
    with open(os.path.join('src','data_handler','stopwords', str(language)+'.txt')) as file: 
        stopwords = [line.rstrip() for line in file]
        text_column = text_column.squeeze().apply(lambda x: remove_elements(x,stopwords))
        
        return(text_column)
                                                            

def tokenize_add_tok_column(input_dataframe, col_names_dict, n_tokens, stopwords, lowercase):
    
    # Tokenize and create new columns with tokenized text, name them "tok_{original_column}"
    # returns also a dictionary mapping text columns to their tokenized counterparts
    tokenized_col_names = {}
    for text_column in col_names_dict[utils.TEXT_COLS_KEY]:
        tokenized_col_names[text_column] = f"tok_{text_column}"
        input_dataframe[tokenized_col_names[text_column]] = tokenize_column(
            input_dataframe[[str(text_column)]], n_tokens, lowercase, stopwords)
    return input_dataframe, tokenized_col_names


def get_label_values(input_dataframe, col_names_dict):
    """returns a dictionary with all unique label values for the specified labels"""
    current_labels = col_names_dict[utils.LABEL_COLS_KEY]
    
    # Create dictionary with names of label columns and label values
    label_values_dict = {}
    for label in current_labels:
        label_values_dict[label] = pd.unique(input_dataframe[label].values.tolist()).tolist()
    return label_values_dict