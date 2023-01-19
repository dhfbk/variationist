import pandas as pd

from io import StringIO


def read_dataset(uploaded_file):
    """"""

    # Convert input file to a string based IO
    stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))

    texts = []
    labels = []
    
    for line in stringio:
        label, text = line.split("\t")
        texts.append(text)
        labels.append(label)

    return texts, labels
    #data_dict = {"texts": texts, "labels": labels}
    #df = pd.from_dict(data_dict)

    #return dataframe