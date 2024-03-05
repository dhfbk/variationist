from src.methods import shared_metrics

def get_label_total(freqs_dict):
    tot_dict= dict()    
    for label in freqs_dict:
        total = 0    
        for w in freqs_dict[label]: total += freqs_dict[label][w]
        tot_dict[label] = total
    return(tot_dict)


def get_unique_words(freqs_dict):
    uniq_dict= dict()    
    for label in freqs_dict:
        uniq_dict[label] = len(freqs_dict[label].keys())
    return(uniq_dict)

def get_freqs (label_values_dict,subsets_of_interest):
    freqs_dict = dict()

    for column in label_values_dict:
        for l in range(len(label_values_dict[column])):
            curr_label = subsets_of_interest[column][l].name
            mydict = shared_metrics.get_all_frequencies(subsets_of_interest[column][l])
            freqs_dict[curr_label] = mydict
    
    return freqs_dict

def ttr(label_values_dict, subsets_of_interest):  

    freqs_dict = get_freqs(label_values_dict,subsets_of_interest)
    uniq_words_dict = get_unique_words(freqs_dict)
    total_dict = get_label_total(freqs_dict)

    ttr_dict = dict()

    for label in freqs_dict:
        ttr_dict[label] = uniq_words_dict[label] / total_dict[label]

    return ttr_dict
    