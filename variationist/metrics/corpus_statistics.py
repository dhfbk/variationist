"""Functions for calculating a series of statistics for a given corpus."""

import pandas as pd
from itertools import islice
from statistics import stdev, mean
from tqdm import tqdm

from variationist.metrics import shared_metrics


def take(n, iterable):
    """Return the first n items of the iterable as a list."""
    return list(islice(iterable, n))


def number_of_texts(label_values_dict, subsets_of_interest):
    """Returns a dictionary with how many texts are in each subset of interest.
    
    Parameters
    ----------
    label_values_dict (`dict`):
        A dictionary containing all of the possible values each variable can take in the input dataset.
    subsets_of_interest (`dict`):
        A dictionary containing a pandas series with tokenized texts for each variable/text column combination out of the variables and text columns specified by the user.
        
    Returns
    -------
    values_dict (`dict`):
        A dict containing the length of each subset.
    """
    values_dict = dict()
    for column in label_values_dict:
        for l in range(len(label_values_dict[column])):
            curr_label = subsets_of_interest[column][l].name
            values_dict[curr_label] = len(subsets_of_interest[column][l])

    return values_dict


def average_text_length(label_values_dict, subsets_of_interest):
    """Returns a dictionary with the average length of texts in each subset of interest.
    
    Parameters
    ----------
    label_values_dict (`dict`):
        A dictionary containing all of the possible values each variable can take in the input dataset.
    subsets_of_interest (`dict`):
        A dictionary containing a pandas series with tokenized texts for each variable/text column combination out of the variables and text columns specified by the user.
        
    Returns
    -------
    values_dict (`dict`):
        A dict containing the average length (and its standard deviation) of texts in each subset.
    """
    values_dict = dict()
    for column in label_values_dict:
        for l in range(len(label_values_dict[column])):
            values_list = []
            curr_label = subsets_of_interest[column][l].name
            for text in subsets_of_interest[column][l]:
                if len(text) == 0:
                    continue
                values_list.append(len(text))
            values_dict[curr_label] = dict()
            if len(values_list) == 0:
                values_dict[curr_label]["mean"] = 0
            else:
                values_dict[curr_label]["mean"] = mean(values_list)
            if len(values_list) < 2:
                values_dict[curr_label]["stdev"] = 0
            else:
                values_dict[curr_label]["stdev"] = stdev(values_list)
    return values_dict


def num_tokens(label_values_dict, subsets_of_interest):
    """Returns a dictionary with the total number of tokens in each subset.
    
    Parameters
    ----------
    label_values_dict (`dict`):
        A dictionary containing all of the possible values each variable can take in the input dataset.
    subsets_of_interest (`dict`):
        A dictionary containing a pandas series with tokenized texts for each variable/text column combination out of the variables and text columns specified by the user.
        
    Returns
    -------
    n_word_dict (`dict`):
        A dict containing the total number of tokens in each subset."""
    n_word_dict = dict()
    for column in label_values_dict:
        for l in range(len(label_values_dict[column])):
            curr_label = subsets_of_interest[column][l].name
            n_word_dict[curr_label] = 0
            for text in subsets_of_interest[column][l]:
                if len(text) == 0:
                    continue
                n_word_dict[curr_label] = n_word_dict[curr_label]+(len(text))
    
    return n_word_dict


def vocab_size(label_values_dict, subsets_of_interest):
    """Returns a dictionary with the total number of unique tokens in each subset - i.e. the size of the vocabulary for each subset.
    
    Parameters
    ----------
    label_values_dict (`dict`):
        A dictionary containing all of the possible values each variable can take in the input dataset.
    subsets_of_interest (`dict`):
        A dictionary containing a pandas series with tokenized texts for each variable/text column combination out of the variables and text columns specified by the user.
        
    Returns
    -------
    vocab_dict (`dict`):
        A dict containing the vocabulary size of each subset."""
    vocab_dict = dict()
    for column in label_values_dict:
        for l in range(len(label_values_dict[column])):
            curr_label = subsets_of_interest[column][l].name
            vocab_dict[curr_label] = set()
            for text in subsets_of_interest[column][l]:
                if len(text) == 0:
                    continue
                vocab_dict[curr_label].update(text)
            vocab_dict[curr_label] = len(vocab_dict[curr_label])

    return vocab_dict


def number_of_duplicates(label_values_dict, subsets_of_interest):
    """Returns a dictionary with the number of duplicate texts in each subset of interest.
    
    Parameters
    ----------
    label_values_dict (`dict`):
        A dictionary containing all of the possible values each variable can take in the input dataset.
    subsets_of_interest (`dict`):
        A dictionary containing a pandas series with tokenized texts for each variable/text column combination out of the variables and text columns specified by the user.
        
    Returns
    -------
    duplicates_dict (`dict`):
        A dict containing the number of duplicate texts in each subset."""
        
    duplicates_dict = dict()
    for column in label_values_dict:
        for l in range(len(label_values_dict[column])):
            text_dic = dict()
            duplicates = 0
            curr_label = subsets_of_interest[column][l].name
            for text in subsets_of_interest[column][l]:
                if len(text) == 0:
                    continue
                if " ".join(text) in text_dic:
                    duplicates += 1
                text_dic[" ".join(text)] = ""
            duplicates_dict[curr_label] = duplicates

    return duplicates_dict


def create_frequency_dictionary(label_values_dict, subsets_of_interest, args):
    """Returns a dictionary with the frequency of tokens in each subset of interest.
    
    Parameters
    ----------
    label_values_dict (`dict`):
        A dictionary containing all of the possible values each variable can take in the input dataset.
    subsets_of_interest (`dict`):
        A dictionary containing a pandas series with tokenized texts for each variable/text column combination out of the variables and text columns specified by the user.
        
    Returns
    -------
    output_freqs (`dict`):
        A dict containing the frequency of each token for each subset of interest."""
    output_freqs = dict()
    for column in label_values_dict:
        for l in tqdm(range(len(label_values_dict[column]))):
            curr_label = subsets_of_interest[column][l].name
            mydict = shared_metrics.get_all_frequencies(subsets_of_interest[column][l])
            sorted_mydict = sorted(mydict.items(), key=lambda x:x[1], reverse=True)
            converted_dict = dict(sorted_mydict)
            output_freqs[curr_label] = converted_dict
            # print("most frequent", curr_label, take(10, converted_dict.items())) #print for debug          
    return output_freqs


def compute_basic_stats(label_values_dict, subsets_of_interest, args):
    """A wrapper function for calling all of the basic statistics functions."""
    stats_dict = dict()
    for stat in ["num_texts", 
                 "avg_text_len",
                 "num_tokens",
                 "vocab_size",
                 "num_duplicates"]:
        stats_dict[stat] = {}
    stats_dict["num_texts"][list(label_values_dict.keys())[0]] = number_of_texts(label_values_dict, subsets_of_interest)
    stats_dict["avg_text_len"][list(label_values_dict.keys())[0]] = average_text_length(label_values_dict, subsets_of_interest)
    stats_dict["num_tokens"][list(label_values_dict.keys())[0]] = num_tokens(label_values_dict, subsets_of_interest)
    stats_dict["vocab_size"][list(label_values_dict.keys())[0]] = vocab_size(label_values_dict, subsets_of_interest)
    stats_dict["num_duplicates"][list(label_values_dict.keys())[0]] = number_of_duplicates(label_values_dict, subsets_of_interest)
    # print(stats_dict)
    return stats_dict

