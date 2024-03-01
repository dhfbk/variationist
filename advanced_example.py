from src.inspector import InspectorArgs, Inspector, metrics
from src.data import tokenization
from src.methods import shared_metrics
from itertools import islice

# TODO allow the user to input the dataset and the inspector args from command line
# TODO allow for text and var names to be integers directly


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
            
            print("most frequent", curr_label, list(islice(converted_dict.items(), 10))) #print for debug
            
    return output_freqs

# print(create_most_frequent_dictionary.__name__)

inspector_arguments = InspectorArgs(text_names=["title", "description"],
                                    var_names=["type", "rating"],
                                    metrics=["pmi", "most-frequent", create_most_frequent_dictionary],
                                    stopwords="en",
                                    n_tokens = 1,
                                    
                                    )

dataset = "data/netflix.tsv"

my_inspector = Inspector(dataset, inspector_arguments)

# custom_tokenizer = tokenization.Tokenizer(inspector_arguments)

# Inspector.tokenizer = custom_tokenizer

output_dict = my_inspector.inspect()

# print(output_dict)

my_inspector.save_output_to_json()