import itertools
import os
import pandas as pd
import re
import stopwordsiso as stopwords
import sys
from tqdm import tqdm

from variationist import utils
from variationist.data import tokenization_utils


def remove_elements(token_list, stopwords):
    """"
    Used for removing stopwords. Given a token array, it will return the same array 
    excluding the elements in stopwords. Used to remove stopwords at the text level.
    
    Parameters
    ----------
    token_list (`Iterable`):
        An array of tokens.
    stopwords (`Iterable`):
        Array of stopwords to be removed from token_list.
        
    Returns
    -------
    new_array (`Iterable`):
        The same array, with stopwords removed.
    """

    new_array = []
    for element in token_list:
        if element.lower() not in stopwords:
            new_array.append(element)

    return new_array


def remove_stopwords(text_column, language, custom_stopwords):
    """"
    Used for removing stopwords. Given an already tokenized pandas Series of texts, 
    it will return the same series, excluding the elements in stopwords. Used to 
    remove stopwords at the column level.
    
    Parameters
    ----------
    token_column (`pandas.Series`):
        A series containing the already tokenized texts.
    language (`str`):
        The language we should retrieve stopwords for.
    custom_stopwords (`Optional[Union[str, list]]`):
        A list of stopwords (or a path to a file containing stopwords, one per line) 
        to be removed before tokenization. If `stopwords` is True, these stopwords 
        will be added to that list. Will default to None.
        
    Returns
    -------
    text_column (`pandas.Series`):
        The same tokenized series as input, with stopwords removed.
    """

    lang_stopwords = []

    # Language need to be ISO 639-1 (two-letter codes, e.g., en, it, fr, de, etc.) 
    if language != None:
        lang_stopwords = stopwords.stopwords(language)
    
    if custom_stopwords != None:
        extra_stopwords = get_custom_stopword_list(custom_stopwords)
        lang_stopwords.update(extra_stopwords)

    text_column = text_column.squeeze().apply(lambda x: remove_elements(x, lang_stopwords))

    return text_column


def get_custom_stopword_list(custom_stopwords):
    """
    Function that returns a list of stopwords from a file (one stopword per line)
    or returns the list itself
    
    Parameters
    ----------
    custom_stopwords (`Optional[Union[str, list]]`):
        A list of stopwords (or a path to a file containing stopwords, one per line) 
        to be removed before tokenization. If `stopwords` is True, these stopwords 
        will be added to that list. Will default to None.
        
    Returns
    -------
    extra_stopwords (`list`):
        A list including the custom stopwords.
    """

    if (type(custom_stopwords) == list):
        extra_stopwords = custom_stopwords
    else:
        extra_stopwords = []
        with open(custom_stopwords, "r") as f:
            for line in f:
                extra_stopwords.append(line.rstrip("\n"))

    return extra_stopwords


def convert_to_ngrams(token_list, n_tokens):
    """
    Function for creating n-grams from tokens. Given a list of tokens and the number 
    of tokens for the n-grams, it returns the same list, but with n-grams as units 
    instead of single tokens. Used to create n-grams at the text level.
    
    Parameters
    ----------
    token_list (`Iterable`):
        An array of tokens.
    n_tokens (`int`):
        The n to use for n-grams. E.g., a value of 2 will result in bi-grams.
        
    Returns
    -------
    new_array (`Iterable`):
        The same array, with n-grams instead of single tokens as units.
    """

    new_array = []
    for i in range(len(token_list) - n_tokens + 1):
        new_array.append(" ".join(token_list[i: i + n_tokens]))
    
    return new_array


def create_tokenized_ngrams_column(tokenized_text_column, n_tokens):
    """
    Function for creating n-grams from tokens. Given an already tokenized pandas 
    Series of texts, it will return the same series, but with n-grams as units 
    instead of single tokens. Used to create n-grams at the text column level.
    
    Parameters
    ----------
    tokenized_text_column (`pandas.Series`):
        A series containing the already tokenized texts.
    n_tokens (`int`):
        The n to use for n-grams. E.g., a value of 2 will result in bi-grams.
        
    Returns
    -------
    new_array (`Iterable`):
        The same array, with n-grams instead of single tokens as units.
    """

    tqdm.pandas()
    tokenized_text_column = tokenized_text_column.squeeze().progress_apply(lambda x: convert_to_ngrams(x,n_tokens))
    
    return tokenized_text_column


