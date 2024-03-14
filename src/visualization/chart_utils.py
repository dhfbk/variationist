from src.visualization.bar_chart import BarChart
from src.visualization.choropleth_chart import ChoroplethChart
from src.visualization.heatmap_chart import HeatmapChart
from src.visualization.scatter_chart import ScatterChart
from src.visualization.scatter_geo_chart import ScatterGeoChart
from src.visualization.temporal_line_chart import TemporalLineChart
# from src.visualization.density_geo_chart import DensityGeoChart


# Definition of variable types and semantics and their mapping to charts, including
# how single variables should be presented and filtered. Note: var_types for > 3 
# dimensions are lexicographically-ordered, and var_semantics are ordered accordingly
VAR_CHARTS_MAP = {
    "3-dims": {
        "coordinates": {
            "general": {
                ScatterChart: {
                    "x": (0, "quantitative"),
                    "y": ("value", "quantitative"),
                    "dropdown": [],
                    "search": [("ngram", "nominal")]
                },
            },
        },
        "nominal": {
            "general": {
                BarChart: {
                    "x": ("value", "quantitative"),
                    "y": ("ngram", "nominal"),
                    "column": (0, "nominal"),
                    "color": (0, "nominal"),
                    "dropdown": [],
                    "search": [("ngram", "nominal")]
                },
            },
            "spatial": {
                BarChart: {
                    "x": ("value", "quantitative"),
                    "y": ("ngram", "nominal"),
                    "column": (0, "nominal"),
                    "color": (0, "nominal"),
                    "dropdown": [],
                    "search": [("ngram", "nominal")]
                },
                ChoroplethChart: {
                    "color": (0, "nominal"),
                    "dropdown": [("ngram", "nominal")],
                    "search": []
                },
            },
        },
        "ordinal": {
            "general": {
                BarChart: {
                    "x": ("value", "quantitative"),
                    "y": ("ngram", "nominal"),
                    "column": (0, "nominal"),
                    "color": (0, "nominal"),
                    "dropdown": [],
                    "search": [("ngram", "nominal")]
                },
            },
            "temporal": {
                TemporalLineChart: {
                    "x": (0, "temporal"),
                    "y": ("value", "quantitative"),
                    "dropdown": [],
                    "search": [("ngram", "nominal")]
                },
            },
        },
        "quantitative": {
            "general": {
                ScatterChart: {
                    "x": (0, "quantitative"),
                    "y": ("value", "quantitative"),
                    "dropdown": [],
                    "search": [("ngram", "nominal")]
                },
            },
        },
    },
    "4-dims": {
        "coordinates-coordinates": {
            "general-general": {
                ScatterChart: {
                    "x": (0, "quantitative"),
                    "y": (1, "quantitative"),
                    "color": ("ngram", "nominal"),
                    "opacity": ("value", "quantitative"),
                    "dropdown": [("ngram", "nominal")],
                    "search": []
                },
            },
            "spatial-spatial": {
                ScatterGeoChart: {
                    "lat": (0, "quantitative"),
                    "lon": (1, "quantitative"),
                    "color": ("value", "quantitative"),
                    "dropdown": [("ngram", "nominal")],
                    "search": []
                },
                # DensityGeoChart: {
                #     "lat": (0, "quantitative"),
                #     "lon": (1, "quantitative"),
                #     "color": ("value", "quantitative"),
                #     "dropdown": [],
                #     "search": [("ngram", "nominal")]
                # },
            },
        },
        "coordinates-nominal": {
            "general-general": {
                ScatterChart: {
                    "x": (0, "quantitative"),
                    "y": ("value", "quantitative"),
                    "color": ("ngram", "nominal"),
                    "extra": (1, "nominal"),
                    "dropdown": [("ngram", "nominal"), (1, "nominal")],
                    "search": []
                },
            },
        },
        "coordinates-ordinal": {
            "general-general": {
                ScatterChart: {
                    "x": (0, "quantitative"),
                    "y": ("value", "quantitative"),
                    "color": ("ngram", "nominal"),
                    "extra": (1, "nominal"),
                    "dropdown": [("ngram", "nominal"), (1, "nominal")],
                    "search": []
                },
            },
            # "general-temporal": [], # @TODO: [line] time (x), coord (y), score (size), ngram (filter) + @FUTURE: heatmap or similar?
        },
        "coordinates-quantitative": {
            "general-general": {
                ScatterChart: {
                    "x": (0, "quantitative"),
                    "y": (1, "quantitative"),
                    "color": ("ngram", "nominal"),
                    "opacity": ("value", "quantitative"),
                    "dropdown": [("ngram", "nominal")],
                    "search": []
                },
            },
        },
        "nominal-nominal": {
            "general-general": {
                HeatmapChart: {
                    "x": (0, "nominal"),
                    "y": (1, "nominal"),
                    "color": ("value", "quantitative"),
                    "dropdown": [("ngram", "nominal")],
                    "search": []
                },
            },
            # "general-spatial": [], # @TODO: [chroplet] spatial (xy), score (color), general (filter), ngram (filter)
        },
        "nominal-ordinal": {
            "general-general": {
                HeatmapChart: {
                    "x": (0, "nominal"),
                    "y": (1, "ordinal"),
                    "color": ("value", "quantitative"),
                    "dropdown": [("ngram", "nominal")],
                    "search": []
                },
            },
            # "general-temporal": [], # @TODO: [line] time (x), score (y), nom (shape), ngram (filter)
            "spatial-general": {
                ChoroplethChart: {
                    "color": (0, "nominal"),
                    "dropdown": [("ngram", "nominal"), (1, "ordinal")],
                    "search": []
                },
            },
            "spatial-temporal": {
                ChoroplethChart: {
                    "color": (0, "nominal"),
                    "dropdown": [("ngram", "nominal"), (1, "temporal")],
                    "search": []
                },
            },
        },
        "nominal-quantitative": {
            "general-general": {
                ScatterChart: {
                    "x": (1, "quantitative"),
                    "y": ("value", "quantitative"),
                    "color": ("ngram", "nominal"),
                    "extra": (0, "nominal"),
                    "dropdown": [("ngram", "nominal"), (0, "nominal")],
                    "search": []
                },
            },
            # "spatial-general": [], # @TODO: [chroplet] spatial (xy), score (color), ~quant (filter), ngram (filter)
        },
        "ordinal-ordinal": {
            "general-general": {
                HeatmapChart: {
                    "x": (0, "ordinal"),
                    "y": (1, "ordinal"),
                    "color": ("value", "quantitative"),
                    "dropdown": [("ngram", "nominal")],
                    "search": []
                },
            },
            # "general-temporal": [], # @TODO: [line] time (x), score (y), ord (~shape), ngram (filter)
        },
        "ordinal-quantitative": {
            "general-general": {
                ScatterChart: {
                    "x": (1, "quantitative"),
                    "y": ("value", "quantitative"),
                    "color": ("ngram", "nominal"),
                    "extra": (0, "nominal"),
                    "dropdown": [("ngram", "nominal"), (0, "nominal")],
                    "search": []
                },
            },
            # "temporal-general": [], # @TODO: [line] time (x), quant (y), score (size), ngram (filter) + @FUTURE: heatmap or similar?
        },
        "quantitative-quantitative": {
            "general-general": {
                ScatterChart: {
                    "x": (0, "quantitative"),
                    "y": (1, "quantitative"),
                    "color": ("ngram", "nominal"),
                    "opacity": ("value", "quantitative"),
                    "dropdown": [("ngram", "nominal")],
                    "search": []
                },
            },
        },
    },
    "5-dims": {
        "coordinates-coordinates-nominal": {
            # "general-general-general": [], # @TODO: [scatter] coord (x), coord (y), nom (filter), ngram (filter) + @FUTURE: add density plot
            # "general-general-spatial": [], # @TODO: [scatter] coord (x), coord (y), nom (filter), ngram (filter) + @FUTURE: add density plot
            # "spatial-spatial-general": [], # @TODO: [scatter] coord (x), coord (y), nom (filter), ngram (filter) + @FUTURE: add density plot
        },
        "coordinates-coordinates-ordinal": {
            # "general-general-general": [], # @TODO: [scatter] coord (x), coord (y), ordinal (filter), ngram (filter) + @FUTURE: add density plot
            "general-general-temporal": {
                ScatterGeoChart: {
                    "lat": (0, "quantitative"),
                    "lon": (1, "quantitative"),
                    "color": ("value", "quantitative"),
                    "dropdown": [],
                    "search": [("ngram", "nominal"), (2, "ordinal")]
                }
            }, # @TODO: [scatter] coord (x), coord (y), ordinal (filter), ngram (filter) + @FUTURE: add density plot
            # "spatial-spatial-general": [], # @TODO: [scatter] coord (x), coord (y), ordinal (filter), ngram (filter) + @FUTURE: add density plot
            # "spatial-spatial-temporal": [], # @TODO: [scatter] coord (x), coord (y), ordinal (filter), ngram (filter) + @FUTURE: add density plot
        },
    },
}