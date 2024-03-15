import geopandas as gpd
import os
import pandas as pd
import plotly.express as px

from typing import Optional

from variationist.visualization.plotly_chart import PlotlyChart

# Speed up vector-based spatial data processing
# See: https://geopandas.org/en/stable/docs/user_guide/io.html#reading-spatial-data
gpd.options.io_engine = "pyogrio"


class DensityGeoChart(PlotlyChart):
    """A class for building a DensityGeoChart object."""

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
        Initialization function for a building a DensityGeoChart object.

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

        # Get relevant dimensions
        lat_name, lat_type = self.get_dim("lat", chart_dims)
        lon_name, lon_type = self.get_dim("lon", chart_dims)
        color_name, color_type = self.get_dim("color", chart_dims)

        # Get the centroids for centering the world map
        centroid_lat = (df_data[lat_name].astype(float).max() + df_data[lat_name].astype(float).min()) / 2
        centroid_lon = (df_data[lon_name].astype(float).max() + df_data[lon_name].astype(float).min()) / 2

        # Set base chart style, dimensions, tooltip, encoding, and extra properties
        self.base_chart = px.density_mapbox(
            df_data, 

            # Set dimensions
            lat = lat_name,
            lon = lon_name,
            z = color_name,

            # Set base chart style
            radius = 10,
            center = dict(lat=centroid_lat, lon=centroid_lon),
            zoom = 4.5,
            color_continuous_scale = px.colors.sequential.Inferno,
            opacity = 0.25,
            mapbox_style = "carto-positron",

            # Set tooltip
            hover_data = {
                lat_name: True,
                lon_name: True,
                "ngram": True,
                color_name: ':.0f'
            }
        )

        # The chart has to be filterable, therefore create and add search/dropdown components to it
        dropdown_keys = []
        dropdown_values = []
        for i in range(len(chart_dims["dropdown"])):
            dropdown_keys.append(self.get_dim("dropdown", {"dropdown": chart_dims["dropdown"][i]})[0])
        for dropdown_key in dropdown_keys:
            dropdown_values.append(list(set(df_data[dropdown_key])))
        self.base_chart = self.add_dropdown_components(self.base_chart, dropdown_values)

        # If the chart has to be zoomable, set the property (supported by default by Plotly)
        # if self.zoomable == True:
        #     self.base_chart = self.base_chart.interactive()

