"""
The Tokenizer class, to handle all the tokenization-related operations of Variationist.
"""
import pandas as pd
import sys

from variationist.data import preprocess_utils, tokenization_utils
from variationist import utils


class Tokenizer:
    """A class that handles all the tokenization-related operations of Variationist.
    
    Parameters
    ----------
    inspector_args (`InspectorArgs`): 
        The arguments that were passed to the Inspector.
    """
    
    def __init__(self, 
                 inspector_args) -> None:
        self.args = inspector_args
        
        self.column_names_dict = {
            utils.TEXT_COLS_KEY: self.args.text_names,
            utils.LABEL_COLS_KEY: self.args.var_names
        }
        if callable(self.args.tokenizer):
            self.tok_function = self.args.tokenizer
        elif self.args.tokenizer.lower() == "whitespace":
            self.tok_function = tokenization_utils.whitespace_tokenization
        elif self.args.tokenizer.startswith("hf::"):
            self.tok_function = tokenization_utils.huggingface_tokenization
        else:
            sys.exit(f"The selected tokenizer ({self.args.tokenizer}) does not match any of the available options. If you intend to use a pretrained tokenizer from HuggingFace, please use the format 'hf::TOKENIZER_NAME'. Other available options are 'whitespace', and a callable function.")
        # TODO add the possibility to add a custom tokenizer as a function in inspectorargs.
    
    
    def tokenize_column(self, 
                        text_column: pd.Series):
        """A function that tokenizes a text column using the selected tokenization function. It will also create n-grams and co-occurrences if requested by the user. It will then return the same text column, but tokenized/grouped according to the desired result.
        
        Parameters
        ----------
        text_column (`pandas.Series`):
            The series (text column) that should be tokenized.
            
        Returns
        -------
        text_column (`pandas.Series`):
            The same series as input, but tokenized/regrouped as requested.
             
        """
        tokenized_text_column = self.tok_function(text_column, self.args)

        if (self.args.stopwords == True):
            if (self.args.language != None) or (self.args.custom_stopwords != None):
                tokenized_text_column = preprocess_utils.remove_stopwords(
                    tokenized_text_column, self.args.language, self.args.custom_stopwords)
            else:
                print("WARNING: Stopword removal has been selected, but the \"language\"",
                    "parameter has not been defined. Skipping stopword removal.")
        else:
            if (self.args.custom_stopwords != None):
                tokenized_text_column = preprocess_utils.remove_stopwords(
                    tokenized_text_column, self.args.language, self.args.custom_stopwords)

        # print(tokenized_text_column)    
        if self.args.n_tokens > 1:
            print("INFO: Creating n-grams...")
            tokenized_text_column = preprocess_utils.create_tokenized_ngrams_column(tokenized_text_column, self.args.n_tokens)
        
        if self.args.n_cooc > 1 and self.args.n_tokens <= 1:
            print("INFO: Creating co-occurrences...")
            tokenized_text_column = preprocess_utils.create_tokenized_cooccurrences_column(tokenized_text_column, self.args.n_cooc, self.args.cooc_window_size, self.args.unique_cooc)
        return tokenized_text_column
    

    def tokenize(self, dataframe):
        """A wrapper function to tokenize each text column and add it to the original input dataframe as 'tok_ORIGINAL_TEXT_COL_NAME'. Returns the dataframe with the added tokenized columns.
        
        Parameters
        ----------
        dataframe (`pandas.DataFrame`):
            The dataframe that contains the data for the analysis
            
        Returns
        -------
        dataframe (`pandas.DataFrame`):
            The same dataframe as input, but with added columns containing the tokenized texts.
        """
        tokenized_col_dict = {}
        for text_col in self.column_names_dict[utils.TEXT_COLS_KEY]:
            print(f"INFO: Tokenizing the {text_col} column...")
            tokenized_col_dict[text_col] = f"tok_{text_col}"
            dataframe[tokenized_col_dict[text_col]] = self.tokenize_column(
                dataframe[[str(text_col)]])
        self.tokenized_col_dict = tokenized_col_dict
        return dataframe
    
       