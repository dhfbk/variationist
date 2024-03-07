from statistics import stdev, mean
import math



def safe_divide(numerator, denominator):
        if denominator == 0 or denominator == 0.0:
            result = 0
        else:
            result = numerator/denominator
        return result

def ttr(label_values_dict, subsets_of_interest):  
    values_dict = dict()
    for column in label_values_dict:
        for l in range(len(label_values_dict[column])):
            values_list = []
            curr_label = subsets_of_interest[column][l].name
            for sentence in subsets_of_interest[column][l]:
                tok = len(sentence)
                typ = len(list(dict.fromkeys(sentence)))
                values_list.append(safe_divide(typ,tok))
            values_dict[curr_label] = dict()
            values_dict[curr_label]["mean"] = mean(values_list)
            values_dict[curr_label]["stdev"] = stdev(values_list)
    print("TTR: ",values_dict)
    return values_dict
    
def rttr(label_values_dict, subsets_of_interest):  
    values_dict = dict()
    for column in label_values_dict:
        for l in range(len(label_values_dict[column])):
            values_list = []
            curr_label = subsets_of_interest[column][l].name
            for sentence in subsets_of_interest[column][l]:
                tok = len(sentence)
                typ = len(list(dict.fromkeys(sentence)))
                values_list.append(safe_divide(typ,math.sqrt(tok)))
            values_dict[curr_label] = dict()
            values_dict[curr_label]["mean"] = mean(values_list)
            values_dict[curr_label]["stdev"] = stdev(values_list)
    print("RTTR: ",values_dict)
    return values_dict

def maas(label_values_dict, subsets_of_interest):  
    values_dict = dict()
    for column in label_values_dict:
        for l in range(len(label_values_dict[column])):
            values_list = []
            curr_label = subsets_of_interest[column][l].name
            for sentence in subsets_of_interest[column][l]:
                tok = len(sentence)
                typ = len(list(dict.fromkeys(sentence)))
                values_list.append(safe_divide((math.log10(tok)-math.log10(typ)), math.pow(math.log10(tok),2)))
            values_dict[curr_label] = dict()
            values_dict[curr_label]["mean"] = mean(values_list)
            values_dict[curr_label]["stdev"] = stdev(values_list)
    print("MAAS: ",values_dict)
    return values_dict

def lttr(label_values_dict, subsets_of_interest):  
    values_dict = dict()
    for column in label_values_dict:
        for l in range(len(label_values_dict[column])):
            values_list = []
            curr_label = subsets_of_interest[column][l].name
            for sentence in subsets_of_interest[column][l]:
                tok = len(sentence)
                typ = len(list(dict.fromkeys(sentence)))
                values_list.append(safe_divide(math.log10(typ), math.log10(tok)))
            values_dict[curr_label] = dict()
            values_dict[curr_label]["mean"] = mean(values_list)
            values_dict[curr_label]["stdev"] = stdev(values_list)
    print("LTTR: ",values_dict)
    return values_dict

