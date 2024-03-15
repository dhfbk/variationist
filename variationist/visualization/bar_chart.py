import altair as alt
import pandas as pd

from typing import Optional

from variationist.visualization.altair_chart import AltairChart


class BarChart(AltairChart):
    """A class for building a BarChart object."""

    def __init__(
        self,
        df_data: pd.core.frame.DataFrame,
        chart_metric: str,
        metadata: dict,
        extra_args: dict = {},
        chart_dims: dict = {},
        zoomable: Optional[bool] = True,
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
        chart_dims: dict
            The mapping dictionary for the variables for the given chart.
        zoomable: Optional[bool] = True
            Whether the (HTML) chart should be zoomable using the mouse or not (if this
            is allowed for the resulting chart type by the underlying visualization 
            library).
        top_per_class_ngrams: int = 20
            The maximum number of highest scoring per-class n-grams to show (for bar
            charts only). If set to None, it will show all the n-grams in the corpus 
            (it may easily be overwhelming). By default is 20 to keep the visualization 
            compact. This parameter is ignored when creating other chart types.
        """

        super().__init__(df_data, chart_metric, metadata, extra_args, zoomable)

        # Set attributes
        self.top_per_class_ngrams = top_per_class_ngrams
        self.metric_label = chart_metric + " value"
        if self.n_cooc == 1:
            self.text_label = (str(self.n_tokens) + "-gram") if self.n_tokens > 1 else "token"
        else:
            self.text_label = "tokens"

        # Set base chart style
        self.base_chart = self.base_chart.mark_bar(height=15, binSpacing=0.5, cornerRadiusEnd=5)

        # Get relevant dimensions
        x_name, x_type = self.get_dim("x", chart_dims)
        y_name, y_type = self.get_dim("y", chart_dims)
        column_name, column_type = self.get_dim("column", chart_dims)
        color_name, color_type = self.get_dim("color", chart_dims)

        # Set dimensions
        x_dim = alt.X(x_name, type=x_type, title=chart_metric)
        y_dim = alt.Y(y_name, type=y_type, title="").sort("-x")
        column_dim = alt.Column(column_name, type=column_type, 
            header=alt.Header(labelFontWeight="bold"))
        color = alt.Color(color_name, color_type, legend=None) # for aestethics only

        # Set tooltip
        tooltip = [
            alt.Tooltip(y_name, type=y_type, title=self.text_label),
            alt.Tooltip(x_name, type=x_type, title=self.metric_label)
        ]

        # Filter data to show up to k top ngrams (based on their value for the metric) for each group
        self.base_chart = self.base_chart.transform_window(
            rank = "rank(" + x_name + ")",
            sort = [alt.SortField(x_name, order="descending"),
                  alt.SortField(y_name, order="ascending")], # break ties in ranking (@temp)
            groupby = [column_name]
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
        chart_width = max(100, 800 / len(list(df_data[column_name].unique())))
        self.base_chart = self.base_chart.properties(width=chart_width, center=True)

        # The chart has to be filterable, therefore create and add a search component to it
        self.base_chart = self.add_search_component(self.base_chart, tooltip, y_dim)

        # If the chart has to be zoomable, set the property (disallowed for bar chart)
        # if self.zoomable == True:
        #     print(f"INFO: Zoom is disallowed for bar charts.")
        #     self.base_chart = self.base_chart.interactive()

        # Create the final chart
        self.chart = self.base_chart

