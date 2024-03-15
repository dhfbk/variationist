from src.inspector import InspectorArgs, Inspector, metrics
from src.data import tokenization
from src.metrics import shared_metrics
from itertools import islice

# TODO allow the user to input the dataset and the inspector args from command line
# TODO allow for text and var names to be integers directly


def create_most_frequent_dictionary(label_values_dict, subsets_of_interest):
    # TODO change the name of this function: it calculates frequency!
    output_freqs = dict()
    for column in label_values_dict:
        for l in range(len(label_values_dict[column])):
            curr_label = subsets_of_interest[column][l].name
            mydict = shared_metrics.get_all_frequencies(subsets_of_interest[column][l])
            
            sorted_mydict = sorted(mydict.items(), key=lambda x:x[1], reverse=True)
            converted_dict = dict(sorted_mydict)
            output_freqs[curr_label] = converted_dict
            print("most frequent", curr_label, list(islice(converted_dict.items(), 10))) #print for debug
    return output_freqs

# print(create_most_frequent_dictionary.__name__)

inspector_arguments = InspectorArgs(text_names=["text"],
                                    var_names=["hatespeech", "annotator_gender"],
                                    var_bins = [0, 0],
                                    metrics=["freq", "pmi", "ttr",
                                             "n_pmi",
                                             "p_pmi",
                                             "np_relevance",
                                             "npw_relevance",
                                             "maas",
                                             "stats"
                                             ],
                                    stopwords="en",
                                    n_tokens = 1,
                                    tokenizer = "whitespace"
                                    # n_cooc = 3,
                                    # cooc_window_size = 3                                    
                                    )


# inspector_arguments = InspectorArgs(text_names=["0", "1"],
#                                     var_names=["2"],
#                                     # var_bins = [0, 10],
#                                     metrics=["freq", "pmi", "ttr",
#                                              "n_pmi",
#                                              "p_pmi",
#                                              "np_relevance",
#                                              "npw_relevance",
#                                              "maas",
#                                              "stats"
#                                              ],
#                                     # stopwords="en",
#                                     n_tokens = 1,
#                                     # tokenizer = "hf::bert-base-uncased"
#                                     tokenizer = "whitespace"
#                                     # n_cooc = 3,
#                                     # cooc_window_size = 3                                    
#                                     )


dataset = "hf::ucberkeley-dlab/measuring-hate-speech::train"
# dataset = "data/netflix.tsv"


my_inspector = Inspector(dataset, inspector_arguments)

# custom_tokenizer = tokenization.Tokenizer(inspector_arguments)

# Inspector.tokenizer = custom_tokenizer

output_dict = my_inspector.inspect()

# print(output_dict)

my_inspector.save_output_to_json()