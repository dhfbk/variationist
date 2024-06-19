import math
import numpy as np
import pandas as pd
from collections import Counter
from itertools import islice
from tqdm import tqdm

from variationist.metrics import shared_metrics, lexical_artifacts


def safe_divide(numerator, denominator):
    """Utility function to avoid zero division errors."""
    if denominator == 0 or denominator == 0.0:
        result = 0
    else:
        result = numerator / denominator

    return result


def take(n, iterable):
    """Return the first n items of the iterable as a list."""
    return list(islice(iterable, n))


def get_total(freqs_merged_dict):
    """Function to add up the frequency of tokens across labels."""
    total = 0
    for w in freqs_merged_dict: total += freqs_merged_dict[w]
    return total


def create_pmi_dictionary(label_values_dict, subsets_of_interest, weighted, freq_cutoff):
    """Creates a dictionary of pmi values for each label."""
    output_pmi = dict()
    freqs_dict = dict()
    freqs_merged_dict = dict()
    totals_dict = dict()
    label_count = dict()

    for column in label_values_dict:
        # print(subsets_of_interest[column])
        for l in tqdm(range(len(label_values_dict[column]))):
            curr_label = subsets_of_interest[column][l].name
            mydict = shared_metrics.get_all_frequencies(subsets_of_interest[column][l])
            freqs_dict[curr_label] = mydict
            tok_list = list(mydict.keys())

            for i in range(len(tok_list)):
                tok = tok_list[i]
                if tok not in freqs_merged_dict:
                    freqs_merged_dict[tok] = 0
                freqs_merged_dict[tok] += mydict[tok]

            for i in subsets_of_interest[column][l]:
                if curr_label not in label_count:
                    label_count[curr_label] = 0
                label_count[curr_label] += 1

    total = get_total(freqs_merged_dict)

    # Keep only tokens above the overall frequency cutoff for the PMI (the total remains the same)
    freqs_merged_dict = {
        tok: count for tok, count in freqs_merged_dict.items() if count >= freq_cutoff
    }

    for label in freqs_dict:
        label_pmi_dict = dict()

        for w in freqs_dict[label]:
            if w in freqs_merged_dict:
                pxy = freqs_dict[label][w]/total
                px = label_count[label]/total
                py = freqs_merged_dict[w]/total
                # pmi_value = math.log2(pxy/(px*py))
                pmi_value = math.log2(safe_divide(pxy,(px*py)))
                if weighted:
                    pmi_value = pmi_value*freqs_dict[label][w]
                label_pmi_dict[w] = pmi_value
        
        sorted_pmiDict = sorted(label_pmi_dict.items(), key=lambda x:x[1], reverse=True)

        converted_dict = dict(sorted_pmiDict)
        output_pmi[str(label)] = converted_dict

    return output_pmi


def pmi(label_values_dict, subsets_of_interest, args):
    """Function to calculate PMI.
    
    Parameters
    ----------
    label_values_dict (`dict`):
        A dictionary containing all of the possible values each variable can take in the input dataset.
    subsets_of_interest (`dict`):
        A dictionary containing a pandas series with tokenized texts for each variable/text column combination out of the variables and text columns specified by the user.
    args (`InspectorArgs`):
        The arguments selected by the user.
        
    Returns
    -------
    output_pmi (`dict`):
        A dictionary with the pmi for each token in each subset of interest.
    """
    output_pmi = create_pmi_dictionary(label_values_dict, subsets_of_interest, False, args.freq_cutoff)
    
    # # Print for debug
    # for label in output_pmi:
    #     sorted_mydict = sorted(output_pmi[label].items(), key=lambda x:x[1], reverse=True)
    #     converted_dict = dict(sorted_mydict)
    #     print("\nPMI", label, take(10, converted_dict.items())) #print for debug

    return output_pmi


