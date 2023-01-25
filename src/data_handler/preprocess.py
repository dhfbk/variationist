import pandas as pd

from io import StringIO


def read_dataset(input_file, has_header=True):
    # Convert input file to a string based IO
    stringio = StringIO(input_file.getvalue().decode("utf-8"))
    df = pd.read_csv(stringio,sep='\t', header=0, index_col=False)
    return df
    """"""

    # if input_file is not None:

    #     is_header = True
    #     texts = []
    #     labels = []

    #     # Convert the input file to a string based IO
    #     stringio = StringIO(input_file.getvalue().decode("utf-8"))
        
    #     # Read it line by line and create the dataframe
    #     for line in stringio:

    #         # If we are reading the first line, store the header columns
    #         if is_header == True:
    #             columns = line.rstrip().split("\t")
    #             is_header = False

    #         # Otherwise, store the content of the file
    #         # @TODO: create the dataframe and generalize to multiple cols and 
    #         # varying positions of the text and labels (variables)
    #         else:
    #             label, text = line.split("\t")
    #             texts.append(text)
    #             labels.append(label)

    #     return texts, labels

    # else:
    #     # @TODO: handle errors in a better way
    # return None

def whitespace_tokenization(text_column):
    tok_column = text_column.squeeze().apply(lambda x: x.split(" "))
    return tok_column

def tokenize(text_column, tokenization_type="whitespace"):
    """"""
    #TODO take an array/series of texts and tokenize it, return same array/series but tokenized
    if tokenization_type == "whitespace":
        tokenized_text_column = whitespace_tokenization(text_column)
    else:
        raise Exception("Only whitespace tokenization is currently supported")
    return tokenized_text_column