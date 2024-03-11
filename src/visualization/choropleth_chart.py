import altair as alt
import geopandas as gpd
import os
import pandas as pd

from typing import Optional

from src.visualization.altair_chart import AltairChart

# Speed up vector-based spatial data processing
# See: https://geopandas.org/en/stable/docs/user_guide/io.html#reading-spatial-data
gpd.options.io_engine = "pyogrio"


class ChoroplethChart(AltairChart):
    """A class for building a ChoroplethChart object."""

    def __init__(
        self,
        df_data: pd.core.frame.DataFrame,
        chart_metric: str,
        metadata: dict,
        extra_args: dict = {},
        chart_dims: dict = {},
        filterable: Optional[bool] = True,
        zoomable: Optional[bool] = True,
        variable_values: list = [],
        top_per_class_ngrams: Optional[int] = None,
    ) -> None:
        """
        Initialization function for a building a ChoroplethChart object.

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

        # Set extra attributes
        self.shapefile_path = extra_args["shapefile_path"]
        self.shapefile_var_name = extra_args["shapefile_var_name"]

        # Check if the specified filepath "shapefile_path" is defined and exists. If not, warn and exit
        if self.shapefile_path is None:
            raise ValueError(f"ERROR. \"shapefile_path\" must be specified for creating spatial charts.\n")
        if not os.path.exists(self.shapefile_path):
            raise ValueError(f"ERROR. The filepath for the shapefile \"{self.shapefile_path}\" does not exist.\n")

        # Load the shapefile and transform geometries to a standard coordinate reference system
        gdf = gpd.read_file(self.shapefile_path).to_crs("epsg:4286")

        # Check if the specified column "shapefile_var_name" exists in the geodataframe
        # If not, warn the user, give them the available options, and exit
        if self.shapefile_var_name not in gdf.columns:
            raise ValueError(f"ERROR. The key \"{self.shapefile_var_name}\" is not in the shapefile.",
                f"\"{self.shapefile_path}\".\nPlease use one among: {', '.join([col for col in gdf.columns])}.")

        # Check if some variable values (area names) do not match the area names in the shapefile
        # If not, warn the user and give them the available values that can possibly match.
        variable_values_not_matched = []
        variable_values_gdf = list(gdf[self.shapefile_var_name])
        for variable_value in variable_values:
            if variable_value not in variable_values_gdf:
                variable_values_not_matched.append(variable_value)
        if len(variable_values_not_matched) > 0:
            print(f"WARNING. Some area names defined in the dataset do not match the area names",
                f"defined in the shapefile \"{self.shapefile_path}\" and therefore will not be part of",
                f"the chart. Consider renaming the area names without a match.\n",
                f"\tArea names without a match: {', '.join(variable_values_not_matched)}.\n",
                f"\tArea names from the shapefile: {', '.join(variable_values_gdf)}.\n")

        # Set background chart style
        background = alt.Chart(gdf).mark_geoshape(
            stroke="white", strokeWidth=0.5, fill="#e1e7e3")

        # Set base chart style
        self.base_chart = self.base_chart.mark_geoshape(
            stroke="white", strokeWidth=0.5)

        # Get relevant dimensions
        color_name, color_type = self.get_dim("color", chart_dims)

        # Collect information from the geopandas dataframe
        self.base_chart = self.base_chart.transform_lookup(
            lookup = color_name,
            from_ = alt.LookupData(data=gdf, key=self.shapefile_var_name, fields=["geometry", "type"]))

        # Set dimensions
        # @TODO: Fix "min" and "NaN" together in the starting legend
        color = alt.Color("value", type="quantitative", title=chart_metric,
            scale=alt.Scale(scheme="lighttealblue", domainMin=min(self.df_data["value"])))

        # Set tooltip
        tooltip = [
            alt.Tooltip("ngram", type="nominal", title=self.text_label),
            alt.Tooltip(color_name, type=color_type),
            alt.Tooltip("value", type="quantitative", title=self.metric_label)
        ]

        # Encoding the data
        self.base_chart = self.base_chart.encode(
            # Note: fill=color will be conditionally added by the "add_dropdown_component"
            tooltip = tooltip
        )

        # Set extra properties for both background and foreground layers
        chart_base_size = 600
        background = background.properties(width=chart_base_size, height=chart_base_size)
        self.base_chart = self.base_chart.properties(width=chart_base_size, height=chart_base_size)

        # If the chart has to be filterable, create and add a search component to it
        # Note: the chart is always filterable for choropleth charts
        if self.filterable == True:
            dropdown_elements = list(set(df_data["ngram"]))
            self.base_chart = self.add_dropdown_component(self.base_chart, tooltip, ["ngram"], dropdown_elements, color)

        # If the chart has to be zoomable, set the property (not supported for choropleth chart by Altair)
        # if self.zoomable == True:
        #     print(f"INFO: Zoom is not supported for choropleth charts by Altair.")
        #     self.base_chart = self.base_chart.interactive()

        # Create the final chart
        self.chart = background + self.base_chart

