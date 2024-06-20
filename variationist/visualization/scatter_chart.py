import altair as alt
import pandas as pd

from typing import Optional

from variationist.visualization.altair_chart import AltairChart


class ScatterChart(AltairChart):
    """A class for building a ScatterChart object."""

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
        Initialization function for a building a ScatterChart object.

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
        if "opacity" in chart_dims:
            self.base_chart = self.base_chart.mark_line(
                point=alt.OverlayMarkDef(size=75, strokeWidth=0.5), strokeWidth=0)
        else:
            self.base_chart = self.base_chart.mark_line(point=True, strokeDash=[1, 0])

        # Get relevant dimensions
        x_name, x_type = self.get_dim("x", chart_dims)
        y_name, y_type = self.get_dim("y", chart_dims)
        if "opacity" in chart_dims:
            opacity_name, opacity_type = self.get_dim("opacity", chart_dims)
        if "extra" in chart_dims:
            extra_name, extra_type = self.get_dim("extra", chart_dims)

        # Use the mean to represent the bin, if defined
        if df_data[x_name][0].startswith("("):
            avgs = []
            for index, row in df_data.iterrows():
                x_min, x_max = row[x_name][1:-1].split(", ")
                avgs.append((float(x_min) + float(x_max)) / 2)
            df_data[x_name] = avgs
        if df_data[y_name][0].startswith("("):
            avgs = []
            for index, row in df_data.iterrows():
                y_min, y_max = row[y_name][1:-1].split(", ")
                avgs.append((float(y_min) + float(y_max)) / 2)
            df_data[y_name] = avgs

        # Set dimensions
        x_domain = list(df_data[x_name].astype(float).unique())
        y_domain = list(df_data[y_name].astype(float).unique())
        x_dim = alt.X(x_name, type=x_type, scale=alt.Scale(domain=[min(x_domain), max(x_domain)]))
        if "opacity" in chart_dims:
            y_dim = alt.Y(y_name, type=y_type, scale=alt.Scale(domain=[min(y_domain), max(y_domain)]), axis=alt.Axis(format=".2f"))
            opacity = alt.Opacity(opacity_name, opacity_type)
        else:
            y_dim = alt.Y(y_name, type=y_type, scale=alt.Scale(domainMin=min(y_domain)), title=chart_metric, axis=alt.Axis(format=".2f"))
        color = alt.Color("ngram", type="nominal", title="", legend=None)

        # Set tooltip
        tooltip = [
            alt.Tooltip("ngram", type="nominal", title=self.text_label),
            alt.Tooltip(x_name, type=x_type),
        ]
        if "opacity" in chart_dims:
            tooltip.append(alt.Tooltip(y_name, type=y_type))
            tooltip.append(alt.Tooltip(opacity_name, type=opacity_type, title=self.metric_label))
        else:
            tooltip.append(alt.Tooltip(y_name, type=y_type, title=self.metric_label))
        if "extra" in chart_dims:
            tooltip.append(alt.Tooltip(extra_name, type=extra_type))

        # Encoding the data
        self.base_chart = self.base_chart.encode(
            x_dim,
            y_dim,
            # Note: color will be conditionally added by the "add_search_component"
            # Note: opacity will be conditionally added by the "add_dropdown_component", if needed
            tooltip
        )

        # Set extra properties
        chart_width = 800
        self.base_chart = self.base_chart.properties(width=chart_width, center=True)

        # The chart has to be filterable, therefore create and add a search component to it
        if ("opacity" in chart_dims) or ("extra" in chart_dims):
            dropdown_keys = []
            dropdown_values = []
            for i in range(len(chart_dims["dropdown"])):
                dropdown_keys.append(
                    self.get_dim("dropdown", {"dropdown": chart_dims["dropdown"][i]})[0])
            for dropdown_key in dropdown_keys:
                dropdown_values.append(list(set(df_data[dropdown_key])))
            if "opacity" in chart_dims:
                self.base_chart = self.add_dropdown_components(
                    self.base_chart, tooltip, dropdown_keys, dropdown_values, color, "opacity")
            else:
                self.base_chart = self.add_dropdown_components(
                    self.base_chart, tooltip, dropdown_keys, dropdown_values, color, "color")
        else:
            self.base_chart = self.add_search_component(self.base_chart, tooltip, color)

        # If the chart has to be zoomable, set the property
        if self.zoomable == True:
            self.base_chart = self.base_chart.interactive()

        # Create the final chart
        self.chart = self.base_chart

