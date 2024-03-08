from statistics import stdev, mean

def number_of_texts(label_values_dict, subsets_of_interest):  
    values_dict = dict()
    for column in label_values_dict:
        for l in range(len(label_values_dict[column])):
            curr_label = subsets_of_interest[column][l].name
            values_dict[curr_label] = len(subsets_of_interest[column][l])
    return values_dict

def average_text_lengt(label_values_dict, subsets_of_interest):  
    values_dict = dict()
    for column in label_values_dict:
        for l in range(len(label_values_dict[column])):
            values_list = []
            curr_label = subsets_of_interest[column][l].name
            for text in subsets_of_interest[column][l]:
                values_list.append(len(text))
            values_dict[curr_label] = dict()
            values_dict[curr_label]["mean"] = mean(values_list)
            values_dict[curr_label]["stdev"] = stdev(values_list)
    return values_dict

def compute_basic_stats(label_values_dict, subsets_of_interest, args):  
    stats_dict = dict()
    stats_dict["number_of_texts"] = number_of_texts(label_values_dict, subsets_of_interest)
    stats_dict["average_text_length"] = average_text_lengt(label_values_dict, subsets_of_interest)
    print(stats_dict)
    return stats_dict