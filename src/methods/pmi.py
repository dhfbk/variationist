import pandas as pd
from itertools import islice
from src.methods import shared_metrics
import math
from collections import Counter
import math
import numpy as np
from tqdm import tqdm

def take(n, iterable):
    """Return the first n items of the iterable as a list."""
    return list(islice(iterable, n))

def get_total(freqs_merged_dict):
    total = 0
    for w in freqs_merged_dict: total += freqs_merged_dict[w]
    return(total)

def create_pmi_dictionary(label_values_dict, subsets_of_interest):
    output_pmi = dict()
    freqs_dict = dict()
    freqs_merged_dict = dict()
    totals_dict= dict()
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
                label_count[curr_label]+=1
    
    total = get_total(freqs_merged_dict)
    
    for label in freqs_dict:
        label_pmi_dict = dict()
        for w in freqs_dict[label]:
            if freqs_dict[label][w] < 3:
                continue
            pxy = freqs_dict[label][w]/total
            px = label_count[label]/total
            py = freqs_merged_dict[w]/total
            pmi_value = math.log(pxy/(px*py))
            label_pmi_dict[w] = pmi_value
        
        sorted_pmiDict = sorted(label_pmi_dict.items(), key=lambda x:x[1], reverse=True)

        converted_dict = dict(sorted_pmiDict)
        output_pmi[label] = converted_dict
    return output_pmi

def pmi(label_values_dict, subsets_of_interest):
    output_pmi = create_pmi_dictionary(label_values_dict, subsets_of_interest)
    
    # Print for debug
    for label in output_pmi:
        sorted_mydict = sorted(output_pmi[label].items(), key=lambda x:x[1], reverse=True)
        converted_dict = dict(sorted_mydict)
        print("\nPMI", label, take(10, converted_dict.items())) #print for debug

    return output_pmi

def pmi_normalized(label_values_dict, subsets_of_interest):
    output_pmi = create_pmi_dictionary(label_values_dict, subsets_of_interest)      
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
    
    # Print for debug
    for label in output_pmi:
        sorted_mydict = sorted(output_pmi[label].items(), key=lambda x:x[1], reverse=True)
        converted_dict = dict(sorted_mydict)
        print("\nPMI normalized", label, take(10, converted_dict.items())) #print for debug

    return output_pmi


def pmi_positive(label_values_dict, subsets_of_interest):
    output_pmi = create_pmi_dictionary(label_values_dict, subsets_of_interest)   
    for label in output_pmi:
        for w in output_pmi[label]:
            if output_pmi[label][w] < 0:
                output_pmi[label][w] = 0        

    # Print for debug
    for label in output_pmi:
        sorted_mydict = sorted(output_pmi[label].items(), key=lambda x:x[1], reverse=True)
        converted_dict = dict(sorted_mydict)
        print("\nPositive PMI", label, take(10, converted_dict.items())) #print for debug

    return output_pmi


def pmi_positive_normalized(label_values_dict, subsets_of_interest):
    output_pmi = create_pmi_dictionary(label_values_dict, subsets_of_interest)   
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
            output_pmi[label][w] = (output_pmi[label][w] - min_value) / (max_value - min_value)

    # Print for debug
    for label in output_pmi:
        sorted_mydict = sorted(output_pmi[label].items(), key=lambda x:x[1], reverse=True)
        converted_dict = dict(sorted_mydict)
        print("\nPositive PMI normalized", label, take(10, converted_dict.items())) #print for debug

    return output_pmi
    #     minmxlist.append(min(output_pmi[label].values()))
    #     minmxlist.append(max(output_pmi[label].values()))

    # min_value = min(minmxlist)
    # max_value = max(minmxlist)
    
    # for label in freqs_dict:
    #     for w in output_pmi[label]:
    #         output_pmi[label][w] = (output_pmi[label][w] - min_value) / (max_value - min_value)
    

    # return output_pmi
                



    # output_pmi = create_pmi_dictionary(label_values_dict, subsets_of_interest)   
    # for label in output_pmi:
    #     for w in output_pmi[label]:
    #         if output_pmi[label][w] < 0:
    #             output_pmi[label][w] = 0        
    #     minmxlist.append(min(output_pmi[label].values()))
    #     minmxlist.append(max(output_pmi[label].values()))

    # min_value = min(minmxlist)
    # max_value = max(minmxlist)
    
    # for label in freqs_dict:
    #     for w in output_pmi[label]:
    #         output_pmi[label][w] = (output_pmi[label][w] - min_value) / (max_value - min_value)
    

    # return output_pmi