def pmi_normalized(label_values_dict, subsets_of_interest, args):
    """Function to calculate normalized PMI.
    
    Parameters
    ----------
    label_values_dict (`dict`):
        A dictionary containing all of the possible values each variable can take in the input dataset.
    subsets_of_interest (`dict`):
        A dictionary containing a pandas series with tokenized texts for each variable/text column combination out of the variables and text columns specified by the user.
    args (`InspectorArgs`):
        The arguments selected by the user.
        
    Returns
    -------
    output_pmi (`dict`):
        A dictionary with the normalized pmi for each token in each subset of interest.
    """
    output_pmi = create_pmi_dictionary(label_values_dict, subsets_of_interest, False, args.freq_cutoff)
    min_max_list = []
    
    for label in output_pmi:
        if len(output_pmi[label]) > 0: # if the list is not empty
            min_max_list.append(min(output_pmi[label].values()))
            min_max_list.append(max(output_pmi[label].values()))

    min_value = min(min_max_list)
    max_value = max(min_max_list)
    
    for label in output_pmi:
        for w in output_pmi[label]:
            output_pmi[label][w] = (output_pmi[label][w] - min_value) / (max_value - min_value)
    
    # # Print for debug
    # for label in output_pmi:
    #     sorted_mydict = sorted(output_pmi[label].items(), key=lambda x:x[1], reverse=True)
    #     converted_dict = dict(sorted_mydict)
    #     print("\nPMI normalized", label, take(10, converted_dict.items())) #print for debug

    return output_pmi


def pmi_positive(label_values_dict, subsets_of_interest, args):
    """Function to calculate positive PMI (negative values are set to 0).
    
    Parameters
    ----------
    label_values_dict (`dict`):
        A dictionary containing all of the possible values each variable can take in the input dataset.
    subsets_of_interest (`dict`):
        A dictionary containing a pandas series with tokenized texts for each variable/text column combination out of the variables and text columns specified by the user.
    args (`InspectorArgs`):
        The arguments selected by the user.
        
    Returns
    -------
    output_pmi (`dict`):
        A dictionary with the positive PMI for each token in each subset of interest.
    """
    output_pmi = create_pmi_dictionary(label_values_dict, subsets_of_interest, False, args.freq_cutoff)
    
    for label in output_pmi:
        for w in output_pmi[label]:
            if output_pmi[label][w] < 0:
                output_pmi[label][w] = 0

    # # Print for debug
    # for label in output_pmi:
    #     sorted_mydict = sorted(output_pmi[label].items(), key=lambda x:x[1], reverse=True)
    #     converted_dict = dict(sorted_mydict)
    #     print("\nPositive PMI", label, take(10, converted_dict.items())) #print for debug

    return output_pmi


def pmi_positive_normalized(label_values_dict, subsets_of_interest, args):
    """Function to calculate positive normalized PMI (negative values are set to 0 and all values are normalized between 0 and 1).
    
    Parameters
    ----------
    label_values_dict (`dict`):
        A dictionary containing all of the possible values each variable can take in the input dataset.
    subsets_of_interest (`dict`):
        A dictionary containing a pandas series with tokenized texts for each variable/text column combination out of the variables and text columns specified by the user.
    args (`InspectorArgs`):
        The arguments selected by the user.
        
    Returns
    -------
    output_pmi (`dict`):
        A dictionary with the positive normalized PMI for each token in each subset of interest.
    """
    output_pmi = create_pmi_dictionary(label_values_dict, subsets_of_interest, False, args.freq_cutoff)

    min_max_list = []
    for label in output_pmi:
        for w in output_pmi[label]:
            if output_pmi[label][w] < 0:
                output_pmi[label][w] = 0
        if len(output_pmi[label]) > 0: # if the list is not empty
            min_max_list.append(min(output_pmi[label].values()))
            min_max_list.append(max(output_pmi[label].values()))

    min_value = min(min_max_list)
    max_value = max(min_max_list)
    
    for label in output_pmi:
        for w in output_pmi[label]:
            output_pmi[label][w] = safe_divide(
                (output_pmi[label][w] - min_value) , (max_value - min_value)
            )

    # # Print for debug
    # for label in output_pmi:
    #     sorted_mydict = sorted(output_pmi[label].items(), key=lambda x:x[1], reverse=True)
    #     converted_dict = dict(sorted_mydict)
    #     print("\nPositive PMI normalized", label, take(10, converted_dict.items())) #print for debug

    return output_pmi


