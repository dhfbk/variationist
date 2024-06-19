import altair as alt
import pandas as pd

from typing import Optional

from variationist.visualization.altair_chart import AltairChart


class LineChart(AltairChart):
    """A class for building a LineChart object."""

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
        Initialization function for a building a LineChart object.

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

        super().__init__(
            df_data, chart_metric, metadata, extra_args, zoomable)

        # Set attributes
        self.top_per_class_ngrams = top_per_class_ngrams
        self.metric_label = chart_metric + " value"
        if self.n_cooc == 1:
            self.text_label = (str(self.n_tokens) + "-gram") if self.n_tokens > 1 else "token"
        else:
            self.text_label = "tokens"

        # Set base chart style
        if ("size" in chart_dims) or ("shape" in chart_dims):
            self.base_chart = self.base_chart.mark_trail(
                point=alt.OverlayMarkDef(size=75, strokeWidth=0.5))
        else:
            self.base_chart = self.base_chart.mark_line(point=True, strokeDash=[1, 0])

        # Get relevant dimensions
        x_name, x_type = self.get_dim("x", chart_dims)
        y_name, y_type = self.get_dim("y", chart_dims)
        if "size" in chart_dims:
            size_name, size_type = self.get_dim("size", chart_dims)
            color_name, color_type = self.get_dim("color", chart_dims)
        if "shape" in chart_dims:
            shape_name, shape_type = self.get_dim("shape", chart_dims)
            color_name, color_type = self.get_dim("color", chart_dims)

        # Set dimensions
        y_domain = list(df_data[y_name].astype(float).unique())
        x_dim = alt.X(x_name, type=x_type)
        if "size" in chart_dims:
            y_dim = alt.Y(y_name, type=y_type)
            size = alt.Size(size_name, type=size_type)
            color = alt.Color(color_name, type=color_type)
        elif "shape" in chart_dims:
            y_dim = alt.Y(y_name, type=y_type)
            shape = alt.Shape(shape_name, type=shape_type)
            color = alt.Color(color_name, type=color_type)
        else:
            y_dim = alt.Y(y_name, type=y_type, title=chart_metric)
            color = alt.Color("ngram", type="nominal", title="", legend=None)

        # Set tooltip
        tooltip = [
            alt.Tooltip("ngram", type="nominal", title=self.text_label),
            alt.Tooltip(x_name, type=x_type),
        ]
        if "size" in chart_dims:
            tooltip.append(alt.Tooltip(y_name, type=y_type))
            tooltip.append(alt.Tooltip(size_name, type=size_type, title=self.metric_label))
        elif "shape" in chart_dims:
            tooltip.append(alt.Tooltip(shape_name, type=shape_type))
            tooltip.append(alt.Tooltip(y_name, type=y_type))
        else:
            tooltip.append(alt.Tooltip(y_name, type=y_type, title=self.metric_label))

        # Encoding the data
        if "shape" in chart_dims:
            self.base_chart = self.base_chart.encode(
                x_dim,
                y_dim,
                color,
                shape,
                # Note: opacity will be conditionally added by the "add_dropdown_component", if needed
                tooltip
            )
        else:
            self.base_chart = self.base_chart.encode(
                x_dim,
                y_dim,
                color,
                # Note: opacity will be conditionally added by the "add_dropdown_component", if needed
                tooltip
            )

        # Set extra properties
        chart_width = 800
        self.base_chart = self.base_chart.properties(width=chart_width, center=True)

        # The chart has to be filterable, therefore create and add a search component to it
        if ("size" in chart_dims) or ("shape" in chart_dims):
            dropdown_keys = []
            dropdown_values = []
            for i in range(len(chart_dims["dropdown"])):
                dropdown_keys.append(
                    self.get_dim("dropdown", {"dropdown": chart_dims["dropdown"][i]})[0])
            for dropdown_key in dropdown_keys:
                dropdown_values.append(list(set(df_data[dropdown_key])))
            if "size" in chart_dims:
                self.base_chart = self.add_dropdown_components(
                    self.base_chart, tooltip, dropdown_keys, dropdown_values, color, "size")
            else:
                self.base_chart = self.add_dropdown_components(
                    self.base_chart, tooltip, dropdown_keys, dropdown_values, color, "shape")
        else:
            self.base_chart = self.add_search_component(self.base_chart, tooltip, color)

        # If the chart has to be zoomable, set the property
        if self.zoomable == True:
            self.base_chart = self.base_chart.interactive()

        # Create the final chart
        self.chart = self.base_chart

