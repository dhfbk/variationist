import altair as alt
import os
import pandas as pd

from typing import Optional

from src.visualization.chart import Chart


class AltairChart(Chart):
    """A base class for building an alt.Chart chart object."""

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
        Initialization function for a building an alt.Chart chart object.

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

        # alt.data_transformers.enable("vegafusion")

        # Create the base chart object which stores the data
        self.base_chart = self.create_base_chart(df_data)


    def create_base_chart(
        self,
        df_data: pd.core.frame.DataFrame,
    ) -> alt.Chart:
        """
        A function that creates a base alt.Chart chart for the given data.

        Parameters
        ----------
        df_data: pd.core.frame.DataFrame
            A long-form dataframe storing the results of a prior analysis for a
            given metric that will be used for visualization purposes.

        Returns
        -------
        base_chart: alt.Chart
            A base alt.Chart chart object.
        """

        base_chart = alt.Chart(self.df_data).mark_bar()

        return base_chart


    def add_search_component(
        self,
        base_chart: alt.Chart,
        tooltip_field: str,
        tooltip: list[alt.Tooltip],
        color: alt.Color,
    ) -> alt.Chart:
        """
        A function that creates a search component and adds it to the chart.

        Parameters
        ----------
        base_chart: alt.Chart
            The base chart object in which to add the search component.
        tooltip_field: str
            The field to show as a tooltip.
        tooltip: list[alt.Tooltip]
            A list of alt.Tooltip objects.
        color: alt.Color
            The alt.Color dimension to be shown in the chart.

        Returns
        -------
        base_chart: alt.Chart
            The same base chart object with the search component added.
        """

        # Create the search component
        search_input = alt.param(
            value = "",
            bind = alt.binding(
                input = "search",
                placeholder = f"insert {self.text_label}...",
                name = f"Filter by {self.text_label} ",
            )
        )

        # Add the search component to the base chart
        base_chart = base_chart.add_params(search_input)

        # Set conditions for filtering when using the search component
        base_chart = base_chart.encode(
            opacity = alt.condition(
                alt.expr.test(alt.expr.regexp(search_input, "i"), alt.datum.ngram),
                alt.value(1),
                alt.value(0)
            ),
            color = alt.condition(
                alt.expr.test(alt.expr.regexp(search_input, "i"), alt.datum.ngram),
                color,
                alt.value("")
            ),
            tooltip = tooltip
        )

        return base_chart


    def add_dropdown_component(
        self,
        base_chart: alt.Chart,
        tooltip: list[alt.Tooltip],
        fields: list[str],
        dropdown_elements: list[str],
        color: alt.Color,
    ) -> alt.Chart:
        """
        A function that creates a dropdown component and adds it to the chart.

        Parameters
        ----------
        base_chart: alt.Chart
            The base chart object in which to add the dropdown component.
        tooltip_field: list[alt.Tooltip]
            A list of alt.Tooltip objects.
        fields: list[str]
            A list of fields whose values are used for populating the dropdown.
        dropdown_elements: list[str]
            A list of possible values for the field to put in the dropdown.
        color: alt.Color
            The alt.Color dimension to be shown in the chart.

        Returns
        -------
        base_chart: alt.Chart
            The same base chart object with the dropdown component added.
        """

        # Create the dropdown component
        dropdown = alt.binding_select(
            options = sorted(["*Select " + self.text_label + "*"] + dropdown_elements), 
            name = f"Filter by {self.text_label} ",
        )
        select = alt.selection_point(
            value = f"*Select {self.text_label}*",
            bind = dropdown,
            fields = fields,
        )

        # Add the search component to the base chart
        base_chart = base_chart.add_params(select)
        base_chart = base_chart.transform_filter(select)

        # Encoding the data
        base_chart = base_chart.encode(
            fill = alt.condition(
                select,
                color,
                alt.value("")
            ),
            tooltip = tooltip
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
                self.chart.save(os.path.join(FOLDER_PATH, "chart.html"))

            # Save the chart to a PDF file in the output folder
            if "pdf" in output_formats:
                # Get the raw data from the chart (it requires "vl_convert" to be installed)
                pdf_data = vlc.vegalite_to_pdf(self.chart.to_json())

                # Write the raw data to the output filepath
                with open(os.path.join(FOLDER_PATH, "chart.pdf"), "wb") as f:
                    f.write(pdf_data)

            # Save the chart to a SVG file in the output folder
            if "svg" in output_formats:
                # Get the raw data from the chart (it requires "vl_convert" to be installed)
                svg_data = vlc.vegalite_to_svg(self.chart.to_json())

                # Write the raw data to the output filepath
                with open(os.path.join(FOLDER_PATH, "chart.svg"), "wt") as f:
                    f.write(svg_data)

            # Save the chart to a PNG file in the output folder
            if "png" in output_formats:
                # Get the raw data from the chart (it requires "vl_convert" to be installed)
                png_data = vlc.vegalite_to_png(self.chart.to_json())

                # Write the raw data to the output filepath
                with open(os.path.join(FOLDER_PATH, "chart.png"), "wb") as f:
                    f.write(png_data)

        # Otherwise, raise an error
        else:
            raise TypeError(f"ERROR: No output formats have been specified.")