def pmi_weighted(label_values_dict, subsets_of_interest, args):
    """Function to calculate weighted PMI.
    
    Parameters
    ----------
    label_values_dict (`dict`):
        A dictionary containing all of the possible values each variable can take in the input dataset.
    subsets_of_interest (`dict`):
        A dictionary containing a pandas series with tokenized texts for each variable/text column combination out of the variables and text columns specified by the user.
    args (`InspectorArgs`):
        The arguments selected by the user.
        
    Returns
    -------
    output_pmi (`dict`):
        A dictionary with the weighted PMI for each token in each subset of interest.
    """
    output_pmi = create_pmi_dictionary(label_values_dict, subsets_of_interest, True, args.freq_cutoff)
    
    # # Print for debug
    # for label in output_pmi:
    #     sorted_mydict = sorted(output_pmi[label].items(), key=lambda x:x[1], reverse=True)
    #     converted_dict = dict(sorted_mydict)
    #     print("\nPMI weighted", label, take(10, converted_dict.items())) #print for debug

    return output_pmi


def pmi_normalized_weighted(label_values_dict, subsets_of_interest, args):
    """Function to calculate normalized weighted PMI.
    
    Parameters
    ----------
    label_values_dict (`dict`):
        A dictionary containing all of the possible values each variable can take in the input dataset.
    subsets_of_interest (`dict`):
        A dictionary containing a pandas series with tokenized texts for each variable/text column combination out of the variables and text columns specified by the user.
    args (`InspectorArgs`):
        The arguments selected by the user.
        
    Returns
    -------
    output_pmi (`dict`):
        A dictionary with the normalized weighted PMI for each token in each subset of interest.
    """
    output_pmi = create_pmi_dictionary(label_values_dict, subsets_of_interest, True, args.freq_cutoff)

    min_max_list = []
    for label in output_pmi:
        if len(output_pmi[label]) > 0: # if the list is not empty
            min_max_list.append(min(output_pmi[label].values()))
            min_max_list.append(max(output_pmi[label].values()))

    min_value = min(min_max_list)
    max_value = max(min_max_list)
    
    for label in output_pmi:
        for w in output_pmi[label]:
            output_pmi[label][w] = (output_pmi[label][w] - min_value) / (max_value - min_value)
    
    # # Print for debug
    # for label in output_pmi:
    #     sorted_mydict = sorted(output_pmi[label].items(), key=lambda x:x[1], reverse=True)
    #     converted_dict = dict(sorted_mydict)
    #     print("\nPMI normalized weighted", label, take(10, converted_dict.items())) #print for debug

    return output_pmi


def pmi_positive_weighted(label_values_dict, subsets_of_interest, args):
    """Function to calculate positive weighted PMI.
    
    Parameters
    ----------
    label_values_dict (`dict`):
        A dictionary containing all of the possible values each variable can take in the input dataset.
    subsets_of_interest (`dict`):
        A dictionary containing a pandas series with tokenized texts for each variable/text column combination out of the variables and text columns specified by the user.
    args (`InspectorArgs`):
        The arguments selected by the user.
        
    Returns
    -------
    output_pmi (`dict`):
        A dictionary with the positive weighted PMI for each token in each subset of interest.
    """
    output_pmi = create_pmi_dictionary(label_values_dict, subsets_of_interest, True, args.freq_cutoff)
    for label in output_pmi:
        for w in output_pmi[label]:
            if output_pmi[label][w] < 0:
                output_pmi[label][w] = 0

    # # Print for debug
    # for label in output_pmi:
    #     sorted_mydict = sorted(output_pmi[label].items(), key=lambda x:x[1], reverse=True)
    #     converted_dict = dict(sorted_mydict)
    #     print("\nPositive PMI weighted", label, take(10, converted_dict.items())) #print for debug

    return output_pmi


