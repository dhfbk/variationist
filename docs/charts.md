# Charts

The visual components of 🕵️‍♀️ **Variationist**. It orchestrates the automatic creation of interactive charts based on the combination of [variable types and semantics](https://github.com/dhfbk/variationist/tree/main/docs/variables.md) from a previous analysis. It defines the optimal dimension or channel (e.g., `x`, `y`, `color`, `size`, `lat`, `lon`, or a dropdown component) for each variable, creating charts with up to 5 dimensions (of which one is reserved for the *quantitative* metric score, and the other to the *nominal* language unit). 

Possible charts currently include the following:
- **Heatmaps**, denoted with the name `HeatmapChart`
- **Temporal line charts**, denoted with the name `TemporalLineChart`
- **Choropleth charts**, denoted with the name `ChoroplethChart`
- **Geographic scatterplots**, denoted with the name `ScatterGeoChart`
- **Standard scatterplots**, denoted with the name `ScatterChart`
- **bar charts**, denoted with the name `BarChart`

For each metric, one or more charts are created (e.g., in the case of *nominal* variable types with *spatial* semantics, both a `BarChart` and a `ScatterGeoChart` are created. Charts can be interactively filtered by language unit through a search input field supporting regular expressions or dropdown menus to smoothly explore unit-variables associations.