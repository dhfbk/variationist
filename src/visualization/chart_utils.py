from src.visualization.bar_chart import BarChart
from src.visualization.temporal_line_chart import TemporalLineChart
from src.visualization.scatter_chart import ScatterChart
from src.visualization.choropleth_chart import ChoroplethChart
from src.visualization.scatter_geo_chart import ScatterGeoChart
# from src.visualization.density_geo_chart import DensityGeoChart


# Definition of variable types and semantics and their mapping to charts, including
# how single variables should be presented and filtered. Note: var_types for > 3 
# dimensions are lexicographically-ordered, and var_semantics are ordered accordingly
VAR_CHARTS_MAP = {
    "3-dims": {
        "coordinates": {
            "general": {
                ScatterChart: {
                    "x": 0,
                    "y": "value",
                    "dropdown": [],
                    "search": ["ngram"]
                },
            },
        },
        "nominal": {
            "general": {
                BarChart: {
                    "x": "value",
                    "y": "ngram",
                    "column": 0,
                    "dropdown": [],
                    "search": ["ngram"]
                },
            },
            "spatial": {
                BarChart: {
                    "x": "value",
                    "y": "ngram",
                    "column": 0,
                    "dropdown": [],
                    "search": ["ngram"]
                },
                ChoroplethChart: {
                    "color": 0,
                    "dropdown": ["ngram"],
                    "search": []
                },
            },
        },
        "ordinal": {
            "general": {
                BarChart: {
                    "x": "value",
                    "y": "ngram",
                    "column": 0,
                    "dropdown": [],
                    "search": ["ngram"]
                },
            },
            "temporal": {
                TemporalLineChart: {
                    "x": 0,
                    "y": "value",
                    "dropdown": [],
                    "search": ["ngram"]
                },
            },
        },
        "quantitative": {
            "general": {
                ScatterChart: {
                    "x": 0,
                    "y": "value",
                    "dropdown": [],
                    "search": ["ngram"]
                },
            },
        },
    },
    "4-dims": {
        "coordinates-coordinates": {
            "general-general": {
                ScatterChart: {
                    "x": 0,
                    "y": "value",
                    "dropdown": [],
                    "search": ["ngram"]
                },
            },
            "spatial-spatial": {
                ScatterGeoChart: {
                    "lat": 0,
                    "lon": 1,
                    "color": "value",
                    "dropdown": [],
                    "search": ["ngram"]
                },
            },
        },
        "coordinates-nominal": { # lexicographically-ordered, also below if same var_types
            # "general-general": [], # @TODO: [scatter] coord (x), score (y), nominal (color), ngram (filter)
        },
        "coordinates-ordinal": { # lexicographically-ordered, also below if same var_types
            # "general-general": [], # @TODO: [scatter] coord (x), score (y), ordinal (color), ngram (filter)
            # "general-temporal": [], # @TODO: [line] time (x), coord (y), score (size), ngram (filter) + @FUTURE: heatmap or similar?
        },
        "coordinates-quantitative": { # lexicographically-ordered, also below if same var_types
            # "general-general": [], # @TODO: [scatter] coord (x), quant (y), score (size), ngram (filter) + @FUTURE: heatmap or similar?
        },
        "nominal-nominal": { # lexicographically-ordered, also below if same var_types
            # "general-general": [], # @TODO: [heatmap] nom (x), nom (y), score (color), ngram (filter)
            # "general-spatial": [], # @TODO: [chroplet] spatial (xy), score (color), general (filter), ngram (filter)
        },
        "nominal-ordinal": { # lexicographically-ordered, also below if same var_types
            # "general-general": [], # @TODO: [heatmap] nom (x), nom (y), score (color), ngram (filter)
            # "general-temporal": [], # @TODO: [line] time (x), score (y), nom (shape), ngram (filter)
            # "spatial-general": [], # @TODO: [chroplet] spatial (xy), score (color), general (filter), ngram (filter)
            "spatial-temporal": {
                ChoroplethChart: {
                    "color": 0,
                    "dropdown": ["ngram", "temporal"],
                    "search": []
                },
            }, # @TODO: [chroplet] spatial (xy), score (color), temporal (filter), ngram (filter)
        },
        "nominal-quantitative": { # lexicographically-ordered, also below if same var_types
            # "general-general": [], # @TODO: [scatter] quant (x), score (y), nom (color), ngram (filter) + @FUTURE: heatmap or similar?
            # "spatial-general": [], # @TODO: [chroplet] spatial (xy), score (color), ~quant (filter), ngram (filter)
        },
        "ordinal-ordinal": { # lexicographically-ordered, also below if same var_types
            # "general-general": [], # @TODO: [heatmap] ord (x), ord (y), score (color), ngram (filter)
            # "general-temporal": [], # @TODO: [line] time (x), score (y), ord (~shape), ngram (filter)
        },
        "ordinal-quantitative": { # lexicographically-ordered, also below if same var_types
            # "general-general": [], # @TODO: [scatter] quant (x), score (y), ordinal (color), ngram (filter)
            # "temporal-general": [], # @TODO: [line] time (x), quant (y), score (size), ngram (filter) + @FUTURE: heatmap or similar?
        },
        "quantitative-quantitative": { # lexicographically-ordered, also below if same var_types
            # "general-general": [], # @TODO: [scatter] quant (x), quant (y), score (size), ngram (filter) + @FUTURE: heatmap or similar?
        },
    },
    "5-dims": {
        "coordinates-coordinates-nominal": { # lexicographically-ordered, also below if same var_types
            # "general-general-general": [], # @TODO: [scatter] coord (x), coord (y), nom (filter), ngram (filter) + @FUTURE: add density plot
            # "general-general-spatial": [], # @TODO: [scatter] coord (x), coord (y), nom (filter), ngram (filter) + @FUTURE: add density plot
            # "spatial-spatial-general": [], # @TODO: [scatter] coord (x), coord (y), nom (filter), ngram (filter) + @FUTURE: add density plot
        },
        "coordinates-coordinates-ordinal": { # lexicographically-ordered, also below if same var_types
            # "general-general-general": [], # @TODO: [scatter] coord (x), coord (y), ordinal (filter), ngram (filter) + @FUTURE: add density plot
            "general-general-temporal": {
                ScatterGeoChart: {
                    "lat": 0,
                    "lon": 1,
                    "color": "value",
                    "dropdown": [],
                    "search": ["ngram", 2]
                }
            }, # @TODO: [scatter] coord (x), coord (y), ordinal (filter), ngram (filter) + @FUTURE: add density plot
            # "spatial-spatial-general": [], # @TODO: [scatter] coord (x), coord (y), ordinal (filter), ngram (filter) + @FUTURE: add density plot
            # "spatial-spatial-temporal": [], # @TODO: [scatter] coord (x), coord (y), ordinal (filter), ngram (filter) + @FUTURE: add density plot
        },
    },
}