def pmi_positive_normalized_weighted(label_values_dict, subsets_of_interest, args):
    """Function to calculate positive normalized weighted PMI.
    
    Parameters
    ----------
    label_values_dict (`dict`):
        A dictionary containing all of the possible values each variable can take in the input dataset.
    subsets_of_interest (`dict`):
        A dictionary containing a pandas series with tokenized texts for each variable/text column combination out of the variables and text columns specified by the user.
    args (`InspectorArgs`):
        The arguments selected by the user.
        
    Returns
    -------
    output_pmi (`dict`):
        A dictionary with the positive normalized weighted PMI for each token in each subset of interest.
    """
    output_pmi = create_pmi_dictionary(label_values_dict, subsets_of_interest, True, args.freq_cutoff)

    min_max_list = []
    for label in output_pmi:
        for w in output_pmi[label]:
            if output_pmi[label][w] < 0:
                output_pmi[label][w] = 0
        if len(output_pmi[label]) > 0: # if the list is not empty
            min_max_list.append(min(output_pmi[label].values()))
            min_max_list.append(max(output_pmi[label].values()))

    min_value = min(min_max_list)
    max_value = max(min_max_list)
    
    for label in output_pmi:
        for w in output_pmi[label]:
            output_pmi[label][w] = safe_divide(
                (output_pmi[label][w] - min_value) , (max_value - min_value))

    # # Print for debug
    # for label in output_pmi:
    #     sorted_mydict = sorted(output_pmi[label].items(), key=lambda x:x[1], reverse=True)
    #     converted_dict = dict(sorted_mydict)
    #     print("\nPositive PMI normalized weighted", label, take(10, converted_dict.items())) #print for debug

    return output_pmi


def class_relevance_positive_normalized(label_values_dict, subsets_of_interest, args):
    """Function to calculate a PMI-based class relevance metric, which consists in normalizing by subset the positive normalized PMI values.
    
    Parameters
    ----------
    label_values_dict (`dict`):
        A dictionary containing all of the possible values each variable can take in the input dataset.
    subsets_of_interest (`dict`):
        A dictionary containing a pandas series with tokenized texts for each variable/text column combination out of the variables and text columns specified by the user.
    args (`InspectorArgs`):
        The arguments selected by the user.
        
    Returns
    -------
    output_pmi (`dict`):
        A dictionary with the positive normalized class relevance metric for each token in each subset of interest.
    """
    output_pmi = create_pmi_dictionary(label_values_dict, subsets_of_interest, False, args.freq_cutoff)

    for label in output_pmi:
        if len(output_pmi[label]) > 0: # if the list is not empty
            min_max_list = []
            min_max_list.append(min(output_pmi[label].values()))
            min_max_list.append(max(output_pmi[label].values()))
            min_value = min(min_max_list)
            max_value = max(min_max_list)

            for w in output_pmi[label]:
                output_pmi[label][w] = safe_divide(
                    (output_pmi[label][w]-min_value), (max_value-min_value))
                if output_pmi[label][w] < 0:
                    output_pmi[label][w] = 0

    return output_pmi


