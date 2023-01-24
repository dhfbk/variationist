import pandas as pd
from io import StringIO

from src.methods import most_frequent

def check_data_type(input_columns, input_processing_type):
    processing_type = dict()
    for n in range(len(input_columns)):
        if input_processing_type[n] not in processing_type:
            processing_type[input_processing_type[n]] = []
        processing_type[input_processing_type[n]].append(input_columns[n])
        
    return processing_type    

def process_dataset(input_dataframe, input_columns, input_processing_type, has_header=True, metrics=[]):

    output_metrics = dict()

    processing_type = check_data_type(input_columns, input_processing_type)

    if 'most_frequent' in metrics:
        if len(processing_type['text']) > 0 and len(processing_type['labels']) > 0:
            # most_frequent_results = most_frequent.compute_most_frequent([lista_testi_1, lista_testi_2]
            most_frequent_results = most_frequent.compute_most_frequent(
                dataframe = input_dataframe, 
                label_columns = processing_type['labels'], 
                text_columns = processing_type['text']
                )
            output_metrics['most_frequent'] = most_frequent_results
        else:
            print('Text or labels missing')

    return output_metrics
    # stringio = StringIO(input_file.getvalue().decode("utf-8"))
    # df = pd.read_csv(stringio,sep='\t', header=0, index_col=False)
    # return df
