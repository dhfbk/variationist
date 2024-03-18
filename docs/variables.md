# Variables

Variables are essential components for computing association metrics with language units. While variables in NLP typically translate to human-annotated "labels", those may be naturally generalized to any kind of meta-information associated to textual data (e.g., genres, datetimes, spatial information, socio-demographic characteristics of authors, amongst others).

🕵️‍♀️ Variationist natively supports a potentially unlimited number of variable combinations during analysis. Due to the variety of data types and semantic meanings that variables may take, each variable (i.e., column name) is defined through the following triplet:

- `var_names` (**variable names**}: a list of variable names to use for the analysis. Each string should correspond to an [input dataset](https://github.com/dhfbk/variationist/tree/main/docs/input-dataset.md) column
- `var_types` (**variable types**}: a list of the types of the variables for representation purposes. They can be either *nominal* (i.e., categorical variables without an intrinsic ordering/ranking), *ordinal* (variablea that can be ordered/ranked), *quantitative* (numerical variablea - either discrete or continuous - which may take any value), or *coordinates* (positiona of a point on the Earth surface, i.e., latitude or longitude)
- `var_semantics` (**variable semantics**}: a list of strings denoting how the variable must be interpreted for visualization purposes. They may be either *temporal* (e.g., variables such as dates or times), *spatial* (e.g., either *coordinates* variables or *nominal* variables with spatial semantics such as countries, states, or provinces), or *general* (any variable that does not fall in the aforementioned semantics)

Please note that each variable should take the same index in the lists `var_names`, `var_types`, and `var_semantics`.