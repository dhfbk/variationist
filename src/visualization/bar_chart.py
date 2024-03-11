import altair as alt
import pandas as pd

from typing import Optional

from src.visualization.altair_chart import AltairChart


class BarChart(AltairChart):
    """A class for building a BarChart object."""

    def __init__(
        self,
        df_data: pd.core.frame.DataFrame,
        chart_metric: str,
        metadata: dict,
        extra_args: dict = {},
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
        extra_args: dict = {}
            A dictionary storing the extra arguments for this chart type. Default = {}.
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

        super().__init__(
            df_data, chart_metric, metadata, extra_args, filterable, zoomable, variable_values)

        # Set attributes
        self.variable_values = variable_values
        self.top_per_class_ngrams = top_per_class_ngrams
        self.metric_label = chart_metric + " value"
        if self.n_cooc == 1:
            self.text_label = (str(self.n_tokens) + "-gram") if self.n_tokens > 1 else "token"
        else:
            self.text_label = "tokens"

        # Set base chart style
        self.base_chart = self.base_chart.mark_bar(height=15, binSpacing=0.5, cornerRadiusEnd=5)

        # Set dimensions
        x_dim = alt.X("value", type="quantitative", title=chart_metric)
        y_dim = alt.Y("ngram", type="nominal", title="").sort("-x")
        column_dim = alt.Column(self.var_names[0], type=self.var_types[0], 
            header=alt.Header(labelFontWeight="bold"))
        color = alt.Color(self.var_names[0], self.var_types[0], legend=None) # for aestethics only

        # Set tooltip (it will be overwritten if "filterable" is True)
        tooltip = [
            alt.Tooltip("ngram", type="nominal", title=self.text_label),
            alt.Tooltip("value", type="quantitative", title=self.metric_label)
        ]

        # Filter data to show up to k top ngrams (based on their value for the metric) for each group
        self.base_chart = self.base_chart.transform_window(
            rank = "rank(value)",
            sort = [alt.SortField("value", order="descending"),
                  alt.SortField("ngram", order="ascending")], # break ties in ranking (@temp)
            groupby = [self.var_names[0]]
        ).transform_filter(
            alt.datum.rank <= self.top_per_class_ngrams
        )

        # Encoding the data
        self.base_chart = self.base_chart.encode(
            x_dim,
            y_dim,
            column_dim,
            color,
            tooltip
        )

        # Set the independent dimensions
        self.base_chart = self.base_chart.resolve_scale(
            x="independent",
            y="independent"
        )

        # Set extra properties
        chart_width = max(100, 800 / len(self.variable_values))
        self.base_chart = self.base_chart.properties(width=chart_width, center=True)

        # If the chart has to be filterable, create and add a search component to it
        if self.filterable == True:
            self.base_chart = self.add_search_component(self.base_chart, tooltip, y_dim)

        # If the chart has to be zoomable, set the property (disallowed for bar chart)
        # if self.zoomable == True:
        #     print(f"INFO: Zoom is disallowed for bar charts.")
        #     self.base_chart = self.base_chart.interactive()

        # Create the final chart
        self.chart = self.base_chart

