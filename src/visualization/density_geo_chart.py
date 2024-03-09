import geopandas as gpd
import os
import pandas as pd
import plotly.express as px

from typing import Optional

from src.visualization.plotly_chart import PlotlyChart

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
        filterable: Optional[bool] = True,
        zoomable: Optional[bool] = True,
        variable_values: list = [],
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
        self.metric_label = chart_metric + " value"
        if self.n_cooc == 1:
            self.text_label = (str(self.n_tokens) + "-gram") if self.n_tokens > 1 else "token"
        else:
            self.text_label = "tokens"

        # Get the centroids for centering the world map
        centroid_lat = (df_data[self.var_names[0]].astype(float).max() + df_data[self.var_names[0]].astype(float).min()) / 2
        centroid_lon = (df_data[self.var_names[1]].astype(float).max() + df_data[self.var_names[1]].astype(float).min()) / 2

        # Set base chart style, dimensions, tooltip, encoding, and extra properties
        self.base_chart = px.density_mapbox(
            df_data, 

            # Set dimensions
            lat = self.var_names[0],
            lon = self.var_names[1],
            z = "value",

            # Set base chart style
            radius = 10,
            center = dict(lat=centroid_lat, lon=centroid_lon),
            zoom = 4.5,
            color_continuous_scale = px.colors.sequential.Inferno,
            opacity = 0.25,
            mapbox_style = "carto-positron",

            # Set tooltip
            hover_data = {
                self.var_names[0]: True,
                self.var_names[1]: True,
                "ngram": True,
                "value": ':.0f'
            }
        )

        # If the chart has to be filterable, create and add a search component to it
        if self.filterable == True:
            dropdown_elements = list(set(df_data["ngram"]))
            self.base_chart = self.add_dropdown_component(self.base_chart, dropdown_elements)

        # If the chart has to be zoomable, set the property (supported by default by Plotly)
        # if self.zoomable == True:
        #     self.base_chart = self.base_chart.interactive()