def class_relevance_normalized_weighted(label_values_dict, subsets_of_interest, args):
    """Function to calculate a PMI-based class relevance metric, which consists in normalizing by subset the normalized weighted PMI values.
    
    Parameters
    ----------
    label_values_dict (`dict`):
        A dictionary containing all of the possible values each variable can take in the input dataset.
    subsets_of_interest (`dict`):
        A dictionary containing a pandas series with tokenized texts for each variable/text column combination out of the variables and text columns specified by the user.
    args (`InspectorArgs`):
        The arguments selected by the user.
        
    Returns
    -------
    output_pmi (`dict`):
        A dictionary with the normalized weighted class relevance metric for each token in each subset of interest.
    """
    output_pmi = create_pmi_dictionary(label_values_dict, subsets_of_interest, True, args.freq_cutoff)

    for label in output_pmi:
        if len(output_pmi[label]) > 0: # if the list is not empty
            min_max_list = []
            min_max_list.append(min(output_pmi[label].values()))
            min_max_list.append(max(output_pmi[label].values()))
            min_value = min(min_max_list)
            max_value = max(min_max_list)

            for w in output_pmi[label]:
                output_pmi[label][w] = safe_divide(
                    (output_pmi[label][w]-min_value), (max_value-min_value)
                )

    return output_pmi


def class_relevance_positive_normalized_weighted(label_values_dict, subsets_of_interest, args):
    """Function to calculate a PMI-based class relevance metric, which consists in normalizing by subset the positive normalized weighted PMI values.
    
    Parameters
    ----------
    label_values_dict (`dict`):
        A dictionary containing all of the possible values each variable can take in the input dataset.
    subsets_of_interest (`dict`):
        A dictionary containing a pandas series with tokenized texts for each variable/text column combination out of the variables and text columns specified by the user.
    args (`InspectorArgs`):
        The arguments selected by the user.
        
    Returns
    -------
    output_pmi (`dict`):
        A dictionary with the positive normalized weighted class relevance metric for each token in each subset of interest.
    """
    output_pmi = create_pmi_dictionary(label_values_dict, subsets_of_interest, True, args.freq_cutoff)

    for label in output_pmi:
        if len(output_pmi[label]) > 0: # if the list is not empty
            min_max_list = []
            min_max_list.append(min(output_pmi[label].values()))
            min_max_list.append(max(output_pmi[label].values()))
            min_value = min(min_max_list)
            max_value = max(min_max_list)

            for w in output_pmi[label]:
                output_pmi[label][w] = safe_divide(
                    (output_pmi[label][w]-min_value), (max_value-min_value))
                if output_pmi[label][w] < 0:
                    output_pmi[label][w] = 0

    return output_pmi


def pmi_lexical_artifacts(label_values_dict, subsets_of_interest, args):
    """Function to calculate a PMI-based class relevance metric as illustrated in Ramponi and Tonelli (2022).
    
    Parameters
    ----------
    label_values_dict (`dict`):
        A dictionary containing all of the possible values each variable can take in the input dataset.
    subsets_of_interest (`dict`):
        A dictionary containing a pandas series with tokenized texts for each variable/text column combination out of the variables and text columns specified by the user.
    args (`InspectorArgs`):
        The arguments selected by the user.
        
    Returns
    -------
    lexical_artifacts_dict (`dict`):
        A dictionary with the associated lexical-artifacts scores for each token in each subset.
    """
    texts_list = []
    labels_list = []
    
    for column in label_values_dict:
            
        for l in range(len(label_values_dict[column])):
            curr_label = subsets_of_interest[column][l].name
                
            for text in subsets_of_interest[column][l]:
                texts_list.append(" ".join(text))
                labels_list.append(str(curr_label))
                    
        uniqe_labels = list(dict.fromkeys(labels_list))

        lexical_artifacts_dict = dict()
        for label in uniqe_labels:
            lexical_artifacts_dict[label] = dict()
            values_df = lexical_artifacts.compute(
                texts = texts_list,
                labels = labels_list,
                label_of_interest = label,
            )
                
            top_k = len(values_df)
                
            for token, row in values_df.head(top_k).iterrows():
                lexical_artifacts_dict[label][token] = row[values_df.columns[0]]
                
        return lexical_artifacts_dict
