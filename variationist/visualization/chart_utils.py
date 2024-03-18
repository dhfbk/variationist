from variationist.visualization.bar_chart import BarChart
from variationist.visualization.choropleth_chart import ChoroplethChart
from variationist.visualization.heatmap_chart import HeatmapChart
from variationist.visualization.scatter_chart import ScatterChart
from variationist.visualization.scatter_geo_chart import ScatterGeoChart
from variationist.visualization.temporal_line_chart import TemporalLineChart
# from variationist.visualization.density_geo_chart import DensityGeoChart


# Definition of variable types and semantics and their mapping to charts, including how single
# variables should be presented and filtered. Note: var_types in charts with more than three
# dimensions are lexicographically-ordered, and the var_semantics are ordered accordingly.

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
            "general-temporal": {
                TemporalLineChart: {
                    "x": (1, "temporal"),
                    "y": (0, "quantitative"),
                    "color": ("ngram", "nominal"),
                    "size": ("value", "quantitative"),
                    "dropdown": [("ngram", "nominal")],
                    "search": []
                },
            }
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
            "general-spatial": {
                ChoroplethChart: {
                    "color": (1, "nominal"),
                    "dropdown": [("ngram", "nominal"), (0, "nominal")],
                    "search": []
                },
            },
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
            "general-temporal": {
                TemporalLineChart: {
                    "x": (1, "temporal"),
                    "y": ("value", "quantitative"),
                    "color": ("ngram", "nominal"),
                    "shape": (0, "nominal"),
                    "dropdown": [("ngram", "nominal")],
                    "search": []
                },
            },
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
            "spatial-general": {
                ChoroplethChart: {
                    "color": (0, "nominal"),
                    "dropdown": [("ngram", "nominal"), (1, "nominal")],
                    "search": []
                },
            },
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
            "general-temporal": {
                TemporalLineChart: {
                    "x": (1, "temporal"),
                    "y": ("value", "quantitative"),
                    "color": ("ngram", "nominal"),
                    "shape": (0, "nominal"),
                    "dropdown": [("ngram", "nominal")],
                    "search": []
                },
            },
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
            "temporal-general": {
                TemporalLineChart: {
                    "x": (0, "temporal"),
                    "y": (1, "quantitative"),
                    "color": ("ngram", "nominal"),
                    "size": ("value", "quantitative"),
                    "dropdown": [("ngram", "nominal")],
                    "search": []
                },
            },
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
            "general-general-general": {
                ScatterChart: {
                    "x": (0, "quantitative"),
                    "y": (1, "quantitative"),
                    "color": ("ngram", "nominal"),
                    "opacity": ("value", "quantitative"),
                    "dropdown": [("ngram", "nominal"), (2, "nominal")],
                    "search": []
                },
            },
            "spatial-spatial-general": {
                ScatterGeoChart: {
                    "lat": (0, "quantitative"),
                    "lon": (1, "quantitative"),
                    "color": ("value", "quantitative"),
                    "dropdown": [("ngram", "nominal"), (2, "nominal")],
                    "search": []
                },
            },
        },
        "coordinates-coordinates-ordinal": {
            "general-general-general": {
                ScatterChart: {
                    "x": (0, "quantitative"),
                    "y": (1, "quantitative"),
                    "color": ("ngram", "nominal"),
                    "opacity": ("value", "quantitative"),
                    "dropdown": [("ngram", "nominal"), (2, "ordinal")],
                    "search": []
                },
            },
            "general-general-temporal": {
                ScatterChart: {
                    "x": (0, "quantitative"),
                    "y": (1, "quantitative"),
                    "color": ("ngram", "nominal"),
                    "opacity": ("value", "quantitative"),
                    "dropdown": [("ngram", "nominal"), (2, "temporal")],
                    "search": []
                },
            },
            "spatial-spatial-general": {
                ScatterGeoChart: {
                    "lat": (0, "quantitative"),
                    "lon": (1, "quantitative"),
                    "color": ("value", "quantitative"),
                    "dropdown": [("ngram", "nominal"), (2, "ordinal")],
                    "search": []
                },
            },
            "spatial-spatial-temporal": {
                ScatterGeoChart: {
                    "lat": (0, "quantitative"),
                    "lon": (1, "quantitative"),
                    "color": ("value", "quantitative"),
                    "dropdown": [("ngram", "nominal"), (2, "temporal")],
                    "search": []
                },
            },
        },
    },
}