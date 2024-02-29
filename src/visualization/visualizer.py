import json
import os
import pandas as pd

from typing import Any, Optional, Union

from chart import Chart


def visualize(
    input_json: Union[str, dict],
    output_folder: str,
    filterable: Optional[bool] = True,
    zoomable: Optional[bool] = True,
    ngrams: Optional[list[str]] = None,
    output_formats: Optional[list[str]] = ["html"],
) -> None:
    """
    A function that orchestrates the creation of charts based on the results
    and metadata from a prior analysis using Variationist. It optionally
    takes extra parameters to customize the ngrams to be shown.

    Parameters
    ----------
    input_json: Union[str, dict]
        A path to the json file or a json/dict object storing metadata and results 
        from a prior analysis using Variationist.
    output_folder: str
        A path to the output folder in which to store the charts and associated
        metadata. If the folder does not exist, it will be automatically created.
    filterable: Optional[bool] = True
        Whether the charts should be searchable by using regexes on ngrams or not.
    zoomable: Optional[bool] = True
        Whether the (HTML) chart should be zoomable using the mouse or not.
    ngrams: Optional[list[str]] = None
        A list of n-grams of interest to focus the resulting visualizations on.
        N-grams should match the number of tokens used in the prior computation
        reflected by the "results" variable (e.g., if unigrams were chosen, this
        list should only contain unigrams).
    output_formats: Optional[list[str]] = ["html"]
        A list of output formats for the charts. By default, only the interactive
        HTML chart is saved, i.e., ["html"]. Extra choices: ["pdf", "svg", "png"].
    """

    # Load the json object storing metadata and results
    json_data = load_json_data(input_json)

    # Get the metadata and per-metric long-form dataframes from the json
    metadata = json_data["metadata"]
    df_metric_data = dict()
    for metric in metadata["metrics"]:
        df_metric_data[metric] = get_df_from_json(
            json_data = json_data["metrics"][metric], 
            var_names = metadata["var_names"],
            focus_ngrams = ngrams)

    # Build a chart object for each computed metric based on variable types and
    # semantics, then save it to the user-specified output folder
    for metric, df_data in df_metric_data.items():
        # @TODO: Orchestrate the creation of charts

        # Create the chart object
        chart = Chart(df_data, metric, metadata, filterable, zoomable)

        # Save the chart to the output folder
        chart.save(output_folder, output_formats)


def load_json_data(
    input_json: Union[str, dict],
) -> dict:
    """
    A function that loads the json/dict object from either a user-defined json 
    filepath or a dict variable (in the latter case, it returns the dict itself).

    Parameters
    ----------
    input_json: Union[str, dict]
        A path to the json file or a json/dict object storing metadata and results 
        from a prior analysis using Variationist.

    Returns
    -------
    json_data: dict
        A json/dict object storing metadata and results of a prior analysis.
    """

    # If the input is a json filepath, read it and store it
    if type(input_json) == str:
        print(f"Loading json data from the filepath \"{input_json}\"...")
        json_data = json.load(open(input_json))
    # If the input is already a json/dict object, use it
    elif type(input_json) == dict:
        print(f"Reading json data...")
        json_data = input_json
    # Otherwise, raise an error
    else:
        raise TypeError(f"ERROR: The input should be a json object or a json filepath.")
    
    return json_data


def get_df_from_json(
    json_data: dict[str, Any],
    var_names: list,
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
    var_names: list
        A list of variable names (i.e., original column names) to be used for
        giving meaningful names to the long-form dataframe.
    fucus_ngrams: Optional[list[str]] = None
        A list of n-grams of interest to focus the filtering on. N-grams should 
        match the number of tokens used in the prior computation (e.g., if 
        unigrams were chosen, this list should only contain unigrams).

    Returns
    -------
    df_data: pd.core.frame.DataFrame
        A long-form dataframe storing the results of a prior analysis.
    """

    # Initialize the lists for variables, ngrams, and values
    variables, ngrams, values = [], [], []

    # Get a machine-readable name for the variable(s) under consideration
    variable_key = " ".join(var_names)

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
        variable_key: variables,
        "ngram": ngrams,
        "value": values
    })
    
    return df_data


if __name__ == "__main__":
    # Run the visualization test
    visualize(
        input_json=os.path.join("data", "output.json"), # or: json.load(open("example-time.json"))
        output_folder="my-charts",
        filterable=True,
        zoomable=True,
        ngrams=None,
        output_formats=["html"])
