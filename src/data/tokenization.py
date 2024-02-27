"""
The Tokenizer class, to handle all the tokenization-related operations of Variationist.
"""
from src.data import preprocess_utils, tokenization_utils
from src import utils


class Tokenizer:
    """A class that handles all the tokenization-related operations of Variationist.
    Parameters
    ----------
    
    """
    
    def __init__(self, inspector_args) -> None:
        self.args = inspector_args
        
        self.column_names_dict = {
            utils.TEXT_COLS_KEY: self.args.text_names,
            utils.LABEL_COLS_KEY: self.args.var_names
        }
        
        if self.args.tokenizer.lower() == "whitespace":
            self.tok_function = tokenization_utils.whitespace_tokenization
        elif self.args.tokenizer.lower() == "spacy":
            self.tok_function = tokenization_utils.spacy_tokenization
        else: # the tokenizer probably is from huggingface. Import and exit if it does not correspond to an actual hf tokenizer.
            self.tok_function = tokenization_utils.huggingface_tokenization
    
    
    def tokenize_column(self, text_column):
        # print(stopwords)
        """"""
        # TODO take an array/series of texts and tokenize it, return same array/series but tokenized
        # TODO do not check here for n_tokens, just tokenize first and THEN add a component that
        # will aggregate the tokens to create bi, tri-grams and so on.
        # TODO we want to add co-occurrences. Should we do that with context windows? e.g. 2 tokens
        # before, 2 tokens after. Could also do co-occurrences of n-grams?
        tokenized_text_column = self.tok_function(text_column, self.args)

        if self.args.stopwords is not False:        
            tokenized_text_column = preprocess_utils.remove_stopwords(tokenized_text_column, self.args.stopwords)
        # print(tokenized_text_column)    
        if self.args.n_tokens > 1:
            tokenized_text_column = preprocess_utils.create_tokenized_ngrams_column(tokenized_text_column, self.args.n_tokens)
        return tokenized_text_column

    def tokenize(self, dataframe):
        tokenized_col_dict = {}
        for text_col in self.column_names_dict[utils.TEXT_COLS_KEY]:
            
            tokenized_col_dict[text_col] = f"tok_{text_col}"
            dataframe[tokenized_col_dict[text_col]] = self.tokenize_column(
                dataframe[[str(text_col)]])
        self.tokenized_col_dict = tokenized_col_dict
        return dataframe
    
            

