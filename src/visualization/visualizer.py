import altair as alt
import json
import os
import pandas as pd
import vl_convert as vlc

from typing import Any, Optional


def visualize(
    input_filepath: str,
    output_folder: str,
    filterable: Optional[bool] = True,
    ngrams: Optional[list[str]] = None,
    save_to_pdf: Optional[bool] = False,
) -> None:
    """
    A function that orchestrates the creation of charts based on the results
    and metadata from a prior analysis using Variationist. It optionally
    takes extra parameters to customize the ngrams to be shown.

    Parameters
    ----------
    input_filepath: str
        A path to the .json file storing metadata and results from a prior 
        analysis using Variationist.
    output_folder: str
        A path to the output folder in which to store the charts and associated
        metadata. If the folder does not exist, it will be automatically created.
    filterable: bool = True
        Whether the charts should be searchable by using regexes on ngrams or not.
    ngrams: Optional[list[str]] = None
        A list of n-grams of interest to focus the resulting visualizations on.
        N-grams should match the number of tokens used in the prior computation
        reflected by the "results" variable (e.g., if unigrams were chosen, this
        list should only contain unigrams).
    save_to_pdf: bool = False
        Whether or not to save the figures as a PDF files in addition to HTML files.
    """

    # Load the json object from the input filepath
    json_data = json.load(open(input_filepath))

    # Get the metadata and per-metric long-form dataframes from the json
    metadata = json_data["metadata"]
    df_metric_data = dict()
    for metric in metadata["metrics"]:
        df_metric_data[metric] = get_df_from_json(
            json_data = json_data["metrics"][metric], 
            focus_ngrams = ngrams)

    # Create a chart for each computed metric
    for metric, df_data in df_metric_data.items():

        # If the chart has to be filterable, define a search component
        if filterable == True:
            search_input = alt.param(
                value = "",
                bind = alt.binding(
                    input = "search",
                    placeholder = "insert ngram...",
                    name = "Filter by ngram ",
                )
            )

        #####################################################################
        # WIP-START. @TODO: Generalize chart creation based on input metadata
        #####################################################################

        # Create the base chart object which stores the data
        base_chart = alt.Chart(df_data).mark_line(point=True).encode(
            alt.X("$VAR:T"),
            alt.Y("value:Q"),
            alt.Color("ngram:N"),
            alt.Tooltip("ngram:N"), # @TODO: Make it work on line plots
        )

        # Add the filtering option to the chart
        if filterable == True:
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
        chart = base_chart

        #####################################################################
        # WIP-END.
        #####################################################################

        # Create the output folder if it does not exist
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # Save the chart to an HTML file in the output folder
        chart.save(os.path.join(output_folder, "chart-" + metric + ".html"))

        # Optionally, save the chart to a PDF file in the output folder
        if save_to_pdf == True:
            save_chart_to_pdf(chart, output_folder, metric)


def get_df_from_json(
    json_data: dict[str, Any],
    focus_ngrams: Optional[list[str]] = None,
) -> pd.core.frame.DataFrame:
    """
    A method that returns a long-form dataframe from a json which 
    stores the information about a prior analysis using Variationist.
    Optionally, it takes a list of ngrams to focus the filtering on.

    Parameters
    ----------
    json_data: dict[str, Any]
        The json object storing the results from a prior analysis in the form:
        {varA: {ngram1: value1, ngram2: value2, ...}, varB: {...}, ...}
    fucus_ngrams: Optional[list[str]] = None
        A list of n-grams of interest to focus the filtering on. N-grams should 
        match the number of tokens used in the prior computation (e.g., if 
        unigrams were chosen, this list should only contain unigrams).

    Returns
    -------
    pd.core.frame.DataFrame
        A long-form dataframe storing the results of a prior analysis.
    """

    # Initialize the lists for variables, ngrams, and values
    variables, ngrams, values = [], [], []

    # Iterate over the json content to store items
    for variable, raw_items in json_data.items():
        for ngram, value in raw_items.items():
            if (focus_ngrams != None) and (ngram not in focus_ngrams):
                continue
            else:
                variables.append(variable)
                ngrams.append(ngram)
                values.append(value)

    # Create the long-form dataframe
    df_data = pd.DataFrame({
        "$VAR": variables, # @TODO: Get the original / define a general name for the variable
        "ngram": ngrams,
        "value": values
    })
    
    return df_data


def save_chart_to_pdf(
    chart: alt.Chart,
    output_folder: str,
    metric: str,
) -> None:
    """
    Parameters
    ----------
    chart: alt.Chart
        A chart object to be saved to a PDF file
    output_folder: str
        A path to the output folder in which to save the chart as a PDF file.
    metric: str
        The metric associated to the chart (for setting the correct filename).
    """

    # Get the raw data from the chart (it requires "vl_convert" to be installed)
    pdf_data = vlc.vegalite_to_pdf(chart.to_json())

    # Write the raw data to the output filepath
    with open(os.path.join(output_folder, "chart-" + metric + ".pdf"), "wb") as f:
        f.write(pdf_data)


if __name__ == "__main__":
    # Run the visualization test
    visualize(
        input_filepath="example-time.json", 
        output_folder="my-charts",
        filterable=True,
        ngrams=None,
        save_to_pdf=True)
