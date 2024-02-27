from src import methods

class Metric:
    """
    The Metric class, a generic class that carries out all the metric operations.
    """
    def __init__(self, metric):
        self.metric = metric
    
        if self.metric == "pmi":
            self.metric_fn = methods.pmi.create_pmi_dictionary
        elif self.metric == "most-frequent":
            self.metric_fn = methods.most_frequent.create_most_frequent_dictionary
        else:
            raise NotImplementedError(f"The metric '{self.metric}' is not implemented.")
    
    def calculate_metric(self, label_values_dict, subsets_of_interest):
        """Calls the appropriate metric function."""
        return self.metric_fn(label_values_dict, subsets_of_interest)