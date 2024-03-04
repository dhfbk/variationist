import pandas as pd

from typing import Optional


class Chart:
    """A base class for building a chart object."""

    def __init__(
        self,
        df_data: pd.core.frame.DataFrame,
        chart_metric: str,
        metadata: dict,
        filterable: Optional[bool] = True,
        zoomable: Optional[bool] = True,
        variable_values: list = [],
    ) -> None:
        """
        Initialization function for a building a chart object.

        Parameters
        ----------
        df_data: pd.core.frame.DataFrame
            A long-form dataframe storing the results of a prior analysis for a
            given metric that will be used for visualization purposes.
        chart_metric: str
            The metric associated to the "df_data" dataframe and thus to the chart.
        metadata: dict
            A dictionary storing the metadata about the prior analysis.
        filterable: Optional[bool] = True
            Whether the chart should be filterable by using regexes on ngrams or not.
        zoomable: Optional[bool] = True
            Whether the (HTML) chart should be zoomable using the mouse or not.
        variable_values: list = []
            A list of the variable values for the given metric
        """

        self.df_data = df_data
        self.chart_metric = chart_metric
        self.var_names = metadata["var_names"]
        self.var_types = metadata["var_types"]
        self.var_semantics = metadata["var_semantics"]
        self.n_tokens = metadata["n_tokens"]
        self.filterable = filterable
        self.zoomable = zoomable
        self.variable_values = variable_values
        self.chart = None

