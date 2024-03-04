import altair as alt
import pandas as pd

from typing import Optional

from src.visualization.altair_chart import AltairChart


class TemporalLineChart(AltairChart):
    """A class for building a BarChart object."""

    def __init__(
        self,
        df_data: pd.core.frame.DataFrame,
        chart_metric: str,
        metadata: dict,
        filterable: Optional[bool] = True,
        zoomable: Optional[bool] = True,
        variable_values: list = [],
        top_per_class_ngrams: Optional[int] = None,
    ) -> None:
        """
        Initialization function for a building a BarChart object.

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
        top_per_class_ngrams: int = 20
            The maximum number of highest scoring per-class n-grams to show. If set to 
            None, it will show all the ngrams in the corpus (it may easily be 
            overwhelming). By default is 20 to keep the visualization compact.
        """

        super().__init__(df_data, chart_metric, metadata, filterable, zoomable, variable_values)

        # Set attributes
        self.top_per_class_ngrams = top_per_class_ngrams
        self.text_label = (str(self.n_tokens) + "-gram") if self.n_tokens > 1 else "token"
        self.metric_label = chart_metric + " value"

        # Set base chart style
        self.base_chart = self.base_chart.mark_line(point=True, strokeDash=[1, 0])

        # Set dimensions
        x_dim = alt.X(self.var_names[0], type=self.var_types[0])
        y_dim = alt.Y("value", type="quantitative", title=chart_metric)
        color = alt.Color("ngram", type="nominal", title="", legend=None)

        # Set tooltip (it will be overwritten if "filterable" is True)
        tooltip = [
            alt.Tooltip("ngram", type="nominal", title=self.text_label),
            alt.Tooltip("value", type="quantitative", title=self.metric_label)
        ]

        # Encoding the data
        self.base_chart = self.base_chart.encode(
            x_dim,
            y_dim,
            color,
            tooltip
        )

        # Set extra properties
        chart_width = 1000
        self.base_chart = self.base_chart.properties(width=chart_width, center=True)

        # If the chart has to be filterable, create and add a search component to it
        if self.filterable == True:
            self.base_chart = self.add_search_component(self.base_chart, tooltip)

        # If the chart has to be zoomable, set the property
        # if self.zoomable == True:
        #     self.base_chart = self.base_chart.interactive()

        # Create the final chart
        self.chart = self.base_chart

