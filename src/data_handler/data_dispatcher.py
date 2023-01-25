import pandas as pd
from io import StringIO

from src.methods import most_frequent
from src.data_handler import preprocess

def get_data_type_dict(input_columns, input_processing_type):
    processing_type_dict = dict()
    for n in range(len(input_columns)):
        if input_processing_type[n] not in processing_type_dict:
            processing_type_dict[input_processing_type[n]] = []
        processing_type_dict[input_processing_type[n]].append(input_columns[n])
    return processing_type_dict


def get_text_series_based_on_column(input_dataframe, current_labels, tokenized_col_names):
    subsets_of_interest = []

    # Create dictionary with names of label columns and label values
    label_values_dict = {}
    for label in current_labels:
        label_values_dict[label] = pd.unique(input_dataframe[label].values.tolist()).tolist()

    for tokenized_text_column in tokenized_col_names:
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



def process_dataset(input_dataframe, input_processing_type, has_header=True, metrics=[]):
    """"""
    # TODO this function should be split into smaller functions
    # TODO there currently is an error when there are multiple text columns
    output_metrics = dict()
    input_columns = input_dataframe.columns.to_list()

    processing_type_dict = get_data_type_dict(input_columns, input_processing_type)

    # Tokenize and create new columns with tokenized text, name them "tok_{original_column}"
    tokenized_col_names = {}
    for text_column in processing_type_dict["text"]:
        tokenized_col_names[text_column] = f"tok_{text_column}"
        input_dataframe[tokenized_col_names[text_column]] = preprocess.tokenize(input_dataframe[text_column])


    current_labels = processing_type_dict["labels"]


    # Create dictionary with names of label columns and label values
    label_values_dict = {}
    for label in current_labels:
        label_values_dict[label] = pd.unique(input_dataframe[label].values.tolist()).tolist()

    print(label_values_dict)

    subsets_of_interest = {}
    # loop through all columns containing text
    for text_column in tokenized_col_names:
        tokenized_text_column = tokenized_col_names[text_column]
        
        # Loop through all columns containing labels
        for label in current_labels:
            current_label_subset = []
            for label_value in label_values_dict[label]:
                df_slice_with_current_label = input_dataframe[(input_dataframe[label] == label_value)]
                # print(df_slice_with_current_label)
                # TODO This has to be fixed. It doesn't work with squeeze when there's only one line in the series,
                # but with more lines it probably won't work WITHOUT the squeeze().
                # series_with_current_label = df_slice_with_current_label[tokenized_text_column].squeeze()
                series_with_current_label = df_slice_with_current_label[tokenized_text_column]
                # print(series_with_current_label)
                series_with_current_label = series_with_current_label.rename(label_value)
                current_label_subset.append(series_with_current_label)
            subsets_of_interest[label] = current_label_subset
            # print(subsets_of_interest)

    print("subsets of interest")
    print(subsets_of_interest)
    output_metrics = {}
    if 'most_frequent' in metrics:
        output_metrics['most_frequent'] = {}
        if len(processing_type_dict['text']) > 0 and len(processing_type_dict['labels']) > 0:
            for label in current_labels:
                curr_label_most_frequent_dict = most_frequent.create_most_frequent_dictionary(subsets_of_interest[label])
                print(curr_label_most_frequent_dict)
                output_metrics['most_frequent'][label] = curr_label_most_frequent_dict
        else:
            print('Text or labels missing')
    return output_metrics
    # stringio = StringIO(input_file.getvalue().decode("utf-8"))
    # df = pd.read_csv(stringio,sep='\t', header=0, index_col=False)
    # return df
