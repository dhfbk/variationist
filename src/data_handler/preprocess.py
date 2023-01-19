import pandas as pd

from io import StringIO


def read_dataset(input_file, has_header=True):
    """"""

    if input_file is not None:

        is_header = True
        texts = []
        labels = []

        # Convert the input file to a string based IO
        stringio = StringIO(input_file.getvalue().decode("utf-8"))
        
        # Read it line by line and create the dataframe
        for line in stringio:

            # If we are reading the first line, store the header columns
            if is_header == True:
                columns = line.rstrip().split("\t")
                is_header = False

            # Otherwise, store the content of the file
            # @TODO: create the dataframe and generalize to multiple cols and 
            # varying positions of the text and labels (variables)
            else:
                label, text = line.split("\t")
                texts.append(text)
                labels.append(label)

        return texts, labels

    else:
        # @TODO: handle errors in a better way
        return None


def tokenize(dataframe):
    """"""
    return dataframe