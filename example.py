import os
from src.inspector import InspectorArgs, Inspector

# TODO allow the user to input the dataset and the inspector args from command line
# TODO allow for text and var names to be integers directly



inspector_arguments = InspectorArgs(text_names=["1"],
                                    var_names=["0"],
                                    metrics=[
                                        "pmi",
                                        "pmi-normalized",
                                        "pmi-positive",
                                        "pmi-positive-normalized", 
                                        "most-frequent",
                                        "ttr",
                                        "rttr",
                                        "maas",
                                        "lttr",
                                        ],
                                    stopwords="en",
                                    n_tokens = 1,
                                    n_cooc = 1,
                                    )

dataset = "data/netflix-toy.tsv"

my_inspector = Inspector(dataset, inspector_arguments)

output_dict = my_inspector.inspect()

# print(output_dict)

my_inspector.save_output_to_json(output_path=os.path.join("data", "output.json"))