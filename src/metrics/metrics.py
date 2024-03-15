from typing import Callable, Union

from src.metrics import corpus_statistics
from src.metrics import lexical_variation
from src.metrics import pmi


class Metric:
    """The Metric class, a generic class that carries out all the metric operations."""

    def __init__(
        self,
        metric: Union[str, Callable[[dict, dict], dict]],
        args: int
    ) -> None:
        """"""

        self.metric = metric
        self.args = args

        if self.metric == "pmi":
            self.metric_fn = pmi.pmi
        elif self.metric == "n_pmi":
            self.metric_fn = pmi.pmi_normalized
        elif self.metric == "p_pmi":
            self.metric_fn = pmi.pmi_positive
        elif self.metric == "np_pmi":
            self.metric_fn = pmi.pmi_positive_normalized
        elif self.metric == "w_pmi":
            self.metric_fn = pmi.pmi_weighted
        elif self.metric == "nw_pmi":
            self.metric_fn = pmi.pmi_normalized_weighted
        elif self.metric == "pw_pmi":
            self.metric_fn = pmi.pmi_positive_weighted
        elif self.metric == "npw_pmi":
            self.metric_fn = pmi.pmi_positive_normalized_weighted
        elif self.metric == "np_relevance":
            self.metric_fn = pmi.class_relevance_positive_normalized
        elif self.metric == "nw_relevance":
            self.metric_fn = pmi.class_relevance_normalized_weighted
        elif self.metric == "npw_relevance":
            self.metric_fn = pmi.class_relevance_positive_normalized_weighted
        elif self.metric == "lex_art":
            self.metric_fn = pmi.pmi_lexical_artifacts
        elif self.metric == "ttr":
            self.metric_fn = lexical_variation.ttr
        elif self.metric == "root_ttr":
            self.metric_fn = lexical_variation.rttr
        elif self.metric == "maas":
            self.metric_fn = lexical_variation.maas
        elif self.metric == "log_ttr":
            self.metric_fn = lexical_variation.lttr
        elif self.metric == "freq":
            self.metric_fn = corpus_statistics.create_frequency_dictionary
        elif self.metric == "stats":
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
