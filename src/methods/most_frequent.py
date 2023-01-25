import pandas as pd

def create_most_frequent_dictionary(text_array):
    output_freqs = dict()
    for text_series in text_array:
        curr_label = text_series.name
        # print(curr_label)
        output_freqs[curr_label] = {}
        for tokenized_text in text_series:
            # print(tokenized_text)
            for token in tokenized_text:
                # print(token)
                if token not in output_freqs[curr_label]:
                    output_freqs[curr_label][token] = 1
                else:
                    output_freqs[curr_label][token] += 1

    return output_freqs