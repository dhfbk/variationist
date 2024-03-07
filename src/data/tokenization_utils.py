import re
from src import utils
from tqdm import tqdm
from transformers import AutoTokenizer
from src import utils

def whitespace_tokenization(text_column, args):
    """Takes as input an array/series of texts and tokenizes it, returns same array/series 
    but tokenized splitting on whitespace."""
    # Remove punctuation and any not alphanumeric charachter      
    
    tqdm.pandas()
    if args.lowercase:
        tok_column = text_column.squeeze().apply(lambda x: str(x).lower())
    else:
        tok_column = text_column.squeeze().astype(str)

    tok_column = tok_column.progress_apply(lambda x: utils.replace_symbols(x))
    tok_column = tok_column.apply(lambda x: re.sub(r'\s+', ' ', x))
    tok_column = tok_column.apply(lambda x: x.strip().split(" "))
    
    # tok_column = tok_column.squeeze().apply(lambda x: pd.Series(x.split(" ")))
    return tok_column


def huggingface_tokenization(text_column, args):
    """Load a HuggingFace AutoTokenizer from the string given by the user."""
    # print(text_column)
    # text_column = text_column.dropna()
    tokenizer_name = args.tokenizer.strip("hf::")
    hf_tokenizer = AutoTokenizer.from_pretrained(tokenizer_name)
    tqdm.pandas()
    tok_column = text_column.squeeze().progress_apply(hf_tokenizer.encode, add_special_tokens=False)
    tok_column = tok_column.squeeze().apply(hf_tokenizer.convert_ids_to_tokens)
    return tok_column


def spacy_tokenization(text_column, args):
    """TODO"""
    raise NotImplementedError("We don't support Spacy tokenization yet.")
    return
