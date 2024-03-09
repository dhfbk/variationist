"""
The Inspector class, to handle all the operations of Variationist.
"""
import os
from dataclasses import dataclass, asdict, field
from datasets import Dataset
import pandas as pd
from src import utils
from typing import Callable, List, Optional, Tuple, Union, Dict
import json
from src.data import preprocess_utils
from src.data.tokenization import Tokenizer
from src.methods import pmi, most_frequent, metrics

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
            The list of variable types corresponding to the variables in `var_names`. Should match the length of `var_names`. Available choices are `nominal` (default), `ordinal`, `quantitative`, and `coordinates`.
        var_semantics (`List[str]`):
            The list of variable semantics corresponding to the variables in `var_names`. Should match the length of `var_names`. Available choices are `general` (default), `temporal`, and `spatial`.
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
        n_cooc (`Int`):
            The number of tokens used for calculating non-consecutive co-occurrences. For example, n=2 means we consider as the base units for our analysis any pair of tokens that co-occur in the same sentence. n=3 means we consider triplets of tokens, etc. Defaults to n=1, meaning no co-occurrences are taken into consideration, and we only consider n-grams.
        unique_cooc (`Bool`):
            Whether to consider unique co-occurrences or not. Default to False (keep duplicate tokens). This does not affect the co-occurrences window size by design (the window size considers the original number of tokens and therefore the original allowed maximum distance between tokens).
        cooc_window_size (`Int`):
            Size of the context window for co-occurrences. For instance, a `cooc_window_size` of 3 means we use a context window of 3 to calculate co-occurrences, meaning that any token that is within 3 tokens before or after a given token is added as a co-occurrence.
        freq_cutoff (`Int`):
            The token frequency, expressed as an integer, below which we do not consider the token in the analysis of pmi-based metrics.
        stopwords (`Bool`):
            Whether to remove stopwords from texts before tokenization or not. Will default to False.
        lowercase (`Bool`):
            Whether to lowercase all the texts before tokenization or not. Will default to False.
    """
    
    tokenizer: Optional[Union[str, Callable]] = 'whitespace'
    language: Optional[str] = None
    metrics: Optional[List] = None
    text_names: Optional[List] = None # explicit column name(s)
    var_names: Optional[List] = None # explicit variable name(s)
    var_types: Optional[List] = None # nominal (default), ordinal, quantitative, coordinates
    var_semantics: Optional[List] = None # default=General, temporal, spatial
    var_subsets: Optional[List] = None
    n_tokens: Optional[int] = 1 # maximum value for this should be 5, otherwise the computation will explode
    n_cooc: Optional[int] = 1
    unique_cooc: Optional[bool] = False
    cooc_window_size: Optional[int] = 0
    freq_cutoff: Optional[int] = 3
    stopwords: Optional[bool] = False # TODO currently we only support stopwords = en,it. Add support for False, spacy, hf
    lowercase: Optional[bool] = False
    
    def to_dict(self):
        """Returns the InspectorArgs values inside a dictionary."""
        self_as_dict = asdict(self)
        # convert any python objects into strings inside the dict
        # so that it can later be converted to json
        for i in range(len(self.metrics)):
            if type(self.metrics[i]) is not str:
                self_as_dict["metrics"][i] = self.metrics[i].__name__
        if type(self.tokenizer) is not str:
            self_as_dict["tokenizer"] = self.tokenizer.__name__
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

        # Set defaults for variable types and semantics in case they are not defined
        if self.args.var_types == None:
            default_type = "nominal"
            self.args.var_types = [default_type] * len(self.args.var_names)
            print(f"INFO: No values have been set for var_types. Defaults to {default_type}.")
        if self.args.var_semantics == None:
            default_semantics = "general"
            self.args.var_semantics = [default_semantics] * len(self.args.var_names)
            print(f"INFO: No values have been set for var_semantics. Defaults to {default_semantics}.")

        # Dictionary for the metadata to be printed in the json output
        metadata_dict = self.args.to_dict()
        print(metadata_dict)
        metadata_dict["dataset"] = self.dataset     
        self.metadata_dict = metadata_dict
        
        # Check if variable definitions match in length
        if any(len(args.var_names) != len(l) for l in [args.var_types, args.var_semantics]):
            raise ValueError(f"ERROR! All variables in {args.var_names} should have an associated "
                            f"variable type and semantics, but now only var_types: {args.var_types} "
                            f"and var_semantics: {args.var_semantics} are provided. Please provide "
                            f"an ordered list of types and semantics that match variable names.")
        
        # Check if column strings are names or indices (for both texts and labels)
        text_names_type = utils.check_column_type(args.text_names)
        label_names_type = utils.check_column_type(args.var_names)
    
        
        # Since the input file/dataset is the same, we require texts and labels columns to be of the same type
        if text_names_type != label_names_type:
            raise ValueError(f"ERROR! text_cols are {text_names_type} while label_cols are {label_names_type}. "
                            "Please provide all column identifiers as names (as in the header line) or indices.")
        self.cols_type = text_names_type
        print(f"INFO: all column identifiers are treated as column {self.cols_type}.")
        
        self.dataframe = utils.convert_file_to_dataframe(self.dataset, cols_type=self.cols_type)
        
        # Create a dictionary containing the specified column strings (values) for texts and labels (keys)
        self.col_names_dict = {
            utils.TEXT_COLS_KEY: args.text_names,
            utils.LABEL_COLS_KEY: args.var_names
        }

        # Instantiate the tokenizer
        self.tokenizer = Tokenizer(self.args)
        
        self.check_columns()


    def check_columns(self):
        # Check if the specified columns are actually in the dataframe
        self.dataframe_cols = [col_name for col_name in self.dataframe.columns]
        for col in self.args.text_names+self.args.var_names:
            if col not in self.dataframe_cols:
                raise ValueError(f"ERROR: the '{col}' column is not present in the dataframe.")
            

    def compute(self):
        """Function that runs the actual computation"""
        # TODO handle metrics in a smarter way.
        label_values_dict = preprocess_utils.get_label_values(self.dataframe, self.col_names_dict)
        
        if len(self.args.var_names) == 1:
            subsets_of_interest = preprocess_utils.get_subset_dict(self.dataframe,
                                                    self.tokenizer.tokenized_col_dict,
                                                    label_values_dict)
        else:        
            # if we have more than two variables, we are interested in the intersections between them

            print("INFO: splitting intersections of variables into subsets...")
            subsets_of_interest = preprocess_utils.get_subset_intersections(self.dataframe,
                                                    self.tokenizer.tokenized_col_dict,
                                                    label_values_dict)
            
            # print(label_values_dict)
            label_values_dict = preprocess_utils.update_label_values_dict_with_inters(label_values_dict)
            print(label_values_dict)
            
        
        
        results_dict = dict()
        for metric in self.args.metrics:
            current_metric = metrics.Metric(metric, self.args)
            if type(metric) is not str:
                metric_name = metric.__name__
            else:
                metric_name = metric
            print(f"INFO: Currently calculating metric {metric_name}...")
            results_dict[metric_name] = {}
            results_dict[metric_name][list(label_values_dict.keys())[0]] = current_metric.calculate_metric(label_values_dict, subsets_of_interest)
            
        # TODO handle series_dict
        self.results_dict = results_dict
        return subsets_of_interest,results_dict

    
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
        self.dataframe = self.tokenizer.tokenize(self.dataframe)
        self.compute()
        self.create_output_dict()
        return self.output_dict