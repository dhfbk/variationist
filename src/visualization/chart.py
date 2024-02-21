import altair as alt
import os
import pandas as pd
import vl_convert as vlc

from typing import Optional


class Chart:
    """A base class for building an alt.Chart chart object."""

    def __init__(
        self,
        df_data: pd.core.frame.DataFrame,
        chart_metric: str,
        filterable: Optional[bool] = True,
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
        filterable: Optional[bool] = True
            Whether the chart should be searchable by using regexes on ngrams or not.
        """

        self.df_data = df_data
        self.chart_metric = chart_metric
        self.filterable = filterable
        self.chart = None

        #####################################################################
        # WIP-START. @TODO: Generalize chart creation based on input metadata
        #####################################################################

        # If the chart has to be filterable, define a search component
        if self.filterable == True:
            search_input = alt.param(
                value = "",
                bind = alt.binding(
                    input = "search",
                    placeholder = "insert ngram...",
                    name = "Filter by ngram ",
                )
            )

        # Create the base chart object which stores the data
        base_chart = alt.Chart(self.df_data).mark_line(point=True, tooltip=True)

        # Create dimensions
        x_dim = alt.X("date", type="temporal")
        y_dim = alt.Y("value", type="quantitative") # value: always "quantitative"
        color_dim = alt.Color("ngram", type="nominal")

        # Extra attributes
        _tooltip = alt.Tooltip("ngram", type="nominal")

        # Encoding data
        base_chart = base_chart.encode(
            x_dim,
            y_dim,
            color_dim,
            _tooltip
        )

        # If the chart has to be filterable, add the filtering option
        if self.filterable == True:
            base_chart = base_chart.encode(
                opacity=alt.condition(
                    alt.expr.test(alt.expr.regexp(search_input, 'i'), alt.datum.ngram),
                    alt.value(1),
                    alt.value(0.05)
                )
            )
            base_chart = base_chart.add_params(search_input)

        # Set extra properties
        base_chart = base_chart.properties(width=1200).interactive()

        # Create the final chart
        self.chart = base_chart

        #####################################################################
        # WIP-END.
        #####################################################################


    def save(
        self,
        output_folder: str,
        output_formats: Optional[list[str]] = ["html"],
    ) -> None:
        """
        A function that saves the chart to the output folder in various formats.

        Parameters
        ----------
        output_folder: str
            A path to the output folder in which to save the chart.
        output_formats: Optional[list[str]] = ["html"]
            A list of output formats for the charts. By default, only the interactive
            HTML chart is saved, i.e., ["html"]. Extra choices: ["pdf", "svg", "png"].
        """

        # If output formats have been specified, save the chart in those formats to 
        # the user-specified output folder
        if len(output_formats) >= 1:
            # Set the base filename for the chart
            BASE_FILENAME = os.path.join(output_folder, "chart-" + self.chart_metric)

            # Create the output folder if it does not exist
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)

            # Save the chart to an HTML file in the output folder
            if "html" in output_formats:
                self.chart.save(os.path.join(BASE_FILENAME + ".html"))

            # Save the chart to a PDF file in the output folder
            if "pdf" in output_formats:
                # Get the raw data from the chart (it requires "vl_convert" to be installed)
                pdf_data = vlc.vegalite_to_pdf(self.chart.to_json())

                # Write the raw data to the output filepath
                with open(os.path.join(BASE_FILENAME + ".pdf"), "wb") as f:
                    f.write(pdf_data)

            # Save the chart to a SVG file in the output folder
            if "svg" in output_formats:
                # Get the raw data from the chart (it requires "vl_convert" to be installed)
                svg_data = vlc.vegalite_to_svg(self.chart.to_json())

                # Write the raw data to the output filepath
                with open(os.path.join(BASE_FILENAME + ".svg"), "wt") as f:
                    f.write(svg_data)

            # Save the chart to a PNG file in the output folder
            if "png" in output_formats:
                # Get the raw data from the chart (it requires "vl_convert" to be installed)
                png_data = vlc.vegalite_to_png(self.chart.to_json())

                # Write the raw data to the output filepath
                with open(os.path.join(BASE_FILENAME + ".png"), "wb") as f:
                    f.write(png_data)

        # Otherwise, raise an error
        else:
            raise TypeError(f"ERROR: No output formats have been specified.")