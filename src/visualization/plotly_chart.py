import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

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
    ): # -> plotly.graph_objs._figure.Figure:
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

        base_chart = go.Figure()

        return base_chart


    def add_dropdown_component(
        self,
        base_chart, # plotly.graph_objs._figure.Figure,
        dropdown_elements: list[str],
    ): # -> plotly.graph_objs._figure.Figure:
        """
        A function that creates a dropdown component and adds it to the chart.

        Parameters
        ----------
        base_chart: alt.Chart
            The base chart object in which to add the dropdown component.
        dropdown_elements: list[str]
            A list of possible values for the field to put in the dropdown.

        Returns
        -------
        base_chart: alt.Chart
            The same base chart object with the dropdown component added.
        """

        # Set the elements on the dropdown
        # @TODO: Release in the next version (0.2.0), also note that this is non trivial: 
        # See: https://stackoverflow.com/questions/72130267/how-to-modify-points-drawn-on-map-using-a-dropdown-menu
        buttons = []
        # for dropdown_element in dropdown_elements:
        #     buttons.append(
        #         dict(args=["type", "value"], label="test", method="restyle"))

        # Update the chart with the dropdown
        base_chart.update_layout(
            updatemenus = [
                dict(
                    buttons = buttons,
                    direction = "down",
                    pad = {"r": 10, "t": 10},
                    showactive = True,
                    x = 0.1,
                    xanchor = "left",
                    y = 1.1,
                    yanchor = "top"
                ),
            ]
        )

        # Add the dropdown component to the chart
        base_chart.update_layout(
            annotations = [
                dict(
                    text = f"Filter by {self.text_label} ",
                    showarrow = False,
                    x = 0,
                    y = 1.085,
                    yref = "paper",
                    align="left"
                )
            ]
        )

        return base_chart


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

        # If output formats have been specified, save the chart in those formats to 
        # subfolders (named as the metric) of the user-specified output folder
        if len(output_formats) >= 1:
            # Set the full folder name
            FOLDER_PATH = os.path.join(output_folder, self.chart_metric)

            # Create the output folder if it does not exist
            if not os.path.exists(FOLDER_PATH):
                os.makedirs(FOLDER_PATH)

            # Save the chart to an HTML file in the output folder
            if "html" in output_formats:
                self.base_chart.write_html(os.path.join(FOLDER_PATH, "chart.html"))

            # Save the chart to a PDF file in the output folder
            if "pdf" in output_formats:
                # Write the raw data to the output filepath
                self.base_chart.write_image(os.path.join(FOLDER_PATH, "chart.pdf"))

            # Save the chart to a SVG file in the output folder
            if "svg" in output_formats:
                # Write the raw data to the output filepath
                self.base_chart.write_image(os.path.join(FOLDER_PATH, "chart.svg"))

            # Save the chart to a PNG file in the output folder
            if "png" in output_formats:
                # Write the raw data to the output filepath
                self.base_chart.write_image(os.path.join(FOLDER_PATH, "chart.png"))

        # Otherwise, raise an error
        else:
            raise TypeError(f"ERROR: No output formats have been specified.")

