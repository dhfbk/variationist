import pandas as pd
import re
from tqdm import tqdm
from transformers import AutoTokenizer

from variationist import utils
from variationist import inspector


def whitespace_tokenization(text_column: pd.Series, 
                            args):
    """Takes as input an array/series of texts and tokenizes it, returns same array/series but tokenized splitting on whitespace.
    
    Parameters
    ----------
    text_column (`pandas.Series`):
        A pandas Series of text that should be tokenized.
    args (`InspectorArgs`):
        The InspectorArgs that were passed to Inspector.
    
    Returns
    -------
    tok_column: `pandas.Series`:
        A pandas Series containing the initial texts but tokenized.
    """     
    
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


def huggingface_tokenization(text_column: pd.Series, 
                             args):
    """Takes as input an series of texts and tokenizes it, returns same series but tokenized using the huggingface tokenizer specified in the InspectorArgs.
    
    Parameters
    ----------
    text_column (`pandas.Series`):
        A pandas Series of text that should be tokenized.
    args (`InspectorArgs`):
        The InspectorArgs that were passed to Inspector.
    
    Returns
    -------
    tok_column: (`pandas.Series`):
        A pandas Series containing the initial texts but tokenized.
    """
    tokenizer_name = args.tokenizer.strip("hf::")
    hf_tokenizer = AutoTokenizer.from_pretrained(tokenizer_name)
    tqdm.pandas()
    nulls = text_column.isnull()
    if nulls.values.any():
        print(f"INFO: we detected one or more null value in the provided text column (indices {list(nulls[nulls].index)}. We will substitute them with an empty string.")
        text_column = text_column.fillna("")
    tok_column = text_column.squeeze().progress_apply(hf_tokenizer.encode, add_special_tokens=False)
    tok_column = tok_column.squeeze().apply(hf_tokenizer.convert_ids_to_tokens)
    return tok_column
