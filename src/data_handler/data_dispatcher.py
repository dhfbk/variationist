import pandas as pd
from io import StringIO

from src.methods import most_frequent
from src.data_handler import preprocess

def check_data_type(input_columns, input_processing_type):
    processing_type = dict()
    for n in range(len(input_columns)):
        if input_processing_type[n] not in processing_type:
            processing_type[input_processing_type[n]] = []
        processing_type[input_processing_type[n]].append(input_columns[n])
    return processing_type    

def process_dataset(input_dataframe, input_processing_type, has_header=True, metrics=[]):
    """"""
    output_metrics = dict()
    input_columns = input_dataframe.columns.to_list()

    processing_type = check_data_type(input_columns, input_processing_type)

    tokenized_col_names = {}
    for text_column in processing_type["text"]:
        tokenized_col_names[text_column] = f"tok_{text_column}"
        input_dataframe[tokenized_col_names[text_column]] = preprocess.tokenize(input_dataframe[text_column])
    
    print(input_dataframe)

    # per ogni label creo una serie pandas con i testi di quella label, TODO se le label sono 2?
    subsets_of_interest = []
    current_labels = processing_type["labels"]
    print(current_labels)

    label_values_dict = {}
    for label in current_labels:
        label_values_dict[label] = pd.unique(input_dataframe[label].values.tolist()).tolist()
    print(label_values_dict)

    for tokenized_text_column in tokenized_col_names:
        for label in label_values_dict:
            for label_value in label_values_dict[label]:
                df_slice_with_current_label = input_dataframe[(input_dataframe[label] == label_value)]
                print(df_slice_with_current_label)
                # TODO This has to be fixed. It doesn't work with squeeze when there's only one line in the series,
                # but with more lines it probably won't work WITHOUT the squeeze()
                # series_with_current_label = df_slice_with_current_label[tokenized_text_column].squeeze()
                series_with_current_label = df_slice_with_current_label[tokenized_text_column]
                print(series_with_current_label)
                series_with_current_label = series_with_current_label.rename(label_value)
                subsets_of_interest.append(series_with_current_label)

    print(subsets_of_interest)

    if 'most_frequent' in metrics:
        if len(processing_type['text']) > 0 and len(processing_type['labels']) > 0:
            most_frequent_dict = most_frequent.create_most_frequent_dictionary(subsets_of_interest)
            output_metrics['most_frequent'] = most_frequent_dict
        else:
            print('Text or labels missing')
    return output_metrics
    # stringio = StringIO(input_file.getvalue().decode("utf-8"))
    # df = pd.read_csv(stringio,sep='\t', header=0, index_col=False)
    # return df
