import pandas as pd

def compute_most_frequent(dataframe, label_columns, text_columns):
    
    output_freqs = dict()

    for column in label_columns:
        labels_list = list(dict.fromkeys(dataframe[column].tolist()))
        for label in labels_list:
            if label not in output_freqs:
                output_freqs[label] = dict()
            selection = dataframe.loc[dataframe[column] == label]
            for text_column in text_columns:
                for text in selection[text_column].values:
                    for token in text.split(" "):
                        if token not in output_freqs[label]:
                            output_freqs[label][token] = 1
                        else:
                            output_freqs[label][token] += 1

            

    return output_freqs