# Input dataset

An input dataset can be defined through the **`dataset`** parameter of the `Inspector` class. 🕵️‍♀️ Variationist currently supports the following:

- A local filepath to tab-separated (`.tsv`) or comme-separated (`.csv`) file
- Pre-computed [pandas](https://pandas.pydata.org/) dataframes
- Any dataset from the 🤗 [Hugging Face datasets](https://huggingface.co/datasets) repository

Note that Hugging Face datasets are often characterized by *subsets* and *splits*. For importing datasets from this repository, we therefore require a string following the format `hf::$DATASET_NAME::$SUBSET::$SPLIT`, where:

- `$DATASET_NAME`: the name of the dataset as indicated in the Hugging Face datasets repository
- `$SUBSET`: the subset of the dataset as indicated in the Hugging Face datasets repository
- `$SPLIT`: the data split of the dataset as indicated in the Hugging Face datasets repository
