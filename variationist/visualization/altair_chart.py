import altair as alt
import functools
import operator
import os
import pandas as pd
import vl_convert as vlc

from typing import Union, Optional

from variationist.visualization.chart import Chart


class AltairChart(Chart):
    """A base class for building an alt.Chart chart object."""

    def __init__(
        self,
        df_data: pd.core.frame.DataFrame,
        chart_metric: str,
        metadata: dict,
        extra_args: dict = {},
        zoomable: Optional[bool] = True,
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
        extra_args: dict = {}
            A dictionary storing the extra arguments for this chart type. Default = {}.
        zoomable: Optional[bool] = True
            Whether the (HTML) chart should be zoomable using the mouse or not (if this
            is allowed for the resulting chart type by the underlying visualization 
            library).
        """

        super().__init__(
            df_data, chart_metric, metadata, extra_args, zoomable)

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
        tooltip: list[alt.Tooltip],
        dim: Union[alt.Color, alt.Y],
    ) -> alt.Chart:
        """
        A function that creates a search component and adds it to the chart.

        Parameters
        ----------
        base_chart: alt.Chart
            The base chart object in which to add the search component.
        tooltip: list[alt.Tooltip]
            A list of alt.Tooltip objects.
        dim: Union[alt.Color, alt.Y]
            The alt.Color or alt.Y dimension to be filtered in the chart.

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
                dim,
                alt.value("")
            ),
            tooltip = tooltip
        )

        return base_chart


    def add_dropdown_components(
        self,
        base_chart: alt.Chart,
        tooltip: list[alt.Tooltip],
        dropdown_keys: list[str],
        dropdown_elements: list[list[str]],
        color: alt.Color,
        operation: str,
    ) -> alt.Chart:
        """
        A function that creates dropdown components and adds them to the chart.

        Parameters
        ----------
        base_chart: alt.Chart
            The base chart object in which to add the dropdown components.
        tooltip: list[alt.Tooltip]
            A list of alt.Tooltip objects.
        dropdown_keys: list[str]
            A list of keys corresponding to each dropdown.
        dropdown_elements: list[str[str]]
            A list of lists, each containing the values for each dropdown (1:1 with dropdown_keys).
        color: alt.Color
            The alt.Color dimension to be filtered in the chart.
        operation: str
            Whether the operation based on color is "fill", "color", or "opacity".

        Returns
        -------
        base_chart: alt.Chart
            The same base chart object with the dropdown components added.
        """

        # Create a list to store the dropdown objects
        dropdowns = []

        # Iterate over the dropdown keys to create a dropdown component with the given values
        for i in range(len(dropdown_keys)):
            # Get the label referring to the dropdown
            dropdown_label = self.text_label if (dropdown_keys[i] == "ngram") else dropdown_keys[i]

            # Create the dropdown component
            dropdown = alt.binding_select(
                options = sorted(
                    ["*Select " + str(dropdown_label) + "*"] + [str(el) for el in dropdown_elements[i]]), 
                name = f"Filter by {dropdown_label} ",
            )
            select = alt.selection_point(
                value = f"*Select {dropdown_label}*",
                bind = dropdown,
                fields = [dropdown_keys[i]],
            )

            # Add the dropdown component to the base chart
            base_chart = base_chart.add_params(select)
            base_chart = base_chart.transform_filter(select)

            # Add it to the list of dropdown component
            dropdowns.append(select)

        # Encoding the data by considering all the dropdown components and the operation
        if operation == "fill":
            base_chart = base_chart.encode(
                fill = alt.condition(
                    functools.reduce(operator.and_, dropdowns),
                    color,
                    alt.value("")
                ),
                tooltip = tooltip
            )
        elif operation == "color":
            base_chart = base_chart.encode(
                color = alt.condition(
                    functools.reduce(operator.and_, dropdowns),
                    color,
                    alt.value("")
                ),
                tooltip = tooltip
            )
        elif operation == "opacity":
            base_chart = base_chart.encode(
                color = alt.condition(
                    functools.reduce(operator.and_, dropdowns),
                    color,
                    alt.value("")
                ),
                opacity = alt.condition(
                    functools.reduce(operator.and_, dropdowns),
                    "value",
                    alt.value(0)
                ),
                tooltip = tooltip
            )
            base_chart = base_chart.configure_legend(disable=True)
        elif operation == "size":
            base_chart = base_chart.encode(
                color = alt.condition(
                    functools.reduce(operator.and_, dropdowns),
                    color,
                    alt.value("")
                ),
                size = alt.condition(
                    functools.reduce(operator.and_, dropdowns),
                    "value",
                    alt.value(0)
                ),
                tooltip = tooltip
            )
            base_chart = base_chart.configure_legend(disable=True)
        elif operation == "shape":
            base_chart = base_chart.encode(
                color = alt.condition(
                    functools.reduce(operator.and_, dropdowns),
                    color,
                    alt.value("")
                ),
                tooltip = tooltip
            )
            base_chart = base_chart.configure_legend(disable=True)
        else:
            raise ValueError(f"The operation \"{operation}\" is not envisioned.")

        return base_chart


    def get_dim(
        self,
        dim: Union[int, str],
        chart_dims: dict,
    ) -> (str, str):
        """
        A function that returns the name and (altair) type of a variable given a
        chart dimension and the previously stored variable names, types, and semantics.

        Parameters
        ----------
        dim: Union[int, str]
            The dimension of interest (e.g., "x", "y", "lat", "lon", "color", etc).
        chart_dims: dict
            The mapping dictionary for the variables of the given chart.

        Returns
        -------
        var_name: str
            The variable name referring to the dimension of interest.
        var_type_: str
            The (altair) variable type referring to the dimension of interest.
        """

        # Simultaneously order the lists referring to the variables
        var_types_ord, var_semantics_ord, var_names_ord = zip(
            *sorted(zip(self.var_types, self.var_semantics, self.var_names)))

        # Get the ordered list of variable names
        var_names = list(var_names_ord)

        # Get the variable name (from string or its index) and the (altair) type for plotting
        var_name = chart_dims[dim][0] if (type(chart_dims[dim][0])==str) else var_names[chart_dims[dim][0]]
        var_type_ = chart_dims[dim][1]

        # @TEMP workaround: Check for unwanted inversions
        if ("ordinal" in self.var_types) and ("quantitative" in self.var_types):
            if ("temporal" in self.var_semantics) and ("general" in self.var_semantics):
                index = 1 if chart_dims[dim][0] == 0 else 0
                var_name = chart_dims[dim][0] if (type(chart_dims[dim][0])==str) else var_names[index]
        
        return var_name, var_type_


    def save(
        self,
        output_folder: str,
        chart_name: str,
        output_formats: Optional[list[str]] = ["html"],
    ) -> None:
        """
        A function that saves the chart to a subfolder (with name matching the metric) 
        of the output folder in various formats.

        Parameters
        ----------
        output_folder: str
            A path to the output folder in which to save the chart.
        chart_name: str
            A name representing the chart object to be saved.
        output_formats: Optional[list[str]] = ["html"]
            A list of output formats for the charts. By default, only the interactive
            HTML chart is saved, i.e., ["html"]. Extra choices: ["pdf", "svg", "png"].
            Note that for very large datasets the extra choices are too heavy to build.
        """

        # If output formats have been specified, save the chart in those formats to 
        # subfolders (named as the metric) of the user-specified output folder
        if len(output_formats) >= 1:

            # Create the output folder if it does not exist
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)

            # Save the chart to an HTML file in the output folder
            if "html" in output_formats:
                output_filepath = os.path.join(output_folder, chart_name + ".html")
                print(f"INFO: Saving it to the filepath: \"{output_filepath}\".")
                self.chart.save(output_filepath)

            # Save the chart to a PDF file in the output folder
            if "pdf" in output_formats:
                try:
                    # Get the raw data from the chart (it requires "vl_convert" to be installed)
                    pdf_data = vlc.vegalite_to_pdf(self.chart.to_json())

                    # Write the raw data to the output filepath
                    output_filepath = os.path.join(output_folder, chart_name + ".pdf")
                    print(f"INFO: Saving it to the filepath: \"{output_filepath}\".")
                    with open(output_filepath, "wb") as f:
                        f.write(pdf_data)
                except Exception:
                    print("The dataset is too big to be serialized as PDF efficiently. Please "
                        "use the interactive HTML.")

            # Save the chart to a SVG file in the output folder
            if "svg" in output_formats:
                try:
                    # Get the raw data from the chart (it requires "vl_convert" to be installed)
                    svg_data = vlc.vegalite_to_svg(self.chart.to_json())

                    # Write the raw data to the output filepath
                    output_filepath = os.path.join(output_folder, chart_name + ".svg")
                    print(f"INFO: Saving it to the filepath: \"{output_filepath}\".")
                    with open(output_filepath, "wt") as f:
                        f.write(svg_data)
                except Exception:
                    print("The dataset is too big to be serialized as SVG efficiently. Please "
                        "use the interactive HTML.")

            # Save the chart to a PNG file in the output folder
            if "png" in output_formats:
                try:
                    # Get the raw data from the chart (it requires "vl_convert" to be installed)
                    png_data = vlc.vegalite_to_png(self.chart.to_json())

                    # Write the raw data to the output filepath
                    output_filepath = os.path.join(output_folder, chart_name + ".png")
                    print(f"INFO: Saving it to the filepath: \"{output_filepath}\".")
                    with open(output_filepath, "wb") as f:
                        f.write(png_data)
                except Exception:
                    print("The dataset is too big to be serialized as PNG efficiently. Please "
                        "use the interactive HTML.")

        # Otherwise, raise an error
        else:
            raise TypeError(f"ERROR: No output formats have been specified.")

