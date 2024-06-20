import altair as alt
import pandas as pd

from typing import Optional

from variationist.visualization.altair_chart import AltairChart


class HeatmapChart(AltairChart):
    """A class for building a HeatmapChart object."""

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
        Initialization function for a building a HeatmapChart object.

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
        self.base_chart = self.base_chart.mark_rect()

        # Get relevant dimensions
        x_name, x_type = self.get_dim("x", chart_dims)
        y_name, y_type = self.get_dim("y", chart_dims)
        color_name, color_type = self.get_dim("color", chart_dims)

        # Handle label ordering for bins
        no_bins = all(var_bin == 0 for var_bin in metadata["var_bins"])
        if no_bins:
            x_domain = sorted(list(df_data[x_name].unique()))
            y_domain = sorted(list(df_data[y_name].unique()), reverse=True)
        else:
            # Heuristics: if there are no bins based on the first element, avoid reversing
            to_reverse = False if df_data[x_name][0].startswith("(") else True
            x_domain = sorted(list(df_data[x_name].unique()), 
                key=lambda x: float(x.split(", ")[0][1:]) if x.startswith("(") else x, reverse=False)
            y_domain = sorted(list(df_data[y_name].unique()), 
                key=lambda y: float(y.split(", ")[0][1:]) if y.startswith("(") else y, reverse=to_reverse)

        # Set dimensions
        x_dim = alt.X(x_name, type=x_type, scale=alt.Scale(domain=x_domain))
        y_dim = alt.Y(y_name, type=y_type, scale=alt.Scale(domain=y_domain))
        color = alt.Color(color_name, type=color_type, title=chart_metric)

        # Set tooltip
        tooltip = [
            alt.Tooltip("ngram", type="nominal", title=self.text_label),
            alt.Tooltip(x_name, type=x_type),
            alt.Tooltip(y_name, type=y_type),
            alt.Tooltip(color_name, type=color_type, title=self.metric_label)
        ]

        # Encoding the data
        self.base_chart = self.base_chart.encode(
            x_dim,
            y_dim,
            # Note: color will be conditionally added by the "add_search_component"
            tooltip
        )

        # Set extra properties
        num_labels_x = len(list(df_data[x_name].unique()))
        num_labels_y = len(list(df_data[y_name].unique()))
        chart_width = min(num_labels_x * 50, 800)
        chart_height = min(num_labels_y * 50, 600)
        self.base_chart = self.base_chart.properties(width=chart_width, height=chart_height, center=True)

        # The chart has to be filterable, therefore create and add search/dropdown components to it
        dropdown_keys = []
        dropdown_values = []
        for i in range(len(chart_dims["dropdown"])):
            dropdown_keys.append(self.get_dim("dropdown", {"dropdown": chart_dims["dropdown"][i]})[0])
        for dropdown_key in dropdown_keys:
            dropdown_values.append(list(set(df_data[dropdown_key])))
        self.base_chart = self.add_dropdown_components(
            self.base_chart, tooltip, dropdown_keys, dropdown_values, color, "fill")

        # If the chart has to be zoomable, set the property
        if self.zoomable == True:
            self.base_chart = self.base_chart.interactive()

        # Create the final chart
        self.chart = self.base_chart

