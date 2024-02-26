import pandas as pd
import re
import os
from src import utils
from src.data import tokenization


def tokenize_column(text_column, n_tokens, lowercase, stopwords, tokenization_type):
    # print(stopwords)
    """"""
    # TODO take an array/series of texts and tokenize it, return same array/series but tokenized
    # TODO do not check here for n_tokens, just tokenize first and THEN add a component that
    # will aggregate the tokens to create bi, tri-grams and so on.
    # TODO we want to add co-occurrences. Should we do that with context windows? e.g. 2 tokens
    # before, 2 tokens after. Could also do co-occurrences of n-grams?
    if tokenization_type == "whitespace":
        # if n_tokens == 1:
            
            tokenized_text_column = tokenization.whitespace_tokenization(text_column, lowercase)
        # else:
        #     raise Exception("Only n_tokens=1 is currently supported")
        
        # if stopwords != None:
        #     raise Exception("Stopword removal is not currently supported")
    # elif we tokenize with huggingface
    # elif we tokenize with spacy
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
    
    with open(os.path.join('src','data','stopwords', str(language)+'.txt')) as file: 
        stopwords = [line.rstrip() for line in file]
        text_column = text_column.squeeze().apply(lambda x: remove_elements(x,stopwords))
        
        return(text_column)
    

def create_tokenized_ngrams_column(tokenized_text_column, n_tokens):
    """TODO"""
    return


# # this could ideally be called after create_tokenized_ngrams_column if we want
# # to analyze cooccurrences of bi/trigrams
# def create_tokenized_cooccurrences_column(tokenized_text_column, context_window):
#     """TODO"""
#     return
                                                            

def tokenize_add_tok_column(input_dataframe, col_names_dict, n_tokens, stopwords, lowercase, tokenization_type):
    
    # Tokenize and create new columns with tokenized text, name them "tok_{original_column}"
    # returns also a dictionary mapping text columns to their tokenized counterparts
    tokenized_col_names = {}
    for text_column in col_names_dict[utils.TEXT_COLS_KEY]:
        tokenized_col_names[text_column] = f"tok_{text_column}"
        input_dataframe[tokenized_col_names[text_column]] = tokenize_column(
            input_dataframe[[str(text_column)]], n_tokens, lowercase, stopwords, tokenization_type)
    return input_dataframe, tokenized_col_names


def get_label_values(input_dataframe, col_names_dict):
    """returns a dictionary with all unique label values for the specified labels"""
    current_labels = col_names_dict[utils.LABEL_COLS_KEY]
    
    # Create dictionary with names of label columns and label values
    label_values_dict = {}
    for label in current_labels:
        label_values_dict[label] = pd.unique(input_dataframe[label].values.tolist()).tolist()
    return label_values_dict