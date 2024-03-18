import altair as alt
import pandas as pd

from typing import Optional

from variationist.visualization.altair_chart import AltairChart


class StatsBarChart(AltairChart):
    """A class for building a BarChart object for basic stats."""

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
        Initialization function for a building a BarChart object for basic stats.

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

        # Get relevant dimensions
        variables = list(self.df_data.keys())
        for main_col in ["statistics", "val_1", "val_2"]:
            variables.remove(main_col)
        y_name, y_type = variables[0], "nominal"

        # Set attributes
        self.top_per_class_ngrams = top_per_class_ngrams
        self.metric_label = chart_metric + " value"
        self.text_label = y_name

        # Set base chart style
        self.base_chart = self.base_chart.mark_bar(height=15, binSpacing=0.5, cornerRadiusEnd=5)

        # Set dimensions
        x_dim = alt.X("val_1", type="quantitative", title="")
        y_dim = alt.Y(y_name, type=y_type, title="").sort("-x")
        column_dim = alt.Column("statistics", type="nominal", 
            header=alt.Header(labelFontWeight="bold"))
        color = alt.Color("statistics", "nominal", legend=None) # for aestethics only

        # Set tooltip
        tooltip = [
            alt.Tooltip(y_name, type=y_type, title=self.text_label),
            alt.Tooltip("val_1", type="quantitative", title="mean"),
            alt.Tooltip("val_2", type="quantitative", title="stdev")
        ]

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
        chart_width = max(100, 800 / len(list(df_data["statistics"].unique())))
        self.base_chart = self.base_chart.properties(width=chart_width, center=True)

        # The chart has not to be filterable
        self.base_chart = self.base_chart.encode(color=y_dim)

        # If the chart has to be zoomable, set the property (disallowed for bar chart)
        # if self.zoomable == True:
        #     print(f"INFO: Zoom is disallowed for bar charts.")
        #     self.base_chart = self.base_chart.interactive()

        # Create the final chart
        self.chart = self.base_chart