# @TODO this will be developed in a future release
# def discretize_granularity(dataframe, var_names, var_types, var_semantics, var_granularity):
#     for i in range(len(var_names)):
#         if var_granularity != None:
#             break
#     # then we will map (check pandas docs)
#     return dataframe


def discretize_bins_col(dataframe_var_col, curr_var_bins):
    """
    A function that will split a variable into bins, assigning new values to that 
    variable based on how many bins were selected by the user with the var_bins 
    parameter in InspectorArgs.
    
    Parameters
    ----------
    dataframe_var_col (pandas.Series):
        A pandas Series, corresponding to the pandas Dataframe column containing 
        the variable that should be divided into bins.
    curr_var_bins (`int`):
        The number of bins to divide the current variable into, as specified by 
        the user using var_bins.
    
    Returns
    -------
    discretized_var_col (pandas.Series):
        The same Series as input, but with values split into bins.
    """
    
    discretized_var_col, bin_names = pd.cut(dataframe_var_col,
                                            bins=curr_var_bins,
                                            retbins=True)
    print(f"""INFO: The calculated cutoff values of bins for the {dataframe_var_col.name} variable are:\n{list(bin_names)}\nThese will be reported as (value_x, value_x+1] in the results.""")
    
    return discretized_var_col


def extract_combinations(token_list, n_items, context_window, unique_cooc):
    """A Function that will extract co-occurrences from tokens if this was set by 
    the user. Used to extract co-occurrences at the text level.
    
    Parameters
    ----------
    token_list (`Iterable`):
        An array of tokens for the text, out of which to extract co-occurrences.
    n_items (`int`):
        The number of co-occurring tokens we should consider. Corresponds to `n_cooc` 
        set by the user in InspectorArgs.
    context_window (`int`):
        Size of the context window for co-occurrences, corresponding to `cooc_window_size` 
        in InspectorArgs.
    unique_cooc (`bool`):
        A boolean for whether to consider unique co-occurrences. If True, multiple 
        occurrences of the same token in a text will be discarded.

    Returns
    -------
    new_array (list):
        returns the new array of tokens, with co-occurrences as basic units rather than 
        the original tokens.
    """

    # Returns token_list merged into cooccurrences
    if context_window == 0:
        context_window = len(token_list)
    new_array = []
    for i in range(len(token_list) - context_window + 1):
        for cooc in itertools.combinations(token_list[i: i + context_window], n_items):
            if (not unique_cooc) or ((unique_cooc) and (len(set(cooc)) == len(cooc))):
                new_array.append(" ".join(sorted(cooc)))
    new_array = list(set(new_array))
    
    return new_array
    

def create_tokenized_cooccurrences_column(tokenized_text_column, n_items, context_window, unique_cooc):
    """
    A Function that will extract co-occurrences from tokens if this was set by the user. 
    Used to extract co-occurrences at the column level.
    
    Parameters
    ----------
    tokenized_text_column (`pandas.Series`):
        A series containing the already tokenized texts.
    n_items (`Int`):
        The number of co-occurring tokens we should consider. Corresponds to `n_cooc` 
        set by the user in InspectorArgs.
    context_window (`Int`):
        Size of the context window for co-occurrences, corresponding to `cooc_window_size` 
        in InspectorArgs.
    unique_cooc (`Bool`):
        A boolean for whether to consider unique co-occurrences. If True, multiple 
        occurrences of the same token in a text will be discarded.

    Returns
    -------
    text_column (`pandas.Series`):
        The same tokenized series as input (overall length of the series will be the same), 
        but with co-occurrences in lieu of the original tokens (meaning sequence length will 
        be far lengthier).
    """
    
    if n_items > context_window and context_window!=0:
        sys.exit(f"ERROR: The size of the context windows cannot be lower than the number of words when extracting the cooccurrences!\nExit.")
    tqdm.pandas()

    tokenized_text_column = tokenized_text_column.squeeze().progress_apply(lambda x: extract_combinations(x,n_items,context_window,unique_cooc))
    
    return tokenized_text_column
                                                            

def get_label_values(input_dataframe, col_names_dict):
    """Returns a dictionary with all unique label values for the specified variables.
    
    Parameters
    ----------
    input_dataframe (`pandas.DataFrame`):
        The dataset to be analyzed.
    col_names_dict (`dict`):
        A dictionary containing the var_names provided by the user.
    
    Returns
    -------
    label_values_dict (`dict`):
        A dictionary containing all of the possible values each variable can take in 
        the input dataset.
    """

    current_labels = col_names_dict[utils.LABEL_COLS_KEY]
    
    # Create dictionary with names of label columns and label values
    label_values_dict = {}
    for label in current_labels:
        label_values_dict[label] = pd.unique(input_dataframe[label]).tolist()
    return label_values_dict


