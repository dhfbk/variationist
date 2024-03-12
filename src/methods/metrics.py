from src.methods import lexical_variation
from src.methods import corpus_statistics
from src import methods
from typing import Callable, Union


class Metric:
    """
    The Metric class, a generic class that carries out all the metric operations.
    """
    def __init__(self, 
                 metric: Union[str, Callable[[dict, dict], dict]],
                 args: int):
        self.metric = metric
        self.args = args

        if self.metric == "pmi":
            self.metric_fn = methods.pmi.pmi
        elif self.metric == "pmi-normalized":
            self.metric_fn = methods.pmi.pmi_normalized
        elif self.metric == "pmi-positive":
            self.metric_fn = methods.pmi.pmi_positive
        elif self.metric == "pmi-positive-normalized":
            self.metric_fn = methods.pmi.pmi_positive_normalized
        elif self.metric == "pmi-weighted":
            self.metric_fn = methods.pmi.pmi_weighted
        elif self.metric == "pmi-normalized-weighted":
            self.metric_fn = methods.pmi.pmi_normalized_weighted
        elif self.metric == "pmi-positive-weighted":
            self.metric_fn = methods.pmi.pmi_positive_weighted
        elif self.metric == "pmi-positive-normalized-weighted":
            self.metric_fn = methods.pmi.pmi_positive_normalized_weighted
        elif self.metric == "ttr":
            self.metric_fn = lexical_variation.ttr
        elif self.metric == "rttr":
            self.metric_fn = lexical_variation.rttr
        elif self.metric == "maas":
            self.metric_fn = lexical_variation.maas
        elif self.metric == "lttr":
            self.metric_fn = lexical_variation.lttr
        elif self.metric == "most-frequent":
            self.metric_fn = methods.most_frequent.create_most_frequent_dictionary
        elif self.metric == "basic-stats":
            self.metric_fn = corpus_statistics.compute_basic_stats
        
        
        elif callable(self.metric):
            self.metric_fn = self.metric
        elif type(self.metric) is str:
            raise NotImplementedError(f"The metric '{self.metric}' is not implemented.")
        else:
            raise ValueError(f"The specified metric should be a callable function or a string matching an implemented metric. Got a {type(self.metric)} instead")
        
    
    def calculate_metric(self, label_values_dict, subsets_of_interest):
        """Calls the appropriate metric function."""
        return self.metric_fn(label_values_dict, subsets_of_interest, self.args)