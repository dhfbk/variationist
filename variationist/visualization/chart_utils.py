from variationist.visualization.bar_chart import BarChart
from variationist.visualization.binned_geo_chart import BinnedGeoChart
from variationist.visualization.choropleth_chart import ChoroplethChart
from variationist.visualization.heatmap_chart import HeatmapChart
from variationist.visualization.line_chart import LineChart
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
                    "search": [("ngram", "nominal")],
                    "for_bins": False
                },
                BarChart: {
                    "x": ("value", "quantitative"),
                    "y": ("ngram", "nominal"),
                    "column": (0, "nominal"),
                    "color": (0, "nominal"),
                    "dropdown": [],
                    "search": [("ngram", "nominal")],
                    "for_bins": True
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
                    "search": [("ngram", "nominal")],
                    "for_bins": False
                },
            },
            "spatial": {
                BarChart: {
                    "x": ("value", "quantitative"),
                    "y": ("ngram", "nominal"),
                    "column": (0, "nominal"),
                    "color": (0, "nominal"),
                    "dropdown": [],
                    "search": [("ngram", "nominal")],
                    "for_bins": False
                },
                ChoroplethChart: {
                    "color": (0, "nominal"),
                    "dropdown": [("ngram", "nominal")],
                    "search": [],
                    "for_bins": False
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
                    "search": [("ngram", "nominal")],
                    "for_bins": False
                },
            },
            "temporal": {
                TemporalLineChart: {
                    "x": (0, "temporal"),
                    "y": ("value", "quantitative"),
                    "dropdown": [],
                    "search": [("ngram", "nominal")],
                    "for_bins": False
                },
                LineChart: {
                    "x": (0, "nominal"),
                    "y": ("value", "quantitative"),
                    "dropdown": [],
                    "search": [("ngram", "nominal")],
                    "for_bins": True
                },
            },
        },
        "quantitative": {
            "general": {
                ScatterChart: {
                    "x": (0, "quantitative"),
                    "y": ("value", "quantitative"),
                    "dropdown": [],
                    "search": [("ngram", "nominal")],
                    "for_bins": "any"
                }
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
                    "search": [],
                    "for_bins": False
                },
                HeatmapChart: {
                    "x": (0, "nominal"),
                    "y": (1, "nominal"),
                    "color": ("value", "quantitative"),
                    "dropdown": [("ngram", "nominal")],
                    "search": [],
                    "for_bins": True
                },
            },
            "spatial-spatial": {
                ScatterGeoChart: {
                    "lat": (0, "quantitative"),
                    "lon": (1, "quantitative"),
                    "color": ("value", "quantitative"),
                    "dropdown": [("ngram", "nominal")],
                    "search": [],
                    "for_bins": False
                },
                BinnedGeoChart: {
                    "lat": (0, "quantitative"),
                    "lon": (1, "quantitative"),
                    "color": ("value", "quantitative"),
                    "dropdown": [("ngram", "nominal")],
                    "search": [],
                    "for_bins": True
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
                    "search": [],
                    "for_bins": False
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
                    "search": [],
                    "for_bins": False
                },
            },
            "general-temporal": {
                TemporalLineChart: {
                    "x": (1, "temporal"),
                    "y": (0, "quantitative"),
                    "color": ("ngram", "nominal"),
                    "size": ("value", "quantitative"),
                    "dropdown": [("ngram", "nominal")],
                    "search": [],
                    "for_bins": False
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
                    "search": [],
                    "for_bins": False
                },
                HeatmapChart: {
                    "x": (0, "nominal"),
                    "y": (1, "nominal"),
                    "color": ("value", "quantitative"),
                    "dropdown": [("ngram", "nominal")],
                    "search": [],
                    "for_bins": True
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
                    "search": [],
                    "for_bins": "any" # @TODO: Adapt this to others, too
                },
            },
            "general-spatial": {
                ChoroplethChart: {
                    "color": (1, "nominal"),
                    "dropdown": [("ngram", "nominal"), (0, "nominal")],
                    "search": [],
                    "for_bins": False
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
                    "search": [],
                    "for_bins": False
                },
            },
            "general-temporal": {
                TemporalLineChart: {
                    "x": (1, "temporal"),
                    "y": ("value", "quantitative"),
                    "color": ("ngram", "nominal"),
                    "shape": (0, "nominal"),
                    "dropdown": [("ngram", "nominal")],
                    "search": [],
                    "for_bins": False
                },
            },
            "spatial-general": {
                ChoroplethChart: {
                    "color": (0, "nominal"),
                    "dropdown": [("ngram", "nominal"), (1, "ordinal")],
                    "search": [],
                    "for_bins": False
                },
            },
            "spatial-temporal": {
                ChoroplethChart: {
                    "color": (0, "nominal"),
                    "dropdown": [("ngram", "nominal"), (1, "temporal")],
                    "search": [],
                    "for_bins": False
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
                    "search": [],
                    "for_bins": False
                },
            },
            "spatial-general": {
                ChoroplethChart: {
                    "color": (0, "nominal"),
                    "dropdown": [("ngram", "nominal"), (1, "nominal")],
                    "search": [],
                    "for_bins": False
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
                    "search": [],
                    "for_bins": False
                },
            },
            "general-temporal": {
                TemporalLineChart: {
                    "x": (1, "temporal"),
                    "y": ("value", "quantitative"),
                    "color": ("ngram", "nominal"),
                    "shape": (0, "nominal"),
                    "dropdown": [("ngram", "nominal")],
                    "search": [],
                    "for_bins": False
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
                    "search": [],
                    "for_bins": False
                },
            },
            "temporal-general": {
                TemporalLineChart: {
                    "x": (0, "temporal"),
                    "y": (1, "quantitative"),
                    "color": ("ngram", "nominal"),
                    "size": ("value", "quantitative"),
                    "dropdown": [("ngram", "nominal")],
                    "search": [],
                    "for_bins": False
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
                    "search": [],
                    "for_bins": False
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
                    "search": [],
                    "for_bins": False
                },
            },
            "spatial-spatial-general": {
                ScatterGeoChart: {
                    "lat": (0, "quantitative"),
                    "lon": (1, "quantitative"),
                    "color": ("value", "quantitative"),
                    "dropdown": [("ngram", "nominal"), (2, "nominal")],
                    "search": [],
                    "for_bins": False
                },
                BinnedGeoChart: {
                    "lat": (0, "quantitative"),
                    "lon": (1, "quantitative"),
                    "color": ("value", "quantitative"),
                    "dropdown": [("ngram", "nominal"), (2, "nominal")],
                    "search": [],
                    "for_bins": True
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
                    "search": [],
                    "for_bins": False
                },
            },
            "general-general-temporal": {
                ScatterChart: {
                    "x": (0, "quantitative"),
                    "y": (1, "quantitative"),
                    "color": ("ngram", "nominal"),
                    "opacity": ("value", "quantitative"),
                    "dropdown": [("ngram", "nominal"), (2, "temporal")],
                    "search": [],
                    "for_bins": False
                },
            },
            "spatial-spatial-general": {
                ScatterGeoChart: {
                    "lat": (0, "quantitative"),
                    "lon": (1, "quantitative"),
                    "color": ("value", "quantitative"),
                    "dropdown": [("ngram", "nominal"), (2, "ordinal")],
                    "search": [],
                    "for_bins": False
                },
                BinnedGeoChart: {
                    "lat": (0, "quantitative"),
                    "lon": (1, "quantitative"),
                    "color": ("value", "quantitative"),
                    "dropdown": [("ngram", "nominal"), (2, "ordinal")],
                    "search": [],
                    "for_bins": True
                },
            },
            "spatial-spatial-temporal": {
                ScatterGeoChart: {
                    "lat": (0, "quantitative"),
                    "lon": (1, "quantitative"),
                    "color": ("value", "quantitative"),
                    "dropdown": [("ngram", "nominal"), (2, "temporal")],
                    "search": [],
                    "for_bins": False
                },
                BinnedGeoChart: {
                    "lat": (0, "quantitative"),
                    "lon": (1, "quantitative"),
                    "color": ("value", "quantitative"),
                    "dropdown": [("ngram", "nominal"), (2, "temporal")],
                    "search": [],
                    "for_bins": True
                },
            },
        },
    },
}