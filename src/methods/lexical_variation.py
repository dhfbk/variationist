from src.methods import shared_metrics
import math

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

def safe_divide(numerator, denominator):
		if denominator == 0 or denominator == 0.0:
			result = 0
		else: result = numerator/denominator
		return result

def ttr(label_values_dict, subsets_of_interest):  

    freqs_dict = get_freqs(label_values_dict,subsets_of_interest)
    types_dict = get_unique_words(freqs_dict)
    tokens_dict = get_label_total(freqs_dict)
    
    ttr_dict = dict()

    for label in freqs_dict:
        ttr_dict[label] = safe_divide(types_dict[label],tokens_dict[label])   
    
    print("TTR: ",ttr_dict)
    return ttr_dict
    
def rttr(label_values_dict, subsets_of_interest):  

    freqs_dict = get_freqs(label_values_dict,subsets_of_interest)
    types_dict = get_unique_words(freqs_dict)
    tokens_dict = get_label_total(freqs_dict)
    
    rttr_dict = dict()

    for label in freqs_dict:
        rttr_dict[label] = safe_divide(types_dict[label],math.sqrt(tokens_dict[label]))
    
    print("RTTR: ",rttr_dict)
    return rttr_dict

def maas(label_values_dict, subsets_of_interest):  

    freqs_dict = get_freqs(label_values_dict,subsets_of_interest)
    types_dict = get_unique_words(freqs_dict)
    tokens_dict = get_label_total(freqs_dict)
    
    maas_dict = dict()

    for label in freqs_dict:
        maas_dict[label] = safe_divide((math.log10(tokens_dict[label])-math.log10(types_dict[label])), math.pow(math.log10(tokens_dict[label]),2))
        
    print("MAAS: ",maas_dict)
    return maas_dict


def lttr(label_values_dict, subsets_of_interest):  

    freqs_dict = get_freqs(label_values_dict,subsets_of_interest)
    types_dict = get_unique_words(freqs_dict)
    tokens_dict = get_label_total(freqs_dict)
    
    lttr_dict = dict()

    for label in freqs_dict:
        lttr_dict[label] = safe_divide(math.log10(types_dict[label]), math.log10(tokens_dict[label]))
    
    print("LTTR: ",lttr_dict)
    return lttr_dict

