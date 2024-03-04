import os
import pandas as pd
import plotly.express as px

from typing import Optional

from src.visualization.chart import Chart


class PlotlyChart(Chart):
    """A base class for building a plotly.graph_objs._figure.Figure chart object."""

    def __init__(
        self,
        df_data: pd.core.frame.DataFrame,
        chart_metric: str,
        metadata: dict,
        filterable: Optional[bool] = True,
        zoomable: Optional[bool] = True,
        variable_values: list = [],
    ) -> None:
        """
        Initialization function for a building a plotly.graph_objs._figure.Figure chart object.

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
        """

        super().__init__(df_data, chart_metric, metadata, filterable, zoomable, variable_values)

        # Create the base chart object which stores the data
        self.base_chart = self.create_base_chart(df_data)


    def create_base_chart(
        self,
        df_data: pd.core.frame.DataFrame,
    ) -> plotly.graph_objs._figure.Figure:
        """
        A function that creates a base plotly.graph_objs._figure.Figure chart for the given data.

        Parameters
        ----------
        df_data: pd.core.frame.DataFrame
            A long-form dataframe storing the results of a prior analysis for a
            given metric that will be used for visualization purposes.

        Returns
        -------
        base_chart: plotly.graph_objs._figure.Figure
            A base plotly.graph_objs._figure.Figure chart object.
        """

        raise NotImplementedError(f"The base chart for Plotly charts has not been implemented yet.")
        return


    def add_search_component(
        self,
        base_chart: plotly.graph_objs._figure.Figure,
    ) -> plotly.graph_objs._figure.Figure:
        """
        A function that creates a search component and adds it to the chart.

        Parameters
        ----------
        base_chart: plotly.graph_objs._figure.Figure
            The base chart object in which to add the search component.

        Returns
        -------
        base_chart: plotly.graph_objs._figure.Figure
            The same base chart object with the search component added.
        """

        raise NotImplementedError(f"The search component for Plotly charts has not been implemented yet.")
        return


    def save(
        self,
        output_folder: str,
        output_formats: Optional[list[str]] = ["html"],
    ) -> None:
        """
        A function that saves the chart to a subfolder (with name matching the metric) 
        of the output folder in various formats.

        Parameters
        ----------
        output_folder: str
            A path to the output folder in which to save the chart.
        output_formats: Optional[list[str]] = ["html"]
            A list of output formats for the charts. By default, only the interactive
            HTML chart is saved, i.e., ["html"]. Extra choices: ["pdf", "svg", "png"].
        """

        # fig.write_html("path/to/file.html")
        raise NotImplementedError(f"The output for Plotly charts has not been implemented yet.")
        return

