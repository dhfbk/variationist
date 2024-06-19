"""
The Inspector class, to handle all the operations of Variationist.
"""
import json
import os
import pandas as pd
import sys
from dataclasses import dataclass, asdict, field
from datasets import Dataset
from typing import Callable, List, Optional, Tuple, Union, Dict

from variationist import utils
from variationist.data import preprocess_utils
from variationist.data.tokenization import Tokenizer
from variationist.metrics import metrics


@dataclass
class InspectorArgs:
    """A dataclass to store all of the arguments that relate to the analysis.
    
    Parameters
    ----------
        text_names (`List[str]`):
            The list of names of text columns in the given dataset to use for the analysis. 
        var_names (`List[str]`):
            The list of variable names to use for the analysis. Each string in var_names 
            should correspond to a dataset column.
        var_types (`List[str]`):
            The list of variable types corresponding to the variables in `var_names`. Should 
            match the length of `var_names`. Available choices are `nominal` (default), 
            `ordinal`, `quantitative`, and `coordinates`. These are mostly used for binning 
            and visualization.
        var_semantics (`List[str]`):
            The list of variable semantics corresponding to the variables in `var_names`. 
            Should match the length of `var_names`. Available choices are `general` (default), 
            `temporal`, and `spatial`. These are mostly used for binning and visualization.
        var_bins (`List[int]`):
            The list of indices for variables that should be split into bins for the analysis. 
            Works with quantitative variables, dates and timestamps. Will default to 0 for each 
            specified variable, indicating 0 bins.
        tokenizer (`str` or `Callable`), *optional*, defaults to `whitespace`):
            The tokenizer used to preprocess the data. Will default to whitespace tokenization 
            if not specified. Alternatively, it can be a string in the format "hf::tokenizer_name" 
            for loading a HuggingFace tokenizer. A custom function can also be passed for 
            tokenization. It should take as input an array of texts (assumed to be a Pandas Series) 
            and the InspectorArgs. It should return the same array but tokenized. Check out our 
            example notebooks for examples.
        language (`str`):
            The language of the text in the dataset. Used for proper tokenization and stopword 
            removal.
        metrics (`List[str, Callable]`, *optional*):
            The list of metrics that should be calculated. It can be one of the metrics natively 
            implemented by Variationist or a custom callable function.
        n_tokens (`Int`):
            The number of tokens that should be considered for the analysis. 1 corresponds to 
            unigrams, 2 corresponds to bigrams, and so on.
        n_cooc (`Int`):
            The number of tokens used for calculating non-consecutive co-occurrences. For example, 
            n=2 means we consider as the base units for our analysis any pair of tokens that 
            co-occur in the same sentence. n=3 means we consider triplets of tokens, etc. Defaults 
            to n=1, meaning no co-occurrences are taken into consideration, and we only consider 
            n-grams.
        unique_cooc (`Bool`):
            Whether to consider unique co-occurrences or not. Default to False (keep duplicate 
            tokens). If True, multiple occurrences of the same token in a text will be discarded. 
            This does not affect the co-occurrences window size by design (the window size 
            considers the original number of tokens and therefore the original allowed maximum 
            distance between tokens).
        cooc_window_size (`Int`):
            Size of the context window for co-occurrences. For instance, a `cooc_window_size` of 
            3 means we use a context window of 3 to calculate co-occurrences, meaning that any 
            token that is within 3 tokens before or after a given token is added as a co-occurrence.
        freq_cutoff (`Int`):
            The token frequency, expressed as an integer, below which we do not consider the token 
            in the analysis of pmi-based metrics. Defaults to 3.
        stopwords (`Bool`):
            Whether to remove stopwords from texts before tokenization or not (using default lists 
            in a given `language`). Will default to False.
        custom_stopwords (`Optional[Union[str, list]]`):
            A list of stopwords (or a path to a file containing stopwords, one per line) to be 
            removed before tokenization. If `stopwords` is True, these stopwords will be added to 
            that list. Will default to None.
        lowercase (`Bool`):
            Whether to lowercase all the texts before tokenization or not. Will default to False.
        ignore_null_var (`Bool`):
            Whether to proceed when null values are present for variables. Defaults to False, as 
            this behavior can have unpredictable results. Set to True to treat "Nan" as any other 
            variable value.
    """
    
    text_names: Optional[List] = None # explicit column name(s)
    var_names: Optional[List] = None # explicit variable name(s)
    metrics: Optional[List] = None
    var_types: Optional[List] = None # nominal (default), ordinal, quantitative, coordinates
    var_semantics: Optional[List] = None # general (default), temporal, spatial
    var_subsets: Optional[List] = None
    var_bins: Optional[List] = None
    tokenizer: Optional[Union[str, Callable]] = 'whitespace'
    language: Optional[str] = None
    n_tokens: Optional[int] = 1 # maximum value for this should be 5, otherwise the computation will explode
    n_cooc: Optional[int] = 1
    unique_cooc: Optional[bool] = False
    cooc_window_size: Optional[int] = 0
    freq_cutoff: Optional[int] = 3
    stopwords: Optional[bool] = False
    custom_stopwords: Optional[Union[str, list]] = None
    lowercase: Optional[bool] = False
    ignore_null_var: Optional[bool] = False
    

    def check_values(self):
        """Checks the values in text_names, var_names and metrics."""

        if self.text_names == None:
            sys.exit("ERROR: No text_names were provided. These are the names or indices of the columns containing the text to be analyzed.")
        if self.var_names == None:
            sys.exit("ERROR: No var_names were provided. These are the names or indices of the columns containing the variables to be analyzed.")
        if self.metrics == None:
            print("WARNING: No metrics were defined. Variationist will assume only some basic dataset statistics are needed. Please consult the documentation to read what metrics are natively supported and how to use your own.")
            self.metrics = ["basic-stats"]
    

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
    The Inspector class. It takes care of orchestrating the analysis, from importing and 
    tokenizing the data to calculating the metrics and creating an output file with all 
    the calculated metrics for each text column, variable, and combination thereof. 

    Parameters
    ----------
        dataset ([`pandas.DataFrame` or `str`]):
            The dataset to be used for our analysis. It can be a pre-loaded pandas dataframe, 
            or a string indicating a filepath to a .tsv, .csv file, or a Huggingface dataset. 
            Huggingface datasets can also be imported using strings, with the following format: 
            'hf::DATASET_NAME'.
        args (`InspectorArguments`)
            The Inspector arguments. Refer to the InspectorArgs class for details on what these 
            should be.
        
    """

    def __init__(
        self,
        dataset: Union[Dataset, pd.DataFrame, str] = None,
        args: InspectorArgs = InspectorArgs(),
        ):
        """"""
        
        self.dataset = dataset
        self.args = args

        args.check_values()
        
        # Set defaults for variable types and semantics in case they are not defined
        if self.args.var_types == None:
            default_type = "nominal"
            self.args.var_types = [default_type] * len(self.args.var_names)
            print(f"INFO: No values have been set for var_types. Defaults to {default_type}.")
        if self.args.var_semantics == None:
            default_semantics = "general"
            self.args.var_semantics = [default_semantics] * len(self.args.var_names)
            print(f"INFO: No values have been set for var_semantics. Defaults to {default_semantics}.")
        if self.args.var_bins == None:
            default_bin = 0
            self.args.var_bins = [default_bin] * len(self.args.var_names)
            # print(f"INFO: No values have been set for var_bins. Defaults to {default_bin}.")

        # Dictionary for the metadata to be printed in the json output
        metadata_dict = self.args.to_dict()
        print("INFO: The metadata we will be using for the current analysis are:")
        print(metadata_dict)
        metadata_dict["dataset"] = self.dataset 
        self.metadata_dict = metadata_dict
        
        # Check if variable definitions match in length
        if any(len(args.var_names) != len(l) for l in [args.var_types, args.var_semantics, args.var_bins]):
            sys.exit(f"ERROR! All variables in {args.var_names} should have an associated "
                            f"variable type, semantics, and bins. We instead got var_types: {args.var_types}, "
                            f"var_semantics: {args.var_semantics}, and var_bins: {args.var_bins}. Please provide "
                            f"an ordered list of types, semantics, and bins that match variable names "
                            f"and which have matching length for correct variable assignment.")
        
        # Check if column strings are names or indices (for both texts and labels)
        text_names_type = utils.check_column_type(args.text_names)
        label_names_type = utils.check_column_type(args.var_names)
    
        # Since the input file/dataset is the same, we require texts and labels columns to be of the same type
        if text_names_type != label_names_type:
            sys.exit(f"ERROR! text_cols are {text_names_type} while label_cols are {label_names_type}. "
                            "Please provide all column identifiers as names (as in the header line) or indices.")
        self.cols_type = text_names_type
        print(f"INFO: all column identifiers are treated as column {self.cols_type}.")
        
        if type(self.dataset) is Dataset:
            self.dataframe = pd.DataFrame(self.dataset)
            self.metadata_dict["dataset"] = self.dataset.info.dataset_name
        elif type(self.dataset) is pd.DataFrame:
            try:
                self.metadata_dict["dataset"] = self.dataset.name
            except:
                self.metadata_dict["dataset"] = "Custom_User_DataFrame"
            self.dataframe = self.dataset
            pass
        elif type(self.dataset) is str:
            self.dataframe = utils.convert_file_to_dataframe(self.dataset, cols_type=self.cols_type)
        else:
            sys.exit(f"The specified dataset is not one of the accepted ones (string, a pandas DataFrame or a Huggingface Dataset), but a type {type(self.dataset)} instead.")
            
        
        # Create a dictionary containing the specified column strings (values) for texts and labels (keys)
        self.col_names_dict = {
            utils.TEXT_COLS_KEY: args.text_names,
            utils.LABEL_COLS_KEY: args.var_names
        }

        # Instantiate the tokenizer
        self.tokenizer = Tokenizer(self.args)
        
        self.check_columns()
        self.check_nan_values()
        
        # Check if we need to bin or discretize any values
        self.discretize = False
        for i in range(len(self.args.var_names)):
            if self.args.var_bins[i] != 0:
                self.discretize = True


    def check_columns(self):
        """A function to check that the specified text and variable columns are actually in 
        the provided dataset."""

        # Check if the specified columns are actually in the dataframe
        self.dataframe_cols = [col_name for col_name in self.dataframe.columns]
        for col in self.args.text_names+self.args.var_names:
            if col not in self.dataframe_cols:
                sys.exit(f"ERROR: the '{col}' column is not present in the dataframe.")
    
    
    def check_nan_values(self):
        """Checks if the specified variable columns contain Nan values and returns an error."""

        for var in self.args.var_names:
            nulls = self.dataframe[var].isnull()
            if nulls.values.any():
                if self.args.ignore_null_var:
                    print(f"INFO: One or more null values were found for the '{var}' variable. The indices (lines) of null values are {list(nulls[nulls].index)}. Since 'ignore_null_var' was set to True, Nan values will be treated as any other variable value. This might lead to unexpected results.")
                else:
                    sys.exit(f"ERROR: One or more null values were found for the '{var}' variable. The indices (lines) of null values are {list(nulls[nulls].index)}. If you wish to ignore null values and proceed, please set 'ignore_null_var' to True when defining the InspectorArgs.")
    
            
    def handle_bins_and_granularity(self):
        """For each variable that requires binning, checks that it can be carried out and calls 
        the dedicated function."""

        for i in range(len(self.args.var_names)):
            curr_var_name = self.args.var_names[i]
            curr_bins = self.args.var_bins[i]
            curr_type = self.args.var_types[i]
            curr_sem = self.args.var_semantics[i]
            curr_var_column = self.dataframe[curr_var_name]
            if curr_bins != 0:
                if (curr_type != "nominal"):
                    if (curr_type == "ordinal") and (curr_sem != "temporal"):
                        sys.exit(f"ERROR: var_bins was defined for variable {curr_var_name}, whose type is 'ordinal' but its semantics is not 'temporal'. However, ordinal values cannot be divided into bins if not of temporal semantics. If the {curr_var_name} variable is numeric, please specify another var_type for it. If it is an actual ordinal variable but not temporal, its var_bins value should be 0.")
                    if type(curr_bins) is int:
                        if curr_sem == "temporal":
                            curr_var_column = pd.to_datetime(curr_var_column)
                        print(f"INFO: For the variable {curr_var_name}, bins were defined. It will therefore be split into {curr_bins} equal bins.")
                        self.dataframe[curr_var_name] = preprocess_utils.discretize_bins_col(
                            curr_var_column, curr_bins
                        )
                    else:
                        sys.exit(f"ERROR: var_bins was defined, but not correctly. We expected a list of integer values for each variable (with 0 for variables where no binning is desired), but instead for the variable {curr_var_name} the input was of type {type(curr_bins).__name__}.")
                else:
                    sys.exit(f"ERROR: var_bins was defined for variable {curr_var_name}, whose type is 'nominal'. However, nominal values cannot be divided into bins. If the {curr_var_name} variable is numeric, please specify another var_type for it. If it is an actual nominal variable, its var_bins value should be 0.")


    def preprocess(self):
        """Performs all of the preprocessing operations of Variationist, such as grouping 
        together variables and dividing variables into bins."""

        # Check if any discretization or binning should be carried out and do it
        if self.discretize == True:
            self.handle_bins_and_granularity()
        
        label_values_dict = preprocess_utils.get_label_values(self.dataframe, self.col_names_dict)
        if len(self.args.var_names) == 1 and  len(self.args.text_names) == 1:
            subsets_of_interest = preprocess_utils.get_subset_dict(self.dataframe,
                                                    self.tokenizer.tokenized_col_dict,
                                                    label_values_dict)
        else:        
            # if we have more than two variables, we are interested in the intersections between them
            subsets_of_interest = preprocess_utils.get_subset_intersections(self.dataframe,
                                                    self.tokenizer.tokenized_col_dict,
                                                    label_values_dict)
            label_values_dict = preprocess_utils.update_label_values_dict_with_inters(
                label_values_dict, self.args.text_names)
        
        return label_values_dict, subsets_of_interest


    def compute(self):
        """Main function carrying out the entire analysis pipeline. It creates a results dict 
        with the calculated metrics."""

        label_values_dict, subsets_of_interest = self.preprocess()
        
        results_dict = dict()
        for metric in self.args.metrics:
            current_metric = metrics.Metric(metric, self.args)
            if type(metric) is not str:
                metric_name = metric.__name__
            else:
                metric_name = metric
            print(f"INFO: Currently calculating metric: '{metric_name}'")
            results_dict[metric_name] = {}
            
            if metric_name == "stats":
                results_dict[metric_name] = current_metric.calculate_metric(
                    label_values_dict, subsets_of_interest)
            else:
                results_dict[metric_name][list(label_values_dict.keys())[0]] = current_metric.calculate_metric(
                    label_values_dict, subsets_of_interest)
            
        self.results_dict = results_dict

        return subsets_of_interest, results_dict

    
    def create_output_dict(self):
        """Function to create the output dictionary, containing both metadata and calculated 
        metrics."""

        output_dict = dict()
        output_dict["metadata"] = self.metadata_dict
        output_dict["metrics"] = self.results_dict
        self.output_dict = output_dict
    

    def inspect(self):
        """Wrapper function for tokenizing, carrying out computation, and saving the output 
        dictionary, which it returns."""

        self.dataframe = self.tokenizer.tokenize(self.dataframe)
        self.compute()
        self.create_output_dict()

        return self.output_dict


    def save_output_to_json(self,
                            output_path = "output.json"
                            ):
        """Saves the output dictionary to a json file, which can then be imported with the 
        Visualizer module."""

        output_file = open(output_path, "w")
        json.dump(self.output_dict, output_file, indent=4)
        output_file.close()
        
