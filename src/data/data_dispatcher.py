import pandas as pd
from src.methods import most_frequent,pmi
from src.data import preprocess

from src import utils

# def get_data_type_dict(input_columns, input_processing_type):
#     processing_type_dict = dict()
#     for n in range(len(input_columns)):
#         if input_processing_type[n] not in processing_type_dict:
#             processing_type_dict[input_processing_type[n]] = []
#         processing_type_dict[input_processing_type[n]].append(input_columns[n])
#     return processing_type_dict


def get_text_series_based_on_column(input_dataframe, current_labels, tok_columns_dict):
    subsets_of_interest = []
    # TODO handle labels with multiple values per example
    
    # Create dictionary with names of label columns and label values
    label_values_dict = {}
    for label in current_labels:
        label_values_dict[label] = pd.unique(input_dataframe[label].values.tolist()).tolist()

    for tokenized_text_column in tok_columns_dict:
        for label in label_values_dict:
            for label_value in label_values_dict[label]:
                df_slice_with_current_label = input_dataframe[(input_dataframe[label] == label_value)]
                # print(df_slice_with_current_label)
                # TODO This has to be fixed. It doesn't work with squeeze when there's only one line in the series,
                # but with more lines it probably won't work WITHOUT the squeeze().
                # series_with_current_label = df_slice_with_current_label[tokenized_text_column].squeeze()
                series_with_current_label = df_slice_with_current_label[tokenized_text_column]
                # print(series_with_current_label)
                series_with_current_label = series_with_current_label.rename(label_value)
                subsets_of_interest.append(series_with_current_label)
    return subsets_of_interest


def get_subset_dict(input_dataframe, col_names_dict, tok_columns_dict, label_values_dict):
    """create a dictionary containing all the subsets of the datasets we will be analyzing."""
    # TODO handle nan values for a specific label.

    current_labels = col_names_dict[utils.LABEL_COLS_KEY]
    subsets_of_interest = {}
    # loop through all columns containing text
    for text_column in tok_columns_dict:
        tokenized_text_column = tok_columns_dict[text_column]
        # Loop through all columns containing labels
        for label in current_labels:
            current_label_subset = []
            for label_value in label_values_dict[label]:

                df_slice_with_current_label = input_dataframe[(input_dataframe[label] == label_value)]

                series_with_current_label = df_slice_with_current_label[tokenized_text_column]
                if len(series_with_current_label) > 1:
                    series_with_current_label = series_with_current_label.squeeze()

                series_with_current_label = series_with_current_label.rename(label_value)
                current_label_subset.append(series_with_current_label)
            subsets_of_interest[label] = current_label_subset
    
    return subsets_of_interest



def process_dataset(input_dataframe, col_names_dict, metrics, n_tokens, stopwords, lowercase):
    
    """function that returns a list of pandas series, one for each label value
    for each label the user selected as relevant, containing the corresponding 
    tokenized texts"""
    # TODO there currently is an error when there are multiple text columns

    print(input_dataframe)
    tokenized_dataframe, tok_columns_dict = preprocess.tokenize_add_tok_column(input_dataframe,
                                                                               col_names_dict,
                                                                               n_tokens,
                                                                               stopwords,
                                                                               lowercase)


    label_values_dict = preprocess.get_label_values(input_dataframe, col_names_dict)
    subsets_of_interest = get_subset_dict(tokenized_dataframe,
                                          col_names_dict,
                                          tok_columns_dict,
                                          label_values_dict)

    # print("subsets of interest")
    
    # print(list(subsets_of_interest.keys()))
    # print(subsets_of_interest["label"])
    # print(subsets_of_interest)
    # for column in label_values_dict:
        
    #     for l in label_values_dict[column]:
    #         print(column,l)  
    #         print(subsets_of_interest[column][0])
    # print(metrics)
    # output_metrics = {}
    results_dict = dict()
    
    if 'most-frequent' in metrics:
        most_frequent_dict = most_frequent.create_most_frequent_dictionary(label_values_dict, subsets_of_interest)
        results_dict['most-frequent'] = most_frequent_dict
        
    if 'pmi' in metrics:
        pmi_dict = pmi.create_pmi_dictionary(label_values_dict, subsets_of_interest)
        results_dict['pmi'] = pmi_dict
        
        # print(most_frequent_dict)
    #     output_metrics['most_frequent'] = {}
    #     if len(col_names_dict['text']) > 0 and len(col_names_dict['labels']) > 0:
    #         for label in current_labels:
    #             curr_label_most_frequent_dict = most_frequent.create_most_frequent_dictionary(subsets_of_interest[label])
    #             print(curr_label_most_frequent_dict)
    #             output_metrics['most_frequent'][label] = curr_label_most_frequent_dict
    #     else:
    #         print('Text or labels missing')
        
    return subsets_of_interest,results_dict