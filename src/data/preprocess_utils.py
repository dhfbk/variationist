import pandas as pd
import re
import os
from src import utils
from src.data import tokenization_utils


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
    

def convert_to_ngrams(token_list, n_tokens):
    # Takes as input a list of tokens and  the length of the ngrams
    # Returns token_list merged into ngrams
    new_array = []
    for i in range(len(token_list) - n_tokens + 1):
        new_array.append(" ".join(token_list[i: i + n_tokens]))
    return(new_array)

def create_tokenized_ngrams_column(tokenized_text_column, n_tokens):
    # Takes as input an already tokenized array/series of texts and the length of the ngrams
    # Returns tokenized_text_column with the tokens merged into ngrams

    tokenized_text_column = tokenized_text_column.squeeze().apply(lambda x: convert_to_ngrams(x,n_tokens))
    return(tokenized_text_column)


# # this could ideally be called after create_tokenized_ngrams_column if we want
# # to analyze cooccurrences of bi/trigrams
# def create_tokenized_cooccurrences_column(tokenized_text_column, context_window):
#     """TODO"""
#     return
                                                            

def get_label_values(input_dataframe, col_names_dict):
    """returns a dictionary with all unique label values for the specified labels"""
    current_labels = col_names_dict[utils.LABEL_COLS_KEY]
    
    # Create dictionary with names of label columns and label values
    label_values_dict = {}
    for label in current_labels:
        label_values_dict[label] = pd.unique(input_dataframe[label].values.tolist()).tolist()
    return label_values_dict


def get_subset_dict(input_dataframe, col_names_dict, tok_columns_dict, label_values_dict):
    """create a dictionary containing all the subsets of the datasets we will be analyzing."""
    # TODO handle nan values for a specific label.

    current_labels = col_names_dict[utils.LABEL_COLS_KEY]
    subsets_of_interest = {}
    # loop through all columns containing text
    for text_column in tok_columns_dict:
        tokenized_text_column = tok_columns_dict[text_column]
        # Loop through all columns containing labels
        for label in current_labels:
            current_label_subset = []
            for label_value in label_values_dict[label]:

                df_slice_with_current_label = input_dataframe[(input_dataframe[label] == label_value)]

                series_with_current_label = df_slice_with_current_label[tokenized_text_column]
                if len(series_with_current_label) > 1:
                    series_with_current_label = series_with_current_label.squeeze()

                series_with_current_label = series_with_current_label.rename(label_value)
                current_label_subset.append(series_with_current_label)
            subsets_of_interest[label] = current_label_subset
    
    return subsets_of_interest