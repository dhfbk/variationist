import os
import pandas as pd

from typing import Any, Optional, Union

from src import utils
from src.visualization.chart import Chart


# @TODO: Maybe change the "ngrams" name for clarity across the script (it supports cooccs, too!)


class VisualizerArgs:
    """A class storing the arguments for the visualization component."""

    def __init__(
        self,
        output_folder: str,
        output_formats: Optional[list[str]] = ["html"],
        filterable: Optional[bool] = True,
        zoomable: Optional[bool] = True,
        criterion: Optional[str] = "top-k-per-var",
        ngrams: Optional[list[str]] = None,
    ) -> None:
        """
        A function that initializes the arguments useful for visualizing charts.

        Parameters
        ----------
        output_folder: str
            A path to the output folder in which to store the charts and associated
            metadata. If the folder does not exist, it will be automatically created.
        output_formats: Optional[list[str]] = ["html"]
            A list of output formats for the charts. By default, only the interactive
            HTML chart is saved, i.e., ["html"]. Extra choices: ["pdf", "svg", "png"].
        filterable: Optional[bool] = True
            Whether the charts should be searchable by using regexes on ngrams or not.
        zoomable: Optional[bool] = True
            Whether the (HTML) chart should be zoomable using the mouse or not.
        criterion: str = "top-k-per-var"
            The criterion that determines how many n-grams to show. If set to None, it 
            will show all the tokens in the corpus (it may easily be overwhelming).
            Choices are: ["top-k-per-var"]. By default, it is "top-k-per-var". Note
            that the value k is automatically determined based on the total number of 
            variables, to keep the visualization compact (max 100 ngrams): k=100/|C|
        ngrams: Optional[list[str]] = None
            A list of n-grams of interest to focus the resulting visualizations on.
            N-grams should match the number of tokens used in the prior computation
            reflected by the "results" variable (e.g., if unigrams were chosen, this
            list should only contain unigrams).
        """
        
        self.output_folder = output_folder
        self.output_formats = output_formats
        self.filterable = filterable
        self.zoomable = zoomable
        self.criterion = criterion
        self.ngrams = ngrams


class Visualizer:
    """A class for the visualization component. It orchestrates the creation of charts 
    based on the results and metadata from a prior analysis using Variationist."""

    def __init__(
        self,
        input_json: Union[str, dict],
        args: VisualizerArgs,
    ) -> None:
        """
        A function that initializes the arguments of the visualizer, the metadata, and
        the per-metric long-form dataframes that will be used for visualization.

        Parameters
        ----------
        input_json: Union[str, dict]
            A path to the json file or a json/dict object storing metadata and results 
            from a prior analysis using Variationist.
        args: VisualizerArgs
            A VisualizerArgs object containing the arguments for the Visualizer
        """

        # Store the visualizer arguments
        self.args = args
        self.metadata = dict()
        self.df_metric_data = dict()

        # Load the json object storing metadata and results
        json_data = utils.load_json_data_from_filepath_or_dict(input_json)

        # Get the metadata and per-metric long-form dataframes from the json
        self.metadata = json_data["metadata"]
        for metric in self.metadata["metrics"]:
            self.df_metric_data[metric] = self.get_df_from_json(
                json_data = json_data["metrics"][metric], 
                var_names = self.metadata["var_names"],
                criterion = self.args.criterion,
                focus_ngrams = self.args.ngrams)


    def get_df_from_json(
        self,
        json_data: dict[str, Any],
        var_names: list,
        criterion: str,
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
        criterion: str = "top-k-per-var"
            The criterion that determines how many n-grams to show. If set to None, it 
            will show all the tokens in the corpus (it may easily be overwhelming).
            Choices are: ["top-k-per-var"]. By default, it is "top-k-per-var". Note
            that the value k is automatically determined based on the total number of 
            variables, to keep the visualization compact (max 100 ngrams): k=100/|C|
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

        # If a criterion is defined, get a set of ngrams to show
        top_elements = set()
        if criterion == "top-k-per-var":
            k = round(100 / len(json_data.keys()))
            for variable, raw_items in json_data.items():
                raw_top_k = sorted(raw_items.items(), key=lambda x:x[1], reverse=True)[:k]
                ngrams_top_k = [element[0] for element in raw_top_k]
                top_elements.update(ngrams_top_k)

        # Iterate over the json content to store items
        for variable, raw_items in json_data.items():
            for ngram, value in raw_items.items():
                if (focus_ngrams != None) and (ngram not in focus_ngrams):
                    continue
                else:
                    if ((criterion == "top-k-per-var") and (ngram in top_elements)) or (criterion == None): 
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


    def visualize(
        self,
    ) -> None:
        """
        A function that orchestrates the creation of charts based on the results
        and metadata from a prior analysis using Variationist.
        """

        # Build a chart object for each computed metric based on variable types and
        # semantics, then save it to the user-specified output folder
        for metric, df_data in self.df_metric_data.items():

            # Create the chart object
            chart = Chart(df_data, metric, self.metadata, self.args.filterable, self.args.zoomable)

            # Save the chart to the output folder
            chart.save(self.args.output_folder, self.args.output_formats)


if __name__ == "__main__":
    # Define the visualizer arguments
    visualizer_args = VisualizerArgs(
        output_folder="results", output_formats=["html"], filterable=True, zoomable=True, ngrams=None)

    # Create dynamic visualizations of the results
    Visualizer(
        input_json=os.path.join("data", "worthit_topic.json"), # or: json.load(open("example-time.json"))
        args=visualizer_args
    ).visualize()
