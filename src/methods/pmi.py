import pandas as pd
from itertools import islice
from src.methods import shared_metrics
import math
from collections import Counter
import math
import numpy as np
from tqdm import tqdm


def safe_divide(numerator, denominator):
        if denominator == 0 or denominator == 0.0:
            result = 0
        else:
            result = numerator/denominator
        return result

def take(n, iterable):
    """Return the first n items of the iterable as a list."""
    return list(islice(iterable, n))

def get_total(freqs_merged_dict):
    total = 0
    for w in freqs_merged_dict: total += freqs_merged_dict[w]
    return(total)

def create_pmi_dictionary(label_values_dict, subsets_of_interest, weighted, freq_cutoff):
    output_pmi = dict()
    freqs_dict = dict()
    freqs_merged_dict = dict()
    totals_dict = dict()
    label_count = dict()

    for column in label_values_dict:
        print(f"INFO: Creating PMI dictionary for {column}:")
        for l in range(len(label_values_dict[column])):
            curr_label = subsets_of_interest[column][l].name
            print(curr_label)
            mydict = shared_metrics.get_all_frequencies(subsets_of_interest[column][l])
            freqs_dict[curr_label] = mydict
            tok_list = list(mydict.keys())
            for i in tqdm(range(len(tok_list))):
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
                # pmi_value = math.log(pxy/(px*py))
                pmi_value = math.log(safe_divide(pxy,(px*py)))
                if weighted:
                    pmi_value = pmi_value*freqs_dict[label][w]
                label_pmi_dict[w] = pmi_value
        
        sorted_pmiDict = sorted(label_pmi_dict.items(), key=lambda x:x[1], reverse=True)

        converted_dict = dict(sorted_pmiDict)
        output_pmi[label] = converted_dict

    return output_pmi


def pmi(label_values_dict, subsets_of_interest, args):
    output_pmi = create_pmi_dictionary(label_values_dict, subsets_of_interest, False, args.freq_cutoff)
    
    # # Print for debug
    # for label in output_pmi:
    #     sorted_mydict = sorted(output_pmi[label].items(), key=lambda x:x[1], reverse=True)
    #     converted_dict = dict(sorted_mydict)
    #     print("\nPMI", label, take(10, converted_dict.items())) #print for debug

    return output_pmi

def pmi_normalized(label_values_dict, subsets_of_interest, args):
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
            output_pmi[label][w] = safe_divide((output_pmi[label][w] - min_value) , (max_value - min_value))

    # # Print for debug
    # for label in output_pmi:
    #     sorted_mydict = sorted(output_pmi[label].items(), key=lambda x:x[1], reverse=True)
    #     converted_dict = dict(sorted_mydict)
    #     print("\nPositive PMI normalized", label, take(10, converted_dict.items())) #print for debug

    return output_pmi










def pmi_weighted(label_values_dict, subsets_of_interest, args):
    output_pmi = create_pmi_dictionary(label_values_dict, subsets_of_interest, True, args.freq_cutoff)
    
    # # Print for debug
    # for label in output_pmi:
    #     sorted_mydict = sorted(output_pmi[label].items(), key=lambda x:x[1], reverse=True)
    #     converted_dict = dict(sorted_mydict)
    #     print("\nPMI weighted", label, take(10, converted_dict.items())) #print for debug

    return output_pmi

def pmi_normalized_weighted(label_values_dict, subsets_of_interest, args):
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
            output_pmi[label][w] = safe_divide((output_pmi[label][w] - min_value) , (max_value - min_value))

    # # Print for debug
    # for label in output_pmi:
    #     sorted_mydict = sorted(output_pmi[label].items(), key=lambda x:x[1], reverse=True)
    #     converted_dict = dict(sorted_mydict)
    #     print("\nPositive PMI normalized weighted", label, take(10, converted_dict.items())) #print for debug

    return output_pmi