def update_label_values_dict_with_inters(label_values_dict, text_names):
    """
    Updates label_values_dict with the intersection names if we have more than 1 var_name 
    or text_name.
    
    Parameters
    ----------
    label_values_dict (`dict`):
        A dictionary containing all of the possible values each variable can take in the 
        input dataset.
    text_names (`list`):
        The list of text column names.
    
    Returns
    -------
    inters_label_values_dict (`dict`):
        A dictionary containing all of the possible intersections of text columns and 
        variables in the input dataset.    
    """

    inters_label_values_dict = {}
    current_var_values = list(label_values_dict.values())
    current_vars = list(label_values_dict.keys())
    # n_vars = len(label_values_dict.keys())
    var_combination_name = "::".join(current_vars)
    if len(text_names) > 1:
        var_combination_name = f"text_name::{var_combination_name}"
        # print(current_var_values)
        current_var_values.append(text_names)
    inters_label_values_dict[var_combination_name] = []
    subset_intersections = itertools.product(*current_var_values)
    for intersection in subset_intersections:
        intersection_name = "::".join(map(str, intersection))
        inters_label_values_dict[var_combination_name].append(intersection_name)

    return inters_label_values_dict


def get_subset_dict(input_dataframe, tok_columns_dict, label_values_dict):
    """
    Creates a dictionary containing all the desired subsets of the dataset we will be analyzing.
    
    Parameters
    ----------
    input_dataframe (`pandas.DataFrame`):
        The dataset to be analyzed.
    tok_columns_dict (`dict`):
        A dictionary containing the names of the columns containing the tokenized specified 
        text columns.
    label_values_dict (`dict`):
        A dictionary containing all of the possible values each variable can take in the 
        input dataset.
        
    Returns
    -------
    subsets_of_interest (`dict`):
        A dictionary containing a pandas series with tokenized texts for each variable value 
        specified by the user.
    """

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
    """
    Creates a dictionary containing all the desired subsets of the dataset we will be 
    analyzing if we have intersections among different text or var columns.
    
    Parameters
    ----------
    input_dataframe (`pandas.DataFrame`):
        The dataset to be analyzed.
    tok_columns_dict (`dict`):
        A dictionary containing the names of the columns containing the tokenized 
        specified text columns.
    label_values_dict (`dict`):
        A dictionary containing all of the possible values each variable can take 
        in the input dataset.
        
    Returns
    -------
    subsets_of_interest (`dict`):
        A dictionary containing a pandas series with tokenized texts for each 
        variable/text column combination out of the variables and text columns 
        specified by the user in the case of multiple text and variable columns.
    """
        
    current_var_values = list(label_values_dict.values())
    current_vars = list(label_values_dict.keys())
    n_vars = len(label_values_dict.keys())
    text_cols = list(tok_columns_dict.keys())
    var_combination_name = "::".join(current_vars)
    if len(text_cols) > 1:
        subsets_of_interest = {f"text_name::{var_combination_name}": []}
    else:
        subsets_of_interest = {var_combination_name: []}
    for text_column in text_cols:
        print("INFO: Splitting intersections of variables into subsets.")
        print(f"Subsets for text column '{text_column}'...")
        tokenized_text_column = tok_columns_dict[text_column]
        subset_intersections = list(itertools.product(*current_var_values))
        for i in tqdm(range(len(subset_intersections))):
            intersection = subset_intersections[i]
            current_subset = input_dataframe
            intersection_name = "::".join(map(str, intersection))
            if len(text_cols) > 1:
                intersection_name = f"{text_column}::{intersection_name}"
            for i in range(n_vars):
                current_subset = current_subset[(current_subset[current_vars[i]] == intersection[i])]
            # if the series contains 2 or more elements, we squeeze it
            if len(current_subset) > 1:
                current_subset = current_subset.squeeze()
            series_with_current_inters = current_subset[tokenized_text_column]
            subsets_of_interest[intersection_name] = current_subset
            series_with_current_inters = series_with_current_inters.rename(intersection_name)
            if len(text_cols) == 1:
                subsets_of_interest[var_combination_name].append(series_with_current_inters)
            else:
                subsets_of_interest[f"text_name::{var_combination_name}"].append(series_with_current_inters)
    
    return subsets_of_interest
