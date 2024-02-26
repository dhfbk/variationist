"""
The Inspector class, to handle all the operations of Variationist.
"""
import os
from dataclasses import dataclass, asdict
from datasets import Dataset
import pandas as pd
from src import utils
from typing import Callable, List, Optional, Tuple, Union, Dict
from src.data import data_dispatcher
import json

@dataclass
class InspectorArgs:
    """A dataclass to store all of the arguments that relate to the analysis.
    
    Parameters
    ----------
        text_names (`List[str]`):
            The list of names of text columns in the given dataset to use for the analysis. 
        var_names (`List[str]`):
            The list of variable names to use for the analysis. Each string in var_names should correspond to a dataset column.
        var_types (`List[str]`):
            The list of variable types corresponding to the variables in `var_names`. Should match the length of `var_names`. Available choices are `nominal` (default), `ordinal`, and `coordinates`.
        var_semantics (`List[str]`):
            The list of variable semantics corresponding to the variables in `var_names`. Should match the length of `var_names`. Available choices are `general`(default), `temporal`, and `spatial`.
        var_subsets (`Tuple[List]`):
            Subsets to use for the analysis. To be used when the combinations of all variables are too many and we want to focus on analyzing a subset against another subset, specifying values for multiple variables. Should follow the format `(['var_a_value_1', 'var_b_value_1'], ['var_a_value_2', 'var_b_value_2'])`.
        tokenizer ([`PreTrainedTokenizerBase`], *optional*, defaults to `whitespace`): #TODO
            The tokenizer used to preprocess the data. Will default to whitespace tokenization if not specified.
        language (`str`):
            The language of the text in the dataset. Used for proper tokenization and stopword removal.
        metrics (`Callable[[EvalPrediction], Dict]`, *optional*):
            The list of metrics that should be calculated.
        n_tokens (`Int`):
            The number of tokens that should be considered for the analysis. 1 corresponds to unigrams, 2 corresponds to bigrams, and so on.
        stopwords (`Bool`):
            Whether to remove stopwords from texts before tokenization or not. Will default to False.
        lowercase (`Bool`):
            Whether to lowercase all the texts before tokenization or not. Will default to False.
    """
    
    tokenizer: Optional[str] = 'whitespace'
    language: Optional[str] = None
    metrics: Optional[List] = None
    text_names: Optional[List] = None # explicit column name(s)
    var_names: Optional[List] = None # explicit variable name(s)
    var_types: Optional[List] = 'nominal' # nominal (default), ordinal, coordinates
    var_semantics: Optional[List] = 'general' # default=General, temporal, spatial
    var_subsets: Optional[List] = None
    n_tokens: Optional[int] = 1 # maximum value for this should be 5, otherwise the computation will explode
    stopwords: Optional[bool] = False # TODO currently we only support stopwords = en,it. Add support for False, spacy, hf
    lowercase: Optional[bool] = False
    
    def to_dict(self):
        """Returns the InspectorArgs values inside a dictionary."""
        self_as_dict = asdict(self)
        return self_as_dict
    



class Inspector:
    """
    # TODO Description of the Inspector class.

    Parameters
    ----------
        dataset ([`pandas.DataFrame` or `datasets.Dataset` or `str`]): #TODO
            The dataset to be used for our analysis.
        args (`InspectorArguments`)
        
    """

    def __init__(
        self,
        dataset: Union[Dataset, pd.DataFrame, str] = None,
        args: InspectorArgs = InspectorArgs(),
        ):
        
        self.dataset = dataset
        self.args = args
       
        # Dictionary for the metadata to be printed in the json output
        metadata_dict = self.args.to_dict()        
        metadata_dict["dataset"] = self.dataset     
        self.metadata_dict = metadata_dict
        
        
        # Check if column strings are names or indices (for both texts and labels)
        text_names_type = utils.check_column_type(args.text_names)
        label_names_type = utils.check_column_type(args.var_names)
        
        # Since the input file/dataset is the same, we require texts and labels columns to be of the same type
        if text_names_type != label_names_type:
            raise ValueError(f"ERROR! text_cols are {text_names_type} while label_cols are {label_names_type}. "
                            "Please provide all column identifiers as names (as in the header line) or indices.")
        cols_type = text_names_type
        print(f"INFO: all column identifiers are treated as column {cols_type}.")

        # TODO
        # this should ideally just become a data util function that we call here on "dataset"
        # then we just assume that that function will return us a dataframe we can work with.
        # dataset = data_utils.turn_into_dataframe(dataset)
        # TODO also add the possibility of dataset already being a huggingface dataset or a pandas dataframe
        if type(dataset) is str:
            # If the input filepath is local, check if the file exists. If not, exit
            if dataset.startswith("hf::"):
                # open dataset with huggingface
                raise NotImplementedError("Variationist does not support huggingface datasets yet")
            elif os.path.isfile(dataset):
                # open with pandas (old function)
                # Read the input file/dataset and store its content in a pandas dataframe
                self.dataframe = utils.convert_file_to_dataframe(dataset, cols_type=cols_type)
            else:
                raise ValueError(f"ERROR! The file '{dataset}' does not exist. Exit.")
         # -------- function should end here

        # Check if the specified columns are actually in the dataframe
        self.dataframe_cols = [col_name for col_name in self.dataframe.columns]
        for col in args.text_names+args.var_names:
            if col not in self.dataframe_cols:
                raise ValueError(f"ERROR: the '{col}' column is not present in the dataframe.")

        # Create a dictionary containing the specified column strings (values) for texts and labels (keys)
        self.column_names_dict = {
            utils.TEXT_COLS_KEY: args.text_names,
            utils.LABEL_COLS_KEY: args.var_names
        }


    def compute(self):
        """Function that runs the actual computation"""
        series_dict,results_dict = data_dispatcher.process_dataset(self.dataframe,
                                                                   self.column_names_dict,
                                                                   metrics=self.args.metrics,
                                                                   n_tokens=self.args.n_tokens,
                                                                   stopwords=self.args.stopwords,
                                                                   lowercase=self.args.lowercase,
                                                                   tokenization_type=self.args.tokenizer)
        # TODO handle series_dict
        self.results_dict = results_dict
    
    def create_output_dict(self):
        """Function to create the output dictionary, containing both metadata and calculated metrics. """
        output_dict = dict()
        output_dict["metadata"] = self.metadata_dict
        output_dict["metrics"] = self.results_dict

        self.output_dict = output_dict
        
    def save_output_to_json(self,
                            output_path = "output.json"
                            ):
        output_file = open(output_path, "w")
        json.dump(self.output_dict, output_file, indent=4)
        output_file.close()
        
    def inspect(self):
        self.compute()
        self.create_output_dict()
        return self.output_dict