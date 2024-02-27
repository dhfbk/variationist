import re
from src import utils

def whitespace_tokenization(text_column, args):
    # Takes as input an array/series of texts and tokenize it, return same array/series but tokenized splitting on whitespaces
    # Remove punctuation and any not alphanumeric charachter
    # ONLY WORKS ON LATIN ALPHABET
    if args.lowercase:
        tok_column = text_column.squeeze().apply(lambda x: str(x).lower())
    else:
        tok_column = text_column.squeeze().astype(str)

    tok_column = tok_column.apply(lambda x: re.sub(r'[^a-zA-Z0-9àèìòùÀÈÌÒÙáéíóúýÁÉÍÓÚÝâêîôûÂÊÎÔÛãñõÃÑÕäëïöüÿÄËÏÖÜŸçÇßØøÅåÆæœ]', ' ', x))
    tok_column = tok_column.apply(lambda x: re.sub(r' +', ' ', x))
    tok_column = tok_column.apply(lambda x: x.split(" "))
    
    # tok_column = tok_column.squeeze().apply(lambda x: pd.Series(x.split(" ")))
    return tok_column


def huggingface_tokenization(text_column, args):
    """TODO"""
    raise NotImplementedError("We don't support huggingface tokenization yet.")
    return


def spacy_tokenization(text_column, args):
    """TODO"""
    raise NotImplementedError("We don't support spacy tokenization yet.")
    return
