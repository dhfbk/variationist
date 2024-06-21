import altair as alt
import os
import pandas as pd
from typing import Any, Optional, Union

from variationist import utils
from variationist.visualization import chart_utils
from variationist.visualization.diversity_bar_chart import DiversityBarChart
from variationist.visualization.text_only_bar_chart import TextOnlyBarChart
from variationist.visualization.stats_bar_chart import StatsBarChart


class VisualizerArgs:
    """A class storing the arguments for the visualization component."""

    def __init__(
        self,
        output_folder: Optional[str] = None,
        output_formats: Optional[list[str]] = ["html"],
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
        output_folder: Optional[str] = None
            A path to the output folder in which to store the charts and associated
            metadata. If the folder does not exist, it will be automatically created.
            If no path is provided, the charts will not be serialized and the possible
            output_formats will be ignored (in this case, the chart objects will be only 
            accessible from the dictionary returned by the "create()" function and be
            shown by using the "show()" function.
        output_formats: Optional[list[str]] = ["html"]
            A list of output formats for the charts. By default, only the interactive
            HTML chart is saved, i.e., ["html"]. Extra choices: ["pdf", "svg", "png"].
        zoomable: Optional[bool] = True
            Whether the (HTML) chart should be zoomable using the mouse or not.
        top_per_class_ngrams: int = 20
            The maximum number of highest scoring per-class n-grams to show (for bar
            charts only). If set to None, it will show all the n-grams in the corpus 
            (it may easily be overwhelming). By default is 20 to keep the visualization 
            compact. This parameter is ignored when creating other chart types.
        ngrams: Optional[list[str]] = None
            A list of n-grams of interest to focus the resulting visualizations on.
            N-grams should match the number of tokens used in the prior computation
            reflected by the "results" variable (e.g., if unigrams were chosen, this
            list should only contain unigrams).
        shapefile_path: Optional[str] = None
            A path to the .shp shapefile to be visualized as background map to the chart
            (needed only when including a variable type "nominal" with "spatial" semantics.
            Note that auxiliary files to the .shp one (i.e., .dbf, .prg, .shx ones) are 
            required for chart creation too, but do not need to be specified. They should
            have the same name as the .shp file but different extension, and be located 
            in the same folder as the .shp file itself. An example of repository where to
            find shapefiles is https://geodata.lib.berkeley.edu/, but there exists many
            other ones and shapefiles provided by national/regional institutions.
        shapefile_var_name: Optional[str] = None
            The key field name in the shapefile which contains the names for the areas 
            which should match the possible values for the variable of interest (e.g., 
            if the variable of interest is "state", here should go the name of the
            variable name encoded in the shapefile containing the possible states).
        """
        
        self.output_folder = output_folder
        self.output_formats = output_formats
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
        self.variable_names = dict()
        self.variable_values = dict()

        # Load the json object storing metadata and results
        json_data = utils.load_json_data_from_filepath_or_dict(input_json)

        # Get the metadata and variable names from the json
        self.metadata = json_data["metadata"]
        self.variable_names = self.metadata["var_names"]

        # Handle case in which 2 text columns are provided (@TODO: Thoroughly test)
        if (len(self.metadata["text_names"]) == 2):
            if (len(self.variable_names) >= 1):
                self.variable_names.insert(0, "text_name")
                self.metadata["var_types"].insert(0, "nominal")
                self.metadata["var_semantics"].insert(0, "general")
                self.metadata["var_bins"].insert(0, 0)
            else:
                self.variable_names = ["text_name::"]

        # Get per-metric long-form dataframes from the json
        for metric in self.metadata["metrics"]:
            # Store the concatenated string useful for multiple variables
            var_names_concat = utils.MULTI_VAR_SEP.join(self.variable_names)

            if metric == "stats":
                # Retrieve the possible values for the variable (combination) and the given metric
                self.variable_values[metric] = list(
                    json_data["metrics"][metric]["num_texts"][var_names_concat].keys())

                # Get the long-form dataframe
                self.df_metric_data[metric] = self.get_stats_df_from_json(
                    json_data = json_data["metrics"][metric], 
                    var_names_concat = var_names_concat)

            else:
                # Retrieve the possible values for the variable (combination) and the given metric
                self.variable_values[metric] = list(
                    json_data["metrics"][metric][var_names_concat].keys())

                # Get the long-form dataframe
                self.df_metric_data[metric] = self.get_df_from_json(
                    json_data = json_data["metrics"][metric], 
                    var_names_concat = var_names_concat,
                    top_per_class_ngrams = self.args.top_per_class_ngrams,
                    focus_ngrams = self.args.ngrams)


    def get_df_from_json(
        self,
        json_data: dict[str, Any],
        var_names_concat: str,
        top_per_class_ngrams: int,
        focus_ngrams: Optional[list[str]] = None,
    ) -> pd.core.frame.DataFrame:
        """
        A function that returns a long-form dataframe from a json which 
        stores the information about a prior analysis using Variationist.
        Optionally, it takes a list of n-grams to focus the filtering on.

        Parameters
        ----------
        json_data: dict[str, Any]
            The json object storing the results from a prior analysis in the form:
            {varA: {ngram1: value1, ngram2: value2, ...}, varB: {...}, ...}. Note
            that varA, varB, etc. could also take the form of "::"-concatenated
            variable names if multiple variables are present in the analysis.
        var_names_concat: str
            A string denoting the ordered concatenation of variable names (i.e., 
            original column names), separated by utils.MULTI_VAR_SEP, to be used for 
            giving meaningful names to the long-form dataframe.
        top_per_class_ngrams: int = 20
            The maximum number of highest scoring per-class n-grams to show (for bar
            charts only). If set to None, it will show all the n-grams in the corpus 
            (it may easily be overwhelming). By default is 20 to keep the visualization 
            compact.
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
        variables, ngrams, values = dict(), [], []

        # Get the individual variables and initialize each of them
        var_names = var_names_concat.split(utils.MULTI_VAR_SEP)
        for var_name in var_names:
            variables[var_name] = []

        # Iterate through variable values and ngram-value pairs and keep those of interest
        for variable, raw_items in json_data[var_names_concat].items():
            for ngram, value in raw_items.items():
                if (focus_ngrams != None) and (ngram not in focus_ngrams):
                    continue
                else:
                    for i in range(len(var_names)):
                        variables[var_names[i]].append(str(variable).split(utils.MULTI_VAR_SEP)[i])
                    ngrams.append(ngram)
                    values.append(value)

        # Create the long-form dataframe
        dict_data = variables
        dict_data["ngram"] = ngrams
        dict_data["value"] = values
        df_data = pd.DataFrame(dict_data)
        
        return df_data


    def get_stats_df_from_json(
        self,
        json_data: dict[str, Any],
        var_names_concat: str,
    ) -> pd.core.frame.DataFrame:
        """
        A function that returns a long-form dataframe from a json which 
        stores the information about a prior analysis using Variationist.
        Optionally, it takes a list of n-grams to focus the filtering on.
        This is a variant of get_df_from_json() to handle basic stats.

        Parameters
        ----------
        json_data: dict[str, Any]
            The json object storing the results from a prior analysis in the form:
            {substatA: {colnameA: {varA: value1, ...}, ...}, substatB: {colnameA:
            {varA: {"mean": value, "stdev": value}, ...}, ...}, ...}. Note
            that varA, varB, etc. could also take the form of "::"-concatenated
            variable names if multiple variables are present in the analysis.
        var_names_concat: str
            A string denoting the ordered concatenation of variable names (i.e., 
            original column names), separated by utils.MULTI_VAR_SEP, to be used for 
            giving meaningful names to the long-form dataframe.

        Returns
        -------
        df_data: pd.core.frame.DataFrame
            A long-form dataframe storing the results of a prior analysis.
        """

        # Initialize the lists for variables, submetrics, and values
        variables, submetric_list, val_1_list, val_2_list = dict(), [], [], []

        # Get the individual variables and initialize each of them
        var_names = var_names_concat.split(utils.MULTI_VAR_SEP)
        for var_name in var_names:
            variables[var_name] = []

        # Iterate through the dictionary to create lists for creating the dataframe
        for submetric, vars_label_vals in json_data.items():
            for raw_vars, label_vals in vars_label_vals.items():
                for label, vals in label_vals.items():
                    is_vals_dict = (type(vals)==dict)
                    if is_vals_dict:
                        val_1, val_2 = vals["mean"], vals["stdev"]
                    else:
                        val_1, val_2 = vals, None

                    for i in range(len(var_names)):
                        variables[var_names[i]].append(str(label).split(utils.MULTI_VAR_SEP)[i])
                    submetric_list.append(submetric)
                    val_1_list.append(val_1)
                    val_2_list.append(val_2)

        # Create the long-form dataframe
        dict_data = variables
        dict_data["statistics"] = submetric_list
        dict_data["val_1"] = val_1_list
        dict_data["val_2"] = val_2_list
        df_data = pd.DataFrame(dict_data)

        return df_data


    def get_charts_metadata(
        self,
        metric: str,
    ) -> dict[str, Any]:
        """
        A function that returns a dictionary containing information on which and how to 
        create charts given prior analysis' var_types and var_semantics metadata.

        Parameters
        ----------
        metric: str
            The metric associated to the "df_data" dataframe and thus to the charts.

        Returns
        -------
        charts_metadata: dict[str, Any]
            A dictionary containing the chart types and information on how to create them.
        """

        # Get lists of attributes for variables
        var_names = self.metadata["var_names"]
        var_types = self.metadata["var_types"]
        var_semantics = self.metadata["var_semantics"]
        var_bins = self.metadata["var_bins"]

        # Double check the lengths of var_* (they must be the same)
        assert len(var_types) == len(var_semantics) == len(var_bins)

        # Skip if no variables have been defined (e.g., case 2 text columns only)
        if len(var_types) == 0:
            return {}

        # Check if there are variables and those are at maximum three
        if (1 <= len(var_types) <= 3):
            # Get the key for dimensions (the amount of dimensions equals to #variables+2)
            dims_key = str(len(var_types) + 2) + "-dims"

            # If there is only a variable, there is no need to order/join names, just take the values
            if len(var_types) == 1:
                var_types_key = var_types[0]
                var_semantics_key = var_semantics[0]
            # Otherwise, we need to create an ordered concatenation of variables for searching
            else:
                # If bins are used and the variable was originally quantitative, change it to nominal here
                as_nominal_idxs = []
                for i in range(len(var_types)):
                    if (var_types[i] == "quantitative") and (var_bins[i] != 0):
                        as_nominal_idxs.append(i)
                for as_nominal_idx in as_nominal_idxs:
                    var_types[as_nominal_idx] = "nominal"

                var_types_ord, var_semantics_ord = zip(*sorted(zip(var_types, var_semantics)))
                var_types_key = '-'.join([var_type for var_type in var_types_ord])
                var_semantics_key = '-'.join([var_semantics for var_semantics in var_semantics_ord])
            
            # Check if the variable type(s) are supported
            if var_types_key in chart_utils.VAR_CHARTS_MAP[dims_key]:
                # Check if the combination of the variable type(s) and semantics are supported
                # If yes, take the dictionary with chart building information
                if var_semantics_key in chart_utils.VAR_CHARTS_MAP[dims_key][var_types_key]:
                    charts_metadata = chart_utils.VAR_CHARTS_MAP[dims_key][var_types_key][var_semantics_key]
                # Otherwise, raise an error
                else:
                    raise ValueError(
                        f"Visualization for \"{var_types_key}\" variable type(s) and \"{var_semantics_key}\" "
                        f"variable semantics is currently not supported. If you have any idea to effectively "
                        f"visualize such combination of types and semantics, we would be happy if you let us "
                        f"know by opening an issue at: https://github.com/dhfbk/variationist/issues.")
            # Otherwise, raise an error
            else:
                raise ValueError(
                    f"Visualization for \"{var_type_key}\" variable type(s) is not supported.")

        # Otherwise, raise an error
        else:
            raise ValueError(
                f"Visualization for {len(var_types)} variable types is not supported yet.")
        
        return charts_metadata


    def create(
        self,
    ) -> dict[str, list[alt.Chart]]:
        """
        A function that orchestrates the creation of charts based on the results
        and metadata from a prior analysis using Variationist, returning a dictionary 
        of metrics (keys) and an associated list of alt.Chart objects (values).

        Returns
        -------
        charts: dict[str, list[alt.Chart]]
            A dictionary containing the metrics as keys and a list of chart objects
            as values.
        """

        # A dictionary holding the chart objects to be returned to the user
        # This is especially useful when the user would show the chart in a notebook
        charts = {}

        # Create a dictionary of chart-specific arguments
        extra_args = {}
        if self.args.shapefile_path != None:
            extra_args["shapefile_path"] = self.args.shapefile_path
        if self.args.shapefile_var_name != None:
            extra_args["shapefile_var_name"] = self.args.shapefile_var_name

        # Build chart objects for each computed metric based on variable types and
        # semantics, then save them to the user-specified output folder
        for metric, df_data in self.df_metric_data.items():
            charts[metric] = dict()

            if metric == "stats":
                # Create the chart object
                print(f"INFO: Creating a BarChart object for metric \"{metric}\"...")
                chart = StatsBarChart(
                    df_data, metric, self.metadata, extra_args, {}, 
                    self.args.zoomable, self.args.top_per_class_ngrams
                )

                # Save the chart to the output folder
                if self.args.output_folder != None:
                    output_filepath = os.path.join(self.args.output_folder, metric)
                    chart.save(output_filepath, "StatsBarChart", self.args.output_formats)

                # Add the chart to the dictionary of metric-associated charts
                charts[metric]["BarChart"] = chart.base_chart

            elif metric in ["ttr", "root_ttr", "log_ttr", "maas"]:
                # Create the chart object
                print(f"INFO: Creating a BarChart object for metric \"{metric}\"...")
                chart = DiversityBarChart(
                    df_data, metric, self.metadata, extra_args, {}, 
                    self.args.zoomable, self.args.top_per_class_ngrams
                )

                # Save the chart to the output folder
                if self.args.output_folder != None:
                    output_filepath = os.path.join(self.args.output_folder, metric)
                    chart.save(output_filepath, "DiversityBarChart", self.args.output_formats)

                # Add the chart to the dictionary of metric-associated charts
                charts[metric]["BarChart"] = chart.base_chart

            else:
                # Get dictionary containing information on which and how to create charts
                charts_metadata = self.get_charts_metadata(metric)

                if len(self.metadata["var_types"]) == 0:
                    print(f"INFO: Creating a BarChart object for metric \"{metric}\"...")
                    chart = TextOnlyBarChart(
                        df_data, metric, self.metadata, extra_args, {}, 
                        self.args.zoomable, self.args.top_per_class_ngrams
                    )
                            
                    # Save the chart to the output folder
                    if self.args.output_folder != None:
                        output_filepath = os.path.join(self.args.output_folder, metric)
                        chart.save(output_filepath, "BarChart", self.args.output_formats)

                        # Add the chart to the dictionary of metric-associated charts
                        charts[metric]["BarChart"] = chart.base_chart
                else:
                    # Iterate over the results and create and save charts based on these information
                    charts_count = 0
                    for ChartClass, chart_info in charts_metadata.items():
                        # Check if at least a variable has bins defined
                        no_bins = all(var_bin == 0 for var_bin in self.metadata["var_bins"])

                        # Create only the subset of charts based on bins definition
                        if (chart_info["for_bins"] == "any") or (no_bins and (chart_info["for_bins"] == False)) or ((no_bins == False) and (chart_info["for_bins"] == True)):
                            # Create the chart object
                            print(f"INFO: Creating a {ChartClass.__name__} object for metric \"{metric}\"...")
                            chart = ChartClass(
                                df_data, metric, self.metadata, extra_args, chart_info, 
                                self.args.zoomable, self.args.top_per_class_ngrams
                            )
                            
                            # Save the chart to the output folder
                            if self.args.output_folder != None:
                                output_filepath = os.path.join(self.args.output_folder, metric)
                                chart.save(output_filepath, ChartClass.__name__, self.args.output_formats)

                            # Add the chart to the dictionary of metric-associated charts
                            charts[metric][ChartClass.__name__] = chart.base_chart

                            charts_count += 1

                    if charts_count == 0:
                        print(f"No visualization is currently supported for the association metric(s) defined, but you can find the results in the output .json file.")

        return charts
