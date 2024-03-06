import os
import pandas as pd

from typing import Any, Optional, Union

from src import utils
from src.visualization.bar_chart import BarChart
from src.visualization.temporal_line_chart import TemporalLineChart
from src.visualization.scatter_chart import ScatterChart
from src.visualization.choropleth_chart import ChoroplethChart


# @TODO: Maybe change the "ngrams" name for clarity across the script (it supports cooccs, too!)
# @TODO: Also redifine/change/remove top_per_class_ngrams


class VisualizerArgs:
    """A class storing the arguments for the visualization component."""

    def __init__(
        self,
        output_folder: str,
        output_formats: Optional[list[str]] = ["html"],
        filterable: Optional[bool] = True,
        zoomable: Optional[bool] = True,
        top_per_class_ngrams: Optional[int] = 20,
        ngrams: Optional[list[str]] = None,
        shapefile_path: Optional[str] = None,
        shapefile_var_name: Optional[str] = None,
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
        top_per_class_ngrams: int = 20
            The maximum number of highest scoring per-class n-grams to show. If set to 
            None, it will show all the ngrams in the corpus (it may easily be 
            overwhelming). By default is 20 to keep the visualization compact.
        ngrams: Optional[list[str]] = None
            A list of n-grams of interest to focus the resulting visualizations on.
            N-grams should match the number of tokens used in the prior computation
            reflected by the "results" variable (e.g., if unigrams were chosen, this
            list should only contain unigrams).
        shapefile_path: Optional[str] = None
            A path to the .shp shapefile to be visualized as background map to the chart.
            Note that auxiliary files to the .shp one (i.e., .dbf, .prg, .shx ones) are 
            required for chart creation too, but do not need to be specified. They should
            have the same name as the .shp file but different extension, and be located 
            in the same folder as the .shp file itself.
        shapefile_var_name: Optional[str] = None
            The key field name in the shapefile which contains the names for the areas 
            which should match the possible values for the variable of interest (e.g., 
            if the variable of interest is "state", here should go the name of the
            variable name encoded in the shapefile containing the possible states).
        """
        
        self.output_folder = output_folder
        self.output_formats = output_formats
        self.filterable = filterable
        self.zoomable = zoomable
        self.top_per_class_ngrams = top_per_class_ngrams
        self.ngrams = ngrams
        self.shapefile_path = shapefile_path
        self.shapefile_var_name = shapefile_var_name


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
        self.variable_values = dict()

        # Load the json object storing metadata and results
        json_data = utils.load_json_data_from_filepath_or_dict(input_json)

        # Get the metadata and per-metric long-form dataframes from the json
        self.metadata = json_data["metadata"]
        for metric in self.metadata["metrics"]:
            self.variable_values[metric] = list(json_data["metrics"][metric].keys())
            self.df_metric_data[metric] = self.get_df_from_json(
                json_data = json_data["metrics"][metric], 
                var_names = self.metadata["var_names"],
                top_per_class_ngrams = self.args.top_per_class_ngrams,
                focus_ngrams = self.args.ngrams)


    def get_df_from_json(
        self,
        json_data: dict[str, Any],
        var_names: list,
        top_per_class_ngrams: int,
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
        top_per_class_ngrams: int = 20
            The maximum number of highest scoring per-class n-grams to show. If set to 
            None, it will show all the ngrams in the corpus (it may easily be 
            overwhelming). By default is 20 to keep the visualization compact.
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

        # Iterate through variables and ngram-value pairs and keep those of interest
        for variable, raw_items in json_data.items():
            if self.args.top_per_class_ngrams != None:
                raw_top_k = sorted(
                    raw_items.items(), key=lambda x:x[1], reverse=True)[:self.args.top_per_class_ngrams]
                ngrams_top_k = [element[0] for element in raw_top_k]
            for ngram, value in raw_items.items():
                if (focus_ngrams != None) and (ngram not in focus_ngrams):
                    continue
                else:
                    if ((self.args.top_per_class_ngrams != None) and (ngram in ngrams_top_k)) or (self.args.top_per_class_ngrams == None): 
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
            # @TODO: Differentiate chart creation by metric
            # @TODO: Add error messages for chart-specific parameters

            if (len(self.metadata["var_types"]) == 1):
                var_type = self.metadata["var_types"][0]
                var_semantics = self.metadata["var_semantics"][0]

                if var_type == "nominal":
                    if var_semantics == "general":
                        # Create a bar chart object
                        chart = BarChart(
                            df_data, metric, self.metadata, self.args.filterable, self.args.zoomable,
                            self.variable_values[metric], self.args.top_per_class_ngrams)
                        # Save the chart to the output folder
                        chart.save(os.path.join(
                            self.args.output_folder, "bar_chart"), self.args.output_formats)
                    elif var_semantics == "spatial":
                        # Create a bar chart object
                        chart = BarChart(
                            df_data, metric, self.metadata, self.args.filterable, self.args.zoomable,
                            self.variable_values[metric], self.args.top_per_class_ngrams)
                        # Save the chart to the output folder
                        chart.save(os.path.join(
                            self.args.output_folder, "bar_chart"), self.args.output_formats)
                        # Create a choropleth map chart object
                        chart = ChoroplethChart(
                            df_data, metric, self.metadata, self.args.filterable, self.args.zoomable,
                            self.variable_values[metric], self.args.top_per_class_ngrams,
                            self.args.shapefile_path, self.args.shapefile_var_name)
                        # Save the chart to the output folder
                        chart.save(os.path.join(
                            self.args.output_folder, "choropleth_chart"), self.args.output_formats)
                    else:
                        # @TODO: Indications of which var_type / var_semantics should be
                        raise ValueError(
                            f"Visualization for variable type {var_type} ({var_semantics}) is not supported.")
                elif var_type == "ordinal":
                    if var_semantics == "general":
                        # Create a bar chart object
                        chart = BarChart(
                            df_data, metric, self.metadata, self.args.filterable, self.args.zoomable,
                            self.variable_values[metric], self.args.top_per_class_ngrams)
                        # Save the chart to the output folder
                        chart.save(os.path.join(
                            self.args.output_folder, "bar_chart"), self.args.output_formats)
                    elif var_semantics == "temporal":
                        # Create a bar chart object
                        # Create a temporal line chart object
                        chart = TemporalLineChart(
                            df_data, metric, self.metadata, self.args.filterable, self.args.zoomable,
                            self.variable_values[metric], self.args.top_per_class_ngrams)
                        # Save the chart to the output folder
                        chart.save(os.path.join(
                            self.args.output_folder, "temporal_line_chart"), self.args.output_formats)
                    else:
                        # @TODO: Indications of which var_type / var_semantics should be
                        raise ValueError(
                            f"Visualization for variable type {var_type} ({var_semantics}) is not supported.")
                elif var_type == "quantitative":
                    if var_semantics == "general":
                        # Create a scatteplot chart object
                        chart = ScatterChart(
                            df_data, metric, self.metadata, self.args.filterable, self.args.zoomable,
                            self.variable_values[metric], self.args.top_per_class_ngrams)
                        # Save the chart to the output folder
                        chart.save(os.path.join(
                            self.args.output_folder, "scatter_chart"), self.args.output_formats)
                    else:
                        # @TODO: Indications of which var_type / var_semantics should be
                        raise ValueError(
                            f"Visualization for variable type {var_type} ({var_semantics}) is not supported.")
                elif var_type == "coordinates":
                    if var_semantics == "general":
                        # Create a scatteplot (?) chart object
                        raise NotImplementedError(
                            f"Visualization for variable type {var_type} ({var_semantics}) is not supported yet.")
                    elif var_semantics == "spatial":
                        # Create a hexbin mapbox (?) chart object
                        # Create a mapbox density heatmap chart object
                        raise NotImplementedError(
                            f"Visualization for variable type {var_type} ({var_semantics}) is not supported yet.")
                    else:
                        # @TODO: Indications of which var_type / var_semantics should be
                        raise ValueError(
                            f"Visualization for variable type {var_type} ({var_semantics}) is not supported.")
                else:
                    raise ValueError(f"ERROR. {var_type} is not supported.")
            else:
                raise NotImplementedError(
                        f"Visualization for >=1 variable types is not supported yet.")


if __name__ == "__main__":
    pass
    
    # # Define the visualizer arguments
    # visualizer_args = VisualizerArgs(
    #     output_folder="results", output_formats=["html"], filterable=True, zoomable=True, top_per_class_ngrams=20, ngrams=None)

    # # Create dynamic visualizations of the results
    # Visualizer(
    #     input_json=os.path.join("data", "worthit_topic.json"), # or: json.load(open("example-time.json"))
    #     args=visualizer_args
    # ).visualize()
