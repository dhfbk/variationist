import altair as alt
import geopandas as gpd
import pandas as pd

from typing import Optional

from src.visualization.altair_chart import AltairChart

# Speed up vector-based spatial data processing
# See: https://geopandas.org/en/stable/docs/user_guide/io.html#reading-spatial-data
gpd.options.io_engine = "pyogrio"


class ChoroplethChart(AltairChart):
    """A class for building a Choropleth object."""

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
        Initialization function for a building a Choropleth object.

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

        # @TODO: Generalize as input field to the class
        shapefile = "Reg01012022_g_WGS84.shp"
        area_names_gdf = "DEN_REG"
        #for col in gdf.columns:
        #    print(col)

        # Load a shapefile and transform geometries to a standard coordinate reference system
        gdf = gpd.read_file(shapefile).to_crs("epsg:4286")

        # Warn the user if some variable values (area names) do not match the area names in the shapefile
        missing_areas = []
        for variable_value in variable_values:
            if variable_value not in list(gdf[area_names_gdf]):
                missing_areas.append(variable_value)
        if len(missing_areas) > 0:
            print(f"WARNING. Some area names defined in the dataset do not match the area names",
                f"defined in the shapefile \"{shapefile}\" and therefore will not be part of the chart.\n",
                f"\tArea names without a match: {', '.join(missing_areas)}.\n",
                f"\tArea names from the shapefile: {', '.join(list(gdf[area_names_gdf]))}.\n")

        # Set base chart style
        self.base_chart = self.base_chart.mark_geoshape(
            fill="lightgray", stroke="white", strokeWidth=0.5)

        # Collect information from the geopandas dataframe
        self.base_chart = self.base_chart.transform_lookup(
            lookup="region",
            from_=alt.LookupData(data=gdf, key="DEN_REG", fields=["geometry", "type"]))

        # Set dimensions
        color = alt.Color("value", type="quantitative", title=chart_metric)

        # Set tooltip (it will be overwritten if "filterable" is True)
        tooltip = [
            alt.Tooltip("ngram", type="nominal", title=self.text_label),
            alt.Tooltip(self.var_names[0], type=self.var_types[0]),
            alt.Tooltip("value", type="quantitative", title=self.metric_label)
        ]

        # Encoding the data
        self.base_chart = self.base_chart.encode(
            fill=color,
            tooltip=tooltip
        )

        # Set extra properties
        chart_base_size = 600
        self.base_chart = self.base_chart.properties(width=chart_base_size, height=chart_base_size)

        # If the chart has to be filterable, create and add a search component to it
        # @TODO: Fix interaction between tokens and the spatial variable when using the filter
        # @TODO: Also set a default for the base visualization without a filter
        if self.filterable == True:
            self.base_chart = self.add_search_component(self.base_chart, "ngram")

        # If the chart has to be zoomable, set the property (not supported for choropleth chart by Altair)
        # if self.zoomable == True:
        #     print(f"INFO: Zoom is not supported for choropleth charts by Altair.")
        #     self.base_chart = self.base_chart.interactive()

        # Create the final chart
        self.chart = self.base_chart

