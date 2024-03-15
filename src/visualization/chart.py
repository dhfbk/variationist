import pandas as pd

from typing import Optional


class Chart:
    """A base class for building a chart object."""

    def __init__(
        self,
        df_data: pd.core.frame.DataFrame,
        chart_metric: str,
        metadata: dict,
        extra_args: dict = {},
        zoomable: Optional[bool] = True,
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
        extra_args: dict = {}
            A dictionary storing the extra arguments for this chart type. Default = {}.
        zoomable: Optional[bool] = True
            Whether the (HTML) chart should be zoomable using the mouse or not (if this
            is allowed for the resulting chart type by the underlying visualization 
            library).
        """

        self.df_data = df_data
        self.chart_metric = chart_metric
        self.var_names = metadata["var_names"]
        self.var_types = metadata["var_types"]
        self.var_semantics = metadata["var_semantics"]
        self.n_tokens = metadata["n_tokens"]
        self.n_cooc = metadata["n_cooc"]
        self.extra_args = {}
        self.zoomable = zoomable
        self.chart = None

