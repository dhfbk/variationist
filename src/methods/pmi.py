import pandas as pd
from itertools import islice
from src.methods import shared_metrics
import math

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
        for l in label_values_dict[column]:            
            mydict = shared_metrics.get_all_frequencies(subsets_of_interest[column][l])
            freqs_dict[l] = mydict
            for i in mydict:
                if i not in freqs_merged_dict:
                    freqs_merged_dict[i] = 0
                freqs_merged_dict[i] += mydict[i]
            for i in subsets_of_interest[column][l]:
                if l not in label_count:
                    label_count[l] = 0
                label_count[l]+=1
    
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
        n_items = take(15, converted_dict.items())
        output_pmi[label] = n_items
            
    return output_pmi