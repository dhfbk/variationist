import pandas as pd
import re
import os
from src import utils
from src.data import tokenization_utils
import itertools
import sys
from tqdm import tqdm
import stopwordsiso as stopwords


def remove_elements(token_list, stopwords):
    # Take as input two lists first the list of tokens of the sentences and as second the list of stopwords
    # Removes elements in  'stopwords' from 'token_list'.
    # Returns token_list without stopwords
    new_array = []
    for element in token_list:
        if element.lower() not in stopwords:
            new_array.append(element)
    return new_array


def remove_stopwords(text_column, language):
    # Takes as input an already tokenized array/series of texts and a language and return it without stopwords
    # Language need to be ISO 639-1  two-letter codes e.g en, it, fr, de 
    lang_stopwords = stopwords.stopwords(language)
    text_column = text_column.squeeze().apply(lambda x: remove_elements(x,lang_stopwords))
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
    tqdm.pandas()
    tokenized_text_column = tokenized_text_column.squeeze().progress_apply(lambda x: convert_to_ngrams(x,n_tokens))
    return(tokenized_text_column)
    # TODO this will be developed in a future release
    # def discretize_granularity(dataframe, var_names, var_types, var_semantics, var_granularity):
    #     for i in range(len(var_names)):
    #         if var_granularity != None:
    #             break
    #     # allora mappiamo le robe. controllare doc pandas
    #     return dataframe


def discretize_bins_col(dataframe_var_col, curr_var_type, curr_var_semantic, curr_var_bins):
    discretized_var_col, bin_names = pd.cut(dataframe_var_col,
                                            bins=curr_var_bins,
                                            retbins=True)
    print(f"""INFO: The calculated cutoff values of bins for the {dataframe_var_col.name} variable are:\n{list(bin_names)}\nThese will be reported as (value_x, value_x+1] in the results.""")
    return discretized_var_col


def extract_combinations(token_list, n_items, context_window, unique_cooc):
    # Takes as input a list of tokens, the number of words that cooccur and the context window size 
    # Returns token_list merged into cooccurrences
    if context_window == 0:
        context_window = len(token_list)
    new_array = []
    for i in range(len(token_list) - context_window + 1):
        for cooc in itertools.combinations(token_list[i: i + context_window], n_items):
            if (not unique_cooc) or ((unique_cooc) and (len(set(cooc)) == len(cooc))):
                new_array.append(" ".join(sorted(cooc)))
    new_array = list(set(new_array))
    return(new_array)
    

def create_tokenized_cooccurrences_column(tokenized_text_column, n_items, context_window, unique_cooc):
    # Takes as input an already tokenized array/series of texts, the number of words that cooccur and the context window size 
    # By default cooccurrences are extracted from the entire text
    # Returns tokenized_text_column with the al the cooccurrences of n words occurring in the test
    if n_items > context_window and context_window!=0:
        sys.exit(f"ERROR: The size of the context windows cannot be lower than the number of words when extracting the cooccurrences!\nExit.")
    tqdm.pandas()

    tokenized_text_column = tokenized_text_column.squeeze().progress_apply(lambda x: extract_combinations(x,n_items,context_window,unique_cooc))
    return(tokenized_text_column)
                                                            

def get_label_values(input_dataframe, col_names_dict):
    """Returns a dictionary with all unique label values for the specified variables."""
    current_labels = col_names_dict[utils.LABEL_COLS_KEY]
    
    # Create dictionary with names of label columns and label values
    label_values_dict = {}
    for label in current_labels:
        # TODO FutureWarning: unique with argument that is not not a Series, Index, ExtensionArray, 
        # or np.ndarray is deprecated and will raise in a future version.
        label_values_dict[label] = pd.unique(input_dataframe[label].values.tolist()).tolist()
    return label_values_dict


def update_label_values_dict_with_inters(label_values_dict):
    inters_label_values_dict = {}
    current_var_values = list(label_values_dict.values())
    current_vars = list(label_values_dict.keys())
    # n_vars = len(label_values_dict.keys())
    var_combination_name = "::".join(current_vars)
    inters_label_values_dict[var_combination_name] = []
    subset_intersections = itertools.product(*current_var_values)
    for intersection in subset_intersections:
        intersection_name = "::".join(map(str, intersection))
        inters_label_values_dict[var_combination_name].append(intersection_name)
    return inters_label_values_dict


def get_subset_dict(input_dataframe, tok_columns_dict, label_values_dict):
    """create a dictionary containing all the subsets of the datasets we will be analyzing."""
    # TODO handle nan values for a specific label.
    current_vars = label_values_dict.keys()
    subsets_of_interest = {}
    # loop through all columns containing text
    for text_column in tok_columns_dict:
        tokenized_text_column = tok_columns_dict[text_column]
        # Loop through all columns containing labels
        for label in current_vars:
            current_label_subset = []
            for label_value in label_values_dict[label]:
                df_slice_with_current_label = input_dataframe[(input_dataframe[label] == label_value)]
                series_with_current_label = df_slice_with_current_label[tokenized_text_column]
                # if the series contains 2 or more elements, we squeeze it
                if len(series_with_current_label) > 1:
                    series_with_current_label = series_with_current_label.squeeze()
                series_with_current_label = series_with_current_label.rename(label_value)
                current_label_subset.append(series_with_current_label)
            subsets_of_interest[label] = current_label_subset    
    return subsets_of_interest    


def get_subset_intersections(input_dataframe, tok_columns_dict, label_values_dict):
    current_var_values = list(label_values_dict.values())
    current_vars = list(label_values_dict.keys())
    n_vars = len(label_values_dict.keys())
    var_combination_name = "::".join(current_vars)
    subsets_of_interest = {var_combination_name: []}
    for text_column in tok_columns_dict:
        tokenized_text_column = tok_columns_dict[text_column]
        subset_intersections = list(itertools.product(*current_var_values))
        for i in tqdm(range(len(subset_intersections))):
            intersection = subset_intersections[i]
            current_subset = input_dataframe
            intersection_name = "::".join(map(str, intersection))
            for i in range(n_vars):
                current_subset = current_subset[(current_subset[current_vars[i]] == intersection[i])]
            # if the series contains 2 or more elements, we squeeze it
            if len(current_subset) > 1:
                current_subset = current_subset.squeeze()
            series_with_current_inters = current_subset[tokenized_text_column]
            subsets_of_interest[intersection_name] = current_subset
            series_with_current_inters = series_with_current_inters.rename(intersection_name)
            subsets_of_interest[var_combination_name].append(series_with_current_inters)
    return subsets_of_interest