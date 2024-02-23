import pandas as pd
from itertools import islice
from src.methods import shared_metrics

def take(n, iterable):
    """Return the first n items of the iterable as a list."""
    return list(islice(iterable, n))

def create_most_frequent_dictionary(label_values_dict, subsets_of_interest):
    # TODO change the name of this function: it just calculates frequency!
    output_freqs = dict()
    for column in label_values_dict:
        for l in range(len(label_values_dict[column])):
            curr_label = subsets_of_interest[column][l].name
            mydict = shared_metrics.get_all_frequencies(subsets_of_interest[column][l])
            
            sorted_mydict = sorted(mydict.items(), key=lambda x:x[1], reverse=True)
            converted_dict = dict(sorted_mydict)
            output_freqs[curr_label] = converted_dict
            
            print("most frequent", curr_label, take(10, converted_dict.items())) #print for debug
            
    return output_freqs